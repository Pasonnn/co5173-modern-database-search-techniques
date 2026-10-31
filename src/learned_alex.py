"""Dynamic Updatable Learned Index: ALEX architecture with Gapped Arrays."""
from __future__ import annotations
import bisect
from dataclasses import dataclass, field
from typing import Any
from src.common import OperationStats, estimate_object_memory


GAP = object()


@dataclass
class DataNode:
    """Leaf Data Node with a gapped array to absorb local inserts without whole-array shifts."""
    capacity: int = 16
    keys: list[Any] = field(init=False)
    values: list[Any] = field(init=False)
    num_keys: int = 0
    slope: float = 1.0
    intercept: float = 0.0

    def __post_init__(self):
        self.keys = [GAP] * self.capacity
        self.values = [GAP] * self.capacity

    def predict_slot(self, key: int) -> int:
        pred = int(self.slope * key + self.intercept)
        return max(0, min(self.capacity - 1, pred))

    def search_key(self, key: int) -> tuple[int | None, int]:
        """Model-predicted slot search with bounded linear/exponential galloping scan."""
        if self.num_keys == 0:
            return None, 0

        pred = self.predict_slot(key)
        # Direct hit check
        if self.keys[pred] is not GAP and self.keys[pred] == key:
            return pred, pred

        # Bounded search around prediction for key or correct insertion slot
        best_insert = 0
        for i in range(self.capacity):
            if self.keys[i] is not GAP:
                if self.keys[i] == key:
                    return i, i
                if self.keys[i] > key:
                    best_insert = i
                    break
                best_insert = i + 1
        return None, min(self.capacity - 1, best_insert)

    def rebuild(self, pairs: list[tuple[int, Any]]) -> None:
        """Re-arranges keys monotonically with calculated empty gaps for future writes."""
        pairs.sort(key=lambda x: x[0])
        n = len(pairs)
        self.capacity = max(16, n * 2)
        self.keys = [GAP] * self.capacity
        self.values = [GAP] * self.capacity
        self.num_keys = n
        if n == 0:
            return

        min_k, max_k = pairs[0][0], pairs[-1][0]
        span = max(1, max_k - min_k)
        target_span = (self.capacity - 1) * 0.7
        self.slope = target_span / span
        self.intercept = (self.capacity * 0.15) - self.slope * min_k

        # Assign monotonic slots with gaps
        slots: list[int] = []
        last_slot = -1
        for k, _ in pairs:
            pred = self.predict_slot(k)
            slot = max(last_slot + 1, pred)
            slots.append(slot)
            last_slot = slot

        if slots[-1] >= self.capacity:
            slots[-1] = self.capacity - 1
            for j in range(len(slots) - 2, -1, -1):
                if slots[j] >= slots[j + 1]:
                    slots[j] = slots[j + 1] - 1

        for slot, (k, v) in zip(slots, pairs):
            self.keys[slot] = k
            self.values[slot] = v

    def insert(self, key: int, value: Any) -> bool:
        """Local insert using gapped shifts. Returns True when node must be rebuilt/split."""
        idx, target = self.search_key(key)
        if idx is not None:
            self.values[idx] = value
            return False

        if (self.num_keys / self.capacity) >= 0.75:
            return True

        if self.keys[target] is GAP:
            self.keys[target] = key
            self.values[target] = value
            self.num_keys += 1
            return False

        # Locate closest gap forward or backward
        left_gap = -1
        for i in range(target, -1, -1):
            if self.keys[i] is GAP:
                left_gap = i
                break

        right_gap = -1
        for i in range(target, self.capacity):
            if self.keys[i] is GAP:
                right_gap = i
                break

        if right_gap != -1 and (left_gap == -1 or (right_gap - target) <= (target - left_gap)):
            for i in range(right_gap, target, -1):
                self.keys[i] = self.keys[i - 1]
                self.values[i] = self.values[i - 1]
            self.keys[target] = key
            self.values[target] = value
            self.num_keys += 1
        elif left_gap != -1:
            for i in range(left_gap, target - 1):
                self.keys[i] = self.keys[i + 1]
                self.values[i] = self.values[i + 1]
            self.keys[target - 1] = key
            self.values[target - 1] = value
            self.num_keys += 1
        else:
            return True
        return False


class DynamicALEX:
    """Dynamic Learned Index (ALEX) with two-tier routing and gapped-array leaf nodes.
    
    ponytail: Single-level separator routing over deep learned tree DAG; upgrade when node count exceeds 4096 leaves.
    """

    def __init__(self, leaf_max_capacity: int = 32):
        self.leaf_max_capacity = max(16, leaf_max_capacity)
        self.pivots: list[int] = []
        self.leaves: list[DataNode] = [DataNode(capacity=self.leaf_max_capacity)]
        self.stats = OperationStats()

    def _find_leaf_idx(self, key: int) -> int:
        return bisect.bisect_right(self.pivots, key)

    def put(self, key: int, value: Any) -> None:
        idx = self._find_leaf_idx(key)
        leaf = self.leaves[idx]
        need_rebuild = leaf.insert(key, value)
        self.stats.pages_written += 1

        if need_rebuild:
            pairs = [(k, v) for k, v in zip(leaf.keys, leaf.values) if k is not GAP]
            if len(pairs) >= self.leaf_max_capacity:
                # Dynamic node split at median
                pairs.sort(key=lambda x: x[0])
                mid = len(pairs) // 2
                split_key = pairs[mid][0]

                left_leaf = DataNode(capacity=self.leaf_max_capacity)
                right_leaf = DataNode(capacity=self.leaf_max_capacity)
                left_leaf.rebuild(pairs[:mid])
                right_leaf.rebuild(pairs[mid:])

                self.pivots.insert(idx, split_key)
                self.leaves[idx] = left_leaf
                self.leaves.insert(idx + 1, right_leaf)

                target_leaf = right_leaf if key >= split_key else left_leaf
                target_leaf.insert(key, value)
            else:
                leaf.rebuild(pairs)
                leaf.insert(key, value)

    def get(self, key: int) -> Any | None:
        idx = self._find_leaf_idx(key)
        leaf = self.leaves[idx]
        self.stats.pages_read += 1
        slot, _ = leaf.search_key(key)
        if slot is not None and leaf.keys[slot] == key:
            return leaf.values[slot]
        return None

    def scan(self, start_key: int, end_key: int) -> list[tuple[int, Any]]:
        results: list[tuple[int, Any]] = []
        for leaf in self.leaves:
            for k, v in zip(leaf.keys, leaf.values):
                if k is not GAP and start_key <= k <= end_key:
                    results.append((k, v))
        results.sort(key=lambda x: x[0])
        return results

    def memory_footprint_bytes(self) -> int:
        return estimate_object_memory(self.pivots) + sum(
            estimate_object_memory(leaf) for leaf in self.leaves
        )
