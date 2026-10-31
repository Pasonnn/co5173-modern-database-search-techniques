"""Lexical Inverted Index and BM25 scoring modeling Lucene / Elasticsearch."""
from __future__ import annotations
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any
from src.common import OperationStats, estimate_object_memory


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric word tokenization."""
    return re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower())


@dataclass
class Posting:
    doc_id: int
    term_freq: int


class InvertedIndex:
    """Inverted Index with BM25 ranking and Boolean search.
    
    ponytail: Plain Python posting lists over SIMD-compressed Roaring Bitmaps and FST term dict; upgrade when corpus exceeds available memory.
    """

    def __init__(self, k1: float = 1.2, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.postings: dict[str, list[Posting]] = defaultdict(list)
        self.doc_lengths: dict[int, int] = {}
        self.doc_store: dict[int, dict[str, Any]] = {}
        self.total_tokens: int = 0
        self.stats = OperationStats()

    def index_document(self, doc_id: int, text: str, attributes: dict[str, Any] | None = None) -> None:
        tokens = tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        self.total_tokens += len(tokens)
        self.doc_store[doc_id] = {
            "text": text,
            "attrs": attributes or {},
        }

        counts = Counter(tokens)
        for term, tf in counts.items():
            self.postings[term].append(Posting(doc_id=doc_id, term_freq=tf))
            self.stats.pages_written += 1

    def search_boolean(self, terms: list[str], mode: str = "AND") -> list[int]:
        """Boolean intersection (AND) or union (OR) across posting lists."""
        clean_terms = [t.lower() for t in terms if t.lower() in self.postings]
        if not clean_terms:
            return []

        doc_sets = [{p.doc_id for p in self.postings[t]} for t in clean_terms]
        if mode.upper() == "AND":
            result = set.intersection(*doc_sets)
        else:
            result = set.union(*doc_sets)
        return sorted(result)

    def search_bm25(self, query: str, limit: int = 10) -> list[tuple[int, float]]:
        """BM25 relevance scoring matching Lucene's ranking function."""
        tokens = tokenize(query)
        if not tokens or not self.doc_lengths:
            return []

        n_docs = len(self.doc_lengths)
        avg_dl = self.total_tokens / max(1, n_docs)
        scores: dict[int, float] = defaultdict(float)

        for token in tokens:
            if token not in self.postings:
                continue
            plist = self.postings[token]
            df = len(plist)
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))

            for p in plist:
                dl = self.doc_lengths[p.doc_id]
                tf = p.term_freq
                # BM25 tf saturation formula
                tf_norm = (tf * (self.k1 + 1.0)) / (
                    tf + self.k1 * (1.0 - self.b + self.b * (dl / avg_dl))
                )
                scores[p.doc_id] += idf * tf_norm
                self.stats.comparisons += 1

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:limit]

    def range_filter(self, attr_key: str, min_val: float, max_val: float) -> list[int]:
        """Simple multi-attribute 1D range scan emulation (BKD tree target)."""
        matching: list[int] = []
        for doc_id, data in self.doc_store.items():
            val = data["attrs"].get(attr_key)
            if val is not None and min_val <= val <= max_val:
                matching.append(doc_id)
        return matching

    def memory_footprint_bytes(self) -> int:
        return estimate_object_memory(self.postings) + estimate_object_memory(self.doc_lengths)
