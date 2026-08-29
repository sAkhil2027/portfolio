"""
Unit tests for Qdrant and Vector Metadata Payload Filtering.
"""

import os
import unittest

os.environ["FAST_EVAL_MODE"] = "1"

from rag.models.document import DocumentChunk
from rag.retrieval.qdrant import QdrantRetriever
from rag.retrieval.vector import matches_metadata_filter


class TestMetadataFiltering(unittest.TestCase):

    def setUp(self):
        self.chunk1 = DocumentChunk(
            id="proj_1",
            text="YouTube AI RAG Chatbot built with FastAPI, LangChain, and Qdrant.",
            source="youtube-ai-rag-chatbot",
            source_type="project",
            category="generative_ai",
            project_id="youtube-ai-rag-chatbot",
            metadata={"technologies": ["Python", "FastAPI", "Qdrant", "LangChain"]}
        )
        self.chunk2 = DocumentChunk(
            id="edu_1",
            text="B.Tech in Mechatronics and Automation Engineering from IIIT Bhagalpur.",
            source="education-iiit-bhagalpur",
            source_type="education",
            category="education",
            education_id="iiit-bhagalpur",
            metadata={"technologies": ["Python", "C++", "ROSMoveIt"]}
        )
        self.retriever = QdrantRetriever(collection_name="test_meta", location=":memory:")
        self.retriever.index_chunks([self.chunk1, self.chunk2])

    def test_single_attribute_filter(self):
        self.assertTrue(matches_metadata_filter(self.chunk1, {"source_type": "project"}))
        self.assertFalse(matches_metadata_filter(self.chunk2, {"source_type": "project"}))

    def test_list_contains_filter(self):
        self.assertTrue(matches_metadata_filter(self.chunk1, {"technologies": "FastAPI"}))
        self.assertFalse(matches_metadata_filter(self.chunk2, {"technologies": "FastAPI"}))

    def test_qdrant_metadata_search(self):
        results = self.retriever.search("FastAPI", top_k=2, metadata_filter={"source_type": "project"})
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].chunk.id, "proj_1")


if __name__ == "__main__":
    unittest.main()
