"""Dataset loader for benchmark evaluation: real-world open datasets with offline fallback."""
from __future__ import annotations
import json
import math
import os
import random
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

REAL_CITIES_URL = "https://raw.githubusercontent.com/datasets/world-cities/master/data/world-cities.csv"
REAL_QUOTES_URL = "https://raw.githubusercontent.com/dwyl/quotes/master/quotes.json"


def get_numerical_dataset(n: int = 20000, distribution: str = "real", seed: int = 42) -> list[int]:
    """Retrieves unique integer keys under real-world, zipfian, or uniform distribution.
    
    ponytail: In-memory list caching over streaming mmap; upgrade when dataset exceeds 10M records.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(seed)

    if distribution == "real":
        cache_file = DATA_DIR / "world_cities_ids.txt"
        keys: list[int] = []
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                keys = [int(line.strip()) for line in f if line.strip()]
        else:
            try:
                req = urllib.request.Request(REAL_CITIES_URL, headers={"User-Agent": "CO5173-Benchmark/1.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    lines = resp.read().decode("utf-8").strip().splitlines()
                # Header is name,country,subcountry,geonameid
                for line in lines[1:]:
                    parts = line.rsplit(",", 1)
                    if len(parts) == 2 and parts[1].strip().isdigit():
                        keys.append(int(parts[1].strip()))
                keys = list(dict.fromkeys(keys))  # deduplicate preserving order
                with open(cache_file, "w", encoding="utf-8") as f:
                    for k in keys:
                        f.write(f"{k}\n")
            except Exception:
                # Deterministic fallback: lognormal distribution matching geographical clustering
                keys = list({int(random.lognormvariate(14, 1.2)) for _ in range(n * 2)})

        if len(keys) < n:
            # Pad with deterministic offsets if larger sample requested
            max_k = max(keys) if keys else 1000000
            extra = [max_k + i * 7 for i in range(n - len(keys))]
            keys.extend(extra)
        
        selected = keys[:n]
        return selected

    elif distribution == "zipfian":
        # Zipf distribution using inverse transform sampling
        alpha = 1.25
        z_keys: set[int] = set()
        while len(z_keys) < n:
            # Generate zipf-like integer keys
            u = random.random()
            val = int(1.0 / (math.pow(1.0 - u, 1.0 / (alpha - 1.0))))
            z_keys.add(val)
        return list(z_keys)

    elif distribution == "uniform":
        return random.sample(range(1, n * 10), n)

    else:
        raise ValueError(f"Unknown distribution: {distribution}")


def get_text_corpus(n: int = 1000, seed: int = 42) -> list[dict[str, str]]:
    """Retrieves text documents for lexical search evaluation."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = DATA_DIR / "quotes_corpus.json"
    corpus: list[dict[str, str]] = []

    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            corpus = json.load(f)
    else:
        try:
            req = urllib.request.Request(REAL_QUOTES_URL, headers={"User-Agent": "CO5173-Benchmark/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            corpus = [{"id": i, "text": item.get("text", ""), "author": item.get("author", "")} for i, item in enumerate(data)]
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(corpus, f)
        except Exception:
            # Synthetic technical corpus fallback
            topics = [
                "database storage engine btree page slotted",
                "lsm log structured merge tree sstable compaction bloom filter",
                "learned index recursive model index cdf linear regression",
                "inverted index bm25 scoring posting list boolean search",
                "distributed storage write amplification memory footprint cache hit",
                "columnar parquet query optimization cost based optimizer index scan"
            ]
            corpus = [{"id": i, "text": f"Document {i} discusses {random.choice(topics)} with high performance metrics.", "author": "System"} for i in range(n)]

    if len(corpus) < n:
        # Repeat with variation if larger corpus requested
        base_len = len(corpus)
        for i in range(base_len, n):
            doc = corpus[i % base_len].copy()
            doc["id"] = i
            corpus.append(doc)

    return corpus[:n]
