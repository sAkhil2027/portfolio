"""
Hybrid Retriever module.
Combines sparse BM25 search scores and dense Vector search scores via Reciprocal Rank Fusion (RRF).
"""

from typing import List, Dict, Any, Optional
from rag.models.document import SearchResult, DocumentChunk
from rag.retrieval.bm25 import BM25Retriever
from rag.retrieval.vector import VectorRetriever


class HybridRetriever:
    """
    Hybrid Retriever integrating BM25 + Dense Vector retrieval with RRF and Metadata Payload Filtering.
    """

    def __init__(self, bm25_retriever: BM25Retriever, vector_retriever: VectorRetriever, rrf_k: int = 60):
        self.bm25 = bm25_retriever
        self.vector = vector_retriever
        self.rrf_k = rrf_k

    def search(self, query: str, top_k: int = 5, bm25_weight: float = 0.5, vector_weight: float = 0.5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """
        Performs hybrid retrieval using Reciprocal Rank Fusion (RRF) with optional metadata filtering.
        """
        bm25_results = self.bm25.search(query, top_k=top_k * 2, metadata_filter=metadata_filter)
        vector_results = self.vector.search(query, top_k=top_k * 2, metadata_filter=metadata_filter)

        chunk_map: Dict[str, DocumentChunk] = {}
        rrf_scores: Dict[str, float] = {}

        # Process BM25 rankings
        for rank, res in enumerate(bm25_results, start=1):
            c_id = res.chunk.id
            chunk_map[c_id] = res.chunk
            score = bm25_weight * (1.0 / (self.rrf_k + rank))
            rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + score

        # Process Vector rankings
        for rank, res in enumerate(vector_results, start=1):
            c_id = res.chunk.id
            chunk_map[c_id] = res.chunk
            score = vector_weight * (1.0 / (self.rrf_k + rank))
            rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + score

        sorted_chunks = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for c_id, score in sorted_chunks[:top_k]:
            results.append(SearchResult(
                chunk=chunk_map[c_id],
                score=float(score),
                retrieval_method="hybrid"
            ))

        return results

