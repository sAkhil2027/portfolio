"""
Unit tests for end-to-end RAGPipeline.
"""

import os
import tempfile
import unittest
from rag.pipeline import RAGPipeline


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        structured_dir = os.path.join(self.temp_dir, "structured")
        documents_dir = os.path.join(self.temp_dir, "documents")
        os.makedirs(structured_dir, exist_ok=True)
        os.makedirs(documents_dir, exist_ok=True)

        with open(os.path.join(structured_dir, "profile.json"), "w") as f:
            f.write('{"name": "Akhil", "title": "AI Engineer"}')

        with open(os.path.join(documents_dir, "bio.md"), "w") as f:
            f.write("# Bio\nAkhil builds high performance RAG pipelines.")

        self.pipeline = RAGPipeline(knowledge_dir=self.temp_dir)

    def test_ingest_and_query(self):
        self.pipeline.ingest_and_index()
        self.assertGreater(len(self.pipeline.documents), 0)
        self.assertGreater(len(self.pipeline.chunks), 0)

        results = self.pipeline.query("RAG pipelines", mode="hybrid", top_k=2)
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()
