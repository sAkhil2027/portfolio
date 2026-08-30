"""
SSE Formatter module.
Formats tokens, sources/citations, related projects, and completion events into Server-Sent Events (SSE) standard strings.
"""

import json
from typing import List, Any, Dict, Optional
from chatbot.models.response import Citation, StreamChunk


class SSEFormatter:
    """
    Formats events and data chunks for HTTP Server-Sent Events (text/event-stream).
    """

    @staticmethod
    def format_event(event: str, data: Dict[str, Any]) -> str:
        """
        Formats a single SSE event line string.
        """
        json_data = json.dumps(data, ensure_ascii=False)
        return f"event: {event}\ndata: {json_data}\n\n"

    def format_token(self, token: str) -> str:
        """
        Formats a single text token event.
        """
        return self.format_event("token", {"token": token})

    def format_sources(self, sources: List[Citation], related_projects: List[str] = None, conversation_id: Optional[str] = None) -> str:
        """
        Formats source citations and related projects metadata event.
        """
        c_dicts = [c.model_dump() for c in sources]
        data = {
            "sources": c_dicts,
            "related_projects": related_projects or [],
        }
        if conversation_id:
            data["conversation_id"] = conversation_id
        return self.format_event("sources", data)

    # Alias method for backward compatibility
    def format_citations(self, citations: List[Citation], related_projects: List[str] = None, conversation_id: Optional[str] = None) -> str:
        return self.format_sources(citations, related_projects=related_projects, conversation_id=conversation_id)

    def format_done(self, confidence: float = 1.0, is_grounded: bool = True, conversation_id: Optional[str] = None) -> str:
        """
        Formats stream completion event.
        """
        data = {
            "status": "completed",
            "confidence": confidence,
            "is_grounded": is_grounded
        }
        if conversation_id:
            data["conversation_id"] = conversation_id
        return self.format_event("done", data)

    def format_error(self, message: str) -> str:
        """
        Formats error event.
        """
        return self.format_event("error", {"error": message})
