# Complete 23-slide presentation dataset
# CO5173 Advanced Data Engineering - Master's Defense Deck
# Strictly calibrated for 15-minute presentation (~39 seconds per slide)

ALL_SLIDES = [
    # ==========================================
    # SECTION 00: INTRODUCTION (Slides 01 - 02)
    # ==========================================
    {
        "id": "slide-01",
        "section": "00 Introduction",
        "badge": "Cover Slide",
        "title": "Storage Engine Duality",
        "subtitle": "Apache Cassandra (LSM-Tree) vs. Elasticsearch (Inverted Index) — A Comparative Study",
        "visual_html": """
        <div style="text-align: center; padding: 25px 20px;">
          <div style="display: inline-block; background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; color: #93c5fd; padding: 4px 14px; border-radius: 9999px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 14px;">
            CO5173 — ADVANCED DATA ENGINEERING • MASTER OF COMPUTER SCIENCE • HCMUT
          </div>
          <h1 style="font-size: 32px; font-weight: 800; color: #f8fafc; margin-bottom: 10px; letter-spacing: -0.5px;">
            Storage Engine Duality: Cassandra vs. Elasticsearch
          </h1>
          <p style="font-size: 15px; color: #94a3b8; max-width: 780px; margin: 0 auto 24px; line-height: 1.5;">
            An Architectural, Algorithmic, and Empirical Master's Defense Investigation into LSM-Trees and Inverted Indexes under the RUM Conjecture
          </p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 720px; margin: 0 auto 20px; text-align: left;">
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 14px 18px;">
              <div style="color: #60a5fa; font-weight: 700; font-size: 14px; margin-bottom: 4px;">⚡ Apache Cassandra (LSM-Tree)</div>
              <div style="color: #cbd5e1; font-size: 12px; line-height: 1.4;">Optimized for high-velocity sequential write ingestion ($52k+$ ops/s) via MemTable & immutable SSTables.</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 14px 18px;">
              <div style="color: #22d3ee; font-weight: 700; font-size: 14px; margin-bottom: 4px;">🔍 Elasticsearch (Inverted Index)</div>
              <div style="color: #cbd5e1; font-size: 12px; line-height: 1.4;">Optimized for microsecond multi-term text search ($35\\ \\mu\\text{s}$) & BM25 ranking via posting lists.</div>
            </div>
          </div>
          <div style="display: inline-block; background: rgba(15, 23, 42, 0.8); border: 1px solid #1e293b; border-radius: 8px; padding: 8px 18px; font-size: 12px; color: #64748b;">
            Theoretical Foundation: Harvard & Boston University <strong style="color: #e2e8f0;">RUM Conjecture</strong> • 100% Zero-Dependency Python Reference Engines
          </div>
        </div>
        """,
        "key_points": [
            "Master's thesis defense: Rigorous empirical and theoretical comparison between Log-Structured Merge-Trees and Inverted Indexes.",
            "Investigating how physical on-disk storage layouts dictate macro-architectural throughput and query latency.",
            "Validated through clean-room reference engines, real-world datasets (10k cities, 1,655 quotes), and 5-round statistical benchmarks."
        ],
        "script_en": "Good day, esteemed committee members and colleagues. Welcome to our defense presentation for CO5173 Advanced Data Engineering. Today, we present a comparative investigation into the storage engine duality between Apache Cassandra's LSM-Tree and Elasticsearch's Inverted Index. In modern data systems, no single database can simultaneously maximize write ingestion and arbitrary text search. Over the next 15 minutes, we examine the fundamental storage laws that govern this trade-off, contrast their internal mechanics, present empirical benchmark evidence, and demonstrate their production synthesis under CQRS.",
        "script_vi": "Kính chào quý Thầy Cô trong Hội đồng và các bạn học viên cao học. Chào mừng quý vị đến với buổi bảo vệ đồ án môn CO5173 Kỹ nghệ Dữ liệu Nâng cao. Hôm nay, nhóm xin trình bày nghiên cứu so sánh về tính nhị nguyên kiến trúc lưu trữ giữa LSM-Tree của Apache Cassandra và Chỉ mục đảo của Elasticsearch. Trong các hệ thống dữ liệu lớn, không một cơ sở dữ liệu đơn lẻ nào có thể vừa tối đa hóa tốc độ ghi, vừa tối ưu hóa tìm kiếm văn bản tùy ý. Trong 15 phút tới, nhóm sẽ làm rõ quy luật lưu trữ chi phối sự đánh đổi này, đối chiếu cơ chế vật lý bên trong, minh chứng bằng thực nghiệm và tổng hợp mô hình CQRS trong thực tế."
    },
    {
        "id": "slide-02",
        "section": "00 Introduction",
        "badge": "15-Min Roadmap",
        "title": "Master's Defense Roadmap (15-Minute Target)",
        "subtitle": "4 Core Acts: Storage Crisis → Storage Mechanics → Empirical Validation → CQRS Synthesis",
        "visual_html": """
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 20px;">
          <div style="background: #111827; border: 1px solid #374151; border-top: 4px solid #ef4444; border-radius: 8px; padding: 16px;">
            <div style="font-size: 11px; font-weight: 700; color: #f87171; margin-bottom: 4px;">ACT 1 (~3 MIN)</div>
            <div style="font-size: 14px; font-weight: 800; color: #f3f4f6; margin-bottom: 8px;">The Storage Crisis</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4;">
              • B+ Tree Eviction Trap<br/>
              • Full-Scan Pathology<br/>
              • Writer vs. Reader Dilemma<br/>
              • The RUM Conjecture
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #64748b; font-weight: 600;">Slides 03 – 06</div>
          </div>
          <div style="background: #111827; border: 1px solid #374151; border-top: 4px solid #3b82f6; border-radius: 8px; padding: 16px;">
            <div style="font-size: 11px; font-weight: 700; color: #60a5fa; margin-bottom: 4px;">ACT 2 (~4 MIN)</div>
            <div style="font-size: 14px; font-weight: 800; color: #f3f4f6; margin-bottom: 8px;">LSM & Cassandra</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4;">
              • MemTable & CommitLog<br/>
              • SSTables & Compaction Debt<br/>
              • Sequential Write Physics<br/>
              • Bloom Filter Fast-Fail
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #64748b; font-weight: 600;">Slides 07 – 11</div>
          </div>
          <div style="background: #111827; border: 1px solid #374151; border-top: 4px solid #06b6d4; border-radius: 8px; padding: 16px;">
            <div style="font-size: 11px; font-weight: 700; color: #22d3ee; margin-bottom: 4px;">ACT 3 (~4 MIN)</div>
            <div style="font-size: 14px; font-weight: 800; color: #f3f4f6; margin-bottom: 8px;">Inverted Index & ES</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4;">
              • Direct Posting Lists<br/>
              • Text Pipeline & NRT Lag<br/>
              • Skip Pointer Highway<br/>
              • Okapi BM25 & RAM Cost
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #64748b; font-weight: 600;">Slides 12 – 16</div>
          </div>
          <div style="background: #111827; border: 1px solid #374151; border-top: 4px solid #10b981; border-radius: 8px; padding: 16px;">
            <div style="font-size: 11px; font-weight: 700; color: #34d399; margin-bottom: 4px;">ACT 4 (~4 MIN)</div>
            <div style="font-size: 14px; font-weight: 800; color: #f3f4f6; margin-bottom: 8px;">Synthesis & Proofs</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4;">
              • Lucene Segment Convergence<br/>
              • 5W1H Matrix Comparison<br/>
              • 5-Round Scorecard (Q1-Q4)<br/>
              • Production CQRS Synthesis
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #64748b; font-weight: 600;">Slides 17 – 23</div>
          </div>
        </div>
        <div style="margin-top: 18px; text-align: center; font-size: 12px; color: #94a3b8;">
          ⏱️ <strong style="color: #f3f4f6;">Pacing Budget:</strong> Exactly 23 visual slides @ ~39 seconds per slide = ~14.5 minutes, preserving breathing room for questions.
        </div>
        """,
        "key_points": [
            "Consolidated 23 visual slides calibrated for a strict 15-minute defense window (~39 seconds per slide).",
            "Act 1: The physical storage crisis and the theoretical foundation of the RUM Conjecture.",
            "Act 2 & 3: Deep dive into LSM-Tree write paths, compaction debt, Bloom filters, and Lucene's NRT pipeline.",
            "Act 4: Architectural convergence, 5-round empirical verification, and dual-engine CQRS production synthesis."
        ],
        "script_en": "Here is our defense roadmap structured into four distinct acts across 23 slides, calibrated precisely for a 15-minute presentation. In Act 1, we analyze the storage crisis—showing why traditional relational engines fail under write-heavy loads and full-text search. In Act 2, we dissect Cassandra's LSM-tree architecture, sequential appends, and compaction debt. In Act 3, we explore Lucene's inverted index, NRT refresh pipeline, and BM25 ranking. Finally, in Act 4, we reveal their architectural convergence, present 5-round empirical benchmark proofs, and show how both engines synthesize in production via CQRS.",
        "script_vi": "Đây là lộ trình báo cáo gồm 4 phần xuyên suốt 23 slide, được căn chỉnh chính xác cho khung thời gian 15 phút bảo vệ. Trong Phần 1, nhóm phân tích cuộc khủng hoảng lưu trữ—chỉ ra vì sao các hệ RDBMS truyền thống gặp bế tắc trước tải ghi lớn và truy vấn toàn văn. Trong Phần 2, ta mổ xẻ kiến trúc LSM-Tree của Cassandra, luồng ghi tuần tự và nợ dồn compaction. Trong Phần 3, ta khám phá chỉ mục đảo của Lucene, quy trình làm tươi NRT và thuật toán BM25. Cuối cùng, trong Phần 4, nhóm chỉ ra sự hội tụ kiến trúc giữa hai hệ thống, công bố số liệu thực nghiệm qua 5 lượt đo và mô hình tích hợp CQRS trong thực tế."
    },

    # ==========================================
    # SECTION 01: STORAGE CRISIS (Slides 03 - 06)
    # ==========================================
    {
        "id": "slide-03",
        "section": "01 Storage Crisis",
        "badge": "Problem 1: B+ Tree",
        "title": "Traditional Databases: The Overwrite & Eviction Trap",
        "subtitle": "Dirty Page Eviction & Unbuffered Write Amplification in In-Place B+ Trees",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px dashed #ef4444; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; color: #f87171; font-weight: 700; margin-bottom: 6px;">BUFFER POOL & PAGE FLUSH MECHANICS</div>
            <div style="font-size: 11px; color: #94a3b8; margin-bottom: 12px;">Standard B+ Tree Page (MySQL InnoDB, PostgreSQL)</div>
            <div style="background: #1e293b; border: 2px solid #ef4444; border-radius: 8px; padding: 14px;">
              <div style="font-size: 11px; color: #38bdf8; margin-bottom: 6px;">RAM: Sequential WAL Append + Dirty Page Buffer</div>
              <div style="background: #dc2626; color: white; padding: 8px; border-radius: 6px; font-size: 13px; font-weight: 700; box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);">
                ✏️ Update 50 bytes of user status in RAM
              </div>
              <div style="font-size: 11px; color: #fca5a5; margin-top: 6px;">Checkpoint / Eviction forces 16 KB In-Place Disk Rewrite!</div>
            </div>
            <div style="margin-top: 12px; font-size: 13px; color: #fb7185; font-weight: 700;">
              Disk Write Amplification: 16,384 B / 50 B = ~327×
            </div>
          </div>
          <div>
            <div style="background: rgba(244, 63, 94, 0.15); border-left: 4px solid #f43f5e; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 15px; font-weight: 800; color: #fb7185;">Page Eviction Write Amplification (~327×)</div>
              <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                While WAL appends absorb immediate writes in memory, dirty pages must eventually flush back to disk in-place. A 50-byte record modification forces rewriting the entire 16 KB page on eviction.
              </div>
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>Write Stalls:</strong> Under sustained write load, the buffer pool fills with dirty pages, triggering aggressive random flushing.<br/>
              • <strong>Random Disk Seeks:</strong> In-place updates scatter writes across arbitrary disk offsets, starving I/O bandwidth.<br/>
              • <strong>SSD Wear:</strong> Constant 16 KB page rewrites cause high flash write amplification and early drive degradation.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Production RDBMS (PostgreSQL, MySQL InnoDB) absorb updates in RAM buffer pools and append sequentially to WAL.",
            "However, dirty pages must eventually flush back to disk in-place during checkpoints or cache eviction.",
            "Modifying a 50-byte record forces rewriting the entire 16,384-byte page: a 327× worst-case write amplification.",
            "Under sustained write pressure, page eviction induces severe random disk I/O thrashing and write stalls."
        ],
        "script_en": "To understand why specialized engines were born, we examine the overwrite trap in relational B+ Tree architectures like InnoDB or PostgreSQL. When a 50-byte record is updated, modern RDBMS absorb writes in memory and append to a Write-Ahead Log. But when dirty pages must be flushed or evicted from the buffer pool during checkpoints, the database must write back the entire 16-kilobyte page in-place. This worst-case 327-fold write amplification causes random disk seeking, saturates controller bandwidth, and caps write ingestion under sustained load.",
        "script_vi": "Để hiểu vì sao các cơ sở dữ liệu chuyên biệt ra đời, trước hết ta phân tích cái bẫy ghi đè của cây B+ trong các hệ RDBMS như InnoDB hay PostgreSQL. Khi cập nhật một bản ghi 50 byte, hệ thống ghi log tuần tự vào WAL và đệm trên RAM. Tuy nhiên, khi các trang bẩn bị đẩy ra đĩa (page eviction) hoặc xả định kỳ (checkpoint), hệ thống buộc phải ghi đè lại toàn bộ trang 16 KB tại chỗ. Hệ số khuếch đại ghi 327 lần ở pha xả đĩa này tạo ra các thao tác tìm kiếm ngẫu nhiên, làm nghẽn băng thông điều khiển đĩa và giới hạn thông lượng ghi khi chịu tải liên tục."
    },
    {
        "id": "slide-04",
        "section": "01 Storage Crisis",
        "badge": "Problem 2: Full Scan",
        "title": "Traditional Databases: The Full-Scan Trap",
        "subtitle": "Why Leading Wildcards and Full-Text Queries Bypass B+ Tree Indexes",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px dashed #f59e0b; border-radius: 12px; padding: 20px;">
            <div style="font-family: monospace; font-size: 13px; color: #f59e0b; background: #0f172a; padding: 10px 14px; border-radius: 6px; border: 1px solid #334155; margin-bottom: 14px;">
              SELECT * FROM articles<br/>
              WHERE content LIKE <span style="color: #ef4444; font-weight: 700;">'%database%'</span>;
            </div>
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 6px; padding: 12px; text-align: center;">
              <div style="color: #f87171; font-weight: 800; font-size: 13px; margin-bottom: 4px;">⚠️ B+ TREE INDEX COMPLETELY BYPASSED</div>
              <div style="font-size: 11.5px; color: #94a3b8;">Leading wildcard '%' makes prefix search impossible. Forces reading 100,000 pages from disk!</div>
            </div>
          </div>
          <div>
            <div style="background: rgba(245, 158, 11, 0.15); border-left: 4px solid #f59e0b; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 15px; font-weight: 800; color: #fcd34d;">Table Scan Pathology ($O(N)$)</div>
              <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                Relational B+ Trees index strings strictly by sorted prefix. A leading wildcard blinds the index, forcing an exhaustive row-by-row table scan.
              </div>
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>I/O Starvation:</strong> The database must read gigabytes of raw data into memory just to check one substring.<br/>
              • <strong>Buffer Pool Churn:</strong> Millions of scanned rows evict hot caching pages, degrading unrelated queries.<br/>
              • <strong>No Relevance Scoring:</strong> Cannot compute Term Frequency (TF) or BM25 relevance; matches are binary.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "B+ Trees index keys via lexicographical prefix sorting; queries with leading wildcards (LIKE '%term%') cannot prune tree branches.",
            "The storage engine falls back to an exhaustive Table Scan ($O(N)$), reading every disk page into the buffer pool.",
            "Traditional relational indexes cannot compute term frequency (TF), document frequency (IDF), or probabilistic relevance scores."
        ],
        "script_en": "The second fundamental failure of traditional databases is full-text search. Relational B+ Trees index strings strictly by their sorted prefixes. When a query contains a leading wildcard such as LIKE '%database%', the index is completely blind and cannot prune any tree branches. The engine is forced to execute an exhaustive table scan, reading every row from disk. This wastes massive I/O, floods the buffer pool, and lacks any mathematical capability to rank which record is the most relevant.",
        "script_vi": "Thất bại căn bản thứ hai của cơ sở dữ liệu truyền thống là tìm kiếm toàn văn. Cây B+ chỉ lập chỉ mục chuỗi ký tự theo thứ tự tiền tố đã sắp xếp. Khi câu truy vấn chứa ký tự đại diện ở đầu như LIKE '%database%', cây chỉ mục hoàn toàn vô hiệu và không thể tỉa nhánh. Hệ thống buộc phải quét toàn bộ bảng, nạp từng dòng dữ liệu từ đĩa vào bộ đệm. Thao tác này gây lãng phí tài nguyên I/O nghiêm trọng, làm tràn bộ đệm RAM và hoàn toàn không có khả năng tính điểm xếp hạng độ liên quan của kết quả."
    },
    {
        "id": "slide-05",
        "section": "01 Storage Crisis",
        "badge": "The Conflict",
        "title": "The Writer vs. Reader Conflict",
        "subtitle": "Why One Physical Layout Cannot Simultaneously Maximize Writes and Text Search",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 22px; margin-top: 10px;">
          <div style="display: grid; grid-template-columns: 1fr 60px 1fr; align-items: center; gap: 14px;">
            <div style="background: rgba(59, 130, 246, 0.1); border: 2px solid #3b82f6; border-radius: 10px; padding: 18px; text-align: center;">
              <div style="font-size: 28px; margin-bottom: 6px;">⚡</div>
              <div style="font-size: 16px; font-weight: 800; color: #60a5fa; margin-bottom: 6px;">FAST WRITING NEEDS:</div>
              <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                • Zero upfront processing<br/>
                • Pure sequential append<br/>
                • No sorting on write<br/>
                • <strong>Goal: Maximize Ingestion</strong>
              </div>
            </div>
            <div style="text-align: center; font-size: 22px; font-weight: 900; color: #ef4444;">
              VS
            </div>
            <div style="background: rgba(6, 182, 212, 0.1); border: 2px solid #06b6d4; border-radius: 10px; padding: 18px; text-align: center;">
              <div style="font-size: 28px; margin-bottom: 6px;">🔍</div>
              <div style="font-size: 16px; font-weight: 800; color: #22d3ee; margin-bottom: 6px;">FAST SEARCH NEEDS:</div>
              <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                • Heavy upfront tokenization<br/>
                • Sorted inverted posting lists<br/>
                • Term frequency dictionaries<br/>
                • <strong>Goal: Microsecond Retrieval</strong>
              </div>
            </div>
          </div>
          <div style="margin-top: 18px; text-align: center; font-size: 13px; color: #e2e8f0; border-top: 1px solid #374151; padding-top: 14px;">
            💥 <strong>The Fundamental Conflict:</strong> You cannot organize raw data for instantaneous append without destroying searchability, and you cannot organize for microsecond search without doing massive upfront indexing.
          </div>
        </div>
        """,
        "key_points": [
            "Fastest Write Path: Raw sequential byte append with zero upfront parsing or index reorganization.",
            "Fastest Search Path: Heavy upfront tokenization, morphological stemming, dictionary hashing, and inverted posting list sorting.",
            "A single monolithic storage layout cannot satisfy both requirements without crippling performance in one dimension."
        ],
        "script_en": "Here lies the core dilemma of database storage engineering: the mechanical requirements for fast writes directly oppose the requirements for fast search. To achieve maximum write throughput, an engine must perform minimal upfront work—simply appending raw bytes sequentially. Conversely, to deliver microsecond full-text search, an engine must perform exhaustive upfront indexing—tokenizing, sorting, and cross-referencing every term. Attempting both on a single storage layout forces an unacceptable compromise.",
        "script_vi": "Đây chính là thế lưỡng nan cốt lõi của kỹ nghệ lưu trữ cơ sở dữ liệu: các yêu cầu vật lý để ghi nhanh hoàn toàn đối nghịch với các yêu cầu để tìm kiếm nhanh. Để đạt thông lượng ghi tối đa, hệ thống phải thực hiện tối thiểu thao tác xử lý ban đầu—chỉ ghi nối tiếp các byte tuần tự. Ngược lại, để tìm kiếm toàn văn trong vài micro-giây, hệ thống phải trả giá bằng việc lập chỉ mục chuyên sâu ngay từ đầu—tách từ, chuẩn hóa và sắp xếp danh sách tài liệu. Cố gắng dung hòa cả hai trên một cấu trúc lưu trữ đơn lẻ chắc chắn sẽ dẫn đến sự thỏa hiệp hiệu năng trầm trọng."
    },
    {
        "id": "slide-06",
        "section": "01 Storage Crisis",
        "badge": "Storage Law",
        "title": "The Fundamental Storage Law: The RUM Conjecture",
        "subtitle": "Minimizing Two Database Overheads Inevitably Worsens the Third: Read (R), Update (U), Memory (M)",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 16px; text-align: center;">
            <svg viewBox="0 0 320 280" style="max-width: 100%; height: 230px;">
              <polygon points="160,25 30,245 290,245" fill="none" stroke="#475569" stroke-width="2.5" stroke-dasharray="4,4" />
              <!-- Read Overhead -->
              <circle cx="160" cy="25" r="18" fill="#06b6d4" />
              <text x="160" y="30" fill="white" font-weight="900" font-size="13" text-anchor="middle">R</text>
              <text x="160" y="-2" fill="#22d3ee" font-weight="800" font-size="11" text-anchor="middle">READ OVERHEAD</text>
              <!-- Update Overhead -->
              <circle cx="30" cy="245" r="18" fill="#3b82f6" />
              <text x="30" y="250" fill="white" font-weight="900" font-size="13" text-anchor="middle">U</text>
              <text x="30" y="278" fill="#60a5fa" font-weight="800" font-size="11" text-anchor="middle">UPDATE (U)</text>
              <!-- Memory Overhead -->
              <circle cx="290" cy="245" r="18" fill="#10b981" />
              <text x="290" y="250" fill="white" font-weight="900" font-size="13" text-anchor="middle">M</text>
              <text x="290" y="278" fill="#34d399" font-weight="800" font-size="11" text-anchor="middle">MEMORY (M)</text>
              <!-- Cassandra Anchor -->
              <circle cx="95" cy="245" r="8" fill="#f59e0b" />
              <text x="95" y="232" fill="#fbbf24" font-weight="800" font-size="11" text-anchor="middle">Cassandra (U, M)</text>
              <!-- Elasticsearch Anchor -->
              <circle cx="190" cy="75" r="8" fill="#f43f5e" />
              <text x="240" y="78" fill="#fb7185" font-weight="800" font-size="11" text-anchor="middle">Elasticsearch (R)</text>
            </svg>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 4px; margin-bottom: 12px;">
              <strong style="color: #60a5fa;">Cassandra (LSM):</strong> Minimizes <strong>Update (U)</strong> and <strong>Memory (M)</strong>. Fast sequential writes and compact Bloom filters (~10 bits/key), accepting higher Read (R) overhead on existing keys.
            </div>
            <div style="background: rgba(6, 182, 212, 0.15); border-left: 4px solid #06b6d4; padding: 12px 16px; border-radius: 4px;">
              <strong style="color: #22d3ee;">Elasticsearch:</strong> Minimizes <strong>Read (R)</strong>. Delivers microsecond full-text search, but pays with massive Memory (M) overhead ($15\\times$ more RAM) and heavy index merge maintenance.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "RUM Conjecture (Harvard/BU): Database designs can optimize at most two corners: Read (R), Update (U), or Memory (M).",
            "Cassandra optimizes Update ($U$) and Memory ($M$) via sequential append and compact Bloom filters, accepting Read ($R$) penalty.",
            "Elasticsearch optimizes Read ($R$) via inverted posting lists, accepting massive Memory ($M \\sim 15\\times$) and Update ($U$) costs."
        ],
        "script_en": "This physical boundary was formalized by researchers at Harvard and Boston University as the RUM Conjecture. It proves that no storage engine can simultaneously minimize Read overhead (R), Update overhead (U), and Memory overhead (M). You can optimize at most two. Cassandra prioritizes Update and Memory overhead through sequential appends and compact Bloom filters, accepting read complexity. Elasticsearch strictly optimizes Read latency, paying a massive penalty in memory and index maintenance.",
        "script_vi": "Ranh giới vật lý này đã được các nhà nghiên cứu tại Harvard và Đại học Boston hình thức hóa thành Giả thuyết RUM. Định lý chứng minh rằng không một bộ máy lưu trữ nào có thể đồng thời tối thiểu hóa cả chi phí Đọc (Read - R), Ghi (Update - U) và Bộ nhớ (Memory - M). Ta chỉ có thể tối ưu tối đa hai đỉnh. Cassandra ưu tiên chi phí Ghi và Bộ nhớ thông qua ghi tuần tự và Bloom Filter cô đọng, chấp nhận đánh đổi độ phức tạp khi đọc. Ngược lại, Elasticsearch tối ưu triệt để độ trễ Đọc, chấp nhận tiêu tốn gấp nhiều lần RAM và chi phí bảo trì chỉ mục."
    },

    # ==========================================
    # SECTION 02: LSM & CASSANDRA (Slides 07 - 11)
    # ==========================================
    {
        "id": "slide-07",
        "section": "02 LSM & Cassandra",
        "badge": "Analogy Step 1",
        "title": "LSM Storage Engine: The Desk Notepad",
        "subtitle": "Step 1: Low-Latency Ingestion via MemTable (RAM) and Sequential CommitLog (Disk)",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div class="notepad-mockup">
            <div style="text-align: center; border-bottom: 2px solid #b45309; padding-bottom: 6px; margin-bottom: 8px;">
              <span style="font-size: 14px; font-weight: 800;">📝 DESK NOTEPAD (MemTable in RAM)</span>
            </div>
            <div class="notepad-line"><span>• 10:01:02 - Book #1042 checked in</span><span style="color: #059669;">✓ OK</span></div>
            <div class="notepad-line"><span>• 10:01:05 - Book #8812 checked in</span><span style="color: #059669;">✓ OK</span></div>
            <div class="notepad-line"><span>• 10:01:09 - Book #0145 checked in</span><span style="color: #059669;">✓ OK</span></div>
            <div class="notepad-line" style="background: rgba(245, 158, 11, 0.2);">
              <span>• 10:01:14 - Book #5521 checked in</span><span style="color: #d97706;">⚡ &lt; 1 µs</span>
            </div>
            <div style="margin-top: 8px; font-size: 10.5px; color: #92400e; text-align: center;">
              Fastest possible write: jot down on desk without walking to shelves!
            </div>
          </div>
          <div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 16px; font-weight: 800; color: #34d399;">Step 1: Write to RAM MemTable</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">
                Incoming writes go directly to an in-memory sorted structure (SkipList or Red-Black Tree).
              </div>
            </div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 14px 18px; border-radius: 6px;">
              <div style="font-size: 16px; font-weight: 800; color: #60a5fa;">Crash Safety: CommitLog (Disk)</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 4px;">
                Simultaneously, the write is appended to a sequential disk file (CommitLog). If the node loses power, the MemTable is reconstructed instantly.
              </div>
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Client writes are received in RAM into a sorted MemTable (concurrent skip list or balanced tree).",
            "Simultaneously, writes are appended sequentially to a durable on-disk CommitLog (Write-Ahead Log).",
            "Because writes require zero disk seeks and no in-place page rewriting, write operations acknowledge in microseconds."
        ],
        "script_en": "To understand Cassandra's Log-Structured Merge-Tree, consider a librarian at a busy intake desk. When thousands of books arrive every minute, you do not run to the shelves to insert each book in alphabetical order. Instead, you quickly jot each entry onto your desk notepad. In Cassandra, this notepad is the MemTable in RAM. For crash resilience, an append-only CommitLog sequentially records every transaction on disk. Because there are zero disk seeks, the write returns in microseconds.",
        "script_vi": "Để hiểu cây LSM của Cassandra, hãy hình dung một thủ thư tại bàn tiếp nhận sách bận rộn. Khi hàng ngàn cuốn sách đổ về mỗi phút, ta không thể chạy đến từng kệ sách để xếp xen kẽ từng cuốn theo thứ tự chữ cái. Thay vào đó, ta ghi thật nhanh vào cuốn sổ tay trên bàn. Trong Cassandra, cuốn sổ tay này chính là MemTable trên RAM. Để đảm bảo an toàn dữ liệu khi sự cố xảy ra, một tiến trình ghi nhật ký CommitLog tuần tự nối tiếp lên đĩa. Do không phát sinh thao tác tìm kiếm ngẫu nhiên trên đĩa, lệnh ghi phản hồi ngay lập tức trong vài micro-giây."
    },
    {
        "id": "slide-08",
        "section": "02 LSM & Cassandra",
        "badge": "SSTable & Compaction",
        "title": "LSM Lifecycle: SSTables & Background Compaction",
        "subtitle": "Freezing Immutable Files, Purging Tombstones, and the Hidden Cost of Compaction Debt",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; margin-top: 8px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 10px; padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">IMMUTABLE SSTABLE FLUSH & COMPACTION</div>
            <div style="background: #0f172a; border-left: 3px solid #10b981; padding: 8px 12px; border-radius: 4px; margin-bottom: 8px; font-size: 11.5px;">
              <strong style="color: #34d399;">1. Flush:</strong> MemTable reaches capacity threshold $\\to$ flushed sequentially as immutable SSTable ($L_0$).
            </div>
            <div style="background: #0f172a; border-left: 3px solid #f59e0b; padding: 8px 12px; border-radius: 4px; margin-bottom: 8px; font-size: 11.5px;">
              <strong style="color: #fbbf24;">2. Tombstones:</strong> Deletions append Tombstone markers; dead records are purged only during compaction.
            </div>
            <div style="background: #0f172a; border-left: 3px solid #3b82f6; padding: 8px 12px; border-radius: 4px; font-size: 11.5px;">
              <strong style="color: #60a5fa;">3. Compaction:</strong> Background multi-way merge sort combines $N$ sorted SSTables into $L_1, L_2$.
            </div>
          </div>
          <div>
            <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
              <div style="font-size: 14px; font-weight: 800; color: #f87171;">The Hidden Trade-Off: Compaction Debt</div>
              <div style="font-size: 11.5px; color: #cbd5e1; margin-top: 4px; line-height: 1.4;">
                LSM does not eliminate write work—it <strong>defers</strong> it to background compaction. Leveled Compaction incurs a write amplification factor of <strong>10× to 30×</strong>.
              </div>
            </div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              • <strong>I/O Compaction Debt:</strong> Under sustained burst ingestion, background compaction cannot keep pace with new SSTable flushes.<br/>
              • <strong>Write Throttling:</strong> If uncompacted SSTables accumulate beyond safe limits, Cassandra deliberately throttles client writes to prevent read degradation.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "When MemTable reaches capacity threshold, it freezes and flushes to disk as an immutable SSTable via sequential I/O.",
            "Deletions are non-destructive: a Tombstone marker with a deletion timestamp is appended to the stream.",
            "Background Compaction: Multi-way merge sort merges overlapping SSTables, discards obsolete versions, and evicts tombstones.",
            "Trade-off (Compaction Debt): LSM defers write work rather than eliminating it. Leveled Compaction incurs 10×–30× write amplification; sustained ingestion can cause I/O debt that throttles foreground writes."
        ],
        "script_en": "When the MemTable fills, Cassandra freezes it and writes an immutable, sorted SSTable sequentially to disk. Deletions do not overwrite data; they are appended as Tombstones. In the background, compaction merges multiple SSTables to eliminate duplicates and reclaim space. But this reveals LSM's critical trade-off: write work is deferred, not eliminated. Leveled compaction introduces a 10× to 30× background write amplification factor. If ingestion exceeds disk bandwidth, background compaction debt will eventually throttle foreground writes.",
        "script_vi": "Khi MemTable đầy, Cassandra đóng băng và xả tuần tự xuống đĩa thành một file SSTable bất biến. Thao tác xóa không ghi đè dữ liệu mà ghi nhận bằng thẻ Tombstone. Ở chế độ nền, tiến trình Compaction hòa trộn nhiều SSTable để loại bỏ dữ liệu cũ và thu hồi dung lượng. Tuy nhiên, đây là sự đánh đổi cốt lõi: công việc ghi bị trì hoãn chứ không biến mất. Compaction theo tầng tạo ra hệ số khuếch đại ghi nền từ 10 đến 30 lần. Nếu nợ dồn I/O compaction tích tụ, hệ thống sẽ buộc phải bóp nghẹt luồng ghi đầu vào."
    },
    {
        "id": "slide-09",
        "section": "02 LSM & Cassandra",
        "badge": "Hardware Physics",
        "title": "Storage Physics: Why Sequential Writing Wins",
        "subtitle": "Sequential Appends Outpace Random Seeks by 50× to 100× on HDDs and NVMe SSDs",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px;">
            <div style="font-size: 13px; color: #94a3b8; font-weight: 700; margin-bottom: 12px;">PHYSICAL HARDWARE SPEEDS</div>
            <div style="margin-bottom: 14px;">
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #ef4444; font-weight: 700;">Random Disk Seek (HDD)</span>
                <span style="color: #ef4444;">~100 - 200 ops/sec</span>
              </div>
              <div style="height: 10px; background: #1e293b; border-radius: 5px; overflow: hidden;">
                <div style="height: 100%; width: 2%; background: #ef4444;"></div>
              </div>
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #10b981; font-weight: 700;">Sequential Append (LSM)</span>
                <span style="color: #10b981;">50,000 - 100,000+ ops/sec</span>
              </div>
              <div style="height: 10px; background: #1e293b; border-radius: 5px; overflow: hidden;">
                <div style="height: 100%; width: 95%; background: linear-gradient(90deg, #10b981, #3b82f6);"></div>
              </div>
            </div>
            <div style="margin-top: 16px; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 6px; padding: 10px; font-size: 12px; text-align: center; color: #93c5fd;">
              Measured Reference Engine Throughput: <strong>52,339 ± 14,096 ops/s</strong> (burst 85k ops/s)
            </div>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 15px; font-weight: 800; color: #60a5fa;">Sequential I/O Dominance</div>
              <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                Hard drive heads do not move; SSD Flash Translation Layers do not undergo erase-block churn. Data streams smoothly at physical bus saturation.
              </div>
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>Mechanical HDD:</strong> Bypasses 5–10 ms actuator arm seek penalties completely.<br/>
              • <strong>NVMe Solid-State:</strong> Eliminates page-rewriting block erasures, preserving flash memory lifespan.<br/>
              • <strong>Predictable Latency:</strong> Ingestion response times remain steady under extreme batching workloads.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Mechanical Disks (HDD): Random head seeks require 5–10 ms physical latency, whereas sequential writes stream at 150+ MB/s.",
            "Solid-State Drives (SSD): Random in-place updates trigger Flash Translation Layer (FTL) block erases and write amplification.",
            "Cassandra's pure sequential append architecture achieves 52,339 sustained ops/s (bursting to 85,000 ops/s) on standard hardware."
        ],
        "script_en": "The mechanical foundation of Cassandra's write performance is hardware physics. On spinning hard drives, random seeks force physical actuator arm repositioning, taking 5 to 10 milliseconds. On modern NVMe SSDs, random updates trigger block erase cycles in the Flash Translation Layer. By transforming all mutations into strictly sequential appends, Cassandra achieves over 52,000 sustained writes per second, bursting up to 85,000 on standard commodity hardware.",
        "script_vi": "Nền tảng cơ học cho tốc độ ghi của Cassandra xuất phát từ vật lý phần cứng. Trên ổ đĩa cơ HDD, tìm kiếm ngẫu nhiên bắt buộc đầu đọc cơ khí phải dịch chuyển, tốn từ 5 đến 10 mili-giây. Trên ổ SSD NVMe hiện đại, việc cập nhật ngẫu nhiên tại chỗ gây ra các chu kỳ xóa khối của tầng FTL. Bằng cách chuyển đổi mọi thao tác ghi thành luồng ghi tuần tự thuần túy, Cassandra đạt thông lượng bền vững hơn 52.000 lượt ghi/giây và đạt đỉnh 85.000 trên phần cứng phổ thông."
    },
    {
        "id": "slide-10",
        "section": "02 LSM & Cassandra",
        "badge": "Read Path Asymmetry",
        "title": "LSM Read Path: Bloom Fast-Fail vs. Positive Read Latency",
        "subtitle": "O(1) Negative Check (3.42 µs) vs. Multi-SSTable Traversal for Existing Keys",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 10px; padding: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 8px;">1. NEGATIVE LOOKUP: BLOOM FAST-FAIL</div>
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 6px; padding: 10px; font-size: 11.5px; color: #cbd5e1; margin-bottom: 10px;">
              Key absent $\\to$ 3 Hash functions check bit array (10 bits/key). Any bit = 0 $\\implies$ 100% guarantee key NOT in SSTable!
              <div style="margin-top: 6px; color: #34d399; font-weight: 700;">⚡ Fast-Fail Time: 3.42 µs (0 Disk Seeks)</div>
            </div>
            <div style="font-size: 13px; font-weight: 700; color: #fb7185; margin-bottom: 8px;">2. POSITIVE LOOKUP: MULTI-SSTABLE TRAVERSAL</div>
            <div style="background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 6px; padding: 10px; font-size: 11.5px; color: #cbd5e1;">
              Key exists $\\to$ Bloom filter matches. Cassandra must check MemTable, then traverse $L_0, L_1, L_2$, decode index fences and read data blocks until newest timestamp found.
              <div style="margin-top: 6px; color: #fb7185; font-weight: 700;">⚠️ Higher Read Amplification than B+ Tree!</div>
            </div>
          </div>
          <div>
            <div style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
              <div style="font-size: 14px; font-weight: 800; color: #60a5fa;">Asymmetric Point Read Latency</div>
              <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                While non-existent keys are eliminated in $O(1)$ RAM time, existing keys suffer higher read amplification in LSM than in balanced B+ Trees ($O(\\log N)$ disk page reads).
              </div>
            </div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              • <strong>10 Bits/Key Efficiency:</strong> In-memory bit array provides 99% negative pruning accuracy at negligible memory cost.<br/>
              • <strong>Tombstone Scanning:</strong> Positive reads must scan through deleted ranges until verifying whether a key is alive or dead.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Negative Read Path: In-memory Bloom filter (10 bits/key) computes $k$ hashes; a single 0-bit fast-fails in $3.42\\ \\mu\\text{s}$ with zero disk seeks.",
            "Positive Read Path: When keys exist, Bloom filter returns positive. The engine must traverse MemTable and multiple SSTable levels.",
            "Index Decoding: Positive point lookups must decode partition summaries and index fences to reconcile versions and tombstones.",
            "Read Amplification: LSM engines have higher positive point-read latency and amplification compared to balanced B+ Trees."
        ],
        "script_en": "Because SSTables are immutable, reading from an LSM-tree is inherently asymmetric. For non-existent keys, Cassandra checks an in-memory Bloom filter requiring only 10 bits per key; a single 0-bit skips disk access in just 3.4 microseconds. However, when the key does exist, Bloom filters yield positive hits, forcing Cassandra to traverse the MemTable and multiple SSTable levels, decoding index blocks until the newest timestamp is found. Thus, positive point reads suffer higher read amplification in LSM than in a balanced B+ Tree.",
        "script_vi": "Vì các SSTable là bất biến, luồng đọc trong cây LSM có tính chất bất đối xứng rõ rệt. Với khóa không tồn tại, Cassandra kiểm tra Bloom Filter trên RAM chỉ tốn 10 bit/khóa; chỉ cần một bit 0 là hủy tìm kiếm trong 3,4 micro-giây mà không cần đọc đĩa. Nhưng khi khóa có tồn tại, Bloom filter trả về dương tính, buộc hệ thống phải tra cứu qua MemTable và nhiều tầng SSTable, giải mã các khối chỉ mục để tìm bản ghi có timestamp mới nhất. Do đó, lượt đọc dương tính trong LSM chịu độ khuếch đại đọc lớn hơn cây B+."
    },
    {
        "id": "slide-11",
        "section": "02 LSM & Cassandra",
        "badge": "Anti-Pattern",
        "title": "Cassandra Warning: 'ALLOW FILTERING' Anti-Pattern",
        "subtitle": "Why Querying Non-Partition Keys Triggers Cluster-Wide Full Scans",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #ef4444; border-radius: 12px; padding: 20px;">
            <div style="font-family: monospace; font-size: 12px; color: #ef4444; background: #0f172a; padding: 10px; border-radius: 6px; border: 1px solid #7f1d1d; margin-bottom: 12px;">
              SELECT * FROM users<br/>
              WHERE email = 'user@hcmut.edu.vn'<br/>
              <span style="color: #fca5a5; font-weight: 700;">ALLOW FILTERING;</span> ⚠️
            </div>
            <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">
              Without the partition key, Cassandra cannot compute the hash ring token. It must broadcast the query to <strong>EVERY NODE</strong> in the cluster!
            </div>
          </div>
          <div>
            <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 15px; font-weight: 800; color: #fca5a5;">The Cluster Scatter-Gather Danger</div>
              <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                ALLOW FILTERING turns an $O(1)$ routed key-value lookup into an $O(N)$ full cluster scan across every SSTable on every storage node.
              </div>
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>Cascading Timeouts:</strong> All nodes saturate disk I/O scanning SSTables, triggering coordinator client timeouts.<br/>
              • <strong>Golden Rule:</strong> In Cassandra, you must design tables around your queries. One query pattern = One dedicated table.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Cassandra's primary key design uses consistent hashing on the Partition Key to route queries directly to the responsible node.",
            "`ALLOW FILTERING` forces the coordinator to scatter-gather the query to every node in the cluster.",
            "Every node must execute a full linear scan of all its SSTables, causing severe latency spikes and query timeouts."
        ],
        "script_en": "Because Cassandra executes partition key lookups in microseconds, developers often fall into a fatal anti-pattern: using ALLOW FILTERING. When you query by primary key, Cassandra hashes the key and routes directly to the single responsible node. But when you filter by a non-partition column with ALLOW FILTERING, the coordinator must broadcast the query to every node in the cluster, forcing each node to scan all its SSTables. This creates severe latency spikes and cluster outages under load.",
        "script_vi": "Bởi vì Cassandra tra cứu theo khóa chính trong vài micro-giây, các kỹ sư thường mắc phải một sai lầm chết người: sử dụng ALLOW FILTERING. Khi truy vấn bằng khóa phân vùng, Cassandra băm khóa và định tuyến thẳng đến đúng một node chịu trách nhiệm. Nhưng khi lọc theo một cột không phải khóa phân vùng kèm ALLOW FILTERING, node điều phối buộc phải phát tán truy vấn tới mọi node trong cụm, ép từng node phải quét qua tất cả các file SSTable của mình. Điều này gây bùng nổ độ trễ và làm tê liệt hệ thống khi có tải."
    },

    # ==========================================
    # SECTION 03: INVERTED INDEX & ES (Slides 12 - 16)
    # ==========================================
    {
        "id": "slide-12",
        "section": "03 Inverted Index & ES",
        "badge": "Search Paradigm",
        "title": "Search Paradigms: Linear Scan vs. Inverted Index",
        "subtitle": "From Exhausting Brute-Force (2,515.55 µs) to Direct Term Indexing (35.21 µs) — 71.5× Speedup",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
          <div class="book-mockup">
            <div class="book-spine"></div>
            <div class="book-lines">
              <div class="book-line"></div>
              <div class="book-line medium"></div>
              <div class="book-line short"></div>
              <div class="book-line"></div>
            </div>
            <div class="laser-bar"></div>
            <div style="background: #0f172a; border: 1px solid #ef4444; border-radius: 6px; padding: 8px; text-align: center; margin-left: 14px;">
              <span style="color: #f87171; font-weight: 700; font-size: 12px;">Linear Scan: 2,515.55 ± 182.40 µs</span>
              <div style="font-size: 10.5px; color: #94a3b8;">Scans every character of every document ($O(N \\cdot L)$)</div>
            </div>
          </div>
          <div>
            <div class="index-entry-card" style="margin-bottom: 12px;">
              <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <span class="index-letter-badge">D</span>
                <strong style="color: #6ee7b7; font-size: 14px;">"database" → [Doc 14, Doc 45, Doc 102]</strong>
              </div>
              <div style="font-size: 12px; color: #cbd5e1;">
                Direct jump to matching document IDs! Search time: <strong>35.21 ± 14.91 µs</strong>.
              </div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 12px 16px; border-radius: 6px;">
              <div style="font-size: 15px; font-weight: 800; color: #34d399;">71.5× Measured Speedup</div>
              <div style="font-size: 11.5px; color: #cbd5e1; margin-top: 4px; line-height: 1.4;">
                Instead of searching text inside documents, the inverted index maps words to documents ($O(1)$ dictionary lookup + postings traversal).
              </div>
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Linear Scan ($O(N \\cdot L)$): Must evaluate query string against every document sequentially; measured at $2,515.55 \\pm 182.40\\ \\mu\\text{s}$.",
            "Inverted Index ($O(1)$ term lookup): Inverts the relationship to map Terms $\\to$ Sorted Document Posting Lists.",
            "Direct Postings Access: Retrieves matching document arrays in $35.21 \\pm 14.91\\ \\mu\\text{s}$, achieving a verified $71.5\\times$ acceleration."
        ],
        "script_en": "Searching text without an index is like reading a 500-page book cover-to-cover to find a single mention. In our benchmarks across 1,655 quotes, an unindexed linear scan took 2,515 microseconds. The Inverted Index inverts this relationship: like the alphabetical index at the back of a book, it maps each term directly to an array of document IDs. Queries jump directly to matches in just 35 microseconds—delivering a verified 71.5-fold empirical speedup.",
        "script_vi": "Tìm kiếm văn bản không có chỉ mục giống như việc phải đọc từng trang một cuốn sách dày 500 trang để tìm một chữ. Trong thực nghiệm trên 1.655 danh ngôn, quét tuyến tính không chỉ mục tốn tới 2.515 micro-giây. Chỉ mục đảo (Inverted Index) đảo ngược mối quan hệ này: giống như mục lục tra cứu theo bảng chữ cái cuối cuốn sách, nó ánh xạ trực tiếp mỗi từ đến một danh sách mã tài liệu. Truy vấn nhảy thẳng tới kết quả chỉ trong 35 micro-giây — mang lại mức tăng tốc thực nghiệm 71,5 lần."
    },
    {
        "id": "slide-13",
        "section": "03 Inverted Index & ES",
        "badge": "Analysis & NRT Refresh",
        "title": "Text Analysis & NRT Refresh: The Lucene Ingestion Pipeline",
        "subtitle": "3-Stage Normalization Conveyor Belt and Bounded 1-Second Near-Real-Time (NRT) Refresh Lag",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 10px; padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">3-STAGE ANALYSIS CONVEYOR BELT</div>
            <div style="display: flex; gap: 8px; margin-bottom: 8px;">
              <div style="flex: 1; background: #0f172a; border: 1px solid #334155; padding: 6px; border-radius: 4px; font-size: 10.5px; text-align: center;">
                <strong style="color: #f59e0b;">1. Char Filter</strong><br/>Strip HTML & emojis
              </div>
              <div style="flex: 1; background: #0f172a; border: 1px solid #334155; padding: 6px; border-radius: 4px; font-size: 10.5px; text-align: center;">
                <strong style="color: #3b82f6;">2. Tokenizer</strong><br/>Split spaces & punct
              </div>
              <div style="flex: 1; background: #0f172a; border: 1px solid #334155; padding: 6px; border-radius: 4px; font-size: 10.5px; text-align: center;">
                <strong style="color: #10b981;">3. Token Filter</strong><br/>Lowercase + Stemming
              </div>
            </div>
            <div style="font-family: monospace; font-size: 11px; background: #0b0f19; padding: 8px; border-radius: 4px; color: #38bdf8; text-align: center;">
              "&lt;b&gt;Databases!&lt;/b&gt;" → "Databases!" → ["Databases"] → ["databas"]
            </div>
          </div>
          <div>
            <div style="background: rgba(6, 182, 212, 0.15); border-left: 4px solid #06b6d4; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
              <div style="font-size: 14px; font-weight: 800; color: #22d3ee;">Near-Real-Time (NRT) Model</div>
              <div style="font-size: 11.5px; color: #cbd5e1; margin-top: 4px; line-height: 1.4;">
                New documents append to memory buffer & translog. They are <strong>NOT searchable</strong> until an explicit or scheduled <code>refresh</code> (default: 1.0s) flushes memory into a new segment.
              </div>
            </div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              • <strong>Bounded Commit Lag:</strong> Elasticsearch is Near-Real-Time, not immediate read-your-writes.<br/>
              • <strong>Symmetric Pipeline:</strong> Query terms must pass through the identical analyzer to match root tokens.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Text Analysis Pipeline: Raw text passes through Character Filters, Tokenizers, and Token Filters (Porter stemming, lowercase).",
            "Symmetric Pipeline: Query strings must traverse the identical analysis pipeline to align with indexed tokens.",
            "Near-Real-Time (NRT) Mechanics: Documents are buffered in memory and appended to a translog; they are NOT immediately searchable.",
            "Bounded Refresh Lag: A scheduled refresh (default: 1.0 s) flushes memory into an immutable segment, creating a bounded commit lag."
        ],
        "script_en": "How does raw text become searchable? Lucene runs strings through a 3-stage conveyor belt: Character Filters remove markup, Tokenizers split words, and Token Filters lowercase and stem terms to root forms. But crucially, indexed documents are not immediately searchable. They are buffered in memory and appended to a translog, becoming searchable only after a scheduled or explicit refresh—defaulting to 1 second. This bounded commit lag defines Elasticsearch's Near-Real-Time consistency, distinct from immediate read-your-writes databases.",
        "script_vi": "Làm thế nào để văn bản tìm kiếm được? Lucene đưa chuỗi ký tự qua dây chuyền 3 bước: Bộ lọc ký tự gỡ thẻ HTML, Bộ tách từ chia từ đơn, và Bộ lọc từ chuyển chữ thường kèm rút gốc từ. Nhưng quan trọng hơn cả, tài liệu chưa thể tìm thấy ngay lập tức. Chúng được đệm trên RAM và ghi log vào translog, chỉ trở nên tìm kiếm được sau chu kỳ refresh định kỳ (mặc định 1 giây) để tạo ra segment mới. Độ trễ cam kết có hạn này tạo nên tính nhất quán Gần-Thời-Gian-Thực (NRT) của Elasticsearch, khác biệt với tính nhất quán đọc ngay của cơ sở dữ liệu khóa chính."
    },
    {
        "id": "slide-14",
        "section": "03 Inverted Index & ES",
        "badge": "Fast Intersection",
        "title": "Finding Multiple Words: Skip Pointers in Posting Lists",
        "subtitle": "Intersecting Sorted Document IDs with Express Highway Leaps (33.69 µs)",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px; margin-top: 10px;">
          <div style="margin-bottom: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">POSTING LIST A ("database"):</div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <span style="background: #1e293b; border: 1px solid #3b82f6; padding: 4px 10px; border-radius: 4px; font-size: 12px;">Doc 10</span>
              <span style="background: #1e293b; border: 1px solid #3b82f6; padding: 4px 10px; border-radius: 4px; font-size: 12px;">Doc 25</span>
              <span style="background: #2563eb; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 800;">Doc 60 (Match)</span>
              <span style="background: #1e293b; border: 1px solid #3b82f6; padding: 4px 10px; border-radius: 4px; font-size: 12px;">Doc 85</span>
            </div>
          </div>
          <div style="margin-bottom: 16px;">
            <div style="font-size: 13px; font-weight: 700; color: #22d3ee; margin-bottom: 6px;">POSTING LIST B ("search"):</div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
              <span style="background: #1e293b; border: 1px solid #06b6d4; padding: 4px 10px; border-radius: 4px; font-size: 12px;">Doc 2</span>
              <span style="color: #64748b; font-size: 11px;">→ (skip) →</span>
              <span style="background: #0891b2; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 800;">Doc 60 (Match)</span>
              <span style="background: #1e293b; border: 1px solid #06b6d4; padding: 4px 10px; border-radius: 4px; font-size: 12px;">Doc 95</span>
            </div>
          </div>
          <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: #a7f3d0;">
            ⚡ <strong>Skip Pointers Leapfrog Highway:</strong> Embedded pointers spaced every $\\sqrt{|P|}$ items allow List B to leap over dozens of documents without inspecting each ID. Multi-term intersection completes in <strong>33.69 µs</strong>.
          </div>
        </div>
        """,
        "key_points": [
            "Boolean AND queries require computing the intersection of multiple sorted posting lists: $P_1 \\cap P_2$.",
            "Standard merge check is $O(|P_1| + |P_2|)$; Skip Pointers placed every $\\sqrt{|P|}$ elements enable sub-linear leapfrogging.",
            "If pointer on List A is at Doc 60, List B skips directly over lower intervals without sequential evaluation."
        ],
        "script_en": "When searching for multiple terms such as 'write AND search', Elasticsearch must intersect their sorted posting lists. Instead of checking every document ID sequentially, Lucene uses Skip Pointers—express lane bridges embedded every square-root-of-P entries. If list A points to Document 60, list B can leapfrog dozens of smaller IDs instantly. In our implementation, this sub-linear leapfrogging evaluates complex multi-term intersections in just 33.69 microseconds.",
        "script_vi": "Khi tìm kiếm nhiều từ đồng thời như 'write AND search', Elasticsearch phải tìm phần giao của các danh sách posting đã sắp xếp. Thay vì kiểm tra từng mã tài liệu một cách tuần tự, Lucene chèn các con trỏ nhảy (Skip Pointers) theo chu kỳ căn bậc hai của P phần tử. Nếu danh sách A đang ở tài liệu 60, danh sách B có thể nhảy cóc qua hàng chục tài liệu nhỏ hơn ngay lập tức. Trong mã nguồn của nhóm, thuật toán nhảy dưới tuyến tính này xử lý phép giao nhiều từ chỉ trong 33,69 micro-giây."
    },
    {
        "id": "slide-15",
        "section": "03 Inverted Index & ES",
        "badge": "Relevance Ranking",
        "title": "Okapi BM25: Principles & Mathematical Formulation",
        "subtitle": "Probabilistic Scoring: IDF Weighting, k1=1.2 Term Saturation, and b=0.75 Length Normalization",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 10px; padding: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">OKAPI BM25 EQUATION</div>
            <div style="background: #0f172a; padding: 10px; border-radius: 6px; border: 1px solid #1e293b; font-size: 12px; margin-bottom: 10px;">
              $$\\text{Score}(D, Q) = \\sum_{t \\in Q} \\text{IDF}(t) \\cdot \\frac{\\text{TF}(t, D) \\cdot (k_1 + 1)}{\\text{TF}(t, D) + k_1 \\cdot \\left(1 - b + b \\cdot \\frac{|D|}{\\text{avgdl}}\\right)}$$
            </div>
            <div style="font-size: 11px; color: #94a3b8; line-height: 1.4;">
              • $\\mathbf{k_1 = 1.2}$: Limits term frequency impact (diminishing returns).<br/>
              • $\\mathbf{b = 0.75}$: Penalizes verbose documents; rewards short focused matches.
            </div>
          </div>
          <div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
              <div style="font-size: 14px; font-weight: 800; color: #34d399;">The 3 Intuitive Rules</div>
              <div style="font-size: 11.5px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                <strong>1. Rare Words Win (IDF):</strong> Common words like "the" get zero score.<br/>
                <strong>2. Anti-Spam Ceiling:</strong> Repeating a word 100 times does not multiply score.<br/>
                <strong>3. Short Document Bonus:</strong> Keyword in a short title scores higher.
              </div>
            </div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              Evaluates top-5 ranked quotes in <strong>118.40 µs</strong> with exact mathematical ranking.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Okapi BM25 is the gold standard probabilistic relevance framework in modern search engines.",
            "Inverse Document Frequency (IDF): Penalizes common stopwords while heavily rewarding discriminative terms.",
            "Term Frequency Saturation ($k_1=1.2$): Enforces an asymptotic upper bound to prevent keyword stuffing.",
            "Document Length Normalization ($b=0.75$): Penalizes long verbose documents in favor of concise, targeted matches."
        ],
        "script_en": "Finding matching documents is only half the battle; ranking the best match requires Okapi BM25. BM25 combines three principles: Inverse Document Frequency rewards rare terms, parameter k1 at 1.2 enforces term frequency saturation to prevent keyword stuffing, and parameter b at 0.75 penalizes verbose documents. In our implementation, this formula evaluates top-5 ranked quotes in 118 microseconds, separating high-relevance matches cleanly.",
        "script_vi": "Tìm thấy tài liệu chỉ mới là một nửa chặng đường; xếp hạng tài liệu phù hợp nhất cần thuật toán Okapi BM25. BM25 kết hợp 3 nguyên tắc: IDF chấm điểm cao cho từ hiếm, tham số k1 bằng 1.2 tạo trần bão hòa tần suất từ để chống spam từ khóa, và tham số b bằng 0.75 phạt tài liệu quá dài. Trong cài đặt của nhóm, công thức này tính toán top 5 kết quả chỉ trong 118 micro-giây, tách biệt chính xác tài liệu liên quan nhất."
    },
    {
        "id": "slide-16",
        "section": "03 Inverted Index & ES",
        "badge": "The RUM Trade-Off",
        "title": "The Cost of Fast Search: 15× Memory Amplification",
        "subtitle": "Measuring RUM Space: 2,293 Bytes/Doc (ES) vs. 154 Bytes/Key (Cassandra)",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px;">
            <div style="font-size: 13px; color: #94a3b8; font-weight: 700; margin-bottom: 14px;">EMPIRICAL MEMORY FOOTPRINT (RAM)</div>
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #60a5fa; font-weight: 700;">Cassandra KV Store</span>
                <span style="color: #60a5fa;">153.7 Bytes/Key</span>
              </div>
              <div style="height: 12px; background: #1e293b; border-radius: 6px; overflow: hidden;">
                <div style="height: 100%; width: 7%; background: #3b82f6;"></div>
              </div>
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span style="color: #22d3ee; font-weight: 700;">Elasticsearch Inverted Index</span>
                <span style="color: #22d3ee;">2,292.8 Bytes/Doc</span>
              </div>
              <div style="height: 12px; background: #1e293b; border-radius: 6px; overflow: hidden;">
                <div style="height: 100%; width: 100%; background: linear-gradient(90deg, #06b6d4, #f43f5e);"></div>
              </div>
            </div>
            <div style="margin-top: 16px; background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 6px; padding: 10px; text-align: center; color: #fca5a5; font-size: 13px; font-weight: 800;">
              Memory Amplification: 14.9× (~15× More RAM)
            </div>
          </div>
          <div>
            <div style="background: rgba(244, 63, 94, 0.15); border-left: 4px solid #f43f5e; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px;">
              <div style="font-size: 15px; font-weight: 800; color: #fb7185;">The Memory (M) Price of Read (R) Speed</div>
              <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                Elasticsearch must precompute and retain term dictionaries, posting lists, skip pointer arrays, and document length tables in RAM.
              </div>
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
              • <strong>Cassandra Thrift:</strong> Needs only 10 bits per key for Bloom filters + sparse index fences.<br/>
              • <strong>Elasticsearch Greed:</strong> Needs inverted pointers for every unique token across all fields.<br/>
              • <strong>Direct RUM Proof:</strong> Minimizing Read latency pushes Memory overhead to the maximum limit.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Empirical Memory Footprint: Cassandra consumes 153.7 Bytes/key vs. Elasticsearch consuming 2,292.8 Bytes/doc.",
            "Elasticsearch precomputes and maintains extensive in-memory auxiliary structures: term dictionaries, skip lists, document lengths.",
            "Confirms RUM Memory ($M$) trade-off: microsecond search latency requires paying a $15\\times$ RAM overhead premium."
        ],
        "script_en": "There is no free lunch in computer science. To achieve 35-microsecond boolean search, Elasticsearch pays an enormous price in memory. While Cassandra requires only 154 bytes per key in RAM for its Bloom filters and index fences, Elasticsearch consumes nearly 2,300 bytes per document to store posting lists and term dictionaries. That is a measured 14.9-to-1 memory ratio, providing concrete empirical proof of the RUM Conjecture.",
        "script_vi": "Không có bữa trưa nào miễn phí trong khoa học máy tính. Để đạt được tốc độ tìm kiếm 35 micro-giây, Elasticsearch phải trả một cái giá khổng lồ về bộ nhớ. Trong khi Cassandra chỉ cần 154 byte cho mỗi khóa trên RAM cho Bloom Filter và con trỏ chỉ mục, Elasticsearch tiêu tốn gần 2.300 byte cho mỗi tài liệu để lưu trữ danh sách posting và từ điển thuật ngữ. Tỷ lệ chênh lệch bộ nhớ 14,9 lần này là minh chứng thực nghiệm sống động cho Giả thuyết RUM."
    },

    # ==========================================
    # SECTION 04: SYNTHESIS & INSIGHTS (Slides 17 - 19)
    # ==========================================
    {
        "id": "slide-17",
        "section": "04 Synthesis",
        "badge": "Master's Insight",
        "title": "Architectural Convergence: Lucene Segments as LSM-Trees",
        "subtitle": "The Hidden Symmetry: Why Inverted Index Lifecycle Mirrors the LSM Storage Architecture",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 20px; margin-top: 10px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid #334155; color: #94a3b8;">
                <th style="padding: 8px 12px;">Storage Lifecycle Phase</th>
                <th style="padding: 8px 12px; color: #60a5fa;">Cassandra (LSM-Tree)</th>
                <th style="padding: 8px 12px; color: #22d3ee;">Elasticsearch (Lucene Index)</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 8px 12px; font-weight: 700; color: #f3f4f6;">1. In-Memory Ingestion</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">MemTable (Sorted SkipList in RAM)</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">In-Memory Document Buffer (RAM)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 8px 12px; font-weight: 700; color: #f3f4f6;">2. Crash-Safety WAL</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">CommitLog (Append-only on disk)</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">Lucene Translog (Append-only on disk)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 8px 12px; font-weight: 700; color: #f3f4f6;">3. Immutable Disk Unit</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">SSTable (.db, .idx immutable files)</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">Lucene Segment (.tim, .doc, .fdt files)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 8px 12px; font-weight: 700; color: #f3f4f6;">4. Deletion Mechanics</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">Tombstone Marker appended to stream</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">Soft Deletion Bitset (.del file)</td>
              </tr>
              <tr>
                <td style="padding: 8px 12px; font-weight: 700; color: #f3f4f6;">5. Background Maintenance</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">Compaction (Leveled / STCS)</td>
                <td style="padding: 8px 12px; color: #cbd5e1;">Segment Merging (TieredMergePolicy)</td>
              </tr>
            </tbody>
          </table>
          <div style="margin-top: 16px; background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 6px; font-size: 12.5px; color: #e2e8f0;">
            💡 <strong>The Master's Insight:</strong> Inverted posting lists cannot be updated in-place without prohibitive sorting costs. Therefore, Lucene internally organizes its segments using the <strong>exact same lifecycle as an LSM-Tree</strong>! Elasticsearch is fundamentally an LSM-Tree whose payload is an inverted index.
          </div>
        </div>
        """,
        "key_points": [
            "Structural Convergence: Modifying sorted posting lists in-place is computationally prohibitive.",
            "Lucene solves this by implementing the exact same lifecycle as an LSM-Tree: In-Memory Buffer, Translog WAL, Immutable Segments, and Tiered Merge Compaction.",
            "Deletions in both engines are non-destructive (Tombstones vs .del bitsets) and purged only during background merging.",
            "Master's Insight: Elasticsearch and Cassandra do not belong to disjoint worlds; Elasticsearch is an LSM-Tree with an inverted index payload."
        ],
        "script_en": "Here is the key architectural revelation of our Master's study: while Cassandra and Elasticsearch appear to be opposite paradigms, their internal storage engines converge on the exact same lifecycle. Inverted posting lists cannot be modified in-place without prohibitive sorting costs. Therefore, Lucene internally functions as an LSM-Tree: incoming documents buffer in memory with a translog, flush to immutable on-disk segments identical to SSTables, and merge in the background via TieredMergePolicy. Elasticsearch does not reject LSM; it implements an LSM-Tree whose payload is an inverted index.",
        "script_vi": "Đây là phát hiện kiến trúc quan trọng nhất trong nghiên cứu cao học của nhóm: dù Cassandra và Elasticsearch có vẻ đối lập, bộ máy lưu trữ bên trong của chúng lại hội tụ về đúng một vòng đời. Danh sách posting không thể sửa đổi tại chỗ nếu không muốn tốn chi phí sắp xếp lại toàn bộ. Vì vậy, Lucene tổ chức hoạt động y hệt một cây LSM: dữ liệu ghi vào bộ đệm RAM kèm translog, xả định kỳ thành các segment bất biến tương đương SSTable, và hòa trộn ngầm ở chế độ nền qua TieredMergePolicy. Elasticsearch không hề phủ nhận LSM; nó chính là một cây LSM với phần tải trọng là chỉ mục đảo."
    },
    {
        "id": "slide-18",
        "section": "04 Synthesis",
        "badge": "Comparison Matrix",
        "title": "Comparing Both Systems: The 5W1H Matrix",
        "subtitle": "Direct Architectural Contrast Across Workloads, Data Layouts, and RUM Compromises",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 18px; margin-top: 10px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid #334155; color: #94a3b8;">
                <th style="padding: 6px 10px; width: 80px;">Dimension</th>
                <th style="padding: 6px 10px; color: #60a5fa;">Apache Cassandra (LSM)</th>
                <th style="padding: 6px 10px; color: #22d3ee;">Elasticsearch (Inverted Index)</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f3f4f6;">WHAT</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Distributed wide-column store for high-throughput appends</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Distributed full-text search and analytical query engine</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f3f4f6;">WHY</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Zero in-place overwrite overhead; maximize ingestion bandwidth</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Microsecond ad-hoc text search and relevance ranking</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f3f4f6;">WHERE</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">System of Record: Time-series telemetry, financial ledgers</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Search View: E-commerce catalogs, log analysis (ELK)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f3f4f6;">WHEN</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Known query access patterns supplying partition keys</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Unpredictable ad-hoc multi-term text queries with scoring</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 10px; font-weight: 700; color: #f3f4f6;">WHO</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">IoT telemetry pipelines, messaging backbones (Discord, Uber)</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Search teams, observability engineers (GitHub, Wikipedia)</td>
              </tr>
              <tr>
                <td style="padding: 6px 10px; font-weight: 700; color: #f3f4f6;">HOW (RUM)</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Optimizes <strong>(U, M)</strong>: Append-only MemTable + 10-bit Bloom</td>
                <td style="padding: 6px 10px; color: #cbd5e1;">Optimizes <strong>(R)</strong>: Inverted posting lists + Okapi BM25</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "key_points": [
            "What: Distributed wide-column store (Cassandra) vs. Distributed text search engine (Elasticsearch).",
            "Why: Maximize write throughput & primary-key reads vs. Maximize ad-hoc text search & ranked relevance.",
            "Where: System of Record for time-series & transactions vs. Read-optimized Search View.",
            "How: Append-only MemTable & SSTable compaction vs. Tokenization pipeline & posting list segment merging."
        ],
        "script_en": "To synthesize both technologies, we apply the 5W1H framework. Cassandra's 'What' is a distributed wide-column store designed for high-throughput appends where queries always supply the partition key. Elasticsearch's 'What' is a distributed search engine designed for ad-hoc multi-term queries with relevance scoring. Cassandra is the secure bank vault; Elasticsearch is the searchable storefront display. Each excels only when applied to the workload it was physically designed to solve.",
        "script_vi": "Để tổng hợp cả hai công nghệ, nhóm áp dụng khung phân tích 5W1H. Về bản chất, Cassandra là cơ sở dữ liệu dạng cột phân tán cho luồng ghi tốc độ cao với các truy vấn luôn có khóa phân vùng. Elasticsearch là công cụ tìm kiếm phân tán cho các truy vấn văn bản phức tạp với tính điểm liên quan. Cassandra đóng vai trò két sắt ngân hàng; Elasticsearch là cửa sổ trưng bày sản phẩm. Mỗi hệ thống chỉ phát huy tối đa sức mạnh khi được đặt đúng vào bài toán mà cấu trúc vật lý của nó hướng tới."
    },
    {
        "id": "slide-19",
        "section": "04 Synthesis",
        "badge": "Physical Law",
        "title": "The Trade-Off Space: RUM Conjecture",
        "subtitle": "Cassandra at (U, M) vs. Elasticsearch at (R) — Proof Neither Can Replace the Other",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 18px; text-align: center;">
            <div style="font-size: 13px; font-weight: 700; color: #38bdf8; margin-bottom: 10px;">RUM CONJECTURE TRADE-OFF SPACE</div>
            <div style="background: #0f172a; border-radius: 8px; padding: 14px; border: 1px solid #1e293b; text-align: left; font-size: 12px; line-height: 1.6;">
              <div style="color: #60a5fa; margin-bottom: 6px;">
                <strong>Cassandra Anchor:</strong> Optimizes $U$ & $M$. Fast writes ($52k+$ ops/s) + compact memory ($154$ B/key). Fails on ad-hoc text search without partition keys.
              </div>
              <div style="color: #22d3ee; margin-bottom: 6px;">
                <strong>Elasticsearch Anchor:</strong> Optimizes $R$. Microsecond search ($35\\ \\mu\\text{s}$) + BM25 ranking. Pays with high RAM ($2,293$ B/doc) and heavy index merge maintenance.
              </div>
              <div style="color: #f87171; font-weight: 700; border-top: 1px solid #334155; padding-top: 6px;">
                Center Triangle: Impossible. No single database can occupy all three vertices.
              </div>
            </div>
          </div>
          <div>
            <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
              <div style="font-size: 14px; font-weight: 800; color: #34d399;">Pareto Optimal Architecture</div>
              <div style="font-size: 11.5px; color: #cbd5e1; margin-top: 4px; line-height: 1.4;">
                Neither engine can replace the other. Attempting to force full-text search into Cassandra requires disastrous full scans; forcing high-velocity writes into Elasticsearch triggers merge thrashing.
              </div>
            </div>
            <div style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
              • <strong>Specialization Inevitability:</strong> The RUM Conjecture mandates architectural duality.<br/>
              • <strong>Engineering Solution:</strong> Coordinate both engines via event-driven replication.
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Mathematical Proof of Specialization: The RUM trade-off space is Pareto-optimal.",
            "Cassandra cannot support microsecond arbitrary search without ballooning its memory and stalling writes.",
            "Elasticsearch cannot accept 50k+ continuous random writes without crippling its segment merge pipeline."
        ],
        "script_en": "When we map both engines onto the RUM Conjecture triangle, their complementary nature becomes mathematically undeniable. Cassandra prioritizes Update and Memory overhead; Elasticsearch prioritizes Read latency. No engineer can break this law; choosing an engine is fundamentally choosing which corner of the trade-off space your application requires. Neither engine can replace the other without violating physical storage limits.",
        "script_vi": "Khi đối chiếu cả hai hệ thống lên tam giác Giả thuyết RUM, tính chất bổ trợ lẫn nhau của chúng trở nên hiển nhiên về mặt toán học. Cassandra ưu tiên chi phí Ghi và Bộ nhớ; Elasticsearch ưu tiên độ trễ Đọc. Không một kỹ sư nào có thể phá vỡ quy luật này; việc chọn database thực chất là chọn góc đánh đổi phù hợp với bài toán của mình. Không hệ thống nào có thể thay thế hoàn toàn hệ thống kia mà không vi phạm các giới hạn vật lý."
    },

    # ==========================================
    # SECTION 05: EXPERIMENTS (Slides 20 - 21)
    # ==========================================
    {
        "id": "slide-20",
        "section": "05 Experiments",
        "badge": "Methodology & Qs",
        "title": "Experimental Setup & Research Questions",
        "subtitle": "Zero-Dependency Reference Engines Tested Across 10,000 Cities and 1,655 Quotes",
        "visual_html": """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
          <div style="background: #111827; border: 1px solid #374151; border-radius: 10px; padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">REFERENCE ENGINE ARTIFACTS</div>
            <div style="background: #0f172a; padding: 8px 12px; border-radius: 4px; margin-bottom: 8px; font-size: 11.5px; border-left: 3px solid #3b82f6;">
              <strong style="color: #60a5fa;">Cassandra Reference:</strong> MemTable (SkipList) + CommitLog + immutable SSTables + 10-bit Bloom Filter + compaction.
            </div>
            <div style="background: #0f172a; padding: 8px 12px; border-radius: 4px; font-size: 11.5px; border-left: 3px solid #06b6d4;">
              <strong style="color: #22d3ee;">Elasticsearch Reference:</strong> 3-stage text analysis + Porter stemmer + sorted postings + skip pointers + Okapi BM25.
            </div>
            <div style="margin-top: 8px; font-size: 11px; color: #94a3b8; text-align: center;">
              100% Pure Python (Zero pip dependencies) • Isolates storage algorithms from OS cache skew.
            </div>
          </div>
          <div>
            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px; font-size: 11.5px; line-height: 1.5;">
              <div style="color: #fbbf24; font-weight: 800; font-size: 12.5px; margin-bottom: 6px;">4 Research Questions (Hypotheses)</div>
              • <strong>Q1 (Write Speed):</strong> Does LSM outpace B+ Tree in sustained write throughput?<br/>
              • <strong>Q2 (Bloom Pruning):</strong> Can Bloom filters eliminate 100% of disk reads on absent keys?<br/>
              • <strong>Q3 (Search Speed):</strong> Does inverted indexing achieve &gt;50× speedup over linear scan?<br/>
              • <strong>Q4 (Memory Ratio):</strong> Does inverted indexing consume &gt;10× more RAM than KV store?
            </div>
          </div>
        </div>
        """,
        "key_points": [
            "Clean-Room Methodology: Implemented reference engines in pure Python without external dependencies.",
            "Eliminates JVM garbage collection pauses, network latency jitter, and OS page cache distortions.",
            "Datasets: 10,000 World Cities (KV lookup) and 1,655 Historical Quotes (full-text multi-term search).",
            "Formulated 4 specific research hypotheses (Q1 through Q4) to evaluate against the RUM Conjecture."
        ],
        "script_en": "To conduct rigorous scientific benchmarks, we implemented zero-dependency reference storage engines in pure Python. This eliminates network latency, operating system page cache noise, and JVM garbage collection artifacts. We evaluate both engines across two datasets: 10,000 world cities for key-value telemetry, and 1,655 historical quotes for full-text queries. We formulated four specific research questions to test write scalability, Bloom filter fast-fails, lexical search acceleration, and memory overhead.",
        "script_vi": "Để thực hiện đo đạc khoa học và công bằng, nhóm đã tự cài đặt các bộ máy lưu trữ tham chiếu không phụ thuộc thư viện ngoài bằng Python thuần. Cách tiếp cận này loại bỏ hoàn toàn nhiễu từ bộ thu dọn rác JVM, độ trễ mạng và bộ đệm trang của hệ điều hành. Nhóm thử nghiệm trên hai bộ dữ liệu thực tế: 10.000 thành phố cho truy vấn khóa-giá trị, và 1.655 danh ngôn cho truy vấn tìm kiếm toàn văn. Bốn câu hỏi nghiên cứu được đặt ra để kiểm chứng tốc độ ghi, bộ lọc Bloom, độ tăng tốc tìm kiếm và tỷ lệ chiếm dụng bộ nhớ."
    },
    {
        "id": "slide-21",
        "section": "05 Experiments",
        "badge": "Live Demo",
        "title": "Live Demonstration: Reproducible Pipeline",
        "subtitle": "Single-Command End-to-End Execution via Terminal (demo.py) and Google Colab",
        "visual_html": """
        <div style="background: #0f172a; border: 2px solid #334155; border-radius: 10px; padding: 18px; margin-top: 10px; font-family: monospace;">
          <div style="display: flex; gap: 6px; margin-bottom: 12px;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: #ef4444;"></div>
            <div style="width: 10px; height: 10px; border-radius: 50%; background: #f59e0b;"></div>
            <div style="width: 10px; height: 10px; border-radius: 50%; background: #10b981;"></div>
            <span style="color: #94a3b8; font-size: 11px; margin-left: 8px;">bash — python3 demo.py --no-pause</span>
          </div>
          <div style="font-size: 12px; color: #e2e8f0; line-height: 1.6;">
            <span style="color: #38bdf8;">$ python3 demo.py --no-pause</span><br/>
            <span style="color: #34d399;">[✓] PART 1: LSM Cassandra writes 10,000 cities</span> → Flush 1 SSTable in 0.19s (52,339 ops/s)<br/>
            <span style="color: #34d399;">[✓] PART 2: Bloom Filter Fast-Fail</span> → Key "Atlantis" pruned in 3.42 µs (0 disk I/O)<br/>
            <span style="color: #34d399;">[✓] PART 3: Inverted Index Search</span> → Multi-term AND evaluated in 35.21 µs (71.5× speedup)<br/>
            <span style="color: #34d399;">[✓] PART 4: Okapi BM25 Ranking</span> → Top quote scored 1.92 in 118.40 µs<br/>
            <span style="color: #34d399;">[✓] PART 5: Memory Footprint</span> → Cassandra: 153.7 B/key vs. ES: 2,292.8 B/doc (14.9× RAM ratio)<br/>
            <span style="color: #fbbf24;">[SUMMARY] All 25 automated invariant tests passed cleanly (pytest tests/).</span>
          </div>
        </div>
        """,
        "key_points": [
            "Fully reproducible artifact: executable locally via `python3 demo.py` or via interactive Google Colab notebook.",
            "Automated test suite with 25 unit tests asserting internal invariants (immutability, skip list leapfrogging, BM25 ordering).",
            "Live demonstration executes end-to-end benchmarking in under 60 seconds."
        ],
        "script_en": "Our implementation is 100% reproducible. By running a single command, 'python3 demo.py --no-pause', examiners can verify every mechanism executing in real time: MemTable batching, immutable SSTable flushes, Bloom filter fast-fails in 3 microseconds, and multi-term BM25 ranking across real datasets. An accompanying unit test suite of 25 automated tests validates all internal invariants.",
        "script_vi": "Mã nguồn của đồ án có tính tái lập 100%. Chỉ với một dòng lệnh 'python3 demo.py --no-pause', Hội đồng có thể kiểm chứng trực tiếp từng cơ chế đang chạy: MemTable nhận dữ liệu, xả file SSTable bất biến, Bloom Filter hủy tìm kiếm trong 3 micro-giây và thuật toán BM25 xếp hạng danh ngôn. Bộ kiểm thử tự động gồm 25 unit test đi kèm đảm bảo tính đúng đắn của mọi bất biến bên trong."
    },

    # ==========================================
    # SECTION 06: RESULTS (Slide 22)
    # ==========================================
    {
        "id": "slide-22",
        "section": "06 Results",
        "badge": "Scorecard & Proofs",
        "title": "Empirical Scorecard & Hypothesis Validation",
        "subtitle": "5-Round Statistical Benchmarks (µ ± σ) Confirming Hypotheses Q1 Through Q4",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 16px; margin-top: 10px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 11.5px; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid #334155; color: #94a3b8;">
                <th style="padding: 6px 8px;">Metric / Operation</th>
                <th style="padding: 6px 8px;">Linear / Baseline</th>
                <th style="padding: 6px 8px; color: #34d399;">Engine Implementation</th>
                <th style="padding: 6px 8px; color: #38bdf8;">Speedup / Ratio</th>
                <th style="padding: 6px 8px; color: #fbbf24;">Hypothesis</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 8px; font-weight: 700;">Cassandra Ingestion</td>
                <td style="padding: 6px 8px; color: #94a3b8;">~1,500 ops/s (B+ page flush)</td>
                <td style="padding: 6px 8px; color: #34d399; font-weight: 700;">52,339 ± 14,096 ops/s</td>
                <td style="padding: 6px 8px; color: #38bdf8;">~35× Write Ingestion</td>
                <td style="padding: 6px 8px; color: #fbbf24;"><strong>Q1 Confirmed</strong> (LSM Write Superiority)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 8px; font-weight: 700;">Bloom Filter Fast-Fail</td>
                <td style="padding: 6px 8px; color: #94a3b8;">150.0 µs (Disk Seek)</td>
                <td style="padding: 6px 8px; color: #34d399; font-weight: 700;">3.42 µs (Absent Key)</td>
                <td style="padding: 6px 8px; color: #38bdf8;">100% Disk Pruning</td>
                <td style="padding: 6px 8px; color: #fbbf24;"><strong>Q2 Confirmed</strong> (Zero Disk I/O on Miss)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 8px; font-weight: 700;">Full-Text Search (AND)</td>
                <td style="padding: 6px 8px; color: #94a3b8;">2,515.55 ± 182.40 µs</td>
                <td style="padding: 6px 8px; color: #34d399; font-weight: 700;">35.21 ± 14.91 µs</td>
                <td style="padding: 6px 8px; color: #38bdf8; font-weight: 800;">71.5× Acceleration</td>
                <td style="padding: 6px 8px; color: #fbbf24;"><strong>Q3 Confirmed</strong> (Posting List Traversal)</td>
              </tr>
              <tr style="border-bottom: 1px solid #1e293b;">
                <td style="padding: 6px 8px; font-weight: 700;">Okapi BM25 Ranking</td>
                <td style="padding: 6px 8px; color: #94a3b8;">N/A (No relevance)</td>
                <td style="padding: 6px 8px; color: #34d399; font-weight: 700;">118.40 ± 24.32 µs</td>
                <td style="padding: 6px 8px; color: #38bdf8;">Top-5 Probabilistic Score</td>
                <td style="padding: 6px 8px; color: #fbbf24;"><strong>Q3 Confirmed</strong> (Ranked Retrieval)</td>
              </tr>
              <tr>
                <td style="padding: 6px 8px; font-weight: 700;">Memory Footprint (RAM)</td>
                <td style="padding: 6px 8px; color: #94a3b8;">153.7 Bytes/Key (Cassandra)</td>
                <td style="padding: 6px 8px; color: #f43f5e; font-weight: 700;">2,292.8 Bytes/Doc (ES)</td>
                <td style="padding: 6px 8px; color: #f43f5e; font-weight: 800;">14.9× RAM Overhead</td>
                <td style="padding: 6px 8px; color: #fbbf24;"><strong>Q4 Confirmed</strong> (RUM Space Penalty)</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "key_points": [
            "Q1 Confirmed: Cassandra sustains 52,339 ops/s (bursting to 85,000 ops/s), validating append-only throughput.",
            "Q2 Confirmed: Bloom filters achieve 100% negative pruning in 3.42 µs, completely eliminating disk seeks on absent keys.",
            "Q3 Confirmed: Inverted index accelerates search by 71.5× (35.21 µs vs 2,515.55 µs scan); BM25 top-5 completes in 118.40 µs.",
            "Q4 Confirmed: Precomputing term posting lists requires 14.9× more memory (2,292.8 B/doc vs 153.7 B/key)."
        ],
        "script_en": "Our empirical scorecard across five statistical trials confirms all four research hypotheses. For Q1, Cassandra delivers over 52,000 writes per second sustained throughput, reaching 85,000 in burst. For Q2, Bloom filters achieve 100% pruning on absent keys in 3.4 to 6.2 microseconds with zero disk I/O. For Q3, inverted index boolean queries execute in 35 microseconds—a 71.5-fold speedup over linear scanning. For Q4, precomputing term dictionaries incurs an exact 14.9-fold memory overhead. The empirical data matches theoretical RUM boundaries.",
        "script_vi": "Bảng điểm thực nghiệm qua 5 lần chạy lặp lại khẳng định cả 4 giả thuyết nghiên cứu. Với Q1, Cassandra đạt tốc độ ghi bền vững hơn 52.000 thao tác/giây, đạt đỉnh 85.000 thao tác/giây. Với Q2, Bloom Filter loại trừ 100% lượt đọc đĩa trên khóa không tồn tại chỉ trong 3,4 đến 6,2 micro-giây. Với Q3, truy vấn chỉ mục đảo hoàn tất trong 35 micro-giây — tăng tốc 71,5 lần so với quét tuyến tính. Với Q4, việc tính trước từ điển thuật ngữ tiêu tốn chính xác gấp 14,9 lần RAM. Số liệu thực nghiệm hoàn toàn khớp với biên lý thuyết của Giả thuyết RUM."
    },

    # ==========================================
    # SECTION 07: ARCHITECTURE & CONCLUSION (Slide 23)
    # ==========================================
    {
        "id": "slide-23",
        "section": "07 Architecture & Conclusion",
        "badge": "CQRS & Verdict",
        "title": "Dual-Engine CQRS Architecture & Final Defense Verdict",
        "subtitle": "Bank Vault (Cassandra) + Storefront Window (ES) via CDC/Kafka & 3 Golden Rules",
        "visual_html": """
        <div style="background: #111827; border: 2px solid #374151; border-radius: 12px; padding: 18px; margin-top: 8px;">
          <!-- CQRS Pipeline -->
          <div style="display: grid; grid-template-columns: 1fr 40px 1fr 40px 1fr; align-items: center; gap: 8px; margin-bottom: 14px;">
            <div style="background: rgba(59, 130, 246, 0.15); border: 2px solid #3b82f6; border-radius: 8px; padding: 10px; text-align: center;">
              <div style="font-size: 13px; font-weight: 800; color: #60a5fa;">🏦 BANK VAULT</div>
              <div style="font-size: 11px; color: #cbd5e1;">Cassandra SoR (Immutable Log)</div>
            </div>
            <div style="text-align: center; color: #f59e0b; font-weight: 900; font-size: 16px;">→</div>
            <div style="background: rgba(245, 158, 11, 0.15); border: 2px solid #f59e0b; border-radius: 8px; padding: 10px; text-align: center;">
              <div style="font-size: 13px; font-weight: 800; color: #fbbf24;">⚡ CDC PIPELINE</div>
              <div style="font-size: 11px; color: #cbd5e1;">Kafka / Debezium Stream</div>
            </div>
            <div style="text-align: center; color: #22d3ee; font-weight: 900; font-size: 16px;">→</div>
            <div style="background: rgba(6, 182, 212, 0.15); border: 2px solid #06b6d4; border-radius: 8px; padding: 10px; text-align: center;">
              <div style="font-size: 13px; font-weight: 800; color: #22d3ee;">🪟 STOREFRONT</div>
              <div style="font-size: 11px; color: #cbd5e1;">Elasticsearch Search View</div>
            </div>
          </div>
          <!-- 3 Golden Rules -->
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px; font-size: 11px;">
            <div style="background: #0f172a; padding: 8px; border-radius: 6px; border-left: 3px solid #3b82f6;">
              <strong style="color: #60a5fa;">1. Respect RUM Trilemma:</strong> No engine can do both; choose storage engine by access pattern.
            </div>
            <div style="background: #0f172a; padding: 8px; border-radius: 6px; border-left: 3px solid #10b981;">
              <strong style="color: #34d399;">2. Never Dual-Write:</strong> App-level dual writes risk split-brain. Replicate via asynchronous CDC.
            </div>
            <div style="background: #0f172a; padding: 8px; border-radius: 6px; border-left: 3px solid #06b6d4;">
              <strong style="color: #22d3ee;">3. Converged Segments:</strong> Both engines share an LSM segment lifecycle under the hood.
            </div>
          </div>
          <div style="text-align: center; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 6px; padding: 8px; font-size: 13px; font-weight: 700; color: #93c5fd;">
            🎓 Master's Defense Verdict: Synthesis beats Compromise. We welcome the Committee's Questions!
          </div>
        </div>
        """,
        "key_points": [
            "Anti-Pattern Warning: Never use application-level dual writes; network failures cause permanent split-brain data divergence.",
            "Production CQRS Synthesis: Cassandra acts as the immutable System of Record; Kafka CDC asynchronously updates Elasticsearch.",
            "Storage Convergence: Both engines utilize an LSM segment lifecycle, complementing each other under CQRS separation.",
            "Final Verdict: Neither engine can subsume the other; architectural excellence lies in combining their specialized physical layouts."
        ],
        "script_en": "In production, never perform dual-writes from application code. Treat Cassandra as the Bank Vault—the durable System of Record accepting high-velocity writes. Treat Elasticsearch as the Storefront Display Window—a disposable, highly indexed search view. Use Change Data Capture via Kafka to asynchronously replicate log commits into search segments. In summary: no single database rules all workloads, but by combining LSM-Tree ingestion with Inverted Index retrieval under CQRS, modern data architectures achieve both maximum write throughput and microsecond search. Thank you, and we welcome your questions.",
        "script_vi": "Trong thực tế, tuyệt đối không ghi đồng thời hai bên từ mã nguồn ứng dụng. Hãy coi Cassandra là Két Sắt Ngân Hàng — nguồn chân lý tin cậy đón nhận luồng ghi tải cao. Hãy coi Elasticsearch là Cửa Sổ Trưng Bày — khung nhìn tìm kiếm đa năng có thể tái tạo bất kỳ lúc nào. Sử dụng Change Data Capture qua Kafka để đồng bộ bất đồng bộ các commit log sang chỉ mục tìm kiếm. Tóm lại: không cơ sở dữ liệu nào giải quyết được mọi bài toán, nhưng bằng cách phối hợp khả năng ghi của LSM với khả năng tìm kiếm của Chỉ mục đảo qua mô hình CQRS, hệ thống sẽ đạt được cả thông lượng ghi tối đa lẫn tốc độ tìm kiếm micro-giây. Xin chân thành cảm ơn Thầy Cô và nhóm sẵn sàng lắng nghe câu hỏi."
    }
]

print(f"Total visual slides loaded: {len(ALL_SLIDES)}")
