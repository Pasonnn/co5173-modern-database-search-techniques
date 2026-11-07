"""Generates publication-quality vector SVG diagrams for Apache Cassandra & Elasticsearch."""
from __future__ import annotations
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent.parent / "report" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def generate_rum_conjecture_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 650" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <linearGradient id="triGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.1" />
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="800" height="650" fill="url(#bgGrad)" rx="16" />

  <!-- Title Header -->
  <text x="400" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="22" font-weight="700" fill="#f8fafc" text-anchor="middle">The RUM Conjecture Trade-Off Space</text>
  <text x="400" y="72" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" fill="#94a3b8" text-anchor="middle">Optimizing any two overheads inevitably compromises the third (Athanassoulis et al., EDBT 2016)</text>

  <!-- Main RUM Triangle -->
  <polygon points="400,140 130,520 670,520" fill="url(#triGrad)" stroke="#38bdf8" stroke-width="3" stroke-linejoin="round" />

  <!-- Dotted trade-off lines -->
  <line x1="400" y1="140" x2="400" y2="520" stroke="#64748b" stroke-dasharray="4,4" stroke-width="1.5" />
  <line x1="130" y1="520" x2="535" y2="330" stroke="#64748b" stroke-dasharray="4,4" stroke-width="1.5" />
  <line x1="670" y1="520" x2="265" y2="330" stroke="#64748b" stroke-dasharray="4,4" stroke-width="1.5" />

  <!-- Vertex R: Read Overhead -->
  <circle cx="400" cy="140" r="32" fill="#0284c7" stroke="#38bdf8" stroke-width="3" filter="url(#shadow)" />
  <text x="400" y="146" font-family="sans-serif" font-size="20" font-weight="800" fill="#ffffff" text-anchor="middle">R</text>
  <text x="400" y="96" font-family="sans-serif" font-size="15" font-weight="700" fill="#38bdf8" text-anchor="middle">READ OVERHEAD</text>
  <text x="400" y="112" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Point lookups, range scans, search latency</text>

  <!-- Vertex U: Update Overhead -->
  <circle cx="130" cy="520" r="32" fill="#d97706" stroke="#fbbf24" stroke-width="3" filter="url(#shadow)" />
  <text x="130" y="526" font-family="sans-serif" font-size="20" font-weight="800" fill="#ffffff" text-anchor="middle">U</text>
  <text x="130" y="572" font-family="sans-serif" font-size="15" font-weight="700" fill="#fbbf24" text-anchor="middle">UPDATE OVERHEAD</text>
  <text x="130" y="590" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Write amplification, random I/O writes</text>

  <!-- Vertex M: Memory / Storage Overhead -->
  <circle cx="670" cy="520" r="32" fill="#7c3aed" stroke="#a78bfa" stroke-width="3" filter="url(#shadow)" />
  <text x="670" y="526" font-family="sans-serif" font-size="20" font-weight="800" fill="#ffffff" text-anchor="middle">M</text>
  <text x="670" y="572" font-family="sans-serif" font-size="15" font-weight="700" fill="#a78bfa" text-anchor="middle">MEMORY OVERHEAD</text>
  <text x="670" y="590" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Index space, Bloom filters, RAM cache</text>

  <!-- Cassandra Box near Vertex U -->
  <g transform="translate(50, 270)" filter="url(#shadow)">
    <rect width="240" height="110" rx="10" fill="#1e293b" stroke="#fbbf24" stroke-width="2" />
    <text x="120" y="26" font-family="sans-serif" font-size="13" font-weight="700" fill="#fbbf24" text-anchor="middle">APACHE CASSANDRA (LSM)</text>
    <text x="120" y="46" font-family="sans-serif" font-size="11" fill="#e2e8f0" text-anchor="middle">Prioritizes Update Ingestion (Low U)</text>
    <text x="120" y="64" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">• Append-only MemTable & CommitLog</text>
    <text x="120" y="80" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">• Trade-off: Read Amplification (R)</text>
    <text x="120" y="96" font-family="sans-serif" font-size="10" fill="#38bdf8" text-anchor="middle">Mitigated via Bloom Filters & Compaction</text>
  </g>

  <!-- Elasticsearch Box near Vertex R & M -->
  <g transform="translate(510, 270)" filter="url(#shadow)">
    <rect width="240" height="110" rx="10" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
    <text x="120" y="26" font-family="sans-serif" font-size="13" font-weight="700" fill="#38bdf8" text-anchor="middle">ELASTICSEARCH (INVERTED)</text>
    <text x="120" y="46" font-family="sans-serif" font-size="11" fill="#e2e8f0" text-anchor="middle">Prioritizes Complex Search (Low R)</text>
    <text x="120" y="64" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">• Instant posting list intersection & BM25</text>
    <text x="120" y="80" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">• Trade-off: Higher Memory (M) & Update (U)</text>
    <text x="120" y="96" font-family="sans-serif" font-size="10" fill="#a78bfa" text-anchor="middle">FST Term Dict + Segment Merge Overhead</text>
  </g>

  <!-- Center Convergence Point -->
  <circle cx="400" cy="385" r="8" fill="#f43f5e" />
  <text x="400" y="415" font-family="sans-serif" font-size="12" font-weight="700" fill="#f43f5e" text-anchor="middle">No Universal Engine</text>
  <text x="400" y="432" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Architectural specialization dictates performance bounds</text>
</svg>
"""
    with open(FIGURES_DIR / "rum_conjecture.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/rum_conjecture.svg")


def generate_lsm_tree_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 680" width="100%" height="100%">
  <defs>
    <linearGradient id="bgLsm" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <filter id="shadowLsm">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <rect width="900" height="680" fill="url(#bgLsm)" rx="16" />

  <text x="450" y="40" font-family="sans-serif" font-size="22" font-weight="700" fill="#f8fafc" text-anchor="middle">Apache Cassandra LSM-Tree Engine Architecture</text>
  <text x="450" y="65" font-family="sans-serif" font-size="13" fill="#94a3b8" text-anchor="middle">High-Throughput Append Path, Read Pruning via Bloom Filters, and Asynchronous Compaction</text>

  <!-- WRITE INGESTION PATH -->
  <g transform="translate(60, 95)" filter="url(#shadowLsm)">
    <rect width="780" height="150" rx="10" fill="#111827" stroke="#3b82f6" stroke-width="2" />
    <text x="25" y="30" font-family="sans-serif" font-size="14" font-weight="700" fill="#60a5fa">IN-MEMORY LEVEL (RAM): MemTable &amp; Sequential Write Log</text>

    <!-- Client Write Request -->
    <rect x="25" y="55" width="160" height="70" rx="6" fill="#1e3a8a" stroke="#60a5fa" />
    <text x="105" y="85" font-family="sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">Client Mutation</text>
    <text x="105" y="105" font-family="sans-serif" font-size="11" fill="#93c5fd" text-anchor="middle">put(k, v) / delete(k)</text>

    <!-- Arrow to WAL -->
    <path d="M 185 90 L 225 70" stroke="#60a5fa" stroke-width="2" fill="none" marker-end="url(#arrow)" />
    <!-- Arrow to MemTable -->
    <path d="M 185 90 L 445 90" stroke="#34d399" stroke-width="2" fill="none" />

    <!-- CommitLog / WAL -->
    <rect x="225" y="50" width="190" height="80" rx="6" fill="#1f2937" stroke="#9ca3af" stroke-width="1.5" />
    <text x="320" y="75" font-family="sans-serif" font-size="12" font-weight="700" fill="#f3f4f6" text-anchor="middle">CommitLog (Disk WAL)</text>
    <text x="320" y="95" font-family="sans-serif" font-size="10" fill="#9ca3af" text-anchor="middle">Sequential disk append only</text>
    <text x="320" y="112" font-family="sans-serif" font-size="10" fill="#ef4444" text-anchor="middle">Guarantees Crash Durability</text>

    <!-- MemTable -->
    <rect x="445" y="50" width="310" height="80" rx="6" fill="#064e3b" stroke="#34d399" stroke-width="2" />
    <text x="600" y="75" font-family="sans-serif" font-size="13" font-weight="700" fill="#a7f3d0" text-anchor="middle">MemTable (Concurrent SkipList)</text>
    <text x="600" y="95" font-family="sans-serif" font-size="11" fill="#ecfdf5" text-anchor="middle">Sorted keys in RAM • O(log N) zero-disk latency</text>
    <text x="600" y="115" font-family="sans-serif" font-size="10" fill="#6ee7b7" text-anchor="middle">Flushes to SSTable upon reaching threshold</text>
  </g>

  <!-- FLUSH TRANSITION -->
  <line x1="600" y1="245" x2="600" y2="290" stroke="#34d399" stroke-width="3" stroke-dasharray="6,4" />
  <text x="640" y="272" font-family="sans-serif" font-size="11" font-weight="700" fill="#34d399">Flush as Immutable SSTable</text>

  <!-- ON-DISK SSTABLES LEVEL -->
  <g transform="translate(60, 290)" filter="url(#shadowLsm)">
    <rect width="780" height="345" rx="10" fill="#111827" stroke="#64748b" stroke-width="2" />
    <text x="25" y="30" font-family="sans-serif" font-size="14" font-weight="700" fill="#94a3b8">ON-DISK LEVEL (STORAGE): Immutable SSTables &amp; Read Path Pruning</text>

    <!-- SSTable Anatomy Box -->
    <g transform="translate(25, 50)">
      <rect width="470" height="270" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
      <text x="235" y="25" font-family="sans-serif" font-size="13" font-weight="700" fill="#38bdf8" text-anchor="middle">Anatomy of an SSTable (Sorted String Table)</text>

      <!-- 1. Bloom Filter -->
      <rect x="20" y="45" width="430" height="55" rx="5" fill="#312e81" stroke="#818cf8" />
      <text x="35" y="68" font-family="sans-serif" font-size="12" font-weight="700" fill="#c7d2fe">1. In-Memory Bloom Filter (~10 bits/key)</text>
      <text x="35" y="88" font-family="sans-serif" font-size="11" fill="#e0e7ff">Kirsch-Mitzenmacher hashing. Fast-fails 99% of absent key queries!</text>

      <!-- 2. Fence Pointers / Sparse Index -->
      <rect x="20" y="115" width="430" height="55" rx="5" fill="#0f172a" stroke="#94a3b8" />
      <text x="35" y="138" font-family="sans-serif" font-size="12" font-weight="700" fill="#e2e8f0">2. Sparse Primary Key Index (Fence Pointers)</text>
      <text x="35" y="158" font-family="sans-serif" font-size="11" fill="#94a3b8">Keys sampled every 128 elements. Binary search narrows disk offset.</text>

      <!-- 3. Sorted Data Blocks -->
      <rect x="20" y="185" width="430" height="70" rx="5" fill="#022c22" stroke="#10b981" />
      <text x="35" y="208" font-family="sans-serif" font-size="12" font-weight="700" fill="#6ee7b7">3. Immutable Sorted Data File &amp; Tombstones</text>
      <text x="35" y="228" font-family="sans-serif" font-size="11" fill="#d1fae5">Sequential sorted records [k_0, k_1, ... k_N]. Deletes written as Tombstones.</text>
      <text x="35" y="244" font-family="sans-serif" font-size="10" fill="#a7f3d0">Appended sequentially with zero random write disk heads movement.</text>
    </g>

    <!-- COMPACTION ENGINE BOX -->
    <g transform="translate(515, 50)">
      <rect width="240" height="270" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5" />
      <text x="120" y="25" font-family="sans-serif" font-size="13" font-weight="700" fill="#f59e0b" text-anchor="middle">Compaction Engine</text>
      <text x="120" y="45" font-family="sans-serif" font-size="11" fill="#fde68a" text-anchor="middle">(Size-Tiered / Leveled)</text>

      <line x1="20" y1="60" x2="220" y2="60" stroke="#334155" />
      <text x="30" y="85" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Merges overlapping SSTables</text>
      <text x="30" y="110" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Multi-way merge sort in O(N)</text>
      <text x="30" y="135" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Discards shadowed versions</text>
      <text x="30" y="160" font-family="sans-serif" font-size="11" fill="#ef4444">• Purges dead Tombstones</text>
      <text x="30" y="185" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Recovers wasted disk space</text>
      <text x="30" y="210" font-family="sans-serif" font-size="11" fill="#38bdf8">• Bounds Read Amplification</text>

      <rect x="25" y="228" width="190" height="30" rx="4" fill="#78350f" stroke="#f59e0b" />
      <text x="120" y="248" font-family="sans-serif" font-size="10" font-weight="700" fill="#fef3c7" text-anchor="middle">Major / Minor Compactions</text>
    </g>
  </g>
</svg>
"""
    with open(FIGURES_DIR / "lsm_tree_architecture.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/lsm_tree_architecture.svg")


def generate_inverted_index_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 680" width="100%" height="100%">
  <defs>
    <linearGradient id="bgInv" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b1120" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <filter id="fShadow">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <rect width="900" height="680" fill="url(#bgInv)" rx="16" />

  <text x="450" y="40" font-family="sans-serif" font-size="22" font-weight="700" fill="#f8fafc" text-anchor="middle">Elasticsearch / Lucene Inverted Index Architecture</text>
  <text x="450" y="65" font-family="sans-serif" font-size="13" fill="#94a3b8" text-anchor="middle">Text Analysis, FST Term Dictionary, Skip-List Postings, and BM25 Relevance Scoring</text>

  <!-- 1. TEXT ANALYSIS PIPELINE -->
  <g transform="translate(60, 95)" filter="url(#fShadow)">
    <rect width="780" height="110" rx="10" fill="#111827" stroke="#38bdf8" stroke-width="1.5" />
    <text x="25" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#38bdf8">1. INGESTION &amp; TEXT ANALYSIS PIPELINE (ANALYZER)</text>

    <!-- Raw Doc -->
    <rect x="25" y="45" width="170" height="50" rx="6" fill="#1e293b" stroke="#64748b" />
    <text x="110" y="66" font-family="sans-serif" font-size="11" font-weight="700" fill="#f1f5f9" text-anchor="middle">Raw Document</text>
    <text x="110" y="82" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">"Cassandra LSM Trees!"</text>

    <!-- Arrow -->
    <path d="M 195 70 L 230 70" stroke="#38bdf8" stroke-width="2" />

    <!-- Character & Tokenizer -->
    <rect x="230" y="45" width="180" height="50" rx="6" fill="#1e3a8a" stroke="#60a5fa" />
    <text x="320" y="66" font-family="sans-serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Tokenizer</text>
    <text x="320" y="82" font-family="sans-serif" font-size="10" fill="#93c5fd" text-anchor="middle">["Cassandra", "LSM", "Trees"]</text>

    <!-- Arrow -->
    <path d="M 410 70 L 445 70" stroke="#38bdf8" stroke-width="2" />

    <!-- Token Filters -->
    <rect x="445" y="45" width="310" height="50" rx="6" fill="#064e3b" stroke="#34d399" />
    <text x="600" y="66" font-family="sans-serif" font-size="11" font-weight="700" fill="#a7f3d0" text-anchor="middle">Token Filters (Lowercase, Porter Stemmer)</text>
    <text x="600" y="82" font-family="sans-serif" font-size="10" fill="#6ee7b7" text-anchor="middle">Tokens: ["cassandra", "lsm", "tree"]</text>
  </g>

  <!-- 2. INVERTED INDEX DATA STRUCTURES -->
  <g transform="translate(60, 225)" filter="url(#fShadow)">
    <rect width="780" height="270" rx="10" fill="#111827" stroke="#818cf8" stroke-width="1.5" />
    <text x="25" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#c7d2fe">2. CORE INVERTED INDEX DATA STRUCTURES</text>

    <!-- Term Dictionary (FST) -->
    <g transform="translate(25, 45)">
      <rect width="250" height="205" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5" />
      <text x="125" y="25" font-family="sans-serif" font-size="12" font-weight="700" fill="#c7d2fe" text-anchor="middle">Term Dictionary (FST)</text>
      <text x="125" y="42" font-family="sans-serif" font-size="10" fill="#a5b4fc" text-anchor="middle">Memory-resident Prefix Automaton</text>

      <rect x="15" y="55" width="220" height="30" rx="4" fill="#312e81" />
      <text x="25" y="75" font-family="sans-serif" font-size="11" font-weight="700" fill="#ffffff">"cassandra"</text>
      <text x="200" y="75" font-family="sans-serif" font-size="11" fill="#38bdf8" text-anchor="end">IDF: 2.1 →</text>

      <rect x="15" y="92" width="220" height="30" rx="4" fill="#312e81" />
      <text x="25" y="112" font-family="sans-serif" font-size="11" font-weight="700" fill="#ffffff">"elastic"</text>
      <text x="200" y="112" font-family="sans-serif" font-size="11" fill="#38bdf8" text-anchor="end">IDF: 1.8 →</text>

      <rect x="15" y="129" width="220" height="30" rx="4" fill="#312e81" />
      <text x="25" y="149" font-family="sans-serif" font-size="11" font-weight="700" fill="#ffffff">"lsm"</text>
      <text x="200" y="149" font-family="sans-serif" font-size="11" fill="#38bdf8" text-anchor="end">IDF: 2.4 →</text>

      <rect x="15" y="166" width="220" height="30" rx="4" fill="#312e81" />
      <text x="25" y="186" font-family="sans-serif" font-size="11" font-weight="700" fill="#ffffff">"tree"</text>
      <text x="200" y="186" font-family="sans-serif" font-size="11" fill="#38bdf8" text-anchor="end">IDF: 1.2 →</text>
    </g>

    <!-- Posting Lists (with skip pointers) -->
    <g transform="translate(300, 45)">
      <rect width="455" height="205" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" />
      <text x="227" y="25" font-family="sans-serif" font-size="12" font-weight="700" fill="#38bdf8" text-anchor="middle">Posting Lists with Skip Pointers &amp; Term Frequencies</text>

      <!-- Row 1: cassandra -->
      <g transform="translate(15, 45)">
        <rect x="0" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#38bdf8" />
        <text x="37" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 1</text>
        <text x="37" y="28" font-family="sans-serif" font-size="9" fill="#93c5fd" text-anchor="middle">tf: 2, pos:[0,4]</text>

        <line x1="75" y1="17" x2="110" y2="17" stroke="#38bdf8" stroke-width="2" />

        <rect x="110" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#38bdf8" />
        <text x="147" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 12</text>
        <text x="147" y="28" font-family="sans-serif" font-size="9" fill="#93c5fd" text-anchor="middle">tf: 1, pos:[2]</text>

        <!-- Skip Pointer -->
        <path d="M 37 0 Q 147 -20 257 0" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,3" fill="none" />
        <text x="147" y="-12" font-family="sans-serif" font-size="8" fill="#fbbf24" text-anchor="middle">Skip Pointer (d=12)</text>

        <line x1="185" y1="17" x2="220" y2="17" stroke="#38bdf8" stroke-width="2" />

        <rect x="220" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#38bdf8" />
        <text x="257" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 45</text>
        <text x="257" y="28" font-family="sans-serif" font-size="9" fill="#93c5fd" text-anchor="middle">tf: 3, pos:[1,5,8]</text>

        <line x1="295" y1="17" x2="330" y2="17" stroke="#38bdf8" stroke-width="2" />

        <rect x="330" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#38bdf8" />
        <text x="367" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 99</text>
        <text x="367" y="28" font-family="sans-serif" font-size="9" fill="#93c5fd" text-anchor="middle">tf: 1, pos:[7]</text>
      </g>

      <!-- Row 2: lsm -->
      <g transform="translate(15, 125)">
        <rect x="0" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#10b981" />
        <text x="37" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 1</text>
        <text x="37" y="28" font-family="sans-serif" font-size="9" fill="#6ee7b7" text-anchor="middle">tf: 1, pos:[1]</text>

        <line x1="75" y1="17" x2="110" y2="17" stroke="#10b981" stroke-width="2" />

        <rect x="110" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#10b981" />
        <text x="147" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 45</text>
        <text x="147" y="28" font-family="sans-serif" font-size="9" fill="#6ee7b7" text-anchor="middle">tf: 2, pos:[3,6]</text>

        <line x1="185" y1="17" x2="220" y2="17" stroke="#10b981" stroke-width="2" />

        <rect x="220" y="0" width="75" height="35" rx="4" fill="#1e293b" stroke="#10b981" />
        <text x="257" y="16" font-family="sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Doc 80</text>
        <text x="257" y="28" font-family="sans-serif" font-size="9" fill="#6ee7b7" text-anchor="middle">tf: 1, pos:[0]</text>

        <text x="330" y="22" font-family="sans-serif" font-size="10" font-weight="700" fill="#34d399">Intersection (AND):</text>
        <text x="330" y="38" font-family="sans-serif" font-size="10" fill="#a7f3d0">Docs [1, 45] in O(min(|P1|, |P2|))</text>
      </g>
    </g>
  </g>

  <!-- 3. BM25 RELEVANCE SCORING -->
  <g transform="translate(60, 510)" filter="url(#fShadow)">
    <rect width="780" height="135" rx="10" fill="#111827" stroke="#f59e0b" stroke-width="1.5" />
    <text x="25" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#fbbf24">3. OKAPI BM25 RELEVANCE RANKING MODEL</text>

    <text x="390" y="60" font-family="Courier, monospace" font-size="13" font-weight="700" fill="#fef08a" text-anchor="middle">
      Score(D, Q) = ∑ [ IDF(q) · ( tf(q, D) · (k₁ + 1) ) / ( tf(q, D) + k₁ · (1 - b + b · |D| / avgdl) ) ]
    </text>

    <text x="45" y="95" font-family="sans-serif" font-size="11" fill="#cbd5e1">• <tspan font-weight="700" fill="#38bdf8">k₁ = 1.2</tspan>: Calibrates Term Frequency saturation curve (prevents spamming from dominating score)</text>
    <text x="45" y="115" font-family="sans-serif" font-size="11" fill="#cbd5e1">• <tspan font-weight="700" fill="#34d399">b = 0.75</tspan>: Document length normalization factor (penalizes abnormally verbose documents)</text>
  </g>
</svg>
"""
    with open(FIGURES_DIR / "inverted_index_architecture.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/inverted_index_architecture.svg")


def generate_benchmark_comparison_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 560" width="100%" height="100%">
  <defs>
    <linearGradient id="bgChart" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
  </defs>

  <rect width="850" height="560" fill="url(#bgChart)" rx="14" />
  <text x="425" y="38" font-family="sans-serif" font-size="20" font-weight="700" fill="#f8fafc" text-anchor="middle">Empirical Benchmark Head-to-Head: Cassandra vs. Elasticsearch</text>
  <text x="425" y="60" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">Evaluated over Real Datasets (N=10,000 World Cities Keys &amp; 1,655 Quotes Corpus)</text>

  <!-- Left Chart: Ingestion Throughput (ops/sec) -->
  <g transform="translate(60, 95)">
    <rect width="330" height="200" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5" />
    <text x="165" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#38bdf8" text-anchor="middle">INGESTION THROUGHPUT (ops/s)</text>
    <text x="165" y="45" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">(Higher is Better)</text>

    <!-- Cassandra LSM -->
    <text x="25" y="90" font-family="sans-serif" font-size="11" font-weight="700" fill="#cbd5e1">Cassandra (LSM)</text>
    <rect x="150" y="75" width="120" height="22" rx="4" fill="#fbbf24" />
    <text x="280" y="91" font-family="sans-serif" font-size="11" font-weight="700" fill="#fbbf24">85,624</text>

    <!-- Elasticsearch Index -->
    <text x="25" y="145" font-family="sans-serif" font-size="11" font-weight="700" fill="#cbd5e1">Elasticsearch</text>
    <rect x="150" y="130" width="132" height="22" rx="4" fill="#38bdf8" />
    <text x="288" y="146" font-family="sans-serif" font-size="11" font-weight="700" fill="#38bdf8">93,935</text>

    <text x="165" y="185" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Both systems achieve high throughput via append buffers</text>
  </g>

  <!-- Right Chart: Query Latency (µs) -->
  <g transform="translate(460, 95)">
    <rect width="330" height="200" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5" />
    <text x="165" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#34d399" text-anchor="middle">QUERY LATENCY (µs)</text>
    <text x="165" y="45" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">(Lower is Better)</text>

    <!-- Cassandra Point Hit -->
    <text x="25" y="80" font-family="sans-serif" font-size="10" font-weight="700" fill="#cbd5e1">Cassandra Hit</text>
    <rect x="140" y="68" width="20" height="18" rx="3" fill="#fbbf24" />
    <text x="170" y="82" font-family="sans-serif" font-size="10" font-weight="700" fill="#fbbf24">5.42 µs</text>

    <!-- Cassandra Miss (Bloom Fast-fail) -->
    <text x="25" y="115" font-family="sans-serif" font-size="10" font-weight="700" fill="#cbd5e1">Cassandra Miss (Bloom)</text>
    <rect x="140" y="103" width="14" height="18" rx="3" fill="#a78bfa" />
    <text x="164" y="117" font-family="sans-serif" font-size="10" font-weight="700" fill="#a78bfa">3.42 µs</text>

    <!-- ES Boolean AND -->
    <text x="25" y="150" font-family="sans-serif" font-size="10" font-weight="700" fill="#cbd5e1">ES Boolean AND</text>
    <rect x="140" y="138" width="55" height="18" rx="3" fill="#38bdf8" />
    <text x="205" y="152" font-family="sans-serif" font-size="10" font-weight="700" fill="#38bdf8">20.36 µs</text>

    <!-- ES BM25 Ranked -->
    <text x="25" y="185" font-family="sans-serif" font-size="10" font-weight="700" fill="#cbd5e1">ES BM25 Ranked</text>
    <rect x="140" y="173" width="145" height="18" rx="3" fill="#f43f5e" />
    <text x="295" y="187" font-family="sans-serif" font-size="10" font-weight="700" fill="#f43f5e">118.4 µs</text>
  </g>

  <!-- Bottom Box: Stress-Test Key Highlights -->
  <g transform="translate(60, 315)">
    <rect width="730" height="215" rx="8" fill="#111827" stroke="#475569" stroke-width="1.5" />
    <text x="365" y="28" font-family="sans-serif" font-size="14" font-weight="700" fill="#f8fafc" text-anchor="middle">Key Stress-Test Findings &amp; RUM Insights</text>

    <!-- Metric 1: Inverted Index Speedup -->
    <rect x="25" y="45" width="330" height="70" rx="6" fill="#1e293b" stroke="#38bdf8" />
    <text x="40" y="68" font-family="sans-serif" font-size="12" font-weight="700" fill="#38bdf8">71.5x Speedup in Lexical Search</text>
    <text x="40" y="88" font-family="sans-serif" font-size="10" fill="#cbd5e1">Inverted Index Posting Intersection (35 µs)</text>
    <text x="40" y="103" font-family="sans-serif" font-size="10" fill="#94a3b8">vs. Brute-force Linear Text Scan (2,515 µs)</text>

    <!-- Metric 2: Cassandra Bloom Filter Pruning -->
    <rect x="375" y="45" width="330" height="70" rx="6" fill="#1e293b" stroke="#a78bfa" />
    <text x="390" y="68" font-family="sans-serif" font-size="12" font-weight="700" fill="#a78bfa">100% Negative SSTable Pruning</text>
    <text x="390" y="88" font-family="sans-serif" font-size="10" fill="#cbd5e1">In-Memory Bloom Filter eliminates all disk seeks</text>
    <text x="390" y="103" font-family="sans-serif" font-size="10" fill="#94a3b8">for absent keys, bounding Read Amplification (R)</text>

    <!-- Memory Footprint Row -->
    <rect x="25" y="130" width="680" height="65" rx="6" fill="#1e293b" stroke="#34d399" />
    <text x="40" y="152" font-family="sans-serif" font-size="12" font-weight="700" fill="#34d399">Index Footprint Trade-off (Memory Amplification M):</text>
    <text x="40" y="172" font-family="sans-serif" font-size="11" fill="#e2e8f0">• Cassandra: ~154 Bytes/key (MemTable + compact Bloom Filter of ~10 bits/key + fence pointers)</text>
    <text x="40" y="187" font-family="sans-serif" font-size="11" fill="#e2e8f0">• Elasticsearch: ~2,293 Bytes/doc (Rich Term Dictionary FST + Posting lists + term frequencies)</text>
  </g>
</svg>
"""
    with open(FIGURES_DIR / "benchmark_comparison.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/benchmark_comparison.svg")


def main():
    generate_rum_conjecture_svg()
    generate_lsm_tree_svg()
    generate_inverted_index_svg()
    generate_benchmark_comparison_svg()


if __name__ == "__main__":
    main()
