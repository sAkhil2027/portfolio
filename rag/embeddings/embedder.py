"""
Text Embedder module for generating dense vector embeddings.
Supports SentenceTransformers with a lightweight fallback vectorizer.
"""

import os
import math
import re
from typing import List


class TextEmbedder:
    """
    Generates embedding vectors for text inputs.
    """

    def __init__(self, model_name: str = None, vector_dim: int = 384):
        self.model_name = model_name or os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.vector_dim = vector_dim
        self._st_model = None
        self._initialized = False

    def _init_model(self):
        if self._initialized:
            return
        try:
            from sentence_transformers import SentenceTransformer
            self._st_model = SentenceTransformer(self.model_name)
        except ImportError:
            self._st_model = None
        self._initialized = True

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single string into a float vector.
        """
        self._init_model()
        if self._st_model is not None:
            vec = self._st_model.encode(text, convert_to_numpy=True)
            return vec.tolist()

        # Fallback hashing vectorizer
        return self._fallback_embed(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of strings into a list of float vectors.
        """
        self._init_model()
        if self._st_model is not None:
            vecs = self._st_model.encode(texts, convert_to_numpy=True)
            return vecs.tolist()

        return [self._fallback_embed(t) for t in texts]

    def _fallback_embed(self, text: str) -> List[float]:
        """
        Lightweight deterministic feature-hashing vectorizer fallback.
        """
        tokens = re.findall(r"\w+", text.lower())
        vec = [0.0] * self.vector_dim
        if not tokens:
            return vec

        for token in tokens:
            idx = abs(hash(token)) % self.vector_dim
            vec[idx] += 1.0

        # L2 Normalize
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]

        return vec
