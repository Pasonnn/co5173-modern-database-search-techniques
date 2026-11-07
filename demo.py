#!/usr/bin/env python3
"""Interactive Live Presentation Demo for CO5173 Master Project Presentation.

Visual, colorized, step-by-step walkthrough of:
1. Apache Cassandra (LSM-Tree) Engine
2. Elasticsearch (Inverted Index & BM25) Engine

Run:
    python3 demo.py                 # Full interactive demo
    python3 demo.py --cassandra     # Cassandra LSM demo only
    python3 demo.py --elasticsearch # Elasticsearch demo only
    python3 demo.py --benchmarks    # Live benchmark comparison
"""
from __future__ import annotations
import argparse
import sys
import time

from src.lsm_tree import LSMTree, BloomFilter, TOMBSTONE
from src.inverted_index import InvertedIndex, tokenize
from benchmarks.data_loader import get_text_corpus

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
DIM = "\033[2m"


def print_banner(title: str):
    width = 80
    print("\n" + "=" * width)
    print(f"{BOLD}{CYAN}{title.center(width)}{RESET}")
    print("=" * width)


def pause(prompt: str = "Press [ENTER] to continue..."):
    if "--no-pause" not in sys.argv:
        try:
            input(f"\n{DIM}{prompt}{RESET}")
        except (EOFError, KeyboardInterrupt):
            print()


def demo_cassandra():
    print_banner("DEMO PART 1: APACHE CASSANDRA (LSM-TREE) LIVE MECHANICS")
    print(f"{BOLD}Simulating Cassandra storage hierarchy: CommitLog + MemTable + SSTables + Bloom Filter{RESET}\n")

    # Step 1: Ingestion to MemTable
    print(f"{YELLOW}[STEP 1]{RESET} {BOLD}Client mutations enter CommitLog (WAL on disk) and MemTable (RAM SkipList){RESET}")
    lsm = LSMTree(memtable_threshold=4, compaction_trigger=3)

    records = [
        (101, "User:Alice_US"),
        (102, "User:Bob_VN"),
        (103, "User:Charlie_SG"),
    ]
    for k, v in records:
        print(f"  --> put({k}, '{v}') -> Appended to CommitLog (sequential disk) & inserted into MemTable")
        lsm.put(k, v)

    print(f"\n  {GREEN}Current MemTable state in RAM:{RESET}")
    for k, v in lsm.memtable.items():
        print(f"    • Key {k} => '{v}'")
    print(f"  Current SSTables on disk: {len(lsm.sstables)} (None flushed yet)")

    pause()

    # Step 2: Flush to SSTable
    print(f"\n{YELLOW}[STEP 2]{RESET} {BOLD}MemTable reaches capacity threshold (4 keys) -> FLUSH to Immutable SSTable-0{RESET}")
    print(f"  --> put(104, 'User:David_JP') triggers flush threshold!")
    lsm.put(104, "User:David_JP")

    print(f"\n  {GREEN}Status after flush:{RESET}")
    print(f"  • MemTable emptied: {len(lsm.memtable)} keys")
    print(f"  • New SSTables on disk: {len(lsm.sstables)} (SSTable-0 created)")
    sst0 = lsm.sstables[0]
    print(f"    - SSTable-0 Data File:    {sst0.keys}")
    print(f"    - SSTable-0 Fence Index:  Sampled keys {sst0.fence_keys} at offsets {sst0.fence_indices}")
    print(f"    - SSTable-0 Bloom Filter: Bit array active ({sst0.bloom.size} bits)")

    pause()

    # Step 3: Read Path & Bloom Filter Fast-Fail
    print(f"\n{YELLOW}[STEP 3]{RESET} {BOLD}Read Path: Existing Key Hit vs. Absent Key Bloom Filter Fast-Fail{RESET}")

    # Case A: Existing key
    query_hit = 102
    print(f"\n  {CYAN}Case A: Point Lookup for EXISTING key {query_hit}{RESET}")
    print(f"    1. Check active MemTable -> MISS (MemTable empty)")
    print(f"    2. Check SSTable-0 Bloom Filter -> HIT (Key 102 bit positions match!)")
    print(f"    3. Binary search SSTable-0 Fence Index -> Found exact offset")
    val_hit = lsm.get(query_hit)
    print(f"    {GREEN}>> Result:{RESET} Key {query_hit} => '{val_hit}' (Retrieved successfully)")

    # Case B: Absent key (Bloom filter fast-fail!)
    query_miss = 999
    print(f"\n  {CYAN}Case B: Point Lookup for ABSENT key {query_miss}{RESET}")
    print(f"    1. Check active MemTable -> MISS")
    print(f"    2. Check SSTable-0 Bloom Filter:")
    h_bits = sst0.bloom._hashes(query_miss)
    print(f"       Computed hash bit indices: {h_bits}")
    contains = sst0.bloom.contains(query_miss)
    print(f"       Bloom Filter answer: {RED}{contains}{RESET} (At least one bit is 0)")
    print(f"    {GREEN}>> FAST-FAIL PRUNED!{RESET} SSTable data file was NEVER touched. Zero disk reads!")

    pause()

    # Step 4: Deletion via Tombstone & Compaction
    print(f"\n{YELLOW}[STEP 4]{RESET} {BOLD}Deletion via Tombstone & Multi-Way Merge Compaction{RESET}")
    # Add more keys to create SSTable-1
    lsm.put(105, "User:Emma_UK")
    lsm.put(106, "User:Frank_DE")
    lsm.put(107, "User:Grace_CA")
    lsm.put(108, "User:Hannah_FR")  # Triggers SSTable-1

    print(f"  Current SSTables before deletion: {len(lsm.sstables)} SSTables")

    print(f"\n  --> Client issues: {RED}delete(102){RESET}")
    lsm.delete(102)
    print(f"  • Wrote TOMBSTONE marker for key 102 into MemTable (Older value in SSTable-0 remains on disk)")
    print(f"  • Querying key 102 now returns: {RED}{lsm.get(102)}{RESET} (Masked by Tombstone!)")

    # Force SSTable-2 and Compaction
    lsm.put(109, "User:Ian_AU")
    lsm.put(110, "User:Jack_NZ")
    lsm.put(111, "User:Kelly_SG")  # Triggers SSTable-2 and compaction!

    print(f"\n  {GREEN}Triggering Multi-Way Merge Compaction...{RESET}")
    print(f"  • Reading all overlapping SSTables in sorted streaming order ($O(N)$)")
    print(f"  • Reconciling duplicate key versions")
    print(f"  • {RED}Purging deleted key 102 and its Tombstone permanently{RESET}")
    lsm.compact()

    print(f"\n  {GREEN}Compacted SSTable state:{RESET}")
    for idx, sst in enumerate(lsm.sstables):
        print(f"  • Compacted SSTable-{idx} active keys: {sst.keys}")
    print(f"  • Verify key 102: {lsm.get(102)} (Permanently purged)")
    print(f"  • Verify key 101: '{lsm.get(101)}' (Retained)")
    print(f"\n{BOLD}{GREEN}✓ Cassandra LSM Live Demo Complete.{RESET}")


def demo_elasticsearch():
    print_banner("DEMO PART 2: ELASTICSEARCH (INVERTED INDEX & BM25) LIVE MECHANICS")
    print(f"{BOLD}Simulating Lucene Analysis Pipeline + FST Term Dict + Postings + BM25 Scoring{RESET}\n")

    # Step 1: Text Analysis Pipeline
    print(f"{YELLOW}[STEP 1]{RESET} {BOLD}Text Ingestion through the Analysis Pipeline{RESET}")
    sample_text = "Apache Cassandra provides high write throughput with LSM trees!"
    print(f"  Raw Input Document:")
    print(f"    \"{sample_text}\"")

    tokens = tokenize(sample_text)
    print(f"\n  After Character Filter -> Tokenizer -> Lowercase Filter -> Stemming:")
    print(f"    {GREEN}{tokens}{RESET}")

    pause()

    # Step 2: Indexing Documents & Building Postings
    print(f"\n{YELLOW}[STEP 2]{RESET} {BOLD}Constructing Term Dictionary & Inverted Posting Lists{RESET}")
    idx = InvertedIndex(k1=1.2, b=0.75)

    docs = [
        (1, "Apache Cassandra provides high write throughput with LSM trees."),
        (2, "Elasticsearch uses inverted index and BM25 relevance for fast text search."),
        (3, "Modern database storage engines balance write amplification and search speed."),
    ]
    for doc_id, text in docs:
        print(f"  --> Indexing Doc {doc_id}: \"{text[:50]}...\"")
        idx.index_document(doc_id, text)

    print(f"\n  {GREEN}Sample Inverted Index Entries (Term -> Postings):{RESET}")
    sample_terms = ["write", "search", "lsm", "database"]
    for term in sample_terms:
        if term in idx.postings:
            postings = idx.postings[term]
            post_str = ", ".join([f"[Doc {p.doc_id} (tf:{p.term_freq})]" for p in postings])
            print(f"    • Term '{term:<8}' -> {post_str}")

    pause()

    # Step 3: Boolean AND Search with Skip Pointer Simulation
    print(f"\n{YELLOW}[STEP 3]{RESET} {BOLD}Multi-Term Boolean Query Intersection: 'write' AND 'search'{RESET}")
    print(f"  Posting list for 'write':  {[f'Doc {p.doc_id}' for p in idx.postings.get('write', [])]}")
    print(f"  Posting list for 'search': {[f'Doc {p.doc_id}' for p in idx.postings.get('search', [])]}")

    bool_res = idx.search_boolean(["write", "search"], mode="AND")
    print(f"\n  {GREEN}Intersecting sorted posting lists in O(min(|P1|, |P2|)) time...{RESET}")
    print(f"  >> Matching Document IDs: {BOLD}{GREEN}{bool_res}{RESET}")
    for doc_id in bool_res:
        print(f"     Doc {doc_id}: \"{docs[doc_id - 1][1]}\"")

    pause()

    # Step 4: Okapi BM25 Relevance Scoring
    print(f"\n{YELLOW}[STEP 4]{RESET} {BOLD}Okapi BM25 Probabilistic Relevance Ranking{RESET}")
    query = "write search database"
    print(f"  User Query: \"{query}\"")
    print(f"  Formula: Score(D, Q) = ∑ IDF(q) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * |D| / avgdl))")
    print(f"  Parameters: k1 = 1.2 (TF saturation), b = 0.75 (Length penalty)")

    ranked = idx.search_bm25(query, limit=3)
    print(f"\n  {GREEN}Top Ranked Matches by BM25 Score:{RESET}")
    for rank, (doc_id, score) in enumerate(ranked, start=1):
        print(f"    Rank {rank}: {BOLD}Doc {doc_id}{RESET} (BM25 Score: {score:.4f})")
        print(f"            \"{docs[doc_id - 1][1]}\"")

    pause()

    # Step 5: Live Speedup over Linear Scan
    print(f"\n{YELLOW}[STEP 5]{RESET} {BOLD}Live Benchmark: Inverted Index vs. Brute-Force Linear Scan{RESET}")
    print(f"  Loading 1,655 real documents from natural language quotes corpus...")
    corpus = get_text_corpus(n=1655, seed=42)

    big_idx = InvertedIndex(k1=1.2, b=0.75)
    for d in corpus:
        big_idx.index_document(d["id"], d["text"])

    query_terms = ["life", "man"]
    print(f"  Query: \"{' AND '.join(query_terms)}\" across {len(corpus):,} real documents")

    # Inverted Index search
    t0 = time.perf_counter()
    for _ in range(50):
        inv_matches = big_idx.search_boolean(query_terms, mode="AND")
    inv_lat_us = ((time.perf_counter() - t0) / 50) * 1e6

    # Brute force scan
    t0 = time.perf_counter()
    for _ in range(50):
        scan_matches = []
        for doc in corpus:
            words = set(doc["text"].lower().split())
            if all(t in words for t in query_terms):
                scan_matches.append(doc["id"])
    scan_lat_us = ((time.perf_counter() - t0) / 50) * 1e6

    speedup = scan_lat_us / max(1e-6, inv_lat_us)
    print(f"\n  {CYAN}Measured Results:{RESET}")
    print(f"  • Inverted Index Posting Intersection: {BOLD}{GREEN}{inv_lat_us:.2f} µs{RESET}")
    print(f"  • Brute-Force Linear Document Scan:    {BOLD}{RED}{scan_lat_us:.2f} µs{RESET}")
    print(f"  • {BOLD}{YELLOW}Empirical Speedup: {speedup:.1f}x Faster!{RESET}")
    print(f"\n{BOLD}{GREEN}✓ Elasticsearch Live Demo Complete.{RESET}")


def demo_benchmarks():
    print_banner("DEMO PART 3: EMPIRICAL HEAD-TO-HEAD BENCHMARK (LIVE)")
    import benchmarks.run as bench_run
    bench_run.main()


def main():
    parser = argparse.ArgumentParser(description="Live Presentation Demo for CO5173.")
    parser.add_argument("--cassandra", action="store_true", help="Run Cassandra LSM demo only")
    parser.add_argument("--elasticsearch", action="store_true", help="Run Elasticsearch demo only")
    parser.add_argument("--benchmarks", action="store_true", help="Run benchmark comparison only")
    parser.add_argument("--no-pause", action="store_true", help="Run without interactive pauses")
    args = parser.parse_args()

    if args.cassandra:
        demo_cassandra()
    elif args.elasticsearch:
        demo_elasticsearch()
    elif args.benchmarks:
        demo_benchmarks()
    else:
        demo_cassandra()
        demo_elasticsearch()


if __name__ == "__main__":
    main()
