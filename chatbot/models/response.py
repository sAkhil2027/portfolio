"""
Pydantic Response Models for Phase 4 Chatbot.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """
    Source citation metadata object for grounded answers.
    """
    citation_id: int = Field(..., description="1-indexed citation number matching prompt anchors")
    chunk_id: str = Field(..., description="Unique document chunk ID")
    title: str = Field(..., description="Title of document or project")
    source: str = Field(..., description="File path or source document identifier")
    section: Optional[str] = Field("General", description="Document section or header name")
    source_type: str = Field("general", description="Source category (e.g. project, experience, education)")
    url: Optional[str] = Field(None, description="In-app deep link URL to project or section")
    score: float = Field(0.0, description="Retrieval similarity/RRF score")


class ChatResponse(BaseModel):
    """
    Complete JSON response object for non-streaming queries.
    """
    answer: str = Field(..., description="Synthesized grounded answer")
    sources: List[Citation] = Field(default_factory=list, description="Extracted source citations")
    related_projects: List[str] = Field(default_factory=list, description="List of related project IDs referenced in answer")
    conversation_id: Optional[str] = Field(None, description="Echoed session or conversation ID")
    confidence_score: float = Field(1.0, description="Grounded confidence metric [0.0 to 1.0]")
    is_grounded: bool = Field(True, description="Whether answer is backed by retrieved knowledge")

    @property
    def citations(self) -> List[Citation]:
        """Backward compatibility property alias for sources."""
        return self.sources


class StreamChunk(BaseModel):
    """
    Single Server-Sent Event (SSE) payload chunk.
    """
    event: str = Field(..., description="Event type: 'token', 'sources', 'done', 'error'")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload dictionary")
