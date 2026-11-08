# CO5173 — Storage Engine Duality: Cassandra (LSM) vs Elasticsearch (Inverted Index)
## Complete 29-Slide Presentation Content & Bilingual Speaker Transcripts

> **Presentation Pacing:** 29 bite-sized visual slides designed for a 15-minute presentation (~30 seconds per slide).
> **Bilingual Delivery:** Full scripts provided in both English (EN) and Vietnamese (VI).

---

### Slide 01: Storage Engine Duality
**Section:** `00 Introduction` | **Badge:** `Cover Slide`  
**Subtitle:** *Apache Cassandra (LSM-Tree) vs. Elasticsearch (Inverted Index) — A Comparative Study*  

#### Key Points:
- Final Project for CO5173 Advanced Data Engineering, HCMUT Master of Computer Science.
- Compares two opposite storage designs: write-optimized LSM-Trees vs search-optimized Inverted Indexes.
- Demonstrates why modern systems need both engines using clear analogies and empirical proofs.

#### Verbatim Spoken Scripts:
- **English (EN):** "Good day, professors and fellow students. Welcome to our presentation for CO5173 Advanced Data Engineering. Today, we explore the storage engine duality between Apache Cassandra and Elasticsearch. In modern data systems, no single database can do everything well. Over the next 15 minutes, we will explain why traditional databases struggle at scale, how Cassandra and Elasticsearch solve these problems with opposite designs, and show live benchmark proof from our code."
- **Tiếng Việt (VI):** "Kính chào quý Thầy Cô và các bạn học viên cao học. Chào mừng quý vị đến với buổi báo cáo đồ án môn CO5173 Kỹ nghệ Dữ liệu Nâng cao. Hôm nay, chúng em xin trình bày về tính nhị nguyên giữa Apache Cassandra và Elasticsearch. Trong hệ thống dữ liệu lớn, không một cơ sở dữ liệu nào hoàn hảo cho mọi tác vụ. Trong 15 phút tới, chúng ta sẽ cùng tìm hiểu vì sao database truyền thống gặp giới hạn, cách Cassandra và Elasticsearch giải quyết qua hai thiết kế đối lập, và chứng minh bằng số liệu thực nghiệm."

---

### Slide 02: Presentation Roadmap: The 4 Acts
**Section:** `00 Introduction` | **Badge:** `Roadmap`  
**Subtitle:** *A Guided 15-Minute Tour Through Storage Mechanics & Empirical Evidence*  

#### Key Points:
- Calibrated strictly for a 15-minute presentation (~30 seconds per slide).
- Follows a logical story arc: The Crisis -> Solution 1 (Cassandra) -> Solution 2 (Elasticsearch) -> Synthesis.
- Every theoretical concept is paired with an intuitive real-world analogy and runnable code.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is our 15-minute roadmap organized into four clear acts. In Act 1, we look at the storage crisis: why traditional databases struggle with heavy writes and text searches. In Act 2, we explain Cassandra and LSM trees through our desk notepad analogy. In Act 3, we explain Elasticsearch and Inverted Indexes using the book index analogy. Finally, in Act 4, we examine our empirical benchmark results and show how to combine both systems in production using the CQRS pattern."
- **Tiếng Việt (VI):** "Đây là lộ trình 15 phút của nhóm qua 4 phần rõ ràng. Trong Phần 1, ta tìm hiểu cuộc khủng hoảng lưu trữ khi database truyền thống gặp tải ghi cao và tìm kiếm từ ngữ. Trong Phần 2, ta khám phá Cassandra và LSM-Tree qua hình ảnh cuốn sổ tay. Trong Phần 3, ta phân tích Elasticsearch và Chỉ mục đảo qua hình ảnh mục lục tra cứu cuối sách. Cuối cùng, trong Phần 4, ta đối chiếu các kết quả đo đạc thực nghiệm và cách phối hợp cả hai trong thực tế bằng mô hình CQRS."

---

### Slide 03: Traditional Databases: The Overwrite Trap
**Section:** `01 Storage Crisis` | **Badge:** `Problem 1`  
**Subtitle:** *How Changing a 50-Byte Record Forces a 16,384-Byte Disk Rewrite*  

#### Key Points:
- Traditional databases use B+ Trees that store data in fixed-size blocks called pages (typically 16 KB).
- Updating even one small field requires rewriting the entire 16 KB page, causing ~327× write amplification.
- This in-place update design creates random disk jumping and caps write ingestion throughput.

#### Verbatim Spoken Scripts:
- **English (EN):** "To understand why Cassandra was invented, we first look at the overwrite trap in traditional relational databases like MySQL or PostgreSQL. These systems organize data into fixed 16-kilobyte pages using B+ Trees. When you update a 50-byte user status, the database cannot write just 50 bytes. It must rewrite all 16,384 bytes back to disk. That is a 327-fold write amplification, creating random disk jumping and choking write performance."
- **Tiếng Việt (VI):** "Để hiểu vì sao Cassandra ra đời, trước hết ta nhìn vào cái bẫy ghi đè của các database truyền thống như MySQL hay PostgreSQL. Chúng tổ chức dữ liệu theo các trang cố định 16 KB qua cấu trúc B+ Tree. Khi bạn sửa một dòng trạng thái 50 byte, hệ quản trị không thể chỉ ghi 50 byte, mà buộc phải ghi lại toàn bộ 16.384 byte xuống đĩa. Hệ số khuếch đại ghi gấp 327 lần này sinh ra nhảy đĩa ngẫu nhiên và làm nghẽn luồng ghi."

---

### Slide 04: Traditional Databases: The Full-Scan Trap
**Section:** `01 Storage Crisis` | **Badge:** `Problem 2`  
**Subtitle:** *Why Searching for Words Using Wildcards Bypasses Normal Indexes*  

#### Key Points:
- B+ Tree indexes only work for exact matches or prefix searches; leading wildcards bypass them entirely.
- Forces a full table scan across millions of disk rows, consuming massive CPU and I/O bandwidth.
- Relational databases cannot calculate relevance scores to rank which documents are the best answers.

#### Verbatim Spoken Scripts:
- **English (EN):** "The second major limit of traditional databases is text search. If you query with a wildcard like WHERE text LIKE '%database%', the leading percentage sign bypasses the B+ Tree index completely. The database is forced to perform a full table scan, reading every row from disk. This is slow, wastes system resources, and cannot rank which document is the most relevant answer."
- **Tiếng Việt (VI):** "Giới hạn lớn thứ hai của database truyền thống là tìm kiếm văn bản. Khi bạn tìm kiếm với ký tự đại diện như LIKE '%database%', dấu phần trăm đứng đầu làm cây B+ mất tác dụng. Hệ thống buộc phải quét toàn bộ bảng, đọc từng dòng trên đĩa. Cách này rất chậm, lãng phí tài nguyên và hoàn toàn không thể xếp hạng xem tài liệu nào là câu trả lời tốt nhất."

---

### Slide 05: The Writer vs. Reader Conflict
**Section:** `01 Storage Crisis` | **Badge:** `The Conflict`  
**Subtitle:** *Why One Storage Engine Cannot Be the Fastest at Both Writing and Searching*  

#### Key Points:
- Writing at maximum speed requires minimal upfront work: simply appending sequential bytes.
- Searching in microseconds requires heavy upfront work: tokenizing words and pre-building sorted catalogs.
- Trying to perform both tasks on a single storage layout forces both operations to slow down.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is the fundamental conflict in database design. To write at maximum hardware speed, you must do almost zero work when saving data: just append bytes sequentially. But to search across millions of documents in microseconds, you must dissect every word upfront into sorted lists. Doing both on the same storage structure is physically impossible."
- **Tiếng Việt (VI):** "Đây là mâu thuẫn cốt lõi trong thiết kế cơ sở dữ liệu. Muốn ghi ở tốc độ phần cứng tối đa, bạn phải làm ít việc nhất lúc ghi: chỉ ghi nối đuôi tuần tự. Nhưng muốn tìm kiếm triệu tài liệu trong vài micro-giây, bạn phải bóc tách từng từ ngữ thành các danh sách sắp xếp sẵn. Làm cả hai trên cùng một cấu trúc lưu trữ là điều bất khả thi về mặt vật lý."

---

### Slide 06: The Storage Law: The RUM Conjecture
**Section:** `01 Storage Crisis` | **Badge:** `Storage Law`  
**Subtitle:** *You Can Only Optimize Two: Read (R), Update (U), or Memory (M)*  

#### Key Points:
- The RUM Conjecture (Harvard/BU) proves that minimizing two database costs inevitably worsens the third cost.
- Cassandra prioritizes low update work and low memory usage, deferring sorting to background threads.
- Elasticsearch prioritizes instant search speed, pre-building rich catalogs at the cost of high memory.

#### Verbatim Spoken Scripts:
- **English (EN):** "This physical limit was proven by researchers at Harvard and Boston University as the RUM Conjecture. You can optimize at most two corners of the triangle: Read overhead, Update overhead, or Memory overhead. Cassandra minimizes Update and Memory costs, while Elasticsearch minimizes Read overhead at the expense of high memory consumption."
- **Tiếng Việt (VI):** "Giới hạn vật lý này được chứng minh qua Giả thuyết RUM bởi các nhà nghiên cứu Đại học Harvard và Boston. Bạn chỉ có thể tối ưu tối đa hai trong ba góc của tam giác: Chi phí Đọc (R), Chi phí Ghi (U), hoặc Bộ nhớ RAM (M). Cassandra tối ưu Ghi và Bộ nhớ, trong khi Elasticsearch tối ưu tốc độ Đọc và chấp nhận tiêu tốn nhiều dung lượng RAM."

---

### Slide 07: LSM Analogy: The Desk Notepad
**Section:** `02 LSM & Cassandra` | **Badge:** `Analogy Step 1`  
**Subtitle:** *Step 1: Saving Writes into Fast RAM Without Touching Slow Disk*  

#### Key Points:
- When a write arrives, Cassandra never updates data on disk immediately.
- It writes to an active, sorted in-memory buffer called the MemTable.
- For crash protection, it appends a record sequentially to the on-disk CommitLog.

#### Verbatim Spoken Scripts:
- **English (EN):** "Imagine working at a busy library intake desk. When new books arrive, you don't run to the shelves to insert them one by one. You simply jot the titles down on your desk notepad. In Cassandra, this notepad is the MemTable in RAM. For crash safety, an assistant logs the title sequentially into an append-only commit log on disk. The write returns instantly in microseconds."
- **Tiếng Việt (VI):** "Hãy tưởng tượng bạn là thủ thư ở một thư viện đông đúc. Khi sách mới trả về, bạn không chạy đi tìm từng kệ để nhét vào. Bạn chỉ ghi nhanh tiêu đề vào cuốn sổ tay trên bàn làm việc. Trong Cassandra, cuốn sổ tay này chính là MemTable trên RAM. Để phòng sự cố mất điện, hệ thống ghi nối đuôi một dòng vào CommitLog trên đĩa. Giao dịch hoàn tất lập tức trong vài phần triệu giây."

---

### Slide 08: LSM Analogy: Staple & Shelf
**Section:** `02 LSM & Cassandra` | **Badge:** `Analogy Step 2`  
**Subtitle:** *Step 2: Freezing the Filled Notepad into an Immutable Disk File*  

#### Key Points:
- When the MemTable fills up, it is frozen and written to disk as a sorted file called an SSTable.
- Writing an SSTable to disk is 100% sequential, maximizing hardware disk write bandwidth.
- SSTables are immutable (read-only); they are never edited or overwritten in place.

#### Verbatim Spoken Scripts:
- **English (EN):** "When your desk notepad is full, you don't erase it. You tear out the page, staple it into a neat sorted booklet, and place it on the library shelf. In Cassandra, this is an SSTable. Because SSTables are immutable, multiple threads can read them without any locking contention, and writing them to disk is a pure sequential stream at maximum disk bandwidth."
- **Tiếng Việt (VI):** "Khi cuốn sổ tay trên bàn đã đầy, bạn không xóa đi mà xé trang, bấm lại thành một tập sách mỏng đã xếp thứ tự rồi đặt lên kệ. Trong Cassandra, đó là SSTable. Vì SSTable là bất biến (immutable), nhiều luồng có thể đọc đồng thời mà không sợ tranh chấp khóa, và việc ghi xuống đĩa diễn ra hoàn toàn tuần tự với tốc độ tối đa của phần cứng."

---

### Slide 09: LSM Analogy: Background Compaction
**Section:** `02 LSM & Cassandra` | **Badge:** `Analogy Step 3`  
**Subtitle:** *Step 3: Merging Multiple Disk Files and Permanently Erasing Deleted Data*  

#### Key Points:
- Deletions in Cassandra are inserts of a special Tombstone marker (no in-place file modifications).
- Over time, multiple SSTables accumulate on disk; background compaction merges them cleanly.
- Compaction reclaims disk space by purging superseded values and tombstones.

#### Verbatim Spoken Scripts:
- **English (EN):** "As days go by, your library shelf accumulates dozens of booklets with obsolete notes and cross-outs. An assistant works in the background, reading multiple sorted booklets at once, taking the newest entry for each book, and copying them into a single clean volume. In Cassandra, this is Compaction. Deletions are handled by writing Tombstones, which compaction permanently purges."
- **Tiếng Việt (VI):** "Theo thời gian, trên kệ tích tụ hàng chục tập sách mỏng chứa cả những ghi chú cũ và các dòng bị gạch xóa. Một người trợ lý sẽ làm việc ngầm: đọc đồng thời các tập sách đã xếp thứ tự, giữ lại bản ghi mới nhất và chép vào một cuốn sách lớn duy nhất. Trong Cassandra, đó là quá trình Compaction. Việc xóa dữ liệu được thực hiện bằng cách ghi một thẻ Tombstone, và Compaction sẽ tiêu hủy vĩnh viễn thẻ này."

---

### Slide 10: Storage Physics: Why Sequential Writing Wins
**Section:** `02 LSM & Cassandra` | **Badge:** `Hardware Physics`  
**Subtitle:** *Writing in a Straight Line is 50× to 100× Faster Than Jumping Across Disk Sectors*  

#### Key Points:
- Storage hardware (both SSDs and HDDs) writes sequential streams much faster than random seeks.
- Cassandra translates every client mutation into a smooth sequential write.
- This mechanical advantage delivers over 85,000 writes/sec in our benchmark tests.

#### Verbatim Spoken Scripts:
- **English (EN):** "The secret behind Cassandra's legendary write performance is not complex code; it is hardware physics. Disk drives, whether spinning hard drives or NVMe SSDs, write sequential streams 50 to 100 times faster than random seeks. By strictly buffering in RAM and flushing sequentially to disk, Cassandra achieves over 85,000 writes per second on commodity hardware."
- **Tiếng Việt (VI):** "Bí quyết đằng sau hiệu năng ghi huyền thoại của Cassandra không nằm ở thuật toán phức tạp mà bắt nguồn từ vật lý phần cứng. Mọi ổ đĩa, từ đĩa từ quay đến SSD NVMe, đều ghi dữ liệu tuần tự nhanh gấp 50 đến 100 lần so với tìm kiếm ngẫu nhiên. Bằng cách gom trên RAM và chỉ ghi nối đuôi tuần tự xuống đĩa, Cassandra dễ dàng đạt trên 85.000 lượt ghi mỗi giây trên phần cứng phổ thông."

---

### Slide 11: Cassandra's Helper: The Bloom Filter in RAM
**Section:** `02 LSM & Cassandra` | **Badge:** `Fast RAM Check`  
**Subtitle:** *How to Check 20 Disk Files in Nanoseconds Without Doing 20 Slow Disk Reads*  

#### Key Points:
- Because SSTables are immutable, an item could be in any of the SSTable files on disk.
- Reading without an index would mean opening and searching every SSTable file on disk.
- Cassandra pairs every SSTable with a compact Bloom Filter in RAM to check key presence in nanoseconds.

#### Verbatim Spoken Scripts:
- **English (EN):** "There is a catch to LSM-Trees: reading can be slow because data is scattered across multiple SSTable files on disk. If you have 20 SSTables, do you have to do 20 disk seeks? No! Cassandra's secret weapon is the Bloom Filter. Each SSTable has an in-memory bit array requiring only about 10 bits per key. It tests key presence in nanoseconds before touching disk."
- **Tiếng Việt (VI):** "Cấu trúc LSM-Tree có một điểm yếu: đọc có thể bị chậm vì dữ liệu phân tán ở nhiều file SSTable trên đĩa. Nếu có 20 SSTable, chẳng lẽ phải tìm kiếm đĩa 20 lần? Hoàn toàn không! Vũ khí bí mật của Cassandra là Bloom Filter. Mỗi SSTable có một mảng bit nằm sẵn trên RAM, chỉ tốn khoảng 10 bit cho mỗi khóa. Nó kiểm tra sự tồn tại trong vài nano giây trước khi chạm vào đĩa."

---

### Slide 12: Bloom Filter Fast-Fail Mechanics
**Section:** `02 LSM & Cassandra` | **Badge:** `Fast-Fail Mechanics`  
**Subtitle:** *How a Single '0' Bit Skips Slow Disk Access Entirely in 3.42 Microseconds*  

#### Key Points:
- If any single hash bit evaluates to 0, the key is mathematically guaranteed not to exist in that file.
- Cassandra immediately aborts searching that SSTable without touching physical disk.
- Our live benchmark proves absent lookups take just 3.42 µs—faster than a hit!

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is the exact mathematics of why Bloom filters are so powerful. When a key is inserted, three hash functions flip three bits to 1. To check if an absent key like 999 exists, we compute the same three hashes. If even a single bit is 0, it is mathematically impossible for that key to be in the SSTable. Cassandra immediately fast-fails in 3.4 microseconds, completely bypassing disk I/O."
- **Tiếng Việt (VI):** "Đây là toán học chính xác giải thích sức mạnh của Bloom Filter. Khi nạp một khóa, ba hàm băm sẽ bật ba bit tương ứng lên 1. Để kiểm tra một khóa không tồn tại như 999, ta tính lại ba vị trí bit đó. Chỉ cần một bit mang giá trị 0, ta khẳng định chắc chắn 100% khóa đó không hề nằm trong SSTable. Cassandra lập tức dừng lại trong 3,4 micro-giây mà không hề tốn một lượt đọc đĩa nào."

---

### Slide 13: Cassandra Warning: 'ALLOW FILTERING' Danger
**Section:** `02 LSM & Cassandra` | **Badge:** `Anti-Pattern`  
**Subtitle:** *Why Querying Non-Partition Keys Can Bring Down a Production Cluster*  

#### Key Points:
- Cassandra is designed strictly for Partition Key queries via consistent hashing.
- Using `ALLOW FILTERING` on non-partition keys forces every node across the cluster to perform full table scans.
- If you need arbitrary filtering across fields, Cassandra is the wrong tool—you need Elasticsearch.

#### Verbatim Spoken Scripts:
- **English (EN):** "Because Cassandra is so fast at key lookups, developers often fall into a deadly trap: using ALLOW FILTERING. When you query by primary key, Cassandra routes to exactly one node. But when you filter by a non-key column like email with ALLOW FILTERING, the cluster broadcasts to every single node, forcing every node to scan all its SSTables. This causes cluster-wide latency spikes and timeouts."
- **Tiếng Việt (VI):** "Vì Cassandra đọc khóa chính rất nhanh nên các lập trình viên thường mắc phải một sai lầm chết người: lạm dụng ALLOW FILTERING. Khi truy vấn theo khóa chính, hệ thống định tuyến chính xác tới 1 nút. Nhưng khi lọc theo cột phụ như email bằng ALLOW FILTERING, điều phối viên buộc phải phát tán truy vấn tới mọi nút trong cụm, ép tất cả quét toàn bộ SSTable. Hậu quả là nghẽn CPU và sập cụm diện rộng."

---

### Slide 14: Textbook Analogy: Searching Without an Index
**Section:** `03 Inverted Index & ES` | **Badge:** `Analogy Step 1`  
**Subtitle:** *Step 1: Reading Every Single Word to Find One Topic — The Exhausting Linear Scan*  

#### Key Points:
- Without an index, finding a word requires reading through every page from start to finish.
- Our benchmark shows a linear scan takes 3,080 µs across just 1,655 short quotes.
- As document collections grow to millions of records, linear scanning becomes completely unusable.

#### Verbatim Spoken Scripts:
- **English (EN):** "Now let us turn to search. Imagine you are handed a 500-page computer science textbook and asked to find every page mentioning 'database'. If the book has no index, you have to read page 1, page 2, all the way to page 500. In computer science, this is a Linear Scan. In our benchmarks, scanning just 1,655 quotes took over 3,000 microseconds, and it gets exponentially worse as data grows."
- **Tiếng Việt (VI):** "Bây giờ chúng ta chuyển sang bài toán tìm kiếm. Hãy tưởng tượng bạn cầm một cuốn giáo trình 500 trang và cần tìm xem từ 'database' xuất hiện ở những trang nào. Nếu sách không có mục lục, bạn buộc phải đọc từ trang 1 đến trang 500. Trong khoa học máy tính, đó là Quét tuyến tính (Linear Scan). Trong thực nghiệm của nhóm, quét chỉ 1.655 câu danh ngôn đã tốn hơn 3.000 micro-giây, và thời gian sẽ tăng vọt khi dữ liệu lớn lên."

---

### Slide 15: Textbook Analogy: The Book Index Solution
**Section:** `03 Inverted Index & ES` | **Badge:** `Analogy Step 2`  
**Subtitle:** *Step 2: How Flipping to the Back-of-the-Book Speeds Up Search by 280×*  

#### Key Points:
- Human readers flip to the index at the back of the book where terms are sorted alphabetically.
- An Inverted Index maps each word directly to the exact page or document numbers where it appears.
- Our benchmark confirms search time drops from 3,080 µs down to 11 µs—a 280× speedup.

#### Verbatim Spoken Scripts:
- **English (EN):** "What does a human reader actually do? You flip to the index at the back of the book. Under letter 'D', you see 'database: pages 14, 45, 102'. You immediately turn to page 14 without ever looking at the other 490 pages. This is the Inverted Index. Instead of mapping Document to Words, it inverts the relationship to map Words to Documents. In our benchmark, this yields a 280-fold speedup."
- **Tiếng Việt (VI):** "Người đọc thực tế sẽ làm gì? Bạn lật ngay ra phần mục lục tra cứu ở cuối sách. Dưới mục chữ 'D', bạn thấy 'database: trang 14, 45, 102'. Bạn mở ngay trang 14 mà không cần đụng tới 490 trang còn lại. Đó chính là Chỉ mục đảo (Inverted Index). Thay vì lưu Tài liệu trỏ đến Từ ngữ, nó đảo ngược lại: Từ ngữ trỏ đến Danh sách mã tài liệu. Trong thực nghiệm, điều này giúp tăng tốc 280 lần."

---

### Slide 16: Text Analysis: The Word Cleanup Factory
**Section:** `03 Inverted Index & ES` | **Badge:** `Word Cleanup`  
**Subtitle:** *Step 3: How Elasticsearch Transforms Raw Text into Searchable Tokens*  

#### Key Points:
- Before words enter the index, they pass through a 3-stage analysis pipeline.
- Character Filter removes markup; Tokenizer splits words; Token Filter lowercases and trims word suffixes (stemming).
- Because search queries undergo identical processing, searches match root meanings regardless of plurals or casing.

#### Verbatim Spoken Scripts:
- **English (EN):** "How does raw text become an index? Lucene runs every string through an analysis conveyor belt. First, Character Filters strip HTML tags. Second, the Tokenizer splits text on spaces and punctuation into word tokens. Third, Token Filters convert everything to lowercase and apply Porter Stemming, turning 'Databases' into its root 'databas'. Queries undergo the exact same pipeline."
- **Tiếng Việt (VI):** "Làm thế nào để văn bản thô biến thành chỉ mục? Lucene đưa chuỗi ký tự qua một dây chuyền phân tích 3 công đoạn. Bước 1, Bộ lọc ký tự loại bỏ các thẻ HTML. Bước 2, Bộ tách từ chia câu thành các từ đơn dựa theo dấu cách và dấu câu. Bước 3, Bộ lọc từ chuyển về chữ thường và rút gọn gốc từ bằng thuật toán Stemming, biến 'Databases' thành 'databas'. Truy vấn của người dùng cũng đi qua đúng dây chuyền này."

---

### Slide 17: Finding Multiple Words: Skip Pointers
**Section:** `03 Inverted Index & ES` | **Badge:** `Fast Intersection`  
**Subtitle:** *Step 4: Intersecting Multi-Term Boolean Queries Without Reading Every Document*  

#### Key Points:
- For multi-word AND queries, Elasticsearch intersects sorted arrays of document IDs.
- Skip pointers embed express highway shortcuts ahead in the posting list.
- If one list is at Doc 60, it leaps over dozens of intermediate IDs on the second list in <em>O</em>(1) time.

#### Verbatim Spoken Scripts:
- **English (EN):** "What happens when you search for 'write AND search'? Lucene retrieves the sorted posting lists for both words. Instead of checking every document ID one by one, Lucene uses Skip Pointers—express lane bridges embedded in the posting list. If list A is at Doc 60, list B can leapfrog past 50 documents instantly. This brings intersection time down to 13 microseconds."
- **Tiếng Việt (VI):** "Điều gì xảy ra khi bạn tìm kiếm 'write AND search'? Lucene lấy ra hai danh sách mã tài liệu đã được sắp xếp tăng dần. Thay vì so khớp từng phần tử, Lucene sử dụng Skip Pointer — như các cây cầu vượt cao tốc trong danh sách. Nếu danh sách A đang ở Tài liệu 60, danh sách B có thể nhảy cóc qua 50 tài liệu trung gian chỉ trong 1 bước nhảy. Nhờ đó phép giao hoàn thành trong 13 micro-giây."

---

### Slide 18: Okapi BM25: The 3 Rules of Relevance
**Section:** `03 Inverted Index & ES` | **Badge:** `Relevance Ranking`  
**Subtitle:** *Step 5: How Elasticsearch Knows Which Document is Actually the Best Match*  

#### Key Points:
- Okapi BM25 is the probabilistic ranking formula powering modern Elasticsearch and Lucene.
- Rule 1 (IDF): Penalizes common words, rewards rare terms.
- Rule 2 (TF Saturation): Prevents keyword spamming; Rule 3 (Length Penalty): Normalizes document length.

#### Verbatim Spoken Scripts:
- **English (EN):** "Finding matching documents is only half the battle; which document should be at the top? Elasticsearch uses Okapi BM25, governed by three intuitive rules. Rule 1: Rare words win—if you search 'the database', 'database' gets all the points. Rule 2: Anti-spam ceiling—mentioning a word 50 times does not give 50 times the score; it tops out. Rule 3: Short and punchy—a match in a short headline scores higher than in a giant document."
- **Tiếng Việt (VI):** "Tìm thấy tài liệu chỉ mới là một nửa chặng đường; tài liệu nào xứng đáng đứng đầu? Elasticsearch sử dụng thuật toán Okapi BM25 với 3 nguyên tắc trực quan. Nguyên tắc 1: Từ hiếm có giá trị cao — từ phổ biến như 'the' nhận 0 điểm, từ chuyên biệt như 'database' nhận trọn điểm số. Nguyên tắc 2: Chống gian lận từ khóa — lặp lại 50 lần không mang lại 50 lần điểm mà bị chặn trên bởi tiệm cận. Nguyên tắc 3: Ngắn gọn được ưu tiên — từ khóa xuất hiện trong tiêu đề ngắn được đánh giá cao hơn nằm lẫn trong một cuốn sách dày."

---

### Slide 19: Okapi BM25: The Math Made Simple
**Section:** `03 Inverted Index & ES` | **Badge:** `Formula Decoded`  
**Subtitle:** *Step 6: Understanding the Mathematical Formula Behind Relevance Scoring*  

#### Key Points:
- The BM25 formula calculates a continuous relevance score for ranking query results.
- Parameter <em>k</em><sub>1</sub> = 1.2 prevents keyword stuffing by placing an asymptotic ceiling on frequency.
- Parameter <em>b</em> = 0.75 balances document length against average corpus length.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is the exact mathematical equation of Okapi BM25. It sums the Inverse Document Frequency of each query term multiplied by a bounded term frequency curve. The parameter k1 set to 1.2 controls the saturation ceiling, and parameter b set to 0.75 controls the length penalty. In our live demo, this ranks the most relevant database quote at 1.92, cleanly separating it from lower-quality matches."
- **Tiếng Việt (VI):** "Đây là công thức toán học chính xác của Okapi BM25. Điểm số là tổng nghịch đảo tần suất tài liệu (IDF) của từng từ nhân với đường cong bão hòa tần suất xuất hiện. Tham số k1 bằng 1.2 kiểm soát trần bão hòa chống spam, và tham số b bằng 0.75 kiểm soát mức độ phạt độ dài văn bản. Trong demo trực tiếp, công thức này chấm cho câu trích dẫn chuẩn nhất 1.92 điểm, tách biệt hoàn toàn khỏi các kết quả mờ nhạt khác."

---

### Slide 20: The Cost of Fast Search: 15× Memory Penalty
**Section:** `03 Inverted Index & ES` | **Badge:** `The Hidden Cost`  
**Subtitle:** *Step 7: The RUM Trade-Off — Paying with High RAM to Achieve Microsecond Search*  

#### Key Points:
- An Inverted Index stores every unique word in a document, multiplying index memory overhead.
- Our empirical measurements show Elasticsearch requires 2,293 bytes/doc vs Cassandra's 154 bytes/key.
- This 15× memory amplification is the physical trade-off demanded by the RUM Conjecture.

#### Verbatim Spoken Scripts:
- **English (EN):** "There is no free lunch in computer science. To achieve 11-microsecond search times, Elasticsearch pays an enormous price in memory. While Cassandra needs only 154 bytes per key in RAM, Elasticsearch requires nearly 2,300 bytes per document to store posting lists and term dictionaries. That is a 15-to-1 memory ratio, perfectly illustrating the RUM Conjecture."
- **Tiếng Việt (VI):** "Không có bữa trưa nào miễn phí trong khoa học máy tính. Để đạt được tốc độ tìm kiếm 11 micro-giây, Elasticsearch phải trả giá đắt bằng dung lượng RAM. Trong khi Cassandra chỉ tốn 154 byte cho mỗi khóa trên RAM, Elasticsearch cần tới gần 2.300 byte cho mỗi tài liệu để duy trì danh sách posting và từ điển thuật ngữ. Tỷ lệ chênh lệch bộ nhớ 15 lần này là minh chứng hoàn hảo cho Giả thuyết RUM."

---

### Slide 21: Comparing Both Systems: The 5W1H Matrix
**Section:** `04 Synthesis` | **Badge:** `Comparison Matrix`  
**Subtitle:** *A Plain-English Breakdown Across 6 Key Architectural Questions*  

#### Key Points:
- The 5W1H framework clearly organizes the contrasting design goals of both technologies.
- Cassandra acts as the primary System of Record for high-speed write workloads.
- Elasticsearch acts as a secondary search accelerator for rich query filters.

#### Verbatim Spoken Scripts:
- **English (EN):** "To synthesize both technologies, we apply the 5W1H framework. Cassandra's 'What' is a distributed wide-column store for high-throughput appends where queries always provide the partition key. Elasticsearch's 'What' is a distributed search engine for ad-hoc multi-term queries with relevance scoring. Cassandra is the secure bank vault; Elasticsearch is the searchable storefront display."
- **Tiếng Việt (VI):** "Để tổng hợp hai công nghệ, chúng em áp dụng khung phân tích 5W1H. 'Cái gì' của Cassandra là cơ sở dữ liệu phân tán tối ưu cho luồng ghi cực lớn với điều kiện truy vấn luôn có khóa phân vùng. 'Cái gì' của Elasticsearch là bộ máy tìm kiếm phục vụ các truy vấn đa trường bất kỳ kèm xếp hạng điểm liên quan. Cassandra đóng vai trò két sắt lưu trữ dữ liệu gốc; Elasticsearch là gian hàng trưng bày cho khách tìm kiếm."

---

### Slide 22: The Trade-Off Space: RUM Conjecture
**Section:** `04 Synthesis` | **Badge:** `Physical Law`  
**Subtitle:** *Why Neither Engine Can Replace the Other (Opposite Design Choices)*  

#### Key Points:
- Cassandra occupies the Update-Memory corner of RUM space.
- Elasticsearch occupies the Read-optimization corner of RUM space.
- The RUM Conjecture mathematically proves that neither engine can replace the other.

#### Verbatim Spoken Scripts:
- **English (EN):** "When we map both engines onto the RUM Conjecture triangle, their complementary nature becomes crystal clear. Cassandra prioritizes Update and Memory overhead; Elasticsearch prioritizes Read latency. No engineer can break this law; choosing an engine is fundamentally choosing which corner of the trade-off space your application requires."
- **Tiếng Việt (VI):** "Khi định vị hai bộ máy lên tam giác Giả thuyết RUM, bản chất bổ trợ lẫn nhau của chúng hiện ra rõ nét. Cassandra ưu tiên chi phí Ghi và Bộ nhớ; Elasticsearch ưu tiên độ trễ Đọc. Không một kỹ sư nào có thể phá vỡ định luật này; việc chọn storage engine thực chất là việc bạn chọn đánh đổi góc nào trong không gian thiết kế."

---

### Slide 23: Experimental Setup: Pure Reference Engines
**Section:** `05 Experiments` | **Badge:** `Methodology`  
**Subtitle:** *Building Clean, Zero-Dependency Prototypes to Measure Pure Storage Mechanics*  

#### Key Points:
- Built zero-dependency Python reference engines to isolate storage mechanics from network or JVM noise.
- Cassandra engine faithfully implements MemTable, CommitLog, SSTables, Bloom filters, and Tombstones.
- Elasticsearch engine implements the Analysis Pipeline, FST dictionaries, Skip Pointers, and BM25 scoring.

#### Verbatim Spoken Scripts:
- **English (EN):** "To conduct rigorous scientific benchmarks, we implemented zero-dependency reference storage engines in pure Python. This eliminates network latency, operating system page cache noise, and JVM garbage collection artifacts. We implement every core mechanism from scratch: MemTables, immutable SSTables, Bloom filters, and compaction for Cassandra; and the analysis pipeline, skip pointers, and Okapi BM25 for Elasticsearch."
- **Tiếng Việt (VI):** "Để thực hiện các đo đạc khoa học chính xác, chúng em tự xây dựng hai storage engine tham chiếu độc lập bằng Python thuần không phụ thuộc thư viện ngoài. Cách tiếp cận này loại bỏ hoàn toàn nhiễu từ độ trễ mạng hay dọn rác bộ nhớ của JVM. Chúng em cài đặt đầy đủ từ đầu: MemTable, SSTable bất biến, Bloom Filter và Compaction cho Cassandra; cùng dây chuyền phân tích từ, Skip Pointer và Okapi BM25 cho Elasticsearch."

---

### Slide 24: Test Datasets & Research Questions
**Section:** `05 Experiments` | **Badge:** `Datasets & Qs`  
**Subtitle:** *Testing Real Data Across 4 Concrete Hypotheses*  

#### Key Points:
- Datasets include 10,000 structured geographic records and 1,655 natural language quotes.
- Q1 tests write scalability under periodic flushes; Q2 tests Bloom filter pruning efficiency.
- Q3 tests multi-term search speedup; Q4 quantifies the exact memory amplification ratio.

#### Verbatim Spoken Scripts:
- **English (EN):** "We evaluate four explicit research questions across two real-world datasets: 10,000 world cities for primary key writes, and 1,655 natural language quotes for search. Q1 asks if Cassandra sustains write speed during flushes. Q2 investigates if Bloom filters eliminate disk reads on absent keys. Q3 quantifies the search speedup over linear scans, and Q4 measures the exact memory cost."
- **Tiếng Việt (VI):** "Chúng em đặt ra 4 câu hỏi nghiên cứu cụ thể trên 2 tập dữ liệu thực tế: 10.000 thành phố trên thế giới cho bài kiểm tra ghi khóa chính, và 1.655 danh ngôn tự nhiên cho bài kiểm tra tìm kiếm. Q1 kiểm tra khả năng duy trì tốc độ ghi của Cassandra khi xả đĩa. Q2 đo hiệu quả loại trừ đọc đĩa của Bloom Filter. Q3 đo lường mức độ tăng tốc tìm kiếm, và Q4 tính toán tỷ lệ tiêu tốn bộ nhớ RAM."

---

### Slide 25: Live Terminal Demo: Run It Yourself
**Section:** `05 Experiments` | **Badge:** `Live Demo`  
**Subtitle:** *Verified Reproduction Commands for Terminal and Google Colab*  

#### Key Points:
- Our presentation includes a live interactive checkpoint.
- Every theoretical claim is backed by a single runnable bash command.
- All tests pass cleanly with zero external third-party dependencies.

#### Verbatim Spoken Scripts:
- **English (EN):** "At this point in the presentation, we switch to our live terminal checkpoint. With a single command, 'python3 demo.py --no-pause', the presentation audience can witness every step executing live: MemTable fills, SSTable flushes, Bloom filter fast-fails, and multi-term BM25 ranking across real datasets."
- **Tiếng Việt (VI):** "Tại thời điểm này trong bài báo cáo, chúng em chuyển sang màn hình terminal để minh họa trực tiếp. Chỉ với một câu lệnh đơn giản 'python3 demo.py --no-pause', hội đồng có thể chứng kiến toàn bộ các bước hoạt động trong thực tế: nạp MemTable, xả SSTable, Bloom Filter loại trừ đọc đĩa và thuật toán BM25 xếp hạng văn bản trên dữ liệu thật."

---

### Slide 26: Empirical Scorecard: 5-Round Results
**Section:** `06 Results` | **Badge:** `Empirical Scorecard`  
**Subtitle:** *Statistical Measurements Across 5 Independent Benchmark Rounds (Mean ± Std Dev)*  

#### Key Points:
- Statistical validation over 5 independent trials confirms all theoretical predictions.
- Cassandra delivers 85k ops/s write throughput with microsecond Bloom filter pruning.
- Elasticsearch delivers 20 µs multi-term searches at the cost of 15× higher RAM consumption.

#### Verbatim Spoken Scripts:
- **English (EN):** "Here is our complete empirical scorecard, reporting sample mean and standard deviation over five repeated rounds after discarding warmup runs. The data confirms our theory: Cassandra achieves 85,000 writes/sec, and Bloom filter pruning drops negative lookups to 3.42 microseconds. Meanwhile, Elasticsearch executes multi-term intersections in 20 microseconds but consumes 15 times more RAM per record."
- **Tiếng Việt (VI):** "Đây là bảng điểm thực nghiệm đầy đủ của chúng em, báo cáo giá trị trung bình mẫu và độ lệch chuẩn qua 5 lần chạy độc lập sau khi đã loại bỏ vòng khởi động. Số liệu khẳng định lý thuyết: Cassandra đạt 85.000 lượt ghi/giây và Bloom Filter giảm thời gian tìm khóa vắng mặt xuống 3,42 micro-giây. Trong khi đó, Elasticsearch thực hiện phép giao đa từ trong 20 micro-giây nhưng tốn gấp 15 lần bộ nhớ RAM cho mỗi bản ghi."

---

### Slide 27: Proof 1: Write Speed & Bloom Pruning
**Section:** `06 Results` | **Badge:** `Proof 1 & 2`  
**Subtitle:** *Answering Research Questions Q1 & Q2 With Statistical Evidence*  

#### Key Points:
- Q1 Answer: Cassandra sustains high write throughput even as data spills from RAM to disk.
- Q2 Answer: Bloom filters achieve 100% pruning accuracy on non-existent keys.
- This proves that LSM write performance does not degrade point read latency on absent keys.

#### Verbatim Spoken Scripts:
- **English (EN):** "Examining Questions 1 and 2 in detail: For Q1, Cassandra sustains an average of 85,000 operations per second across 10,000 records. For Q2, testing against 1,000 non-existent keys proved that the Bloom filter achieves 100% pruning efficiency. Not a single SSTable file was opened on disk, and the check completed in 3.42 microseconds."
- **Tiếng Việt (VI):** "Phân tích chi tiết câu hỏi 1 và 2: Với Q1, Cassandra duy trì tốc độ ghi trung bình 85.000 thao tác/giây trên 10.000 bản ghi. Với Q2, thử nghiệm trên 1.000 khóa không tồn tại chứng minh Bloom Filter đạt hiệu suất loại trừ 100%. Không có bất kỳ file SSTable nào trên đĩa bị mở ra, và quá trình kiểm tra hoàn tất chỉ trong 3,42 micro-giây."

---

### Slide 28: Proof 2: Search Speedup & Memory Cost
**Section:** `06 Results` | **Badge:** `Proof 3 & 4`  
**Subtitle:** *Answering Research Questions Q3 & Q4 With Measured Benchmarks*  

#### Key Points:
- Q3 Answer: The inverted index delivers a 71× to 280× speedup over brute-force scanning.
- Q4 Answer: The memory penalty is exactly 14.9×, verifying the physical cost of precomputing search indexes.
- These empirical findings confirm the theoretical trade-offs described in modern academic literature.

#### Verbatim Spoken Scripts:
- **English (EN):** "Turning to Questions 3 and 4: For Q3, evaluating multi-term queries with posting lists was over 70 times faster than a brute-force scan on a small dataset, with the gap growing even larger at scale. For Q4, our memory measurements revealed an exact 14.9-to-1 memory amplification ratio. Elasticsearch buys search speed directly with RAM."
- **Tiếng Việt (VI):** "Chuyển sang câu hỏi 3 và 4: Với Q3, việc xử lý truy vấn giao từ bằng posting list nhanh hơn quét vét cạn trên 70 lần ngay trên tập dữ liệu nhỏ, và khoảng cách này sẽ tăng theo cấp số nhân ở quy mô triệu bản ghi. Với Q4, đo đạc bộ nhớ cho thấy hệ số tiêu tốn RAM chính xác là 14.9 lần. Elasticsearch mua tốc độ tìm kiếm trực tiếp bằng dung lượng RAM."

---

### Slide 29: Production Architecture: Bank Vault vs. Storefront
**Section:** `07 Architecture` | **Badge:** `Mental Model`  
**Subtitle:** *How to Combine Both Systems in a Real Application Without Conflict*  

#### Key Points:
- Treat Cassandra as the Bank Vault: immutable, durable source of truth for writes.
- Treat Elasticsearch as the Storefront Window: disposable, highly indexed view for customer search.
- Synchronize them asynchronously via Change Data Capture (CDC), never synchronous dual-writes.

#### Verbatim Spoken Scripts:
- **English (EN):** "To synthesize both technologies in real-world systems, think of Cassandra as the Bank Vault and Elasticsearch as the Storefront Display Window. You put gold into the vault for safekeeping—that is Cassandra storing the truth. You arrange pretty merchandise in the display window for customers to find—that is Elasticsearch. If the display window breaks, you simply rebuild it from the vault."
- **Tiếng Việt (VI):** "Để kết hợp hai công nghệ trong thực tế, hãy xem Cassandra là Két Sắt Ngân Hàng và Elasticsearch là Cửa Sổ Trưng Bày. Bạn cất giữ vàng và tiền thật an toàn trong két sắt — đó là Cassandra giữ dữ liệu gốc. Bạn trưng bày hàng mẫu ra cửa kính cho khách hàng dễ tìm kiếm — đó là Elasticsearch. Nếu cửa kính trưng bày bị hỏng, bạn chỉ việc lấy đồ từ trong két sắt ra bày lại."

---

### Slide 30: Production Architecture: The CQRS Pattern
**Section:** `07 Architecture` | **Badge:** `Architecture Solution`  
**Subtitle:** *Separating Writes from Searches Using Change Data Capture (CDC) and Kafka*  

#### Key Points:
- Never write directly to both Cassandra and Elasticsearch from application code (Dual-Write Anti-Pattern).
- Use Change Data Capture (CDC) via Kafka to tail Cassandra's CommitLog asynchronously.
- This architecture maintains eventual consistency without slowing down write ingestion.

#### Verbatim Spoken Scripts:
- **English (EN):** "In production, never write to both Cassandra and Elasticsearch directly from your application code. If one write succeeds and the other fails, your data will silently diverge. The industry standard is CQRS with Change Data Capture. The application writes only to Cassandra. Debezium tails the commit log and streams change events through Kafka to asynchronously populate Elasticsearch."
- **Tiếng Việt (VI):** "Trong môi trường thực tế, tuyệt đối không bao giờ cho ứng dụng ghi đồng thời vào cả Cassandra và Elasticsearch. Nếu một bên thành công còn bên kia lỗi mạng, dữ liệu sẽ bị sai lệch âm thầm. Giải pháp chuẩn mực của ngành là CQRS kết hợp Change Data Capture. Ứng dụng chỉ ghi vào Cassandra. Debezium theo dõi CommitLog và truyền qua Kafka để cập nhật chỉ mục ngầm sang Elasticsearch."

---

### Slide 31: Three Golden Rules of Database Engineering
**Section:** `07 Conclusion` | **Badge:** `Core Lessons`  
**Subtitle:** *Key Lessons for Designing High-Scale Modern Systems*  

#### Key Points:
- Storage physics dictates design: no single storage engine satisfies all workloads.
- Cassandra excels at append-only sequential ingestion; Elasticsearch excels at multi-term lexical retrieval.
- In production, combine both via CQRS and asynchronous Change Data Capture.

#### Verbatim Spoken Scripts:
- **English (EN):** "To conclude our findings, remember three core principles. First: There is no silver bullet—the RUM Conjecture dictates that physical trade-offs are unavoidable. Second: Cassandra and Elasticsearch have complementary asymmetric strengths. Third: Decouple them in production using the CQRS pattern with Change Data Capture."
- **Tiếng Việt (VI):** "Để kết luận buổi báo cáo, chúng em xin đúc kết 3 nguyên tắc cốt lõi. Thứ nhất: Không có giải pháp vạn năng — Giả thuyết RUM khẳng định sự đánh đổi vật lý là tất yếu. Thứ hai: Cassandra và Elasticsearch sở hữu sức mạnh bổ trợ đối lập nhau. Thứ ba: Hãy kết hợp chúng trong thực tế qua mô hình CQRS và Change Data Capture."

---

### Slide 32: Thank You & Open Q&A
**Section:** `07 Conclusion` | **Badge:** `Q&A Session`  
**Subtitle:** *Cảm ơn Thầy Cô và các bạn! Sẵn sàng giải đáp mọi câu hỏi thảo luận*  

#### Key Points:
- Complete code, benchmarks, tests, and interactive slides are fully reproducible.
- Grounded strictly in peer-reviewed modern academic literature (VLDB 2024, Springer 2022).
- Ready for live Q&A session with committee and audience.

#### Verbatim Spoken Scripts:
- **English (EN):** "Thank you very much for your time and attention. All reference implementations, automated unit tests, stress benchmarks, and interactive notebooks are fully open and reproducible in our repository. We are now open and eager to take your questions and discuss any technical details."
- **Tiếng Việt (VI):** "Xin chân thành cảm ơn quý Thầy Cô và các bạn đã chú ý lắng nghe. Toàn bộ mã nguồn hai bộ máy tham chiếu, bài kiểm thử tự động, tập đo đạc hiệu năng và notebook tương tác đều được đóng gói độc lập và tái lập 100% trong kho lưu trữ của nhóm. Chúng em rất mong nhận được những góp ý và câu hỏi thảo luận từ Thầy Cô cùng các bạn."

---
