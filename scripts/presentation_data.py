# Complete 32-slide presentation dataset
import json
import os

ALL_SLIDES = [
    # ------------------ SLIDE 01: COVER / TITLE SLIDE ------------------
    {
        "id": "slide-01",
        "section": "00 Introduction",
        "badge": "Cover Slide",
        "title": "Storage Engine Duality",
        "subtitle": "Apache Cassandra (LSM-Tree) vs. Elasticsearch (Inverted Index) — A Comparative Study",
        "visual_html": """
        <div style="text-align: center; padding: 10px 0;">
          <div style="display: inline-block; background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; color: #93c5fd; padding: 4px 14px; border-radius: 9999px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 14px;">
            CO5173 — ADVANCED DATA ENGINEERING • MASTER OF COMPUTER SCIENCE • HCMUT
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 820px; margin: 0 auto; text-align: left;">
            <div style="background: rgba(59, 130, 246, 0.1); border: 2px solid #3b82f6; border-radius: 12px; padding: 18px;">
              <div style="font-size: 32px; margin-bottom: 6px;">🏛️</div>
              <div style="font-size: 18px; font-weight: 800; color: #60a5fa;">Apache Cassandra</div>
              <div style="font-size: 12px; color: #93c5fd; font-family: monospace;">Log-Structured Merge-Tree (LSM)</div>
              <div style="margin-top: 10px; font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                <strong>Optimized for high-speed writes:</strong> Buffers writes in fast RAM and writes smooth sequential streams to disk without random seeks.
              </div>
            </div>
            <div style="background: rgba(6, 182, 212, 0.1); border: 2px solid #06b6d4; border-radius: 12px; padding: 18px;">
              <div style="font-size: 32px; margin-bottom: 6px;">🔍</div>
              <div style="font-size: 18px; font-weight: 800; color: #22d3ee;">Elasticsearch</div>
              <div style="font-size: 12px; color: #67e8f9; font-family: monospace;">Inverted Index & Okapi BM25</div>
              <div style="margin-top: 10px; font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                <strong>Optimized for rich text search:</strong> Catalogs every word like a book index and ranks best matches using relevance math.
              </div>
            </div>
          </div>
          <div style="margin-top: 16px; font-size: 12.5px; color: #94a3b8; font-family: monospace;">
            Theoretical Foundation: The RUM Conjecture (Harvard / BU) • VLDB Journal (2024) • Springer (2022)
          </div>
        </div>
        """,
        "key_points": [
          "Final Project for CO5173 Advanced Data Engineering, HCMUT Master of Computer Science.",
          "Compares two opposite storage designs: write-optimized LSM-Trees vs search-optimized Inverted Indexes.",
          "Demonstrates why modern systems need both engines using clear analogies and empirical proofs."
        ],
        "script_en": "Good day, professors and fellow students. Welcome to our presentation for CO5173 Advanced Data Engineering. Today, we explore the storage engine duality between Apache Cassandra and Elasticsearch. In modern data systems, no single database can do everything well. Over the next 15 minutes, we will explain why traditional databases struggle at scale, how Cassandra and Elasticsearch solve these problems with opposite designs, and show live benchmark proof from our code.",
        "script_vi": "Kính chào quý Thầy Cô và các bạn học viên cao học. Chào mừng quý vị đến với buổi báo cáo đồ án môn CO5173 Kỹ nghệ Dữ liệu Nâng cao. Hôm nay, chúng em xin trình bày về tính nhị nguyên giữa Apache Cassandra và Elasticsearch. Trong hệ thống dữ liệu lớn, không một cơ sở dữ liệu nào hoàn hảo cho mọi tác vụ. Trong 15 phút tới, chúng ta sẽ cùng tìm hiểu vì sao database truyền thống gặp giới hạn, cách Cassandra và Elasticsearch giải quyết qua hai thiết kế đối lập, và chứng minh bằng số liệu thực nghiệm."
    },

    # ------------------ SLIDE 02: ROADMAP / AGENDA ------------------
    {
        "id": "slide-02",
        "section": "00 Introduction",
        "badge": "Roadmap",
        "title": "Presentation Roadmap: The 4 Acts",
        "subtitle": "A Guided 15-Minute Tour Through Storage Mechanics & Empirical Evidence",
        "visual_html": """
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 10px;">
          <div style="background: #1e293b; border-top: 4px solid #ef4444; border-radius: 8px; padding: 16px;">
            <div style="font-size: 12px; font-weight: 800; color: #f87171;">ACT 1</div>
            <div style="font-size: 14px; font-weight: 800; color: #fff; margin: 6px 0;">The Storage Crisis</div>
            <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              Why traditional databases (B+ Trees) waste disk work on small updates and crawl when searching words.
            </p>
          </div>
          <div style="background: #1e293b; border-top: 4px solid #3b82f6; border-radius: 8px; padding: 16px;">
            <div style="font-size: 12px; font-weight: 800; color: #60a5fa;">ACT 2</div>
            <div style="font-size: 14px; font-weight: 800; color: #fff; margin: 6px 0;">Cassandra & LSM</div>
            <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              The Desk Notepad analogy, immutable disk files, background cleanup, and microsecond Bloom filters.
            </p>
          </div>
          <div style="background: #1e293b; border-top: 4px solid #06b6d4; border-radius: 8px; padding: 16px;">
            <div style="font-size: 12px; font-weight: 800; color: #22d3ee;">ACT 3</div>
            <div style="font-size: 14px; font-weight: 800; color: #fff; margin: 6px 0;">Elasticsearch & Index</div>
            <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              The Book Index analogy, text cleanup pipeline, skip-pointer shortcuts, and BM25 relevance ranking.
            </p>
          </div>
          <div style="background: #1e293b; border-top: 4px solid #10b981; border-radius: 8px; padding: 16px;">
            <div style="font-size: 12px; font-weight: 800; color: #34d399;">ACT 4</div>
            <div style="font-size: 14px; font-weight: 800; color: #fff; margin: 6px 0;">Experiments & CQRS</div>
            <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              Live terminal checkpoints, 5-round benchmark scorecard, Bank Vault vs. Storefront, and Kafka sync.
            </p>
          </div>
        </div>
        """,
        "key_points": [
          "Calibrated strictly for a 15-minute presentation (~30 seconds per slide).",
          "Follows a logical story arc: The Crisis -> Solution 1 (Cassandra) -> Solution 2 (Elasticsearch) -> Synthesis.",
          "Every theoretical concept is paired with an intuitive real-world analogy and runnable code."
        ],
        "script_en": "Here is our 15-minute roadmap organized into four clear acts. In Act 1, we look at the storage crisis: why traditional databases struggle with heavy writes and text searches. In Act 2, we explain Cassandra and LSM trees through our desk notepad analogy. In Act 3, we explain Elasticsearch and Inverted Indexes using the book index analogy. Finally, in Act 4, we examine our empirical benchmark results and show how to combine both systems in production using the CQRS pattern.",
        "script_vi": "Đây là lộ trình 15 phút của nhóm qua 4 phần rõ ràng. Trong Phần 1, ta tìm hiểu cuộc khủng hoảng lưu trữ khi database truyền thống gặp tải ghi cao và tìm kiếm từ ngữ. Trong Phần 2, ta khám phá Cassandra và LSM-Tree qua hình ảnh cuốn sổ tay. Trong Phần 3, ta phân tích Elasticsearch và Chỉ mục đảo qua hình ảnh mục lục tra cứu cuối sách. Cuối cùng, trong Phần 4, ta đối chiếu các kết quả đo đạc thực nghiệm và cách phối hợp cả hai trong thực tế bằng mô hình CQRS."
    },

    # ------------------ SLIDE 03: THE STORAGE CRISIS - OVERWRITE TRAP ------------------
    {
        "id": "slide-03",
        "section": "01 Storage Crisis",
        "badge": "Problem 1",
        "title": "Traditional Databases: The Overwrite Trap",
        "subtitle": "How Changing a 50-Byte Record Forces a 16,384-Byte Disk Rewrite",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px dashed #ef4444; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; color: #f87171; font-weight: 700; margin-bottom: 8px;">FIXED DISK PAGE (16 KB = 16,384 BYTES)</div>
            <div style="font-size: 11px; color: #94a3b8; margin-bottom: 12px;">Standard B+ Tree Page (MySQL InnoDB, PostgreSQL)</div>
            <div style="background: #1e293b; border: 2px solid #ef4444; border-radius: 8px; padding: 16px;">
              <div style="height: 10px; background: #334155; border-radius: 4px; margin-bottom: 8px;"></div>
              <div style="background: #dc2626; color: white; padding: 8px; border-radius: 6px; font-size: 13px; font-weight: 700; box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);">
                ✏️ Change only 50 bytes of user status
              </div>
              <div style="height: 10px; background: #334155; border-radius: 4px; margin-top: 8px;"></div>
            </div>
            <div style="margin-top: 14px; font-size: 13px; color: #fb7185; font-weight: 700;">
              Rewrites the entire 16,384 bytes back to disk!
            </div>
          </div>
          <div>
            <div style="background: rgba(244, 63, 94, 0.15); border-left: 4px solid #f43f5e; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #fb7185;">Write Amplification: ~327× Waste</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">
                <strong>Write Amplification:</strong> Writing much more data to physical disk than the application actually changed (16,384 bytes written / 50 bytes changed).
              </div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Random Disk Seeks:</strong> Disk heads jump around to find scattered pages, causing queue bottlenecks.<br/>
              • <strong>Flash Drive Wear:</strong> Wasting writes burns out SSD lifespan much faster.<br/>
              • <strong>Lock Contention:</strong> The whole 16 KB page is locked, forcing readers to wait.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Traditional databases use B+ Trees that store data in fixed-size blocks called pages (typically 16 KB).",
          "Updating even one small field requires rewriting the entire 16 KB page, causing ~327× write amplification.",
          "This in-place update design creates random disk jumping and caps write ingestion throughput."
        ],
        "script_en": "To understand why Cassandra was invented, we first look at the overwrite trap in traditional relational databases like MySQL or PostgreSQL. These systems organize data into fixed 16-kilobyte pages using B+ Trees. When you update a 50-byte user status, the database cannot write just 50 bytes. It must rewrite all 16,384 bytes back to disk. That is a 327-fold write amplification, creating random disk jumping and choking write performance.",
        "script_vi": "Để hiểu vì sao Cassandra ra đời, trước hết ta nhìn vào cái bẫy ghi đè của các database truyền thống như MySQL hay PostgreSQL. Chúng tổ chức dữ liệu theo các trang cố định 16 KB qua cấu trúc B+ Tree. Khi bạn sửa một dòng trạng thái 50 byte, hệ quản trị không thể chỉ ghi 50 byte, mà buộc phải ghi lại toàn bộ 16.384 byte xuống đĩa. Hệ số khuếch đại ghi gấp 327 lần này sinh ra nhảy đĩa ngẫu nhiên và làm nghẽn luồng ghi."
    },

    # ------------------ SLIDE 04: FULL-SCAN SEARCH TRAP ------------------
    {
        "id": "slide-04",
        "section": "01 Storage Crisis",
        "badge": "Problem 2",
        "title": "Traditional Databases: The Full-Scan Trap",
        "subtitle": "Why Searching for Words Using Wildcards Bypasses Normal Indexes",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div class="book-mockup">
            <div class="book-spine"></div>
            <div class="laser-bar"></div>
            <div style="font-size: 12px; color: #94a3b8; font-weight: 700; margin-left: 16px;">
              BRUTE-FORCE SCANNING: PAGE 289 / 500
            </div>
            <div class="book-lines">
              <div class="book-line"></div>
              <div class="book-line short"></div>
              <div class="book-line medium"></div>
              <div class="book-line"></div>
              <div class="book-line short"></div>
            </div>
            <div style="margin-left: 16px; background: rgba(244, 63, 94, 0.25); border: 1px solid #f43f5e; border-radius: 6px; padding: 6px 12px; font-size: 12px; color: #fca5a5; font-family: monospace;">
              WHERE text LIKE '%database%' -> Reading every single row!
            </div>
          </div>
          <div>
            <div style="background: rgba(244, 63, 94, 0.15); border-left: 4px solid #f43f5e; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #fb7185;">Full Table Scan: Linear Growth</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">
                <strong>Full Table Scan:</strong> Reading all rows from start to finish because the index cannot search inside words.
              </div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>B+ Tree Bypassed:</strong> B+ Tree indexes only help when matching the start of a word; wildcards (<code>%word%</code>) disable them.<br/>
              • <strong>No Relevance Scoring:</strong> SQL only returns a binary Yes/No match; it cannot rank which result is best.<br/>
              • <strong>Multi-Word Pain:</strong> Searching multiple words (AND/OR) causes repeated expensive disk reads.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "B+ Tree indexes only work for exact matches or prefix searches; leading wildcards bypass them entirely.",
          "Forces a full table scan across millions of disk rows, consuming massive CPU and I/O bandwidth.",
          "Relational databases cannot calculate relevance scores to rank which documents are the best answers."
        ],
        "script_en": "The second major limit of traditional databases is text search. If you query with a wildcard like WHERE text LIKE '%database%', the leading percentage sign bypasses the B+ Tree index completely. The database is forced to perform a full table scan, reading every row from disk. This is slow, wastes system resources, and cannot rank which document is the most relevant answer.",
        "script_vi": "Giới hạn lớn thứ hai của database truyền thống là tìm kiếm văn bản. Khi bạn tìm kiếm với ký tự đại diện như LIKE '%database%', dấu phần trăm đứng đầu làm cây B+ mất tác dụng. Hệ thống buộc phải quét toàn bộ bảng, đọc từng dòng trên đĩa. Cách này rất chậm, lãng phí tài nguyên và hoàn toàn không thể xếp hạng xem tài liệu nào là câu trả lời tốt nhất."
    },

    # ------------------ SLIDE 05: FUNDAMENTAL DILEMMA ------------------
    {
        "id": "slide-05",
        "section": "01 Storage Crisis",
        "badge": "The Conflict",
        "title": "The Writer vs. Reader Conflict",
        "subtitle": "Why One Storage Engine Cannot Be the Fastest at Both Writing and Searching",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 22px; margin-top: 10px;">
          <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center;">
            <div style="background: #1e293b; border-radius: 8px; padding: 18px; text-align: center; border-top: 4px solid #3b82f6;">
              <div style="font-size: 17px; font-weight: 800; color: #60a5fa;">The Fast Writer Priority</div>
              <p style="font-size: 13px; color: #94a3b8; margin-top: 8px; line-height: 1.5;">
                "Do zero indexing upfront. Just append raw data smoothly into memory and onto disk as fast as it arrives!"
              </p>
              <div style="margin-top: 12px; font-size: 12px; background: rgba(59, 130, 246, 0.2); color: #93c5fd; padding: 6px; border-radius: 4px; font-weight: 700;">
                Apache Cassandra (LSM-Tree)
              </div>
            </div>

            <div style="font-size: 26px; font-weight: 900; color: #f59e0b;">⚡ VS ⚡</div>

            <div style="background: #1e293b; border-radius: 8px; padding: 18px; text-align: center; border-top: 4px solid #06b6d4;">
              <div style="font-size: 17px; font-weight: 800; color: #22d3ee;">The Instant Reader Priority</div>
              <p style="font-size: 13px; color: #94a3b8; margin-top: 8px; line-height: 1.5;">
                "Dissect every word upfront, build sorted term catalogs, and calculate relevance scores before answering!"
              </p>
              <div style="margin-top: 12px; font-size: 12px; background: rgba(6, 182, 212, 0.2); color: #67e8f9; padding: 6px; border-radius: 4px; font-weight: 700;">
                Elasticsearch (Inverted Index)
              </div>
            </div>
          </div>
          <div style="margin-top: 18px; text-align: center; font-size: 13px; color: #e2e8f0; border-top: 1px solid #374151; padding-top: 14px;">
            <strong>The Core Storage Law:</strong> Heavy indexing during writes kills write speed. Skipping indexing kills search speed.
          </div>
        </div>
        """,
        "key_points": [
          "Writing at maximum speed requires minimal upfront work: simply appending sequential bytes.",
          "Searching in microseconds requires heavy upfront work: tokenizing words and pre-building sorted catalogs.",
          "Trying to perform both tasks on a single storage layout forces both operations to slow down."
        ],
        "script_en": "Here is the fundamental conflict in database design. To write at maximum hardware speed, you must do almost zero work when saving data: just append bytes sequentially. But to search across millions of documents in microseconds, you must dissect every word upfront into sorted lists. Doing both on the same storage structure is physically impossible.",
        "script_vi": "Đây là mâu thuẫn cốt lõi trong thiết kế cơ sở dữ liệu. Muốn ghi ở tốc độ phần cứng tối đa, bạn phải làm ít việc nhất lúc ghi: chỉ ghi nối đuôi tuần tự. Nhưng muốn tìm kiếm triệu tài liệu trong vài micro-giây, bạn phải bóc tách từng từ ngữ thành các danh sách sắp xếp sẵn. Làm cả hai trên cùng một cấu trúc lưu trữ là điều bất khả thi về mặt vật lý."
    },

    # ------------------ SLIDE 06: RUM CONJECTURE ------------------
    {
        "id": "slide-06",
        "section": "01 Storage Crisis",
        "badge": "Storage Law",
        "title": "The Storage Law: The RUM Conjecture",
        "subtitle": "You Can Only Optimize Two: Read (R), Update (U), or Memory (M)",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 13px; font-weight: 700; color: #94a3b8; margin-bottom: 8px;">THE RUM TRIANGLE</div>
            <div style="padding: 10px; background: #0f172a; border-radius: 8px; border: 1px solid #1e293b;">
              <div style="font-size: 14px; font-weight: 800; color: #f43f5e; margin-bottom: 12px;">▲ Read Overhead (R)</div>
              <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 800;">
                <span style="color: #3b82f6;">◄ Update (U)</span>
                <span style="color: #10b981;">Memory (M) ►</span>
              </div>
            </div>
            <div style="margin-top: 12px; font-size: 11.5px; color: #94a3b8;">
              Athanassoulis et al. (Harvard / BU, EDBT 2016)
            </div>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 4px; margin-bottom: 12px;">
              <strong style="color: #60a5fa;">Cassandra (LSM):</strong> Minimizes <strong>Update (U) + Memory (M)</strong>. Fast appends in low RAM; point reads are accelerated by in-memory Bloom filters.
            </div>
            <div style="background: rgba(6, 182, 212, 0.15); border-left: 4px solid #06b6d4; padding: 12px 16px; border-radius: 4px;">
              <strong style="color: #22d3ee;">Elasticsearch:</strong> Minimizes <strong>Read (R)</strong>. Delivers microsecond search, but pays with high memory (15× more RAM) and heavy index merges.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "The RUM Conjecture (Harvard/BU) proves that minimizing two database costs inevitably worsens the third cost.",
          "Cassandra prioritizes low update work and low memory usage, deferring sorting to background threads.",
          "Elasticsearch prioritizes instant search speed, pre-building rich catalogs at the cost of high memory."
        ],
        "script_en": "This physical limit was proven by researchers at Harvard and Boston University as the RUM Conjecture. You can optimize at most two corners of the triangle: Read overhead, Update overhead, or Memory overhead. Cassandra minimizes Update and Memory costs, while Elasticsearch minimizes Read overhead at the expense of high memory consumption.",
        "script_vi": "Giới hạn vật lý này được chứng minh qua Giả thuyết RUM bởi các nhà nghiên cứu Đại học Harvard và Boston. Bạn chỉ có thể tối ưu tối đa hai trong ba góc của tam giác: Chi phí Đọc (R), Chi phí Ghi (U), hoặc Bộ nhớ RAM (M). Cassandra tối ưu Ghi và Bộ nhớ, trong khi Elasticsearch tối ưu tốc độ Đọc và chấp nhận tiêu tốn nhiều dung lượng RAM."
    }
]

print("Script template written.")


# Part 2: LSM-Tree & Cassandra (Slides 07-13)

PART_2_SLIDES = [
    {
        "id": "slide-07",
        "section": "02 LSM & Cassandra",
        "badge": "Analogy Step 1",
        "title": "LSM Analogy: The Desk Notepad",
        "subtitle": "Step 1: Saving Writes into Fast RAM Without Touching Slow Disk",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div class="notepad-mockup">
            <div style="font-size: 13px; font-weight: 800; border-bottom: 2px solid #b45309; padding-bottom: 6px; margin-bottom: 8px;">
              📝 DESK NOTEPAD (MemTable in RAM)
            </div>
            <div class="notepad-line"><span>k101: Alice (US)</span><span style="color: #10b981;">v1</span></div>
            <div class="notepad-line"><span>k102: Bob (UK)</span><span style="color: #10b981;">v1</span></div>
            <div class="notepad-line"><span>k103: Charlie (CA)</span><span style="color: #10b981;">v1</span></div>
            <div class="notepad-line" style="border: none;"><span>k104: Diana (VN)</span><span style="color: #10b981;">v1</span></div>
            <div style="margin-top: 10px; font-size: 11.5px; color: #b45309; text-align: right;">
              Automatically kept sorted in memory: <em>O</em>(log <em>M</em>)
            </div>
          </div>
          <div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #34d399;">Fast Memory Buffering</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">Zero disk seeks during customer writes</div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>MemTable (RAM Buffer):</strong> An in-memory sorted write buffer (like a notepad on your desk) that accepts writes instantly.<br/>
              • <strong>CommitLog (Crash Safety):</strong> An append-only log on disk that records every write in arrival order so no data is lost on power failure.<br/>
              • <strong>Result:</strong> Writes finish in microseconds without waiting for slow disk seeking.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "When a write arrives, Cassandra never updates data on disk immediately.",
          "It writes to an active, sorted in-memory buffer called the MemTable.",
          "For crash protection, it appends a record sequentially to the on-disk CommitLog."
        ],
        "script_en": "Imagine working at a busy library intake desk. When new books arrive, you don't run to the shelves to insert them one by one. You simply jot the titles down on your desk notepad. In Cassandra, this notepad is the MemTable in RAM. For crash safety, an assistant logs the title sequentially into an append-only commit log on disk. The write returns instantly in microseconds.",
        "script_vi": "Hãy tưởng tượng bạn là thủ thư ở một thư viện đông đúc. Khi sách mới trả về, bạn không chạy đi tìm từng kệ để nhét vào. Bạn chỉ ghi nhanh tiêu đề vào cuốn sổ tay trên bàn làm việc. Trong Cassandra, cuốn sổ tay này chính là MemTable trên RAM. Để phòng sự cố mất điện, hệ thống ghi nối đuôi một dòng vào CommitLog trên đĩa. Giao dịch hoàn tất lập tức trong vài phần triệu giây."
    },
    {
        "id": "slide-08",
        "section": "02 LSM & Cassandra",
        "badge": "Analogy Step 2",
        "title": "LSM Analogy: Staple & Shelf",
        "subtitle": "Step 2: Freezing the Filled Notepad into an Immutable Disk File",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #3b82f6; border-radius: 12px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <span style="font-size: 13px; font-weight: 800; color: #60a5fa;">DISK SHELF: SSTables</span>
              <span style="background: #1e3a8a; color: #bfdbfe; font-size: 11px; padding: 2px 8px; border-radius: 4px;">READ-ONLY / IMMUTABLE</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
              <div style="background: #1e293b; border: 1px solid #475569; border-radius: 6px; padding: 10px; font-family: monospace; font-size: 12px;">
                <div style="color: #38bdf8; font-weight: 700;">📕 SSTable-0 (Flushed at 10:00)</div>
                <div style="color: #94a3b8; margin-top: 4px;">Keys: [101, 102, 103, 104] — Sorted</div>
              </div>
              <div style="background: #1e293b; border: 1px solid #475569; border-radius: 6px; padding: 10px; font-family: monospace; font-size: 12px;">
                <div style="color: #38bdf8; font-weight: 700;">📘 SSTable-1 (Flushed at 10:05)</div>
                <div style="color: #94a3b8; margin-top: 4px;">Keys: [105, 106, 107, 108] — Sorted</div>
              </div>
            </div>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #60a5fa;">Flushing to SSTable</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">100% sequential disk streaming</div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Flushing:</strong> When the MemTable fills up (64–256 MB), it freezes and writes out to disk in one smooth line.<br/>
              • <strong>SSTable (Sorted String Table):</strong> An immutable, read-only disk file containing sorted keys.<br/>
              • <strong>Why Immutability Matters:</strong> Because files never change in-place, multiple readers can read safely without lock conflicts.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "When the MemTable fills up, it is frozen and written to disk as a sorted file called an SSTable.",
          "Writing an SSTable to disk is 100% sequential, maximizing hardware disk write bandwidth.",
          "SSTables are immutable (read-only); they are never edited or overwritten in place."
        ],
        "script_en": "When your desk notepad is full, you don't erase it. You tear out the page, staple it into a neat sorted booklet, and place it on the library shelf. In Cassandra, this is an SSTable. Because SSTables are immutable, multiple threads can read them without any locking contention, and writing them to disk is a pure sequential stream at maximum disk bandwidth.",
        "script_vi": "Khi cuốn sổ tay trên bàn đã đầy, bạn không xóa đi mà xé trang, bấm lại thành một tập sách mỏng đã xếp thứ tự rồi đặt lên kệ. Trong Cassandra, đó là SSTable. Vì SSTable là bất biến (immutable), nhiều luồng có thể đọc đồng thời mà không sợ tranh chấp khóa, và việc ghi xuống đĩa diễn ra hoàn toàn tuần tự với tốc độ tối đa của phần cứng."
    },
    {
        "id": "slide-09",
        "section": "02 LSM & Cassandra",
        "badge": "Analogy Step 3",
        "title": "LSM Analogy: Background Compaction",
        "subtitle": "Step 3: Merging Multiple Disk Files and Permanently Erasing Deleted Data",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #10b981; border-radius: 12px; padding: 20px;">
            <div style="font-size: 13px; font-weight: 800; color: #34d399; margin-bottom: 12px;">MULTI-WAY STREAMING MERGE</div>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div style="background: #1e293b; padding: 8px 12px; border-radius: 6px; font-size: 12px; font-family: monospace;">
                SSTable-0: [k101:v1, <span style="color:#ef4444;">k102:v1</span>]
              </div>
              <div style="background: #1e293b; padding: 8px 12px; border-radius: 6px; font-size: 12px; font-family: monospace;">
                SSTable-1: [k101:v2, <span style="color:#ef4444;">k102:TOMBSTONE</span>]
              </div>
              <div style="text-align: center; color: #f59e0b; font-size: 16px;">⬇️ Background Compactor ⬇️</div>
              <div style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; padding: 10px 12px; border-radius: 6px; font-size: 12px; font-family: monospace;">
                <strong>Compacted SSTable:</strong> [k101:v2]<br/>
                <span style="color: #6ee7b7; font-size: 11px;">✓ k102 tombstone purged | ✓ Old v1 discarded</span>
              </div>
            </div>
          </div>
          <div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #34d399;">Background Clean-Up</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">Merges sorted files in the background</div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Tombstone (Deletion Marker):</strong> Cassandra never deletes data in-place; it writes a special deletion note called a Tombstone.<br/>
              • <strong>Compaction:</strong> Background threads merge multiple sorted SSTables into one clean file, keeping only the newest version of each key.<br/>
              • <strong>Garbage Removal:</strong> Compaction permanently erases dead records and frees up disk space.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Deletions in Cassandra are inserts of a special Tombstone marker (no in-place file modifications).",
          "Over time, multiple SSTables accumulate on disk; background compaction merges them cleanly.",
          "Compaction reclaims disk space by purging superseded values and tombstones."
        ],
        "script_en": "As days go by, your library shelf accumulates dozens of booklets with obsolete notes and cross-outs. An assistant works in the background, reading multiple sorted booklets at once, taking the newest entry for each book, and copying them into a single clean volume. In Cassandra, this is Compaction. Deletions are handled by writing Tombstones, which compaction permanently purges.",
        "script_vi": "Theo thời gian, trên kệ tích tụ hàng chục tập sách mỏng chứa cả những ghi chú cũ và các dòng bị gạch xóa. Một người trợ lý sẽ làm việc ngầm: đọc đồng thời các tập sách đã xếp thứ tự, giữ lại bản ghi mới nhất và chép vào một cuốn sách lớn duy nhất. Trong Cassandra, đó là quá trình Compaction. Việc xóa dữ liệu được thực hiện bằng cách ghi một thẻ Tombstone, và Compaction sẽ tiêu hủy vĩnh viễn thẻ này."
    },
    {
        "id": "slide-10",
        "section": "02 LSM & Cassandra",
        "badge": "Hardware Physics",
        "title": "Storage Physics: Why Sequential Writing Wins",
        "subtitle": "Writing in a Straight Line is 50× to 100× Faster Than Jumping Across Disk Sectors",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px;">
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #60a5fa; font-weight: 700;">Cassandra Sequential Append</span>
                <span style="color: #60a5fa; font-weight: 700;">~500 MB/s</span>
              </div>
              <div style="height: 16px; background: #1e293b; border-radius: 8px; overflow: hidden;">
                <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
              </div>
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #f87171; font-weight: 700;">B+ Tree Random In-Place Seek</span>
                <span style="color: #f87171; font-weight: 700;">~5-10 MB/s</span>
              </div>
              <div style="height: 16px; background: #1e293b; border-radius: 8px; overflow: hidden;">
                <div style="width: 5%; height: 100%; background: #ef4444;"></div>
              </div>
            </div>
            <div style="margin-top: 18px; font-size: 12px; color: #94a3b8; text-align: center;">
              Mechanical HDDs waste 95% of time seeking. SSDs suffer block erase overhead.
            </div>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #60a5fa;">The Physics Advantage</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">Exploiting raw disk bus speed</div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Sequential I/O:</strong> Writing data smoothly in one continuous stream uses 100% of the disk connection speed.<br/>
              • <strong>Zero Read-Before-Write:</strong> Unlike B+ Trees, Cassandra never has to read a page from disk before saving an update.<br/>
              • <strong>Predictable Throughput:</strong> Write speed stays high and stable (>85,000 writes/sec in our tests).
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Storage hardware (both SSDs and HDDs) writes sequential streams much faster than random seeks.",
          "Cassandra translates every client mutation into a smooth sequential write.",
          "This mechanical advantage delivers over 85,000 writes/sec in our benchmark tests."
        ],
        "script_en": "The secret behind Cassandra's legendary write performance is not complex code; it is hardware physics. Disk drives, whether spinning hard drives or NVMe SSDs, write sequential streams 50 to 100 times faster than random seeks. By strictly buffering in RAM and flushing sequentially to disk, Cassandra achieves over 85,000 writes per second on commodity hardware.",
        "script_vi": "Bí quyết đằng sau hiệu năng ghi huyền thoại của Cassandra không nằm ở thuật toán phức tạp mà bắt nguồn từ vật lý phần cứng. Mọi ổ đĩa, từ đĩa từ quay đến SSD NVMe, đều ghi dữ liệu tuần tự nhanh gấp 50 đến 100 lần so với tìm kiếm ngẫu nhiên. Bằng cách gom trên RAM và chỉ ghi nối đuôi tuần tự xuống đĩa, Cassandra dễ dàng đạt trên 85.000 lượt ghi mỗi giây trên phần cứng phổ thông."
    },
    {
        "id": "slide-11",
        "section": "02 LSM & Cassandra",
        "badge": "Fast RAM Check",
        "title": "Cassandra's Helper: The Bloom Filter in RAM",
        "subtitle": "How to Check 20 Disk Files in Nanoseconds Without Doing 20 Slow Disk Reads",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #475569; border-radius: 12px; padding: 22px; margin-top: 10px;">
          <div style="font-size: 13px; font-weight: 800; color: #38bdf8; margin-bottom: 10px;">IN-MEMORY BIT ARRAY (~10 BITS PER KEY)</div>
          <div class="bit-array-grid">
            <div class="bit-cell one"><span>1</span><span style="font-size:9px; color:#6ee7b7;">b0</span></div>
            <div class="bit-cell zero"><span>0</span><span style="font-size:9px;">b1</span></div>
            <div class="bit-cell one"><span>1</span><span style="font-size:9px; color:#6ee7b7;">b2</span></div>
            <div class="bit-cell zero"><span>0</span><span style="font-size:9px;">b3</span></div>
            <div class="bit-cell one"><span>1</span><span style="font-size:9px; color:#6ee7b7;">b4</span></div>
            <div class="bit-cell zero"><span>0</span><span style="font-size:9px;">b5</span></div>
            <div class="bit-cell fail-target"><span>0</span><span style="font-size:9px;">b6</span></div>
            <div class="bit-cell one"><span>1</span><span style="font-size:9px; color:#6ee7b7;">b7</span></div>
            <div class="bit-cell zero"><span>0</span><span style="font-size:9px;">b8</span></div>
            <div class="bit-cell one"><span>1</span><span style="font-size:9px; color:#6ee7b7;">b9</span></div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
            <div style="background: #1e293b; padding: 12px; border-radius: 6px; font-size: 12.5px; line-height: 1.5;">
              <strong style="color: #60a5fa;">The LSM Read Problem:</strong> A requested key could reside in any of 20 SSTable files on disk. Checking all 20 would require 20 slow disk lookups!
            </div>
            <div style="background: #1e293b; padding: 12px; border-radius: 6px; font-size: 12.5px; line-height: 1.5;">
              <strong style="color: #34d399;">The Bloom Solution:</strong> A compact bit-checker in RAM (~10 bits per key). It answers in nanoseconds: <em>"Definitely NOT in this file"</em> or <em>"Might be here"</em>.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Because SSTables are immutable, an item could be in any of the SSTable files on disk.",
          "Reading without an index would mean opening and searching every SSTable file on disk.",
          "Cassandra pairs every SSTable with a compact Bloom Filter in RAM to check key presence in nanoseconds."
        ],
        "script_en": "There is a catch to LSM-Trees: reading can be slow because data is scattered across multiple SSTable files on disk. If you have 20 SSTables, do you have to do 20 disk seeks? No! Cassandra's secret weapon is the Bloom Filter. Each SSTable has an in-memory bit array requiring only about 10 bits per key. It tests key presence in nanoseconds before touching disk.",
        "script_vi": "Cấu trúc LSM-Tree có một điểm yếu: đọc có thể bị chậm vì dữ liệu phân tán ở nhiều file SSTable trên đĩa. Nếu có 20 SSTable, chẳng lẽ phải tìm kiếm đĩa 20 lần? Hoàn toàn không! Vũ khí bí mật của Cassandra là Bloom Filter. Mỗi SSTable có một mảng bit nằm sẵn trên RAM, chỉ tốn khoảng 10 bit cho mỗi khóa. Nó kiểm tra sự tồn tại trong vài nano giây trước khi chạm vào đĩa."
    },
    {
        "id": "slide-12",
        "section": "02 LSM & Cassandra",
        "badge": "Fast-Fail Mechanics",
        "title": "Bloom Filter Fast-Fail Mechanics",
        "subtitle": "How a Single '0' Bit Skips Slow Disk Access Entirely in 3.42 Microseconds",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #ef4444; border-radius: 12px; padding: 20px;">
            <div style="font-size: 14px; font-weight: 800; color: #fb7185; margin-bottom: 12px;">
              QUERY: Looking up Absent Key 999
            </div>
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 12px; line-height: 1.8;">
              1. Hash 1 (Key 999) -> Bit Index 2 -> Value: <span style="color:#34d399; font-weight:700;">1</span><br/>
              2. Hash 2 (Key 999) -> Bit Index 4 -> Value: <span style="color:#34d399; font-weight:700;">1</span><br/>
              3. Hash 3 (Key 999) -> Bit Index 6 -> Value: <span style="color:#ef4444; font-weight:900;">0 (ZERO!)</span>
            </div>
            <div style="margin-top: 14px; background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; border-radius: 8px; padding: 12px; text-align: center;">
              <div style="font-size: 15px; font-weight: 800; color: #fca5a5;">🛡️ FAST-FAIL PRUNED!</div>
              <div style="font-size: 12px; color: #fecaca; margin-top: 4px;">
                Mathematically impossible for Key 999 to be in this SSTable file.<br/>
                <strong>Zero Disk I/O Performed!</strong>
              </div>
            </div>
          </div>
          <div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #34d399;">3.42 µs Miss Latency</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">Measured 37% faster than finding an existing key!</div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Zero False Negatives:</strong> If any calculated bit is 0, the key is 100% guaranteed absent.<br/>
              • <strong>Prunes Irrelevant Files:</strong> Cassandra immediately skips opening the file on disk.<br/>
              • <strong>Hardware Benefit:</strong> Converts a slow disk search into an instant memory bit check.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "If any single hash bit evaluates to 0, the key is mathematically guaranteed not to exist in that file.",
          "Cassandra immediately aborts searching that SSTable without touching physical disk.",
          "Our live benchmark proves absent lookups take just 3.42 µs—faster than a hit!"
        ],
        "script_en": "Here is the exact mathematics of why Bloom filters are so powerful. When a key is inserted, three hash functions flip three bits to 1. To check if an absent key like 999 exists, we compute the same three hashes. If even a single bit is 0, it is mathematically impossible for that key to be in the SSTable. Cassandra immediately fast-fails in 3.4 microseconds, completely bypassing disk I/O.",
        "script_vi": "Đây là toán học chính xác giải thích sức mạnh của Bloom Filter. Khi nạp một khóa, ba hàm băm sẽ bật ba bit tương ứng lên 1. Để kiểm tra một khóa không tồn tại như 999, ta tính lại ba vị trí bit đó. Chỉ cần một bit mang giá trị 0, ta khẳng định chắc chắn 100% khóa đó không hề nằm trong SSTable. Cassandra lập tức dừng lại trong 3,4 micro-giây mà không hề tốn một lượt đọc đĩa nào."
    },
    {
        "id": "slide-13",
        "section": "02 LSM & Cassandra",
        "badge": "Anti-Pattern",
        "title": "Cassandra Warning: 'ALLOW FILTERING' Danger",
        "subtitle": "Why Querying Non-Partition Keys Can Bring Down a Production Cluster",
        "visual_html": """
        <div style="background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; border-radius: 12px; padding: 22px; margin-top: 10px;">
          <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <span style="font-size: 28px;">🔥</span>
            <div>
              <div style="font-size: 16px; font-weight: 800; color: #f87171;">THE DANGEROUS CASSANDRA ANTI-PATTERN</div>
              <div style="font-family: monospace; font-size: 13px; color: #fca5a5; margin-top: 2px;">
                SELECT * FROM users WHERE email = 'alice@example.com' ALLOW FILTERING;
              </div>
            </div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
            <div style="background: #1e293b; padding: 14px; border-radius: 8px; font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              <strong style="color: #60a5fa;">Partition Key (The Right Way):</strong> Cassandra hashes the primary key (e.g., <code>user_id</code>) to route directly to exactly 1 server. Instant <em>O</em>(1) lookup.
            </div>
            <div style="background: #1e293b; padding: 14px; border-radius: 8px; font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              <strong style="color: #f87171;">ALLOW FILTERING (The Wrong Way):</strong> Cassandra has no index on <code>email</code>. It must broadcast to <strong>EVERY server in the cluster</strong> and scan EVERY SSTable on disk!
            </div>
          </div>
          <div style="margin-top: 16px; text-align: center; font-size: 13px; color: #fecaca; font-weight: 700;">
            ⚠️ Consequence: Cluster-wide CPU spikes, disk thrashing, and client query timeouts!
          </div>
        </div>
        """,
        "key_points": [
          "Cassandra is designed strictly for Partition Key queries via consistent hashing.",
          "Using `ALLOW FILTERING` on non-partition keys forces every node across the cluster to perform full table scans.",
          "If you need arbitrary filtering across fields, Cassandra is the wrong tool—you need Elasticsearch."
        ],
        "script_en": "Because Cassandra is so fast at key lookups, developers often fall into a deadly trap: using ALLOW FILTERING. When you query by primary key, Cassandra routes to exactly one node. But when you filter by a non-key column like email with ALLOW FILTERING, the cluster broadcasts to every single node, forcing every node to scan all its SSTables. This causes cluster-wide latency spikes and timeouts.",
        "script_vi": "Vì Cassandra đọc khóa chính rất nhanh nên các lập trình viên thường mắc phải một sai lầm chết người: lạm dụng ALLOW FILTERING. Khi truy vấn theo khóa chính, hệ thống định tuyến chính xác tới 1 nút. Nhưng khi lọc theo cột phụ như email bằng ALLOW FILTERING, điều phối viên buộc phải phát tán truy vấn tới mọi nút trong cụm, ép tất cả quét toàn bộ SSTable. Hậu quả là nghẽn CPU và sập cụm diện rộng."
    }
]

print("Part 2 slides created.")


# Part 3: Inverted Index & Elasticsearch (Slides 14-20)

PART_3_SLIDES = [
    {
        "id": "slide-14",
        "section": "03 Inverted Index & ES",
        "badge": "Analogy Step 1",
        "title": "Textbook Analogy: Searching Without an Index",
        "subtitle": "Step 1: Reading Every Single Word to Find One Topic — The Exhausting Linear Scan",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div class="book-mockup">
            <div class="book-spine"></div>
            <div class="laser-bar"></div>
            <div style="font-size: 12px; color: #94a3b8; font-weight: 700; margin-left: 16px;">
              📖 500-PAGE TEXTBOOK: SCANNING PAGE BY PAGE
            </div>
            <div class="book-lines">
              <div class="book-line"></div>
              <div class="book-line medium"></div>
              <div class="book-line short"></div>
              <div class="book-line"></div>
              <div class="book-line medium"></div>
            </div>
            <div style="margin-left: 16px; background: rgba(244, 63, 94, 0.2); border: 1px solid #f43f5e; border-radius: 6px; padding: 6px 12px; font-size: 12px; color: #fca5a5; font-family: monospace;">
              Page 1... Page 2... Page 350... -> Linear scan is exhausting!
            </div>
          </div>
          <div>
            <div style="background: rgba(244, 63, 94, 0.15); border-left: 4px solid #f43f5e; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #fb7185;">Linear Scan: 3,080 µs</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">
                <strong>Linear Scan (Brute-Force Scan):</strong> Reading word-by-word through every page from start to finish.
              </div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Exhausting Effort:</strong> Even for just 1,655 quotes, reading every word takes 3,080 µs.<br/>
              • <strong>Scales Poorly:</strong> On a million documents, this linear search crawls from milliseconds to full minutes.<br/>
              • <strong>No Reusability:</strong> Every new search starts from scratch—none of the previous reading work is saved!
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Without an index, finding a word requires reading through every page from start to finish.",
          "Our benchmark shows a linear scan takes 3,080 µs across just 1,655 short quotes.",
          "As document collections grow to millions of records, linear scanning becomes completely unusable."
        ],
        "script_en": "Now let us turn to search. Imagine you are handed a 500-page computer science textbook and asked to find every page mentioning 'database'. If the book has no index, you have to read page 1, page 2, all the way to page 500. In computer science, this is a Linear Scan. In our benchmarks, scanning just 1,655 quotes took over 3,000 microseconds, and it gets exponentially worse as data grows.",
        "script_vi": "Bây giờ chúng ta chuyển sang bài toán tìm kiếm. Hãy tưởng tượng bạn cầm một cuốn giáo trình 500 trang và cần tìm xem từ 'database' xuất hiện ở những trang nào. Nếu sách không có mục lục, bạn buộc phải đọc từ trang 1 đến trang 500. Trong khoa học máy tính, đó là Quét tuyến tính (Linear Scan). Trong thực nghiệm của nhóm, quét chỉ 1.655 câu danh ngôn đã tốn hơn 3.000 micro-giây, và thời gian sẽ tăng vọt khi dữ liệu lớn lên."
    },
    {
        "id": "slide-15",
        "section": "03 Inverted Index & ES",
        "badge": "Analogy Step 2",
        "title": "Textbook Analogy: The Book Index Solution",
        "subtitle": "Step 2: How Flipping to the Back-of-the-Book Speeds Up Search by 280×",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div class="book-mockup" style="background: linear-gradient(135deg, #0f2b2e, #091a1c); border-color: #06b6d4;">
            <div class="book-spine" style="background: #041214;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-left: 16px;">
              <span style="font-size: 13px; font-weight: 800; color: #22d3ee;">📚 BACK OF BOOK: INVERTED INDEX</span>
              <span class="index-letter-badge">D</span>
            </div>
            <div style="margin-left: 16px; display: flex; flex-direction: column; gap: 8px;">
              <div class="index-entry-card">
                <span style="color: #67e8f9; font-weight: 800; font-family: monospace;">"database"</span>
                <span style="color: #94a3b8; font-size: 12px; margin-left: 8px;">➔ [Pages: 14, 45, 102, 380]</span>
              </div>
              <div style="background: #1e293b; border-radius: 6px; padding: 8px 12px; font-size: 12px;">
                <span style="color: #94a3b8; font-family: monospace;">"distributed"</span>
                <span style="color: #64748b; margin-left: 8px;">➔ [Pages: 14, 88, 102, 412]</span>
              </div>
            </div>
            <div style="margin-left: 16px; font-size: 12px; color: #34d399; font-weight: 700;">
              ✓ Instant Jump! Never read pages 1 to 13!
            </div>
          </div>
          <div>
            <div style="background: rgba(6, 182, 212, 0.15); border-left: 4px solid #06b6d4; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #22d3ee;">Direct Jump: 280× Faster</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">Search time drops from 3,080 µs down to 11 µs!</div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Inverted Index:</strong> Reverses the catalog direction: instead of <code>Document -> Words</code>, it maps <code>Word -> List of Document IDs</code>.<br/>
              • <strong>Posting List:</strong> The sorted list of document IDs containing that word (e.g., Pages 14, 45, 102).<br/>
              • <strong>Direct Jump:</strong> The search engine jumps straight to matching documents without looking at any other pages.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Human readers flip to the index at the back of the book where terms are sorted alphabetically.",
          "An Inverted Index maps each word directly to the exact page or document numbers where it appears.",
          "Our benchmark confirms search time drops from 3,080 µs down to 11 µs—a 280× speedup."
        ],
        "script_en": "What does a human reader actually do? You flip to the index at the back of the book. Under letter 'D', you see 'database: pages 14, 45, 102'. You immediately turn to page 14 without ever looking at the other 490 pages. This is the Inverted Index. Instead of mapping Document to Words, it inverts the relationship to map Words to Documents. In our benchmark, this yields a 280-fold speedup.",
        "script_vi": "Người đọc thực tế sẽ làm gì? Bạn lật ngay ra phần mục lục tra cứu ở cuối sách. Dưới mục chữ 'D', bạn thấy 'database: trang 14, 45, 102'. Bạn mở ngay trang 14 mà không cần đụng tới 490 trang còn lại. Đó chính là Chỉ mục đảo (Inverted Index). Thay vì lưu Tài liệu trỏ đến Từ ngữ, nó đảo ngược lại: Từ ngữ trỏ đến Danh sách mã tài liệu. Trong thực nghiệm, điều này giúp tăng tốc 280 lần."
    },
    {
        "id": "slide-16",
        "section": "03 Inverted Index & ES",
        "badge": "Word Cleanup",
        "title": "Text Analysis: The Word Cleanup Factory",
        "subtitle": "Step 3: How Elasticsearch Transforms Raw Text into Searchable Tokens",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px; margin-top: 10px;">
          <div style="font-size: 13px; font-weight: 700; color: #94a3b8; margin-bottom: 12px;">
            LUCENE TEXT ANALYSIS PIPELINE (3-STAGE ASSEMBLY LINE)
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; align-items: center; text-align: center;">
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #475569;">
              <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">RAW TEXT</div>
              <div style="font-size: 12px; color: #fca5a5; font-family: monospace; margin-top: 6px;">
                "&lt;b&gt;Databases!&lt;/b&gt;"
              </div>
            </div>
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #3b82f6;">
              <div style="font-size: 11px; color: #60a5fa; font-weight: 700;">1. CHAR FILTER</div>
              <div style="font-size: 12px; color: #cbd5e1; font-family: monospace; margin-top: 6px;">
                Strip HTML: "Databases!"
              </div>
            </div>
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #3b82f6;">
              <div style="font-size: 11px; color: #60a5fa; font-weight: 700;">2. TOKENIZER</div>
              <div style="font-size: 12px; color: #cbd5e1; font-family: monospace; margin-top: 6px;">
                Split words: ["Databases"]
              </div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.2); padding: 12px; border-radius: 8px; border: 2px solid #10b981;">
              <div style="font-size: 11px; color: #34d399; font-weight: 700;">3. TOKEN FILTER</div>
              <div style="font-size: 12px; color: #6ee7b7; font-family: monospace; margin-top: 6px;">
                Lowercase & Stem: <strong>"databas"</strong>
              </div>
            </div>
          </div>
          <div style="margin-top: 16px; font-size: 12.5px; color: #cbd5e1; text-align: center; line-height: 1.5;">
            <strong>Stemming:</strong> Trimming suffixes so searches for 'databases', 'database', or 'databased' all match the root word 'databas'.<br/>
            Both stored documents at index-time AND user search queries pass through this identical pipeline.
          </div>
        </div>
        """,
        "key_points": [
          "Before words enter the index, they pass through a 3-stage analysis pipeline.",
          "Character Filter removes markup; Tokenizer splits words; Token Filter lowercases and trims word suffixes (stemming).",
          "Because search queries undergo identical processing, searches match root meanings regardless of plurals or casing."
        ],
        "script_en": "How does raw text become an index? Lucene runs every string through an analysis conveyor belt. First, Character Filters strip HTML tags. Second, the Tokenizer splits text on spaces and punctuation into word tokens. Third, Token Filters convert everything to lowercase and apply Porter Stemming, turning 'Databases' into its root 'databas'. Queries undergo the exact same pipeline.",
        "script_vi": "Làm thế nào để văn bản thô biến thành chỉ mục? Lucene đưa chuỗi ký tự qua một dây chuyền phân tích 3 công đoạn. Bước 1, Bộ lọc ký tự loại bỏ các thẻ HTML. Bước 2, Bộ tách từ chia câu thành các từ đơn dựa theo dấu cách và dấu câu. Bước 3, Bộ lọc từ chuyển về chữ thường và rút gọn gốc từ bằng thuật toán Stemming, biến 'Databases' thành 'databas'. Truy vấn của người dùng cũng đi qua đúng dây chuyền này."
    },
    {
        "id": "slide-17",
        "section": "03 Inverted Index & ES",
        "badge": "Fast Intersection",
        "title": "Finding Multiple Words: Skip Pointers",
        "subtitle": "Step 4: Intersecting Multi-Term Boolean Queries Without Reading Every Document",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 22px; margin-top: 10px;">
          <div style="font-size: 13px; font-weight: 800; color: #38bdf8; margin-bottom: 12px;">
            BOOLEAN SEARCH QUERY: "write" AND "search"
          </div>
          <div style="margin-bottom: 18px;">
            <div style="font-size: 11.5px; color: #94a3b8; margin-bottom: 6px;">Word 'write' Posting List:</div>
            <div class="railway-track">
              <div class="doc-station">D1</div>
              <div class="doc-station">D3</div>
              <div class="doc-station">D12</div>
              <div class="doc-station">D25</div>
              <div class="doc-station match">D60</div>
              <div class="doc-station">D88</div>
            </div>
          </div>
          <div>
            <div style="font-size: 11.5px; color: #94a3b8; margin-bottom: 6px;">Word 'search' Posting List (With Skip Pointers every 8 docs):</div>
            <div class="railway-track" style="border-color: #06b6d4;">
              <div class="doc-station">D2</div>
              <div style="color: #06b6d4; font-size: 18px; font-weight: 900; animation: leapJump 2s infinite;">↷ LEAP OVER 57 DOCS ↷</div>
              <div class="doc-station match">D60</div>
              <div class="doc-station">D94</div>
            </div>
          </div>
          <div style="margin-top: 16px; font-size: 12.5px; color: #6ee7b7; text-align: center; font-weight: 700;">
            ✓ Instant Match Found at Doc 60 in 13.38 µs! Zero linear traversal of skipped items!
          </div>
        </div>
        """,
        "key_points": [
          "For multi-word AND queries, Elasticsearch intersects sorted arrays of document IDs.",
          "Skip pointers embed express highway shortcuts ahead in the posting list.",
          "If one list is at Doc 60, it leaps over dozens of intermediate IDs on the second list in <em>O</em>(1) time."
        ],
        "script_en": "What happens when you search for 'write AND search'? Lucene retrieves the sorted posting lists for both words. Instead of checking every document ID one by one, Lucene uses Skip Pointers—express lane bridges embedded in the posting list. If list A is at Doc 60, list B can leapfrog past 50 documents instantly. This brings intersection time down to 13 microseconds.",
        "script_vi": "Điều gì xảy ra khi bạn tìm kiếm 'write AND search'? Lucene lấy ra hai danh sách mã tài liệu đã được sắp xếp tăng dần. Thay vì so khớp từng phần tử, Lucene sử dụng Skip Pointer — như các cây cầu vượt cao tốc trong danh sách. Nếu danh sách A đang ở Tài liệu 60, danh sách B có thể nhảy cóc qua 50 tài liệu trung gian chỉ trong 1 bước nhảy. Nhờ đó phép giao hoàn thành trong 13 micro-giây."
    },
    {
        "id": "slide-18",
        "section": "03 Inverted Index & ES",
        "badge": "Relevance Ranking",
        "title": "Okapi BM25: The 3 Rules of Relevance",
        "subtitle": "Step 5: How Elasticsearch Knows Which Document is Actually the Best Match",
        "visual_html": """
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 10px;">
          <div style="background: #1e293b; border-top: 4px solid #3b82f6; border-radius: 8px; padding: 18px;">
            <div style="font-size: 24px; margin-bottom: 6px;">💎</div>
            <div style="font-size: 14px; font-weight: 800; color: #60a5fa;">1. Rare Words Win</div>
            <div style="font-size: 12px; color: #93c5fd; font-family: monospace; margin: 4px 0;">Inverse Document Freq (IDF)</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-top: 8px;">
              Common words like <em>"the"</em> or <em>"is"</em> get zero points. Rare words like <em>"Cassandra"</em> carry massive scoring weight.
            </p>
          </div>

          <div style="background: #1e293b; border-top: 4px solid #f59e0b; border-radius: 8px; padding: 18px;">
            <div style="font-size: 24px; margin-bottom: 6px;">🛡️</div>
            <div style="font-size: 14px; font-weight: 800; color: #fbbf24;">2. Anti-Spam Ceiling</div>
            <div style="font-size: 12px; color: #fde68a; font-family: monospace; margin: 4px 0;">TF Saturation (k₁ = 1.2)</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-top: 8px;">
              Repeating <em>"database"</em> 50 times in a blog post will NOT give you 50x points. The score tops out at an asymptotic limit.
            </p>
          </div>

          <div style="background: #1e293b; border-top: 4px solid #10b981; border-radius: 8px; padding: 18px;">
            <div style="font-size: 24px; margin-bottom: 6px;">⚖️</div>
            <div style="font-size: 14px; font-weight: 800; color: #34d399;">3. Short & Punchy</div>
            <div style="font-size: 12px; color: #a7f3d0; font-family: monospace; margin: 4px 0;">Length Penalty (b = 0.75)</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-top: 8px;">
              Finding a word in a short 10-word sentence is much more relevant than finding it buried in a 10,000-word book.
            </p>
          </div>
        </div>
        """,
        "key_points": [
          "Okapi BM25 is the probabilistic ranking formula powering modern Elasticsearch and Lucene.",
          "Rule 1 (IDF): Penalizes common words, rewards rare terms.",
          "Rule 2 (TF Saturation): Prevents keyword spamming; Rule 3 (Length Penalty): Normalizes document length."
        ],
        "script_en": "Finding matching documents is only half the battle; which document should be at the top? Elasticsearch uses Okapi BM25, governed by three intuitive rules. Rule 1: Rare words win—if you search 'the database', 'database' gets all the points. Rule 2: Anti-spam ceiling—mentioning a word 50 times does not give 50 times the score; it tops out. Rule 3: Short and punchy—a match in a short headline scores higher than in a giant document.",
        "script_vi": "Tìm thấy tài liệu chỉ mới là một nửa chặng đường; tài liệu nào xứng đáng đứng đầu? Elasticsearch sử dụng thuật toán Okapi BM25 với 3 nguyên tắc trực quan. Nguyên tắc 1: Từ hiếm có giá trị cao — từ phổ biến như 'the' nhận 0 điểm, từ chuyên biệt như 'database' nhận trọn điểm số. Nguyên tắc 2: Chống gian lận từ khóa — lặp lại 50 lần không mang lại 50 lần điểm mà bị chặn trên bởi tiệm cận. Nguyên tắc 3: Ngắn gọn được ưu tiên — từ khóa xuất hiện trong tiêu đề ngắn được đánh giá cao hơn nằm lẫn trong một cuốn sách dày."
    },
    {
        "id": "slide-19",
        "section": "03 Inverted Index & ES",
        "badge": "Formula Decoded",
        "title": "Okapi BM25: The Math Made Simple",
        "subtitle": "Step 6: Understanding the Mathematical Formula Behind Relevance Scoring",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 22px; margin-top: 10px;">
          <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 18px; text-align: center;">
            <div style="font-family: 'Cambria Math', 'DejaVu Sans', serif; font-size: 18px; color: #38bdf8; font-weight: 700; letter-spacing: 0.5px;">
              Score(<em>D</em>, <em>Q</em>) = ∑ <span style="color:#60a5fa;">IDF(<em>q</em>)</span> × [ <sup><em>tf</em> × (<span style="color:#fbbf24;"><em>k</em><sub>1</sub></span> + 1)</sup> / <sub><em>tf</em> + <span style="color:#fbbf24;"><em>k</em><sub>1</sub></span> × (1 − <span style="color:#34d399;"><em>b</em></span> + <span style="color:#34d399;"><em>b</em></span> × |<em>D</em>| / avgdl)</sub> ]
            </div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 18px;">
            <div style="background: #1e293b; padding: 12px; border-radius: 6px; font-size: 12.5px; border-left: 3px solid #fbbf24; line-height: 1.5;">
              <strong style="color: #fbbf24;">Parameter <em>k</em><sub>1</sub> = 1.2 (TF Saturation):</strong><br/>
              Controls how fast term frequency score tops out. As <em>tf</em> increases, score approaches <em>k</em><sub>1</sub> + 1 = 2.2. Prevents SEO keyword spamming.
            </div>
            <div style="background: #1e293b; padding: 12px; border-radius: 6px; font-size: 12.5px; border-left: 3px solid #34d399; line-height: 1.5;">
              <strong style="color: #34d399;">Parameter <em>b</em> = 0.75 (Length Penalty):</strong><br/>
              Penalizes documents longer than the average document length (|<em>D</em>| > avgdl). When <em>b</em> = 1, fully scales by length; when <em>b</em> = 0, length is ignored.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "The BM25 formula calculates a continuous relevance score for ranking query results.",
          "Parameter <em>k</em><sub>1</sub> = 1.2 prevents keyword stuffing by placing an asymptotic ceiling on frequency.",
          "Parameter <em>b</em> = 0.75 balances document length against average corpus length."
        ],
        "script_en": "Here is the exact mathematical equation of Okapi BM25. It sums the Inverse Document Frequency of each query term multiplied by a bounded term frequency curve. The parameter k1 set to 1.2 controls the saturation ceiling, and parameter b set to 0.75 controls the length penalty. In our live demo, this ranks the most relevant database quote at 1.92, cleanly separating it from lower-quality matches.",
        "script_vi": "Đây là công thức toán học chính xác của Okapi BM25. Điểm số là tổng nghịch đảo tần suất tài liệu (IDF) của từng từ nhân với đường cong bão hòa tần suất xuất hiện. Tham số k1 bằng 1.2 kiểm soát trần bão hòa chống spam, và tham số b bằng 0.75 kiểm soát mức độ phạt độ dài văn bản. Trong demo trực tiếp, công thức này chấm cho câu trích dẫn chuẩn nhất 1.92 điểm, tách biệt hoàn toàn khỏi các kết quả mờ nhạt khác."
    },
    {
        "id": "slide-20",
        "section": "03 Inverted Index & ES",
        "badge": "The Hidden Cost",
        "title": "The Cost of Fast Search: 15× Memory Penalty",
        "subtitle": "Step 7: The RUM Trade-Off — Paying with High RAM to Achieve Microsecond Search",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px;">
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #06b6d4; font-weight: 700;">Elasticsearch Inverted Index</span>
                <span style="color: #06b6d4; font-weight: 700;">2,293 Bytes / Doc</span>
              </div>
              <div style="height: 16px; background: #1e293b; border-radius: 8px; overflow: hidden;">
                <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #06b6d4, #22d3ee);"></div>
              </div>
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #60a5fa; font-weight: 700;">Cassandra LSM Primary Index</span>
                <span style="color: #60a5fa; font-weight: 700;">154 Bytes / Key</span>
              </div>
              <div style="height: 16px; background: #1e293b; border-radius: 8px; overflow: hidden;">
                <div style="width: 6.7%; height: 100%; background: #3b82f6;"></div>
              </div>
            </div>
            <div style="margin-top: 18px; font-size: 12px; color: #f59e0b; text-align: center; font-weight: 700;">
              Elasticsearch requires ~15× more memory per record than Cassandra!
            </div>
          </div>
          <div>
            <div style="background: rgba(6, 182, 212, 0.15); border-left: 4px solid #06b6d4; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #22d3ee;">Memory Amplification</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">
                <strong>Memory Amplification:</strong> Extra RAM consumed to maintain in-memory dictionaries and posting lists.
              </div>
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Multiple Words per Doc:</strong> Each document produces 50 to 500 separate word entries.<br/>
              • <strong>In-Memory Dictionaries:</strong> Lucene keeps the entire word dictionary loaded in RAM for speed.<br/>
              • <strong>The Trade-Off:</strong> Microsecond search speed is paid for with massive RAM consumption.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "An Inverted Index stores every unique word in a document, multiplying index memory overhead.",
          "Our empirical measurements show Elasticsearch requires 2,293 bytes/doc vs Cassandra's 154 bytes/key.",
          "This 15× memory amplification is the physical trade-off demanded by the RUM Conjecture."
        ],
        "script_en": "There is no free lunch in computer science. To achieve 11-microsecond search times, Elasticsearch pays an enormous price in memory. While Cassandra needs only 154 bytes per key in RAM, Elasticsearch requires nearly 2,300 bytes per document to store posting lists and term dictionaries. That is a 15-to-1 memory ratio, perfectly illustrating the RUM Conjecture.",
        "script_vi": "Không có bữa trưa nào miễn phí trong khoa học máy tính. Để đạt được tốc độ tìm kiếm 11 micro-giây, Elasticsearch phải trả giá đắt bằng dung lượng RAM. Trong khi Cassandra chỉ tốn 154 byte cho mỗi khóa trên RAM, Elasticsearch cần tới gần 2.300 byte cho mỗi tài liệu để duy trì danh sách posting và từ điển thuật ngữ. Tỷ lệ chênh lệch bộ nhớ 15 lần này là minh chứng hoàn hảo cho Giả thuyết RUM."
    }
]

print("Part 3 slides created.")


# Part 4: Synthesis, Experiments, Architecture, Takeaways & Goodbye (Slides 21-32)

PART_4_SLIDES = [
    {
        "id": "slide-21",
        "section": "04 Synthesis",
        "badge": "Comparison Matrix",
        "title": "Comparing Both Systems: The 5W1H Matrix",
        "subtitle": "A Plain-English Breakdown Across 6 Key Architectural Questions",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 18px; margin-top: 10px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 12px; color: #cbd5e1;">
            <thead>
              <tr style="border-bottom: 2px solid #374151; text-align: left;">
                <th style="padding: 6px 10px; color: #94a3b8;">Question</th>
                <th style="padding: 6px 10px; color: #60a5fa;">Apache Cassandra (LSM)</th>
                <th style="padding: 6px 10px; color: #22d3ee;">Elasticsearch (Inverted Index)</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f59e0b;">What?</td>
                <td style="padding: 6px 10px;">Distributed wide-column database (stores rows by key)</td>
                <td style="padding: 6px 10px;">Distributed search engine (indexes every word inside text)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f59e0b;">Why?</td>
                <td style="padding: 6px 10px;">Extreme write speed with zero downtime</td>
                <td style="padding: 6px 10px;">Instant multi-word search with relevance ranking</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f59e0b;">Who?</td>
                <td style="padding: 6px 10px;">High-speed logging, IoT sensor streams, transactions</td>
                <td style="padding: 6px 10px;">E-commerce product search, site search, log analytics (ELK)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f59e0b;">Where?</td>
                <td style="padding: 6px 10px;">The Bank Vault (System of Record / Source of Truth)</td>
                <td style="padding: 6px 10px;">The Storefront Window (Search Accelerator / User Catalog)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f59e0b;">When?</td>
                <td style="padding: 6px 10px;">Queries specify the exact Partition Key (<em>O</em>(1) routing)</td>
                <td style="padding: 6px 10px;">Queries search for words or filter across multiple fields</td>
              </tr>
              <tr>
                <td style="padding: 6px 10px; font-weight: 700; color: #f59e0b;">How?</td>
                <td style="padding: 6px 10px;">MemTable (RAM) + CommitLog (Disk) + SSTables (Read-only)</td>
                <td style="padding: 6px 10px;">Word Dictionary + Posting Lists + Skip Pointers + BM25</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "key_points": [
          "The 5W1H framework clearly organizes the contrasting design goals of both technologies.",
          "Cassandra acts as the primary System of Record for high-speed write workloads.",
          "Elasticsearch acts as a secondary search accelerator for rich query filters."
        ],
        "script_en": "To synthesize both technologies, we apply the 5W1H framework. Cassandra's 'What' is a distributed wide-column store for high-throughput appends where queries always provide the partition key. Elasticsearch's 'What' is a distributed search engine for ad-hoc multi-term queries with relevance scoring. Cassandra is the secure bank vault; Elasticsearch is the searchable storefront display.",
        "script_vi": "Để tổng hợp hai công nghệ, chúng em áp dụng khung phân tích 5W1H. 'Cái gì' của Cassandra là cơ sở dữ liệu phân tán tối ưu cho luồng ghi cực lớn với điều kiện truy vấn luôn có khóa phân vùng. 'Cái gì' của Elasticsearch là bộ máy tìm kiếm phục vụ các truy vấn đa trường bất kỳ kèm xếp hạng điểm liên quan. Cassandra đóng vai trò két sắt lưu trữ dữ liệu gốc; Elasticsearch là gian hàng trưng bày cho khách tìm kiếm."
    },
    {
        "id": "slide-22",
        "section": "04 Synthesis",
        "badge": "Physical Law",
        "title": "The Trade-Off Space: RUM Conjecture",
        "subtitle": "Why Neither Engine Can Replace the Other (Opposite Design Choices)",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; font-weight: 700; color: #94a3b8; margin-bottom: 12px;">RUM CONJECTURE PROFILE</div>
            <div style="background: #0f172a; border-radius: 8px; padding: 16px; border: 1px solid #1e293b;">
              <div style="font-size: 14px; font-weight: 800; color: #06b6d4; margin-bottom: 8px;">
                Elasticsearch: Minimized Read (R)
              </div>
              <div style="font-size: 12px; color: #94a3b8; margin-bottom: 16px;">
                High Update overhead (U) & High Memory (M)
              </div>
              <div style="font-size: 14px; font-weight: 800; color: #60a5fa; margin-bottom: 8px;">
                Cassandra: Minimized Update (U) + Memory (M)
              </div>
              <div style="font-size: 12px; color: #94a3b8;">
                Sacrifices Read overhead (R), reclaimed via Bloom Filters
              </div>
            </div>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 4px; margin-bottom: 12px;">
              <strong style="color: #60a5fa;">The Architectural Law:</strong> A single storage engine cannot occupy both corners simultaneously without internal partitioning.
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
              • <strong>Cassandra:</strong> Writes fast by postponing sorting to background compaction threads.<br/>
              • <strong>Elasticsearch:</strong> Searches fast by tokenizing and sorting word lists upfront.<br/>
              • <strong>Conclusion:</strong> Complementary teammates, not competitors.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Cassandra occupies the Update-Memory corner of RUM space.",
          "Elasticsearch occupies the Read-optimization corner of RUM space.",
          "The RUM Conjecture mathematically proves that neither engine can replace the other."
        ],
        "script_en": "When we map both engines onto the RUM Conjecture triangle, their complementary nature becomes crystal clear. Cassandra prioritizes Update and Memory overhead; Elasticsearch prioritizes Read latency. No engineer can break this law; choosing an engine is fundamentally choosing which corner of the trade-off space your application requires.",
        "script_vi": "Khi định vị hai bộ máy lên tam giác Giả thuyết RUM, bản chất bổ trợ lẫn nhau của chúng hiện ra rõ nét. Cassandra ưu tiên chi phí Ghi và Bộ nhớ; Elasticsearch ưu tiên độ trễ Đọc. Không một kỹ sư nào có thể phá vỡ định luật này; việc chọn storage engine thực chất là việc bạn chọn đánh đổi góc nào trong không gian thiết kế."
    },
    {
        "id": "slide-23",
        "section": "05 Experiments",
        "badge": "Methodology",
        "title": "Experimental Setup: Pure Reference Engines",
        "subtitle": "Building Clean, Zero-Dependency Prototypes to Measure Pure Storage Mechanics",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px;">
          <div style="background: #1e293b; border: 2px solid #3b82f6; border-radius: 10px; padding: 18px;">
            <div style="font-size: 16px; font-weight: 800; color: #60a5fa; margin-bottom: 8px;">
              🏛️ Cassandra Reference Engine
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>MemTable:</strong> In-memory sorted write buffer.<br/>
              • <strong>CommitLog:</strong> Sequential disk append with CRC32 checksums.<br/>
              • <strong>SSTable:</strong> Read-only binary key-value disk files.<br/>
              • <strong>Bloom Filter:</strong> In-memory bit array skipping absent files.<br/>
              • <strong>Compaction:</strong> Background merge-cleaner erasing tombstones.
            </div>
          </div>
          <div style="background: #1e293b; border: 2px solid #06b6d4; border-radius: 10px; padding: 18px;">
            <div style="font-size: 16px; font-weight: 800; color: #22d3ee; margin-bottom: 8px;">
              🔍 Elasticsearch Reference Engine
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>Analysis Pipeline:</strong> Strips HTML, tokenizes, and stems words.<br/>
              • <strong>Term Dictionary:</strong> In-memory word lookup catalog.<br/>
              • <strong>Posting Lists:</strong> Sorted arrays of document IDs.<br/>
              • <strong>Skip Pointers:</strong> Highway bridges for fast multi-word AND search.<br/>
              • <strong>Okapi BM25:</strong> Tunable relevance scoring (<em>k</em><sub>1</sub> = 1.2, <em>b</em> = 0.75).
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Built zero-dependency Python reference engines to isolate storage mechanics from network or JVM noise.",
          "Cassandra engine faithfully implements MemTable, CommitLog, SSTables, Bloom filters, and Tombstones.",
          "Elasticsearch engine implements the Analysis Pipeline, FST dictionaries, Skip Pointers, and BM25 scoring."
        ],
        "script_en": "To conduct rigorous scientific benchmarks, we implemented zero-dependency reference storage engines in pure Python. This eliminates network latency, operating system page cache noise, and JVM garbage collection artifacts. We implement every core mechanism from scratch: MemTables, immutable SSTables, Bloom filters, and compaction for Cassandra; and the analysis pipeline, skip pointers, and Okapi BM25 for Elasticsearch.",
        "script_vi": "Để thực hiện các đo đạc khoa học chính xác, chúng em tự xây dựng hai storage engine tham chiếu độc lập bằng Python thuần không phụ thuộc thư viện ngoài. Cách tiếp cận này loại bỏ hoàn toàn nhiễu từ độ trễ mạng hay dọn rác bộ nhớ của JVM. Chúng em cài đặt đầy đủ từ đầu: MemTable, SSTable bất biến, Bloom Filter và Compaction cho Cassandra; cùng dây chuyền phân tích từ, Skip Pointer và Okapi BM25 cho Elasticsearch."
    },
    {
        "id": "slide-24",
        "section": "05 Experiments",
        "badge": "Datasets & Qs",
        "title": "Test Datasets & Research Questions",
        "subtitle": "Testing Real Data Across 4 Concrete Hypotheses",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #374151; border-radius: 10px; padding: 18px;">
            <div style="font-size: 14px; font-weight: 800; color: #f59e0b; margin-bottom: 12px;">TEST DATASETS</div>
            <div style="margin-bottom: 14px;">
              <strong style="color: #60a5fa;">1. World Cities Dataset:</strong><br/>
              <span style="font-size: 12.5px; color: #cbd5e1;">N = 10,000 geographic records with unique primary keys. Ideal for testing write speed.</span>
            </div>
            <div>
              <strong style="color: #22d3ee;">2. Natural Quotes Corpus:</strong><br/>
              <span style="font-size: 12.5px; color: #cbd5e1;">N = 1,655 natural quotes with 5,820 words. Ideal for testing word search & BM25 ranking.</span>
            </div>
          </div>
          <div style="background: #111827; border: 2px solid #374151; border-radius: 10px; padding: 18px;">
            <div style="font-size: 14px; font-weight: 800; color: #38bdf8; margin-bottom: 12px;">RESEARCH QUESTIONS</div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>Q1 (Write Speed):</strong> Can Cassandra sustain >70k ops/sec even when flushing to disk?<br/>
              • <strong>Q2 (Bloom Filter Pruning):</strong> Does the Bloom filter skip 100% of absent key disk reads?<br/>
              • <strong>Q3 (Search Speedup):</strong> How many times faster is the inverted index than a linear scan?<br/>
              • <strong>Q4 (Memory Footprint):</strong> Exactly how much more RAM does an inverted index consume?
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Datasets include 10,000 structured geographic records and 1,655 natural language quotes.",
          "Q1 tests write scalability under periodic flushes; Q2 tests Bloom filter pruning efficiency.",
          "Q3 tests multi-term search speedup; Q4 quantifies the exact memory amplification ratio."
        ],
        "script_en": "We evaluate four explicit research questions across two real-world datasets: 10,000 world cities for primary key writes, and 1,655 natural language quotes for search. Q1 asks if Cassandra sustains write speed during flushes. Q2 investigates if Bloom filters eliminate disk reads on absent keys. Q3 quantifies the search speedup over linear scans, and Q4 measures the exact memory cost.",
        "script_vi": "Chúng em đặt ra 4 câu hỏi nghiên cứu cụ thể trên 2 tập dữ liệu thực tế: 10.000 thành phố trên thế giới cho bài kiểm tra ghi khóa chính, và 1.655 danh ngôn tự nhiên cho bài kiểm tra tìm kiếm. Q1 kiểm tra khả năng duy trì tốc độ ghi của Cassandra khi xả đĩa. Q2 đo hiệu quả loại trừ đọc đĩa của Bloom Filter. Q3 đo lường mức độ tăng tốc tìm kiếm, và Q4 tính toán tỷ lệ tiêu tốn bộ nhớ RAM."
    },
    {
        "id": "slide-25",
        "section": "05 Experiments",
        "badge": "Live Demo",
        "title": "Live Terminal Demo: Run It Yourself",
        "subtitle": "Verified Reproduction Commands for Terminal and Google Colab",
        "visual_html": """
        <div style="background: #090d16; border: 2px solid #10b981; border-radius: 12px; padding: 20px; font-family: monospace; margin-top: 10px;">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2937; padding-bottom: 8px; margin-bottom: 12px;">
            <span style="color: #34d399; font-weight: 800; font-size: 13px;">💻 LIVE CLI REPRODUCTION COMMANDS</span>
            <span style="color: #94a3b8; font-size: 11px;">STANDALONE & RUNNABLE</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 10px; font-size: 12.5px;">
            <div style="background: #111827; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #3b82f6;">
              <span style="color: #94a3b8;"># 1. Run Complete End-to-End Demo (Both Engines):</span><br/>
              <span style="color: #60a5fa; font-weight: 700;">python3 demo.py --no-pause</span>
            </div>
            <div style="background: #111827; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #38bdf8;">
              <span style="color: #94a3b8;"># 2. Run Cassandra LSM Mechanics Alone:</span><br/>
              <span style="color: #38bdf8; font-weight: 700;">python3 demo.py --cassandra --no-pause</span>
            </div>
            <div style="background: #111827; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #06b6d4;">
              <span style="color: #94a3b8;"># 3. Run Elasticsearch Search & BM25 Mechanics Alone:</span><br/>
              <span style="color: #22d3ee; font-weight: 700;">python3 demo.py --elasticsearch --no-pause</span>
            </div>
            <div style="background: #111827; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #10b981;">
              <span style="color: #94a3b8;"># 4. Run Automated Test Suite (100% Passing):</span><br/>
              <span style="color: #34d399; font-weight: 700;">python3 tests/test_all.py</span>
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Our presentation includes a live interactive checkpoint.",
          "Every theoretical claim is backed by a single runnable bash command.",
          "All tests pass cleanly with zero external third-party dependencies."
        ],
        "script_en": "At this point in the presentation, we switch to our live terminal checkpoint. With a single command, 'python3 demo.py --no-pause', the presentation audience can witness every step executing live: MemTable fills, SSTable flushes, Bloom filter fast-fails, and multi-term BM25 ranking across real datasets.",
        "script_vi": "Tại thời điểm này trong bài báo cáo, chúng em chuyển sang màn hình terminal để minh họa trực tiếp. Chỉ với một câu lệnh đơn giản 'python3 demo.py --no-pause', hội đồng có thể chứng kiến toàn bộ các bước hoạt động trong thực tế: nạp MemTable, xả SSTable, Bloom Filter loại trừ đọc đĩa và thuật toán BM25 xếp hạng văn bản trên dữ liệu thật."
    },
    {
        "id": "slide-26",
        "section": "06 Results",
        "badge": "Empirical Scorecard",
        "title": "Empirical Scorecard: 5-Round Results",
        "subtitle": "Statistical Measurements Across 5 Independent Benchmark Rounds (Mean ± Std Dev)",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 18px; margin-top: 10px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 12px; color: #cbd5e1;">
            <thead>
              <tr style="border-bottom: 2px solid #374151; text-align: left;">
                <th style="padding: 6px 10px; color: #94a3b8;">Metric</th>
                <th style="padding: 6px 10px; color: #60a5fa;">Apache Cassandra (LSM)</th>
                <th style="padding: 6px 10px; color: #22d3ee;">Elasticsearch (Inverted Index)</th>
                <th style="padding: 6px 10px; color: #f59e0b;">Speedup / Ratio</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700;">Ingestion Throughput</td>
                <td style="padding: 6px 10px; color: #60a5fa; font-weight: 700;">85,624 ± 6,126 ops/s</td>
                <td style="padding: 6px 10px; color: #22d3ee; font-weight: 700;">93,935 ± 3,385 docs/s</td>
                <td style="padding: 6px 10px;">Comparable</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700;">Point Lookup (Hit)</td>
                <td style="padding: 6px 10px; color: #34d399; font-weight: 700;">5.42 ± 0.27 µs</td>
                <td style="padding: 6px 10px; color: #94a3b8;">N/A (Requires Term Query)</td>
                <td style="padding: 6px 10px;">Instant Key Read</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700;">Negative Query (Miss)</td>
                <td style="padding: 6px 10px; color: #34d399; font-weight: 700;">3.42 ± 0.71 µs (Bloom)</td>
                <td style="padding: 6px 10px; color: #94a3b8;">N/A</td>
                <td style="padding: 6px 10px; color: #34d399; font-weight: 700;">37% Faster than Hit</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700;">Multi-Term Boolean AND</td>
                <td style="padding: 6px 10px; color: #f87171;">Unsupported (Full Scan)</td>
                <td style="padding: 6px 10px; color: #22d3ee; font-weight: 700;">20.36 ± 3.98 µs</td>
                <td style="padding: 6px 10px; color: #38bdf8; font-weight: 700;">71.5× vs Linear</td>
              </tr>
              <tr style="border-bottom: 1px solid #1f2937;">
                <td style="padding: 6px 10px; font-weight: 700;">Okapi BM25 Ranked Top-5</td>
                <td style="padding: 6px 10px; color: #f87171;">Unsupported</td>
                <td style="padding: 6px 10px; color: #22d3ee; font-weight: 700;">118.40 ± 15.83 µs</td>
                <td style="padding: 6px 10px;">Sub-millisecond</td>
              </tr>
              <tr>
                <td style="padding: 6px 10px; font-weight: 700;">Index Memory Footprint</td>
                <td style="padding: 6px 10px; color: #60a5fa; font-weight: 700;">153.7 Bytes / key</td>
                <td style="padding: 6px 10px; color: #f43f5e; font-weight: 700;">2,292.8 Bytes / doc</td>
                <td style="padding: 6px 10px; color: #f59e0b; font-weight: 700;">14.9× RAM Penalty</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "key_points": [
          "Statistical validation over 5 independent trials confirms all theoretical predictions.",
          "Cassandra delivers 85k ops/s write throughput with microsecond Bloom filter pruning.",
          "Elasticsearch delivers 20 µs multi-term searches at the cost of 15× higher RAM consumption."
        ],
        "script_en": "Here is our complete empirical scorecard, reporting sample mean and standard deviation over five repeated rounds after discarding warmup runs. The data confirms our theory: Cassandra achieves 85,000 writes/sec, and Bloom filter pruning drops negative lookups to 3.42 microseconds. Meanwhile, Elasticsearch executes multi-term intersections in 20 microseconds but consumes 15 times more RAM per record.",
        "script_vi": "Đây là bảng điểm thực nghiệm đầy đủ của chúng em, báo cáo giá trị trung bình mẫu và độ lệch chuẩn qua 5 lần chạy độc lập sau khi đã loại bỏ vòng khởi động. Số liệu khẳng định lý thuyết: Cassandra đạt 85.000 lượt ghi/giây và Bloom Filter giảm thời gian tìm khóa vắng mặt xuống 3,42 micro-giây. Trong khi đó, Elasticsearch thực hiện phép giao đa từ trong 20 micro-giây nhưng tốn gấp 15 lần bộ nhớ RAM cho mỗi bản ghi."
    },
    {
        "id": "slide-27",
        "section": "06 Results",
        "badge": "Proof 1 & 2",
        "title": "Proof 1: Write Speed & Bloom Pruning",
        "subtitle": "Answering Research Questions Q1 & Q2 With Statistical Evidence",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px;">
          <div style="background: #1e293b; border-left: 4px solid #3b82f6; border-radius: 8px; padding: 18px;">
            <div style="font-size: 15px; font-weight: 800; color: #60a5fa; margin-bottom: 8px;">
              Q1: Ingestion Scalability
            </div>
            <div style="font-size: 26px; font-weight: 900; color: #fff;">85,624 ops/s</div>
            <div style="font-size: 12px; color: #93c5fd; margin-top: 4px;">Standard Deviation: ±6,126 ops/s</div>
            <div style="margin-top: 12px; font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
              • Within MemTable buffer: Exceeds <strong>233,747 ops/s</strong>.<br/>
              • During background disk flushes: Smoothly amortizes at <strong>73,374 ops/s</strong> without write stalls.
            </div>
          </div>
          <div style="background: #1e293b; border-left: 4px solid #10b981; border-radius: 8px; padding: 18px;">
            <div style="font-size: 15px; font-weight: 800; color: #34d399; margin-bottom: 8px;">
              Q2: Bloom Filter Fast-Fail
            </div>
            <div style="font-size: 26px; font-weight: 900; color: #fff;">3.42 µs Latency</div>
            <div style="font-size: 12px; color: #a7f3d0; margin-top: 4px;">100% of SSTables Pruned on Disk</div>
            <div style="margin-top: 12px; font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
              • Tested across 1,000 non-existent keys.<br/>
              • Every single query aborted in RAM; exactly <strong>0 disk reads</strong> performed.<br/>
              • 37% faster than retrieving an existing record from disk.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Q1 Answer: Cassandra sustains high write throughput even as data spills from RAM to disk.",
          "Q2 Answer: Bloom filters achieve 100% pruning accuracy on non-existent keys.",
          "This proves that LSM write performance does not degrade point read latency on absent keys."
        ],
        "script_en": "Examining Questions 1 and 2 in detail: For Q1, Cassandra sustains an average of 85,000 operations per second across 10,000 records. For Q2, testing against 1,000 non-existent keys proved that the Bloom filter achieves 100% pruning efficiency. Not a single SSTable file was opened on disk, and the check completed in 3.42 microseconds.",
        "script_vi": "Phân tích chi tiết câu hỏi 1 và 2: Với Q1, Cassandra duy trì tốc độ ghi trung bình 85.000 thao tác/giây trên 10.000 bản ghi. Với Q2, thử nghiệm trên 1.000 khóa không tồn tại chứng minh Bloom Filter đạt hiệu suất loại trừ 100%. Không có bất kỳ file SSTable nào trên đĩa bị mở ra, và quá trình kiểm tra hoàn tất chỉ trong 3,42 micro-giây."
    },
    {
        "id": "slide-28",
        "section": "06 Results",
        "badge": "Proof 3 & 4",
        "title": "Proof 2: Search Speedup & Memory Cost",
        "subtitle": "Answering Research Questions Q3 & Q4 With Measured Benchmarks",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px;">
          <div style="background: #1e293b; border-left: 4px solid #06b6d4; border-radius: 8px; padding: 18px;">
            <div style="font-size: 15px; font-weight: 800; color: #22d3ee; margin-bottom: 8px;">
              Q3: Search Acceleration
            </div>
            <div style="font-size: 26px; font-weight: 900; color: #fff;">71.5× – 280× Speedup</div>
            <div style="font-size: 12px; color: #67e8f9; margin-top: 4px;">20.36 µs vs 2,515 µs Linear Scan</div>
            <div style="margin-top: 12px; font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
              • Boolean query <code>'life' AND 'man'</code> evaluated in <strong>20.36 µs</strong>.<br/>
              • Linear scan required inspecting all 1,655 document strings byte-by-byte.<br/>
              • Gap widens by orders of magnitude as corpus size scales to millions.
            </div>
          </div>
          <div style="background: #1e293b; border-left: 4px solid #f43f5e; border-radius: 8px; padding: 18px;">
            <div style="font-size: 15px; font-weight: 800; color: #fb7185; margin-bottom: 8px;">
              Q4: Memory Footprint Penalty
            </div>
            <div style="font-size: 26px; font-weight: 900; color: #fff;">14.9× RAM Overhead</div>
            <div style="font-size: 12px; color: #fca5a5; margin-top: 4px;">2,292.8 B/doc vs 153.7 B/key</div>
            <div style="margin-top: 12px; font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
              • Cassandra index overhead: 1.53 MB for 10,000 keys.<br/>
              • Elasticsearch index overhead: 3.79 MB for just 1,655 documents.<br/>
              • Confirms the RUM Conjecture: sub-millisecond search requires massive memory.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Q3 Answer: The inverted index delivers a 71× to 280× speedup over brute-force scanning.",
          "Q4 Answer: The memory penalty is exactly 14.9×, verifying the physical cost of precomputing search indexes.",
          "These empirical findings confirm the theoretical trade-offs described in modern academic literature."
        ],
        "script_en": "Turning to Questions 3 and 4: For Q3, evaluating multi-term queries with posting lists was over 70 times faster than a brute-force scan on a small dataset, with the gap growing even larger at scale. For Q4, our memory measurements revealed an exact 14.9-to-1 memory amplification ratio. Elasticsearch buys search speed directly with RAM.",
        "script_vi": "Chuyển sang câu hỏi 3 và 4: Với Q3, việc xử lý truy vấn giao từ bằng posting list nhanh hơn quét vét cạn trên 70 lần ngay trên tập dữ liệu nhỏ, và khoảng cách này sẽ tăng theo cấp số nhân ở quy mô triệu bản ghi. Với Q4, đo đạc bộ nhớ cho thấy hệ số tiêu tốn RAM chính xác là 14.9 lần. Elasticsearch mua tốc độ tìm kiếm trực tiếp bằng dung lượng RAM."
    },
    {
        "id": "slide-29",
        "section": "07 Architecture",
        "badge": "Mental Model",
        "title": "Production Architecture: Bank Vault vs. Storefront",
        "subtitle": "How to Combine Both Systems in a Real Application Without Conflict",
        "visual_html": """
        <div class="dual-system-grid" style="margin-top: 10px;">
          <div class="system-box vault">
            <div style="font-size: 32px; margin-bottom: 6px;">🏦</div>
            <div style="font-size: 18px; font-weight: 800; color: #f59e0b;">THE BANK VAULT</div>
            <div style="font-size: 12px; color: #fde68a; font-family: monospace; margin: 4px 0;">Apache Cassandra (System of Record)</div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5; margin-top: 10px; text-align: left;">
              • Strict source of truth for transactional data.<br/>
              • Accepts high-frequency sensor & ledger writes.<br/>
              • Zero risk of index corruption or re-index downtime.
            </div>
          </div>

          <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
            <div style="font-size: 12px; font-weight: 800; color: #34d399;">Kafka / CDC</div>
            <div style="width: 60px; height: 10px; background: repeating-linear-gradient(45deg, #10b981, #10b981 10px, #059669 10px, #059669 20px); border-radius: 4px; animation: conveyorMove 2s linear infinite;"></div>
            <div style="font-size: 11px; color: #94a3b8;">Asynchronous Replication</div>
          </div>

          <div class="system-box storefront">
            <div style="font-size: 32px; margin-bottom: 6px;">🏬</div>
            <div style="font-size: 18px; font-weight: 800; color: #22d3ee;">THE STOREFRONT WINDOW</div>
            <div style="font-size: 12px; color: #67e8f9; font-family: monospace; margin: 4px 0;">Elasticsearch (Search Accelerator)</div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5; margin-top: 10px; text-align: left;">
              • Customer-facing search and filtering catalog.<br/>
              • If an index corrupts, re-stream from the Vault.<br/>
              • Scaled independently for query volume.
            </div>
          </div>
        </div>
        """,
        "key_points": [
          "Treat Cassandra as the Bank Vault: immutable, durable source of truth for writes.",
          "Treat Elasticsearch as the Storefront Window: disposable, highly indexed view for customer search.",
          "Synchronize them asynchronously via Change Data Capture (CDC), never synchronous dual-writes."
        ],
        "script_en": "To synthesize both technologies in real-world systems, think of Cassandra as the Bank Vault and Elasticsearch as the Storefront Display Window. You put gold into the vault for safekeeping—that is Cassandra storing the truth. You arrange pretty merchandise in the display window for customers to find—that is Elasticsearch. If the display window breaks, you simply rebuild it from the vault.",
        "script_vi": "Để kết hợp hai công nghệ trong thực tế, hãy xem Cassandra là Két Sắt Ngân Hàng và Elasticsearch là Cửa Sổ Trưng Bày. Bạn cất giữ vàng và tiền thật an toàn trong két sắt — đó là Cassandra giữ dữ liệu gốc. Bạn trưng bày hàng mẫu ra cửa kính cho khách hàng dễ tìm kiếm — đó là Elasticsearch. Nếu cửa kính trưng bày bị hỏng, bạn chỉ việc lấy đồ từ trong két sắt ra bày lại."
    },
    {
        "id": "slide-30",
        "section": "07 Architecture",
        "badge": "Architecture Solution",
        "title": "Production Architecture: The CQRS Pattern",
        "subtitle": "Separating Writes from Searches Using Change Data Capture (CDC) and Kafka",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px; margin-top: 10px;">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; border-radius: 8px; padding: 14px;">
              <div style="font-size: 14px; font-weight: 800; color: #f87171; margin-bottom: 6px;">❌ THE DUAL-WRITE DANGER</div>
              <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
                App writes to Cassandra, then writes to Elasticsearch.<br/>
                • If ES fails or network drops -> <strong>Silent Data Divergence!</strong><br/>
                • Partial failures leave users with phantom search results.
              </div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; border-radius: 8px; padding: 14px;">
              <div style="font-size: 14px; font-weight: 800; color: #34d399; margin-bottom: 6px;">✓ THE CQRS + CDC SOLUTION</div>
              <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
                App writes ONLY to Cassandra (Command).<br/>
                • <strong>Debezium CDC:</strong> Tails Cassandra CommitLog.<br/>
                • Streams event to <strong>Kafka</strong> -> Async worker indexes into ES.<br/>
                • Guarantees eventual consistency and zero write slowdown!
              </div>
            </div>
          </div>
          <div style="margin-top: 16px; font-size: 12.5px; color: #94a3b8; text-align: center;">
            <strong>CQRS (Command Query Responsibility Segregation):</strong> Separates the write path (Commands) from the read path (Queries) so both run at maximum speed.
          </div>
        </div>
        """,
        "key_points": [
          "Never write directly to both Cassandra and Elasticsearch from application code (Dual-Write Anti-Pattern).",
          "Use Change Data Capture (CDC) via Kafka to tail Cassandra's CommitLog asynchronously.",
          "This architecture maintains eventual consistency without slowing down write ingestion."
        ],
        "script_en": "In production, never write to both Cassandra and Elasticsearch directly from your application code. If one write succeeds and the other fails, your data will silently diverge. The industry standard is CQRS with Change Data Capture. The application writes only to Cassandra. Debezium tails the commit log and streams change events through Kafka to asynchronously populate Elasticsearch.",
        "script_vi": "Trong môi trường thực tế, tuyệt đối không bao giờ cho ứng dụng ghi đồng thời vào cả Cassandra và Elasticsearch. Nếu một bên thành công còn bên kia lỗi mạng, dữ liệu sẽ bị sai lệch âm thầm. Giải pháp chuẩn mực của ngành là CQRS kết hợp Change Data Capture. Ứng dụng chỉ ghi vào Cassandra. Debezium theo dõi CommitLog và truyền qua Kafka để cập nhật chỉ mục ngầm sang Elasticsearch."
    },
    {
        "id": "slide-31",
        "section": "07 Conclusion",
        "badge": "Core Lessons",
        "title": "Three Golden Rules of Database Engineering",
        "subtitle": "Key Lessons for Designing High-Scale Modern Systems",
        "visual_html": """
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 10px;">
          <div style="background: #1e293b; border-top: 4px solid #3b82f6; border-radius: 8px; padding: 18px;">
            <div style="font-size: 24px; margin-bottom: 6px;">📐</div>
            <div style="font-size: 14px; font-weight: 800; color: #60a5fa;">1. No Silver Bullet</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-top: 8px;">
              The RUM Conjecture is absolute: no single storage engine can achieve maximum write speed, instant text search, and low memory at the same time.
            </p>
          </div>

          <div style="background: #1e293b; border-top: 4px solid #10b981; border-radius: 8px; padding: 18px;">
            <div style="font-size: 24px; margin-bottom: 6px;">⚡</div>
            <div style="font-size: 14px; font-weight: 800; color: #34d399;">2. Asymmetric Strengths</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-top: 8px;">
              Cassandra writes sequentially at 85k ops/s. Elasticsearch evaluates complex multi-term text queries 280× faster than linear scans.
            </p>
          </div>

          <div style="background: #1e293b; border-top: 4px solid #06b6d4; border-radius: 8px; padding: 18px;">
            <div style="font-size: 24px; margin-bottom: 6px;">🔄</div>
            <div style="font-size: 14px; font-weight: 800; color: #22d3ee;">3. Decouple via CQRS</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-top: 8px;">
              Combine the Bank Vault and Storefront Window using CDC and Kafka. Let each engine do what hardware physics built it to do.
            </p>
          </div>
        </div>
        """,
        "key_points": [
          "Storage physics dictates design: no single storage engine satisfies all workloads.",
          "Cassandra excels at append-only sequential ingestion; Elasticsearch excels at multi-term lexical retrieval.",
          "In production, combine both via CQRS and asynchronous Change Data Capture."
        ],
        "script_en": "To conclude our findings, remember three core principles. First: There is no silver bullet—the RUM Conjecture dictates that physical trade-offs are unavoidable. Second: Cassandra and Elasticsearch have complementary asymmetric strengths. Third: Decouple them in production using the CQRS pattern with Change Data Capture.",
        "script_vi": "Để kết luận buổi báo cáo, chúng em xin đúc kết 3 nguyên tắc cốt lõi. Thứ nhất: Không có giải pháp vạn năng — Giả thuyết RUM khẳng định sự đánh đổi vật lý là tất yếu. Thứ hai: Cassandra và Elasticsearch sở hữu sức mạnh bổ trợ đối lập nhau. Thứ ba: Hãy kết hợp chúng trong thực tế qua mô hình CQRS và Change Data Capture."
    },
    {
        "id": "slide-32",
        "section": "07 Conclusion",
        "badge": "Q&A Session",
        "title": "Thank You & Open Q&A",
        "subtitle": "Cảm ơn Thầy Cô và các bạn! Sẵn sàng giải đáp mọi câu hỏi thảo luận",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #3b82f6; border-radius: 12px; padding: 22px; text-align: center; margin-top: 10px;">
          <div style="font-size: 36px; margin-bottom: 6px;">🎓</div>
          <div style="font-size: 22px; font-weight: 900; color: #fff;">THANK YOU / CẢM ƠN QUÝ THẦY CÔ VÀ CÁC BẠN!</div>
          <div style="font-size: 13.5px; color: #93c5fd; margin-top: 4px;">
            CO5173 Advanced Data Engineering • Master of Computer Science • HCMUT
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; text-align: left;">
            <div style="background: #1e293b; border-radius: 8px; padding: 14px; border-left: 3px solid #10b981;">
              <div style="font-size: 13px; font-weight: 800; color: #34d399; margin-bottom: 4px;">📂 Open-Source Reproducibility</div>
              <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
                • Interactive Notebook: <a href="https://colab.research.google.com/github/Pasonnn/co5173-modern-database-search-techniques/blob/main/demo.ipynb" target="_blank" style="color: #38bdf8; text-decoration: underline; font-weight: 700;">Open in Google Colab</a><br/>
                • Interactive CLI: <code>python3 demo.py --no-pause</code><br/>
                • Automated Tests: <code>python3 tests/test_all.py</code> (100% Pass)<br/>
                • Benchmarks: <code>python3 benchmarks/run.py</code>
              </div>
            </div>
            <div style="background: #1e293b; border-radius: 8px; padding: 14px; border-left: 3px solid #f59e0b;">
              <div style="font-size: 13px; font-weight: 800; color: #fbbf24; margin-bottom: 4px;">📚 Peer-Reviewed Literature (> 2021)</div>
              <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
                • [1] Huynh et al., <em>VLDB Journal</em> (2024) [DOI: 10.1007/s00778-023-00826-9]<br/>
                • [2] Lin, Nogueira, & Yates, <em>Springer</em> (2022) [DOI: 10.1007/978-3-031-02181-7]
              </div>
            </div>
          </div>

          <div style="margin-top: 18px; font-size: 14px; color: #38bdf8; font-weight: 700;">
            💬 We are now ready to take your questions and discuss technical details!
          </div>
        </div>
        """,
        "key_points": [
          "Complete code, benchmarks, tests, and interactive slides are fully reproducible.",
          "Grounded strictly in peer-reviewed modern academic literature (VLDB 2024, Springer 2022).",
          "Ready for live Q&A session with committee and audience."
        ],
        "script_en": "Thank you very much for your time and attention. All reference implementations, automated unit tests, stress benchmarks, and interactive notebooks are fully open and reproducible in our repository. We are now open and eager to take your questions and discuss any technical details.",
        "script_vi": "Xin chân thành cảm ơn quý Thầy Cô và các bạn đã chú ý lắng nghe. Toàn bộ mã nguồn hai bộ máy tham chiếu, bài kiểm thử tự động, tập đo đạc hiệu năng và notebook tương tác đều được đóng gói độc lập và tái lập 100% trong kho lưu trữ của nhóm. Chúng em rất mong nhận được những góp ý và câu hỏi thảo luận từ Thầy Cô cùng các bạn."
    }
]

print("Part 4 slides created.")


ALL_SLIDES = ALL_SLIDES + PART_2_SLIDES + PART_3_SLIDES + PART_4_SLIDES
print(f"Total visual slides loaded: {len(ALL_SLIDES)}")
