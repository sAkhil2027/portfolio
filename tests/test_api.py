"""
FastAPI RAG Search REST API Endpoint Integration Tests.
"""

import os
import unittest
from fastapi.testclient import TestClient

# Set fast eval mode for unit testing
os.environ["FAST_EVAL_MODE"] = "1"

from app import create_app


class TestRAGAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = TestClient(cls.app)

    def test_rag_search_endpoint(self):
        with TestClient(self.app) as client:
            response = client.post(
                "/api/rag/search",
                json={
                    "query": "FastAPI",
                    "top_k": 2,
                    "mode": "bm25"
                }
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertGreater(len(data["matches"]), 0)

    def test_rag_search_with_metadata_filter(self):
        with TestClient(self.app) as client:
            response = client.post(
                "/api/rag/search",
                json={
                    "query": "Python",
                    "top_k": 2,
                    "mode": "bm25",
                    "source_type": "project"
                }
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            if data["matches"]:
                self.assertEqual(data["matches"][0]["source_type"], "project")

    def test_health_check_endpoint(self):
        with TestClient(self.app) as client:
            response = client.get("/health")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "healthy")
            self.assertIn("pre_loaded_chunks", data)


if __name__ == "__main__":
    unittest.main()
