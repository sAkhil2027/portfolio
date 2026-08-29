"""
Unified Ingestion & Indexing Script for Akhil Portfolio RAG Architecture.
Ingests knowledge documents, chunks text, generates dense vector embeddings and sparse BM25 vectors,
and indexes into both local JSON persistence and Qdrant Vector Store.

Usage: python scripts/index.py
"""

import os
import sys

# Ensure root workspace directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from rag.pipeline import RAGPipeline
from rag.retrieval.qdrant import QdrantRetriever

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
BM25_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "bm25_index.pkl")
VECTOR_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "vector_index.json")


def main():
    print("=================================================================")
    print("          UNIFIED RAG KNOWLEDGE INGESTION & INDEXING           ")
    print("=================================================================\n")

    # 1. Initialize Pipeline & Ingest Knowledge Base
    print("[1/3] Loading documents, applying cleaner & section chunking...")
    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    pipeline.ingest_and_index()

    # 2. Save Local BM25 and Vector Indices
    print("\n[2/3] Saving local persistence files (bm25_index.pkl & vector_index.json)...")
    pipeline.save_indices(BM25_INDEX_PATH, VECTOR_INDEX_PATH)
    print(f" -> BM25 Index saved to:   {BM25_INDEX_PATH}")
    print(f" -> Vector Index saved to: {VECTOR_INDEX_PATH}")

    # 3. Index Dense + Sparse BM25 Vectors to Qdrant Store (Cloud / Local / Memory)
    qdrant_url = os.getenv("QDRANT_URL", "").strip()
    target_loc = qdrant_url if qdrant_url else os.path.join(KNOWLEDGE_DIR, "qdrant_db")

    print(f"\n[3/3] Indexing Dense + Sparse BM25 Vectors to Qdrant ({target_loc})...")
    qdrant_retriever = QdrantRetriever(embedder=pipeline.embedder, location=target_loc)
    qdrant_retriever.index_chunks(pipeline.chunks)
    print(f"[SUCCESS] Qdrant Multi-Vector Collection successfully indexed!")

    print("\n=================================================================")
    print("           [SUCCESS] MASTER INDEXING COMPLETE                    ")
    print("=================================================================\n")


if __name__ == "__main__":
    main()
