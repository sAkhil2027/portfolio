"""
Embedding Model Evaluation Metrics Module.
Evaluates embedding latency, vector norm consistency, and distance separation.
"""

import math
import time
from typing import List, Dict, Any, Tuple
from rag.embeddings.embedder import TextEmbedder


def cosine_sim(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot / (norm1 * norm2)


class EmbeddingEvaluator:
    """
    Evaluator for dense vector embedding quality and throughput.
    """

    def __init__(self, embedder: TextEmbedder = None):
        self.embedder = embedder or TextEmbedder()

    def evaluate_throughput(self, sample_texts: List[str] = None) -> Dict[str, Any]:
        """
        Measures batch embedding throughput and average latency per text.
        """
        texts = sample_texts or [
            "FastAPI high performance RAG backend application.",
            "Deep Learning model fine-tuning with PyTorch and Transformers.",
            "Qdrant vector similarity search index for portfolio assistant.",
            "Smart India Hackathon national finalist AI developer."
        ]

        t0 = time.perf_counter()
        embeddings = self.embedder.embed_batch(texts)
        t1 = time.perf_counter()

        total_time_ms = (t1 - t0) * 1000.0
        avg_latency_ms = total_time_ms / len(texts) if texts else 0.0
        vector_dim = len(embeddings[0]) if embeddings else 0

        # Check L2 norms
        norms = [math.sqrt(sum(v * v for v in vec)) for vec in embeddings]
        avg_norm = sum(norms) / len(norms) if norms else 0.0

        return {
            "num_samples": len(texts),
            "total_time_ms": total_time_ms,
            "avg_latency_ms": avg_latency_ms,
            "vector_dimension": vector_dim,
            "avg_vector_l2_norm": avg_norm,
            "is_normalized": abs(avg_norm - 1.0) < 0.05
        }

    def evaluate_separation(self, positive_pair: Tuple[str, str], negative_pair: Tuple[str, str]) -> Dict[str, Any]:
        """
        Evaluates cosine similarity separation between related vs unrelated text pairs.
        """
        pos_vec1 = self.embedder.embed_text(positive_pair[0])
        pos_vec2 = self.embedder.embed_text(positive_pair[1])
        pos_sim = cosine_sim(pos_vec1, pos_vec2)

        neg_vec1 = self.embedder.embed_text(negative_pair[0])
        neg_vec2 = self.embedder.embed_text(negative_pair[1])
        neg_sim = cosine_sim(neg_vec1, neg_vec2)

        separation_margin = pos_sim - neg_sim

        return {
            "positive_pair": positive_pair,
            "positive_similarity": pos_sim,
            "negative_pair": negative_pair,
            "negative_similarity": neg_sim,
            "separation_margin": separation_margin,
            "has_good_separation": separation_margin > 0.15
        }
