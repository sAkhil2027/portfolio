"""
LLM Generation Quality & Groundedness Metrics Module.
Evaluates answer faithfulness (0% hallucination), answer relevance, and context utilization.
"""

import re
from typing import List, Dict, Any, Set
from rag.models.document import SearchResult


class LLMEvaluator:
    """
    Evaluates LLM generated answers against retrieved RAG context chunks.
    """

    def _tokenize(self, text: str) -> Set[str]:
        return set(re.findall(r"\w+", text.lower()))

    def evaluate_faithfulness(self, response_text: str, retrieved_results: List[SearchResult]) -> Dict[str, Any]:
        """
        Evaluates faithfulness (groundedness). Checks if claim words in response exist in retrieved context.
        Higher score (closer to 1.0) means lower risk of hallucination.
        """
        if not response_text or not retrieved_results:
            return {"faithfulness_score": 0.0, "is_grounded": False}

        resp_tokens = self._tokenize(response_text)
        if not resp_tokens:
            return {"faithfulness_score": 1.0, "is_grounded": True}

        context_text = " ".join([res.chunk.text for res in retrieved_results])
        context_tokens = self._tokenize(context_text)

        # Filter out common stop words
        stop_words = {"is", "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "of", "with", "by"}
        claim_tokens = resp_tokens.difference(stop_words)

        if not claim_tokens:
            return {"faithfulness_score": 1.0, "is_grounded": True}

        supported_tokens = claim_tokens.intersection(context_tokens)
        score = len(supported_tokens) / len(claim_tokens)

        return {
            "faithfulness_score": score,
            "faithfulness_pct": score * 100.0,
            "supported_claims_count": len(supported_tokens),
            "total_claims_count": len(claim_tokens),
            "is_grounded": score >= 0.70
        }

    def evaluate_answer_relevance(self, query: str, response_text: str) -> Dict[str, Any]:
        """
        Evaluates keyword relevance between the user query and the generated response.
        """
        q_tokens = self._tokenize(query)
        r_tokens = self._tokenize(response_text)

        if not q_tokens:
            return {"relevance_score": 1.0}

        overlap = q_tokens.intersection(r_tokens)
        score = len(overlap) / len(q_tokens)

        return {
            "relevance_score": score,
            "relevance_pct": score * 100.0,
            "query_keywords_matched": list(overlap)
        }

    def evaluate_context_utilization(self, response_text: str, retrieved_results: List[SearchResult]) -> Dict[str, Any]:
        """
        Evaluates the proportion of retrieved chunks referenced in the final response.
        """
        if not retrieved_results:
            return {"utilization_pct": 0.0, "used_chunks_count": 0}

        r_tokens = self._tokenize(response_text)
        used_count = 0

        for res in retrieved_results:
            c_tokens = self._tokenize(res.chunk.text)
            if len(c_tokens.intersection(r_tokens)) >= 2:
                used_count += 1

        utilization_pct = (used_count / len(retrieved_results)) * 100.0

        return {
            "utilization_pct": utilization_pct,
            "used_chunks_count": used_count,
            "total_chunks_count": len(retrieved_results)
        }
