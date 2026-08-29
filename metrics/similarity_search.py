"""
Similarity Search Evaluation & Mode Comparison Module.
Benchmarks BM25, Vector, and Hybrid search latency, score distributions, and mode agreements.
"""

import time
from typing import List, Dict, Any, Set
from rag.pipeline import RAGPipeline


class SearchEvaluator:
    """
    Evaluator for comparing similarity search modes (BM25 vs Vector vs Hybrid).
    """

    def __init__(self, pipeline: RAGPipeline = None):
        self.pipeline = pipeline

    def compare_modes(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Runs query across BM25, Vector, and Hybrid modes, measuring latency and result overlaps.
        """
        if not self.pipeline:
            raise ValueError("RAGPipeline instance is required for evaluation.")

        modes = ["bm25", "vector", "hybrid"]
        mode_results = {}

        for mode in modes:
            t0 = time.perf_counter()
            results = self.pipeline.query(query, mode=mode, top_k=top_k, rerank=False)
            t1 = time.perf_counter()

            latency_ms = (t1 - t0) * 1000.0
            scores = [res.score for res in results]
            chunk_ids = [res.chunk.id for res in results]

            mode_results[mode] = {
                "latency_ms": latency_ms,
                "top_chunk_ids": chunk_ids,
                "scores": scores,
                "max_score": max(scores) if scores else 0.0,
                "avg_score": sum(scores) / len(scores) if scores else 0.0
            }

        # Calculate rank overlap agreement between BM25 and Vector
        bm25_ids = set(mode_results["bm25"]["top_chunk_ids"])
        vector_ids = set(mode_results["vector"]["top_chunk_ids"])
        overlap_count = len(bm25_ids.intersection(vector_ids))
        overlap_pct = (overlap_count / top_k) * 100.0 if top_k > 0 else 0.0

        return {
            "query": query,
            "top_k": top_k,
            "bm25_vs_vector_overlap_pct": overlap_pct,
            "mode_benchmarks": mode_results
        }

    def benchmark_queries(self, test_queries: List[str], top_k: int = 5) -> Dict[str, Any]:
        """
        Runs comparison benchmark over a suite of sample queries.
        """
        results = []
        total_overlap = 0.0
        mode_latencies = {"bm25": 0.0, "vector": 0.0, "hybrid": 0.0}

        for q in test_queries:
            res = self.compare_modes(q, top_k=top_k)
            results.append(res)
            total_overlap += res["bm25_vs_vector_overlap_pct"]

            for m in ["bm25", "vector", "hybrid"]:
                mode_latencies[m] += res["mode_benchmarks"][m]["latency_ms"]

        n = len(test_queries) if test_queries else 1
        avg_latencies = {m: mode_latencies[m] / n for m in mode_latencies}

        return {
            "num_queries": len(test_queries),
            "top_k": top_k,
            "avg_bm25_vs_vector_overlap_pct": total_overlap / n,
            "avg_latencies_ms": avg_latencies,
            "details": results
        }
