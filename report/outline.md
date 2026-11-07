# Course: Data Engineering (CO5173) - HCMUT
## Project Report Outline: Specialized Modern Database Search Engines — Apache Cassandra (LSM) vs. Elasticsearch (Inverted Index)

**Instructor:** Assoc. Prof. Tran Minh Quang  
**Students:**  
- Nguyen Dinh Hoang Son (Student ID: `2670362`)  
- Nguyen Doan Phuc An (Student ID: `2670249`)  
**Location & Date:** Ho Chi Minh City – 2026  
**Repository:** [https://github.com/Pasonnn/co5173-modern-database-search-techniques](https://github.com/Pasonnn/co5173-modern-database-search-techniques)

---

### 1. Introduction & Theoretical Foundation
- **1.1. The Divergence of Modern Database Search:**
  - Why traditional relational indexing (B+ Tree) cannot simultaneously serve high-throughput ingestion and unstructured lexical retrieval.
- **1.2. The RUM Conjecture (Athanassoulis et al., EDBT 2016):**
  - Formalizing the trilemma: Read Amplification ($R$), Update Amplification ($U$), and Memory/Storage Amplification ($M$).
  - Mapping Cassandra (optimizing $U$) vs. Elasticsearch (optimizing $R$ for arbitrary text predicates).
- **1.3. Scope & Objectives:**
  - In-depth architectural deconstruction, mathematical modeling, and empirical benchmarking of Apache Cassandra (LSM-Tree) and Elasticsearch (Inverted Index).

---

### 2. High-Throughput Write-Optimized Search: Apache Cassandra (LSM-Tree)
- **2.1. Workload Target & Architectural Rationale:**
  - Write-intensive ingestion, append-heavy time-series, sensor telemetry, and partitioned key-value lookups.
- **2.2. The Storage Hierarchy:**
  - **CommitLog:** Sequential disk Write-Ahead Logging (WAL) for durability without random I/O.
  - **MemTable:** Concurrent in-memory sorted structure (SkipList) supporting $O(\log N)$ point writes in RAM.
  - **Immutable SSTables (Sorted String Tables):** Flushed immutable runs composed of Data Files, Primary Fence Index, and Summary blocks.
- **2.3. Read Path Mechanics & Pruning:**
  - Hierarchical read path: Active MemTable $\rightarrow$ In-memory Bloom Filter $\rightarrow$ Sparse Fence Pointers $\rightarrow$ Targeted SSTable Data Block.
  - Bloom Filter double-hashing (Kirsch-Mitzenmacher optimization) to eliminate unnecessary disk seeks on absent keys.
- **2.4. Mutation Lifecycle & Compaction:**
  - Deletion mechanics via Tombstones and TTL markers.
  - Asynchronous multi-way merge compaction: Size-Tiered Compaction Strategy (STCS) vs. Leveled Compaction Strategy (LCS).
  - Theoretical bounds on Read Amplification ($R$) vs. Write Amplification ($W$).

---

### 3. Lexical & Multi-Attribute Search: Elasticsearch (Inverted Index & Lucene)
- **3.1. Workload Target & Architectural Rationale:**
  - Unstructured full-text search, multi-term filtering, log analytics, and relevance-scored information retrieval.
- **3.2. Text Ingestion & Analysis Pipeline:**
  - Tokenization, normalization, stop-word elimination, and linguistic stemming (Porter Stemmer).
- **3.3. Core Data Structures:**
  - **Term Dictionary:** Finite State Transducer (FST) compressed in RAM for $O(\text{term\_length})$ dictionary lookups.
  - **Posting Lists:** Ordered document IDs, term frequencies ($tf$), and term positions/offsets.
  - **Skip Lists / Skip Pointers:** Enabling sub-linear $O(\min(|P_1|, |P_2|))$ posting intersections for multi-term Boolean AND queries.
- **3.4. Probabilistic Relevance Ranking (Okapi BM25):**
  - Mathematical formulation of BM25 scoring: Inverse Document Frequency (IDF), term frequency saturation ($k_1 = 1.2$), and document length normalization ($b = 0.75$).
- **3.5. Immutability & Segment Lifecycle:**
  - Lucene segment immutability, in-memory indexing buffer, Translog durability, and background TieredMergePolicy.

---

### 4. Empirical Evaluation & Head-to-Head Comparison
- **4.1. Scientific Benchmark Setup & Methodology:**
  - Real-world datasets: World Cities Geonames ($N=10,000$ numerical primary keys) and Quotes Natural Language Corpus ($N=1,655$ documents).
  - Rigorous scientific measurement: 1 warmup run (discarded) + 5 repeated trials; reporting mean and standard deviation ($\mu \pm \sigma$).
- **4.2. Ingestion Throughput & Query Latency:**
  - Cassandra sequential ingestion vs. Elasticsearch tokenization & posting construction rate.
  - Point lookup hit vs. miss latency (Bloom Filter fast-fail).
  - BM25 ranked scoring vs. Boolean AND/OR posting list intersections.
- **4.3. Workload Stress-Testing Suite:**
  - 4.3.1. Cassandra write ingestion scaling across batch sizes ($N=2,500$ to $10,000$).
  - 4.3.2. Bloom Filter fast-fail impact on absent key lookups (100% disk seek pruning).
  - 4.3.3. Lexical search acceleration: Inverted Index vs. Brute-force linear scan ($71.5\times$ speedup).
  - 4.3.4. Memory footprint scaling across data volume.
- **4.4. Master Architectural Comparison Table:**
  - Comprehensive trade-off matrix across algorithmic complexity, RUM overheads, and empirical numbers.

---

### 5. Architectural Synthesis & System Selection Framework
- **5.1. System Selection Heuristic:**
  - Concrete decision tree for database engineers: when to adopt Cassandra vs. Elasticsearch.
- **5.2. Modern Dual-Engine Integration Patterns:**
  - CQRS (Command Query Responsibility Segregation): Cassandra for high-velocity write ingestion + Change Data Capture (CDC / Debezium) syncing to Elasticsearch for real-time faceted search.
- **5.3. Summary Conclusion:**
  - Synthesis of findings and concluding takeaways.
