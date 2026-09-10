import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from rag.pipeline import RAGPipeline

KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
BM25_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "bm25_index.pkl")
VECTOR_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "vector_index.json")

def main():
    print("[generate_indices] Ingesting and building RAG indices...")
    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    pipeline.ingest_and_index()
    pipeline.save_indices(BM25_INDEX_PATH, VECTOR_INDEX_PATH)
    print(f"[generate_indices] Saved BM25 index ({len(pipeline.chunks)} chunks) to: {BM25_INDEX_PATH}")
    print(f"[generate_indices] Saved vector index to: {VECTOR_INDEX_PATH}")

if __name__ == "__main__":
    main()

