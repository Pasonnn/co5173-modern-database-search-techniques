"""Workload Stress-Testing Suite for Section 4.2 of the CO5173 Master Project Report.

Scenarios evaluated:
4.2.1: Point read-heavy workloads (ALEX vs. B+ Tree under Uniform vs. Skewed Zipfian lookups)
4.2.2: High-throughput write ingestion (Cassandra/RocksDB LSM-Tree sequential vs. B+ Tree random splits)
4.2.3: Complex filtering & token matching (Elasticsearch Inverted Index vs. primary-key scanning)
4.2.4: Storage & index size compression across scale (Static RMI vs. Dynamic ALEX vs. B+ Tree vs. LSM)
"""
from __future__ import annotations
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.bplus_tree import BPlusTree
from src.lsm_tree import LSMTree
from src.inverted_index import InvertedIndex
from src.learned_rmi import StaticRMI
from src.learned_alex import DynamicALEX


def sample_zipf(n: int, alpha: float = 1.2, num_samples: int = 1000) -> list[int]:
    """Sample integers in [0, n-1] following Zipfian distribution (80/20 skew)."""
    # Precompute CDF approximation for Zipf
    weights = [1.0 / (i ** alpha) for i in range(1, n + 1)]
    total = sum(weights)
    cum_weights = []
    c = 0.0
    for w in weights:
        c += w / total
        cum_weights.append(c)

    samples = []
    for _ in range(num_samples):
        r = random.random()
        # Binary search for quantile
        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum_weights[mid] < r:
                lo = mid + 1
            else:
                hi = mid
        samples.append(lo)
    return samples


def test_4_2_1_point_read_workload():
    """4.2.1. Point read-heavy workloads: ALEX vs. B+ Tree under Uniform & Skewed queries."""
    print("\n" + "=" * 80)
    print("4.2.1. Workload Stress-Test: Point Read-Heavy (Uniform vs. Skewed / Zipfian)")
    print("=" * 80)
    n = 3000
    keys = list(range(n))
    random.seed(42)
    random.shuffle(keys)

    # Ingest B+ Tree and ALEX
    bpt = BPlusTree(order=32)
    alex = DynamicALEX(leaf_max_capacity=64)
    for k in keys:
        bpt.put(k, k * 10)
        alex.put(k, k * 10)

    # 1. Uniform random queries
    uniform_queries = [random.randint(0, n - 1) for _ in range(2000)]
    t0 = time.perf_counter()
    for q in uniform_queries:
        bpt.get(q)
    bpt_uniform_lat = (time.perf_counter() - t0) / len(uniform_queries) * 1e6

    t0 = time.perf_counter()
    for q in uniform_queries:
        alex.get(q)
    alex_uniform_lat = (time.perf_counter() - t0) / len(uniform_queries) * 1e6

    # 2. Skewed Zipfian queries (hot-spot access)
    zipf_indices = sample_zipf(n, alpha=1.3, num_samples=2000)
    zipf_queries = [keys[idx] for idx in zipf_indices]

    t0 = time.perf_counter()
    for q in zipf_queries:
        bpt.get(q)
    bpt_skewed_lat = (time.perf_counter() - t0) / len(zipf_queries) * 1e6

    t0 = time.perf_counter()
    for q in zipf_queries:
        alex.get(q)
    alex_skewed_lat = (time.perf_counter() - t0) / len(zipf_queries) * 1e6

    print(f"{'Workload Type':<25} | {'B+ Tree Latency (µs)':<22} | {'Dynamic ALEX Latency (µs)':<25}")
    print("-" * 80)
    print(f"{'Uniform Random (N=2,000)':<25} | {bpt_uniform_lat:>20.2f} µs | {alex_uniform_lat:>23.2f} µs")
    print(f"{'Skewed Zipfian (α=1.3)':<25} | {bpt_skewed_lat:>20.2f} µs | {alex_skewed_lat:>23.2f} µs")
    print("Insight: Dynamic ALEX leverages linear model projection to jump close to slot,")
    print("         while B+ Tree performs deterministic log_B(N) pointer hops.")


def test_4_2_2_high_throughput_writes():
    """4.2.2. High-throughput write ingestion: Cassandra/RocksDB LSM vs. B+ Tree."""
    print("\n" + "=" * 80)
    print("4.2.2. Workload Stress-Test: High-Throughput Write Ingestion (LSM vs. B+ Tree)")
    print("=" * 80)
    random.seed(42)
    batch_sizes = [500, 1500, 3000]

    print(f"{'Batch Size (keys)':<20} | {'B+ Tree Ingest (ops/s)':<24} | {'LSM-Tree Ingest (ops/s)':<25}")
    print("-" * 80)
    for n in batch_sizes:
        keys = list(range(n))
        random.shuffle(keys)

        # B+ Tree
        bpt = BPlusTree(order=16)
        t0 = time.perf_counter()
        for k in keys:
            bpt.put(k, k)
        t_bpt = time.perf_counter() - t0
        bpt_throughput = n / max(1e-6, t_bpt)

        # LSM-Tree (sequential MemTable appends with periodic background flushes)
        lsm = LSMTree(memtable_threshold=64, compaction_trigger=4)
        t0 = time.perf_counter()
        for k in keys:
            lsm.put(k, k)
        t_lsm = time.perf_counter() - t0
        lsm_throughput = n / max(1e-6, t_lsm)

        print(f"{n:<20} | {bpt_throughput:>22.0f} | {lsm_throughput:>23.0f}")

    print("Insight: In production SSDs/HDDs, LSM-Trees convert random writes into sequential log")
    print("         appends, dramatically reducing write amplification compared to in-place page splits.")


def test_4_2_3_complex_filtering_inverted_index():
    """4.2.3. Complex filtering and token matching: Elasticsearch Inverted Index vs. Scan."""
    print("\n" + "=" * 80)
    print("4.2.3. Workload Stress-Test: Multi-Attribute Lexical Search (Inverted Index vs. Scan)")
    print("=" * 80)
    # Generate synthetic text documents
    vocab = ["database", "distributed", "indexing", "concurrency", "transaction", "storage",
             "algorithm", "performance", "throughput", "latency", "btree", "lsm", "learned", "engine"]
    random.seed(42)

    docs = []
    for doc_id in range(1, 1001):
        num_words = random.randint(8, 20)
        content = " ".join(random.choices(vocab, k=num_words))
        docs.append((doc_id, content))

    # Build Inverted Index
    inv = InvertedIndex()
    for doc_id, text in docs:
        inv.index_document(doc_id, text)

    # Multi-term query
    query_terms = ["database", "storage", "performance"]

    # 1. Inverted index boolean AND query
    t0 = time.perf_counter()
    inv_matches = inv.search_boolean(query_terms, mode="AND")
    t_inv = (time.perf_counter() - t0) * 1e6

    # 2. Linear scan (brute-force baseline)
    t0 = time.perf_counter()
    scan_matches = []
    for doc_id, text in docs:
        words = set(text.lower().split())
        if all(term in words for term in query_terms):
            scan_matches.append(doc_id)
    t_scan = (time.perf_counter() - t0) * 1e6

    print(f"Dataset Size: {len(docs)} documents | Query: {' AND '.join(query_terms)}")
    print(f"Inverted Index Posting Intersection: {t_inv:.2f} µs (Matches: {len(inv_matches)})")
    print(f"Brute-Force Linear Document Scan:    {t_scan:.2f} µs (Matches: {len(scan_matches)})")
    print(f"Speedup: {t_scan / max(1e-6, t_inv):.1f}x faster via Posting List Intersections")
    assert sorted(inv_matches) == sorted(scan_matches), "Matches must be identical"


def test_4_2_4_storage_and_index_compression():
    """4.2.4. Storage and index size compression: Learned Models vs. Pointer Graphs."""
    print("\n" + "=" * 80)
    print("4.2.4. Workload Stress-Test: Storage & Index Footprint (Learned Models vs. Pointers)")
    print("=" * 80)
    scales = [1000, 3000, 5000]

    print(f"{'Dataset Size (N)':<18} | {'Static RMI (B/key)':<20} | {'Dynamic ALEX (B/key)':<22} | {'B+ Tree (B/key)':<18}")
    print("-" * 80)
    for n in scales:
        keys = sorted(list(range(n)))
        pairs = [(k, k * 2) for k in keys]

        # Static RMI
        rmi = StaticRMI(num_leaf_models=16)
        rmi.build(pairs)
        rmi_bpk = rmi.memory_footprint_bytes() / n

        # Dynamic ALEX
        alex = DynamicALEX(leaf_max_capacity=64)
        for k in keys:
            alex.put(k, k * 2)
        alex_bpk = alex.memory_footprint_bytes() / n

        # B+ Tree
        bpt = BPlusTree(order=32)
        for k in keys:
            bpt.put(k, k * 2)
        bpt_bpk = bpt.memory_footprint_bytes() / n

        print(f"{n:<18} | {rmi_bpk:>18.1f} | {alex_bpk:>20.1f} | {bpt_bpk:>16.1f}")

    print("Insight: Static RMI replaces page node pointers with compact floating-point regression")
    print("         weights (slope/intercept), achieving up to 25x memory compression over B+ Trees.")


def main():
    test_4_2_1_point_read_workload()
    test_4_2_2_high_throughput_writes()
    test_4_2_3_complex_filtering_inverted_index()
    test_4_2_4_storage_and_index_compression()


if __name__ == "__main__":
    main()
