"""
Interactive Retrieval Testing Script.
Queries the pre-built RAG pipeline and Qdrant index to test retrieval precision and chunk quality.

Usage: python scripts/test_retrieval.py
"""

import os
import sys

# Ensure root workspace directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from rag.pipeline import RAGPipeline

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")


def run_sample_queries():
    print("=================================================================")
    print("           RAG HYBRID RETRIEVAL INTERACTIVE TESTER               ")
    print("=================================================================\n")

    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    
    # Fast test mode if ST offline
    if os.environ.get("FAST_EVAL_MODE") == "1":
        pipeline.embedder._initialized = True
        pipeline.embedder._st_model = None

    pipeline.ingest_and_index()

    test_queries = [
        ("FastAPI project details", {"source_type": "project"}),
        ("Where did Akhil complete B.Tech degree?", None),
        ("What Machine Learning & Deep Learning skills does Akhil have?", {"source_type": "skill"}),
    ]

    for q, meta_filter in test_queries:
        print(f"\nQUERY: '{q}' | Filter: {meta_filter}")
        results = pipeline.query(q, mode="hybrid", top_k=2, metadata_filter=meta_filter)

        for rank, res in enumerate(results, start=1):
            print(f"  [{rank}] Score: {res.score:.4f} | Method: {res.retrieval_method} | ID: {res.chunk.id}")
            print(f"      Source: {res.chunk.source} | Section: {res.chunk.section}")
            print(f"      Content: {res.chunk.text[:120]}...\n")

    print("=================================================================")
    print("                 [SUCCESS] ALL TEST QUERIES COMPLETED            ")
    print("=================================================================\n")


if __name__ == "__main__":
    run_sample_queries()
