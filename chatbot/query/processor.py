"""
Query Processor module.
Normalizes incoming chat queries, infers metadata filters, and performs zero-latency follow-up query rewriting.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from chatbot.models.request import ChatMessage


class QueryProcessor:
    """
    Sanitizes user input, extracts intent/filters, and rewrites contextual follow-up questions.
    """

    PROJECT_KEYWORDS = {
        "rag": "rag-pipeline",
        "vector": "qdrant-search",
        "fastapi": "portfolio-website",
        "portfolio": "portfolio-website",
        "nlp": "medical-ner",
        "ner": "medical-ner",
        "fraud": "fraud-detection",
        "credit": "fraud-detection",
        "vision": "traffic-vision",
        "yolo": "traffic-vision",
    }

    SOURCE_TYPE_PATTERNS = {
        r"\b(project|projects|work|built|github|code)\b": "project",
        r"\b(experience|work history|job|role|company|internship|career)\b": "experience",
        r"\b(education|degree|gpa|university|college|certification|course)\b": "education",
        r"\b(skill|skills|python|pytorch|sql|docker|fastapi|rag)\b": "skill",
    }

    PRONOUN_PATTERNS = r"\b(it|that|this|the project|that project|his role|their work)\b"

    def process(self, query: str, history: Optional[List[ChatMessage]] = None, user_filters: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Cleans query string, rewrites contextual follow-up pronouns if present in history, and infers metadata filters.
        """
        cleaned_query = query.strip()
        cleaned_query = re.sub(r"\s+", " ", cleaned_query)

        # Handle contextual follow-up rewriting if history is present
        if history and re.search(self.PRONOUN_PATTERNS, cleaned_query, re.IGNORECASE):
            last_subject = self._extract_last_subject(history)
            if last_subject:
                cleaned_query = self._rewrite_followup_query(cleaned_query, last_subject)

        filters = dict(user_filters or {})

        # Infer source_type if missing
        if "source_type" not in filters:
            q_lower = cleaned_query.lower()
            for pattern, stype in self.SOURCE_TYPE_PATTERNS.items():
                if re.search(pattern, q_lower):
                    filters["source_type"] = stype
                    break

        return cleaned_query, filters

    def _extract_last_subject(self, history: List[ChatMessage]) -> Optional[str]:
        """
        Scans recent user messages in history to identify the primary subject noun/project phrase.
        """
        # Look at the last user message in history
        user_msgs = [m for m in history if getattr(m, "role", None) == "user" or (isinstance(m, dict) and m.get("role") == "user")]
        if not user_msgs:
            return None

        last_user_text = user_msgs[-1].content if hasattr(user_msgs[-1], "content") else user_msgs[-1].get("content", "")
        if not last_user_text:
            return None

        # 1. Try matching explicit project names or phrases
        match = re.search(r"(\b[\w\s\-']+(?:project|application|system|chatbot|model|experience|role|skills?)\b)", last_user_text, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            # Clean leading fluff words
            subject = re.sub(r"^(tell me about|what is|how did|about|akhil's|akhil)\s+", "", subject, flags=re.IGNORECASE).strip()
            if subject:
                return subject

        # 2. Fallback: extract last 3-4 words of previous turn
        words = last_user_text.strip().split()
        if len(words) >= 2:
            return " ".join(words[-3:])

        return None

    def _rewrite_followup_query(self, query: str, last_subject: str) -> str:
        """
        Replaces referential pronouns with the extracted last subject phrase.
        """
        # Replace 'it', 'that', 'this project' with subject
        if re.search(r"\b(it|that|this project|the project)\b", query, re.IGNORECASE):
            rewritten = re.sub(r"\b(it|that|this project|the project)\b", f"Akhil's {last_subject}", query, count=1, flags=re.IGNORECASE)
            return rewritten

        # Fallback: append subject context to query
        return f"{query} (referring to {last_subject})"
