"""
BM25 Sparse Vector Encoder module.
Encodes raw text into sparse term-frequency vector representations for Qdrant sparse indexing.
"""

import math
import re
from typing import List, Dict, Tuple


class BM25SparseEncoder:
    """
    Computes sparse term-frequency BM25 vector indices and weights for text inputs.
    """

    def __init__(self, vocab_size: int = 100000):
        self.vocab_size = vocab_size

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def encode_text(self, text: str) -> Tuple[List[int], List[float]]:
        """
        Encodes a single string into sparse (indices, values) float vectors.
        """
        tokens = self._tokenize(text)
        if not tokens:
            return [], []

        tf_map: Dict[int, float] = {}
        for token in tokens:
            idx = abs(hash(token)) % self.vocab_size
            tf_map[idx] = tf_map.get(idx, 0.0) + 1.0

        indices = list(tf_map.keys())
        values = [math.log(1.0 + freq) for freq in tf_map.values()]
        return indices, values

    def encode_batch(self, texts: List[str]) -> List[Tuple[List[int], List[float]]]:
        """
        Encodes a list of strings into sparse (indices, values) vectors.
        """
        return [self.encode_text(t) for t in texts]
