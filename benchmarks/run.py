"""Benchmark runner evaluating the RUM trade-off space across modern database search architectures.

Scientific rigor:
- Evaluates over real-world dataset (World Cities Geoname IDs: N=10,000).
- Executes 1 warmup run followed by 5 repeated measurement trials.
- Reports empirical sample mean (µ) and sample standard deviation (σ).
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


def run_single_trial(name: str, keys: list[int], queries: list[int], range_queries: list[tuple[int, int]]):
    # 1. Ingestion
    t0 = time.perf_counter()
    if name == "B+ Tree":
        engine = BPlusTree(order=32)
        for k in keys:
            engine.put(k, k * 2)
    elif name == "LSM-Tree":
        engine = LSMTree(memtable_threshold=128, compaction_trigger=4)
        for k in keys:
            engine.put(k, k * 2)
    elif name == "Static RMI":
        engine = StaticRMI(num_leaf_models=64)
        sorted_pairs = sorted([(k, k * 2) for k in keys], key=lambda x: x[0])
        engine.build(sorted_pairs)
    elif name == "Dynamic ALEX":
        engine = DynamicALEX(leaf_max_capacity=64)
        for k in keys:
            engine.put(k, k * 2)
    else:
        raise ValueError(f"Unknown engine: {name}")
    t_ingest = time.perf_counter() - t0
    ingest_throughput = len(keys) / max(1e-6, t_ingest)

    # 2. Point Lookups
    t0 = time.perf_counter()
    hits = 0
    for q in queries:
        if engine.get(q) is not None:
            hits += 1
    t_lookup = time.perf_counter() - t0
    lookup_latency_us = (t_lookup / len(queries)) * 1e6

    # 3. Range Queries
    t0 = time.perf_counter()
    for low, high in range_queries:
        _ = engine.scan(low, high)
    t_range = time.perf_counter() - t0
    range_throughput = len(range_queries) / max(1e-6, t_range)

    # 4. Memory Footprint
    mem_bytes = engine.memory_footprint_bytes()
    bytes_per_key = mem_bytes / max(1, len(keys))

    return {
        "ingest": ingest_throughput,
        "lookup": lookup_latency_us,
        "range": range_throughput,
        "bytes_per_key": bytes_per_key,
        "hit_ratio": hits / len(queries),
    }


def benchmark_engine_statistical(name: str, keys: list[int], queries: list[int], range_queries: list[tuple[int, int]], num_trials: int = 5):
    # Warmup run (discarded to eliminate cache warming / JIT branch anomalies)
    _ = run_single_trial(name, keys, queries, range_queries)

    ingest_runs = []
    lookup_runs = []
    range_runs = []
    bpk_runs = []

    for _ in range(num_trials):
        res = run_single_trial(name, keys, queries, range_queries)
        ingest_runs.append(res["ingest"])
        lookup_runs.append(res["lookup"])
        range_runs.append(res["range"])
        bpk_runs.append(res["bytes_per_key"])

    ingest_m, ingest_s = calc_stats(ingest_runs)
    lookup_m, lookup_s = calc_stats(lookup_runs)
    range_m, range_s = calc_stats(range_runs)
    bpk_m, bpk_s = calc_stats(bpk_runs)

    return {
        "engine": name,
        "ingest_mean": ingest_m,
        "ingest_std": ingest_s,
        "lookup_mean": lookup_m,
        "lookup_std": lookup_s,
        "range_mean": range_m,
        "range_std": range_s,
        "bpk_mean": bpk_m,
    }


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
    tee = TeeLogger(os.path.join(results_dir, "latest_run.txt"))
    sys.stdout = tee
    try:
        _run_benchmarks()
    finally:
        sys.stdout = tee.terminal
        tee.close()


def _run_benchmarks():
    n_keys = 10000
    trials = 5
    random.seed(42)

    print("=" * 105)
    print(f"CO5173 EMPIRICAL BENCHMARK: 5 REPEATED TRIALS (N={n_keys:,} Real-World Geoname Keys)")
    print("=" * 105)

    keys = get_numerical_dataset(n=n_keys, distribution="real", seed=42)

    # Queries: 50% existing keys, 50% non-existing keys
    existing_q = random.sample(keys, min(1000, len(keys)))
    max_k = max(keys)
    non_existing_q = [max_k + i * 3 for i in range(1000)]
    queries = existing_q + non_existing_q
    random.shuffle(queries)

    min_k, span = min(keys), max(keys) - min(keys)
    step = span // 200
    sample_starts = random.sample(keys, 100)
    range_queries = [(k, k + step) for k in sample_starts]

    engines = ["B+ Tree", "LSM-Tree", "Static RMI", "Dynamic ALEX"]
    results = []
    for eng in engines:
        print(f"Running {eng} (1 warmup + {trials} measurement trials)...")
        res = benchmark_engine_statistical(eng, keys, queries, range_queries, num_trials=trials)
        results.append(res)

    print("\n" + "=" * 105)
    print(f"{'Engine':<14} | {'Ingest (ops/s) (µ ± σ)':<26} | {'Lookup (µs) (µ ± σ)':<24} | {'Range (ops/s) (µ ± σ)':<22} | {'Bytes/Key':<10}")
    print("-" * 105)
    for r in results:
        ingest_str = f"{r['ingest_mean']:>10.0f} ± {r['ingest_std']:<6.0f}"
        lookup_str = f"{r['lookup_mean']:>8.2f} ± {r['lookup_std']:<5.2f}"
        range_str = f"{r['range_mean']:>8.0f} ± {r['range_std']:<5.0f}"
        print(
            f"{r['engine']:<14} | {ingest_str:<26} | {lookup_str:<24} | "
            f"{range_str:<22} | {r['bpk_mean']:>9.1f}"
        )
    print("=" * 105)

    # Inverted index evaluation on real quotes corpus
    print("\n--- Lexical Inverted Index on Real Text Corpus (BM25 + Boolean Search) ---")
    corpus = get_text_corpus(n=1655, seed=42)
    inv = InvertedIndex()
    t0 = time.perf_counter()
    for doc in corpus:
        inv.index_document(doc["id"], doc["text"], attributes={"author": doc.get("author", "")})
    t_idx = (time.perf_counter() - t0) * 1e3
    print(f"Indexed {len(corpus):,} real documents in {t_idx:.2f} ms")

    # 5 runs of BM25 scoring
    bm25_latencies = []
    test_query = "life success freedom wisdom courage"
    for _ in range(5):
        t0 = time.perf_counter()
        bm25_res = inv.search_bm25(test_query, limit=5)
        bm25_latencies.append((time.perf_counter() - t0) * 1e6)
    m_lat, s_lat = calc_stats(bm25_latencies)
    print(f"BM25 Top Match: Doc ID {bm25_res[0][0]} (Score: {bm25_res[0][1]:.3f})")
    print(f"BM25 Search Latency (5 runs): {m_lat:.2f} ± {s_lat:.2f} µs")

    # Boolean search
    bool_matches = inv.search_boolean(["life", "time"], mode="AND")
    print(f"Boolean AND ['life', 'time'] matched {len(bool_matches)} documents: {bool_matches}")


if __name__ == "__main__":
    main()
