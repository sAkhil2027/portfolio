"""
Unit tests for QdrantVectorRetriever.
"""

import os
import unittest

os.environ["FAST_EVAL_MODE"] = "1"

from rag.models.document import DocumentChunk
from rag.retrieval.qdrant import QdrantRetriever


class TestQdrantRetriever(unittest.TestCase):

    def setUp(self):
        self.retriever = QdrantRetriever(collection_name="test_qdrant", location=":memory:")
        self.chunks = [
            DocumentChunk(
                id="q1",
                text="Building RAG AI Agent with FastAPI and Qdrant vector database.",
                source="project-1",
                source_type="project",
                category="projects",
                project_id="qdrant-rag",
                metadata={"technologies": ["Python", "FastAPI", "Qdrant"]}
            ),
            DocumentChunk(
                id="q2",
                text="Statistical machine learning algorithms and linear algebra coursework.",
                source="edu-1",
                source_type="education",
                category="education",
                education_id="iiit-bhagalpur",
                metadata={"technologies": ["Python", "NumPy"]}
            )
        ]
        self.retriever.index_chunks(self.chunks)

    def test_qdrant_search(self):
        results = self.retriever.search("Qdrant FastAPI", top_k=2)
        self.assertGreater(len(results), 0)
        self.assertIn("q1", [r.chunk.id for r in results])

    def test_qdrant_metadata_filter(self):
        results = self.retriever.search("Python", top_k=2, metadata_filter={"source_type": "project"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk.id, "q1")


if __name__ == "__main__":
    unittest.main()
