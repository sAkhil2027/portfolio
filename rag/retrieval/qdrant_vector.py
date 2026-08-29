"""
Qdrant Vector Database Search Retriever module.
Provides production-grade vector indexing, payload storage, and similarity search using Qdrant.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from rag.models.document import DocumentChunk, SearchResult
from rag.embeddings.embedder import TextEmbedder
from rag.retrieval.vector import VectorRetriever, matches_metadata_filter


class QdrantVectorRetriever:
    """
    Qdrant Vector Database Search Index.
    Supports Qdrant in-memory, local disk, or cloud instances with metadata payload filtering.
    """

    def __init__(self, collection_name: str = "portfolio_knowledge", embedder: TextEmbedder = None, location: str = None):
        self.collection_name = collection_name
        self.embedder = embedder or TextEmbedder()
        self.location = location or os.environ.get("QDRANT_URL") or ":memory:"
        self.api_key = os.environ.get("QDRANT_API_KEY")
        self.chunks: List[DocumentChunk] = []
        self._qdrant_client = None
        self._is_qdrant_available = False
        self._fallback_retriever = None

        self._init_qdrant()

    def _init_qdrant(self):
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models

            if self.location and self.location.startswith(("http://", "https://")):
                self._qdrant_client = QdrantClient(url=self.location, api_key=self.api_key)
            else:
                self._qdrant_client = QdrantClient(location=self.location)

            self._models = models
            self._is_qdrant_available = True
        except (ImportError, Exception) as e:
            print(f"[QdrantVectorRetriever] Note: qdrant-client not loaded ({e}). Using native VectorRetriever fallback.")
            self._is_qdrant_available = False
            self._fallback_retriever = VectorRetriever(embedder=self.embedder)

    def _ensure_collection(self, vector_size: int):
        if not self._is_qdrant_available:
            return

        try:
            collections = self._qdrant_client.get_collections().collections
            col_names = [c.name for c in collections]

            if self.collection_name not in col_names:
                self._qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self._models.VectorParams(
                        size=vector_size,
                        distance=self._models.Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"[QdrantVectorRetriever] Warning creating collection: {e}")

    def index_chunks(self, chunks: List[DocumentChunk]):
        """
        Embeds DocumentChunks and indexes vectors & metadata payloads into Qdrant.
        """
        self.chunks = chunks
        if not chunks:
            return

        if not self._is_qdrant_available:
            self._fallback_retriever.index_chunks(chunks)
            return

        texts = [c.text for c in chunks]
        vectors = self.embedder.embed_batch(texts)
        if not vectors:
            return

        vector_dim = len(vectors[0])
        self._ensure_collection(vector_dim)

        points = []
        for idx, (chunk, vec) in enumerate(zip(chunks, vectors)):
            payload = {
                "chunk_id": chunk.id,
                "text": chunk.text,
                "source": chunk.source,
                "source_type": chunk.source_type,
                "category": chunk.category,
                "project_id": chunk.project_id,
                "experience_id": chunk.experience_id,
                "education_id": chunk.education_id,
                "entity_id": chunk.entity_id,
                "metadata": chunk.metadata,
                "technologies": chunk.technologies,
                "section": chunk.section
            }
            # Add point
            points.append(self._models.PointStruct(
                id=idx,
                vector=vec,
                payload=payload
            ))

        self._qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query: str, top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """
        Searches Qdrant vector index using query embedding and optional Qdrant payload filters.
        """
        if not self._is_qdrant_available:
            return self._fallback_retriever.search(query, top_k=top_k, metadata_filter=metadata_filter)

        q_vec = self.embedder.embed_text(query)

        # Build Qdrant filter condition
        query_filter = None
        if metadata_filter:
            must_conditions = []
            for key, val in metadata_filter.items():
                if isinstance(val, str):
                    must_conditions.append(self._models.FieldCondition(
                        key=key,
                        match=self._models.MatchValue(value=val)
                    ))
            if must_conditions:
                query_filter = self._models.Filter(must=must_conditions)

        try:
            search_hits = self._qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=q_vec,
                query_filter=query_filter,
                limit=top_k
            )

            results = []
            for hit in search_hits:
                payload = hit.payload or {}
                chunk = DocumentChunk(
                    id=payload.get("chunk_id", str(hit.id)),
                    text=payload.get("text", ""),
                    source=payload.get("source", "unknown"),
                    source_type=payload.get("source_type", "general"),
                    category=payload.get("category", "general"),
                    project_id=payload.get("project_id"),
                    experience_id=payload.get("experience_id"),
                    education_id=payload.get("education_id"),
                    entity_id=payload.get("entity_id"),
                    metadata=payload.get("metadata", {})
                )
                results.append(SearchResult(
                    chunk=chunk,
                    score=float(hit.score),
                    retrieval_method="qdrant_vector"
                ))

            return results
        except Exception as e:
            print(f"[QdrantVectorRetriever] Search fallback due to: {e}")
            return self._fallback_retriever.search(query, top_k=top_k, metadata_filter=metadata_filter)
