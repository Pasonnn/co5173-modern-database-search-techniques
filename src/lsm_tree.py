"""Log-Structured Merge-Tree (LSM-Tree) modeling RocksDB / Cassandra."""
from __future__ import annotations
import bisect
import hashlib
from dataclasses import dataclass, field
from typing import Any
from src.common import OperationStats, estimate_object_memory


TOMBSTONE = object()


class BloomFilter:
    """Bit-array Bloom Filter for fast negative membership testing."""

    def __init__(self, size_bits: int = 256, hash_count: int = 3):
        self.size = size_bits
        self.hash_count = hash_count
        self.bits = [0] * size_bits

    def _hashes(self, key: int) -> list[int]:
        # Fast double-hashing (Kirsch-Mitzenmacher technique used in Cassandra & Guava)
        h1 = hash((key, 0x9E3779B9))
        h2 = hash((key, 0x85EBCA6B)) | 1
        return [abs(h1 + i * h2) % self.size for i in range(self.hash_count)]

    def add(self, key: int) -> None:
        for bit_idx in self._hashes(key):
            self.bits[bit_idx] = 1

    def contains(self, key: int) -> bool:
        return all(self.bits[bit_idx] == 1 for bit_idx in self._hashes(key))


@dataclass
class SSTable:
    """Immutable Sorted String Table with sparse fence index and bloom filter."""
    keys: list[int]
    values: list[Any]
    bloom: BloomFilter
    fence_keys: list[int] = field(init=False)
    fence_indices: list[int] = field(init=False)

    def __post_init__(self):
        # Sparse index every 16 items (similar to block fence pointers)
        step = max(1, len(self.keys) // 8)
        self.fence_keys = self.keys[::step]
        self.fence_indices = list(range(0, len(self.keys), step))

    def get(self, key: int) -> tuple[bool, Any | None]:
        if not self.bloom.contains(key):
            return False, None

        # Binary search sparse fence pointers to isolate block range
        f_idx = bisect.bisect_right(self.fence_keys, key) - 1
        start = self.fence_indices[max(0, f_idx)]
        end = (
            self.fence_indices[f_idx + 1]
            if f_idx + 1 < len(self.fence_indices)
            else len(self.keys)
        )

        sub_keys = self.keys[start:end]
        idx = bisect.bisect_left(sub_keys, key)
        if idx < len(sub_keys) and sub_keys[idx] == key:
            val = self.values[start + idx]
            return True, (None if val is TOMBSTONE else val)
        return False, None


class LSMTree:
    """Log-Structured Merge-Tree with MemTable, immutable SSTables, and compaction.
    
    ponytail: In-memory list SSTables over POSIX file appends; upgrade when measuring direct I/O sync latency and OS page cache pollution.
    """

    def __init__(self, memtable_threshold: int = 32, compaction_trigger: int = 4):
        self.memtable_threshold = memtable_threshold
        self.compaction_trigger = compaction_trigger
        self.memtable: dict[int, Any] = {}
        self.sstables: list[SSTable] = []  # Newest to oldest
        self.stats = OperationStats()

    def put(self, key: int, value: Any) -> None:
        self.memtable[key] = value
        self.stats.pages_written += 1
        if len(self.memtable) >= self.memtable_threshold:
            self._flush_memtable()

    def delete(self, key: int) -> None:
        self.put(key, TOMBSTONE)

    def _flush_memtable(self) -> None:
        if not self.memtable:
            return
        sorted_keys = sorted(self.memtable.keys())
        sorted_values = [self.memtable[k] for k in sorted_keys]

        bf = BloomFilter(size_bits=max(128, len(sorted_keys) * 10))
        for k in sorted_keys:
            bf.add(k)

        sstable = SSTable(keys=sorted_keys, values=sorted_values, bloom=bf)
        self.sstables.insert(0, sstable)
        self.memtable.clear()

        if len(self.sstables) >= self.compaction_trigger:
            self.compact()

    def compact(self) -> None:
        """Merge all SSTables into a single compacted SSTable (Major Compaction)."""
        if not self.sstables:
            return
        merged: dict[int, Any] = {}
        # Merge oldest to newest so newest values overwrite older ones
        for sst in reversed(self.sstables):
            for k, v in zip(sst.keys, sst.values):
                merged[k] = v

        # Filter out tombstones on major compaction
        compacted_keys = [k for k, v in sorted(merged.items()) if v is not TOMBSTONE]
        compacted_values = [merged[k] for k in compacted_keys]

        bf = BloomFilter(size_bits=max(128, len(compacted_keys) * 10))
        for k in compacted_keys:
            bf.add(k)

        self.sstables = [SSTable(keys=compacted_keys, values=compacted_values, bloom=bf)]
        self.stats.pages_written += len(compacted_keys)

    def get(self, key: int) -> Any | None:
        # 1. Check active MemTable
        if key in self.memtable:
            val = self.memtable[key]
            return None if val is TOMBSTONE else val

        # 2. Check immutable SSTables (newest to oldest)
        for sst in self.sstables:
            self.stats.pages_read += 1
            found, val = sst.get(key)
            if found:
                return val
        return None

    def scan(self, start_key: int, end_key: int) -> list[tuple[int, Any]]:
        # Multi-way merge across memtable and all SSTables
        merged: dict[int, Any] = {}
        for sst in reversed(self.sstables):
            for k, v in zip(sst.keys, sst.values):
                if start_key <= k <= end_key:
                    merged[k] = v

        for k, v in self.memtable.items():
            if start_key <= k <= end_key:
                merged[k] = v

        return [(k, v) for k, v in sorted(merged.items()) if v is not TOMBSTONE]

    def memory_footprint_bytes(self) -> int:
        return estimate_object_memory(self.memtable) + estimate_object_memory(self.sstables)
