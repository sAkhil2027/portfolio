"""
Dense Vector Similarity Retriever module.
"""

import json
import math
import os
from typing import List, Tuple, Dict, Any, Optional
from rag.models.document import DocumentChunk, Chunk, SearchResult
from rag.embeddings.embedder import TextEmbedder


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot / (norm1 * norm2)


def matches_metadata_filter(chunk: DocumentChunk, filter_dict: Optional[Dict[str, Any]]) -> bool:
    if not filter_dict:
        return True
    for key, expected_val in filter_dict.items():
        val = getattr(chunk, key, None)
        if val is None and hasattr(chunk, "metadata") and isinstance(chunk.metadata, dict):
            val = chunk.metadata.get(key)

        if val is None:
            return False

        if isinstance(val, list):
            if isinstance(expected_val, list):
                if not any(item in val for item in expected_val):
                    return False
            else:
                if expected_val not in val and str(expected_val).lower() not in [str(x).lower() for x in val]:
                    return False
        else:
            if str(val).lower() != str(expected_val).lower():
                return False
    return True


class VectorRetriever:
    """
    Dense Vector Similarity Search Index with Metadata Payload Filtering.
    """

    def __init__(self, embedder: TextEmbedder = None):
        self.embedder = embedder or TextEmbedder()
        self.chunks: List[DocumentChunk] = []
        self.vectors: List[List[float]] = []

    def index_chunks(self, chunks: List[DocumentChunk]):
        """
        Generates vector embeddings and builds index for DocumentChunk objects.
        """
        self.chunks = chunks
        if not chunks:
            self.vectors = []
            return

        texts = [c.text for c in chunks]
        self.vectors = self.embedder.embed_batch(texts)

    def search(self, query: str, top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """
        Searches vector index using cosine similarity against query embedding with optional metadata filtering.
        """
        if not self.chunks or not self.vectors:
            return []

        q_vec = self.embedder.embed_text(query)
        scores: List[Tuple[int, float]] = []

        for idx, doc_vec in enumerate(self.vectors):
            chunk = self.chunks[idx]
            if metadata_filter and not matches_metadata_filter(chunk, metadata_filter):
                continue
            sim = cosine_similarity(q_vec, doc_vec)
            scores.append((idx, sim))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:top_k]:
            results.append(SearchResult(
                chunk=self.chunks[idx],
                score=float(score),
                retrieval_method="vector"
            ))

        return results

    def save(self, filepath: str):
        """
        Saves vector index and chunks to JSON file.
        """
        data = {
            "chunks": [c.model_dump() for c in self.chunks],
            "vectors": self.vectors
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load(self, filepath: str):
        """
        Loads vector index and chunks from JSON file.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.chunks = [DocumentChunk(**c) for c in data["chunks"]]
            self.vectors = data["vectors"]

