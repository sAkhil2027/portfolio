"""
Streamlined Qdrant Vector Database Search Retriever module.
Provides dense + sparse BM25 multi-vector indexing and native hybrid retrieval on Qdrant.
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from rag.models.document import DocumentChunk, SearchResult
from rag.embeddings.embedder import TextEmbedder
from rag.sparse.encoder import BM25SparseEncoder
from rag.retrieval.vector import VectorRetriever, matches_metadata_filter


class QdrantRetriever:
    """
    Production Qdrant Vector Search Engine with Dense + Sparse BM25 multi-vector indexing.
    """

    def __init__(self, collection_name: str = "portfolio_knowledge", embedder: TextEmbedder = None, location: Optional[str] = None):
        self.collection_name = collection_name
        self.embedder = embedder or TextEmbedder()
        self.sparse_encoder = BM25SparseEncoder()
        self.chunks: List[DocumentChunk] = []

        env_url = os.environ.get("QDRANT_URL", "").strip()
        env_key = os.environ.get("QDRANT_API_KEY", "").strip()

        self.location = location or (env_url if env_url else ":memory:")
        self.api_key = env_key or None

        self._qdrant_client = None
        self._is_qdrant_available = False
        self._fallback_retriever = None

        self._init_qdrant()

    def _init_qdrant(self):
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models

            if self.location.startswith(("http://", "https://")):
                self._qdrant_client = QdrantClient(url=self.location, api_key=self.api_key)
            elif self.location == ":memory:":
                self._qdrant_client = QdrantClient(location=":memory:")
            else:
                self._qdrant_client = QdrantClient(path=self.location)

            self._models = models
            self._is_qdrant_available = True
        except (ImportError, Exception) as e:
            print(f"[QdrantRetriever] Note: qdrant-client not loaded ({e}). Using native VectorRetriever fallback.")
            self._is_qdrant_available = False
            self._fallback_retriever = VectorRetriever(embedder=self.embedder)

    def _ensure_collection(self, vector_size: int = 384):
        if not self._is_qdrant_available:
            return

        try:
            collections = self._qdrant_client.get_collections().collections
            col_names = [c.name for c in collections]

            if self.collection_name not in col_names:
                self._qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config={
                        "dense": self._models.VectorParams(
                            size=vector_size,
                            distance=self._models.Distance.COSINE
                        )
                    },
                    sparse_vectors_config={
                        "bm25": self._models.SparseVectorParams()
                    }
                )
        except Exception as e:
            print(f"[QdrantRetriever] Warning creating collection: {e}")

    def index_chunks(self, chunks: List[DocumentChunk], batch_size: int = 100):
        """
        Embeds DocumentChunks and upserts dense and sparse BM25 vectors into Qdrant using deterministic UUIDs & batching.
        """
        self.chunks = chunks
        if not chunks:
            return

        if not self._is_qdrant_available:
            self._fallback_retriever.index_chunks(chunks)
            return

        texts = [c.text for c in chunks]
        dense_vectors = self.embedder.embed_batch(texts)
        if not dense_vectors:
            return

        vector_dim = len(dense_vectors[0])
        self._ensure_collection(vector_dim)

        points = []
        for chunk, d_vec in zip(chunks, dense_vectors):
            s_indices, s_values = self.sparse_encoder.encode_text(chunk.text)

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

            # Generate deterministic UUID v5 point ID from chunk.id
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.id))

            points.append(self._models.PointStruct(
                id=point_id,
                vector={
                    "dense": d_vec,
                    "bm25": self._models.SparseVector(indices=s_indices, values=s_values)
                },
                payload=payload
            ))

        # Batch upserts in groups of batch_size
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self._qdrant_client.upsert(
                collection_name=self.collection_name,
                points=batch
            )

    def _build_qdrant_filter(self, metadata_filter: Optional[Dict[str, Any]]):
        """
        Constructs Qdrant FieldCondition objects for string, integer, boolean, or list (MatchAny) payload attributes.
        """
        if not metadata_filter or not self._models:
            return None

        must_conditions = []
        for key, val in metadata_filter.items():
            if isinstance(val, (str, int, bool)):
                must_conditions.append(self._models.FieldCondition(
                    key=key,
                    match=self._models.MatchValue(value=val)
                ))
            elif isinstance(val, list):
                if hasattr(self._models, "MatchAny"):
                    must_conditions.append(self._models.FieldCondition(
                        key=key,
                        match=self._models.MatchAny(any=val)
                    ))
                else:
                    for item in val:
                        must_conditions.append(self._models.FieldCondition(
                            key=key,
                            match=self._models.MatchValue(value=item)
                        ))

        if must_conditions:
            return self._models.Filter(must=must_conditions)
        return None

    def search(self, query: str, top_k: int = 5, mode: str = "hybrid", metadata_filter: Optional[Dict[str, Any]] = None, min_score: float = 0.0) -> List[SearchResult]:
        """
        Searches Qdrant with optional payload metadata filtering and min_score thresholding.
        """
        if not self._is_qdrant_available:
            results = self._fallback_retriever.search(query, top_k=top_k, metadata_filter=metadata_filter)
            return [r for r in results if r.score >= min_score]

        q_dense = self.embedder.embed_text(query)
        s_indices, s_values = self.sparse_encoder.encode_text(query)

        query_filter = self._build_qdrant_filter(metadata_filter)

        try:
            search_hits = []
            # Use Qdrant Native Prefetch & Reciprocal Rank Fusion (RRF) for hybrid mode if query_points is supported
            if mode == "hybrid" and hasattr(self._qdrant_client, "query_points") and hasattr(self._models, "Prefetch"):
                try:
                    prefetch_list = [
                        self._models.Prefetch(
                            query=q_dense,
                            using="dense",
                            limit=top_k * 2
                        )
                    ]
                    if s_indices and s_values and hasattr(self._models, "SparseVector"):
                        prefetch_list.append(
                            self._models.Prefetch(
                                query=self._models.SparseVector(indices=s_indices, values=s_values),
                                using="bm25",
                                limit=top_k * 2
                            )
                        )

                    fusion_query = self._models.FusionQuery(fusion=self._models.Fusion.RRF) if hasattr(self._models, "FusionQuery") else None

                    res = self._qdrant_client.query_points(
                        collection_name=self.collection_name,
                        prefetch=prefetch_list,
                        query=fusion_query,
                        query_filter=query_filter,
                        limit=top_k
                    )
                    search_hits = getattr(res, "points", res)
                except Exception as ex:
                    # Standard vector search fallback if query_points parameters differ
                    search_hits = self._qdrant_client.search(
                        collection_name=self.collection_name,
                        query_vector=("dense", q_dense),
                        query_filter=query_filter,
                        limit=top_k
                    )
            else:
                vector_name = "bm25" if mode == "bm25" else "dense"
                query_vec = ("dense", q_dense)
                search_hits = self._qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vec,
                    query_filter=query_filter,
                    limit=top_k
                )

            results = []
            for hit in search_hits:
                score_val = float(hit.score)
                if min_score > 0.0 and score_val < min_score:
                    continue

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
                    score=score_val,
                    retrieval_method=f"qdrant_{mode}"
                ))

            return results
        except Exception as e:
            print(f"[QdrantRetriever] Search fallback due to: {e}")
            return self._fallback_retriever.search(query, top_k=top_k, metadata_filter=metadata_filter)


# Alias for backward compatibility
QdrantVectorRetriever = QdrantRetriever
