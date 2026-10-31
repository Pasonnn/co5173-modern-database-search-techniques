"""Benchmark runner evaluating the RUM trade-off space across modern database search architectures."""
from __future__ import annotations
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


def benchmark_engine(name: str, keys: list[int], queries: list[int], range_queries: list[tuple[int, int]]):
    print(f"\n--- Benchmarking {name} (N={len(keys):,}) ---")

    # 1. Ingestion
    t0 = time.perf_counter()
    if name == "B+ Tree":
        engine = BPlusTree(order=32)
        for k in keys:
            engine.put(k, k * 2)
    elif name == "LSM-Tree":
        engine = LSMTree(memtable_threshold=64, compaction_trigger=4)
        for k in keys:
            engine.put(k, k * 2)
    elif name == "Static RMI":
        engine = StaticRMI(num_leaf_models=32)
        sorted_pairs = sorted([(k, k * 2) for k in keys], key=lambda x: x[0])
        engine.build(sorted_pairs)
    elif name == "Dynamic ALEX":
        engine = DynamicALEX(leaf_max_capacity=64)
        for k in keys:
            engine.put(k, k * 2)
    else:
        raise ValueError(f"Unknown engine {name}")
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
    scanned_count = 0
    for low, high in range_queries:
        res = engine.scan(low, high)
        scanned_count += len(res)
    t_range = time.perf_counter() - t0
    range_throughput = len(range_queries) / max(1e-6, t_range)

    # 4. Memory Footprint
    mem_bytes = engine.memory_footprint_bytes()
    bytes_per_key = mem_bytes / max(1, len(keys))

    return {
        "engine": name,
        "ingest_ops_sec": ingest_throughput,
        "lookup_lat_us": lookup_latency_us,
        "range_ops_sec": range_throughput,
        "bytes_per_key": bytes_per_key,
        "hit_ratio": hits / len(queries),
    }


def main():
    n_keys = 2000
    random.seed(42)

    keys = list(range(n_keys))
    random.shuffle(keys)

    # Queries: 50% existing keys, 50% non-existing keys
    existing_q = random.sample(keys, min(500, len(keys)))
    non_existing_q = [k + n_keys * 2 for k in range(500)]
    queries = existing_q + non_existing_q
    random.shuffle(queries)

    range_queries = [(k, k + 50) for k in random.sample(keys, 100)]

    engines = ["B+ Tree", "LSM-Tree", "Static RMI", "Dynamic ALEX"]
    results = []
    for eng in engines:
        res = benchmark_engine(eng, keys, queries, range_queries)
        results.append(res)

    # Print summary table
    print("\n" + "=" * 95)
    print(f"{'Engine':<16} | {'Ingest (ops/s)':<16} | {'Point Lookup (µs)':<18} | {'Range (ops/s)':<15} | {'Bytes/Key':<12}")
    print("-" * 95)
    for r in results:
        print(
            f"{r['engine']:<16} | {r['ingest_ops_sec']:>14.0f} | {r['lookup_lat_us']:>16.2f} | "
            f"{r['range_ops_sec']:>13.0f} | {r['bytes_per_key']:>10.1f}"
        )
    print("=" * 95)

    # Inverted index benchmark
    print("\n--- Benchmarking Inverted Index (BM25 + Boolean Search) ---")
    corpus = [
        (1, "Relational databases use B+ Trees for balanced tree traversal and leaf range scans."),
        (2, "RocksDB and Apache Cassandra adopt LSM-Trees to achieve high sequential write throughput."),
        (3, "Learned index structures replace comparison pointers with CDF approximation functions."),
        (4, "Elasticsearch uses inverted indexes with BM25 ranking for full-text lexical search."),
        (5, "ALEX introduces gapped arrays to handle dynamic updatable workloads in learned models."),
    ]
    inv = InvertedIndex()
    t0 = time.perf_counter()
    for doc_id, text in corpus:
        inv.index_document(doc_id, text)
    t_idx = time.perf_counter() - t0

    bm25_res = inv.search_bm25("learned index models search")
    print(f"Indexed {len(corpus)} documents in {t_idx * 1e3:.2f} ms")
    print(f"BM25 Top Match: Doc ID {bm25_res[0][0]} (Score: {bm25_res[0][1]:.3f})")
    print(f"Boolean AND Match for ['database', 'search']: {inv.search_boolean(['database', 'search'], mode='AND')}")


if __name__ == "__main__":
    main()
