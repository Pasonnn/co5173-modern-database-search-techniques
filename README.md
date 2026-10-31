# Search Techniques in Modern Database Systems

**Course:** Data Engineering (CO5173) – Vietnam National University Ho Chi Minh City, HCMUT  
**Instructor:** Assoc. Prof. Tran Minh Quang  
**Authors:**
- Nguyen Dinh Hoang Son (Student ID: 2670362)
- Nguyen Doan Phuc An (Student ID: 2670249)

---

## 1. Project Overview

Modern database engines diverge in their internal search indexing architectures because no single data structure can optimize simultaneously for reads, writes, and storage. This repository implements, benchmarks, and analyzes the five foundational database search architectures:

1. **B+ Tree** (*Comparison-Based Pointer Architecture* – MySQL InnoDB)
2. **LSM-Tree** (*Log-Structured Merge Architecture* – Apache Cassandra / RocksDB)
3. **Inverted Index + BM25** (*Lexical Multi-Attribute Retrieval* – Apache Lucene / Elasticsearch)
4. **Static RMI** (*Recursive Model Index / CDF Function Approximation* – BOURBON)
5. **Dynamic ALEX** (*Updatable Learned Index with Gapped Arrays*)

---

## 2. Theoretical Foundation: The RUM Conjecture

Every storage and indexing engine operates within the **RUM Trade-off Space**:
- **Read Amplification ($R$):** The number of disk/memory pages inspected per lookup.
- **Update Amplification ($U$):** The number of physical writes/bytes shifted per record update.
- **Memory/Space Amplification ($M$):** Overhead of internal pointers, fence indexes, or gap buffers.

```
                  Read (R)
                  /      \
                 /        \
         B+ Tree /          \ Static RMI
                /   Trade    \
               /    Space     \
              /                \
    Update (U) ----------------- Memory (M)
      (LSM-Tree)                 (Dynamic ALEX)
```

| Engine | Primary Workload | Read Amp ($R$) | Update Amp ($U$) | Memory Amp ($M$) | Core Mechanism |
|---|---|---|---|---|---|
| **B+ Tree** | OLTP ACID point/range | $O(\log_B N)$ | High (in-place page writes) | Moderate (tree pointers) | Page fanout & leaf chaining |
| **LSM-Tree** | High-throughput ingestion | Higher (multi-run checks) | $O(1)$ sequential appends | Low (dense SSTables) | MemTable + Bloom + Compaction |
| **Inverted Index** | Unstructured text search | $O(1)$ term lookup + list scan | High (posting updates) | High (term dict + postings) | Term Dictionary + BM25 + Posting Lists |
| **Static RMI** | Read-heavy immutable OLAP | $O(1)$ function + bounded scan | Extreme (full retrain) | Ultra-low (~3.5 B/key) | CDF hierarchical linear spline |
| **Dynamic ALEX** | Hybrid read-heavy with inserts | Near $O(1)$ | Low local shifts / spikes on split | Low-moderate (gapped capacity) | Gapped Data Nodes + Galloping Search |

---

## 3. Repository Structure

```
.
├── src/
│   ├── common.py          # Shared metrics telemetry & base protocol
│   ├── bplus_tree.py      # 3.1 B+ Tree engine (InnoDB model)
│   ├── lsm_tree.py        # 3.2 LSM-Tree engine (RocksDB/Cassandra model)
│   ├── inverted_index.py  # 3.3 Lexical Inverted Index & BM25 ranking (Elasticsearch model)
│   ├── learned_rmi.py     # 3.4 Static Learned Index / RMI (BOURBON model)
│   └── learned_alex.py    # 3.5 Dynamic Updatable Learned Index (ALEX model)
├── benchmarks/
│   └── run.py             # Empirical benchmark runner evaluating RUM metrics
├── tests/
│   └── test_all.py        # Correctness self-checks for all 5 indexing engines
├── report/
│   └── outline.md         # Full project report syllabus outline
├── requirements.txt       # Minimal dependencies (standard library first)
└── README.md
```

---

## 4. Quickstart

### Prerequisites
- Python 3.10+ (Standard library only; zero mandatory third-party dependencies).

### Run Correctness Verification
Execute the automated test suite verifying point lookups, updates, deletions, range scans, and edge cases across all five engines:
```bash
python3 tests/test_all.py
```

### Run Performance Benchmarks
Run side-by-side ingestion, point lookup, range scan, and memory footprint benchmarks:
```bash
python3 benchmarks/run.py
```

Sample output:
```
===============================================================================================
Engine           | Ingest (ops/s)   | Point Lookup (µs)  | Range (ops/s)   | Bytes/Key   
-----------------------------------------------------------------------------------------------
B+ Tree          |        1534388 |             0.42 |        232644 |       87.3
LSM-Tree         |          81289 |             2.75 |         15032 |      150.7
Static RMI       |         889099 |             0.88 |        185183 |        3.5
Dynamic ALEX     |         176308 |             4.06 |          7371 |       93.9
===============================================================================================
```

---

## 5. Linking to GitHub

To link this local repository to a new GitHub repository:

1. Create a repository on GitHub (e.g. `co5173-modern-database-search-techniques`).
2. Add the remote and push:
```bash
git remote add origin git@github.com:Pasonnn/<repo-name>.git
git push -u origin main
```
