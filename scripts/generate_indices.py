import os
from rag.pipeline import RAGPipeline
from app import KNOWLEDGE_DIR, BM25_INDEX_PATH, VECTOR_INDEX_PATH

def main():
    # Initialise pipeline with the knowledge directory
    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    # Build documents, clean, chunk and index them
    pipeline.ingest_and_index()
    # Persist the two indexes to the expected locations
    pipeline.save_indices(BM25_INDEX_PATH, VECTOR_INDEX_PATH)
    print("[generate_indices] Saved BM25 index to:", BM25_INDEX_PATH)
    print("[generate_indices] Saved vector index to:", VECTOR_INDEX_PATH)

if __name__ == "__main__":
    main()
