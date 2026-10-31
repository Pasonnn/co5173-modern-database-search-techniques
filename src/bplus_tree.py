"""B+ Tree Index implementation modeling MySQL InnoDB page-based layout."""
from __future__ import annotations
import bisect
from dataclasses import dataclass, field
from typing import Any
from src.common import OperationStats, estimate_object_memory


@dataclass
class LeafNode:
    keys: list[int] = field(default_factory=list)
    values: list[Any] = field(default_factory=list)
    next_leaf: LeafNode | None = None
    is_leaf: bool = True

    def insert(self, key: int, value: Any) -> None:
        idx = bisect.bisect_left(self.keys, key)
        if idx < len(self.keys) and self.keys[idx] == key:
            self.values[idx] = value
        else:
            self.keys.insert(idx, key)
            self.values.insert(idx, value)


@dataclass
class InternalNode:
    keys: list[int] = field(default_factory=list)
    children: list[InternalNode | LeafNode] = field(default_factory=list)
    is_leaf: bool = False


class BPlusTree:
    """B+ Tree index with configurable branching factor (order).
    
    ponytail: In-memory pointer chaining over slotted 16KB page disk serialization; upgrade when modeling direct buffer pool paging and WAL write stall.
    """

    def __init__(self, order: int = 32):
        self.order = max(3, order)
        self.root: InternalNode | LeafNode = LeafNode()
        self.stats = OperationStats()

    def get(self, key: int) -> Any | None:
        curr = self.root
        while not curr.is_leaf:
            self.stats.pages_read += 1
            idx = bisect.bisect_right(curr.keys, key)
            curr = curr.children[idx]

        self.stats.pages_read += 1
        idx = bisect.bisect_left(curr.keys, key)
        if idx < len(curr.keys) and curr.keys[idx] == key:
            return curr.values[idx]
        return None

    def put(self, key: int, value: Any) -> None:
        split_result = self._insert(self.root, key, value)
        if split_result is not None:
            promoted_key, new_child = split_result
            new_root = InternalNode(keys=[promoted_key], children=[self.root, new_child])
            self.root = new_root
            self.stats.pages_written += 1

    def _insert(
        self, node: InternalNode | LeafNode, key: int, value: Any
    ) -> tuple[int, InternalNode | LeafNode] | None:
        if node.is_leaf:
            node.insert(key, value)
            self.stats.pages_written += 1
            if len(node.keys) >= self.order:
                return self._split_leaf(node)
            return None

        # Internal node routing
        idx = bisect.bisect_right(node.keys, key)
        split_child = self._insert(node.children[idx], key, value)
        if split_child is not None:
            promoted_key, new_child = split_child
            node.keys.insert(idx, promoted_key)
            node.children.insert(idx + 1, new_child)
            self.stats.pages_written += 1
            if len(node.keys) >= self.order:
                return self._split_internal(node)
        return None

    def _split_leaf(self, leaf: LeafNode) -> tuple[int, LeafNode]:
        mid = len(leaf.keys) // 2
        new_leaf = LeafNode(
            keys=leaf.keys[mid:],
            values=leaf.values[mid:],
            next_leaf=leaf.next_leaf,
        )
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        leaf.next_leaf = new_leaf
        return new_leaf.keys[0], new_leaf

    def _split_internal(self, node: InternalNode) -> tuple[int, InternalNode]:
        mid = len(node.keys) // 2
        promoted_key = node.keys[mid]
        new_node = InternalNode(
            keys=node.keys[mid + 1 :],
            children=node.children[mid + 1 :],
        )
        node.keys = node.keys[:mid]
        node.children = node.children[: mid + 1]
        return promoted_key, new_node

    def scan(self, start_key: int, end_key: int) -> list[tuple[int, Any]]:
        results: list[tuple[int, Any]] = []
        curr = self.root
        while not curr.is_leaf:
            idx = bisect.bisect_right(curr.keys, start_key)
            curr = curr.children[idx]

        while curr is not None:
            for k, v in zip(curr.keys, curr.values):
                if k > end_key:
                    return results
                if k >= start_key:
                    results.append((k, v))
            curr = curr.next_leaf
        return results

    def memory_footprint_bytes(self) -> int:
        return estimate_object_memory(self.root)
