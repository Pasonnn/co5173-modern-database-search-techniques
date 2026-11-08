# CO5173 — Storage Engine Duality: Cassandra (LSM) vs Elasticsearch (Inverted Index)
## Complete 23-Slide Presentation Content & Bilingual Speaker Transcripts

> **Presentation Pacing:** 23 bite-sized visual slides designed for a 15-minute presentation (~39 seconds per slide).
> **Bilingual Delivery:** Full scripts provided in both English (EN) and Vietnamese (VI).

---

### Slide 01: Storage Engine Duality
**Section:** `00 Introduction` | **Badge:** `Cover Slide`  
**Subtitle:** *Apache Cassandra (LSM-Tree) vs. Elasticsearch (Inverted Index) — A Comparative Study*  

#### Key Points:
- Master's thesis defense: Rigorous empirical and theoretical comparison between Log-Structured Merge-Trees and Inverted Indexes.
- Investigating how physical on-disk storage layouts dictate macro-architectural throughput and query latency.
- Validated through clean-room reference engines, real-world datasets (10k cities, 1,655 quotes), and 5-round statistical benchmarks.

#### Verbatim Spoken Scripts:
- **English (EN):** "Good day, esteemed committee members and colleagues. Welcome to our defense presentation for CO5173 Advanced Data Engineering. Today, we present a comparative investigation into the storage engine duality between Apache Cassandra's LSM-Tree and Elasticsearch's Inverted Index. In modern data systems, no single database can simultaneously maximize write ingestion and arbitrary text search. Over the next 15 minutes, we examine the fundamental storage laws that govern this trade-off, contrast their internal mechanics, present empirical benchmark evidence, and demonstrate their production synthesis under CQRS."
- **Tiếng Việt (VI):** "Kính chào quý Thầy Cô trong Hội đồng và các bạn học viên cao học. Chào mừng quý vị đến với buổi bảo vệ đồ án môn CO5173 Kỹ nghệ Dữ liệu Nâng cao. Hôm nay, nhóm xin trình bày nghiên cứu so sánh về tính nhị nguyên kiến trúc lưu trữ giữa LSM-Tree của Apache Cassandra và Chỉ mục đảo của Elasticsearch. Trong các hệ thống dữ liệu lớn, không một cơ sở dữ liệu đơn lẻ nào có thể vừa tối đa hóa tốc độ ghi, vừa tối ưu hóa tìm kiếm văn bản tùy ý. Trong 15 phút tới, nhóm sẽ làm rõ quy luật lưu trữ chi phối sự đánh đổi này, đối chiếu cơ chế vật lý bên trong, minh chứng bằng thực nghiệm và tổng hợp mô hình CQRS trong thực tế."

---

### Slide 02: Master's Defense Roadmap (15-Minute Target)
**Section:** `00 Introduction` | **Badge:** `15-Min Roadmap`  
**Subtitle:** *4 Core Acts: Storage Crisis → Storage Mechanics → Empirical Validation → CQRS Synthesis*  

#### Key Points:
- Consolidated 23 visual slides calibrated for a strict 15-minute defense window (~39 seconds per slide).
- Act 1: The physical storage crisis and the theoretical foundation of the RUM Conjecture.
- Act 2 & 3: Deep dive into LSM-Tree write paths, compaction debt, Bloom filters, and Lucene's NRT pipeline.
- Act 4: Architectural convergence, 5-round empirical verification, and dual-engine CQRS production synthesis.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is our defense roadmap structured into four distinct acts across 23 slides, calibrated precisely for a 15-minute presentation. In Act 1, we analyze the storage crisis—showing why traditional relational engines fail under write-heavy loads and full-text search. In Act 2, we dissect Cassandra's LSM-tree architecture, sequential appends, and compaction debt. In Act 3, we explore Lucene's inverted index, NRT refresh pipeline, and BM25 ranking. Finally, in Act 4, we reveal their architectural convergence, present 5-round empirical benchmark proofs, and show how both engines synthesize in production via CQRS."
- **Tiếng Việt (VI):** "Đây là lộ trình báo cáo gồm 4 phần xuyên suốt 23 slide, được căn chỉnh chính xác cho khung thời gian 15 phút bảo vệ. Trong Phần 1, nhóm phân tích cuộc khủng hoảng lưu trữ—chỉ ra vì sao các hệ RDBMS truyền thống gặp bế tắc trước tải ghi lớn và truy vấn toàn văn. Trong Phần 2, ta mổ xẻ kiến trúc LSM-Tree của Cassandra, luồng ghi tuần tự và nợ dồn compaction. Trong Phần 3, ta khám phá chỉ mục đảo của Lucene, quy trình làm tươi NRT và thuật toán BM25. Cuối cùng, trong Phần 4, nhóm chỉ ra sự hội tụ kiến trúc giữa hai hệ thống, công bố số liệu thực nghiệm qua 5 lượt đo và mô hình tích hợp CQRS trong thực tế."

---

### Slide 03: Traditional Databases: The Overwrite & Eviction Trap
**Section:** `01 Storage Crisis` | **Badge:** `Problem 1: B+ Tree`  
**Subtitle:** *Dirty Page Eviction & Unbuffered Write Amplification in In-Place B+ Trees*  

#### Key Points:
- Production RDBMS (PostgreSQL, MySQL InnoDB) absorb updates in RAM buffer pools and append sequentially to WAL.
- However, dirty pages must eventually flush back to disk in-place during checkpoints or cache eviction.
- Modifying a 50-byte record forces rewriting the entire 16,384-byte page: a 327× worst-case write amplification.
- Under sustained write pressure, page eviction induces severe random disk I/O thrashing and write stalls.

#### Verbatim Spoken Scripts:
- **English (EN):** "To understand why specialized engines were born, we examine the overwrite trap in relational B+ Tree architectures like InnoDB or PostgreSQL. When a 50-byte record is updated, modern RDBMS absorb writes in memory and append to a Write-Ahead Log. But when dirty pages must be flushed or evicted from the buffer pool during checkpoints, the database must write back the entire 16-kilobyte page in-place. This worst-case 327-fold write amplification causes random disk seeking, saturates controller bandwidth, and caps write ingestion under sustained load."
- **Tiếng Việt (VI):** "Để hiểu vì sao các cơ sở dữ liệu chuyên biệt ra đời, trước hết ta phân tích cái bẫy ghi đè của cây B+ trong các hệ RDBMS như InnoDB hay PostgreSQL. Khi cập nhật một bản ghi 50 byte, hệ thống ghi log tuần tự vào WAL và đệm trên RAM. Tuy nhiên, khi các trang bẩn bị đẩy ra đĩa (page eviction) hoặc xả định kỳ (checkpoint), hệ thống buộc phải ghi đè lại toàn bộ trang 16 KB tại chỗ. Hệ số khuếch đại ghi 327 lần ở pha xả đĩa này tạo ra các thao tác tìm kiếm ngẫu nhiên, làm nghẽn băng thông điều khiển đĩa và giới hạn thông lượng ghi khi chịu tải liên tục."

---

### Slide 04: Traditional Databases: The Full-Scan Trap
**Section:** `01 Storage Crisis` | **Badge:** `Problem 2: Full Scan`  
**Subtitle:** *Why Leading Wildcards and Full-Text Queries Bypass B+ Tree Indexes*  

#### Key Points:
- B+ Trees index keys via lexicographical prefix sorting; queries with leading wildcards (LIKE '%term%') cannot prune tree branches.
- The storage engine falls back to an exhaustive Table Scan ($O(N)$), reading every disk page into the buffer pool.
- Traditional relational indexes cannot compute term frequency (TF), document frequency (IDF), or probabilistic relevance scores.

#### Verbatim Spoken Scripts:
- **English (EN):** "The second fundamental failure of traditional databases is full-text search. Relational B+ Trees index strings strictly by their sorted prefixes. When a query contains a leading wildcard such as LIKE '%database%', the index is completely blind and cannot prune any tree branches. The engine is forced to execute an exhaustive table scan, reading every row from disk. This wastes massive I/O, floods the buffer pool, and lacks any mathematical capability to rank which record is the most relevant."
- **Tiếng Việt (VI):** "Thất bại căn bản thứ hai của cơ sở dữ liệu truyền thống là tìm kiếm toàn văn. Cây B+ chỉ lập chỉ mục chuỗi ký tự theo thứ tự tiền tố đã sắp xếp. Khi câu truy vấn chứa ký tự đại diện ở đầu như LIKE '%database%', cây chỉ mục hoàn toàn vô hiệu và không thể tỉa nhánh. Hệ thống buộc phải quét toàn bộ bảng, nạp từng dòng dữ liệu từ đĩa vào bộ đệm. Thao tác này gây lãng phí tài nguyên I/O nghiêm trọng, làm tràn bộ đệm RAM và hoàn toàn không có khả năng tính điểm xếp hạng độ liên quan của kết quả."

---

### Slide 05: The Writer vs. Reader Conflict
**Section:** `01 Storage Crisis` | **Badge:** `The Conflict`  
**Subtitle:** *Why One Physical Layout Cannot Simultaneously Maximize Writes and Text Search*  

#### Key Points:
- Fastest Write Path: Raw sequential byte append with zero upfront parsing or index reorganization.
- Fastest Search Path: Heavy upfront tokenization, morphological stemming, dictionary hashing, and inverted posting list sorting.
- A single monolithic storage layout cannot satisfy both requirements without crippling performance in one dimension.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here lies the core dilemma of database storage engineering: the mechanical requirements for fast writes directly oppose the requirements for fast search. To achieve maximum write throughput, an engine must perform minimal upfront work—simply appending raw bytes sequentially. Conversely, to deliver microsecond full-text search, an engine must perform exhaustive upfront indexing—tokenizing, sorting, and cross-referencing every term. Attempting both on a single storage layout forces an unacceptable compromise."
- **Tiếng Việt (VI):** "Đây chính là thế lưỡng nan cốt lõi của kỹ nghệ lưu trữ cơ sở dữ liệu: các yêu cầu vật lý để ghi nhanh hoàn toàn đối nghịch với các yêu cầu để tìm kiếm nhanh. Để đạt thông lượng ghi tối đa, hệ thống phải thực hiện tối thiểu thao tác xử lý ban đầu—chỉ ghi nối tiếp các byte tuần tự. Ngược lại, để tìm kiếm toàn văn trong vài micro-giây, hệ thống phải trả giá bằng việc lập chỉ mục chuyên sâu ngay từ đầu—tách từ, chuẩn hóa và sắp xếp danh sách tài liệu. Cố gắng dung hòa cả hai trên một cấu trúc lưu trữ đơn lẻ chắc chắn sẽ dẫn đến sự thỏa hiệp hiệu năng trầm trọng."

---

### Slide 06: The Fundamental Storage Law: The RUM Conjecture
**Section:** `01 Storage Crisis` | **Badge:** `Storage Law`  
**Subtitle:** *Minimizing Two Database Overheads Inevitably Worsens the Third: Read (R), Update (U), Memory (M)*  

#### Key Points:
- RUM Conjecture (Harvard/BU): Database designs can optimize at most two corners: Read (R), Update (U), or Memory (M).
- Cassandra optimizes Update ($U$) and Memory ($M$) via sequential append and compact Bloom filters, accepting Read ($R$) penalty.
- Elasticsearch optimizes Read ($R$) via inverted posting lists, accepting massive Memory ($M \sim 15\times$) and Update ($U$) costs.

#### Verbatim Spoken Scripts:
- **English (EN):** "This physical boundary was formalized by researchers at Harvard and Boston University as the RUM Conjecture. It proves that no storage engine can simultaneously minimize Read overhead (R), Update overhead (U), and Memory overhead (M). You can optimize at most two. Cassandra prioritizes Update and Memory overhead through sequential appends and compact Bloom filters, accepting read complexity. Elasticsearch strictly optimizes Read latency, paying a massive penalty in memory and index maintenance."
- **Tiếng Việt (VI):** "Ranh giới vật lý này đã được các nhà nghiên cứu tại Harvard và Đại học Boston hình thức hóa thành Giả thuyết RUM. Định lý chứng minh rằng không một bộ máy lưu trữ nào có thể đồng thời tối thiểu hóa cả chi phí Đọc (Read - R), Ghi (Update - U) và Bộ nhớ (Memory - M). Ta chỉ có thể tối ưu tối đa hai đỉnh. Cassandra ưu tiên chi phí Ghi và Bộ nhớ thông qua ghi tuần tự và Bloom Filter cô đọng, chấp nhận đánh đổi độ phức tạp khi đọc. Ngược lại, Elasticsearch tối ưu triệt để độ trễ Đọc, chấp nhận tiêu tốn gấp nhiều lần RAM và chi phí bảo trì chỉ mục."

---

### Slide 07: LSM Storage Engine: The Desk Notepad
**Section:** `02 LSM & Cassandra` | **Badge:** `Analogy Step 1`  
**Subtitle:** *Step 1: Low-Latency Ingestion via MemTable (RAM) and Sequential CommitLog (Disk)*  

#### Key Points:
- Client writes are received in RAM into a sorted MemTable (concurrent skip list or balanced tree).
- Simultaneously, writes are appended sequentially to a durable on-disk CommitLog (Write-Ahead Log).
- Because writes require zero disk seeks and no in-place page rewriting, write operations acknowledge in microseconds.

#### Verbatim Spoken Scripts:
- **English (EN):** "To understand Cassandra's Log-Structured Merge-Tree, consider a librarian at a busy intake desk. When thousands of books arrive every minute, you do not run to the shelves to insert each book in alphabetical order. Instead, you quickly jot each entry onto your desk notepad. In Cassandra, this notepad is the MemTable in RAM. For crash resilience, an append-only CommitLog sequentially records every transaction on disk. Because there are zero disk seeks, the write returns in microseconds."
- **Tiếng Việt (VI):** "Để hiểu cây LSM của Cassandra, hãy hình dung một thủ thư tại bàn tiếp nhận sách bận rộn. Khi hàng ngàn cuốn sách đổ về mỗi phút, ta không thể chạy đến từng kệ sách để xếp xen kẽ từng cuốn theo thứ tự chữ cái. Thay vào đó, ta ghi thật nhanh vào cuốn sổ tay trên bàn. Trong Cassandra, cuốn sổ tay này chính là MemTable trên RAM. Để đảm bảo an toàn dữ liệu khi sự cố xảy ra, một tiến trình ghi nhật ký CommitLog tuần tự nối tiếp lên đĩa. Do không phát sinh thao tác tìm kiếm ngẫu nhiên trên đĩa, lệnh ghi phản hồi ngay lập tức trong vài micro-giây."

---

### Slide 08: LSM Lifecycle: SSTables & Background Compaction
**Section:** `02 LSM & Cassandra` | **Badge:** `SSTable & Compaction`  
**Subtitle:** *Freezing Immutable Files, Purging Tombstones, and the Hidden Cost of Compaction Debt*  

#### Key Points:
- When MemTable reaches capacity threshold, it freezes and flushes to disk as an immutable SSTable via sequential I/O.
- Deletions are non-destructive: a Tombstone marker with a deletion timestamp is appended to the stream.
- Background Compaction: Multi-way merge sort merges overlapping SSTables, discards obsolete versions, and evicts tombstones.
- Trade-off (Compaction Debt): LSM defers write work rather than eliminating it. Leveled Compaction incurs 10×–30× write amplification; sustained ingestion can cause I/O debt that throttles foreground writes.

#### Verbatim Spoken Scripts:
- **English (EN):** "When the MemTable fills, Cassandra freezes it and writes an immutable, sorted SSTable sequentially to disk. Deletions do not overwrite data; they are appended as Tombstones. In the background, compaction merges multiple SSTables to eliminate duplicates and reclaim space. But this reveals LSM's critical trade-off: write work is deferred, not eliminated. Leveled compaction introduces a 10× to 30× background write amplification factor. If ingestion exceeds disk bandwidth, background compaction debt will eventually throttle foreground writes."
- **Tiếng Việt (VI):** "Khi MemTable đầy, Cassandra đóng băng và xả tuần tự xuống đĩa thành một file SSTable bất biến. Thao tác xóa không ghi đè dữ liệu mà ghi nhận bằng thẻ Tombstone. Ở chế độ nền, tiến trình Compaction hòa trộn nhiều SSTable để loại bỏ dữ liệu cũ và thu hồi dung lượng. Tuy nhiên, đây là sự đánh đổi cốt lõi: công việc ghi bị trì hoãn chứ không biến mất. Compaction theo tầng tạo ra hệ số khuếch đại ghi nền từ 10 đến 30 lần. Nếu nợ dồn I/O compaction tích tụ, hệ thống sẽ buộc phải bóp nghẹt luồng ghi đầu vào."

---

### Slide 09: Storage Physics: Why Sequential Writing Wins
**Section:** `02 LSM & Cassandra` | **Badge:** `Hardware Physics`  
**Subtitle:** *Sequential Appends Outpace Random Seeks by 50× to 100× on HDDs and NVMe SSDs*  

#### Key Points:
- Mechanical Disks (HDD): Random head seeks require 5–10 ms physical latency, whereas sequential writes stream at 150+ MB/s.
- Solid-State Drives (SSD): Random in-place updates trigger Flash Translation Layer (FTL) block erases and write amplification.
- Cassandra's pure sequential append architecture achieves 52,339 sustained ops/s (bursting to 85,000 ops/s) on standard hardware.

#### Verbatim Spoken Scripts:
- **English (EN):** "The mechanical foundation of Cassandra's write performance is hardware physics. On spinning hard drives, random seeks force physical actuator arm repositioning, taking 5 to 10 milliseconds. On modern NVMe SSDs, random updates trigger block erase cycles in the Flash Translation Layer. By transforming all mutations into strictly sequential appends, Cassandra achieves over 52,000 sustained writes per second, bursting up to 85,000 on standard commodity hardware."
- **Tiếng Việt (VI):** "Nền tảng cơ học cho tốc độ ghi của Cassandra xuất phát từ vật lý phần cứng. Trên ổ đĩa cơ HDD, tìm kiếm ngẫu nhiên bắt buộc đầu đọc cơ khí phải dịch chuyển, tốn từ 5 đến 10 mili-giây. Trên ổ SSD NVMe hiện đại, việc cập nhật ngẫu nhiên tại chỗ gây ra các chu kỳ xóa khối của tầng FTL. Bằng cách chuyển đổi mọi thao tác ghi thành luồng ghi tuần tự thuần túy, Cassandra đạt thông lượng bền vững hơn 52.000 lượt ghi/giây và đạt đỉnh 85.000 trên phần cứng phổ thông."

---

### Slide 10: LSM Read Path: Bloom Fast-Fail vs. Positive Read Latency
**Section:** `02 LSM & Cassandra` | **Badge:** `Read Path Asymmetry`  
**Subtitle:** *O(1) Negative Check (3.42 µs) vs. Multi-SSTable Traversal for Existing Keys*  

#### Key Points:
- Negative Read Path: In-memory Bloom filter (10 bits/key) computes $k$ hashes; a single 0-bit fast-fails in $3.42\ \mu\text{s}$ with zero disk seeks.
- Positive Read Path: When keys exist, Bloom filter returns positive. The engine must traverse MemTable and multiple SSTable levels.
- Index Decoding: Positive point lookups must decode partition summaries and index fences to reconcile versions and tombstones.
- Read Amplification: LSM engines have higher positive point-read latency and amplification compared to balanced B+ Trees.

#### Verbatim Spoken Scripts:
- **English (EN):** "Because SSTables are immutable, reading from an LSM-tree is inherently asymmetric. For non-existent keys, Cassandra checks an in-memory Bloom filter requiring only 10 bits per key; a single 0-bit skips disk access in just 3.4 microseconds. However, when the key does exist, Bloom filters yield positive hits, forcing Cassandra to traverse the MemTable and multiple SSTable levels, decoding index blocks until the newest timestamp is found. Thus, positive point reads suffer higher read amplification in LSM than in a balanced B+ Tree."
- **Tiếng Việt (VI):** "Vì các SSTable là bất biến, luồng đọc trong cây LSM có tính chất bất đối xứng rõ rệt. Với khóa không tồn tại, Cassandra kiểm tra Bloom Filter trên RAM chỉ tốn 10 bit/khóa; chỉ cần một bit 0 là hủy tìm kiếm trong 3,4 micro-giây mà không cần đọc đĩa. Nhưng khi khóa có tồn tại, Bloom filter trả về dương tính, buộc hệ thống phải tra cứu qua MemTable và nhiều tầng SSTable, giải mã các khối chỉ mục để tìm bản ghi có timestamp mới nhất. Do đó, lượt đọc dương tính trong LSM chịu độ khuếch đại đọc lớn hơn cây B+."

---

### Slide 11: Cassandra Warning: 'ALLOW FILTERING' Anti-Pattern
**Section:** `02 LSM & Cassandra` | **Badge:** `Anti-Pattern`  
**Subtitle:** *Why Querying Non-Partition Keys Triggers Cluster-Wide Full Scans*  

#### Key Points:
- Cassandra's primary key design uses consistent hashing on the Partition Key to route queries directly to the responsible node.
- `ALLOW FILTERING` forces the coordinator to scatter-gather the query to every node in the cluster.
- Every node must execute a full linear scan of all its SSTables, causing severe latency spikes and query timeouts.

#### Verbatim Spoken Scripts:
- **English (EN):** "Because Cassandra executes partition key lookups in microseconds, developers often fall into a fatal anti-pattern: using ALLOW FILTERING. When you query by primary key, Cassandra hashes the key and routes directly to the single responsible node. But when you filter by a non-partition column with ALLOW FILTERING, the coordinator must broadcast the query to every node in the cluster, forcing each node to scan all its SSTables. This creates severe latency spikes and cluster outages under load."
- **Tiếng Việt (VI):** "Bởi vì Cassandra tra cứu theo khóa chính trong vài micro-giây, các kỹ sư thường mắc phải một sai lầm chết người: sử dụng ALLOW FILTERING. Khi truy vấn bằng khóa phân vùng, Cassandra băm khóa và định tuyến thẳng đến đúng một node chịu trách nhiệm. Nhưng khi lọc theo một cột không phải khóa phân vùng kèm ALLOW FILTERING, node điều phối buộc phải phát tán truy vấn tới mọi node trong cụm, ép từng node phải quét qua tất cả các file SSTable của mình. Điều này gây bùng nổ độ trễ và làm tê liệt hệ thống khi có tải."

---

### Slide 12: Search Paradigms: Linear Scan vs. Inverted Index
**Section:** `03 Inverted Index & ES` | **Badge:** `Search Paradigm`  
**Subtitle:** *From Exhausting Brute-Force (2,515.55 µs) to Direct Term Indexing (35.21 µs) — 71.5× Speedup*  

#### Key Points:
- Linear Scan ($O(N \cdot L)$): Must evaluate query string against every document sequentially; measured at $2,515.55 \pm 182.40\ \mu\text{s}$.
- Inverted Index ($O(1)$ term lookup): Inverts the relationship to map Terms $\to$ Sorted Document Posting Lists.
- Direct Postings Access: Retrieves matching document arrays in $35.21 \pm 14.91\ \mu\text{s}$, achieving a verified $71.5\times$ acceleration.

#### Verbatim Spoken Scripts:
- **English (EN):** "Searching text without an index is like reading a 500-page book cover-to-cover to find a single mention. In our benchmarks across 1,655 quotes, an unindexed linear scan took 2,515 microseconds. The Inverted Index inverts this relationship: like the alphabetical index at the back of a book, it maps each term directly to an array of document IDs. Queries jump directly to matches in just 35 microseconds—delivering a verified 71.5-fold empirical speedup."
- **Tiếng Việt (VI):** "Tìm kiếm văn bản không có chỉ mục giống như việc phải đọc từng trang một cuốn sách dày 500 trang để tìm một chữ. Trong thực nghiệm trên 1.655 danh ngôn, quét tuyến tính không chỉ mục tốn tới 2.515 micro-giây. Chỉ mục đảo (Inverted Index) đảo ngược mối quan hệ này: giống như mục lục tra cứu theo bảng chữ cái cuối cuốn sách, nó ánh xạ trực tiếp mỗi từ đến một danh sách mã tài liệu. Truy vấn nhảy thẳng tới kết quả chỉ trong 35 micro-giây — mang lại mức tăng tốc thực nghiệm 71,5 lần."

---

### Slide 13: Text Analysis & NRT Refresh: The Lucene Ingestion Pipeline
**Section:** `03 Inverted Index & ES` | **Badge:** `Analysis & NRT Refresh`  
**Subtitle:** *3-Stage Normalization Conveyor Belt and Bounded 1-Second Near-Real-Time (NRT) Refresh Lag*  

#### Key Points:
- Text Analysis Pipeline: Raw text passes through Character Filters, Tokenizers, and Token Filters (Porter stemming, lowercase).
- Symmetric Pipeline: Query strings must traverse the identical analysis pipeline to align with indexed tokens.
- Near-Real-Time (NRT) Mechanics: Documents are buffered in memory and appended to a translog; they are NOT immediately searchable.
- Bounded Refresh Lag: A scheduled refresh (default: 1.0 s) flushes memory into an immutable segment, creating a bounded commit lag.

#### Verbatim Spoken Scripts:
- **English (EN):** "How does raw text become searchable? Lucene runs strings through a 3-stage conveyor belt: Character Filters remove markup, Tokenizers split words, and Token Filters lowercase and stem terms to root forms. But crucially, indexed documents are not immediately searchable. They are buffered in memory and appended to a translog, becoming searchable only after a scheduled or explicit refresh—defaulting to 1 second. This bounded commit lag defines Elasticsearch's Near-Real-Time consistency, distinct from immediate read-your-writes databases."
- **Tiếng Việt (VI):** "Làm thế nào để văn bản tìm kiếm được? Lucene đưa chuỗi ký tự qua dây chuyền 3 bước: Bộ lọc ký tự gỡ thẻ HTML, Bộ tách từ chia từ đơn, và Bộ lọc từ chuyển chữ thường kèm rút gốc từ. Nhưng quan trọng hơn cả, tài liệu chưa thể tìm thấy ngay lập tức. Chúng được đệm trên RAM và ghi log vào translog, chỉ trở nên tìm kiếm được sau chu kỳ refresh định kỳ (mặc định 1 giây) để tạo ra segment mới. Độ trễ cam kết có hạn này tạo nên tính nhất quán Gần-Thời-Gian-Thực (NRT) của Elasticsearch, khác biệt với tính nhất quán đọc ngay của cơ sở dữ liệu khóa chính."

---

### Slide 14: Finding Multiple Words: Skip Pointers in Posting Lists
**Section:** `03 Inverted Index & ES` | **Badge:** `Fast Intersection`  
**Subtitle:** *Intersecting Sorted Document IDs with Express Highway Leaps (33.69 µs)*  

#### Key Points:
- Boolean AND queries require computing the intersection of multiple sorted posting lists: $P_1 \cap P_2$.
- Standard merge check is $O(|P_1| + |P_2|)$; Skip Pointers placed every $\sqrt{|P|}$ elements enable sub-linear leapfrogging.
- If pointer on List A is at Doc 60, List B skips directly over lower intervals without sequential evaluation.

#### Verbatim Spoken Scripts:
- **English (EN):** "When searching for multiple terms such as 'write AND search', Elasticsearch must intersect their sorted posting lists. Instead of checking every document ID sequentially, Lucene uses Skip Pointers—express lane bridges embedded every square-root-of-P entries. If list A points to Document 60, list B can leapfrog dozens of smaller IDs instantly. In our implementation, this sub-linear leapfrogging evaluates complex multi-term intersections in just 33.69 microseconds."
- **Tiếng Việt (VI):** "Khi tìm kiếm nhiều từ đồng thời như 'write AND search', Elasticsearch phải tìm phần giao của các danh sách posting đã sắp xếp. Thay vì kiểm tra từng mã tài liệu một cách tuần tự, Lucene chèn các con trỏ nhảy (Skip Pointers) theo chu kỳ căn bậc hai của P phần tử. Nếu danh sách A đang ở tài liệu 60, danh sách B có thể nhảy cóc qua hàng chục tài liệu nhỏ hơn ngay lập tức. Trong mã nguồn của nhóm, thuật toán nhảy dưới tuyến tính này xử lý phép giao nhiều từ chỉ trong 33,69 micro-giây."

---

### Slide 15: Okapi BM25: Principles & Mathematical Formulation
**Section:** `03 Inverted Index & ES` | **Badge:** `Relevance Ranking`  
**Subtitle:** *Probabilistic Scoring: IDF Weighting, k1=1.2 Term Saturation, and b=0.75 Length Normalization*  

#### Key Points:
- Okapi BM25 is the gold standard probabilistic relevance framework in modern search engines.
- Inverse Document Frequency (IDF): Penalizes common stopwords while heavily rewarding discriminative terms.
- Term Frequency Saturation ($k_1=1.2$): Enforces an asymptotic upper bound to prevent keyword stuffing.
- Document Length Normalization ($b=0.75$): Penalizes long verbose documents in favor of concise, targeted matches.

#### Verbatim Spoken Scripts:
- **English (EN):** "Finding matching documents is only half the battle; ranking the best match requires Okapi BM25. BM25 combines three principles: Inverse Document Frequency rewards rare terms, parameter k1 at 1.2 enforces term frequency saturation to prevent keyword stuffing, and parameter b at 0.75 penalizes verbose documents. In our implementation, this formula evaluates top-5 ranked quotes in 118 microseconds, separating high-relevance matches cleanly."
- **Tiếng Việt (VI):** "Tìm thấy tài liệu chỉ mới là một nửa chặng đường; xếp hạng tài liệu phù hợp nhất cần thuật toán Okapi BM25. BM25 kết hợp 3 nguyên tắc: IDF chấm điểm cao cho từ hiếm, tham số k1 bằng 1.2 tạo trần bão hòa tần suất từ để chống spam từ khóa, và tham số b bằng 0.75 phạt tài liệu quá dài. Trong cài đặt của nhóm, công thức này tính toán top 5 kết quả chỉ trong 118 micro-giây, tách biệt chính xác tài liệu liên quan nhất."

---

### Slide 16: The Cost of Fast Search: 15× Memory Amplification
**Section:** `03 Inverted Index & ES` | **Badge:** `The RUM Trade-Off`  
**Subtitle:** *Measuring RUM Space: 2,293 Bytes/Doc (ES) vs. 154 Bytes/Key (Cassandra)*  

#### Key Points:
- Empirical Memory Footprint: Cassandra consumes 153.7 Bytes/key vs. Elasticsearch consuming 2,292.8 Bytes/doc.
- Elasticsearch precomputes and maintains extensive in-memory auxiliary structures: term dictionaries, skip lists, document lengths.
- Confirms RUM Memory ($M$) trade-off: microsecond search latency requires paying a $15\times$ RAM overhead premium.

#### Verbatim Spoken Scripts:
- **English (EN):** "There is no free lunch in computer science. To achieve 35-microsecond boolean search, Elasticsearch pays an enormous price in memory. While Cassandra requires only 154 bytes per key in RAM for its Bloom filters and index fences, Elasticsearch consumes nearly 2,300 bytes per document to store posting lists and term dictionaries. That is a measured 14.9-to-1 memory ratio, providing concrete empirical proof of the RUM Conjecture."
- **Tiếng Việt (VI):** "Không có bữa trưa nào miễn phí trong khoa học máy tính. Để đạt được tốc độ tìm kiếm 35 micro-giây, Elasticsearch phải trả một cái giá khổng lồ về bộ nhớ. Trong khi Cassandra chỉ cần 154 byte cho mỗi khóa trên RAM cho Bloom Filter và con trỏ chỉ mục, Elasticsearch tiêu tốn gần 2.300 byte cho mỗi tài liệu để lưu trữ danh sách posting và từ điển thuật ngữ. Tỷ lệ chênh lệch bộ nhớ 14,9 lần này là minh chứng thực nghiệm sống động cho Giả thuyết RUM."

---

### Slide 17: Architectural Convergence: Lucene Segments as LSM-Trees
**Section:** `04 Synthesis` | **Badge:** `Master's Insight`  
**Subtitle:** *The Hidden Symmetry: Why Inverted Index Lifecycle Mirrors the LSM Storage Architecture*  

#### Key Points:
- Structural Convergence: Modifying sorted posting lists in-place is computationally prohibitive.
- Lucene solves this by implementing the exact same lifecycle as an LSM-Tree: In-Memory Buffer, Translog WAL, Immutable Segments, and Tiered Merge Compaction.
- Deletions in both engines are non-destructive (Tombstones vs .del bitsets) and purged only during background merging.
- Master's Insight: Elasticsearch and Cassandra do not belong to disjoint worlds; Elasticsearch is an LSM-Tree with an inverted index payload.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is the key architectural revelation of our Master's study: while Cassandra and Elasticsearch appear to be opposite paradigms, their internal storage engines converge on the exact same lifecycle. Inverted posting lists cannot be modified in-place without prohibitive sorting costs. Therefore, Lucene internally functions as an LSM-Tree: incoming documents buffer in memory with a translog, flush to immutable on-disk segments identical to SSTables, and merge in the background via TieredMergePolicy. Elasticsearch does not reject LSM; it implements an LSM-Tree whose payload is an inverted index."
- **Tiếng Việt (VI):** "Đây là phát hiện kiến trúc quan trọng nhất trong nghiên cứu cao học của nhóm: dù Cassandra và Elasticsearch có vẻ đối lập, bộ máy lưu trữ bên trong của chúng lại hội tụ về đúng một vòng đời. Danh sách posting không thể sửa đổi tại chỗ nếu không muốn tốn chi phí sắp xếp lại toàn bộ. Vì vậy, Lucene tổ chức hoạt động y hệt một cây LSM: dữ liệu ghi vào bộ đệm RAM kèm translog, xả định kỳ thành các segment bất biến tương đương SSTable, và hòa trộn ngầm ở chế độ nền qua TieredMergePolicy. Elasticsearch không hề phủ nhận LSM; nó chính là một cây LSM với phần tải trọng là chỉ mục đảo."

---

### Slide 18: Comparing Both Systems: The 5W1H Matrix
**Section:** `04 Synthesis` | **Badge:** `Comparison Matrix`  
**Subtitle:** *Direct Architectural Contrast Across Workloads, Data Layouts, and RUM Compromises*  

#### Key Points:
- What: Distributed wide-column store (Cassandra) vs. Distributed text search engine (Elasticsearch).
- Why: Maximize write throughput & primary-key reads vs. Maximize ad-hoc text search & ranked relevance.
- Where: System of Record for time-series & transactions vs. Read-optimized Search View.
- How: Append-only MemTable & SSTable compaction vs. Tokenization pipeline & posting list segment merging.

#### Verbatim Spoken Scripts:
- **English (EN):** "To synthesize both technologies, we apply the 5W1H framework. Cassandra's 'What' is a distributed wide-column store designed for high-throughput appends where queries always supply the partition key. Elasticsearch's 'What' is a distributed search engine designed for ad-hoc multi-term queries with relevance scoring. Cassandra is the secure bank vault; Elasticsearch is the searchable storefront display. Each excels only when applied to the workload it was physically designed to solve."
- **Tiếng Việt (VI):** "Để tổng hợp cả hai công nghệ, nhóm áp dụng khung phân tích 5W1H. Về bản chất, Cassandra là cơ sở dữ liệu dạng cột phân tán cho luồng ghi tốc độ cao với các truy vấn luôn có khóa phân vùng. Elasticsearch là công cụ tìm kiếm phân tán cho các truy vấn văn bản phức tạp với tính điểm liên quan. Cassandra đóng vai trò két sắt ngân hàng; Elasticsearch là cửa sổ trưng bày sản phẩm. Mỗi hệ thống chỉ phát huy tối đa sức mạnh khi được đặt đúng vào bài toán mà cấu trúc vật lý của nó hướng tới."

---

### Slide 19: The Trade-Off Space: RUM Conjecture
**Section:** `04 Synthesis` | **Badge:** `Physical Law`  
**Subtitle:** *Cassandra at (U, M) vs. Elasticsearch at (R) — Proof Neither Can Replace the Other*  

#### Key Points:
- Mathematical Proof of Specialization: The RUM trade-off space is Pareto-optimal.
- Cassandra cannot support microsecond arbitrary search without ballooning its memory and stalling writes.
- Elasticsearch cannot accept 50k+ continuous random writes without crippling its segment merge pipeline.

#### Verbatim Spoken Scripts:
- **English (EN):** "When we map both engines onto the RUM Conjecture triangle, their complementary nature becomes mathematically undeniable. Cassandra prioritizes Update and Memory overhead; Elasticsearch prioritizes Read latency. No engineer can break this law; choosing an engine is fundamentally choosing which corner of the trade-off space your application requires. Neither engine can replace the other without violating physical storage limits."
- **Tiếng Việt (VI):** "Khi đối chiếu cả hai hệ thống lên tam giác Giả thuyết RUM, tính chất bổ trợ lẫn nhau của chúng trở nên hiển nhiên về mặt toán học. Cassandra ưu tiên chi phí Ghi và Bộ nhớ; Elasticsearch ưu tiên độ trễ Đọc. Không một kỹ sư nào có thể phá vỡ quy luật này; việc chọn database thực chất là chọn góc đánh đổi phù hợp với bài toán của mình. Không hệ thống nào có thể thay thế hoàn toàn hệ thống kia mà không vi phạm các giới hạn vật lý."

---

### Slide 20: Experimental Setup & Research Questions
**Section:** `05 Experiments` | **Badge:** `Methodology & Qs`  
**Subtitle:** *Zero-Dependency Reference Engines Tested Across 10,000 Cities and 1,655 Quotes*  

#### Key Points:
- Clean-Room Methodology: Implemented reference engines in pure Python without external dependencies.
- Eliminates JVM garbage collection pauses, network latency jitter, and OS page cache distortions.
- Datasets: 10,000 World Cities (KV lookup) and 1,655 Historical Quotes (full-text multi-term search).
- Formulated 4 specific research hypotheses (Q1 through Q4) to evaluate against the RUM Conjecture.

#### Verbatim Spoken Scripts:
- **English (EN):** "To conduct rigorous scientific benchmarks, we implemented zero-dependency reference storage engines in pure Python. This eliminates network latency, operating system page cache noise, and JVM garbage collection artifacts. We evaluate both engines across two datasets: 10,000 world cities for key-value telemetry, and 1,655 historical quotes for full-text queries. We formulated four specific research questions to test write scalability, Bloom filter fast-fails, lexical search acceleration, and memory overhead."
- **Tiếng Việt (VI):** "Để thực hiện đo đạc khoa học và công bằng, nhóm đã tự cài đặt các bộ máy lưu trữ tham chiếu không phụ thuộc thư viện ngoài bằng Python thuần. Cách tiếp cận này loại bỏ hoàn toàn nhiễu từ bộ thu dọn rác JVM, độ trễ mạng và bộ đệm trang của hệ điều hành. Nhóm thử nghiệm trên hai bộ dữ liệu thực tế: 10.000 thành phố cho truy vấn khóa-giá trị, và 1.655 danh ngôn cho truy vấn tìm kiếm toàn văn. Bốn câu hỏi nghiên cứu được đặt ra để kiểm chứng tốc độ ghi, bộ lọc Bloom, độ tăng tốc tìm kiếm và tỷ lệ chiếm dụng bộ nhớ."

---

### Slide 21: Live Demonstration: Reproducible Pipeline
**Section:** `05 Experiments` | **Badge:** `Live Demo`  
**Subtitle:** *Single-Command End-to-End Execution via Terminal (demo.py) and Google Colab*  

#### Key Points:
- Fully reproducible artifact: executable locally via `python3 demo.py` or via interactive Google Colab notebook.
- Automated test suite with 25 unit tests asserting internal invariants (immutability, skip list leapfrogging, BM25 ordering).
- Live demonstration executes end-to-end benchmarking in under 60 seconds.

#### Verbatim Spoken Scripts:
- **English (EN):** "Our implementation is 100% reproducible. By running a single command, 'python3 demo.py --no-pause', examiners can verify every mechanism executing in real time: MemTable batching, immutable SSTable flushes, Bloom filter fast-fails in 3 microseconds, and multi-term BM25 ranking across real datasets. An accompanying unit test suite of 25 automated tests validates all internal invariants."
- **Tiếng Việt (VI):** "Mã nguồn của đồ án có tính tái lập 100%. Chỉ với một dòng lệnh 'python3 demo.py --no-pause', Hội đồng có thể kiểm chứng trực tiếp từng cơ chế đang chạy: MemTable nhận dữ liệu, xả file SSTable bất biến, Bloom Filter hủy tìm kiếm trong 3 micro-giây và thuật toán BM25 xếp hạng danh ngôn. Bộ kiểm thử tự động gồm 25 unit test đi kèm đảm bảo tính đúng đắn của mọi bất biến bên trong."

---

### Slide 22: Empirical Scorecard & Hypothesis Validation
**Section:** `06 Results` | **Badge:** `Scorecard & Proofs`  
**Subtitle:** *5-Round Statistical Benchmarks (µ ± σ) Confirming Hypotheses Q1 Through Q4*  

#### Key Points:
- Q1 Confirmed: Cassandra sustains 52,339 ops/s (bursting to 85,000 ops/s), validating append-only throughput.
- Q2 Confirmed: Bloom filters achieve 100% negative pruning in 3.42 µs, completely eliminating disk seeks on absent keys.
- Q3 Confirmed: Inverted index accelerates search by 71.5× (35.21 µs vs 2,515.55 µs scan); BM25 top-5 completes in 118.40 µs.
- Q4 Confirmed: Precomputing term posting lists requires 14.9× more memory (2,292.8 B/doc vs 153.7 B/key).

#### Verbatim Spoken Scripts:
- **English (EN):** "Our empirical scorecard across five statistical trials confirms all four research hypotheses. For Q1, Cassandra delivers over 52,000 writes per second sustained throughput, reaching 85,000 in burst. For Q2, Bloom filters achieve 100% pruning on absent keys in 3.4 to 6.2 microseconds with zero disk I/O. For Q3, inverted index boolean queries execute in 35 microseconds—a 71.5-fold speedup over linear scanning. For Q4, precomputing term dictionaries incurs an exact 14.9-fold memory overhead. The empirical data matches theoretical RUM boundaries."
- **Tiếng Việt (VI):** "Bảng điểm thực nghiệm qua 5 lần chạy lặp lại khẳng định cả 4 giả thuyết nghiên cứu. Với Q1, Cassandra đạt tốc độ ghi bền vững hơn 52.000 thao tác/giây, đạt đỉnh 85.000 thao tác/giây. Với Q2, Bloom Filter loại trừ 100% lượt đọc đĩa trên khóa không tồn tại chỉ trong 3,4 đến 6,2 micro-giây. Với Q3, truy vấn chỉ mục đảo hoàn tất trong 35 micro-giây — tăng tốc 71,5 lần so với quét tuyến tính. Với Q4, việc tính trước từ điển thuật ngữ tiêu tốn chính xác gấp 14,9 lần RAM. Số liệu thực nghiệm hoàn toàn khớp với biên lý thuyết của Giả thuyết RUM."

---

### Slide 23: Dual-Engine CQRS Architecture & Final Defense Verdict
**Section:** `07 Architecture & Conclusion` | **Badge:** `CQRS & Verdict`  
**Subtitle:** *Bank Vault (Cassandra) + Storefront Window (ES) via CDC/Kafka & 3 Golden Rules*  

#### Key Points:
- Anti-Pattern Warning: Never use application-level dual writes; network failures cause permanent split-brain data divergence.
- Production CQRS Synthesis: Cassandra acts as the immutable System of Record; Kafka CDC asynchronously updates Elasticsearch.
- Storage Convergence: Both engines utilize an LSM segment lifecycle, complementing each other under CQRS separation.
- Final Verdict: Neither engine can subsume the other; architectural excellence lies in combining their specialized physical layouts.

#### Verbatim Spoken Scripts:
- **English (EN):** "In production, never perform dual-writes from application code. Treat Cassandra as the Bank Vault—the durable System of Record accepting high-velocity writes. Treat Elasticsearch as the Storefront Display Window—a disposable, highly indexed search view. Use Change Data Capture via Kafka to asynchronously replicate log commits into search segments. In summary: no single database rules all workloads, but by combining LSM-Tree ingestion with Inverted Index retrieval under CQRS, modern data architectures achieve both maximum write throughput and microsecond search. Thank you, and we welcome your questions."
- **Tiếng Việt (VI):** "Trong thực tế, tuyệt đối không ghi đồng thời hai bên từ mã nguồn ứng dụng. Hãy coi Cassandra là Két Sắt Ngân Hàng — nguồn chân lý tin cậy đón nhận luồng ghi tải cao. Hãy coi Elasticsearch là Cửa Sổ Trưng Bày — khung nhìn tìm kiếm đa năng có thể tái tạo bất kỳ lúc nào. Sử dụng Change Data Capture qua Kafka để đồng bộ bất đồng bộ các commit log sang chỉ mục tìm kiếm. Tóm lại: không cơ sở dữ liệu nào giải quyết được mọi bài toán, nhưng bằng cách phối hợp khả năng ghi của LSM với khả năng tìm kiếm của Chỉ mục đảo qua mô hình CQRS, hệ thống sẽ đạt được cả thông lượng ghi tối đa lẫn tốc độ tìm kiếm micro-giây. Xin chân thành cảm ơn Thầy Cô và nhóm sẵn sàng lắng nghe câu hỏi."

---
