"""Runnable test suite verifying all 5 modern database search indexing structures."""
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import random
from src.bplus_tree import BPlusTree
from src.lsm_tree import LSMTree
from src.inverted_index import InvertedIndex
from src.learned_rmi import StaticRMI
from src.learned_alex import DynamicALEX


def test_bplus_tree():
    tree = BPlusTree(order=4)
    data = {i: f"val_{i}" for i in range(100)}
    for k, v in data.items():
        tree.put(k, v)

    # Point lookups
    for k, v in data.items():
        assert tree.get(k) == v, f"B+ Tree lookup failed for {k}"
    assert tree.get(999) is None

    # Overwrite
    tree.put(10, "new_val_10")
    assert tree.get(10) == "new_val_10"

    # Range scan
    scan_res = tree.scan(20, 25)
    assert [k for k, _ in scan_res] == list(range(20, 26))


def test_lsm_tree():
    lsm = LSMTree(memtable_threshold=8, compaction_trigger=3)
    data = {i: f"lsm_{i}" for i in range(50)}
    for k, v in data.items():
        lsm.put(k, v)

    for k, v in data.items():
        assert lsm.get(k) == v, f"LSM lookup failed for {k}"
    assert lsm.get(999) is None

    # Deletion via Tombstone
    lsm.delete(15)
    assert lsm.get(15) is None

    # Force compaction
    lsm.compact()
    assert lsm.get(15) is None
    assert lsm.get(16) == "lsm_16"

    # Range scan
    scan_res = lsm.scan(30, 35)
    assert [k for k, _ in scan_res] == list(range(30, 36))


def test_inverted_index():
    idx = InvertedIndex()
    idx.index_document(1, "Modern database storage engines use B+ Tree for OLTP.", {"year": 2020})
    idx.index_document(2, "LSM Tree provides high write ingestion throughput in RocksDB.", {"year": 2022})
    idx.index_document(3, "Learned index models use CDF approximation to accelerate search.", {"year": 2024})

    # Boolean search
    assert idx.search_boolean(["tree", "engines"], mode="AND") == [1]
    assert idx.search_boolean(["lsm", "database"], mode="OR") == [1, 2]

    # BM25 ranking
    bm25_res = idx.search_bm25("storage engines database")
    assert len(bm25_res) > 0
    assert bm25_res[0][0] == 1  # Doc 1 is top match

    # Range filtering
    assert idx.range_filter("year", 2021, 2025) == [2, 3]


def test_learned_rmi():
    rmi = StaticRMI(num_leaf_models=8)
    sorted_data = [(i * 2, f"rmi_{i}") for i in range(100)]
    rmi.build(sorted_data)

    for k, v in sorted_data:
        assert rmi.get(k) == v, f"RMI lookup failed for {k}"
    assert rmi.get(999) is None
    assert rmi.get(3) is None  # Odd key not present

    scan_res = rmi.scan(10, 20)
    assert [k for k, _ in scan_res] == [10, 12, 14, 16, 18, 20]


def test_learned_alex():
    alex = DynamicALEX(leaf_max_capacity=16)
    keys = list(range(100))
    random.shuffle(keys)
    for k in keys:
        alex.put(k, f"alex_{k}")

    for k in range(100):
        assert alex.get(k) == f"alex_{k}", f"ALEX lookup failed for {k}"
    assert alex.get(999) is None

    # Overwrite
    alex.put(42, "updated_alex")
    assert alex.get(42) == "updated_alex"

    scan_res = alex.scan(10, 15)
    assert [k for k, _ in scan_res] == list(range(10, 16))


if __name__ == "__main__":
    test_bplus_tree()
    test_lsm_tree()
    test_inverted_index()
    test_learned_rmi()
    test_learned_alex()
    print("ALL 5 SEARCH TECHNIQUE SELF-CHECKS PASSED SUCCESSFULLY.")
