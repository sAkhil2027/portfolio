"""
Unit tests for TextCleaner and TextChunker modules.
"""

import unittest
from rag.models.document import Document
from rag.preprocessing.cleaner import TextCleaner
from rag.preprocessing.chunker import TextChunker
from knowledge.schemas import DocumentMetadata
class TestChunking(unittest.TestCase):

    def setUp(self):
        self.cleaner = TextCleaner(remove_markdown_syntax=True, lower_case=False)
        self.chunker = TextChunker(chunk_size=100, chunk_overlap=20)

    def test_cleaner(self):
        raw_text = "# Header Title\n\nThis is **bold** text with [link](http://example.com)."
        cleaned = self.cleaner.clean(raw_text)
        self.assertNotIn("# Header", cleaned)
        self.assertNotIn("**bold**", cleaned)
        self.assertIn("bold text", cleaned)

    def test_chunker(self):
        long_content = "Word " * 50
        doc = Document(
            doc_id="test_doc",
            content=long_content,
            metadata=DocumentMetadata(source="test.md", title="Test Doc")
        )
        chunks = self.chunker.chunk_document(doc)
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0].doc_id, "test_doc")
        self.assertIn("chunk_0", chunks[0].chunk_id)


if __name__ == "__main__":
    unittest.main()
