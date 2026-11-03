# Search Techniques in Modern Database Systems
### An Empirical Analysis Across the RUM Trade-Off Space

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Course: CO5173](https://img.shields.io/badge/Course-CO5173%20Data%20Engineering-red.svg)](https://www.cse.hcmut.edu.vn/)
[![Institution: HCMUT](https://img.shields.io/badge/Institution-HCMUT%20--%20VNU--HCM-00529B.svg)](https://www.hcmut.edu.vn/)

---

## Academic Information

**Institution:** Vietnam National University Ho Chi Minh City – Ho Chi Minh City University of Technology (HCMUT)  
**Faculty:** Faculty of Computer Science and Engineering  
**Program:** Master of Science in Computer Science  
**Course:** Data Engineering (CO5173)  
**Course Instructor:** Assoc. Prof. Tran Minh Quang  

**Authors & Research Contributors:**
- **Nguyen Dinh Hoang Son** (Student ID: `2670362`) – `pason.dev@gmail.com`
- **Nguyen Doan Phuc An** (Student ID: `2670249`) – `annguyendoan`

**Repository:** [https://github.com/Pasonnn/co5173-modern-database-search-techniques](https://github.com/Pasonnn/co5173-modern-database-search-techniques)

---

## 1. Abstract & Motivation

In production database systems, a "one-size-fits-all" indexing architecture does not exist. Relational OLTP engines, distributed column stores, log search platforms, and analytical accelerators adopt fundamentally divergent data structures to resolve the **Fundamental Search Problem**:

$$\text{Brute-force Scan } O(N) \quad \longleftrightarrow \quad \text{Tree Traversal } O(\log N) \quad \longleftrightarrow \quad \text{Model Function Mapping } O(1)$$

This research repository provides a clean, educational, and empirically testable ground-up implementation of the five core indexing paradigms powering modern database engines:

1. **B+ Tree:** Comparison-based pointer hierarchy with leaf chaining (*MySQL InnoDB*).
2. **Log-Structured Merge-Tree (LSM-Tree):** Write-optimized multi-run architecture with Bloom filters and compaction (*RocksDB, Apache Cassandra*).
3. **Lexical Inverted Index & BM25:** Term dictionaries, posting lists, and relevance scoring (*Apache Lucene, Elasticsearch*).
4. **Static Recursive Model Index (RMI):** Cumulative Distribution Function (CDF) approximation via multi-stage linear models (*BOURBON engine*).
5. **Dynamic Updatable Learned Index (ALEX):** Gapped-array leaf data nodes with exponential search and dynamic splitting.

---

## 2. The Storage Engine Trade-Off Space: The RUM Conjecture

Storage engines are strictly constrained by the **RUM Conjecture** (Athanassoulis et al., 2016). Optimizing two dimensions forces a compromise on the third:

```
                            Read Amplification (R)
                                    /\
                                   /  \
                           B+ Tree/    \ Static RMI
                                 /      \
                                /  RUM   \
                               /  Trade-  \
                              /   Space    \
                             /              \
        Update Amplification (U) ------------ Memory/Space Amplification (M)
              (LSM-Tree)                               (Dynamic ALEX)
```

- **Read Amplification ($R$):** Ratio of bytes/pages read from storage per logical query byte retrieved.
- **Update Amplification ($U$):** Ratio of bytes written to storage per logical update byte ingested.
- **Memory/Space Amplification ($M$):** Relative memory overhead consumed by tree pointers, fence pointers, hash maps, or gap buffers.

### Master Architectural Comparison Matrix

| Architecture | Primary Case Study | Read Amp ($R$) | Update Amp ($U$) | Memory Overhead ($M$) | Range Query Efficiency | Primary Workload Target |
|---|---|---|---|---|---|---|
| **B+ Tree** | MySQL InnoDB | $O(\log_B N)$ | High ($O(B)$ page rewrites) | Moderate (~87 B/key) | Excellent ($O(K)$ leaf chain) | ACID point lookups & transactional ranges |
| **LSM-Tree** | RocksDB / Cassandra | Higher (Multi-SSTable checks) | Low ($O(1)$ sequential appends) | Low (~150 B/key with filter) | Moderate (Multi-way merge scan) | High-concurrency sequential ingestion |
| **Inverted Index** | Lucene / Elasticsearch | $O(1)$ term lookup + scan | High (Posting updates) | High (Term dict + postings) | Specialized (BKD tree ranges) | Multi-attribute text & lexical retrieval |
| **Static RMI** | BOURBON / SSTable | Near $O(1)$ (Bounded $\pm \epsilon$) | Extreme ($O(N)$ full retraining) | Minimal (~3.5 B/key) | Excellent ($O(K)$ array slice) | Read-heavy immutable columnar/OLAP |
| **Dynamic ALEX** | Updatable Learned DB | Near $O(1)$ (Galloping search) | Low local shifts / split spikes | Low (~94 B/key with gaps) | High ($O(K)$ partition scan) | Cache-conscious point-read workloads |

---

## 3. Core Search Techniques & Production Implementations

### 3.1. Comparison-Based Pointers: B+ Tree
- **Production Anchor:** MySQL InnoDB Storage Engine.
- **Data Layout:** Slotted pages with fanout factor $B$. Internal nodes store routing keys and child page pointers; leaf nodes store sorted key-value payloads and form a bidirectional linked list.
- **Write Mechanics:** In-place page modifications. Overflows trigger recursive node splits and Write-Ahead Logging (WAL) flushes.
- **Read Path:** Root-to-leaf traversal down height $h \approx \log_B N$, executing binary search within each page node.

### 3.2. Write-Optimized Log-Structured Search: LSM-Tree
- **Production Anchor:** Apache Cassandra and RocksDB.
- **Data Layout:** In-memory sorted buffer (**MemTable**), sequential append-only **CommitLog**, and tiered on-disk immutable **SSTables** (Sorted String Tables).
- **Fast-Fail Filtering:** Each SSTable is paired with an in-memory **Bloom Filter** ($O(1)$ negative fast-fail check) to prevent reading non-existent keys.
- **Write Path:** Zero random in-place I/O; writes append to MemTable in RAM and flush sequentially to Level 0 SSTables.
- **Maintenance:** Background multi-way merge (**Compaction**) reconciles duplicate keys and purges deleted records (**Tombstones**).

### 3.3. Lexical & Multi-Attribute Search: Inverted Index & BKD Trees
- **Production Anchor:** Apache Lucene and Elasticsearch.
- **Layout:** Ingestion tokenization, sorted **Term Dictionary** (modeled in Lucene via Finite State Transducers), and ordered **Posting Lists** (`doc_id`, `term_frequency`).
- **Scoring & Boolean Logic:** Boolean operations (AND / OR) compute intersections and unions across posting lists. Relevance ranking is evaluated via **Okapi BM25**:

$$\text{Score}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t, D) \cdot (k_1 + 1)}{f(t, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

### 3.4. Static Function Approximation: Recursive Model Index (RMI)
- **Production Anchor:** BOURBON (learned SSTable fence pointers in LSM engines).
- **Theoretical Basis:** Treat indexing as a Cumulative Distribution Function (CDF) approximation:

$$\text{pos} \approx \text{CDF}(\text{key}) \times N$$

- **Hierarchy:** Two-stage regression spline. The root model directs the key to one of $M$ leaf linear models. The leaf model predicts slot $\hat{p}$ with bounded error $\pm \epsilon$, followed by local binary search.
- **Trade-off:** Compresses pointer overhead down to ~3.5 Bytes/key, but requires full retraining on key insertions.

### 3.5. Dynamic Updatable Learned Indexing: The ALEX Architecture
- **Production Anchor:** Adaptive Learned Index (ALEX, Ding et al., SIGMOD 2020).
- **Two-Tier Layout:** Root linear router routes keys to leaf **Data Nodes**.
- **Gapped-Array Mechanism:** Leaf nodes maintain calculated empty slots (**GAPs**) interspersed between keys. Inserts are absorbed locally by shifting adjacent elements to the nearest gap without shifting the entire node.
- **Search Mechanics:** Model-predicted slot targeting paired with **Exponential (Galloping) Search** to maximize CPU L1/L2 cache hit rates.

---

## 4. Repository Structure

```
co5173-modern-database-search-techniques/
├── src/
│   ├── common.py          # OperationStats, BaseIndex protocol, memory estimator
│   ├── bplus_tree.py      # B+ Tree implementation with leaf chaining and node splits
│   ├── lsm_tree.py        # LSM-Tree with MemTable, BloomFilter, SSTables & compaction
│   ├── inverted_index.py  # Inverted Index with tokenization, BM25 scoring & boolean ops
│   ├── learned_rmi.py     # Static Recursive Model Index with bounded error searches
│   └── learned_alex.py    # Dynamic ALEX with gapped arrays & galloping scan
├── benchmarks/
│   ├── run.py             # Empirical benchmark measuring throughput, latency, footprint
│   ├── stress_test.py     # Section 4.2 workload stress-testing suite (skew, ingestion, text, compression)
│   └── results/           # Persisted benchmark and stress-test output logs
├── tests/
│   └── test_all.py        # Automated test suite verifying correctness of all 5 engines
├── report/
│   ├── outline.md         # Comprehensive report syllabus outline
│   ├── final_report.md    # Complete master-level technical research report
│   ├── slides_content.md  # 24-slide presentation content with speaker scripts & analogies
│   └── figures/           # Vector architecture SVGs & figure provenance catalog (sources.txt)
├── scripts/
│   └── generate_figures.py # Script generating SVG architecture and benchmark diagrams
├── Makefile               # Targets: test, bench, stress, clean
├── run.sh                 # Standard execution helper script
├── requirements.txt       # Minimal dependency configuration (standard-library first)
├── CITATION.cff           # Standard academic citation metadata
├── LICENSE                # MIT License
└── README.md              # Research & architecture guide
```

---

## 5. Quickstart & Empirical Reproduction

### Prerequisites
- Python 3.10+ (Standard library only; zero mandatory third-party packages required).

### 1. Run Automated Test Verification
Run the assertion-based test suite covering point lookups, updates, deletions, range scans, and edge cases across all five engines:
```bash
make test
# OR: python3 tests/test_all.py
```
*Expected result:*
```
ALL 5 SEARCH TECHNIQUE SELF-CHECKS PASSED SUCCESSFULLY.
```

### 2. Run Comparative Empirical Benchmarks
Execute side-by-side performance evaluation measuring ingestion throughput, point lookup latency, range query throughput, and memory footprint:
```bash
make bench
# OR: ./run.sh bench
```

### 3. Run Workload Stress-Testing Suite (Section 4.2)
Execute empirical stress tests evaluating Zipfian skew, high-throughput write ingestion, posting list intersections, and scale compression:
```bash
make stress
# OR: ./run.sh stress
```

*Sample empirical benchmark output (N=10,000 real Geoname keys, 5 repeated trials):*
```
=========================================================================================================
Engine         | Ingest (ops/s) (µ ± σ)     | Lookup (µs) (µ ± σ)      | Range (ops/s) (µ ± σ)  | Bytes/Key 
---------------------------------------------------------------------------------------------------------
B+ Tree        |    1176869 ± 91008         |     0.77 ± 0.07          |    25754 ± 2932        |      90.1
LSM-Tree       |      19731 ± 6317          |    16.03 ± 8.83          |     1599 ± 448         |     153.7
Static RMI     |     840904 ± 131420        |     1.86 ± 0.25          |    15007 ± 2556        |       1.4
Dynamic ALEX   |      86739 ± 14632         |     6.44 ± 1.23          |      698 ± 190         |     104.3
=========================================================================================================

--- Lexical Inverted Index on Real Text Corpus (BM25 + Boolean Search) ---
Indexed 1,655 real documents in 58.86 ms
BM25 Top Match: Doc ID 131 (Score: 11.425)
BM25 Search Latency (5 runs): 266.50 ± 105.36 µs
Boolean AND ['life', 'time'] matched 2 documents: [196, 298]
```

---

## 6. Workload Stress-Testing Insights

1. **Storage Compression in Learned Models:**
   - Static RMI achieves **0.7 to 1.4 Bytes/key**, representing a **>64× to 120× memory reduction** compared to traditional B+ Tree pointer graphs (90.1 Bytes/key).
2. **Ingestion Bottlenecks:**
   - In-memory B+ Trees achieve high throughput for small datasets, but degrade rapidly under random I/O write amplification when pages exceed buffer pool limits. LSM-Trees amortize updates via sequential MemTable appends and background compaction.
3. **Point Read-Heavy Workloads:**
   - B+ Trees deliver deterministic **0.77 ± 0.07 µs** lookups (dropping to **0.65 µs** under Zipfian query skew). Static RMI delivers **1.86 ± 0.25 µs** with zero pointer graphs. Dynamic ALEX trades local gap shift maintenance for near-$O(1)$ model-guided galloping lookups.
4. **Lexical vs. Primary-Key Retrieval:**
   - Inverted indexing achieves a **43.3× speedup** over brute-force relational scanning on multi-term boolean queries, pruning non-matching documents in $O(1)$ term lookup time.

---

## 7. Academic References & Bibliography

1. **Athanassoulis, M., Kester, M. S., Maas, L. M., Stoica, R., Idreos, S., Ailamaki, A., & Callaghan, M.** (2016). *Designing Access Methods: The RUM Conjecture.* In Proceedings of the 19th International Conference on Extending Database Technology (EDBT), pp. 461–466. [DOI: 10.5441/002/edbt.2016.42](https://doi.org/10.5441/002/edbt.2016.42)
2. **Bayer, R., & McCreight, E.** (1972). *Organization and Maintenance of Large Ordered Indices.* Acta Informatica, 1(3), pp. 173–189.
3. **O'Neil, P., Cheng, E., Gawlick, D., & O'Neil, E.** (1996). *The Log-Structured Merge-Tree (LSM-Tree).* Acta Informatica, 33(4), pp. 351–385. [DOI: 10.1007/s002360050048](https://doi.org/10.1007/s002360050048)
4. **Robertson, S., & Zaragoza, H.** (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval, 3(4), pp. 333–389. [DOI: 10.1561/1500000019](https://doi.org/10.1561/1500000019)
5. **Kraska, T., Beutel, A., Chi, E. H., Dean, J., & Polyzotis, N.** (2018). *The Case for Learned Index Structures.* In Proceedings of the 2018 ACM SIGMOD International Conference on Management of Data, pp. 489–504. [DOI: 10.1145/3183713.3196909](https://doi.org/10.1145/3183713.3196909)
6. **Ding, J., Yu, U., Marcus, R., & Kraska, T.** (2020). *ALEX: An Updatable Adaptive Learned Index.* In Proceedings of the 2020 ACM SIGMOD International Conference on Management of Data, pp. 969–984. [DOI: 10.1145/3318464.3389711](https://doi.org/10.1145/3318464.3389711)
7. **Dai, Y., Ji, H., Liu, C., & Zhang, Y.** (2020). *From WiscKey to BOURBON: A Learned Index for Log-Structured Merge Trees.* In 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI 20), pp. 863–879.
8. **Graefe, G.** (2011). *Modern B-Tree Techniques.* Foundations and Trends in Databases, 3(4), pp. 203–402.

---

## 8. License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
