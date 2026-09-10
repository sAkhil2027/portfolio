"""
Text Embedder module for generating dense vector embeddings.
Supports Hugging Face Inference API, SentenceTransformers, and a lightweight deterministic fallback vectorizer.
"""

import os
import math
import re
from typing import List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class TextEmbedder:
    """
    Generates embedding vectors for text inputs.
    Supports Hugging Face Serverless Inference API (0MB RAM),
    SentenceTransformers, and deterministic fallback vectorizer.
    """

    def __init__(self, model_name: str = None, vector_dim: int = 384):
        self.model_name = model_name or os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.vector_dim = vector_dim
        self._st_model = None
        self._initialized = False

        # Hugging Face Inference API configuration
        self.hf_token = (
            os.environ.get("HF_TOKEN")
            or os.environ.get("HUGGING_FACE_HUB_TOKEN")
            or os.environ.get("HUGGINGFACE_API_KEY")
        )
        self.hf_endpoint = (
            f"https://router.huggingface.co/hf-inference/models/sentence-transformers/{self.model_name}/pipeline/feature-extraction"
        )

    def _init_model(self):
        if self._initialized:
            return

        # Default to lightweight API or deterministic vectorizer unless heavy embeddings are explicitly requested
        # Protects cloud free-tiers (Render 512MB RAM) against PyTorch OOM crashes
        enable_heavy = os.environ.get("ENABLE_HEAVY_EMBEDDINGS", "0").lower() in ("1", "true")
        use_lightweight = os.environ.get("USE_LIGHTWEIGHT_EMBEDDINGS", "1").lower() in ("1", "true")
        fast_eval = os.environ.get("FAST_EVAL_MODE", "0").lower() in ("1", "true")

        if not enable_heavy or use_lightweight or fast_eval:
            self._st_model = None
            self._initialized = True
            return

        try:
            from sentence_transformers import SentenceTransformer
            self._st_model = SentenceTransformer(self.model_name)
        except (ImportError, Exception) as e:
            print(f"[TextEmbedder] Note: SentenceTransformer bypassed ({e}). Using HF API / lightweight fallback.")
            self._st_model = None
        self._initialized = True

    def _embed_hf_api(self, text: str) -> Optional[List[float]]:
        """
        Embeds a single string using Hugging Face Serverless Inference API.
        Requires zero RAM on Render and avoids heavy PyTorch dependencies.
        """
        hf_token = (
            self.hf_token
            or os.environ.get("HF_TOKEN")
            or os.environ.get("HUGGING_FACE_HUB_TOKEN")
            or os.environ.get("HUGGINGFACE_API_KEY")
        )
        if not hf_token:
            return None

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {hf_token.strip()}"
        }
        payload = {"inputs": text}

        try:
            import httpx
            with httpx.Client(timeout=8.0) as client:
                resp = client.post(self.hf_endpoint, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        # Handle potential nested list response e.g. [[...]] or [...]
                        if data and isinstance(data[0], list):
                            return data[0]
                        return data
        except Exception as e:
            print(f"[TextEmbedder] HF API embedding warning: {e}")

        return None

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single string into a float vector.
        Priority:
        1. Hugging Face Serverless Inference API (if HF_TOKEN set - 0 MB RAM)
        2. Local SentenceTransformer (if enabled & installed)
        3. Deterministic lightweight feature hashing fallback (zero RAM)
        """
        self._init_model()

        # 1. Try Hugging Face Serverless Inference API
        hf_vec = self._embed_hf_api(text)
        if hf_vec and len(hf_vec) == self.vector_dim:
            return hf_vec

        # 2. Try local SentenceTransformer (if heavy mode explicitly enabled)
        if self._st_model is not None:
            vec = self._st_model.encode(text, convert_to_numpy=True)
            return vec.tolist()

        # 3. Fallback deterministic hashing vectorizer
        return self._fallback_embed(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of strings into a list of float vectors.
        """
        self._init_model()

        if self._st_model is not None:
            vecs = self._st_model.encode(texts, convert_to_numpy=True)
            return vecs.tolist()

        # Process each text through embed_text (HF API or fallback)
        return [self.embed_text(t) for t in texts]

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

