"""
Index Dense Vectors Script.
Ingests knowledge documents, generates vector embeddings, builds Vector index, and saves to knowledge/vector_index.json.
"""

import os
import sys

# Ensure root workspace directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.pipeline import RAGPipeline

from rag.retrieval.qdrant_vector import QdrantVectorRetriever

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
VECTOR_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "vector_index.json")
QDRANT_DIR = os.path.join(KNOWLEDGE_DIR, "qdrant_db")


def main():
    print("--- Building Dense Vector Search Index ---")
    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    pipeline.ingest_and_index()
    pipeline.vector_retriever.save(VECTOR_INDEX_PATH)
    print(f"[SUCCESS] In-Memory Vector Index saved to {VECTOR_INDEX_PATH}")

    print("--- Building Persistent Qdrant Vector Storage ---")
    qdrant_retriever = QdrantVectorRetriever(embedder=pipeline.embedder, location=QDRANT_DIR)
    qdrant_retriever.index_chunks(pipeline.chunks)
    print(f"[SUCCESS] Persistent Qdrant Vector Storage saved to {QDRANT_DIR}")


if __name__ == "__main__":
    main()
