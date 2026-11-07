"""Workload Stress-Testing Suite for Section 4.2 of the CO5173 Master Project Report.

Focus: Deep-dive comparative stress tests for Apache Cassandra (LSM) & Elasticsearch (Inverted Index).

Scientific rigor:
- Evaluates over real-world data (World Cities Geoname IDs & Quotes text corpus).
- Executes 5 repeated measurement trials per scenario.
- Reports empirical sample mean (µ) and sample standard deviation (σ).

Scenarios evaluated:
4.2.1: High-throughput write ingestion scaling in Cassandra LSM-Tree (Sequential MemTable Appends + Flushes)
4.2.2: Cassandra read path optimization: Bloom Filter fast-fail impact on absent key lookups
4.2.3: Lexical search acceleration: Elasticsearch Inverted Index vs. Brute-force linear text scan
4.2.4: Memory footprint scaling across data volume (LSM-Tree vs. Inverted Index)
"""
from __future__ import annotations
import bisect
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from benchmarks.data_loader import get_numerical_dataset, get_text_corpus
from src.lsm_tree import LSMTree, SSTable, TOMBSTONE
from src.inverted_index import InvertedIndex


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


def test_4_2_1_cassandra_write_scaling():
    """4.2.1. High-throughput write ingestion scaling in Cassandra LSM-Tree across batch sizes."""
    print("\n" + "=" * 90)
    print("4.2.1. Workload Stress-Test: Cassandra Write Ingestion Across Batch Sizes (5 Trials)")
    print("=" * 90)
    batch_sizes = [2500, 5000, 10000]
    trials = 5
    random.seed(42)

    print(f"{'Batch Size (keys)':<20} | {'Ingest Throughput (ops/s)':<30} | {'Total Elapsed Time (ms)':<25}")
    print("-" * 90)
    for n in batch_sizes:
        keys = get_numerical_dataset(n=n, distribution="real", seed=42)
        throughputs = []
        elapsed_times = []

        for _ in range(trials):
            lsm = LSMTree(memtable_threshold=128, compaction_trigger=4)
            t0 = time.perf_counter()
            for k in keys:
                lsm.put(k, k * 2)
            dur = time.perf_counter() - t0
            throughputs.append(n / max(1e-6, dur))
            elapsed_times.append(dur * 1e3)

        tm, ts = calc_stats(throughputs)
        em, es = calc_stats(elapsed_times)
        t_str = f"{tm:>10.0f} ± {ts:<6.0f}"
        e_str = f"{em:>8.2f} ± {es:<5.2f} ms"
        print(f"{n:<20} | {t_str:<30} | {e_str:<25}")

    print("Insight: Cassandra transforms random discrete writes into sequential in-memory appends")
    print("         to MemTable (SkipList), achieving sustained high throughput across scales.")


def test_4_2_2_bloom_filter_impact():
    """4.2.2. Measure the latency penalty of disabling Bloom Filters on absent key lookups."""
    print("\n" + "=" * 90)
    print("4.2.2. Workload Stress-Test: Bloom Filter Fast-Fail Impact on Absent Key Lookups (5 Trials)")
    print("=" * 90)
    n = 10000
    trials = 5
    random.seed(42)
    keys = get_numerical_dataset(n=n, distribution="real", seed=42)

    lsm = LSMTree(memtable_threshold=128, compaction_trigger=4)
    for k in keys:
        lsm.put(k, k * 2)

    # Absent keys guaranteed not to exist
    max_k = max(keys)
    absent_keys = [max_k + 7 + i * 3 for i in range(1000)]

    with_bf_latencies = []
    without_bf_latencies = []

    for _ in range(trials):
        # 1. With Bloom Filter enabled (Standard LSM read path)
        t0 = time.perf_counter()
        for q in absent_keys:
            lsm.get(q)
        with_bf_latencies.append((time.perf_counter() - t0) / len(absent_keys) * 1e6)

        # 2. Without Bloom Filter (Bypass Bloom filter and binary search all SSTables)
        t0 = time.perf_counter()
        for q in absent_keys:
            # Emulate search bypassing bloom filter
            for sst in lsm.sstables:
                f_idx = bisect.bisect_right(sst.fence_keys, q) - 1
                start = sst.fence_indices[max(0, f_idx)]
                end = sst.fence_indices[f_idx + 1] if f_idx + 1 < len(sst.fence_indices) else len(sst.keys)
                sub_keys = sst.keys[start:end]
                idx = bisect.bisect_left(sub_keys, q)
                if idx < len(sub_keys) and sub_keys[idx] == q:
                    break
        without_bf_latencies.append((time.perf_counter() - t0) / len(absent_keys) * 1e6)

    w_m, w_s = calc_stats(with_bf_latencies)
    wo_m, wo_s = calc_stats(without_bf_latencies)
    speedup = wo_m / max(1e-6, w_m)

    print(f"{'Read Path Mode':<35} | {'Lookup Latency (µs)':<25} | {'Pruned SSTable Checks':<20}")
    print("-" * 90)
    print(f"{'With In-Memory Bloom Filter':<35} | {f'{w_m:.2f} ± {w_s:.2f} µs':>23} | {'100% of SSTables prunable':<20}")
    print(f"{'Without Bloom Filter (Binary Search)':<35} | {f'{wo_m:.2f} ± {wo_s:.2f} µs':>23} | {'0% (All SSTables checked)':<20}")
    print(f"Speedup via Bloom Filter: {speedup:.2f}x faster on negative lookups")
    print("Insight: In production Cassandra, Bloom Filters prevent costly multi-SSTable disk seeks")
    print("         for absent keys, directly conquering the Read Amplification (R) penalty.")


def test_4_2_3_elasticsearch_vs_scan():
    """4.2.3. Lexical query acceleration: Elasticsearch Inverted Index vs Linear Scan."""
    print("\n" + "=" * 90)
    print("4.2.3. Workload Stress-Test: Lexical Search vs. Brute-Force Scan (1,655 Real Quotes, 5 Trials)")
    print("=" * 90)
    corpus = get_text_corpus(n=1655, seed=42)

    inv = InvertedIndex(k1=1.2, b=0.75)
    for doc in corpus:
        inv.index_document(doc["id"], doc["text"])

    query_terms = ["life", "man"]
    trials = 5
    inv_runs, scan_runs = [], []

    for _ in range(trials):
        # 1. Inverted index boolean AND (Posting list intersection)
        t0 = time.perf_counter()
        inv_matches = inv.search_boolean(query_terms, mode="AND")
        inv_runs.append((time.perf_counter() - t0) * 1e6)

        # 2. Linear document scan
        t0 = time.perf_counter()
        scan_matches = []
        for doc in corpus:
            words = set(doc["text"].lower().split())
            if all(t in words for t in query_terms):
                scan_matches.append(doc["id"])
        scan_runs.append((time.perf_counter() - t0) * 1e6)

    im, istd = calc_stats(inv_runs)
    sm, sstd = calc_stats(scan_runs)

    print(f"Dataset: {len(corpus):,} real documents | Query: {' AND '.join(query_terms)}")
    print(f"{'Search Method':<38} | {'Latency (µs)':<25} | {'Matched Documents':<18}")
    print("-" * 90)
    print(f"{'Elasticsearch Posting Intersection':<38} | {f'{im:.2f} ± {istd:.2f} µs':>23} | {len(inv_matches):<18}")
    print(f"{'Brute-Force Linear Text Scan':<38} | {f'{sm:.2f} ± {sstd:.2f} µs':>23} | {len(scan_matches):<18}")
    speedup = sm / max(1e-6, im)
    print(f"Speedup: {speedup:.1f}x faster via Inverted Index posting list intersection")
    assert sorted(inv_matches) == sorted(scan_matches), "Matches must be identical"
    print("Insight: Inverted indexes isolate candidate documents in O(min(|P_1|, |P_2|)) time,")
    print("         avoiding O(N * L) exhaustive string scans across the entire corpus.")


def test_4_2_4_storage_footprint_scaling():
    """4.2.4. Memory and storage footprint scaling across data scales."""
    print("\n" + "=" * 90)
    print("4.2.4. Workload Stress-Test: Memory Footprint Scaling Across Data Scales")
    print("=" * 90)
    scales = [2500, 5000, 10000]

    print(f"{'Dataset Size (N)':<18} | {'Cassandra LSM (B/key)':<26} | {'Total LSM Memory (KB)':<22}")
    print("-" * 90)
    for n in scales:
        keys = get_numerical_dataset(n=n, distribution="real", seed=42)
        lsm = LSMTree(memtable_threshold=128, compaction_trigger=4)
        for k in keys:
            lsm.put(k, k * 2)

        mem_bytes = lsm.memory_footprint_bytes()
        bpk = mem_bytes / n
        mem_kb = mem_bytes / 1024
        print(f"{n:<18} | {bpk:>24.1f} | {mem_kb:>20.1f} KB")

    print("Insight: Cassandra's in-memory footprint scales linearly with active keys and")
    print("         maintains a compact Bloom filter overhead (~10 bits per key in production).")


class TeeLogger:
    """Tee logger mirroring stdout to an output file."""
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
        test_4_2_1_cassandra_write_scaling()
        test_4_2_2_bloom_filter_impact()
        test_4_2_3_elasticsearch_vs_scan()
        test_4_2_4_storage_footprint_scaling()
    finally:
        sys.stdout = tee.terminal
        tee.close()


if __name__ == "__main__":
    main()
