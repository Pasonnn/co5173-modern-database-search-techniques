# Course: Data Engineering (CO5173) - HCMUT
## Project Report Outline: Search Techniques in Modern Database Systems

**Instructor:** Assoc. Prof. Tran Minh Quang  
**Students:**  
- Nguyen Dinh Hoang Son (Student ID: 2670362)  
- Nguyen Doan Phuc An (Student ID: 2670249)  
**Location & Date:** Ho Chi Minh City – 2026  

---

### 1. Introduction to Database Indexing & Search Mechanics
- **1.1. The Fundamental Search Problem:**
  - Point lookups, range scans, and full-text retrieval ($O(N)$ scans vs. $O(\log N)$ tree traversals vs. $O(1)$ function mappings).
- **1.2. The Storage Engine Trade-off Space:**
  - The RUM Conjecture (Read, Update, and Memory/Space Amplification) across relational, distributed, and analytical databases.
- **1.3. Taxonomy of Modern Index Architectures:**
  - Comparison-based trees, log-structured engines, lexical inverted indexes, and learned function approximations.

---

### 2. Architectural Paradigms: Why Systems Diverge
- **2.1. The Workload-Driven Design Philosophy:**
  - Why a one-size-fits-all index does not exist in production database design.
- **2.2. Workload Alignment Across Production Engines:**
  - **2.2.1.** High-concurrency sequential ingestion (Apache Cassandra / RocksDB).
  - **2.2.2.** High-dimensional unstructured text & log search (Elasticsearch / Lucene).
  - **2.2.3.** ACID point-and-range transactional workloads (MySQL InnoDB).
  - **2.2.4.** In-memory cache-conscious analytical acceleration (Learned Models).

---

### 3. Core Search Techniques & Production Case Studies
- **3.1. Comparison-Based Pointers: B+ Tree Architecture**
  - Case Study: MySQL InnoDB Storage Engine.
  - Storage Layout: Branching factor (fanout), page boundaries (16KB), key-pointer serialization.
  - Search & Range Mechanics: Hierarchical pointer traversal down height $h$, sibling leaf chaining, CPU cache misses.
  - Write Path: In-place page updates, page splits/merges, Write-Ahead Logging (WAL).
  - Trade-off Profile: Predictable $O(\log N)$ latency vs. high write amplification and pointer memory overhead.
- **3.2. Write-Optimized Log-Structured Search: LSM-Tree Architecture**
  - Case Study: Apache Cassandra & RocksDB.
  - Storage Hierarchy: MemTable (SkipList), sequential CommitLog, immutable SSTables.
  - Read & Search Mechanics: Bloom Filter fast-fail ($O(1)$), SSTable sparse index & block traversal.
  - Write & Maintenance: Sequential appends, background multi-way merging (Size-Tiered vs. Leveled), tombstone lifecycle.
  - Trade-off Profile: High ingestion throughput vs. read amplification and compaction I/O spikes.
- **3.3. Lexical & Multi-Attribute Search: Inverted Index & BKD Trees**
  - Case Study: Elasticsearch & Apache Lucene.
  - Text Analysis & Layout: Tokenization, Term Dictionary (FSTs), ordered Posting Lists.
  - Search Execution: Boolean operations (AND/OR), BM25 relevance scoring.
  - Multidimensional Search: Block $k$-d trees (BKD Trees) for numeric/timestamp filtering.
  - Trade-off Profile: Sub-second unstructured queries vs. memory-intensive term dictionaries and high indexing compute.
- **3.4. Static Function Approximation: Static Learned Indexes (RMI)**
  - System Integration: Immutable SSTable Fence Pointers (e.g., BOURBON Engine in LSMs).
  - Core Concept: Cumulative Distribution Function (CDF) approximation: $\text{pos} \approx \text{CDF}(\text{key}) \times N$.
  - Recursive Model Index (RMI): Multi-stage hierarchical regression with bounded error $[\text{pos}-\epsilon, \text{pos}+\epsilon]$.
  - Industrial Fit: Immutable LSM SSTables (permanent order, zero in-place updates).
  - The Static Bottleneck: $O(N)$ copy overhead and complete retraining on dynamic writes.
- **3.5. Dynamic Updatable Learned Indexing: The ALEX Architecture**
  - Storage Layout: Two-tier hierarchy (Internal routing models vs. Leaf Data Nodes).
  - Gapped-Array Mechanism: Calculated gaps to absorb writes locally without full array shifts.
  - Search Mechanics: Model-predicted slot targeting with Exponential (Galloping) Search.
  - Trade-off Profile: Near-$O(1)$ lookup latency and low memory footprint vs. node expansion/retraining spikes.

---

### 4. Empirical Evaluation & Comparative Analysis
- **4.1. Master Search Technology Comparison Matrix:**
  - Side-by-side evaluation across: B+ Tree, LSM-Tree, Inverted Index, Static RMI, Dynamic ALEX.
  - Metrics: Point Lookup Latency, Sequential Ingestion, Random Insert Cost, Memory Footprint (Bytes/Key), Range Query Capability, Primary Workload Target.
- **4.2. Workload Stress-Testing Insights:**
  - 4.2.1. Point read-heavy workloads (ALEX vs. B+ Tree cache efficiency).
  - 4.2.2. High-throughput write ingestion (Cassandra LSM vs. tree-based structures).
  - 4.2.3. Complex filtering and token matching (Elasticsearch vs. primary-key indexes).
  - 4.2.4. Storage and index size compression (Learned models vs. pointer graphs).

---

### 5. Architectural Synthesis & Future Horizons
- **5.1. System Selection Framework:**
  - Decision heuristics for database engine architects based on RUM priorities.
- **5.2. Emerging Hybrid Designs:**
  - Integrating learned models into distributed LSM SSTables (Learned-Cassandra) and analytical columnar data stores.
