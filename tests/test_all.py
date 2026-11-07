"""Runnable test suite verifying Cassandra (LSM-Tree) and Elasticsearch (Inverted Index)."""
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lsm_tree import LSMTree, BloomFilter, TOMBSTONE
from src.inverted_index import InvertedIndex, tokenize


def test_bloom_filter():
    """Verify Bloom Filter behavior: zero false negatives and high true negative rate."""
    bf = BloomFilter(size_bits=256, hash_count=3)
    keys = [10, 20, 30, 40, 50]
    for k in keys:
        bf.add(k)

    # Must contain all inserted keys (zero false negatives)
    for k in keys:
        assert bf.contains(k) is True, f"False negative on key {k}"

    # Non-existent keys should predominantly return False
    absent_keys = [101, 102, 103, 104, 105, 999]
    negatives = sum(1 for k in absent_keys if not bf.contains(k))
    assert negatives >= len(absent_keys) * 0.8, "Bloom filter false positive rate unexpectedly high"


def test_cassandra_lsm_tree():
    """Verify Cassandra LSM-Tree mechanics: MemTable flush, SSTable fence index, Tombstones, Compaction."""
    lsm = LSMTree(memtable_threshold=8, compaction_trigger=3)
    data = {i: f"lsm_{i}" for i in range(50)}
    for k, v in data.items():
        lsm.put(k, v)

    # Point lookups
    for k, v in data.items():
        assert lsm.get(k) == v, f"LSM lookup failed for key {k}"
    assert lsm.get(999) is None, "Non-existent key should return None"

    # Overwrite semantics (newest entry in MemTable overrides SSTables)
    lsm.put(10, "updated_val_10")
    assert lsm.get(10) == "updated_val_10"

    # Deletion via Tombstone marker
    lsm.delete(15)
    assert lsm.get(15) is None, "Deleted key should return None"

    # Trigger Major Compaction and verify tombstone purging
    lsm.compact()
    assert lsm.get(15) is None
    assert lsm.get(16) == "lsm_16"
    assert lsm.get(10) == "updated_val_10"

    # Multi-way merge range scan across MemTable and SSTables
    scan_res = lsm.scan(30, 35)
    assert [k for k, _ in scan_res] == list(range(30, 36))

    # Memory footprint calculation returns positive integer
    assert lsm.memory_footprint_bytes() > 0


def test_elasticsearch_inverted_index():
    """Verify Elasticsearch Inverted Index: Tokenization, Posting lists, Boolean AND/OR, BM25 scoring."""
    idx = InvertedIndex(k1=1.2, b=0.75)
    idx.index_document(1, "Apache Cassandra provides high write ingestion throughput via LSM trees.", {"year": 2021, "cluster": "prod"})
    idx.index_document(2, "Elasticsearch uses inverted index and Lucene segments for text retrieval.", {"year": 2023, "cluster": "analytics"})
    idx.index_document(3, "Modern database systems balance write amplification and search latency.", {"year": 2025, "cluster": "prod"})

    # Tokenizer check
    assert tokenize("Hello, World! 123") == ["hello", "world", "123"]

    # Boolean search
    assert idx.search_boolean(["cassandra", "throughput"], mode="AND") == [1]
    assert idx.search_boolean(["elasticsearch", "cassandra"], mode="OR") == [1, 2]
    assert idx.search_boolean(["nonexistent_term"], mode="AND") == []

    # BM25 relevance scoring
    bm25_res = idx.search_bm25("elasticsearch inverted index")
    assert len(bm25_res) > 0
    assert bm25_res[0][0] == 2  # Doc 2 is top ranked

    # Attribute range filtering (simulating BKD tree / doc values)
    assert idx.range_filter("year", 2022, 2026) == [2, 3]

    # Memory footprint calculation
    assert idx.memory_footprint_bytes() > 0


if __name__ == "__main__":
    test_bloom_filter()
    test_cassandra_lsm_tree()
    test_elasticsearch_inverted_index()
    print("ALL TESTS PASSED: Apache Cassandra (LSM) & Elasticsearch (Inverted Index).")
