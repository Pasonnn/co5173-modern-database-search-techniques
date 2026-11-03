# PRESENTATION SLIDES: SEARCH TECHNIQUES IN MODERN DATABASE SYSTEMS
## An Architectural, Theoretical, and Empirical Analysis Across the RUM Trade-Off Space

**Course:** Data Engineering (CO5173) – Ho Chi Minh City University of Technology (HCMUT)  
**Instructor:** Assoc. Prof. Tran Minh Quang  
**Authors:** Nguyen Dinh Hoang Son (ID: `2670362`), Nguyen Doan Phuc An (ID: `2670249`)  
**Format:** 24 Focused, Bite-Sized Slides (with Relatable Analogies & Exact Speaker Scripts)  
**Target Duration:** 15–20 Minutes  

---

### SLIDE 1: Title & Presentation Overview
- **Visuals:** Title banner, University logo, Author credentials.
- **Header:** Search Techniques in Modern Database Systems
- **Subtitle:** An Architectural, Theoretical, and Empirical Analysis Across the RUM Trade-Off Space
- **Presenters:** Nguyen Dinh Hoang Son (`2670362`) & Nguyen Doan Phuc An (`2670249`)
- **Key Takeaway:** No single database index fits all workloads. Today, systems diverge based on fundamental trade-offs.
- **Speaker Script (45s):**
  > "Good morning, Professor and fellow classmates. Today we are presenting our research on 'Search Techniques in Modern Database Systems.' For over four decades, relational databases treated the B+ Tree as the default answer to every indexing problem. But in modern data engineering, workloads have radically fragmented. A bank verifying transactions has completely different retrieval needs than a distributed cluster ingesting millions of sensor logs, or an e-commerce catalog searching product titles. Today, we break down five core indexing architectures, explain why systems diverge, and ground our analysis in rigorous empirical benchmarks."

---

### SLIDE 2: The Core Problem: Beyond Brute-Force Scanning
- **Visuals:** Contrast graphic: Full Table Scan ($O(N)$ sequential disk reads) vs Index Access ($O(\log N)$ or $O(1)$ direct hops).
- **Core Dilemma:** 
  - Without an index, finding one record in 100 million rows requires reading gigabytes of data.
  - Every index trades auxiliary storage space and update work to create a fast shortcut.
- **Analogy:** Searching for a specific topic in an encyclopaedia by reading every single page from cover to cover versus checking an organized reference table.
- **Speaker Script (45s):**
  > "At the physical storage layer, retrieval reduces to a basic question: how do we find a record without reading the entire disk? A brute-force scan costs order N operations. On modern 100-million-row tables, that is catastrophic. An index is simply an auxiliary data structure that trades storage space and write maintenance to provide a shortcut. But what kind of shortcut should you build? That depends entirely on the physics of your storage media and your query patterns."

---

### SLIDE 3: The Governing Law: The RUM Conjecture
- **Visuals:** `report/figures/rum_conjecture.svg` (Displaying the RUM triangle).
- **Key Concepts:**
  - Formulated by Manos Athanassoulis et al. (EDBT 2016).
  - You cannot simultaneously minimize all three overheads:
    1. **Read Amplification ($R$):** Physical bytes read / Logical bytes returned.
    2. **Update Amplification ($U$):** Physical bytes written / Logical bytes modified.
    3. **Memory Amplification ($M$):** Index memory overhead / Raw data size.
- **Speaker Script (50s):**
  > "Just as the CAP theorem governs distributed data systems, the design of database storage engines is governed by the RUM Conjecture, formulated by Athanassoulis and colleagues in 2016. The theorem proves that you cannot simultaneously optimize Read Amplification, Update Amplification, and Memory Amplification. If you optimize for instant reads, updates suffer. If you optimize to absorb massive writes, reads degrade. If you compress index memory, you sacrifice update flexibility. Every search technique we study today is a deliberate choice on this triangle."

---

### SLIDE 4: Taxonomy: Four Paradigms, Five Engines
- **Visuals:** 4-quadrant architectural map:
  - **1. Pointer Hierarchies:** B+ Tree (MySQL InnoDB / SQLite)
  - **2. Log-Structured Merging:** LSM-Tree (RocksDB / Apache Cassandra)
  - **3. Lexical Inversion:** Inverted Index + BM25 (Elasticsearch / Lucene)
  - **4. Function Approximations:** Static RMI (BOURBON) & Dynamic ALEX
- **Key Message:** The database world has transitioned from fixed pointer graphs to sequential logs, token inverted lists, and mathematical CDF models.
- **Speaker Script (45s):**
  > "We categorize modern search mechanisms into four distinct paradigms encompassing five core implementations: First, pointer-based balanced trees with the B+ Tree. Second, write-optimized sequential engines with the LSM-Tree. Third, lexical token inversion with BM25 ranking. And fourth, machine-learned Cumulative Distribution Function approximations, both static with RMI and dynamic with ALEX. Let us examine each one."

---

### SLIDE 5: B+ Tree: The Intuition & Analogy
- **Visuals:** Diagram comparing a structured library card catalog / filing cabinet to a multi-level B+ Tree.
- **The Analogy:**
  - *The Organized Filing Cabinet / Phonebook:*
    - Drawer labels tell you which drawer to open ('A–D', 'E–H').
    - Inside the drawer, folder tabs narrow you down to a section.
    - At the bottom, physical papers are sorted alphabetically and taped together in a continuous chain.
- **Core Concept:** Separate the routing directions (internal nodes) from the actual physical data (leaf nodes).
- **Speaker Script (45s):**
  > "To understand the B+ Tree, think of a massive office filing cabinet or a classic phonebook. The labels on the outside of the drawers don't contain your documents—they just tell you which drawer to open. Inside, folder tabs guide you to the right section. Only at the very bottom, in the leaf folders, do you find the actual papers. In a B+ Tree, internal nodes store only routing keys, while the leaf pages hold the actual data, chained together so you can flip through consecutive pages without ever going back to the drawer label."

---

### SLIDE 6: B+ Tree: Mechanics & MySQL InnoDB
- **Visuals:** `report/figures/bplus_tree_reference.png` (Slotted page layout down to linked leaves).
- **Inventors & Year:** Rudolf Bayer & Edward McCreight (1970/1972); Douglas Comer (1979).
- **Production Systems:** MySQL InnoDB (clustered primary index), SQLite, PostgreSQL, Oracle.
- **Storage Layout:** Fixed 16KB slotted pages. Fanout $B \in [100, 1000]$. Tree height $h \le 3\text{--}4$ for millions of rows.
- **Execution Paths:**
  - *Read:* Binary search within page down height $h$. Contiguous range scan across leaf sibling pointers.
  - *Write:* In-place page insert. If full, page splits into two half-filled pages ($B/2$ keys each), promoting the median key upward.
- **Speaker Script (50s):**
  > "Invented by Bayer and McCreight in the early 1970s, the B+ Tree is the default engine for relational OLTP databases like MySQL InnoDB and SQLite. InnoDB uses fixed 16KB pages. Because each internal page can hold hundreds of child pointers, the tree has a massive fanout. A 3-level tree can index over 100 million rows. Finding any row requires at most 3 to 4 page hops, and the top levels remain permanently pinned in memory. Furthermore, range queries simply follow leaf sibling pointers sequentially without re-traversing the root."

---

### SLIDE 7: B+ Tree: Performance & The Write Amplification Flaw
- **Visuals:** Bar metric callout: 0.77 µs Point Lookup vs Write Amplification diagram (20-byte change $\to$ 16KB disk write).
- **Benchmark Findings (Our Testbed):**
  - Point Lookup: **0.77 ± 0.07 µs** (fastest deterministic read of all engines; 0.65 µs under cache-pinned Zipfian access).
  - Range Query: **25,754 ± 2,932 ops/s** (smooth leaf streaming).
- **The Critical Flaw (The RUM Bottleneck):**
  - **High Write Amplification ($U > 10\times\text{--}30\times$):** Updating a single 20-byte customer balance requires writing a full 16KB dirty page to disk.
  - On SSDs, random page writes trigger flash memory wear and heavy garbage collection.
- **Speaker Script (50s):**
  > "Our empirical benchmarks show that B+ Trees are kings of read predictability: point lookups take under 0.8 microseconds (0.77 µs), and range scans exceed 25,000 queries per second. But its fatal flaw is write amplification. Because B+ Trees update fixed-size pages in-place, changing a single 20-byte column forces the database to write an entire 16-kilobyte dirty page to disk. In write-heavy environments, this causes massive write amplification, wearing out SSDs and bottlenecking throughput."

---

### SLIDE 8: LSM-Tree: The Intuition & Analogy
- **Visuals:** Diagram: A journalist scribbling rapidly into a pocket notepad vs. filing books into an archival shelf.
- **The Analogy:**
  - *The Journalist's Pocket Notebook:*
    - When events happen fast, you don't run across town to file each paper into the library. You jot it down quickly in an append-only notepad.
    - Only when your notepad fills up do you sit down, sort the notes alphabetically, and file them into the archive in batches.
- **Core Concept:** Convert chaotic, random disk writes into sequential in-memory appends; defer sorting to background batch processing.
- **Speaker Script (45s):**
  > "Imagine you are a reporter taking notes at a live event. You don't run to the central library to file every single sentence into its proper alphabetical shelf—you would miss everything. Instead, you scribble notes rapidly into an append-only pocket notepad. Only when the notepad is full do you sit down, sort the notes, and file them into your archive in batches. This is the exact philosophy of the Log-Structured Merge-Tree: never perform random disk writes in real time. Batch everything in memory, and sort later in the background."

---

### SLIDE 9: LSM-Tree: Architecture & Mechanics
- **Visuals:** `report/figures/lsm_tree_architecture.svg` (MemTable, sequential WAL, SSTables, Bloom filters, Compaction).
- **Inventors & Year:** Patrick O'Neil et al. (1996).
- **Production Systems:** Apache Cassandra, RocksDB (Meta), Google Bigtable, CockroachDB (Pebble).
- **Storage Hierarchy:**
  - *MemTable (RAM SkipList):* Absorbs concurrent writes instantly.
  - *CommitLog (WAL):* Sequential append-only disk log for durability.
  - *SSTables (Disk):* Immutable sorted files arranged in hierarchical levels ($L_0, L_1, L_2$).
  - *Bloom Filters:* In-memory bit arrays providing $O(1)$ fast-fail checks for absent keys.
  - *Compaction:* Multi-way merge-sorting in the background to purge overwritten keys and tombstones.
- **Speaker Script (55s):**
  > "Patrick O'Neil introduced the LSM-Tree in 1996, and it powers modern write-heavy systems like Cassandra and RocksDB. When a write arrives, it is appended to a sequential disk log and inserted into an in-memory SkipList called the MemTable. No random disk I/O occurs. When the MemTable fills, it flushes to disk as an immutable Sorted String Table, or SSTable. Because data is spread across multiple SSTables, each file has an in-memory Bloom filter that checks in O(1) CPU time whether a key exists, avoiding disk reads for 99% of negative queries. In the background, compaction threads merge overlapping SSTables together."

---

### SLIDE 10: LSM-Tree: Performance & The Read Trade-Off
- **Visuals:** Trade-off comparison card: Ingest Throughput vs Read Latency (16.03 µs) vs Range (1,599 ops/s).
- **Benchmark Findings (Our Testbed):**
  - **Ingest Throughput:** Sustains steady streaming across massive batch sizes where B+ Trees degrade from dirty page flushing.
  - **Point Lookup Latency:** **16.03 ± 8.83 µs** (substantially slower than B+ Tree's 0.77 µs).
  - **Range Query Throughput:** **1,599 ± 448 ops/s** (16$\times$ slower than B+ Tree).
- **The Trade-off:** Sacrificing read amplification ($R$) and range query speed to minimize update amplification ($U \approx 1$).
- **Speaker Script (45s):**
  > "The LSM-Tree perfectly illustrates the RUM trade-off. By transforming random writes into sequential appends, it maximizes write throughput and protects SSD endurance. But reads pay the price: our benchmarks show point lookup latency rises to 16 microseconds because a query may need to check the MemTable and multiple SSTable levels. Range queries drop to 1,600 ops per second because the database must merge-sort streams from multiple files simultaneously. You buy write throughput by sacrificing read amplification."

---

### SLIDE 11: Inverted Index: The Intuition & Analogy
- **Visuals:** Diagram of a textbook: Content pages vs The Back-of-the-Book Index.
- **The Analogy:**
  - *The Back-of-the-Book Subject Index:*
    - If you want to find where a textbook mentions 'concurrency' and 'deadlock', you don't read Chapter 1 through 10.
    - You flip to the back of the book, look up 'concurrency', see pages [45, 112, 230], look up 'deadlock', see pages [112, 115], and intersect them: **Page 112!**
- **Core Concept:** Invert the traditional data mapping: instead of Document $\to$ Words, map Word $\to$ Documents.
- **Speaker Script (45s):**
  > "Consider how you search for a concept in a physical textbook. You don't scan all 500 pages from front to back. You flip straight to the index at the back of the book. Under the word 'concurrency', you find page numbers 45, 112, and 230. Under 'deadlock', you find 112 and 115. To find where both topics appear together, you simply take the intersection of those two lists: page 112. This is the Inverted Index: instead of storing which words are in a document, it stores which documents contain each word."

---

### SLIDE 12: Inverted Index: Mechanics & Okapi BM25
- **Visuals:** Pipeline diagram: Raw text $\to$ Tokenization $\to$ Term Dict (FST) $\to$ Posting Lists $\to$ BM25 Formula.
- **Inventors & Year:** Gerard Salton (1968/1971); Stephen E. Robertson & Karen Spärck Jones (Okapi BM25, 1994/2009).
- **Production Systems:** Elasticsearch, Apache Lucene, OpenSearch, Apache Solr.
- **Internal Mechanics:**
  - *Analysis Pipeline:* Tokenization, lowercasing, stop-words, and morphological stemming ("searching" $\to$ "search").
  - *Term Dictionary:* In-memory Finite State Transducer (FST) pointing to compressed on-disk posting lists.
  - *Okapi BM25 Relevance Scoring:*
    $$\text{Score}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t, D)(k_1 + 1)}{f(t, D) + k_1(1 - b + b \cdot \frac{|D|}{\text{avgdl}})}$$
- **Speaker Script (55s):**
  > "Pioneered by Gerard Salton and refined by Stephen Robertson with the Okapi BM25 formula, the inverted index powers systems like Elasticsearch and Apache Lucene. Text is processed through a pipeline: broken into tokens, lowercased, and stemmed to root words. Unique words are stored in an in-memory dictionary called a Finite State Transducer, pointing to sorted posting lists of document IDs. When you query for multiple terms, the engine intersects the posting lists using skip pointers or bitwise SIMD instructions, scoring matches using BM25, which accounts for document length and term saturation."

---

### SLIDE 13: Inverted Index: Empirical Speedup vs Relational Scans
- **Visuals:** Speedup callout graphic: 233.59 µs (Inverted Index) vs 10,122.97 µs (Relational Scan) $\to$ **43.3$\times$ Faster!**
- **Benchmark Findings (Our Testbed - 1,655 Real Quotes):**
  - Multi-term Boolean Query (`life AND man`):
    - *Brute-Force Scan:* **10,122.97 ± 2,735.03 µs** (scans every word in all 1,655 documents).
    - *Inverted Index Intersection:* **233.59 ± 116.72 µs** (inspects only matching posting lists).
    - **Empirical Acceleration:** **43.3$\times$ speedup!**
  - BM25 Top-5 Relevance Ranking: **266.50 ± 105.36 µs**.
- **Speaker Script (45s):**
  > "Why can't we just use a B+ Tree for full-text search? Because B+ Trees can only index sorted prefixes. If you search for words appearing anywhere in a sentence, the relational database is forced into a brute-force scan. In our benchmark over 1,655 real documents, scanning the raw text took over 10 milliseconds. The inverted index resolved the exact same query in 233 microseconds—over 43 times faster—because it bypassed 99.8% of the text corpus without reading a single non-matching document."

---

### SLIDE 14: Static Learned Index (RMI): The Intuition & Analogy
- **Visuals:** Diagram: Estimating the thickness of a thick book to guess a page number vs flipping page by page.
- **The Analogy:**
  - *Estimating Page Position by Book Thickness:*
    - If you are handed an 800-page dictionary and asked to find page 400, you don't flip through pages 1, 2, 3...
    - You pinch the book exactly in the middle. Your fingers land around page 395. Then you flip just 2 or 3 pages to reach 400.
- **Core Insight:** In a sorted array, Key $\to$ Position is a mathematical function: the **Cumulative Distribution Function (CDF)**.
- **Speaker Script (45s):**
  > "If someone hands you an 800-page dictionary and asks for page 400, you don't start at page 1 and turn pages one by one. You pinch the book directly in the middle. You might land on page 395, and from there you only need to flip three or four pages to find the exact target. In 2018, Tim Kraska and Google Brain made a groundbreaking observation: a sorted database index is simply a Cumulative Distribution Function. Why store megabytes of tree pointers when you can fit a mathematical function that calculates where the key ought to be?"

---

### SLIDE 15: Static Learned Index (RMI): Architecture & Bounded Errors
- **Visuals:** `report/figures/learned_index_rmi.svg` (Root model $\to$ Leaf model $\to$ Bounded search window $\hat{p} \pm \epsilon$).
- **Inventors & Year:** Tim Kraska et al. (MIT & Google Brain, ACM SIGMOD 2018); BOURBON (USENIX OSDI 2020).
- **Target Systems:** BOURBON (learned RocksDB/WiscKey SSTables), Google BigQuery, columnar Parquet footers.
- **How It Works:**
  - *Two-Stage Hierarchy:* Root model routes key to a leaf partition; leaf model evaluates $pos = \lfloor \alpha \cdot k + \beta \rfloor$.
  - *Strict Error Bounds:* During training, the index records the maximum positive and negative deviation ($\epsilon$).
  - *Bounded Search:* Final discovery uses local binary search within $[\hat{p} - \epsilon, \hat{p} + \epsilon]$, fitting inside 1–2 CPU cache lines.
- **Speaker Script (55s):**
  > "This is the Recursive Model Index, or RMI. Instead of pointer hops, it uses a two-stage hierarchy of lightweight linear models. The root model directs the key to the appropriate leaf model, and the leaf model calculates the predicted position using basic slope-intercept arithmetic. Crucially, during training, RMI calculates the exact maximum prediction error epsilon. It guarantees that the true record is located within a tiny window around the prediction. A bounded binary search completes the lookup inside a single CPU cache line, without a single pointer hop."

---

### SLIDE 16: Static Learned Index (RMI): Memory Collapse
- **Visuals:** Bar comparison: B+ Tree (90.1 Bytes/key) vs Static RMI (**0.7 to 1.4 Bytes/key**). Callout: **>120$\times$ Memory Reduction!**
- **Benchmark Findings (Our Testbed):**
  - **Memory Footprint:** Drops to **1.4 Bytes/key** at $N=5,000$, and **0.7 Bytes/key** at $N=10,000$.
  - **Memory Compression:** **64$\times$ to 120$\times$ smaller than B+ Tree** (90.1 Bytes/key) and LSM-Tree (153.7 Bytes/key).
  - **Point Lookup Latency:** **1.86 ± 0.25 µs** (near B+ Tree speeds, zero pointer traversal).
- **The Trade-off:** Purely immutable. Inserting new keys alters the CDF and requires full $O(N)$ model retraining.
- **Speaker Script (45s):**
  > "Look at the memory numbers from our empirical testbed: While B+ Trees require 90 Bytes per key to maintain pointers and node structures, Static RMI collapses memory consumption to just 0.7 to 1.4 Bytes per key. That is over 120 times more compact than a B+ Tree, while maintaining rapid 1.8-microsecond point lookups! In petabyte-scale data warehouses and immutable SSTables—such as the BOURBON storage engine—this saves massive amounts of expensive server DRAM. Its only limitation is that it is immutable; inserting new keys requires retraining."

---

### SLIDE 17: Dynamic Learned Index (ALEX): The Intuition & Gapped Arrays
- **Visuals:** Diagram of an array with intentionally placed empty slots: `[10] [15] [GAP] [25] [30] [GAP] [45]`.
- **The Analogy:**
  - *A Notebook with Blank Lines Reserved:*
    - If you write notes with zero spaces, adding a sentence in the middle forces you to erase and rewrite the entire page.
    - If you leave three blank lines between sections, you can write new entries immediately without moving other text.
- **Core Concept:** ALEX marries machine-learned CDF projection with **adaptive gapped arrays** and B+ Tree node splitting.
- **Speaker Script (45s):**
  > "To make learned indexes dynamic, Jialin Ding and Tim Kraska introduced ALEX in SIGMOD 2020. If you write your notes tightly packed on a page, inserting a sentence in the middle forces you to erase and rewrite everything below it. But if you intentionally leave blank lines throughout the page, you can insert new notes directly into the nearest empty slot. ALEX distributes empty positions, or GAPs, throughout its leaf arrays. When a write arrives, the model predicts the slot. If it's a gap, write time is O(1). If occupied, it shifts only local keys to the nearest gap."

---

### SLIDE 18: Dynamic Learned Index (ALEX): Adaptive Splitting & Trade-offs
- **Visuals:** Diagram showing DataNode expansion and splitting down into two child nodes.
- **Inventors & Year:** Jialin Ding, Umar Farooq Minhas, Jia Yu, Chi Wang, Jaeyoung Do, Tim Kraska (SIGMOD 2020).
- **Mechanics:**
  - *Internal Nodes:* Route queries via linear models.
  - *Data Nodes:* Hold sorted keys, gaps, and a local regression model.
  - *Adaptive Splitting:* When a node fills or prediction error exceeds bound $\epsilon_{max}$, the node splits or doubles capacity.
  - *Lookup:* Galloping exponential search outward from model-predicted slot.
- **Benchmark Findings (Our Testbed):**
  - Ingestion: **86,739 ± 14,632 ops/s** (fully dynamic real-time insertion).
  - Point Lookup: **2.38 ± 0.54 µs** (uniform) | **3.07 ± 0.56 µs** (skewed).
  - Memory: **104.3 Bytes/key** (includes gap buffer space).
- **Speaker Script (50s):**
  > "When an ALEX data node fills up or prediction error grows too large, it dynamically splits or expands, just like a B+ Tree page split. Lookups use the model to jump directly to candidate slots, followed by an exponential galloping scan. In our benchmarks, ALEX absorbed over 86,000 dynamic insertions per second while delivering 2.3-microsecond lookups. It proves that learned indexes don't have to be read-only. However, keeping empty gaps increases its memory footprint to around 104 Bytes per key, and node splits can cause occasional latency spikes."

---

### SLIDE 19: Scientific Evaluation Methodology
- **Visuals:** Graphic depicting experimental rigor: Real Open Datasets + Warmup Run + 5 Repeated Trials ($\mu \pm \sigma$).
- **Methodology Highlights:**
  - *Real-World Datasets:*
    1. **10,000 Real Geoname IDs** from the global World Cities open dataset (realistic non-uniform spacing and clustering).
    2. **1,655 Real Text Documents** from the Quotes corpus (natural sentence variations).
  - *Scientific Rigor:*
    - 1 Discarded Warmup Run (eliminates cold-start cache and JIT branch predictor noise).
    - 5 Repeated Measurement Trials per metric.
    - All metrics reported as Sample Mean $\pm$ Standard Deviation ($\mu \pm \sigma$).
- **Speaker Script (45s):**
  > "To evaluate these architectures scientifically, we avoided toy synthetic distributions. We extracted 10,000 real geographic IDs from the global World Cities dataset, reflecting real-world clustering, and 1,655 natural language documents from the Quotes corpus. Furthermore, because single benchmark runs can be distorted by CPU cache warming and OS scheduling, every single test executed an initial warmup run that was discarded, followed by five repeated measurement trials. We report the exact sample mean and standard deviation across all tests."

---

### SLIDE 20: Master Head-to-Head Comparison Matrix
- **Visuals:** `report/figures/benchmark_comparison.svg` + Master Benchmark Table:

| Search Architecture | Ingest Throughput (ops/s) | Point Lookup Latency ($\mu$s) | Range Throughput (ops/s) | Memory (Bytes/Key) |
|---|---|---|---|---|
| **B+ Tree (InnoDB)** | **1,176,869 ± 91,008** | **0.77 ± 0.07** | **25,754 ± 2,932** | 90.1 |
| **LSM-Tree (RocksDB)** | 19,731 ± 6,317 | 16.03 ± 8.83 | 1,599 ± 448 | 153.7 |
| **Static RMI (BOURBON)** | 840,904 ± 131,420 | 1.86 ± 0.25 | 15,007 ± 2,556 | **1.4** |
| **Dynamic ALEX** | 86,739 ± 14,632 | 6.44 ± 1.23 | 698 ± 190 | 104.3 |
| **Inverted Index (Lucene)**| 42,370 docs/sec | 233.59 ± 116.72 (AND) | N/A (BKD Tree) | Variable |

- **Speaker Script (55s):**
  > "Here is our master head-to-head comparison matrix, and it tells a compelling story: B+ Tree leads in point lookup latency at 0.77 microseconds and range scans at 25,000 ops/second. But look at Static RMI: it slashes memory footprint down to 1.4 Bytes per key—nearly two orders of magnitude smaller than B+ Trees (90 Bytes) and LSM-Trees (153 Bytes)—while still delivering fast 1.8-microsecond lookups. LSM-Tree accepts higher read latency in exchange for sequential write absorption. Dynamic ALEX strikes a middle ground, enabling updatable learned search at 86,000 writes per second. Every engine dominates in its designated operational envelope."

---

### SLIDE 21: Workload Stress-Tests: Locality & Scaling Curves
- **Visuals:** Two stress-test chart panels:
  - *Panel A (Zipfian Skew):* Uniform (1.00 µs B+ Tree vs 2.38 µs ALEX) vs Zipfian $\alpha=1.3$ (0.65 µs B+ Tree vs 3.07 µs ALEX).
  - *Panel B (Memory Scaling Curve):* RMI footprint collapsing from 3.6 $\to$ 1.5 $\to$ **0.7 Bytes/key** as $N$ scales to 10,000.
- **Key Takeaways:**
  - Skewed access (80/20 rule) speeds up B+ Tree by **35%** due to CPU L1/L2 cache residency.
  - Linear models break the linear storage barrier: index parameters amortize as dataset size grows.
- **Speaker Script (50s):**
  > "We also evaluated these architectures under workload stress-tests. In Panel A, we tested query skew. Under a Zipfian distribution where 80% of queries target 20% of hot records, B+ Tree read latency improved by 35% down to 0.65 microseconds because upper routing pages remain permanently resident in CPU L1/L2 caches. In Panel B, we tracked memory scaling. Traditional B+ Trees maintain a flat 90 Bytes per key because every record requires pointer infrastructure. Static RMI, however, amortizes its linear regression parameters, dropping to just 0.7 Bytes per key as data volume grows."

---

### SLIDE 22: Practical System Selection Framework
- **Visuals:** Flowchart / Decision Tree:
  1. Unstructured text or multi-attribute filtering? $\to$ **Inverted Index + BM25** (Elasticsearch).
  2. Write-dominated ingestion (IoT, logs, clickstreams)? $\to$ **LSM-Tree** (Cassandra / RocksDB).
  3. General transactional OLTP with ACID and low read latency? $\to$ **B+ Tree** (MySQL InnoDB).
  4. Immutable analytical warehouse with DRAM constraints? $\to$ **Static RMI** (BOURBON / BigQuery).
  5. In-memory updatable analytics? $\to$ **Dynamic ALEX**.
- **Speaker Script (50s):**
  > "From these findings, we synthesize a concrete decision framework for systems architects: If your application queries full-text tokens or arbitrary attribute filters, choose an Inverted Index with BM25. If your workload is write-dominated—like IoT telematics or financial audit logging—deploy an LSM-Tree. For standard relational OLTP requiring predictable sub-millisecond point reads and ACID transactions, the B+ Tree remains the gold standard. For immutable analytical partitions where memory costs are prohibitive, use Static RMI to save 90% of index RAM. And for in-memory updatable caching, deploy ALEX."

---

### SLIDE 23: Emerging Frontiers: Hybrid Architectures
- **Visuals:** Conceptual diagram of three cutting-edge hybrid storage designs:
  - **1. Learned LSM-Trees (BOURBON):** Embedding linear models inside immutable SSTables, replacing binary-search fence pointers.
  - **2. Hardware-Accelerated Inverted Indexes:** Using SIMD AVX-512 vector instructions and GPUs for terabit-per-second Roaring Bitmap intersections.
  - **3. Self-Tuning Autonomous Storage:** Dynamic tiering converting cold B+ Tree pages into compressed learned models and hot partitions into gapped arrays.
- **Speaker Script (40s):**
  > "The future of database search lies in combining these paradigms into hybrid engines. Systems like BOURBON embed learned RMI models directly inside LSM SSTables, cutting memory by 80% while accelerating point lookups. Modern search engines are using GPU kernels and SIMD AVX-512 vector instructions to perform bitwise posting list intersections at terabit-per-second memory bandwidths. The boundary between pointers, logs, and models is blurring into self-tuning autonomous storage."

---

### SLIDE 24: Conclusion & Foundational References
- **Visuals:** Summary card + Key Academic Citations:
  - *Bayer & McCreight (1970/1972)* – B-Trees (*Acta Informatica*)
  - *O'Neil et al. (1996)* – LSM-Tree (*Acta Informatica*)
  - *Robertson & Zaragoza (2009)* – BM25 (*Foundations and Trends in IR*)
  - *Athanassoulis et al. (2016)* – RUM Conjecture (*EDBT*)
  - *Kraska et al. (2018)* – Learned Index Structures (*ACM SIGMOD*)
  - *Ding et al. (2020)* – ALEX (*ACM SIGMOD*)
  - *Dai et al. (2020)* – BOURBON (*USENIX OSDI*)
- **Core Summary:** No universal index exists. Workload profiling and the RUM space dictate the optimal architecture.
- **Speaker Script (35s):**
  > "To conclude: there is no silver bullet in database indexing. B+ Trees optimize read latency; LSM-Trees optimize write absorption; Inverted Indexes optimize multi-attribute text pruning; and Learned Models optimize memory footprint. Understanding the RUM trade-off space allows data engineers to design systems matched to the physical realities of their workloads. Thank you very much for your time. We are now open for questions."
