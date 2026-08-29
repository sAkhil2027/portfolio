"""
Chunking & Retrieval Metrics Module.
Calculates HitRate@K, Precision@K, Recall@K, and MRR (Mean Reciprocal Rank).
"""

from typing import List, Dict, Any, Set
from rag.pipeline import RAGPipeline


class RetrievalEvaluator:
    """
    Evaluates chunking and retrieval performance using standard IR metrics.
    """

    def __init__(self, pipeline: RAGPipeline = None):
        self.pipeline = pipeline

    def evaluate_query(self, query: str, expected_docs: List[str], top_k: int = 3, mode: str = "hybrid") -> Dict[str, Any]:
        """
        Evaluates a single query against expected ground-truth target document IDs/sources.
        """
        if not self.pipeline:
            raise ValueError("RAGPipeline instance is required for evaluation.")

        results = self.pipeline.query(query, mode=mode, top_k=top_k)
        retrieved_sources = [res.chunk.source for res in results]
        retrieved_ids = [res.chunk.id for res in results]

        expected_set = set(expected_docs)

        # Check matching sources or chunk IDs
        matches = [s for s in retrieved_sources if s in expected_set or any(exp in s for exp in expected_set)]
        if not matches:
            matches = [c_id for c_id in retrieved_ids if c_id in expected_set or any(exp in c_id for exp in expected_set)]

        is_hit = len(matches) > 0
        hit_score = 1.0 if is_hit else 0.0

        # Calculate MRR (Reciprocal Rank of first matching hit)
        mrr = 0.0
        for rank, src in enumerate(retrieved_sources, start=1):
            if src in expected_set or any(exp in src for exp in expected_set):
                mrr = 1.0 / rank
                break

        precision = len(matches) / top_k if top_k > 0 else 0.0
        recall = len(matches) / len(expected_set) if expected_set else 0.0

        return {
            "query": query,
            "top_k": top_k,
            "mode": mode,
            "is_hit": is_hit,
            "hit_score": hit_score,
            "precision": precision,
            "recall": recall,
            "mrr": mrr,
            "retrieved_sources": retrieved_sources,
            "expected_docs": expected_docs
        }

    def evaluate_benchmark(self, eval_dataset: List[Dict[str, Any]], top_k: int = 3, mode: str = "hybrid") -> Dict[str, Any]:
        """
        Evaluates a full benchmark dataset of evaluation pairs.
        """
        eval_results = []
        total_hits = 0
        total_precision = 0.0
        total_recall = 0.0
        total_mrr = 0.0
        n = len(eval_dataset)

        if n == 0:
            return {"hit_rate_pct": 0.0, "avg_precision_pct": 0.0, "avg_recall_pct": 0.0, "avg_mrr": 0.0}

        for item in eval_dataset:
            query = item["query"]
            expected = item["expected_docs"]
            res = self.evaluate_query(query, expected, top_k=top_k, mode=mode)
            eval_results.append(res)

            if res["is_hit"]:
                total_hits += 1
            total_precision += res["precision"]
            total_recall += res["recall"]
            total_mrr += res["mrr"]

        return {
            "total_queries": n,
            "top_k": top_k,
            "mode": mode,
            "hit_rate_pct": (total_hits / n) * 100.0,
            "avg_precision_pct": (total_precision / n) * 100.0,
            "avg_recall_pct": (total_recall / n) * 100.0,
            "avg_mrr": total_mrr / n,
            "details": eval_results
        }
