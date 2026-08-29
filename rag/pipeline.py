"""
RAG Master Pipeline module.
Orchestrates document loading, cleaning, chunking, embedding, indexing, hybrid retrieval, and reranking.
"""

import os
from typing import List, Optional, Dict, Any
from rag.loaders.json_loader import JSONLoader
from rag.loaders.markdown_loader import MarkdownLoader
from rag.preprocessing.cleaner import TextCleaner
from rag.preprocessing.chunker import TextChunker
from rag.embeddings.embedder import TextEmbedder
from rag.retrieval.bm25 import BM25Retriever
from rag.retrieval.vector import VectorRetriever
from rag.retrieval.qdrant import QdrantRetriever
from rag.retrieval.hybrid import HybridRetriever
from rag.retrieval.reranker import Reranker
from rag.models.document import Document, DocumentChunk, Chunk, SearchResult


class RAGPipeline:
    """
    Master pipeline orchestrating RAG workflows for Akhil Portfolio.
    """

    def __init__(self, knowledge_dir: str, use_qdrant: bool = False):
        self.knowledge_dir = knowledge_dir
        self.structured_dir = os.path.join(knowledge_dir, "structured")
        self.documents_dir = os.path.join(knowledge_dir, "documents")
        self.use_qdrant = use_qdrant

        self.cleaner = TextCleaner()
        self.chunker = TextChunker(chunk_size=500, chunk_overlap=50)
        self.embedder = TextEmbedder()

        self.bm25_retriever = BM25Retriever()
        if use_qdrant:
            self.vector_retriever = QdrantRetriever(embedder=self.embedder)
        else:
            self.vector_retriever = VectorRetriever(embedder=self.embedder)

        self.hybrid_retriever = HybridRetriever(self.bm25_retriever, self.vector_retriever)
        self.reranker = Reranker()

        self.documents: List[Document] = []
        self.chunks: List[DocumentChunk] = []


    def ingest_and_index(self):
        """
        Ingests structured JSON and markdown documents, chunks text, and indexes in BM25 & Vector retrievers.
        """
        json_loader = JSONLoader(self.structured_dir)
        markdown_loader = MarkdownLoader(self.documents_dir)

        docs = []
        docs.extend(json_loader.load_documents())
        docs.extend(markdown_loader.load_documents())
        self.documents = docs

        # Clean document contents
        for d in self.documents:
            d.content = self.cleaner.clean(d.content)

        # Chunk documents
        self.chunks = self.chunker.chunk_documents(self.documents)

        # Index chunks
        self.bm25_retriever.index_chunks(self.chunks)
        self.vector_retriever.index_chunks(self.chunks)

        print(f"[RAGPipeline] Successfully ingested {len(self.documents)} documents, generated {len(self.chunks)} chunks, and indexed BM25 & Vector retrievers.")

    def query(self, query_text: str, mode: str = "hybrid", top_k: int = 5, rerank: bool = True, metadata_filter: Optional[Dict[str, Any]] = None, min_score: float = 0.0) -> List[SearchResult]:
        """
        Queries the indexed RAG pipeline with optional metadata filtering and score thresholding.
        mode: 'bm25', 'vector', or 'hybrid'
        """
        if mode == "bm25":
            results = self.bm25_retriever.search(query_text, top_k=top_k, metadata_filter=metadata_filter)
        elif mode == "vector":
            results = self.vector_retriever.search(query_text, top_k=top_k, metadata_filter=metadata_filter)
        else:
            results = self.hybrid_retriever.search(query_text, top_k=top_k, metadata_filter=metadata_filter)

        if min_score > 0.0:
            results = [r for r in results if r.score >= min_score]

        if rerank:
            results = self.reranker.rerank(query_text, results, top_k=top_k)

        return results

    def save_indices(self, bm25_path: str, vector_path: str):
        """
        Saves BM25 and Vector indices to disk.
        """
        self.bm25_retriever.save(bm25_path)
        self.vector_retriever.save(vector_path)

    def load_indices(self, bm25_path: str, vector_path: str):
        """
        Loads BM25 and Vector indices from disk.
        """
        if os.path.exists(bm25_path):
            self.bm25_retriever.load(bm25_path)
        if os.path.exists(vector_path):
            self.vector_retriever.load(vector_path)
        self.chunks = self.vector_retriever.chunks
