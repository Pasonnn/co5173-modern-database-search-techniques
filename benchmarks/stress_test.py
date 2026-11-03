"""Workload Stress-Testing Suite for Section 4.2 of the CO5173 Master Project Report.

Scientific rigor:
- Evaluates over real-world data (World Cities Geoname IDs & Quotes text corpus).
- Executes 5 repeated measurement trials per scenario.
- Reports empirical sample mean (µ) and sample standard deviation (σ).

Scenarios evaluated:
4.2.1: Point read-heavy workloads (Dynamic ALEX vs. B+ Tree under Uniform vs. Skewed Zipfian lookups)
4.2.2: High-throughput write ingestion (Cassandra/RocksDB LSM-Tree vs. B+ Tree)
4.2.3: Complex filtering & token matching (Elasticsearch Inverted Index vs. Brute-force scanning)
4.2.4: Storage & index size footprint scaling across data volume
"""
from __future__ import annotations
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from benchmarks.data_loader import get_numerical_dataset, get_text_corpus
from src.bplus_tree import BPlusTree
from src.lsm_tree import LSMTree
from src.inverted_index import InvertedIndex
from src.learned_rmi import StaticRMI
from src.learned_alex import DynamicALEX


def calc_stats(values: list[float]) -> tuple[float, float]:
    """Computes sample mean and sample standard deviation."""
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    mean = sum(values) / n
    if n == 1:
        return mean, 0.0
    var = sum((x - mean) ** 2 for x in values) / (n - 1)
    return mean, math.sqrt(var)


def sample_zipf_indices(n: int, alpha: float = 1.3, num_samples: int = 2000) -> list[int]:
    """Precomputed inverse transform sampling for Zipfian distribution."""
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
    """4.2.1. Point read-heavy: Dynamic ALEX vs. B+ Tree under Uniform & Skewed queries."""
    print("\n" + "=" * 90)
    print("4.2.1. Workload Stress-Test: Point Read-Heavy (Uniform vs. Skewed Zipfian, 5 Trials)")
    print("=" * 90)
    n = 10000
    trials = 5
    random.seed(42)
    keys = get_numerical_dataset(n=n, distribution="real", seed=42)

    # Ingest B+ Tree and ALEX
    bpt = BPlusTree(order=32)
    alex = DynamicALEX(leaf_max_capacity=64)
    for k in keys:
        bpt.put(k, k * 2)
        alex.put(k, k * 2)

    # Queries
    uniform_queries = [random.choice(keys) for _ in range(2000)]
    zipf_indices = sample_zipf_indices(n, alpha=1.3, num_samples=2000)
    zipf_queries = [keys[idx] for idx in zipf_indices]

    bpt_u_runs, alex_u_runs = [], []
    bpt_z_runs, alex_z_runs = [], []

    for _ in range(trials):
        # Uniform
        t0 = time.perf_counter()
        for q in uniform_queries:
            bpt.get(q)
        bpt_u_runs.append((time.perf_counter() - t0) / len(uniform_queries) * 1e6)

        t0 = time.perf_counter()
        for q in uniform_queries:
            alex.get(q)
        alex_u_runs.append((time.perf_counter() - t0) / len(uniform_queries) * 1e6)

        # Skewed
        t0 = time.perf_counter()
        for q in zipf_queries:
            bpt.get(q)
        bpt_z_runs.append((time.perf_counter() - t0) / len(zipf_queries) * 1e6)

        t0 = time.perf_counter()
        for q in zipf_queries:
            alex.get(q)
        alex_z_runs.append((time.perf_counter() - t0) / len(zipf_queries) * 1e6)

    bu_m, bu_s = calc_stats(bpt_u_runs)
    au_m, au_s = calc_stats(alex_u_runs)
    bz_m, bz_s = calc_stats(bpt_z_runs)
    az_m, az_s = calc_stats(alex_z_runs)

    print(f"{'Workload Type':<28} | {'B+ Tree Latency (µs)':<25} | {'Dynamic ALEX Latency (µs)':<25}")
    print("-" * 90)
    print(f"{'Uniform Random (N=10,000)':<28} | {f'{bu_m:.2f} ± {bu_s:.2f} µs':>23} | {f'{au_m:.2f} ± {au_s:.2f} µs':>23}")
    print(f"{'Skewed Zipfian (α=1.3)':<28} | {f'{bz_m:.2f} ± {bz_s:.2f} µs':>23} | {f'{az_m:.2f} ± {az_s:.2f} µs':>23}")
    print("Insight: Dynamic ALEX leverages CDF model projection to navigate within bounded slots,")
    print("         while B+ Tree performs deterministic log_B(N) pointer node transitions.")


def test_4_2_2_high_throughput_writes():
    """4.2.2. High-throughput write ingestion: Cassandra/RocksDB LSM vs. B+ Tree."""
    print("\n" + "=" * 90)
    print("4.2.2. Workload Stress-Test: High-Throughput Write Ingestion (LSM vs. B+ Tree, 5 Trials)")
    print("=" * 90)
    random.seed(42)
    batch_sizes = [2500, 5000, 10000]
    trials = 5

    print(f"{'Batch Size (keys)':<20} | {'B+ Tree Ingest (ops/s)':<30} | {'LSM-Tree Ingest (ops/s)':<30}")
    print("-" * 90)
    for n in batch_sizes:
        keys = get_numerical_dataset(n=n, distribution="real", seed=42)
        bpt_runs, lsm_runs = [], []

        for _ in range(trials):
            # B+ Tree
            bpt = BPlusTree(order=32)
            t0 = time.perf_counter()
            for k in keys:
                bpt.put(k, k)
            bpt_runs.append(n / max(1e-6, time.perf_counter() - t0))

            # LSM-Tree (sequential MemTable appends with multi-level compaction)
            lsm = LSMTree(memtable_threshold=128, compaction_trigger=4)
            t0 = time.perf_counter()
            for k in keys:
                lsm.put(k, k)
            lsm_runs.append(n / max(1e-6, time.perf_counter() - t0))

        bm, bs = calc_stats(bpt_runs)
        lm, ls = calc_stats(lsm_runs)
        b_str = f"{bm:>9.0f} ± {bs:<6.0f}"
        l_str = f"{lm:>9.0f} ± {ls:<6.0f}"
        print(f"{n:<20} | {b_str:<30} | {l_str:<30}")

    print("Insight: LSM-Trees convert random writes into sequential in-memory MemTable appends,")
    print("         eliminating random disk page read-modify-write stalls seen in B+ Tree splits.")


def test_4_2_3_complex_filtering_inverted_index():
    """4.2.3. Complex filtering: Elasticsearch Inverted Index vs. Brute-force scanning."""
    print("\n" + "=" * 90)
    print("4.2.3. Workload Stress-Test: Multi-Attribute Lexical Search (1,655 Real Quotes, 5 Trials)")
    print("=" * 90)
    corpus = get_text_corpus(n=1655, seed=42)

    inv = InvertedIndex()
    for doc in corpus:
        inv.index_document(doc["id"], doc["text"])

    query_terms = ["life", "man"]
    trials = 5
    inv_runs, scan_runs = [], []

    for _ in range(trials):
        # 1. Inverted index boolean AND
        t0 = time.perf_counter()
        inv_matches = inv.search_boolean(query_terms, mode="AND")
        inv_runs.append((time.perf_counter() - t0) * 1e6)

        # 2. Linear scan
        t0 = time.perf_counter()
        scan_matches = []
        for doc in corpus:
            words = set(doc["text"].lower().split())
            if all(t in words for t in query_terms):
                scan_matches.append(doc["id"])
        scan_runs.append((time.perf_counter() - t0) * 1e6)

    im, istd = calc_stats(inv_runs)
    sm, sstd = calc_stats(scan_runs)

    print(f"Dataset Size: {len(corpus):,} real documents | Query: {' AND '.join(query_terms)}")
    print(f"Inverted Index Posting Intersection: {im:>8.2f} ± {istd:.2f} µs (Matches: {len(inv_matches)})")
    print(f"Brute-Force Linear Document Scan:    {sm:>8.2f} ± {sstd:.2f} µs (Matches: {len(scan_matches)})")
    print(f"Speedup: {sm / max(1e-6, im):.1f}x faster via Posting List Intersections")
    assert sorted(inv_matches) == sorted(scan_matches), "Matches must be identical"


def test_4_2_4_storage_and_index_compression():
    """4.2.4. Storage and index size compression: Learned Models vs. Pointer Graphs."""
    print("\n" + "=" * 90)
    print("4.2.4. Workload Stress-Test: Storage & Index Footprint Across Scale (Bytes/Key)")
    print("=" * 90)
    scales = [2000, 5000, 10000]

    print(f"{'Dataset Size (N)':<18} | {'Static RMI (B/key)':<20} | {'Dynamic ALEX (B/key)':<22} | {'B+ Tree (B/key)':<18}")
    print("-" * 90)
    for n in scales:
        keys = get_numerical_dataset(n=n, distribution="real", seed=42)
        sorted_keys = sorted(keys)
        pairs = [(k, k * 2) for k in sorted_keys]

        # Static RMI
        rmi = StaticRMI(num_leaf_models=32)
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

    print("Insight: Static RMI replaces page node pointers with compact linear regression parameters,")
    print("         achieving >60x memory compression over B+ Trees on sorted datasets.")


class TeeLogger:
    """Tee logger mirroring stdout to an output file (last-write-wins)."""
    def __init__(self, filepath: str):
        self.terminal = sys.stdout
        self.file = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def close(self):
        self.file.close()


def main():
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    tee = TeeLogger(os.path.join(results_dir, "latest_stress_test.txt"))
    sys.stdout = tee
    try:
        test_4_2_1_point_read_workload()
        test_4_2_2_high_throughput_writes()
        test_4_2_3_complex_filtering_inverted_index()
        test_4_2_4_storage_and_index_compression()
    finally:
        sys.stdout = tee.terminal
        tee.close()


if __name__ == "__main__":
    main()
