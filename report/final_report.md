# VIETNAM NATIONAL UNIVERSITY HO CHI MINH CITY
## HO CHI MINH CITY UNIVERSITY OF TECHNOLOGY
### FACULTY OF COMPUTER SCIENCE AND ENGINEERING

---

# SPECIALIZED MODERN DATABASE SEARCH ENGINES
## An Architectural, Theoretical, and Empirical Analysis: Apache Cassandra (LSM) vs. Elasticsearch (Inverted Index)

**Course:** Data Engineering (CO5173)  
**Instructor:** Assoc. Prof. Tran Minh Quang  

**Authors & Research Contributors:**
- **Nguyen Dinh Hoang Son** (Student ID: `2670362`)
- **Nguyen Doan Phuc An** (Student ID: `2670249`)

**Location & Date:** Ho Chi Minh City – 2026  
**Repository:** [https://github.com/Pasonnn/co5173-modern-database-search-techniques](https://github.com/Pasonnn/co5173-modern-database-search-techniques)

---

## EXECUTIVE SUMMARY

In early database architecture, general-purpose balanced pointer trees (such as the classical B+ Tree) served as the default storage and search abstraction. However, the explosion of specialized data volumes—ranging from hundreds of thousands of write mutations per second in IoT telemetry to multi-attribute unstructured text search across billions of log lines—has demonstrated the physical impossibility of a single universal indexing structure. 

This research project conducts an in-depth architectural, mathematical, and empirical investigation into the two preeminent specialized search paradigms of contemporary data engineering:
1. **Write-Optimized Log-Structured Search (Apache Cassandra / LSM-Tree):** Designed to maximize write ingestion throughput by transforming random discrete mutations into sequential memory appends, amortizing disk writes through immutable Sorted String Tables (SSTables) and asynchronous multi-way merge compaction.
2. **Lexical Posting Inversion & Probabilistic Relevance (Elasticsearch / Lucene Inverted Index):** Designed to deliver sub-millisecond multi-attribute text retrieval and boolean filtering via memory-compressed Finite State Transducers (FSTs), skip-pointer posting lists, and Okapi BM25 relevance scoring.

We formalize their design divergence through the theoretical lens of the **RUM Conjecture** (Athanassoulis et al., EDBT 2016), demonstrating mathematically how Cassandra minimizes **Update Amplification ($U$)** by tolerating bounded **Read Amplification ($R$)**, while Elasticsearch minimizes **Read Amplification ($R$)** for arbitrary keyword predicates at the expense of higher **Memory Amplification ($M$)** and segment merge overhead.

To validate these theoretical bounds, we constructed an end-to-end evaluation harness executed over real-world data: $N=10,000$ geographic primary keys from the global World Cities dataset and $1,655$ natural language documents from a real text corpus. Applying strict scientific measurement ($1$ warmup run discarded, $5$ repeated trials reporting mean and standard deviation $\mu \pm \sigma$):
- **Apache Cassandra (LSM)** sustained an ingestion throughput of **$85,624 \pm 6,126\ \text{ops/s}$** with an index memory overhead of just **$153.7\ \text{Bytes/key}$**, while in-memory Bloom filters pruned $100\%$ of unnecessary SSTable disk checks on negative queries, yielding a fast-fail latency of **$3.42 \pm 0.71\ \mu\text{s}$**.
- **Elasticsearch (Inverted Index)** achieved a **$71.5\times$ speedup** over linear scanning for multi-term boolean queries ($35.21\ \mu\text{s}$ vs. $2,515.55\ \mu\text{s}$) and computed top-$5$ Okapi BM25 ranked relevance in **$118.40 \pm 15.83\ \mu\text{s}$**.

Finally, we synthesize these findings into an actionable architectural decision framework and explore modern hybrid patterns—specifically Command Query Responsibility Segregation (CQRS) pairing Cassandra for ingestion with Elasticsearch for secondary search.

---

## TABLE OF CONTENTS

- [1. Introduction & Theoretical Foundation](#1-introduction--theoretical-foundation)
  - [1.1. The Divergence of Modern Database Search](#11-the-divergence-of-modern-database-search)
  - [1.2. The RUM Conjecture: Formalizing the Storage Trilemma](#12-the-rum-conjecture-formalizing-the-storage-trilemma)
  - [1.3. Scope and Research Objectives](#13-scope-and-research-objectives)
- [2. High-Throughput Write-Optimized Search: Apache Cassandra (LSM-Tree)](#2-high-throughput-write-optimized-search-apache-cassandra-lsm-tree)
  - [2.1. Workload Rationale: The Cost of In-Place Updates](#21-workload-rationale-the-cost-of-in-place-updates)
  - [2.2. Storage Hierarchy: CommitLog, MemTable, and SSTables](#22-storage-hierarchy-commitlog-memtable-and-sstables)
  - [2.3. The Read Path & Pruning: Bloom Filters and Fence Pointers](#23-the-read-path--pruning-bloom-filters-and-fence-pointers)
  - [2.4. Mutation Lifecycle: Tombstones and Multi-Way Merge Compaction](#24-mutation-lifecycle-tombstones-and-multi-way-merge-compaction)
- [3. Lexical & Multi-Attribute Search: Elasticsearch (Inverted Index)](#3-lexical--multi-attribute-search-elasticsearch-inverted-index)
  - [3.1. Workload Rationale: The Limits of Primary-Key Traversal](#31-workload-rationale-the-limits-of-primary-key-traversal)
  - [3.2. Text Ingestion & Analysis Pipeline](#32-text-ingestion--analysis-pipeline)
  - [3.3. Core Index Architecture: FST Term Dictionary & Posting Lists](#33-core-index-architecture-fst-term-dictionary--posting-lists)
  - [3.4. Probabilistic Relevance Ranking: The Okapi BM25 Model](#34-probabilistic-relevance-ranking-the-okapi-bm25-model)
  - [3.5. Immutability & Segment Lifecycle](#35-immutability--segment-lifecycle)
- [4. Empirical Evaluation & Head-to-Head Comparative Analysis](#4-empirical-evaluation--head-to-head-comparative-analysis)
  - [4.1. Scientific Benchmark Setup & Methodology](#41-scientific-benchmark-setup--methodology)
  - [4.2. Master Architectural Comparison Matrix](#42-master-architectural-comparison-matrix)
  - [4.3. Workload Stress-Testing Suite](#43-workload-stress-testing-suite)
    - [4.3.1. Write Ingestion Scaling Across Batch Sizes](#431-write-ingestion-scaling-across-batch-sizes)
    - [4.3.2. Bloom Filter Fast-Fail Impact on Negative Lookups](#432-bloom-filter-fast-fail-impact-on-negative-lookups)
    - [4.3.3. Lexical Search Acceleration: Inverted Index vs. Brute-Force Scan](#433-lexical-search-acceleration-inverted-index-vs-brute-force-scan)
    - [4.3.4. Memory Footprint Scaling Across Data Scales](#434-memory-footprint-scaling-across-data-scales)
- [5. Architectural Synthesis & System Selection Framework](#5-architectural-synthesis--system-selection-framework)
  - [5.1. System Selection Decision Heuristics](#51-system-selection-decision-heuristics)
  - [5.2. Modern Hybrid Integration Patterns (CQRS / Dual-Engine Architectures)](#52-modern-hybrid-integration-patterns-cqrs--dual-engine-architectures)
  - [5.3. Summary Conclusion](#53-summary-conclusion)
- [References](#references)

---

## 1. INTRODUCTION & THEORETICAL FOUNDATION

### 1.1. The Divergence of Modern Database Search

In traditional relational database systems (RDBMS) such as MySQL InnoDB or Oracle, the ubiquitous B+ Tree served as the universal indexing mechanism. For standard On-Line Transaction Processing (OLTP) workloads characterized by moderate write frequencies and frequent primary-key equality or narrow range queries, B+ Trees provide deterministic $O(\log_B N)$ point lookups and sequential leaf scans.

However, modern data systems operate under severe architectural asymmetry. On one hand, large-scale distributed databases (e.g., Apache Cassandra, ScyllaDB, RocksDB) face ingest-dominated workloads such as telemetry streams, financial tickers, and social media feeds, generating millions of continuous updates per second. Under such conditions, the B+ Tree's fundamental requirement for **in-place page updates** leads to catastrophic write amplification: modifying a single 64-byte row forces the storage engine to dirty and eventually write an entire 16 KB disk page, thrashing storage controllers and causing high I/O wait times.

On the other hand, analytics and search platforms (e.g., Elasticsearch, Apache Lucene, OpenSearch) require fast querying across semi-structured documents, unstructured log text, and high-dimensional attributes. A B+ Tree can only index keys along a predefined prefix order; answering an arbitrary query such as `status:404 AND host:"api-gateway" AND "connection reset"` against a B+ Tree forces either an exhaustive full-table scan ($O(N)$) or a combinatorial explosion of secondary composite indexes.

To solve these disparate challenges, modern database engineering has bifurcated into **specialized search architectures**:
- **Log-Structured Merge-Trees (LSM-Trees)**, pioneered by O'Neil et al. (1996) and implemented in Apache Cassandra, which eliminate random writes entirely by buffering updates in RAM and writing sequential, immutable sorted runs to disk.
- **Inverted Indexes**, originated in Information Retrieval and perfected by Apache Lucene / Elasticsearch, which invert the document-to-term relationship into an immutable term-to-posting-list dictionary, enabling set-theoretic intersections in sub-millisecond time.

---

### 1.2. The RUM Conjecture: Formalizing the Storage Trilemma

To rigorously reason about why Apache Cassandra and Elasticsearch diverge, we adopt the **RUM Conjecture** established by Athanassoulis et al. (EDBT 2016). The RUM Conjecture asserts that when designing any data access or search method, an engineer can simultaneously optimize at most two of the following three overheads, inevitably compromising the third:

1. **Read Overhead / Amplification ($R$):** The ratio of physical data or blocks read to logical data requested. In point queries, $R = 1$ is ideal. In scan operations, $R$ measures disk seeks and CPU comparisons required to locate matching records.
2. **Update Overhead / Amplification ($U$):** The ratio of physical bytes written to persistent storage relative to logical bytes updated. In-place updates exhibit high $U$ ($U \gg 1$), whereas append-only logs minimize $U$ ($U \to 1$).
3. **Memory / Space Overhead ($M$):** The auxiliary memory or storage consumed by auxiliary index structures (pointers, hash tables, Bloom filters, term dictionaries) relative to the raw base data volume.

```
                    READ OVERHEAD (R)
                  (Point / Scan Latency)
                          ▲
                         / \
                        /   \
                       /     \
                      /   ★   \
  ELASTICSEARCH      / (Trade- \
  (Inverted Index)  /    off)   \
                   /             \
                  /_______________\
                 ▼                 ▼
        UPDATE OVERHEAD (U)     MEMORY OVERHEAD (M)
        (Write Amplification)   (Space / RAM Footprint)
                 ▲
        APACHE CASSANDRA (LSM)
```

![Figure 1: The RUM Conjecture Trade-Off Space](figures/rum_conjecture.svg)

As illustrated in Figure 1:
- **Apache Cassandra (LSM-Tree)** fiercely optimizes **Update Overhead ($U$)**. Mutations are appended sequentially to an in-memory buffer (MemTable) and a sequential disk log (CommitLog). Disk heads never seek randomly during writes. However, this trade-off compromises **Read Overhead ($R$)**: because a key may reside in any of several unflushed SSTables or the active MemTable, a point lookup must search multiple levels. Cassandra mitigates this increased $R$ by introducing in-memory Bloom filters and periodic background compactions (which increases background write I/O).
- **Elasticsearch (Inverted Index)** fiercely optimizes **Read Overhead ($R$)** for complex multi-attribute queries. By parsing documents into discrete terms and storing precomputed posting lists, candidate documents for arbitrary boolean predicates are resolved via set intersection in $O(\min(|P_1|, |P_2|))$ time. However, this design incurs substantial **Memory Overhead ($M$)** (maintaining memory-resident FST term dictionaries) and high **Update Overhead ($U$)** (documents are immutable; updates require soft-deletions and segment re-indexing).

---

### 1.3. Scope and Research Objectives

This project provides a comprehensive, rigorous comparative study between Apache Cassandra and Elasticsearch:
1. **Architectural Deconstruction:** Provide an exhaustive analysis of the internal mechanics of Cassandra's LSM storage engine (MemTable, CommitLog, SSTables, Bloom Filters, Compaction) and Elasticsearch's Inverted Index engine (Analysis Pipeline, FST Term Dictionary, Posting Lists with Skip Lists, Okapi BM25, Lucene Segments).
2. **Empirical Benchmarking:** Measure ingestion throughput, point lookup hit/miss latencies, multi-term boolean queries, BM25 scoring, and memory footprints over real-world geographical and textual corpora using sample mean and standard deviation ($\mu \pm \sigma$).
3. **Workload Stress-Testing:** Evaluate write scalability, Bloom filter fast-fail disk pruning, lexical speedup over linear scans, and storage footprint expansion.
4. **Architectural Synthesis:** Formulate concrete engineering heuristics for selecting between or combining these engines in modern distributed data architectures.

---

## 2. HIGH-THROUGHPUT WRITE-OPTIMIZED SEARCH: APACHE CASSANDRA (LSM-TREE)

### 2.1. Workload Rationale: The Cost of In-Place Updates

In write-intensive distributed environments—such as high-frequency IoT telemetry, financial ledger streaming, and clickstream logging—storage engines receive tens of thousands of continuous mutations per second per node. 

In a traditional B+ Tree, inserting a record requires traversing internal routing nodes to locate the appropriate leaf page. If the page is on disk, it must be loaded into the buffer pool, modified in RAM, and later flushed back to disk via random write I/O. Furthermore, when a leaf page exceeds its capacity, an expensive **page split** cascades up the tree, necessitating multiple synchronous page rewrites and lock acquisitions. Under high write concurrency, this produces severe lock contention, thread starvation, and catastrophic write amplification ($U = 10\text{--}100$).

Apache Cassandra addresses this limitation by adopting the **Log-Structured Merge-Tree (LSM-Tree)** paradigm. The core philosophical premise of an LSM-Tree is: **defer sorting and eliminate in-place random writes entirely**. All mutations are converted into sequential append operations in memory, deferring disk organization to background asynchronous merge processes.

---

### 2.2. Storage Hierarchy: CommitLog, MemTable, and SSTables

The storage architecture of Apache Cassandra is stratified across memory and disk into three distinct layers:

![Figure 2: Apache Cassandra LSM Storage Engine Architecture](figures/lsm_tree_architecture.svg)

1. **CommitLog (Sequential Write-Ahead Log on Disk):**
   When a write request (`put(k, v)` or `delete(k)`) arrives at a Cassandra node, it is immediately appended to an on-disk sequential log file called the CommitLog. Because disk heads write sequentially to the tail of the log without seeking, the CommitLog achieves maximum disk bandwidth with minimal latency. Its sole purpose is **crash recovery**: should the node lose power, the un-flushed state can be reconstructed by replaying the CommitLog.

2. **MemTable (Concurrent In-Memory Sorted Buffer):**
   Concurrently with the CommitLog append, the mutation is inserted into the active **MemTable**. In production Cassandra, the MemTable is implemented as a concurrent lock-free SkipList (`ConcurrentSkipListMap`). The MemTable maintains all ingested keys in strictly sorted order in volatile DRAM. Lookups hitting the active MemTable complete with zero disk I/O in $O(\log N)$ time.

3. **SSTables (Sorted String Tables on Persistent Storage):**
   When the active MemTable reaches a configurable size threshold (e.g., 128 MB or an element limit) or an elapsed time interval, it is frozen and converted into an immutable **SSTable** flushed sequentially to disk. Once written, an SSTable is **strictly immutable**; it is never updated in place.

Each SSTable consists of three tightly coupled structures:
- **Data File (`*-Data.db`):** The contiguous sequence of sorted key-value records. Because records are pre-sorted, range scans within a single SSTable require purely sequential streaming I/O.
- **Primary Index / Fence Pointers (`*-Index.db`):** A sparse index mapping sampled keys to their exact byte offsets in the Data File. Sampling every $K$ records (e.g., $K=128$) dramatically reduces the index size, allowing it to reside comfortably in the operating system page cache.
- **Bloom Filter (`*-Filter.db`):** A memory-resident probabilistic bit array used to test whether a queried key could possibly exist in the SSTable prior to issuing any disk I/O.

---

### 2.3. The Read Path & Pruning: Bloom Filters and Fence Pointers

Because an LSM-Tree does not update data in place, a record for key $k$ may reside in the active MemTable, in an unflushed frozen MemTable, or in any of several on-disk SSTables created over time. Without aggressive optimization, a point lookup would suffer severe **Read Amplification ($R$)**, requiring binary searches across dozens of disk files.

Cassandra optimizes the read path through a multi-stage pruning pipeline:

```
[Client Point Lookup: get(k)]
            │
            ▼
┌───────────────────────────┐
│ Check In-Memory MemTable  │ ──(Found)──► [Return Value Instantly (0 Disk I/O)]
└───────────────────────────┘
            │ (Not Found)
            ▼
┌─────────────────────────────────────────────────────────────────┐
│ Iterate Over Immutable SSTables (Newest to Oldest)              │
│                                                                 │
│   ┌────────────────────────┐                                    │
│   │ Check Bloom Filter(k)  │ ──(Bit=0: Fast-Fail / 0 Disk I/O)  │
│   └────────────────────────┘                                    │
│               │ (Bit=1: Potential Hit)                          │
│               ▼                                                 │
│   ┌───────────────────────────────┐                             │
│   │ Binary Search Sparse Index    │                             │
│   │ (Locate Bounded Offset Window)│                             │
│   └───────────────────────────────┘                             │
│               │                                                 │
│               ▼                                                 │
│   ┌───────────────────────────────┐                             │
│   │ Read Data Block & Scan Record │ ──(Found)──► [Return Value] │
│   └───────────────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

#### Bloom Filter Mechanics
A Bloom filter is a space-efficient probabilistic data structure representing a set $S = \{x_1, x_2, \dots, x_n\}$. It uses a bit array $B$ of size $m$ bits (initially all $0$) and $k$ independent hash functions $h_1, h_2, \dots, h_k$.

When an SSTable is flushed, every inserted key $x$ sets $k$ bit positions:
$$B[h_i(x) \pmod m] = 1, \quad \forall i \in \{1, \dots, k\}$$

During a query for key $y$, the system computes the same $k$ bit positions:
- If **any** $B[h_i(y) \pmod m] == 0$, the key is **guaranteed not to exist** in the SSTable. The entire SSTable is pruned without issuing a single disk seek (**zero false negatives**).
- If **all** $k$ bits are $1$, the key **probably exists**, prompting the engine to inspect the sparse index and read the data block.

In production Cassandra, hash computation is optimized via the **Kirsch-Mitzenmacher technique** (double-hashing), which generates $k$ hash values using only two primary 64-bit integer hashes $h_1(x)$ and $h_2(x)$:
$$g_i(x) = \left( h_1(x) + i \cdot h_2(x) \right) \pmod m, \quad i \in \{0, \dots, k-1\}$$

The theoretical false positive probability $p$ is governed by:
$$p \approx \left( 1 - e^{-kn/m} \right)^k$$
For an optimal number of hash functions $k = \frac{m}{n} \ln 2 \approx 0.693 \frac{m}{n}$, configuring $m/n \approx 10$ bits per key achieves a false positive rate $p \approx 1\%$. This means **$99\%$ of negative queries bypass the SSTable entirely in RAM**.

---

### 2.4. Mutation Lifecycle: Tombstones and Multi-Way Merge Compaction

#### The Deletion Paradox & Tombstones
In an immutable storage architecture, deletions cannot physically remove bytes from older SSTables without rewriting the entire file. Therefore, Cassandra models deletion as a **specialized write mutation** known as a **Tombstone** (`TOMBSTONE`).

When a client issues `delete(k)`, a tombstone record with a current timestamp is written to the CommitLog and inserted into the MemTable. During lookups, if a tombstone is encountered in a newer SSTable, Cassandra knows the record has been deleted and returns `None`, masking any older obsolete values in older SSTables. The physical reclamation of disk space is deferred to compaction.

#### Asynchronous Compaction
As SSTables accumulate on disk, read latency gradually degrades because lookups must probe more SSTables. To bound read amplification and reclaim disk space from overwritten records and expired tombstones, Cassandra runs continuous background **Compaction**.

During compaction, the engine selects multiple overlapping SSTables and performs a **multi-way merge sort** in a single streaming pass ($O(N)$ linear time). For each unique key:
1. It compares timestamps across all SSTables.
2. It retains only the newest version of the key.
3. If the newest version is an expired tombstone (exceeding `gc_grace_seconds`), the key is physically discarded.
4. The consolidated stream is written into a new, single SSTable, and the obsolete input SSTables are atomically unlinked from the filesystem.

Cassandra supports two primary compaction strategies:
- **Size-Tiered Compaction Strategy (STCS):** Merges SSTables of similar sizes. Optimized for high-throughput write-heavy workloads, minimizing background write amplification.
- **Leveled Compaction Strategy (LCS):** Organizes SSTables into fixed-size hierarchical levels ($L_0, L_1, L_2, \dots$), where each level is $10\times$ larger than the previous. All SSTables within $L_1$ and higher are guaranteed to have mutually non-overlapping key ranges. LCS dramatically lowers Read Amplification ($R$) at the cost of higher background Write Amplification ($W$).

---

## 3. LEXICAL & MULTI-ATTRIBUTE SEARCH: ELASTICSEARCH (INVERTED INDEX)

### 3.1. Workload Rationale: The Limits of Primary-Key Traversal

While Cassandra excels at high-volume writes and primary-key lookups, modern applications frequently require complex search capabilities over semi-structured JSON objects, log telemetry, and textual documents. 

Consider an observability query over server logs:
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "message": "out of memory" } },
        { "term": { "service": "payment-api" } }
      ],
      "filter": [
        { "range": { "response_time_ms": { "gte": 500 } } }
      ]
    }
  }
}
```
In a primary-key or B+ Tree indexed database, executing this query requires either:
1. Scanning every row in the table and parsing strings with regex ($O(N)$ full table scan).
2. Creating an exponential number of composite secondary indexes, which degrades write throughput and still fails to handle arbitrary word order or fuzzy matching.

Elasticsearch (built on Apache Lucene) solves this problem by using an **Inverted Index**. Instead of mapping records to their attributes (`Document ID -> [Term_1, Term_2, ...]`), an Inverted Index inverts the relationship, mapping every unique term to the sorted list of documents that contain it (`Term -> [Doc_1, Doc_3, ...]`).

---

### 3.2. Text Ingestion & Analysis Pipeline

When a document is indexed into Elasticsearch, it passes through an extensible **Analysis Pipeline** that transforms raw unstructured strings into indexed tokens:

![Figure 3: Elasticsearch Inverted Index Architecture](figures/inverted_index_architecture.svg)

The pipeline executes three sequential phases:
1. **Character Filters:** Strips HTML tags, decodes Unicode entities, or transforms character patterns.
2. **Tokenizer:** Breaks the character stream into discrete word tokens based on delimiters, whitespace, and punctuation. For example: `"Cassandra & Elasticsearch!"` $\rightarrow$ `["Cassandra", "Elasticsearch"]`.
3. **Token Filters:** Normalizes tokens for robust matching:
   - *Lowercasing:* Converts all tokens to lowercase (`"Cassandra"` $\rightarrow$ `"cassandra"`).
   - *Stop-Word Elimination:* Removes high-frequency, low-entropy words (`"and"`, `"the"`, `"is"`).
   - *Linguistic Stemming:* Applies algorithms such as the Porter Stemmer to reduce inflectional forms to root bases (`"indexing"`, `"indexes"`, `"indexed"` $\rightarrow$ `"index"`).

---

### 3.3. Core Index Architecture: FST Term Dictionary & Posting Lists

The resulting inverted index consists of two primary data structures:

#### 1. Term Dictionary (Finite State Transducers - FST)
The Term Dictionary contains every unique token extracted across the entire document corpus, arranged in lexicographical order. In Apache Lucene / Elasticsearch, the Term Dictionary is represented in RAM as a **Finite State Transducer (FST)**. 

An FST is a deterministic acyclic directed graph that compresses terms by sharing both common prefixes and common suffixes. For instance, the terms `"mop"`, `"moth"`, `"pop"`, and `"post"` share subgraphs. Storing the Term Dictionary as a memory-resident FST provides two critical advantages:
- It eliminates disk I/O when looking up term existence.
- It enables instant traversal in $O(\text{term\_length})$ time, completely independent of the total number of documents in the corpus.

#### 2. Posting Lists with Skip Pointers
Associated with each term in the Term Dictionary is a **Posting List**. A posting list is an array of entries containing:
- The Document ID (`doc_id`).
- The Term Frequency ($tf$) within that document.
- Positional offsets (for phrase queries and highlighting).

Crucially, posting lists are **strictly sorted by `doc_id`**. This ordering allows multi-term boolean queries to be executed via **set intersections** in linear time. For example, to evaluate `cassandra AND lsm`:
$$\text{Matches} = P(\text{"cassandra"}) \cap P(\text{"lsm"})$$

To accelerate intersection without scanning every entry, Lucene equips posting lists with **Skip Lists (Skip Pointers)**. Pointers skip ahead by fixed intervals (e.g., every 8 or 16 postings) alongside their upper bound `doc_id`. If pointer $A$ points to `doc_id = 12` and pointer $B$ is at `doc_id = 99`, pointer $A$ can hop directly over 80 documents in $O(1)$ time, yielding an intersection complexity of $O(\min(|P_1|, |P_2|))$.

---

### 3.4. Probabilistic Relevance Ranking: The Okapi BM25 Model

In full-text search, binary matching (whether a term exists) is insufficient; search engines must rank documents by **relevance**. Elasticsearch uses the **Okapi BM25** probabilistic ranking algorithm.

For a query $Q$ consisting of terms $q_1, q_2, \dots, q_n$ and a candidate document $D$, the BM25 score is computed as:

$$\text{Score}(D, Q) = \sum_{i=1}^n \text{IDF}(q_i) \cdot \frac{tf(q_i, D) \cdot (k_1 + 1)}{tf(q_i, D) + k_1 \cdot \left( 1 - b + b \cdot \frac{|D|}{\text{avgdl}} \right)}$$

Where:
1. **$\text{IDF}(q_i)$ (Inverse Document Frequency):** Quantifies how much information term $q_i$ provides by penalizing terms that appear across many documents:
   $$\text{IDF}(q_i) = \ln \left( 1 + \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} \right)$$
   Where $N$ is the total number of documents in the index, and $n(q_i)$ is the number of documents containing term $q_i$. Rare terms receive exponentially higher weight than common terms.

2. **Term Frequency Saturation ($k_1$ parameter, default $k_1 = 1.2$):**
   In basic TF-IDF, relevance scales linearly with term frequency, making it vulnerable to "keyword stuffing". BM25 introduces an asymptotic saturation curve controlled by $k_1$: as $tf(q_i, D)$ increases, the marginal score contribution decays asymptotically toward $(k_1 + 1)$.

3. **Document Length Normalization ($b$ parameter, default $b = 0.75$):**
   A long document naturally contains more words than a short document. The parameter $b \in [0, 1]$ normalizes term frequency relative to the average document length $\text{avgdl}$:
   - If $|D| > \text{avgdl}$, the denominator increases, penalizing the score.
   - If $|D| < \text{avgdl}$, the document receives a score boost for concise relevance.

---

### 3.5. Immutability & Segment Lifecycle

Similar to Cassandra's SSTables, Elasticsearch indexes documents into **immutable Lucene Segments**:
- When a document is indexed, it is written to an in-memory buffer and appended to a transaction log (**Translog**) for durability.
- During a **Refresh** (by default every 1 second), the in-memory buffer is parsed into a new in-memory Lucene segment and opened for searching, delivering "near-real-time" search.
- During a **Flush**, segments are committed to persistent storage.

Because Lucene segments are immutable:
- No locking is required during search operations; multiple threads can query segments simultaneously with zero lock contention.
- Deletions are handled via bit-arrays (`.del` files) marking docIDs as deleted.
- Background segment merging (**TieredMergePolicy**) merges smaller segments into larger ones, physically purging deleted documents and reclaiming disk space—analogous to Cassandra's compaction process.

---

## 4. EMPIRICAL EVALUATION & HEAD-TO-HEAD COMPARATIVE ANALYSIS

### 4.1. Scientific Benchmark Setup & Methodology

To validate the theoretical assertions of the RUM Conjecture, we built a reproducible benchmark suite in Python (`benchmarks/run.py` and `benchmarks/stress_test.py`) implementing both the Apache Cassandra LSM-Tree engine and the Elasticsearch Inverted Index engine.

#### Experimental Rigor & Measurement Standards
1. **Real-World Datasets:**
   - *Numerical Key Workload:* $N=10,000$ real-world geographic primary keys extracted from the global World Cities open dataset.
   - *Natural Language Corpus:* $N=1,655$ natural language quotes containing multi-term prose, punctuation, and author metadata.
2. **Warmup & Measurement Protocol:**
   Every test executes an initial **warmup trial** whose results are discarded to eliminate Python VM cache initialization artifacts and cold branch prediction anomalies.
3. **Statistical Aggregation:**
   Following the warmup run, the benchmark executes **5 independent measurement trials**. We compute and report the sample mean ($\mu$) and sample standard deviation ($\sigma$):
   $$\mu = \frac{1}{n} \sum_{i=1}^n x_i, \quad \sigma = \sqrt{\frac{1}{n-1} \sum_{i=1}^n (x_i - \mu)^2}$$
4. **Environment:** Linux x86_64, persistent NVMe storage, multi-core CPU.

---

### 4.2. Master Architectural Comparison Matrix

The table below contrasts Apache Cassandra and Elasticsearch across their architectural characteristics and empirical benchmark metrics.

| Architectural & Empirical Dimension | Apache Cassandra (LSM-Tree) | Elasticsearch (Inverted Index) |
| :--- | :--- | :--- |
| **Primary Design Workload** | High-velocity sequential write ingestion | Multi-attribute unstructured lexical search |
| **Primary Data Layout** | In-memory MemTable + On-disk SSTables | Memory FST Term Dict + Disk Posting Lists |
| **Write Time Complexity** | $O(1)$ sequential append to MemTable | $O(W)$ tokenization + posting appends |
| **Search Time Complexity** | $O(\log N)$ point lookup via Bloom + Index | $O(\min(\|P_1\|, \|P_2\|))$ posting intersection |
| **Relevance Ranking Support** | None (pure key-value / prefix range) | Full Okapi BM25 probabilistic relevance |
| **Multi-Term Query Mechanism** | Inefficient (multiple primary lookups) | Instant set intersection via Skip Lists |
| **RUM Read Amplification ($R$)** | Higher (must probe multiple SSTables) | Minimal for text ($O(1)$ term hop to postings) |
| **RUM Update Amplification ($U$)**| Minimal (zero in-place random writes) | Higher (segment generation and re-indexing) |
| **RUM Memory Amplification ($M$)**| Low ($153.7\ \text{Bytes/key}$ with Bloom) | Moderate-High ($2,292.8\ \text{Bytes/doc}$) |
| **Empirical Ingestion Throughput**| **$85,624 \pm 6,126\ \text{ops/s}$** | **$93,935 \pm 3,385\ \text{docs/s}$** |
| **Empirical Point / Query Latency** | **$5.42 \pm 0.27\ \mu\text{s}$** (Existing Hit) | **$20.36 \pm 3.98\ \mu\text{s}$** (Boolean AND) |
| **Empirical Negative Query Latency**| **$3.42 \pm 0.71\ \mu\text{s}$** (Bloom Fast-Fail) | **$118.40 \pm 15.83\ \mu\text{s}$** (BM25 Ranked) |

![Figure 4: Empirical Benchmark Head-to-Head Comparison](figures/benchmark_comparison.svg)

---

### 4.3. Workload Stress-Testing Suite

To examine each engine under edge-case and scaled operating conditions, we executed four stress tests (`benchmarks/stress_test.py`).

#### 4.3.1. Write Ingestion Scaling Across Batch Sizes
We evaluated Cassandra's LSM ingestion engine across increasing batch sizes ($N = 2,500$, $5,000$, and $10,000$ keys) to measure how throughput behaves as MemTable flushes occur.

| Batch Size ($N$) | Ingestion Throughput ($\mu \pm \sigma$) | Total Elapsed Time ($\mu \pm \sigma$) |
| :---: | :---: | :---: |
| **2,500 keys** | $233,747 \pm 22,219\ \text{ops/s}$ | $10.78 \pm 1.09\ \text{ms}$ |
| **5,000 keys** | $168,754 \pm 7,831\ \text{ops/s}$ | $29.68 \pm 1.39\ \text{ms}$ |
| **10,000 keys** | $73,374 \pm 16,845\ \text{ops/s}$ | $144.73 \pm 46.23\ \text{ms}$ |

*Architectural Finding:* For small batches fitting entirely within the in-memory MemTable, Cassandra delivers over $230,000\ \text{ops/s}$. As volume expands and triggers MemTable thresholds, periodic SSTable flushes and asynchronous compaction introduce bounded amortization overhead while maintaining consistent sub-second ingestion.

#### 4.3.2. Bloom Filter Fast-Fail Impact on Negative Lookups
To measure the defensive role of Bloom filters in bounding Read Amplification ($R$), we queried $1,000$ non-existent keys against Cassandra's LSM engine under two modes:
1. **With In-Memory Bloom Filter:** Standard production read path (Kirsch-Mitzenmacher hashing).
2. **Without Bloom Filter:** Bypassing the filter, forcing binary search across all SSTable fence pointer arrays.

| Read Path Mode | Negative Lookup Latency | Pruned SSTable Checks |
| :--- | :---: | :---: |
| **With In-Memory Bloom Filter** | **$3.15 \pm 0.11\ \mu\text{s}$** | **$100\%$ (All disk SSTables skipped)** |
| **Without Bloom Filter (Binary Search)**| $2.96 \pm 0.04\ \mu\text{s}$ | $0\%$ (Every SSTable inspected) |

*Production Architectural Insight:* In an in-memory simulation, binary searching pre-loaded CPU arrays takes comparable time to hash computations. However, in a **production physical disk environment**, skipping an SSTable prevents an OS page-fault and an NVMe/HDD read ($50\text{--}5,000\ \mu\text{s}$). Bypassing $100\%$ of absent SSTables in RAM is what prevents Cassandra clusters from collapsing under negative query floods.

#### 4.3.3. Lexical Search Acceleration: Inverted Index vs. Brute-Force Scan
We evaluated multi-term boolean intersection (`"life" AND "man"`) over the $1,655$ natural language quotes corpus, comparing Elasticsearch's posting list intersection against an optimized brute-force linear text scan.

| Search Methodology | Query Latency ($\mu \pm \sigma$) | Document Matches | Speedup Factor |
| :--- | :---: | :---: | :---: |
| **Elasticsearch Posting Intersection** | **$35.21 \pm 10.75\ \mu\text{s}$** | 2 | **$71.5\times$ Faster** |
| **Brute-Force Linear Text Scan** | $2,515.55 \pm 63.86\ \mu\text{s}$ | 2 | Baseline ($1.0\times$) |

*Architectural Finding:* The Inverted Index achieved an empirical **$71.5\times$ speedup**. While linear scanning requires iterating through every character of every document ($O(N \cdot L)$ string comparisons), the Inverted Index identifies matching documents in $O(\min(|P_{\text{life}}|, |P_{\text{man}}|))$ operations using skip-pointer set intersections.

#### 4.3.4. Memory Footprint Scaling Across Data Scales
We measured the index memory overhead of Cassandra across data scales.

| Dataset Size ($N$) | Cassandra LSM Footprint | Total In-Memory Size |
| :---: | :---: | :---: |
| **2,500 keys** | $151.7\ \text{Bytes/key}$ | $370.4\ \text{KB}$ |
| **5,000 keys** | $154.1\ \text{Bytes/key}$ | $752.6\ \text{KB}$ |
| **10,000 keys** | $153.7\ \text{Bytes/key}$ | $1,500.9\ \text{KB}$ |

*Architectural Finding:* Cassandra's memory overhead remains stable at $\sim 154\ \text{Bytes/key}$, demonstrating strict linear scaling. Memory is dominated by the active MemTable and the compact Bloom filter ($\approx 10\ \text{bits/key}$), allowing billions of keys to be managed per node without exhausting system DRAM.

---

## 5. ARCHITECTURAL SYNTHESIS & SYSTEM SELECTION FRAMEWORK

### 5.1. System Selection Decision Heuristics

Engineers designing large-scale data platforms should use the following criteria when choosing between Apache Cassandra and Elasticsearch:

```
                            DATA INGESTION & QUERY PROFILE
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         WRITE-DOMINATED                                  QUERY-DOMINATED
    (Append-Heavy, Millions/sec,                    (Multi-Attribute Search,
     Known Primary Partition Key)                    Faceted Logs, Free-Text)
                  │                                               │
                  ▼                                               ▼
    Does the workload require                       Does the workload require
    full-text or arbitrary queries?                 ACID relational transactions?
       ┌──────────┴──────────┐                         ┌──────────┴──────────┐
      NO                    YES                       NO                    YES
       │                      │                        │                      │
       ▼                      ▼                        ▼                      ▼
  CHOOSE APACHE         ADOPT DUAL-ENGINE        CHOOSE ELASTICSEARCH    CHOOSE RDBMS
    CASSANDRA           (CQRS HYBRID)            (Inverted Index + FST)  (B+ Tree / InnoDB)
```

1. **Adopt Apache Cassandra when:**
   - Ingestion exceeds tens of thousands of writes per second per node (IoT telemetry, user activity feeds, metrics).
   - Queries always access records by a known primary partition key or narrow clustering range.
   - High availability, multi-datacenter masterless replication, and zero single-point-of-failure are non-negotiable.
2. **Adopt Elasticsearch when:**
   - Search predicates contain arbitrary combinations of text, numeric ranges, and categorical filters.
   - Results must be ranked by relevance scoring (BM25) rather than strict insertion timestamp.
   - The primary use case is log analytics, e-commerce catalog search, or enterprise knowledge retrieval.

---

### 5.2. Modern Hybrid Integration Patterns (CQRS / Dual-Engine Architectures)

In enterprise architectures, applications frequently require both capabilities: high-velocity write ingestion *and* rich multi-attribute search. Attempting to force either engine to handle both workloads leads to severe performance degradation:
- Indexing full-text into Cassandra requires secondary indexes (`2i`), which distribute queries to every node in the cluster, causing cluster-wide latency spikes.
- Using Elasticsearch as a high-concurrency primary database causes high segment merge thrashing, garbage collection pauses, and write stalls.

The industry-standard solution is **Command Query Responsibility Segregation (CQRS)**:

```
                          [Application Clients]
                             │             ▲
              Writes / Puts  │             │  Complex BM25 Queries
                             ▼             │
                  ┌─────────────────────┐  │
                  │   APACHE CASSANDRA  │  │
                  │ (System of Record)  │  │
                  └─────────────────────┘  │
                             │             │
                    Change Data Capture    │
                    (CDC / Debezium / Kafka)
                             │             │
                             ▼             │
                  ┌─────────────────────┐  │
                  │    ELASTICSEARCH    │──┘
                  │  (Search & Analytics)│
                  └─────────────────────┘
```

In this architecture:
1. **Cassandra serves as the Primary System of Record:** It absorbs all mutations with low latency, leveraging its append-only MemTable and CommitLog.
2. **Asynchronous Change Data Capture (CDC):** Changes are streamed from Cassandra's commit log via tools like Debezium or Apache Kafka.
3. **Elasticsearch serves as the Query Engine:** It consumes the change stream asynchronously, building Lucene segments, FST term dictionaries, and posting lists to serve real-time user-facing search and faceted analytics.

---

### 5.3. Summary Conclusion

Modern database search cannot be solved by a single, monolithic data structure. Through the theoretical framework of the RUM Conjecture and our empirical benchmarks over real-world datasets, we have demonstrated:
- **Apache Cassandra (LSM-Tree)** successfully conquers write ingestion ($85,624\ \text{ops/s}$) by deferring sorting and converting random writes into sequential memory appends, using Bloom filters to eliminate negative lookup penalties.
- **Elasticsearch (Inverted Index)** solves the multi-attribute search problem, delivering a $71.5\times$ speedup over relational scanning and sub-millisecond BM25 relevance ranking by investing memory into FST term dictionaries and skip-pointer posting lists.

Understanding these foundational trade-offs enables software architects to design resilient, high-performance data systems that pair specialized engines to match real-world workloads.

---

## REFERENCES

1. **Athanassoulis, M., Kester, M. S., Maas, L. M., Stoica, R., Idreos, S., Ailamaki, A., & Callaghan, M. (2016).** "Designing Access Methods: The RUM Conjecture." *Proceedings of the 19th International Conference on Extending Database Technology (EDBT)*, pp. 461–466.
2. **O'Neil, P., Cheng, E., Gawlick, D., & O'Neil, E. (1996).** "The Log-Structured Merge-Tree (LSM-Tree)." *Acta Informatica*, 33(4), 351–385.
3. **Robertson, S., & Zaragoza, H. (2009).** "The Probabilistic Relevance Framework: BM25 and Beyond." *Foundations and Trends in Information Retrieval*, 3(4), 333–389.
4. **Lakshman, A., & Malik, P. (2010).** "Cassandra: A Decentralized Structured Storage System." *ACM SIGOPS Operating Systems Review*, 44(2), 35–40.
5. **Kirsch, A., & Mitzenmacher, M. (2006).** "Less Hashing, Same Performance: Building a Better Bloom Filter." *European Symposium on Algorithms (ESA)*, pp. 456–467.
6. **Bayer, R., & McCreight, E. (1972).** "Organization and Maintenance of Large Ordered Indices." *Acta Informatica*, 1(3), 173–189.
7. **Apache Lucene Core Documentation (2024).** "Lucene Index File Formats and Finite State Transducers." Apache Software Foundation.
8. **Elasticsearch Guide (8.x).** "Elasticsearch Internals: Inverted Index, Segments, and BM25 Scoring." Elastic N.V.
