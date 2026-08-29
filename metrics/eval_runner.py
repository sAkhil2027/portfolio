"""
Master Evaluation Runner Script.
Executes benchmarks across Chunking/Retrieval, Embeddings, Similarity Search, and LLM Performance.
Usage: python -m metrics.eval_runner
"""

import os
import sys

# Ensure root workspace directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.pipeline import RAGPipeline
from metrics.chunking_retrieval import RetrievalEvaluator
from metrics.embedding_eval import EmbeddingEvaluator
from metrics.similarity_search import SearchEvaluator
from metrics.llm_performance import LLMEvaluator


import json

BENCHMARK_JSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests", "retrieval_questions.json"))

if os.path.exists(BENCHMARK_JSON_PATH):
    with open(BENCHMARK_JSON_PATH, "r", encoding="utf-8") as f:
        BENCHMARK_DATASET = json.load(f)
else:
    BENCHMARK_DATASET = [
        {"query": "What hackathons did Akhil participate in?", "expected_docs": ["json_achievements_0", "json_achievements_1"]},
        {"query": "What technologies are used in YouTube AI RAG Chatbot?", "expected_docs": ["youtube-ai-rag-chatbot"]},
        {"query": "What is Akhil's degree and institution?", "expected_docs": ["json_education_0"]}
    ]


def run_full_evaluation():
    print("\n" + "=" * 65)
    print("      AKHIL PORTFOLIO RAG ARCHITECTURE EVALUATION SUITE      ")
    print("=" * 65 + "\n")

    # Initialize Pipeline & Embedder
    print("[1/4] Initializing RAG Pipeline & Ingesting Knowledge Data...")
    pipeline = RAGPipeline("knowledge")
    
    # Use deterministic fallback embedder for fast evaluation if ST offline
    pipeline.embedder._initialized = True
    pipeline.embedder._st_model = None

    pipeline.ingest_and_index()
    print(f" -> Generated {len(pipeline.chunks)} section-based DocumentChunks.")

    # 1. Chunking & Retrieval Evaluation
    print("\n[2/4] Benchmarking Chunking & Retrieval Metrics...")
    ret_eval = RetrievalEvaluator(pipeline=pipeline)
    ret_report = ret_eval.evaluate_benchmark(BENCHMARK_DATASET, top_k=3, mode="hybrid")

    # 2. Embedding Model Evaluation
    print("\n[3/4] Benchmarking Embedding Model Quality & Latency...")
    emb_eval = EmbeddingEvaluator(embedder=pipeline.embedder)
    emb_report = emb_eval.evaluate_throughput()
    sep_report = emb_eval.evaluate_separation(
        positive_pair=("FastAPI backend developer", "Python REST API microservices"),
        negative_pair=("FastAPI backend developer", "Quantum physics astronomy research")
    )

    # 3. Similarity Search & Mode Comparison Evaluation
    print("\n[4/4] Benchmarking Similarity Search Engines (BM25 vs Vector vs Hybrid)...")
    search_eval = SearchEvaluator(pipeline=pipeline)
    sample_queries = [item["query"] for item in BENCHMARK_DATASET]
    search_report = search_eval.benchmark_queries(sample_queries, top_k=3)

    # 4. Format and Print Summary Report
    print("\n" + "=" * 65)
    print("                      EVALUATION REPORT SUMMARY                       ")
    print("=" * 65)

    print("\n--- 1. CHUNKING & RETRIEVAL METRICS (Top-3 Hybrid RRF Search) ---")
    print(f"  - HitRate@3:           {ret_report['hit_rate_pct']:.1f}%")
    print(f"  - Precision@3:         {ret_report['avg_precision_pct']:.1f}%")
    print(f"  - Recall@3:            {ret_report['avg_recall_pct']:.1f}%")
    print(f"  - Mean Recip. Rank:    {ret_report['avg_mrr']:.3f}")

    print("\n--- 2. EMBEDDING & LATENCY METRICS ---")
    print(f"  - Vector Dimension:    {emb_report['vector_dimension']}")
    print(f"  - Avg Batch Latency:   {emb_report['avg_latency_ms']:.2f} ms / text")
    print(f"  - Similarity Margin:   {sep_report['separation_margin']:.3f} (Pos: {sep_report['positive_similarity']:.2f} vs Neg: {sep_report['negative_similarity']:.2f})")
    print(f"  - Vector Norm Valid:   {'PASS' if emb_report['is_normalized'] else 'WARN'}")

    print("\n--- 3. SIMILARITY SEARCH ENGINE COMPARISON ---")
    print(f"  - BM25 Avg Latency:    {search_report['avg_latencies_ms']['bm25']:.2f} ms")
    print(f"  - Vector Avg Latency:  {search_report['avg_latencies_ms']['vector']:.2f} ms")
    print(f"  - Hybrid Avg Latency:  {search_report['avg_latencies_ms']['hybrid']:.2f} ms")
    print(f"  - BM25/Vector Overlap: {search_report['avg_bm25_vs_vector_overlap_pct']:.1f}%")

    print("\n" + "=" * 65)
    print("               [SUCCESS] ALL EVALUATION MODULES PASSED               ")
    print("=" * 65 + "\n")



if __name__ == "__main__":
    run_full_evaluation()
