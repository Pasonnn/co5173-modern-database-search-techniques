"""Generates publication-quality vector SVG diagrams and downloads reference architecture figures."""
from __future__ import annotations
import urllib.request
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent.parent / "report" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def download_reference_figures():
    """Downloads authoritative reference diagrams with graceful offline fallback."""
    refs = [
        (
            "bplus_tree_reference.png",
            "https://upload.wikimedia.org/wikipedia/commons/3/37/Bplustree.png"
        ),
    ]
    for filename, url in refs:
        target = FIGURES_DIR / filename
        if not target.exists():
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "CO5173-Research/1.0 (academic; student)"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    with open(target, "wb") as f:
                        f.write(resp.read())
                print(f"Downloaded reference: {filename}")
            except Exception as e:
                print(f"Notice: Reference download for {filename} deferred ({e}).")


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

  <!-- Vertices -->
  <!-- Vertex R: Read Amplification -->
  <circle cx="400" cy="140" r="14" fill="#38bdf8" filter="url(#shadow)" />
  <circle cx="400" cy="140" r="7" fill="#0f172a" />
  <rect x="250" y="85" width="300" height="42" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow)" />
  <text x="400" y="104" font-family="sans-serif" font-size="14" font-weight="700" fill="#38bdf8" text-anchor="middle">READ AMPLIFICATION (R)</text>
  <text x="400" y="120" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Bytes Read from Storage / Payload Bytes</text>

  <!-- Vertex U: Update Amplification -->
  <circle cx="130" cy="520" r="14" fill="#f43f5e" filter="url(#shadow)" />
  <circle cx="130" cy="520" r="7" fill="#0f172a" />
  <rect x="20" y="545" width="230" height="42" rx="8" fill="#1e293b" stroke="#f43f5e" stroke-width="1.5" filter="url(#shadow)" />
  <text x="135" y="564" font-family="sans-serif" font-size="13" font-weight="700" fill="#f43f5e" text-anchor="middle">UPDATE AMPLIFICATION (U)</text>
  <text x="135" y="580" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Bytes Written / Updated Payload</text>

  <!-- Vertex M: Memory Amplification -->
  <circle cx="670" cy="520" r="14" fill="#10b981" filter="url(#shadow)" />
  <circle cx="670" cy="520" r="7" fill="#0f172a" />
  <rect x="550" y="545" width="230" height="42" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)" />
  <text x="665" y="564" font-family="sans-serif" font-size="13" font-weight="700" fill="#10b981" text-anchor="middle">MEMORY AMPLIFICATION (M)</text>
  <text x="665" y="580" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Index DRAM Overhead / Raw Data</text>

  <!-- Architecture Badges Mapped on RUM Axes -->
  <!-- 1. B+ Tree -->
  <g transform="translate(240, 260)" filter="url(#shadow)">
    <rect width="130" height="52" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="65" y="22" font-family="sans-serif" font-size="13" font-weight="700" fill="#38bdf8" text-anchor="middle">B+ TREE</text>
    <text x="65" y="40" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Low R, Mod. M, High U</text>
  </g>

  <!-- 2. Static RMI -->
  <g transform="translate(435, 260)" filter="url(#shadow)">
    <rect width="135" height="52" rx="6" fill="#0f172a" stroke="#a855f7" stroke-width="2" />
    <text x="67" y="22" font-family="sans-serif" font-size="13" font-weight="700" fill="#c084fc" text-anchor="middle">STATIC RMI</text>
    <text x="67" y="40" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Ultra-Low M (1.4 B/k), Low R</text>
  </g>

  <!-- 3. LSM-Tree -->
  <g transform="translate(180, 440)" filter="url(#shadow)">
    <rect width="135" height="52" rx="6" fill="#0f172a" stroke="#f43f5e" stroke-width="2" />
    <text x="67" y="22" font-family="sans-serif" font-size="13" font-weight="700" fill="#f43f5e" text-anchor="middle">LSM-TREE</text>
    <text x="67" y="40" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Ultra-Low U, Higher R</text>
  </g>

  <!-- 4. Dynamic ALEX -->
  <g transform="translate(480, 440)" filter="url(#shadow)">
    <rect width="135" height="52" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2" />
    <text x="67" y="22" font-family="sans-serif" font-size="13" font-weight="700" fill="#34d399" text-anchor="middle">DYNAMIC ALEX</text>
    <text x="67" y="40" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Low R, Mod. U (Gaps)</text>
  </g>

  <!-- Inverted Index Indicator -->
  <g transform="translate(290, 365)" filter="url(#shadow)">
    <rect width="220" height="34" rx="6" fill="#1e1e38" stroke="#fbbf24" stroke-width="1.5" />
    <text x="110" y="21" font-family="sans-serif" font-size="11" font-weight="600" fill="#fbbf24" text-anchor="middle">INVERTED INDEX: Lexical / High M</text>
  </g>
</svg>
"""
    with open(FIGURES_DIR / "rum_conjecture.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/rum_conjecture.svg")


def generate_lsm_tree_svg():
    svg = r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 560" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <filter id="sh" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <rect width="850" height="560" fill="url(#bg)" rx="14" />
  <text x="425" y="38" font-family="sans-serif" font-size="20" font-weight="700" fill="#f9fafb" text-anchor="middle">Log-Structured Merge-Tree (LSM) Architecture</text>
  <text x="425" y="60" font-family="sans-serif" font-size="12" fill="#9ca3af" text-anchor="middle">Sequential Append Ingestion, In-Memory MemTable, and Multi-Level Merging (RocksDB / Cassandra)</text>

  <!-- Client Mutation -->
  <rect x="40" y="100" width="140" height="50" rx="8" fill="#1f2937" stroke="#3b82f6" stroke-width="2" filter="url(#sh)"/>
  <text x="110" y="125" font-family="sans-serif" font-size="13" font-weight="700" fill="#60a5fa" text-anchor="middle">Client Writes</text>
  <text x="110" y="140" font-family="sans-serif" font-size="10" fill="#9ca3af" text-anchor="middle">PUT(key, val) / DEL</text>

  <!-- Write Split Arrows -->
  <path d="M 180 120 L 250 120 L 250 100 L 290 100" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" />
  <path d="M 180 130 L 250 130 L 250 160 L 290 160" fill="none" stroke="#f43f5e" stroke-width="2" />

  <!-- WAL Log -->
  <rect x="290" y="75" width="220" height="44" rx="6" fill="#1e293b" stroke="#f43f5e" stroke-width="1.5" filter="url(#sh)"/>
  <text x="400" y="97" font-family="sans-serif" font-size="12" font-weight="700" fill="#f43f5e" text-anchor="middle">WAL (CommitLog on Disk)</text>
  <text x="400" y="112" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Sequential Append-Only Durability</text>

  <!-- MemTable (RAM) -->
  <rect x="290" y="140" width="220" height="65" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2" filter="url(#sh)"/>
  <text x="400" y="165" font-family="sans-serif" font-size="13" font-weight="700" fill="#38bdf8" text-anchor="middle">MemTable (RAM SkipList)</text>
  <text x="400" y="182" font-family="sans-serif" font-size="10" fill="#cbd5e1" text-anchor="middle">Absorbs Concurrent Mutations ($O(\log M)$)</text>
  <text x="400" y="196" font-family="sans-serif" font-size="9" fill="#10b981" text-anchor="middle">Zero Random Disk Head Seeks</text>

  <!-- Flush Arrow -->
  <path d="M 400 205 L 400 250" fill="none" stroke="#10b981" stroke-width="2" stroke-dasharray="4,4" />
  <text x="450" y="232" font-family="sans-serif" font-size="11" font-weight="600" fill="#34d399">Flush (Threshold)</text>

  <!-- Disk SSTable Levels Container -->
  <rect x="40" y="260" width="770" height="260" rx="10" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="60" y="285" font-family="sans-serif" font-size="13" font-weight="700" fill="#94a3b8">PERSISTENT DURABLE STORAGE: SSTABLE RUNS</text>

  <!-- Level 0 -->
  <text x="60" y="325" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">Level 0:</text>
  <text x="60" y="340" font-family="sans-serif" font-size="10" fill="#64748b">(Overlapping)</text>

  <!-- SSTable 1 -->
  <g transform="translate(150, 305)">
    <rect width="180" height="50" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1" />
    <text x="90" y="22" font-family="sans-serif" font-size="11" font-weight="700" fill="#f8fafc" text-anchor="middle">SSTable 0-1 (Keys: 10-900)</text>
    <text x="90" y="40" font-family="sans-serif" font-size="9" fill="#fbbf24" text-anchor="middle">Bloom Filter + Fence Index</text>
  </g>

  <!-- SSTable 2 -->
  <g transform="translate(350, 305)">
    <rect width="180" height="50" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1" />
    <text x="90" y="22" font-family="sans-serif" font-size="11" font-weight="700" fill="#f8fafc" text-anchor="middle">SSTable 0-2 (Keys: 50-850)</text>
    <text x="90" y="40" font-family="sans-serif" font-size="9" fill="#fbbf24" text-anchor="middle">Bloom Filter + Fence Index</text>
  </g>

  <!-- Compaction Arrow -->
  <path d="M 400 365 L 400 405" fill="none" stroke="#f43f5e" stroke-width="2" />
  <text x="475" y="390" font-family="sans-serif" font-size="11" font-weight="700" fill="#f43f5e">Background Compaction (Merge-Sort)</text>

  <!-- Level 1 -->
  <text x="60" y="445" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">Level 1:</text>
  <text x="60" y="460" font-family="sans-serif" font-size="10" fill="#64748b">(Partitioned)</text>

  <g transform="translate(150, 425)">
    <rect width="180" height="50" rx="5" fill="#1e293b" stroke="#10b981" stroke-width="1" />
    <text x="90" y="22" font-family="sans-serif" font-size="11" font-weight="700" fill="#f8fafc" text-anchor="middle">SSTable 1-A [10-350]</text>
    <text x="90" y="40" font-family="sans-serif" font-size="9" fill="#34d399" text-anchor="middle">Purged Overwritten Keys</text>
  </g>
  <g transform="translate(350, 425)">
    <rect width="180" height="50" rx="5" fill="#1e293b" stroke="#10b981" stroke-width="1" />
    <text x="90" y="22" font-family="sans-serif" font-size="11" font-weight="700" fill="#f8fafc" text-anchor="middle">SSTable 1-B [351-700]</text>
    <text x="90" y="40" font-family="sans-serif" font-size="9" fill="#34d399" text-anchor="middle">Tombstones Removed</text>
  </g>
  <g transform="translate(550, 425)">
    <rect width="180" height="50" rx="5" fill="#1e293b" stroke="#10b981" stroke-width="1" />
    <text x="90" y="22" font-family="sans-serif" font-size="11" font-weight="700" fill="#f8fafc" text-anchor="middle">SSTable 1-C [701-999]</text>
    <text x="90" y="40" font-family="sans-serif" font-size="9" fill="#34d399" text-anchor="middle">Compacted Non-Overlapping</text>
  </g>

  <!-- Point Read Query Flow -->
  <rect x="580" y="100" width="230" height="105" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5" filter="url(#sh)"/>
  <text x="695" y="125" font-family="sans-serif" font-size="12" font-weight="700" fill="#a5b4fc" text-anchor="middle">READ PATH ORDER</text>
  <text x="695" y="145" font-family="sans-serif" font-size="10" fill="#e0e7ff" text-anchor="middle">1. Search Active MemTable</text>
  <text x="695" y="162" font-family="sans-serif" font-size="10" fill="#e0e7ff" text-anchor="middle">2. Check In-Memory Bloom Filter</text>
  <text x="695" y="179" font-family="sans-serif" font-size="10" fill="#e0e7ff" text-anchor="middle">3. Inspect L0 -> L1 -> L2 SSTables</text>
  <text x="695" y="196" font-family="sans-serif" font-size="9" fill="#fbbf24" text-anchor="middle">Bloom filter prunes 99% negative reads</text>
</svg>
"""
    with open(FIGURES_DIR / "lsm_tree_architecture.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/lsm_tree_architecture.svg")


def generate_learned_index_rmi_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 560" width="100%" height="100%">
  <defs>
    <linearGradient id="bgRmi" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c0a1f" />
      <stop offset="100%" stop-color="#181432" />
    </linearGradient>
    <filter id="fShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <rect width="850" height="560" fill="url(#bgRmi)" rx="14" />
  <text x="425" y="38" font-family="sans-serif" font-size="20" font-weight="700" fill="#faf5ff" text-anchor="middle">Recursive Model Index (RMI): CDF Function Approximation</text>
  <text x="425" y="60" font-family="sans-serif" font-size="12" fill="#c084fc" text-anchor="middle">Replacing Pointer B-Trees with Lightweight Mathematical Linear Splines (Kraska et al., SIGMOD 2018)</text>

  <!-- Query Key -->
  <rect x="350" y="85" width="150" height="42" rx="6" fill="#2e1065" stroke="#a855f7" stroke-width="2" filter="url(#fShadow)" />
  <text x="425" y="111" font-family="sans-serif" font-size="13" font-weight="700" fill="#f3e8ff" text-anchor="middle">Lookup Key: k</text>

  <!-- Down Arrow -->
  <line x1="425" y1="127" x2="425" y2="160" stroke="#a855f7" stroke-width="2" />

  <!-- Stage 1 Root Model -->
  <g transform="translate(250, 160)" filter="url(#fShadow)">
    <rect width="350" height="70" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="2" />
    <text x="175" y="28" font-family="sans-serif" font-size="14" font-weight="700" fill="#c7d2fe" text-anchor="middle">STAGE 1: ROOT LINEAR MODEL</text>
    <text x="175" y="48" font-family="sans-serif" font-size="12" fill="#e0e7ff" text-anchor="middle">Model: Leaf_Index = floor(a_0 * k + b_0)</text>
    <text x="175" y="63" font-family="sans-serif" font-size="10" fill="#38bdf8" text-anchor="middle">Routes Key Domain to Target Leaf Partition [0 .. M-1]</text>
  </g>

  <!-- Partition Routing Lines -->
  <line x1="330" y1="230" x2="160" y2="280" stroke="#818cf8" stroke-width="1.5" />
  <line x1="425" y1="230" x2="425" y2="280" stroke="#818cf8" stroke-width="1.5" />
  <line x1="520" y1="230" x2="690" y2="280" stroke="#818cf8" stroke-width="1.5" />

  <!-- Stage 2 Leaf Models -->
  <!-- Leaf 0 -->
  <g transform="translate(60, 280)" filter="url(#fShadow)">
    <rect width="200" height="75" rx="6" fill="#1f1841" stroke="#c084fc" stroke-width="1.5" />
    <text x="100" y="24" font-family="sans-serif" font-size="12" font-weight="700" fill="#f5d0fe" text-anchor="middle">Leaf Model 0</text>
    <text x="100" y="44" font-family="sans-serif" font-size="11" fill="#e9d5ff" text-anchor="middle">pos = a_0*k + b_0</text>
    <text x="100" y="63" font-family="sans-serif" font-size="10" fill="#34d399" text-anchor="middle">Error Bound: ± 3 slots</text>
  </g>

  <!-- Leaf 1 -->
  <g transform="translate(325, 280)" filter="url(#fShadow)">
    <rect width="200" height="75" rx="6" fill="#1f1841" stroke="#c084fc" stroke-width="1.5" />
    <text x="100" y="24" font-family="sans-serif" font-size="12" font-weight="700" fill="#f5d0fe" text-anchor="middle">Leaf Model 1 (Target)</text>
    <text x="100" y="44" font-family="sans-serif" font-size="11" fill="#e9d5ff" text-anchor="middle">pos = a_1*k + b_1</text>
    <text x="100" y="63" font-family="sans-serif" font-size="10" fill="#34d399" text-anchor="middle">Error Bound: ± 2 slots</text>
  </g>

  <!-- Leaf M-1 -->
  <g transform="translate(590, 280)" filter="url(#fShadow)">
    <rect width="200" height="75" rx="6" fill="#1f1841" stroke="#c084fc" stroke-width="1.5" />
    <text x="100" y="24" font-family="sans-serif" font-size="12" font-weight="700" fill="#f5d0fe" text-anchor="middle">Leaf Model M-1</text>
    <text x="100" y="44" font-family="sans-serif" font-size="11" fill="#e9d5ff" text-anchor="middle">pos = a_m*k + b_m</text>
    <text x="100" y="63" font-family="sans-serif" font-size="10" fill="#34d399" text-anchor="middle">Error Bound: ± 4 slots</text>
  </g>

  <!-- Target Prediction Line down to array -->
  <line x1="425" y1="355" x2="425" y2="400" stroke="#34d399" stroke-width="2" />
  <text x="480" y="385" font-family="sans-serif" font-size="11" font-weight="700" fill="#34d399">Predicted Offset p̂</text>

  <!-- Contiguous Sorted Data Array -->
  <rect x="50" y="410" width="750" height="60" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <text x="75" y="445" font-family="sans-serif" font-size="12" font-weight="700" fill="#94a3b8">Data Array:</text>

  <!-- Array Cells -->
  <g transform="translate(170, 420)">
    <rect x="0" width="60" height="40" fill="#1e293b" stroke="#475569" />
    <text x="30" y="25" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Key 20</text>

    <rect x="60" width="60" height="40" fill="#1e293b" stroke="#475569" />
    <text x="90" y="25" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Key 24</text>

    <rect x="120" width="70" height="40" fill="#1e293b" stroke="#475569" />
    <text x="155" y="25" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Key 29</text>

    <!-- Bounded Window (Target) -->
    <rect x="190" width="160" height="40" fill="#064e3b" stroke="#10b981" stroke-width="2" />
    <text x="270" y="25" font-family="sans-serif" font-size="11" font-weight="700" fill="#a7f3d0" text-anchor="middle">Bounded Window [p̂ - ε, p̂ + ε]</text>

    <rect x="350" width="70" height="40" fill="#1e293b" stroke="#475569" />
    <text x="385" y="25" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Key 45</text>

    <rect x="420" width="70" height="40" fill="#1e293b" stroke="#475569" />
    <text x="455" y="25" font-family="sans-serif" font-size="11" fill="#cbd5e1" text-anchor="middle">Key 50</text>
  </g>

  <!-- Final Callout -->
  <text x="425" y="510" font-family="sans-serif" font-size="12" font-weight="700" fill="#38bdf8" text-anchor="middle">Result: Bounded Binary Search completes in O(1) CPU cache lines. Memory footprint: 1.4 Bytes/Key.</text>
</svg>
"""
    with open(FIGURES_DIR / "learned_index_rmi.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/learned_index_rmi.svg")


def generate_benchmark_comparison_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 560" width="100%" height="100%">
  <defs>
    <linearGradient id="bgChart" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
  </defs>

  <rect width="850" height="560" fill="url(#bgChart)" rx="14" />
  <text x="425" y="38" font-family="sans-serif" font-size="20" font-weight="700" fill="#f8fafc" text-anchor="middle">Empirical Benchmark Head-to-Head (N=10,000 Real Keys)</text>
  <text x="425" y="60" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">Comparison of Point Lookup Latency (µs, lower is better) vs. Memory Footprint (Bytes/Key, lower is better)</text>

  <!-- Left Chart: Point Lookup Latency (µs) -->
  <g transform="translate(60, 100)">
    <rect width="330" height="380" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5" />
    <text x="165" y="30" font-family="sans-serif" font-size="14" font-weight="700" fill="#38bdf8" text-anchor="middle">POINT LOOKUP LATENCY (µs)</text>
    <text x="165" y="48" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">(Lower is Better)</text>

    <!-- Bars -->
    <!-- B+ Tree: 0.77 µs -->
    <text x="30" y="100" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">B+ Tree</text>
    <rect x="110" y="85" width="25" height="24" rx="4" fill="#38bdf8" />
    <text x="145" y="102" font-family="sans-serif" font-size="11" font-weight="700" fill="#38bdf8">0.77 µs</text>

    <!-- Static RMI: 1.86 µs -->
    <text x="30" y="160" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">Static RMI</text>
    <rect x="110" y="145" width="45" height="24" rx="4" fill="#a855f7" />
    <text x="165" y="162" font-family="sans-serif" font-size="11" font-weight="700" fill="#c084fc">1.86 µs</text>

    <!-- Dynamic ALEX: 6.44 µs -->
    <text x="30" y="220" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">Dynamic ALEX</text>
    <rect x="110" y="205" width="105" height="24" rx="4" fill="#10b981" />
    <text x="225" y="222" font-family="sans-serif" font-size="11" font-weight="700" fill="#34d399">6.44 µs</text>

    <!-- LSM-Tree: 16.03 µs -->
    <text x="30" y="280" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">LSM-Tree</text>
    <rect x="110" y="265" width="190" height="24" rx="4" fill="#f43f5e" />
    <text x="308" y="282" font-family="sans-serif" font-size="10" font-weight="700" fill="#f43f5e">16.03 µs</text>

    <text x="165" y="345" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">B+ Tree deterministic pointers deliver lowest</text>
    <text x="165" y="362" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">point read latency via memory cache pinning.</text>
  </g>

  <!-- Right Chart: Memory Footprint (Bytes/Key) -->
  <g transform="translate(460, 100)">
    <rect width="330" height="380" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5" />
    <text x="165" y="30" font-family="sans-serif" font-size="14" font-weight="700" fill="#a855f7" text-anchor="middle">INDEX MEMORY FOOTPRINT (B/Key)</text>
    <text x="165" y="48" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">(Lower is Better)</text>

    <!-- Bars -->
    <!-- Static RMI: 1.4 B/key -->
    <text x="30" y="100" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">Static RMI</text>
    <rect x="110" y="85" width="10" height="24" rx="4" fill="#a855f7" />
    <text x="130" y="102" font-family="sans-serif" font-size="11" font-weight="700" fill="#c084fc">1.4 B/key (&gt;64x compression)</text>

    <!-- B+ Tree: 90.1 B/key -->
    <text x="30" y="160" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">B+ Tree</text>
    <rect x="110" y="145" width="135" height="24" rx="4" fill="#38bdf8" />
    <text x="255" y="162" font-family="sans-serif" font-size="11" font-weight="700" fill="#38bdf8">90.1 B/key</text>

    <!-- Dynamic ALEX: 104.3 B/key -->
    <text x="30" y="220" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">Dynamic ALEX</text>
    <rect x="110" y="205" width="150" height="24" rx="4" fill="#10b981" />
    <text x="270" y="222" font-family="sans-serif" font-size="11" font-weight="700" fill="#34d399">104.3 B/key</text>

    <!-- LSM-Tree: 153.7 B/key -->
    <text x="30" y="280" font-family="sans-serif" font-size="12" font-weight="700" fill="#cbd5e1">LSM-Tree</text>
    <rect x="110" y="265" width="195" height="24" rx="4" fill="#f43f5e" />
    <text x="165" y="315" font-family="sans-serif" font-size="11" font-weight="700" fill="#f43f5e">153.7 B/key (Bloom filters + SSTables)</text>

    <text x="165" y="345" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Static RMI eliminates child node pointers,</text>
    <text x="165" y="362" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">compressing index footprint down to ~1 Byte/key.</text>
  </g>
</svg>
"""
    with open(FIGURES_DIR / "benchmark_comparison.svg", "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print("Generated: report/figures/benchmark_comparison.svg")


def main():
    download_reference_figures()
    generate_rum_conjecture_svg()
    generate_lsm_tree_svg()
    generate_learned_index_rmi_svg()
    generate_benchmark_comparison_svg()


if __name__ == "__main__":
    main()
