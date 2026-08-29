"""
Unit tests for metrics framework package.
"""

import unittest
from metrics.chunking_retrieval import RetrievalEvaluator
from metrics.embedding_eval import EmbeddingEvaluator
from metrics.llm_performance import LLMEvaluator
from rag.models.document import DocumentChunk, SearchResult


class TestMetrics(unittest.TestCase):

    def test_llm_faithfulness(self):
        evaluator = LLMEvaluator()
        chunk = DocumentChunk(
            id="c1",
            text="Akhil built a high performance RAG backend with FastAPI and Qdrant.",
            source="projects",
            source_type="project",
            category="project"
        )
        res = SearchResult(chunk=chunk, score=0.9, retrieval_method="hybrid")
        report = evaluator.evaluate_faithfulness("Akhil built RAG backend with FastAPI.", [res])
        self.assertTrue(report["is_grounded"])
        self.assertGreater(report["faithfulness_score"], 0.7)

    def test_embedding_eval(self):
        evaluator = EmbeddingEvaluator()
        sep = evaluator.evaluate_separation(
            ("FastAPI backend", "Python web service"),
            ("FastAPI backend", "Astronomy planet science")
        )
        self.assertIn("separation_margin", sep)


if __name__ == "__main__":
    unittest.main()
