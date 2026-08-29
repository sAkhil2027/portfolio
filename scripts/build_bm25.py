"""
Build BM25 Index Script.
Ingests knowledge documents, generates text chunks, builds BM25 index, and saves to knowledge/bm25_index.pkl.
"""

import os
import sys

# Ensure root workspace directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.pipeline import RAGPipeline

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
BM25_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "bm25_index.pkl")


def main():
    print("--- Building BM25 Search Index ---")
    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    pipeline.ingest_and_index()
    pipeline.bm25_retriever.save(BM25_INDEX_PATH)
    print(f"[SUCCESS] BM25 Index saved to {BM25_INDEX_PATH}")


if __name__ == "__main__":
    main()
