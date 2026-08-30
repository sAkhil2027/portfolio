"""
Unit tests for Environment Isolation & Production Fallback Guard.
"""

import os
import unittest

os.environ["FAST_EVAL_MODE"] = "1"

from rag.retrieval.qdrant import QdrantRetriever


class TestEnvironmentGuard(unittest.TestCase):

    def test_development_mode_fallback_permitted(self):
        os.environ["ENVIRONMENT"] = "development"
        # Invalid host location in dev mode should fall back without crashing
        retriever = QdrantRetriever(collection_name="test_dev", location="http://invalid-host-dev:6333")
        self.assertFalse(retriever._is_qdrant_available)
        self.assertIsNotNone(retriever._fallback_retriever)

    def test_production_mode_fallback_forbidden(self):
        os.environ["ENVIRONMENT"] = "production"
        # Invalid host location in prod mode should disable fallback
        retriever = QdrantRetriever(collection_name="test_prod", location="http://invalid-host-prod:6333")
        self.assertFalse(retriever._is_qdrant_available)
        self.assertIsNone(retriever._fallback_retriever)
        
        # Searching when Qdrant is down in production must raise RuntimeError
        with self.assertRaises(RuntimeError):
            retriever.search("FastAPI", top_k=2)

    @classmethod
    def tearDownClass(cls):
        os.environ["ENVIRONMENT"] = "development"


if __name__ == "__main__":
    unittest.main()
