"""
BM25 Lexical Keyword Retriever module.
"""

import math
import pickle
import re
from typing import List, Dict, Tuple, Optional, Any
from rag.models.document import DocumentChunk, Chunk, SearchResult
from rag.retrieval.vector import matches_metadata_filter


class BM25Retriever:
    """
    BM25 Sparse Lexical Keyword Search Index with Metadata Payload Filtering.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks: List[DocumentChunk] = []
        self.corpus_tokens: List[List[str]] = []
        self.doc_len: List[int] = []
        self.avgdl: float = 0.0
        self.doc_freqs: List[Dict[str, int]] = []
        self.idf: Dict[str, float] = {}

    STOPWORDS = {
        "does", "do", "did", "have", "has", "had", "is", "am", "are", "was", "were",
        "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of", "with",
        "by", "any", "all", "some", "tell", "me", "about", "what", "which", "who",
        "how", "where", "when", "why", "can", "could", "would", "should", "his", "her",
        "their", "akhil", "akhils"
    }

    def _normalize_token(self, token: str) -> str:
        """Normalizes English plurals and standard suffixes."""
        if token.endswith("ies") and len(token) > 4:
            return token[:-3] + "y"
        if token.endswith("es") and len(token) > 3 and token[-3] in ("s", "x", "z", "c", "h"):
            return token[:-2]
        if token.endswith("s") and not token.endswith("ss") and len(token) > 3:
            return token[:-1]
        return token

    def _tokenize(self, text: str, is_query: bool = False) -> List[str]:
        raw_tokens = re.findall(r"\w+", text.lower())
        tokens = []
        for t in raw_tokens:
            if is_query and t in self.STOPWORDS:
                continue
            norm = self._normalize_token(t)
            tokens.append(norm)
            if norm != t:
                tokens.append(t)

        if is_query and not tokens:
            tokens = [self._normalize_token(t) for t in raw_tokens]

        return tokens

    def index_chunks(self, chunks: List[DocumentChunk]):
        """
        Builds the BM25 index over a list of DocumentChunk objects.
        """
        self.chunks = chunks
        self.corpus_tokens = [self._tokenize(c.text, is_query=False) for c in chunks]
        self.doc_len = [len(tokens) for tokens in self.corpus_tokens]
        num_docs = len(chunks)

        if num_docs == 0:
            self.avgdl = 0.0
            return

        self.avgdl = sum(self.doc_len) / float(num_docs)

        self.doc_freqs = []
        df_counts: Dict[str, int] = {}

        for tokens in self.corpus_tokens:
            frequencies: Dict[str, int] = {}
            for t in tokens:
                frequencies[t] = frequencies.get(t, 0) + 1
            self.doc_freqs.append(frequencies)

            for t in frequencies.keys():
                df_counts[t] = df_counts.get(t, 0) + 1

        self.idf = {}
        for word, freq in df_counts.items():
            self.idf[word] = math.log((num_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """
        Searches the BM25 index and returns top_k SearchResult matches with optional metadata filtering.
        """
        if not self.chunks or self.avgdl == 0.0:
            return []

        q_tokens = self._tokenize(query, is_query=True)
        scores: List[float] = [0.0] * len(self.chunks)

        for i, doc_freq in enumerate(self.doc_freqs):
            chunk = self.chunks[i]
            if metadata_filter and not matches_metadata_filter(chunk, metadata_filter):
                continue

            score = 0.0
            d_len = self.doc_len[i]
            for token in q_tokens:
                if token not in doc_freq:
                    continue
                tf = doc_freq[token]
                idf = self.idf.get(token, 0.0)
                numerator = idf * tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (d_len / self.avgdl))
                score += numerator / denominator
            scores[i] = score

        indexed_scores = list(enumerate(scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in indexed_scores[:top_k]:
            chunk = self.chunks[idx]
            if metadata_filter and not matches_metadata_filter(chunk, metadata_filter):
                continue
            if score > 0.0 or len(results) < top_k:
                results.append(SearchResult(
                    chunk=chunk,
                    score=float(score),
                    retrieval_method="bm25"
                ))

        return results

    def save(self, filepath: str):
        """
        Saves the BM25 index to a pickle file.
        """
        with open(filepath, "wb") as f:
            pickle.dump({
                "k1": self.k1,
                "b": self.b,
                "chunks": [c.model_dump() for c in self.chunks],
                "corpus_tokens": self.corpus_tokens,
                "doc_len": self.doc_len,
                "avgdl": self.avgdl,
                "doc_freqs": self.doc_freqs,
                "idf": self.idf,
            }, f)

    def load(self, filepath: str):
        """
        Loads the BM25 index from a pickle file.
        """
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            self.k1 = data["k1"]
            self.b = data["b"]
            self.chunks = [DocumentChunk(**c) for c in data["chunks"]]
            self.corpus_tokens = data["corpus_tokens"]
            self.doc_len = data["doc_len"]
            self.avgdl = data["avgdl"]
            self.doc_freqs = data["doc_freqs"]
            self.idf = data["idf"]

