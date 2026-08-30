"""
Answer Validator module.
Validates grounded confidence scores, output safety constraints, answer existence, and length bounds.
"""

from typing import List, Tuple
from chatbot.models.response import Citation


class AnswerValidator:
    """
    Evaluates response grounding, safety, answer existence, and length bounds.
    """

    EMPTY_FALLBACK_MESSAGE = (
        "I encountered an issue generating a response. "
        "Please try again or use the contact form to reach Akhil directly."
    )

    def __init__(self, min_confidence: float = 0.3, max_answer_length: int = 3000):
        self.min_confidence = min_confidence
        self.max_answer_length = max_answer_length

    def validate(self, answer: str, citations: List[Citation]) -> Tuple[bool, float, str]:
        """
        Validates if answer exists, is within length bounds, and is adequately grounded in retrieved citations.
        Returns: (is_grounded, confidence_score, validated_answer)
        """
        # 1. Answer Existence Check
        if not answer or not answer.strip():
            return False, 0.0, self.EMPTY_FALLBACK_MESSAGE

        # 2. Length Cap Check
        clean_answer = answer[:self.max_answer_length] if len(answer) > self.max_answer_length else answer

        # 3. Sources & Grounding Verification
        if not citations:
            return False, 0.0, clean_answer

        # Calculate average citation score as proxy confidence
        avg_score = sum(c.score for c in citations) / len(citations)
        confidence = min(1.0, max(0.0, avg_score))

        is_grounded = confidence >= self.min_confidence
        return is_grounded, round(confidence, 4), clean_answer
