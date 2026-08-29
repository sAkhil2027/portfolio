"""
Unit tests for BM25, Vector, Hybrid retrievers and Reranker.
"""

import unittest
from rag.models.document import Chunk
from rag.retrieval.bm25 import BM25Retriever
from rag.retrieval.vector import VectorRetriever
from rag.retrieval.hybrid import HybridRetriever
from rag.retrieval.reranker import Reranker
from knowledge.schemas import DocumentMetadata


class TestRetrieval(unittest.TestCase):

    def setUp(self):
        meta = DocumentMetadata(source="test.md", title="AI Portfolio")
        self.chunks = [
            Chunk(chunk_id="c1", doc_id="d1", content="FastAPI web backend application with Python.", chunk_index=0, metadata=meta),
            Chunk(chunk_id="c2", doc_id="d2", content="Deep Learning model training with PyTorch and Transformers.", chunk_index=0, metadata=meta),
            Chunk(chunk_id="c3", doc_id="d3", content="Data Engineering pipeline with PostgreSQL and Redis.", chunk_index=0, metadata=meta),
        ]
        self.bm25 = BM25Retriever()
        self.bm25.index_chunks(self.chunks)

        self.vector = VectorRetriever()
        self.vector.index_chunks(self.chunks)

        self.hybrid = HybridRetriever(self.bm25, self.vector)
        self.reranker = Reranker()

    def test_bm25_search(self):
        results = self.bm25.search("FastAPI Python", top_k=2)
        self.assertGreater(len(results), 0)
        self.assertIn("FastAPI", results[0].chunk.content)

    def test_vector_search(self):
        results = self.vector.search("PyTorch Deep Learning", top_k=2)
        self.assertGreater(len(results), 0)

    def test_hybrid_search(self):
        results = self.hybrid.search("PostgreSQL Redis pipeline", top_k=2)
        self.assertGreater(len(results), 0)

    def test_reranker(self):
        candidates = self.hybrid.search("FastAPI", top_k=2)
        reranked = self.reranker.rerank("FastAPI", candidates, top_k=2)
        self.assertEqual(len(reranked), len(candidates))

    def test_metadata_filter(self):
        # Set source_type on chunks
        self.chunks[0].source_type = "project"
        self.chunks[1].source_type = "education"
        self.vector.index_chunks(self.chunks)

        results = self.vector.search("FastAPI", top_k=5, metadata_filter={"source_type": "project"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk.id, "c1")


if __name__ == "__main__":
    unittest.main()
