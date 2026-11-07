# PRESENTATION SLIDES: SPECIALIZED MODERN DATABASE SEARCH ENGINES
## An Architectural, Theoretical, and Empirical Analysis: Apache Cassandra (LSM) vs. Elasticsearch (Inverted Index)

**Course:** Data Engineering (CO5173) – Ho Chi Minh City University of Technology (HCMUT)  
**Instructor:** Assoc. Prof. Tran Minh Quang  
**Authors:** Nguyen Dinh Hoang Son (ID: `2670362`) & Nguyen Doan Phuc An (ID: `2670249`)  
**Format:** 16 Progressive Animation Slides + 2 Interactive Live Terminal Demo Stops  
**Target Duration:** Exactly 15 Minutes (Strictly Time-Calibrated)  

---

### PRESENTATION TIMING BREAKDOWN (15:00 TOTAL)
1. **Part 1: Theoretical Foundation & Divergence** — Slides 1 to 2 *(2:00)*
2. **Part 2: Apache Cassandra Architecture (Step-by-Step Animation)** — Slides 3 to 7 *(3:15)*
3. **Part 3: 🛑 LIVE TERMINAL DEMO 1 (Cassandra Engine)** — Slide 8 *(2:00)*
4. **Part 4: Elasticsearch Architecture (Step-by-Step Animation)** — Slides 9 to 13 *(3:15)*
5. **Part 5: 🛑 LIVE TERMINAL DEMO 2 (Elasticsearch & BM25)** — Slide 14 *(2:00)*
6. **Part 6: Empirical Benchmark Synthesis & CQRS Conclusion** — Slides 15 to 16 *(2:30)*

---

## PART 1: THEORETICAL FOUNDATION & DIVERGENCE

### SLIDE 1: Title & Presentation Scope
- **Time Allocation:** 0:45 min (Elapsed: 0:00 – 0:45)
- **Visuals:** Title banner, HCMUT CSE logo, Author IDs.
- **Slide Content:**
  - **Specialized Modern Database Search Engines**
  - *Apache Cassandra (LSM) vs. Elasticsearch (Inverted Index)*
  - **Presenters:** Nguyen Dinh Hoang Son (`2670362`) & Nguyen Doan Phuc An (`2670249`)
  - **Key Premise:** General-purpose tree indexes (B+ Tree) fail under modern workload asymmetry. Storage engines must physically specialize.
- **Speaker Script (45s):**
  > "Good morning, Professor Tran Minh Quang and classmates. Today we present 'Specialized Modern Database Search Engines.' For decades, relational databases relied on B+ Trees as the default answer for data access. But modern data systems have fragmented: high-velocity append workloads like IoT telemetry demand completely different storage physics than multi-attribute text retrieval across terabytes of logs. 
  > Today, we examine the two dominant specialized search paradigms: Apache Cassandra's Log-Structured Merge-Tree and Elasticsearch's Inverted Index. We walk through their architectures step-by-step like an animation, pause for live code demonstrations, and synthesize their real empirical trade-offs."

---

### SLIDE 2: The Governing Law: The RUM Conjecture
- **Time Allocation:** 1:15 min (Elapsed: 0:45 – 2:00)
- **Visuals:** Vector graphic: `report/figures/rum_conjecture.svg` (The RUM Triangle).
- **Slide Content:**
  - **The Storage Trilemma (Athanassoulis et al., EDBT 2016):**
    - **Read Amplification ($R$):** Physical bytes read / logical bytes returned.
    - **Update Amplification ($U$):** Physical bytes written / logical bytes modified.
    - **Memory Amplification ($M$):** Index storage footprint / base data size.
  - **The Trade-Off Bound:** You can optimize at most two overheads; the third inevitably degrades.
  - **Cassandra:** Minimizes **$U$** (append-only) $\to$ compromises **$R$** (multi-SSTable search).
  - **Elasticsearch:** Minimizes **$R$** (instant text search) $\to$ compromises **$M$** (FST memory) & **$U$** (re-indexing).
- **Speaker Script (75s):**
  > "Database engine design is governed by the RUM Conjecture, formulated in 2016. Just as the CAP theorem governs distributed consensus, RUM proves you cannot simultaneously minimize Read Amplification, Update Amplification, and Memory Amplification.
  > In a traditional B+ Tree, updating one 64-byte row rewrites an entire 16 KB page, causing heavy random I/O and high Update Amplification U.
  > To eliminate random disk writes, Apache Cassandra buffers writes in RAM and writes sequential immutable runs, minimizing Update Overhead U at the expense of higher Read Amplification R.
  > In contrast, Elasticsearch solves multi-attribute queries by precomputing inverted posting lists in memory, achieving near-zero Read Overhead R for complex text, but paying with substantial Memory Overhead M.
  > Neither engine is universally superior—they occupy opposite ends of the RUM triangle."

---

## PART 2: APACHE CASSANDRA ARCHITECTURE (STEP-BY-STEP ANIMATION)

### SLIDE 3: Cassandra Storage Hierarchy Overview
- **Time Allocation:** 0:45 min (Elapsed: 2:00 – 2:45)
- **Visuals:** Full Architecture Overview: `report/figures/lsm_tree_architecture.svg`.
- **Slide Content:**
  - **Philosophy:** Defer sorting, eliminate in-place random writes, convert disk I/O into sequential streams.
  - **In-Memory Tier (RAM):**
    - `CommitLog`: Sequential WAL on disk for crash durability ($O(1)$ disk append).
    - `MemTable`: Concurrent lock-free SkipList in DRAM ($O(\log N)$ point writes).
  - **Persistent Tier (Disk):**
    - `Immutable SSTables`: Sorted data runs with in-memory Bloom Filters and Sparse Fence Indexes.
    - `Compaction Engine`: Asynchronous multi-way merge sort.
- **Speaker Script (45s):**
  > "Let us look at Apache Cassandra's storage architecture. Its core philosophy is simple: never update data in place.
  > Instead of seeking randomly on disk, Cassandra partitions storage into an in-memory tier and an immutable persistent tier.
  > Mutations enter a sequential CommitLog on disk for durability and a MemTable SkipList in RAM.
  > As the MemTable fills, it flushes to disk as immutable Sorted String Tables (SSTables).
  > Let us now step through exactly what happens during writes, flushes, reads, and deletes across the next four animation frames."

---

### SLIDE 4: [ANIMATION FRAME 1/4] Cassandra Write Path
- **Time Allocation:** 0:35 min (Elapsed: 2:45 – 3:20)
- **Visual Animation Frame:**
```
Client Mutation: put(k, v)
       │
       ├──► [1. Append Sequential] ────► CommitLog (Disk WAL: 0 seeks, O(1))
       │
       └──► [2. Insert Sorted]     ────► MemTable (Concurrent SkipList in RAM)
                                         Status: Client ACK immediately!
                                         (Zero random disk I/O, Zero page locking)
```
- **Slide Content:**
  - **Dual-write mechanics:** Synchronous append to CommitLog + concurrent insert to MemTable.
  - **Latency:** Microsecond response time in DRAM; no disk head seeks.
- **Speaker Script (35s):**
  > "Frame 1: A client mutation arrives. Cassandra does two things in parallel: it appends the write sequentially to the CommitLog for crash safety, and inserts it into the sorted MemTable in RAM. The client receives an instant acknowledgment. Notice: zero random disk I/O, zero page locking, and zero page splitting."

---

### SLIDE 5: [ANIMATION FRAME 2/4] MemTable Threshold Flush
- **Time Allocation:** 0:35 min (Elapsed: 3:20 – 3:55)
- **Visual Animation Frame:**
```
MemTable reaches Capacity (e.g., 128 MB)
       │
       ▼ [Freeze & Stream Sequential I/O]
┌────────────────────────────────────────────────────────┐
│ Immutable SSTable-0 Created on Disk                    │
│  ├─ Bloom Filter   : Bit array hashed via Murmur3/KM   │
│  ├─ Sparse Index   : Fence keys sampled every 128 keys │
│  └─ Data File      : Strictly sorted key-value records │
└────────────────────────────────────────────────────────┘
MemTable resets to empty; CommitLog segment truncated.
```
- **Slide Content:**
  - **Sequential Disk Flush:** Converts random memory mutations into one contiguous disk stream.
  - **Immutability:** SSTables are never rewritten in place; concurrency requires zero read locks.
- **Speaker Script (35s):**
  > "Frame 2: When the MemTable hits its threshold, Cassandra freezes it and streams it sequentially to disk as an immutable SSTable. The SSTable contains three files: the sorted Data file, a Sparse Fence Index, and an in-memory Bloom filter. The MemTable resets, and the old CommitLog is truncated."

---

### SLIDE 6: [ANIMATION FRAME 3/4] Read Path Pruning & Fast-Fail
- **Time Allocation:** 0:40 min (Elapsed: 3:55 – 4:35)
- **Visual Animation Frame:**
```
Query: get(Key K)
  │
  ├─► [1. Check MemTable] ──(Hit)──► Return Value (0 disk reads)
  │         │ (Miss)
  │         ▼
  └─► [2. Probe SSTables (Newest to Oldest)]
        │
        ├─► [Bloom Filter Test]
        │     ├─► Any Bit == 0? ──► FAST-FAIL PRUNED! (0 Disk Seeks)
        │     └─► All Bits == 1? (Potential Hit)
        │           │
        │           ▼
        └─► [Sparse Fence Index] ──(Binary Search)──► Localized Data Block Seek
```
- **Slide Content:**
  - **Bloom Filter Double-Hashing:** $g_i(x) = (h_1(x) + i \cdot h_2(x)) \pmod m$.
  - Sized at $\sim 10\ \text{bits/key}$ for $1\%$ false positive rate.
  - **Pruning Effect:** $99\%$ of absent key lookups are rejected in RAM before touching disk!
- **Speaker Script (40s):**
  > "Frame 3: How does Cassandra read from multiple SSTables without slow disk scans?
  > It first checks the MemTable in RAM. If missed, it probes each SSTable's Bloom Filter. If any bit is zero, the key is mathematically guaranteed not to exist—pruning the entire SSTable with zero disk I/O!
  > If the filter indicates a potential match, Cassandra binary searches the sparse fence index in RAM to pinpoint the exact disk block."

---

### SLIDE 7: [ANIMATION FRAME 4/4] Tombstones & Compaction
- **Time Allocation:** 0:40 min (Elapsed: 4:35 – 5:15)
- **Visual Animation Frame:**
```
1. Deletion: delete(k) ──► Writes TOMBSTONE(k, timestamp) into MemTable
   (Past versions in older SSTables remain masked until compaction)

2. Asynchronous Multi-Way Merge Compaction:
   [ SSTable-0: k1, k2, k3 (v1) ] ┐
   [ SSTable-1: k3 (v2), k4     ] ┼─► [ Multi-Way Merge ] ─► [ Compacted SSTable: ]
   [ SSTable-2: TOMBSTONE(k2)   ] ┘   (Purge k2, pick k3 v2)   [ k1, k3 (v2), k4   ]
```
- **Slide Content:**
  - **Tombstones:** Immutable deletes represented as timestamped markers.
  - **Compaction:** $O(N)$ streaming merge sort reconciles versions, purges expired tombstones, and bounds Read Amplification ($R$).
- **Speaker Script (40s):**
  > "Frame 4: Because files are immutable, deletes cannot erase bytes from older SSTables. Instead, Cassandra writes a Tombstone with a timestamp.
  > In the background, Compaction performs an $O(N)$ multi-way merge sort across overlapping SSTables. It reconciles duplicate versions, purges dead tombstones, and emits a single, compacted SSTable—reclaiming disk space."

---

### SLIDE 8: 🛑 LIVE CODE DEMO STOP 1: Cassandra Engine
- **Time Allocation:** 2:00 min (Elapsed: 5:15 – 7:15)
- **Visuals:** Full-screen terminal session running `demo.py`.
- **Slide Content:**
  - **DEMO STOP 1: APACHE CASSANDRA IN ACTION**
  - **Terminal Command:**
    ```bash
    python3 demo.py --cassandra
    ```
  - **Live Execution Checkpoints:**
    1. *Step 1:* Ingestion into MemTable & CommitLog.
    2. *Step 2:* Capacity threshold trigger $\to$ SSTable-0 flush with Bloom filter generation.
    3. *Step 3:* Existing key point hit ($5.4\ \mu\text{s}$) vs. Absent key Bloom filter **Fast-Fail** ($3.4\ \mu\text{s}$, 0 disk reads).
    4. *Step 4:* Tombstone deletion & Multi-way merge compaction permanently purging dead keys.
- **Speaker Script (120s):**
  > "Now, let us switch directly to the terminal and see Cassandra's storage engine execute live.
  > *(Switch to terminal and run `python3 demo.py --cassandra`)*
  > In Step 1, we insert records into our MemTable. You can see the keys ordered in RAM.
  > In Step 2, our fourth key triggers the threshold. Notice SSTable-0 is created on disk, generating fence pointers and Bloom filter bits.
  > In Step 3, watch the read path: when querying existing key 102, the Bloom filter hits and retrieves the value. But look at absent key 999: the Bloom filter calculates hash bits, discovers a zero, and immediately returns false. The SSTable data file is never opened!
  > In Step 4, we delete key 102. It writes a Tombstone. When we trigger multi-way merge compaction, SSTable-0 and SSTable-1 merge, key 102 is permanently purged, and disk space is recovered.
  > Let us return to our slides and explore Elasticsearch."

---

## PART 3: ELASTICSEARCH ARCHITECTURE (STEP-BY-STEP ANIMATION)

### SLIDE 9: Elasticsearch & Inverted Index Overview
- **Time Allocation:** 0:45 min (Elapsed: 7:15 – 8:00)
- **Visuals:** Full Architecture Overview: `report/figures/inverted_index_architecture.svg`.
- **Slide Content:**
  - **Philosophy:** Invert the relationship: instead of `Doc -> [Terms]`, store `Term -> [Sorted DocIDs]`.
  - **Target Workload:** Arbitrary multi-attribute search, log analytics, and relevance ranking.
  - **Core Components:**
    - `Analysis Pipeline`: Character Filter $\to$ Tokenizer $\to$ Token Filters (Stemming).
    - `Term Dictionary`: In-memory Finite State Transducer (FST) with prefix/suffix compression.
    - `Posting Lists`: Sorted document IDs with Skip Lists and term frequencies ($tf$).
    - `BM25 Scoring`: Probabilistic relevance ranking with length normalization.
- **Speaker Script (45s):**
  > "Now we transition to Elasticsearch and Apache Lucene.
  > Why can't Cassandra or MySQL handle search? Because they map documents to columns. To search 'distributed consensus' in millions of log rows, a relational database must scan every single line of text.
  > Elasticsearch solves this by inverting the relationship: creating a dictionary of all unique terms, mapping each word to the sorted list of documents containing it.
  > Let us trace a document through the analysis pipeline, FST dictionary, skip lists, and BM25 scoring across the next four animation frames."

---

### SLIDE 10: [ANIMATION FRAME 1/4] Text Analysis Pipeline
- **Time Allocation:** 0:35 min (Elapsed: 8:00 – 8:35)
- **Visual Animation Frame:**
```
Raw Text: "Apache Cassandra provides high write throughput with LSM trees!"
  │
  ├──► [1. Char Filter]   ──► Strips HTML tags, decodes special symbols
  │
  ├──► [2. Tokenizer]     ──► Splits on whitespace/punctuation:
  │                           ["Apache", "Cassandra", "provides", "high", ...]
  │
  └──► [3. Token Filters] ──► Lowercasing: "Cassandra" -> "cassandra"
                              Stop-words: drops "with"
                              Porter Stemmer: "provides" -> "provid", "trees" -> "tree"
```
- **Slide Content:**
  - Normalizes linguistic variations into canonical root tokens.
  - Ensures queries match text regardless of case or grammatical inflection.
- **Speaker Script (35s):**
  > "Frame 1: Before text can be indexed, it enters the Analysis Pipeline. Character filters strip markup; the tokenizer breaks sentences into words on whitespace and punctuation; and token filters lowercase tokens, remove stop-words, and apply linguistic stemmers like the Porter Stemmer—reducing 'indexing' and 'indexes' to the root 'index'."

---

### SLIDE 11: [ANIMATION FRAME 2/4] FST Term Dictionary & Posting Lists
- **Time Allocation:** 0:35 min (Elapsed: 8:35 – 9:10)
- **Visual Animation Frame:**
```
TERM DICTIONARY (In-Memory FST)              POSTING LISTS (On Disk / OS Cache)
┌─────────────────────────────────┐          ┌────────────────────────────────────────┐
│ Finite State Transducer         │          │ Strictly Sorted by doc_id              │
│ (Prefix & Suffix Compressed)    │          │                                        │
│  "cassandra" ───────────────────┼─────────►│ [Doc 1 (tf:1)] ──► [Doc 3 (tf:2)]      │
│  "elastic"   ───────────────────┼─────────►│ [Doc 2 (tf:1)] ──► [Doc 4 (tf:1)]      │
│  "lsm"       ───────────────────┼─────────►│ [Doc 1 (tf:2)]                          │
│  "write"     ───────────────────┼─────────►│ [Doc 1 (tf:1)] ──► [Doc 2 (tf:1)]      │
└─────────────────────────────────┘          └────────────────────────────────────────┘
Lookup complexity: O(term_length)            Contains: doc_id, term_freq, positions
```
- **Slide Content:**
  - **FST:** In-memory graph sharing prefixes and suffixes; instant term lookup in $O(\text{len})$.
  - **Posting Lists:** Sorted arrays enabling fast set-theoretic operations.
- **Speaker Script (35s):**
  > "Frame 2: Lucene stores unique terms in a Finite State Transducer (FST) in memory. Because the FST compresses common prefixes and suffixes, millions of terms fit into megabytes of RAM, resolving term lookups in order term-length time.
  > Each term points to its Posting List: a sorted sequence of Document IDs and term frequencies."

---

### SLIDE 12: [ANIMATION FRAME 3/4] Boolean Search with Skip Lists
- **Time Allocation:** 0:40 min (Elapsed: 9:10 – 9:50)
- **Visual Animation Frame:**
```
Query: "write" AND "search"
Posting P("write"):  [Doc 1] ──────────────────► [Doc 45] ──► [Doc 99]
                           \ (Skip Pointer: d=45) /
Posting P("search"): [Doc 12] ─► [Doc 28] ─────► [Doc 45] ──► [Doc 80]

Step 1: P("write") at Doc 1 < P("search") at Doc 12 -> Hop via Skip Pointer to Doc 45!
Step 2: P("search") at Doc 12 < 45 -> Scan to Doc 45 -> MATCH FOUND: Doc 45!
Intersection Complexity: O(min(|P1|, |P2|))
```
- **Slide Content:**
  - **Skip Pointers:** Embedded every $K$ documents (e.g., 16 docs) in posting lists.
  - Allows skipping non-matching document blocks in $O(1)$ time without scanning every entry.
- **Speaker Script (40s):**
  > "Frame 3: For multi-term queries like 'write AND search', Elasticsearch intersects their sorted posting lists.
  > To avoid scanning millions of documents, Lucene equips postings with Skip Lists. If list A is at doc 1 and list B is at doc 45, list A uses its skip pointer to leap directly to doc 45 in $O(1)$ time, skipping over intermediate documents. Set intersection executes in $O(\min(|P_1|, |P_2|))$."

---

### SLIDE 13: [ANIMATION FRAME 4/4] Okapi BM25 Relevance Scoring
- **Time Allocation:** 0:45 min (Elapsed: 9:50 – 10:35)
- **Visual Animation Frame:**
```
Score(D, Q) = ∑ [ IDF(q) · ( tf(q, D) · (k₁ + 1) ) / ( tf(q, D) + k₁ · (1 - b + b · |D| / avgdl) ) ]
                  ▲              ▲                                   ▲
                  │              │                                   │
       1. Inverse Doc Freq    2. TF Saturation Curve             3. Length Penalty
       Rare terms get higher  Marginal gain decays               Penalizes verbose docs,
       weight multiplier.     (Caps keyword stuffing).           boosts concise matches.
       k₁ = 1.2               b = 0.75
```
- **Slide Content:**
  - Replaces naive linear TF-IDF with an asymptotic saturation curve ($k_1 = 1.2$).
  - Document length normalization ($b = 0.75$) prevents long documents from unfairly dominating.
- **Speaker Script (45s):**
  > "Frame 4: Elasticsearch ranks results using Okapi BM25.
  > First, Inverse Document Frequency assigns higher weight to rare terms.
  > Second, the parameter $k_1 = 1.2$ introduces term frequency saturation: unlike linear TF-IDF where repeating a word 50 times multiplies your score by 50, BM25 asymptotes toward $k_1 + 1$, neutralizing keyword stuffing.
  > Third, parameter $b = 0.75$ penalizes verbose documents and rewards concise matches."

---

### SLIDE 14: 🛑 LIVE CODE DEMO STOP 2: Elasticsearch & BM25
- **Time Allocation:** 2:00 min (Elapsed: 10:35 – 12:35)
- **Visuals:** Full-screen terminal session running `demo.py`.
- **Slide Content:**
  - **DEMO STOP 2: ELASTICSEARCH IN ACTION**
  - **Terminal Command:**
    ```bash
    python3 demo.py --elasticsearch
    ```
  - **Live Execution Checkpoints:**
    1. *Step 1:* Analysis pipeline tokenization & Porter stemming.
    2. *Step 2:* Inverted posting list inspection (`Term -> [Doc IDs, TF]`).
    3. *Step 3:* Boolean AND query set intersection (`"write" AND "search"`).
    4. *Step 4:* Okapi BM25 ranked scoring breakdown.
    5. *Step 5:* Live speedup benchmark: Inverted Index vs. Brute-force linear scan over 1,655 quotes (**70x+ faster!**).
- **Speaker Script (120s):**
  > "Let us return to the terminal for Demo 2: Elasticsearch in action.
  > *(Switch to terminal and run `python3 demo.py --elasticsearch`)*
  > In Step 1, our text passes through the tokenizer and stemmer, turning 'throughput' and 'provides' into normalized root tokens.
  > In Step 2, you see the inverted index entries: each term points to its sorted posting list with doc IDs and term frequencies.
  > In Step 3, we execute a Boolean AND query for 'write' and 'search'. Lucene intersects the posting lists and returns Document 3 in microseconds.
  > In Step 4, we run BM25 ranked scoring for 'write search database'. BM25 calculates the exact scores, ranking Document 3 highest because it matches multiple query terms.
  > In Step 5, we test against the real 1,655-document quotes corpus. A linear scan takes over 3,000 microseconds. The Inverted Index resolves the query in just 11 microseconds—delivering a massive 280x live speedup!
  > Let us return to the slides for our empirical conclusions."

---

## PART 4: EMPIRICAL BENCHMARKS & ARCHITECTURAL SYNTHESIS

### SLIDE 15: Head-to-Head Empirical Benchmark Results
- **Time Allocation:** 1:15 min (Elapsed: 12:35 – 13:50)
- **Visuals:** Empirical bar charts: `report/figures/benchmark_comparison.svg`.
- **Slide Content:**

| Empirical Dimension (5 Trials, $\mu \pm \sigma$) | Apache Cassandra (LSM) | Elasticsearch (Inverted Index) |
| :--- | :---: | :---: |
| **Ingestion Throughput** | **$85,624 \pm 6,126\ \text{ops/s}$** | **$93,935 \pm 3,385\ \text{docs/s}$** |
| **Point Lookup Latency (Hit)** | **$5.42 \pm 0.27\ \mu\text{s}$** | N/A |
| **Negative Query Latency (Miss)** | **$3.42 \pm 0.71\ \mu\text{s}$** (Bloom fast-fail) | N/A |
| **Boolean AND Query Latency** | N/A | **$20.36 \pm 3.98\ \mu\text{s}$** |
| **BM25 Top-5 Ranked Query Latency** | N/A | **$118.40 \pm 15.83\ \mu\text{s}$** |
| **Index Memory Footprint** | **$153.7\ \text{Bytes/key}$** | **$2,292.8\ \text{Bytes/document}$** |

- **Key Takeaways:**
  - Cassandra achieves high ingestion with low memory overhead ($153.7\ \text{B/key}$), relying on Bloom filters to protect against Read Amplification.
  - Elasticsearch delivers sub-millisecond lexical queries, but requires $15\times$ more memory ($2,292.8\ \text{B/doc}$) for FST term dictionaries.
- **Speaker Script (75s):**
  > "Here are our consolidated benchmark results measured across repeated trials over 10,000 geographic keys and 1,655 natural language quotes.
  > Cassandra delivers over 85,000 operations per second write throughput, with point lookup hits at 5.4 microseconds and Bloom filter fast-fails at 3.4 microseconds. Its index memory footprint is extremely compact: just 153.7 Bytes per key.
  > Elasticsearch matches ingestion via its in-memory buffer, and evaluates Boolean AND queries in 20 microseconds and BM25 ranking in 118 microseconds. But notice the RUM memory trade-off: it consumes 2,292 Bytes per document—fifteen times more memory—to maintain its rich FST term dictionary and posting metadata."

---

### SLIDE 16: Architectural Synthesis: CQRS Pattern & System Selection
- **Time Allocation:** 1:10 min (Elapsed: 13:50 – 15:00)
- **Visuals:** Architecture Diagram: CQRS Integration Pattern (Cassandra Writes $\to$ Debezium/Kafka CDC $\to$ Elasticsearch Queries) + Decision Tree.
- **Slide Content:**
  - **The Golden Rule:** Never force a single engine outside its RUM specialization.
    - Secondary indexes (`2i`) in Cassandra cause cluster-wide scatter-gather latency spikes.
    - Using Elasticsearch as a primary write-heavy database causes segment merge thrashing.
  - **The Production Solution: Dual-Engine CQRS:**
    - **Cassandra (Write Path / System of Record):** Absorbs high-volume ingestion with linear horizontal scaling.
    - **Change Data Capture (CDC / Debezium / Kafka):** Asynchronously streams commit-log mutations.
    - **Elasticsearch (Read Path / Search & Analytics):** Builds inverted indexes to serve rich user search and BM25 ranking.
- **Speaker Script (70s):**
  > "To conclude: what is the final engineering takeaway?
  > Never force an engine to handle queries that contradict its physical design.
  > If you add secondary indexes to Cassandra, you cause scatter-gather latency spikes across every node. If you use Elasticsearch as a high-concurrency transactional database, constant segment merges and GC pauses will degrade your cluster.
  > The enterprise standard is CQRS: Command Query Responsibility Segregation.
  > Deploy Apache Cassandra as your primary System of Record to absorb high-velocity writes with guaranteed durability and linear scaling.
  > Then, use Change Data Capture—via Debezium or Kafka—to asynchronously stream mutations into Elasticsearch to serve rich BM25 text queries and analytics.
  > By understanding the RUM Conjecture, we combine specialized architectures to achieve optimal scale.
  > Thank you, and we welcome your questions!"

---

## APPENDIX: LIVE DEMO CHEAT SHEET FOR PRESENTERS

| Demo Section | Command to Run | What to Point at on Screen | Duration |
| :--- | :--- | :--- | :---: |
| **Demo 1: Cassandra** | `python3 demo.py --cassandra` | MemTable order $\to$ SSTable flush $\to$ Bloom Filter FAST-FAIL $\to$ Tombstone purge during compaction | 2:00 min |
| **Demo 2: Elasticsearch** | `python3 demo.py --elasticsearch` | Tokenizer output $\to$ Posting lists $\to$ Skip Pointer intersection $\to$ BM25 scores $\to$ 70x+ speedup over linear scan | 2:00 min |
| **Backup / Benchmark** | `python3 demo.py --benchmarks` | Full statistical table with sample mean ($\mu$) and standard deviation ($\sigma$) | Extra Q&A |
