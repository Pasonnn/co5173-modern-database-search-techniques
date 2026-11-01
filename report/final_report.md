# VIETNAM NATIONAL UNIVERSITY HO CHI MINH CITY
# HO CHI MINH CITY UNIVERSITY OF TECHNOLOGY
### FACULTY OF COMPUTER SCIENCE AND ENGINEERING

---

# COURSE PROJECT REPORT
## SEARCH TECHNIQUES IN MODERN DATABASE SYSTEMS
### An Architectural, Theoretical, and Empirical Analysis Across the RUM Trade-Off Space

**Course:** Data Engineering (CO5173)  
**Instructor:** Assoc. Prof. Tran Minh Quang  

**Authors & Research Contributors:**
- **Nguyen Dinh Hoang Son** (Student ID: `2670362`)
- **Nguyen Doan Phuc An** (Student ID: `2670249`)

**Location & Date:** Ho Chi Minh City – 2026  
**Repository:** [https://github.com/Pasonnn/co5173-modern-database-search-techniques](https://github.com/Pasonnn/co5173-modern-database-search-techniques)

---

## TABLE OF CONTENTS

- [1. Introduction to Database Indexing & Search Mechanics](#1-introduction-to-database-indexing--search-mechanics)
  - [1.1. The Fundamental Search Problem](#11-the-fundamental-search-problem)
  - [1.2. The Storage Engine Trade-Off Space: The RUM Conjecture](#12-the-storage-engine-trade-off-space-the-rum-conjecture)
  - [1.3. Taxonomy of Modern Index Architectures](#13-taxonomy-of-modern-index-architectures)
- [2. Architectural Paradigms: Why Systems Diverge](#2-architectural-paradigms-why-systems-diverge)
  - [2.1. The Workload-Driven Design Philosophy](#21-the-workload-driven-design-philosophy)
  - [2.2. Workload Alignment Across Production Engines](#22-workload-alignment-across-production-engines)
- [3. Core Search Techniques & Production Case Studies](#3-core-search-techniques--production-case-studies)
  - [3.1. Comparison-Based Pointers: B+ Tree Architecture (MySQL InnoDB)](#31-comparison-based-pointers-b-tree-architecture-mysql-innodb)
  - [3.2. Write-Optimized Log-Structured Search: LSM-Tree (RocksDB / Cassandra)](#32-write-optimized-log-structured-search-lsm-tree-rocksdb--cassandra)
  - [3.3. Lexical & Multi-Attribute Search: Inverted Index & BKD Trees (Lucene / Elasticsearch)](#33-lexical--multi-attribute-search-inverted-index--bkd-trees-lucene--elasticsearch)
  - [3.4. Static Function Approximation: Static Learned Indexes (RMI / BOURBON)](#34-static-function-approximation-static-learned-indexes-rmi--bourbon)
  - [3.5. Dynamic Updatable Learned Indexing: The ALEX Architecture](#35-dynamic-updatable-learned-indexing-the-alex-architecture)
- [4. Empirical Evaluation & Comparative Analysis](#4-empirical-evaluation--comparative-analysis)
  - [4.1. Master Search Technology Comparison Matrix](#41-master-search-technology-comparison-matrix)
  - [4.2. Workload Stress-Testing Insights](#42-workload-stress-testing-insights)
- [5. Architectural Synthesis & Future Horizons](#5-architectural-synthesis--future-horizons)
  - [5.1. System Selection Framework (RUM Decision Heuristics)](#51-system-selection-framework-rum-decision-heuristics)
  - [5.2. Emerging Hybrid Designs](#52-emerging-hybrid-designs)
- [References](#references)

---

## 1. Introduction to Database Indexing & Search Mechanics

### 1.1. The Fundamental Search Problem
At the physical storage layer of database management systems (DBMS), data retrieval reduces to locating records matching given predicates: point queries ($K = k$), range queries ($k_{low} \le K \le k_{high}$), or lexical pattern matches. Without auxiliary structures, locating a record in an unsorted table requires a full relation scan of $O(N)$ computational and I/O complexity.

Primary index structures trade auxiliary storage space and maintenance overhead during updates to transform the access path:
- **Brute-Force Scan:** $O(N)$ sequential page reads. Zero index storage overhead, zero update cost, but catastrophic read performance on large datasets.
- **Comparison-Based Traversal:** $O(\log N)$ or $O(\log_B N)$ step-wise decision paths through hierarchical tree pointers (e.g., B+ Trees).
- **Direct Hash/Function Mapping:** $O(1)$ amortized lookup via hash functions or learned Cumulative Distribution Function (CDF) approximations.

### 1.2. The Storage Engine Trade-Off Space: The RUM Conjecture
The design of access methods is governed by the **RUM Conjecture** (Athanassoulis et al., 2016). The conjecture states that optimizing for two of the three fundamental database overheads—**Read Amplification ($R$)**, **Update Amplification ($U$)**, and **Memory/Space Amplification ($M$)**—inevitably compromises the third.

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

1. **Read Amplification ($R$):** The ratio between the physical data read from disk/memory and the actual logical payload returned to the query.
2. **Update Amplification ($U$):** The ratio between the physical bytes written to durable storage and the uncompressed logical update size.
3. **Memory/Space Amplification ($M$):** The auxiliary memory overhead required by pointers, hash buckets, gap buffers, or fence indexes over the raw data size.

### 1.3. Taxonomy of Modern Index Architectures
Modern indexing structures fall into four overarching architectural paradigms:
1. **Comparison-Based Tree Indexes:** B+ Tree, B-link Tree, Masstree. Utilize strict key comparisons and pointer links; standard in transactional relational DBMS.
2. **Log-Structured Multi-Run Engines:** LSM-Trees, StepMerge, Fractal Trees. Sacrifice point read efficiency to absorb massive write throughput via sequential log appends and deferred merges.
3. **Lexical Inverted Indexes & Multi-Dimensional Partitioning:** Inverted Posting Lists, Finite State Transducers (FSTs), and BKD Trees. Optimize tokenized search and multi-attribute geometric bounding boxes.
4. **Learned Function Approximations:** Recursive Model Indexes (RMI), PGM-index, ALEX. Replace explicit comparison pointers with functional approximations of the data distribution.

---

## 2. Architectural Paradigms: Why Systems Diverge

### 2.1. The Workload-Driven Design Philosophy
In database engine design, there is no universal optimal access method. An engine optimized for transactional debit/credit point reads cannot simultaneously sustain millions of sensor telemetry writes per second without latency degradation. System architects diverge based on workload-driven priorities:
- **Read-dominated vs. Write-dominated workloads:** Favoring low $R$ versus low $U$.
- **Point queries vs. Range scans vs. Multi-predicate text filtering:** Demanding sorted ordering, tokenized inverted lists, or multidimensional trees.
- **Hardware constraints:** In-memory CPU cache locality, NVMe SSD sequential vs. random I/O asymmetry, and DRAM footprint costs.

### 2.2. Workload Alignment Across Production Engines
- **High-concurrency sequential ingestion (Apache Cassandra / RocksDB):** Heavy append rates exceed disk random write bandwidth. LSM-Trees convert random writes into sequential disk flushes.
- **High-dimensional unstructured text & log search (Elasticsearch / Apache Lucene):** Queries filter arbitrarily on combinations of words and ranges. Inverted index posting lists with BM25 ranking provide sub-second retrieval across unstructured text corpus.
- **ACID point-and-range transactional workloads (MySQL InnoDB):** Predictable read latencies, fine-grained row-level locking, and high-performance range scans make B+ Trees the gold standard for relational OLTP.
- **In-memory cache-conscious analytical acceleration (Learned Models):** Read-heavy analytical workloads running on large memory nodes leverage learned regression models to replace deep pointer chains with direct arithmetic slot prediction.

---

## 3. Core Search Techniques & Production Case Studies

### 3.1. Comparison-Based Pointers: B+ Tree Architecture (MySQL InnoDB)
- **Data Layout:** Slotted pages with fanout factor $B$ (default 16KB in InnoDB). Internal nodes contain routing keys and child page pointers; leaf nodes contain sorted key-value tuples and are chained in a bidirectional linked list.
- **Search Mechanics:** Top-down traversal down height $h \approx \log_B N$. At each page, binary search locates the child pointer. Leaf-level range queries follow sibling pointers without re-traversing the root.
- **Write Path:** In-place page updates. If an insertion exceeds page capacity, the page splits into two half-filled pages ($B/2$ keys), propagating key promotions upward. Durability is maintained via Write-Ahead Logging (WAL / redo log).
- **Trade-off Profile:** Predictable $O(\log N)$ read latency and efficient $O(K)$ range scans, but suffers from high update amplification ($U$) due to full 16KB page rewrites for 10-byte modifications, and moderate pointer memory overhead ($M$).

### 3.2. Write-Optimized Log-Structured Search: LSM-Tree (RocksDB / Cassandra)
- **Storage Hierarchy:**
  - **MemTable:** In-memory sorted buffer (e.g., SkipList) absorbing concurrent writes.
  - **CommitLog (WAL):** Sequential append-only disk log ensuring durability.
  - **SSTables (Sorted String Tables):** Immutable disk files arranged in hierarchical levels ($L_0, L_1, \dots$).
- **Search Mechanics:** Point lookups inspect the active MemTable, followed by immutable MemTables, then disk SSTables from youngest to oldest. To prevent reading every SSTable on disk, each file is paired with an in-memory **Bloom Filter** providing an $O(1)$ fast-fail check for absent keys.
- **Write & Compaction:** Writes are pure sequential appends. When the MemTable fills, it flushes to disk as an immutable SSTable. In the background, **Compaction** performs multi-way merges across overlapping SSTables to discard superseded versions and purge **Tombstones** (delete markers).
- **Trade-off Profile:** Unmatched write ingestion throughput ($U \approx 1$), but elevated read amplification ($R$) across multiple SSTable runs and periodic compaction I/O latency spikes.

### 3.3. Lexical & Multi-Attribute Search: Inverted Index & BKD Trees (Lucene / Elasticsearch)
- **Data Layout:** Text analysis pipeline tokenizes and normalizes documents into terms. A **Term Dictionary** maps unique terms to ordered **Posting Lists** containing document IDs and term frequencies.
- **Search Execution & Relevance Scoring:** Boolean queries compute set intersections (AND) and unions (OR) using posting list skip-pointers or compressed bitsets (Roaring Bitmaps). Document relevance is computed via the **Okapi BM25** probabilistic scoring formula:

$$\text{Score}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t, D) \cdot (k_1 + 1)}{f(t, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

- **Multidimensional Search:** Lucene pairs inverted lists with **Block $k$-d trees (BKD Trees)** to execute range and geospatial bounding-box queries over numeric and coordinate data.
- **Trade-off Profile:** Enables fast sub-second multi-field unstructured queries, but incurs heavy term dictionary memory consumption and compute-intensive ingestion pipelines.

### 3.4. Static Function Approximation: Static Learned Indexes (RMI / BOURBON)
- **Core Concept:** A sorted primary key index can be viewed as approximating the data's Cumulative Distribution Function (CDF):

$$\text{pos} \approx \text{CDF}(\text{key}) \times N$$

- **Recursive Model Index (RMI):** A hierarchy of lightweight regression models (e.g., linear models: $y = \alpha \cdot x + \beta$). The root model routes key $k$ to a leaf model, which predicts slot $\hat{p}$ with a mathematically bounded maximum error $[\hat{p} - \epsilon, \hat{p} + \epsilon]$. Final slot discovery completes via local binary search within the bounded window.
- **Industrial Fit:** RMI cannot accommodate dynamic inserts without full $O(N)$ retraining, making it unsuitable for primary OLTP tables. However, it fits **immutable SSTables** in LSM storage engines (as implemented in the BOURBON engine), replacing sparse fence pointers with negligible memory footprints.
- **Trade-off Profile:** Ultra-low memory footprint (~3.5 Bytes/key) and rapid point lookups, but completely non-updatable without retraining.

### 3.5. Dynamic Updatable Learned Indexing: The ALEX Architecture
- **Storage Layout:** Adaptive Learned Index (ALEX) organizes data into a two-tier hierarchy: internal routing nodes containing linear models and leaf **Data Nodes** holding sorted keys.
- **Gapped-Array Mechanism:** To absorb dynamic writes without shifting the entire array, ALEX introduces empty slots (**GAPs**) interspersed across the leaf array. New insertions shift only local adjacent keys into the nearest gap.
- **Search Mechanics:** The internal linear model routes the query to the correct Data Node. The leaf model projects the key directly onto the target slot. If the predicted slot does not hold the exact key, ALEX performs **Exponential (Galloping) Search**, leveraging CPU cache lines.
- **Trade-off Profile:** Delivers near-$O(1)$ point lookup latency and low memory footprint while supporting real-time inserts, but exhibits occasional latency spikes during node expansion, splitting, and local retraining.

---

## 4. Empirical Evaluation & Comparative Analysis

### 4.1. Master Search Technology Comparison Matrix

The table below summarizes empirical measurements obtained from benchmarking all five search architectures under identical test harness conditions:

| Search Architecture | Ingestion Throughput (ops/sec) | Point Lookup Latency ($\mu$s) | Range Query Throughput (ops/sec) | Memory Footprint (Bytes/Key) | Primary Workload Fit |
|---|---|---|---|---|---|
| **B+ Tree (InnoDB Model)** | 208,490 | 1.86 $\mu$s | 54,638 | 87.3 B/key | OLTP ACID point lookups & transactional ranges |
| **LSM-Tree (RocksDB Model)** | 15,727 | 12.98 $\mu$s | 3,143 | 150.7 B/key | Sequential append-heavy time-series & log ingestion |
| **Static RMI (BOURBON Model)** | 211,435 | 4.90 $\mu$s | 46,203 | **3.5 B/key** | Immutable analytical columnar & SSTable fence lookups |
| **Dynamic ALEX** | 34,106 | 17.46 $\mu$s | 1,754 | 93.9 B/key | Read-heavy workloads with moderate dynamic insertions |
| **Inverted Index (Lucene Model)** | Tokenized (~1,500 docs/s) | 227 $\mu$s (Multi-term AND) | N/A (BKD tree) | Variable (Posting lists) | Lexical unstructured text search & BM25 ranking |

---

### 4.2. Workload Stress-Testing Insights

#### 4.2.1. Point Read-Heavy Workloads (ALEX vs. B+ Tree Cache Efficiency)
- Under uniform random point queries, B+ Trees execute deterministic $\log_B N$ comparisons, achieving 1.08 $\mu$s latency.
- Dynamic ALEX projects directly to candidate slots, yielding 1.26 $\mu$s.
- Under skewed **Zipfian distributions ($\alpha = 1.3$)**, hot keys concentrate within upper cache lines, dropping B+ Tree latency to 0.77 $\mu$s and ALEX latency to 0.84 $\mu$s.

#### 4.2.2. High-Throughput Write Ingestion (LSM vs. B+ Tree)
- In-memory B+ Trees handle modest batches rapidly, but on physical disk, random page insertions trigger severe write amplification ($U = O(B)$) due to dirty page flushing and node splits.
- LSM-Trees decouple ingestion from disk sorting: writes hit sequential MemTable buffers, deferring I/O to background compaction threads and preserving high ingestion throughput across multi-gigabyte streams.

#### 4.2.3. Complex Filtering & Token Matching (Inverted Index vs. Scan)
- Evaluating a 3-term boolean conjunction (`database AND storage AND performance`) across 1,000 synthetic documents:
  - **Inverted Index Posting Intersection:** **227.12 $\mu$s** (252 matching documents).
  - **Linear Full Relation Scan:** **1,514.06 $\mu$s**.
  - **Speedup:** **6.7$\times$ faster** via posting list intersection, eliminating non-matching documents without reading document payloads.

#### 4.2.4. Storage and Index Size Compression (Learned Models vs. Pointer Graphs)
- **Static RMI** replaces internal child page pointers and fence keys with compact floating-point linear weights $(\alpha, \beta)$, achieving an index memory footprint of **0.8 to 3.5 Bytes/key**.
- This represents an **order-of-magnitude (up to 25$\times$) memory compression** over traditional pointer-based B+ Trees (~87.3 to 89.8 Bytes/key) and LSM-Trees with Bloom filters (~150.7 Bytes/key).

---

## 5. Architectural Synthesis & Future Horizons

### 5.1. System Selection Framework (RUM Decision Heuristics)

Database engine architects should apply the following decision heuristics when selecting or designing storage index engines:

1. **Prioritize Read Latency ($R \downarrow$) & Range Scans:**
   - Select **B+ Tree** if records require dynamic in-place updates with strict transactional concurrency and predictable millisecond latencies.
   - Select **Static RMI** if records are immutable (data warehouse partitions, SSTables) and DRAM footprint is constrained.
2. **Prioritize Write Throughput ($U \downarrow$):**
   - Select **LSM-Tree** if write ingestion rates exceed disk random I/O limits. Pair with tuned Bloom filters ($m/n \approx 10$ bits/key) to minimize point read degradation.
3. **Prioritize Lexical Relevance & Multi-Predicate Filtering:**
   - Select **Inverted Index with BM25** paired with **BKD Trees** for unstructured textual tokens and multidimensional numeric attributes.
4. **Prioritize In-Memory Footprint & Read Acceleration:**
   - Select **Dynamic ALEX** for in-memory analytical workloads where dataset distributions can be approximated via piecewise linear splines.

### 5.2. Emerging Hybrid Designs
The frontier of modern database research combines these paradigms into hybrid storage engines:
- **Learned-Cassandra / BOURBON:** Replacing traditional binary-search SSTable index blocks and fence pointers with compact RMI models, cutting LSM memory consumption by 80% while accelerating point lookups.
- **Columnar Learned Engines:** Integrating piecewise CDF approximations directly into Parquet/ORC file footers to prune data chunks without evaluating dictionary pages.
- **Hardware-Accelerated Inverted Indexes:** Utilizing GPU and SIMD AVX-512 vector instructions for parallel bitwise intersection of Roaring Bitmaps in real-time log analytics.

---

## References

1. **Athanassoulis, M., Kester, M. S., Maas, L. M., Stoica, R., Idreos, S., Ailamaki, A., & Callaghan, M.** (2016). *Designing Access Methods: The RUM Conjecture.* In Proceedings of the 19th International Conference on Extending Database Technology (EDBT), pp. 461–466.
2. **Bayer, R., & McCreight, E.** (1972). *Organization and Maintenance of Large Ordered Indices.* Acta Informatica, 1(3), pp. 173–189.
3. **O'Neil, P., Cheng, E., Gawlick, D., & O'Neil, E.** (1996). *The Log-Structured Merge-Tree (LSM-Tree).* Acta Informatica, 33(4), pp. 351–385.
4. **Robertson, S., & Zaragoza, H.** (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval, 3(4), pp. 333–389.
5. **Kraska, T., Beutel, A., Chi, E. H., Dean, J., & Polyzotis, N.** (2018). *The Case for Learned Index Structures.* In Proceedings of the 2018 ACM SIGMOD International Conference on Management of Data, pp. 489–504.
6. **Ding, J., Yu, U., Marcus, R., & Kraska, T.** (2020). *ALEX: An Updatable Adaptive Learned Index.* In Proceedings of the 2020 ACM SIGMOD International Conference on Management of Data, pp. 969–984.
7. **Dai, Y., Ji, H., Liu, C., & Zhang, Y.** (2020). *From WiscKey to BOURBON: A Learned Index for Log-Structured Merge Trees.* In 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI 20), pp. 863–879.
8. **Graefe, G.** (2011). *Modern B-Tree Techniques.* Foundations and Trends in Databases, 3(4), pp. 203–402.
