"""
Reranker module for re-scoring and re-ordering search candidates.
"""

import re
from typing import List
from rag.models.document import SearchResult


class Reranker:
    """
    Reranks candidate SearchResults using term precision and context relevance.
    """

    def __init__(self, title_boost: float = 1.5, exact_match_boost: float = 2.0):
        self.title_boost = title_boost
        self.exact_match_boost = exact_match_boost

    def rerank(self, query: str, candidates: List[SearchResult], top_k: int = 5) -> List[SearchResult]:
        """
        Reranks a list of SearchResult candidate objects.
        """
        if not candidates:
            return []

        q_terms = set(re.findall(r"\w+", query.lower()))
        query_lower = query.lower().strip()

        reranked = []
        for cand in candidates:
            chunk = cand.chunk
            content_lower = chunk.text.lower()
            base_score = cand.score
            boost = 1.0

            # Exact match boost
            if query_lower in content_lower:
                boost *= self.exact_match_boost

            # Title matching boost
            title_val = None
            if isinstance(chunk.metadata, dict):
                title_val = chunk.metadata.get("title")
            elif hasattr(chunk.metadata, "title"):
                title_val = chunk.metadata.title

            if title_val:
                t_terms = set(re.findall(r"\w+", str(title_val).lower()))
                if q_terms.intersection(t_terms):
                    boost *= self.title_boost

            # Technology term overlap boost
            tech_val = None
            if isinstance(chunk.metadata, dict):
                tech_val = chunk.metadata.get("technologies")
            elif hasattr(chunk.metadata, "technologies"):
                tech_val = chunk.metadata.technologies

            if tech_val:
                tech_str = " ".join(tech_val).lower() if isinstance(tech_val, list) else str(tech_val).lower()
                if any(term in tech_str for term in q_terms):
                    boost *= 1.25

            final_score = base_score * boost
            reranked.append(SearchResult(
                chunk=chunk,
                score=float(final_score),
                retrieval_method=f"{cand.retrieval_method}+reranked"
            ))


        reranked.sort(key=lambda x: x.score, reverse=True)
        return reranked[:top_k]
