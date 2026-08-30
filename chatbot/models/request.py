"""
Pydantic Request Models for Phase 4 Chatbot.
Supports dual-key payloads ('message' or 'query') and tight portfolio bounds.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator


class ChatMessage(BaseModel):
    """
    Single message turn in conversation history.
    """
    role: str = Field(..., description="Role of speaker: 'user', 'assistant', or 'system'")
    content: str = Field(..., min_length=1, max_length=2000, description="Message text content")


class ChatRequest(BaseModel):
    """
    API payload for chat completion and streaming requests.
    Supports both 'message' and 'query' JSON keys seamlessly.
    """
    query: Optional[str] = Field(None, min_length=1, max_length=500, description="Current user query text")
    message: Optional[str] = Field(None, min_length=1, max_length=500, description="Alias for user query text")
    
    conversation_id: Optional[str] = Field(None, max_length=50, description="Optional session or conversation ID")
    history: List[ChatMessage] = Field(default_factory=list, max_length=10, description="Prior conversation messages (max 10 turns)")
    top_k: int = Field(5, ge=1, le=10, description="Number of retrieved knowledge chunks [1 to 10]")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata payload filters (e.g. source_type, category)")
    stream: bool = Field(True, description="Whether to stream response via SSE")

    @model_validator(mode="before")
    @classmethod
    def resolve_message_alias(cls, data: Any) -> Any:
        """
        Maps incoming 'message' key to 'query' if 'query' is not explicitly provided.
        """
        if isinstance(data, dict):
            msg_val = data.get("message")
            query_val = data.get("query")
            
            if msg_val and not query_val:
                data["query"] = msg_val
            elif not query_val and not msg_val:
                raise ValueError("Either 'message' or 'query' must be provided and non-empty.")
        return data
