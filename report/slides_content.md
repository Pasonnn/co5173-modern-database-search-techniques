# PRESENTATION SLIDES: SEARCH TECHNIQUES IN MODERN DATABASE SYSTEMS
## An Architectural, Theoretical, and Empirical Analysis Across the RUM Trade-Off Space

**Course:** Data Engineering (CO5173) – Ho Chi Minh City University of Technology (HCMUT)  
**Instructor:** Assoc. Prof. Tran Minh Quang  
**Authors:** Nguyen Dinh Hoang Son (ID: `2670362`), Nguyen Doan Phuc An (ID: `2670249`)  
**Duration:** 15 Minutes (15 Slides, ~1 min/slide)  

---

### SLIDE 1: Title & Introduction
- **Time:** [0:00 – 1:00]
- **Slide Header:** Search Techniques in Modern Database Systems: An Empirical Analysis Across the RUM Space
- **Visuals / Layout:**
  - Course: Data Engineering (CO5173), HCMUT
  - Presenters: Nguyen Dinh Hoang Son (`2670362`), Nguyen Doan Phuc An (`2670249`)
  - Subtitle: *Why no single indexing engine fits all workloads, and how modern databases navigate the trade-off space.*
- **Key Points:**
  - The fundamental search problem: locating records without scanning $O(N)$ data.
  - Divergence of modern hardware: Fast NVMe SSDs, multi-core parallelism, massive DRAM.
  - Divergence of workloads: High-frequency IoT writes vs. microsecond OLTP reads vs. full-text search.
- **Speaker Script (60s):**
  > "Good morning, Professor and fellow classmates. Today, we present our research on 'Search Techniques in Modern Database Systems.' For decades, relational databases treated the B+ Tree as the default index for everything. However, in modern computing, data volumes have exploded, hardware has evolved, and workload requirements have radically diverged. Today, no single search technique can satisfy all applications. We analyze five foundational indexing paradigms—B+ Trees, LSM-Trees, Inverted Indexes, Static Learned RMI, and Dynamic Learned ALEX—under the lens of the RUM Conjecture, supported by empirical benchmarks over real-world datasets with rigorous statistical averaging."

---

### SLIDE 2: The Theoretical Foundation: The RUM Conjecture
- **Time:** [1:00 – 2:00]
- **Slide Header:** The Storage Engine Trade-Off Space: The RUM Conjecture
- **Visuals / Layout:**
  - `report/figures/rum_conjecture.svg` (Projected Full Screen)
  - Triangle Diagram:
    - Vertex 1: **Read Amplification ($R$)**
    - Vertex 2: **Update Amplification ($U$)**
    - Vertex 3: **Memory/Space Amplification ($M$)**
- **Key Points:**
  - **Read Amplification ($R$):** Bytes physically read from storage vs. logical payload returned.
  - **Update Amplification ($U$):** Bytes written to durable media vs. logical bytes modified.
  - **Memory Amplification ($M$):** RAM overhead of pointers/metadata over raw data size.
  - **Theorem (Athanassoulis et al., EDBT 2016):** Optimizing any two overheads inevitably degrades the third.
- **Speaker Script (60s):**
  > "To understand why database engines differ, we must understand the RUM Conjecture, formulated by Athanassoulis and colleagues in 2016. Just like the CAP theorem in distributed systems, the RUM Conjecture establishes that you cannot simultaneously minimize Read Amplification, Update Amplification, and Memory Amplification. If you optimize for sub-microsecond reads and sequential range scans like a B+ Tree, your update cost climbs. If you optimize for write absorption like an LSM-Tree, read amplification increases. If you compress memory using learned models, update flexibility drops. Modern search techniques are deliberate compromises on this triangle."

---

### SLIDE 3: Taxonomy of Five Core Search Paradigms
- **Time:** [2:00 – 3:00]
- **Slide Header:** Five Search Paradigms: From Pointers to Models
- **Visuals / Layout:** 2x2 Paradigm Matrix + 1 Text Engine
  - **Comparison Pointers:** B+ Tree (MySQL InnoDB, SQLite)
  - **Log-Structured Multi-Run:** LSM-Tree (RocksDB, Cassandra)
  - **Lexical Postings & BM25:** Inverted Index (Elasticsearch, Lucene)
  - **Static Function Approximation:** Recursive Model Index / RMI (BOURBON, BigQuery)
  - **Dynamic Updatable Machine Learning:** ALEX (Adaptive Learned Index)
- **Key Points:**
  - Structural transition: Hierarchical pointers $\to$ append logs $\to$ inverted lists $\to$ mathematical CDF regression.
  - Unified evaluation harness: Built from scratch and benchmarked on identical hardware.
- **Speaker Script (60s):**
  > "We categorize modern search mechanisms into four distinct paradigms encompassing five core implementations: First, comparison-based pointer hierarchies with the B+ Tree. Second, write-optimized log-structured merge trees. Third, lexical inverted indexes with BM25 ranking. Fourth, static machine-learned CDF regression models with RMI. And fifth, dynamic updatable learned indexes with ALEX. Let us now examine each technique through our structured framework: WHAT, WHO, WHY, HOW, and empirical PERFORMANCE."

---

### SLIDE 4: Technique 1: B+ Tree (MySQL InnoDB / SQLite)
- **Time:** [3:00 – 4:00]
- **Slide Header:** B+ Tree: The Comparison-Based Gold Standard
- **Visuals / Layout:**
  - `report/figures/bplus_tree_reference.png`
  - Slotted page diagram showing internal navigation nodes ($B \approx 100\text{--}1000$) down to bidirectional leaf linked list.
- **Content Framework:**
  - **WHAT:** Invented by Rudolf Bayer & Edward McCreight (1970/1972); refined by Douglas Comer (1979). Self-balancing $B$-way tree; records stored exclusively at leaves.
  - **WHO:** MySQL InnoDB, SQLite, PostgreSQL, Oracle, Microsoft SQL Server.
  - **WHY:** Relational OLTP needs deterministic sub-millisecond point reads and contiguous range scans (`BETWEEN`). Hash tables fail ranges; binary trees cause disk thrashing ($O(\log_2 N)$ vs $O(\log_B N)$).
  - **HOW:** 16KB slotted pages; top-down binary search down $h \approx \log_B N$; leaf pointer chaining; in-place page splits ($B/2$ keys); Write-Ahead Logging (WAL).
  - **PERFORMANCE:** **0.52 ± 0.03 µs** point lookup; **33,871 ± 3,429 ops/s** range throughput. Weakness: High update amplification ($U > 10$) on random writes.
- **Speaker Script (60s):**
  > "The B+ Tree was invented by Bayer and McCreight in 1970. It powers relational database engines like MySQL InnoDB and SQLite. Why? Because transactional business systems require deterministic read latency and fast sequential range scans. In a B+ Tree, wide fanout keeps tree height extremely low—usually 3 to 4 levels for millions of records. Leaves form a contiguous bidirectional linked list. Our benchmarks show B+ Trees excel in read latency at 0.52 microseconds and over 33,000 range operations per second. However, its Achilles' heel is write amplification: modifying a 20-byte row requires writing an entire 16KB dirty page to disk."

---

### SLIDE 5: Technique 2: LSM-Tree (RocksDB / Apache Cassandra)
- **Time:** [4:00 – 5:00]
- **Slide Header:** LSM-Tree: Write-Optimized Log-Structured Merging
- **Visuals / Layout:**
  - `report/figures/lsm_tree_architecture.svg`
  - Write flow diagram: MemTable (RAM) $\to$ Flush $\to L_0$ SSTables $\to$ Background Compaction $\to L_1, L_2$ with Bloom Filters.
- **Content Framework:**
  - **WHAT:** Invented by Patrick O'Neil et al. (1996). Eliminates in-place updates by buffering mutations in memory and flushing immutable sorted runs.
  - **WHO:** Apache Cassandra, RocksDB, Google Bigtable, CockroachDB, TiKV.
  - **WHY:** Write-dominated workloads (IoT telemetry, time-series, log streams) choke B+ Trees with random disk I/O and page splits. LSM converts random writes into sequential appends ($U \approx 1$).
  - **HOW:** In-memory MemTable (SkipList) + sequential WAL; background flush to immutable SSTables; in-memory Bloom filters for $O(1)$ negative lookup pruning; tiered/leveled merge compaction.
  - **PERFORMANCE:** Eliminates disk write stalls. Trade-off: Read latency increases to **13.27 ± 5.49 µs** (checking multiple SSTables) and range throughput is **1,747 ops/s** due to multi-stream merging.
- **Speaker Script (60s):**
  > "When your workload is overwhelmed by incoming writes, such as sensor telemetry in Cassandra or embedded key-value writes in RocksDB, B+ Trees degrade due to random disk I/O. Patrick O'Neil invented the Log-Structured Merge-Tree in 1996 to solve this. Instead of updating pages in-place, writes append sequentially to an in-memory MemTable. When full, it flushes sequentially as an immutable SSTable. In-memory Bloom filters prevent unnecessary disk reads for absent keys. In exchange for massive write endurance and throughput, point lookup latency rises to 13.27 microseconds because a read may need to inspect multiple SSTable levels."

---

### SLIDE 6: Technique 3: Inverted Index & BM25 (Elasticsearch / Lucene)
- **Time:** [5:00 – 6:00]
- **Slide Header:** Lexical Inverted Index: Full-Text Search & BM25
- **Visuals / Layout:**
  - Text pipeline: Raw text $\to$ Tokenizer $\to$ Term Dictionary (FST) $\to$ Posting Lists `[DocID, TF]`.
  - Formula: $\text{BM25 Score}(D, Q) = \sum \text{IDF}(t) \cdot \frac{\text{TF}(k_1+1)}{\text{TF} + k_1(1-b+b\frac{|D|}{\text{avgdl}})}$.
- **Content Framework:**
  - **WHAT:** Inverted files pioneered by Gerard Salton (1968/1971); Okapi BM25 ranking formulated by Stephen Robertson (1994/2009). Maps Terms $\to$ Document IDs.
  - **WHO:** Elasticsearch, Apache Lucene, OpenSearch, Solr, Meilisearch.
  - **WHY:** Unstructured text and multi-field log queries cannot be sorted along a single 1D B+ Tree key. Searching substring tokens in B+ Trees forces an $O(N)$ full table scan.
  - **HOW:** Text normalization/tokenization; Finite State Transducers (FST) for term dictionary; posting list intersection via skip pointers and Roaring Bitmaps; BM25 probabilistic relevance scoring.
  - **PERFORMANCE:** Boolean multi-term intersection executes in **92.99 ± 39.03 µs** on real text, achieving a **41.9$\times$ speedup** over brute-force table scanning (3.9 ms).
- **Speaker Script (60s):**
  > "What if our query is not an integer key, but unstructured words like 'database storage performance'? In a B+ Tree, this requires a catastrophic full relation scan. Gerard Salton pioneered the Inverted Index, and Stephen Robertson developed the Okapi BM25 scoring algorithm. By inverting the mapping from Document-to-Words to Word-to-Document posting lists, Elasticsearch resolves complex multi-term boolean queries in microseconds. On our real text corpus of 1,655 documents, posting list intersection resolved queries in 93 microseconds—nearly 42 times faster than scanning the table directly."

---

### SLIDE 7: Technique 4: Static Learned Index: RMI (BOURBON / BigQuery)
- **Time:** [6:00 – 7:00]
- **Slide Header:** Static Learned Index: Recursive Model Index (RMI)
- **Visuals / Layout:**
  - `report/figures/learned_index_rmi.svg`
  - Diagram: Key $k \to$ Root Model $\to$ Leaf Model $j \to$ Predicted Position $\hat{p} \pm \epsilon \to$ Local Binary Search.
  - Concept: $\text{Position}(k) \approx N \times \text{CDF}(k)$.
- **Content Framework:**
  - **WHAT:** Proposed by Tim Kraska et al. (MIT & Google Brain, SIGMOD 2018); extended to LSM SSTables in BOURBON (OSDI 2020). Models sorted keys as a Cumulative Distribution Function.
  - **WHO:** BOURBON (learned RocksDB/WiscKey), Google BigQuery, columnar Parquet file indexing.
  - **WHY:** Massive cold data warehouses spend 20%–30% of total DRAM storing B+ Tree pointers and fence keys (~90 B/key).
  - **HOW:** Two-stage hierarchy of linear regression models ($y = \alpha x + \beta$); root model routes to leaf partition; leaf model predicts slot with mathematically guaranteed error bound $[\hat{p} - \epsilon, \hat{p} + \epsilon]$; final bounded binary search.
  - **PERFORMANCE:** Memory drops to **1.4 Bytes/key** (**64.3$\times$ smaller than B+ Tree**); point lookup: **1.55 ± 0.18 µs**. Weakness: Static; cannot insert without full retraining.
- **Speaker Script (60s):**
  > "In 2018, Kraska and Google Brain published a radical observation: a sorted database index is simply a Cumulative Distribution Function predicting record positions. Instead of storing megabytes of tree pointers, we can train lightweight linear regression models. This is the Recursive Model Index, or RMI. In read-only analytics and immutable SSTables—such as the BOURBON storage engine—RMI compresses index memory down to an astonishing 1.4 Bytes per key. That is over 64 times smaller than a B+ Tree, while maintaining fast 1.55-microsecond point lookups. Its limitation is that it is immutable; inserting new keys alters the CDF and requires retraining."

---

### SLIDE 8: Technique 5: Dynamic Updatable Learned Index: ALEX
- **Time:** [7:00 – 8:00]
- **Slide Header:** Dynamic Learned Index: ALEX Architecture
- **Visuals / Layout:**
  - Gapped Array layout: `[Key 10] [Key 15] [ GAP ] [Key 25] [ GAP ] [Key 40]`.
  - Tree of linear models routing to dynamic leaf DataNodes.
- **Content Framework:**
  - **WHAT:** Invented by Jialin Ding, Tim Kraska et al. (MIT & Microsoft Research, SIGMOD 2020). Combines learned CDF projection with adaptive gapped arrays to enable dynamic inserts.
  - **WHO:** In-memory HTAP prototypes, high-frequency financial caching layers, modern analytical caches.
  - **WHY:** High-throughput in-memory search needs the CPU cache efficiency of learned models, but cannot tolerate the read-only restriction of static RMI.
  - **HOW:** Internal routing nodes with linear models; leaf DataNodes with gapped arrays (empty slots absorb inserts locally without whole-array shifts); model-driven slot projection + galloping search; node splitting when capacity or error exceeds threshold.
  - **PERFORMANCE:** Ingestion: **78,490 ± 24,253 ops/s**; point lookup: **8.07 ± 2.88 µs**; memory: **104.3 B/key**.
- **Speaker Script (60s):**
  > "To overcome the read-only restriction of RMI, Ding and Kraska introduced ALEX in SIGMOD 2020. ALEX marries machine learning with the gapped array concept. Within each leaf DataNode, empty slots or GAPs are distributed proportionally among keys. When you insert a key, ALEX predicts the slot: if it is a gap, insertion is instantaneous; if occupied, it shifts only local keys to the nearest gap. When a node fills, it splits dynamically just like a B+ Tree. ALEX sustains up to 78,000 dynamic insertions per second while delivering model-based lookups, proving that learned indexes can be dynamic."

---

### SLIDE 9: Scientific Benchmark Setup & Methodology
- **Time:** [8:00 – 9:30]
- **Slide Header:** Empirical Methodology & Real-World Datasets
- **Visuals / Layout:**
  - Two Dataset Badges:
    1. **Real-World Geoname IDs:** 10,000 keys from World Cities dataset (real geographical skew & non-uniform gaps).
    2. **Real Text Corpus:** 1,655 documents from Quotes dataset (natural sentence lengths, real vocabulary).
  - Scientific Rigor Protocol:
    - 1 Discarded Warmup Run (eliminates cold cache / JIT anomalies).
    - 5 Repeated Measurement Trials per metric.
    - Statistical Reporting: Sample Mean $\pm$ Standard Deviation ($\mu \pm \sigma$).
- **Key Points:**
  - All five engines tested on identical Linux hardware with fixed CPU affinity.
  - Evaluated on Ingestion throughput, Point lookup latency, Range query throughput, and Memory bytes per key.
- **Speaker Script (90s):**
  > "To evaluate these five techniques scientifically, we adhered strictly to academic research standards. We avoided synthetic uniform toys and instead used real-world data: 10,000 real Geoname IDs from the global World Cities open dataset, reflecting real geographic clustering, and 1,655 natural language text documents from the Quotes corpus. Furthermore, single-run benchmarks can be deceptive due to CPU branch prediction and memory warming. Therefore, every single test executed an initial warmup run that was discarded, followed by five repeated measurement trials. We report the exact empirical sample mean and sample standard deviation across all operations."

---

### SLIDE 10: Master Comparison Matrix: Empirical Head-to-Head
- **Time:** [9:30 – 11:00]
- **Slide Header:** Master Technology Comparison: Real Dataset (N=10,000, 5 Trials)
- **Visuals / Layout:**
  - `report/figures/benchmark_comparison.svg`
  - Master Benchmark Table:

| Search Architecture | Ingest Throughput (ops/s) | Point Lookup Latency ($\mu$s) | Range Throughput (ops/s) | Memory (Bytes/Key) |
|---|---|---|---|---|
| **B+ Tree (InnoDB)** | **1,666,698 ± 201,877** | **0.52 ± 0.03** | **33,871 ± 3,429** | 90.1 |
| **LSM-Tree (RocksDB)** | 24,210 ± 7,880 | 13.27 ± 5.49 | 1,747 ± 501 | 153.7 |
| **Static RMI (BOURBON)** | 1,065,747 ± 18,054 | 1.55 ± 0.18 | 18,537 ± 521 | **1.4** |
| **Dynamic ALEX** | 78,490 ± 24,253 | 8.07 ± 2.88 | 661 ± 280 | 104.3 |
| **Inverted Index (Lucene)**| 42,370 docs/sec | 92.99 ± 39.03 (AND) | N/A (BKD Tree) | Variable |

- **Speaker Script (90s):**
  > "Here is our master comparison matrix. Notice how clearly the RUM trade-offs emerge from the data: B+ Tree leads in point lookup latency at 0.52 microseconds and delivers the highest range throughput at over 33,000 ops per second. However, look at Static RMI: its memory footprint is an astonishing 1.4 Bytes per key—nearly two orders of magnitude smaller than B+ Tree (90.1 Bytes) and LSM-Tree (153.7 Bytes)—while maintaining a very competitive 1.55-microsecond read latency. LSM-Tree trades point read latency (13.27 microseconds) and range throughput for sequential write absorption and SSD endurance. Each engine dominates in its intended domain."

---

### SLIDE 11: Workload Stress-Test: Point Reads & Write Ingestion
- **Time:** [11:00 – 12:00]
- **Slide Header:** Stress-Tests: Read Locality & Write Scalability
- **Visuals / Layout:** Two-panel comparison:
  - **Panel A (Read Skew):** Uniform (2.32 µs B+ Tree vs 6.74 µs ALEX) vs Zipfian $\alpha=1.3$ (1.63 µs B+ Tree vs 8.19 µs ALEX).
  - **Panel B (Write Scalability):** Batch scaling from 2,500 to 10,000 keys.
- **Key Insights:**
  - Zipfian access (80/20 rule) accelerates B+ Tree by **29.7%** because upper routing pages remain resident in CPU L1/L2 caches.
  - In physical storage, B+ Trees suffer severe write amplification ($U > 10$) under random writes; LSM-Trees sustain steady streaming by writing to sequential logs.
- **Speaker Script (60s):**
  > "Let us look at two stress-tests: In Panel A, we tested query skew. Under a Zipfian distribution where 80% of queries target 20% of hot keys, B+ Tree latency drops from 2.32 microseconds to 1.63 microseconds—a 30% performance boost because upper tree nodes remain warm in CPU cache. In Panel B, we examine write ingestion across growing batches. In RAM, both absorb writes well, but on physical SSDs, B+ Trees experience severe write amplification because every split flushes 16KB dirty pages, whereas LSM-Trees write sequentially to disk."

---

### SLIDE 12: Workload Stress-Test: Lexical Search & Memory Compression
- **Time:** [12:00 – 13:00]
- **Slide Header:** Stress-Tests: Multi-Attribute Pruning & Memory Scaling
- **Visuals / Layout:** Two-panel comparison:
  - **Panel A (Lexical Search):** Inverted Index (92.99 µs) vs Full Scan (3,899.73 µs) $\to$ **41.9$\times$ Speedup**.
  - **Panel B (Memory Scaling):** Memory/key as $N$ grows from 2,000 to 10,000:
    - B+ Tree: Flat at ~90.1 Bytes/key.
    - Static RMI: Drops from 3.6 $\to$ 1.5 $\to$ **0.7 Bytes/key** (>120$\times$ compression).
- **Key Insights:**
  - Inverted indexes prune 99.8% of documents without touching raw document payloads.
  - Linear model parameters amortize as $N$ grows, breaking the linear pointer storage barrier.
- **Speaker Script (60s):**
  > "In our third stress-test, we evaluated multi-term text search on 1,655 real documents. Full-table relational scanning required nearly 3.9 milliseconds. The inverted index resolved the boolean intersection in 93 microseconds—a 42-fold speedup—because posting lists skip non-matching documents entirely. In our fourth stress-test, we evaluated memory footprint as data scales to 10,000 keys. B+ Trees maintain a flat 90 Bytes per key due to explicit node pointers. Static RMI, however, amortizes its linear regression parameters, dropping down to just 0.7 Bytes per key—over 120 times more compact than a B+ Tree!"

---

### SLIDE 13: System Selection Framework: The RUM Decision Tree
- **Time:** [13:00 – 14:00]
- **Slide Header:** Architecture Decision Framework: Choosing the Right Engine
- **Visuals / Layout:**
  - Flowchart:
    1. Unstructured text or multi-field attributes? $\to$ **Inverted Index + BM25** (Elasticsearch).
    2. Write-dominated time-series / logs? $\to$ **LSM-Tree** (Cassandra / RocksDB).
    3. General OLTP with ACID and low read latency? $\to$ **B+ Tree** (MySQL InnoDB).
    4. Immutable analytical warehouse with RAM limits? $\to$ **Static Learned RMI** (BOURBON).
    5. In-memory updatable analytical cache? $\to$ **Dynamic ALEX**.
- **Speaker Script (60s):**
  > "Based on our findings, we formulate a practical decision framework for database architects: First, if your queries involve full-text search, token matching, or multi-attribute filtering, deploy an Inverted Index with BM25. Second, if your workload is write-dominated—such as logging or IoT telemetry—choose an LSM-Tree. Third, for standard transactional OLTP requiring predictable sub-millisecond reads and ACID transactions, the B+ Tree remains unmatched. Fourth, for immutable analytical partitions and SSTables where DRAM is expensive, use Static RMI to cut memory by 90%. And fifth, for in-memory updatable analytics, deploy dynamic learned structures like ALEX."

---

### SLIDE 14: Emerging Hybrid Architectures & Future Horizons
- **Time:** [14:00 – 14:30]
- **Slide Header:** Emerging Frontiers: Hybrid & Hardware-Accelerated Search
- **Visuals / Layout:** Three architectural frontiers:
  - **1. Learned LSM-Trees (BOURBON / RocksDB-RMI):** Replaces binary search index blocks with learned linear models in SSTables, saving 80% RAM.
  - **2. Hardware-Accelerated Bitsets:** SIMD AVX-512 and GPU kernels for ultra-fast Roaring Bitmap posting list intersections.
  - **3. Autonomous Self-Tuning Storage:** Dynamic tiering that transforms cold B+ Tree pages into learned models and hot partitions into gapped arrays.
- **Speaker Script (30s):**
  > "The future of database search lies in hybrid architectures: Systems like BOURBON embed learned RMI models directly inside LSM SSTables, cutting memory by 80%. Meanwhile, modern search engines utilize SIMD AVX-512 vector instructions and GPUs to accelerate posting list bitset intersections at terabit memory bandwidths."

---

### SLIDE 15: Conclusion & Academic References
- **Time:** [14:30 – 15:00]
- **Slide Header:** Conclusion & Foundational References
- **Visuals / Layout:**
  - Summary takeaway: *No universal index exists. Workload profiling and the RUM conjecture dictate the optimal search architecture.*
  - Key Citations:
    - Bayer & McCreight (1970/1972) – B-Trees (*Acta Informatica*)
    - O'Neil et al. (1996) – LSM-Tree (*Acta Informatica*)
    - Robertson & Zaragoza (2009) – BM25 (*FnT in Information Retrieval*)
    - Kraska et al. (2018) – Learned Indexes (*ACM SIGMOD*)
    - Ding et al. (2020) – ALEX (*ACM SIGMOD*)
    - Dai et al. (2020) – BOURBON (*USENIX OSDI*)
    - Athanassoulis et al. (2016) – RUM Conjecture (*EDBT*)
- **Speaker Script (30s):**
  > "In conclusion, our research demonstrates that modern database search is defined by workload-driven trade-offs. By understanding the RUM space and the algorithmic mechanics of each paradigm, engineers can select and design optimal data systems. Thank you for your attention. We are now open for questions."
