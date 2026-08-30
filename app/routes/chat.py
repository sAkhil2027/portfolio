"""
Chatbot API Routes APIRouter for FastAPI.
Provides POST /api/chat/stream (SSE) and POST /api/chat (JSON) endpoints with IP rate limiting.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from chatbot.models.request import ChatRequest
from chatbot.service import ChatbotService
from chatbot.safety.rate_limiter import RateLimiter
from chatbot.streaming.sse import SSEFormatter

chat_bp = APIRouter()

# In-memory IP rate limiter: 20 requests per minute per IP
rate_limiter = RateLimiter(max_requests=20, window_seconds=60)
sse_formatter = SSEFormatter()


def get_client_ip(request: Request) -> str:
    """
    Extracts client IP address, respecting X-Forwarded-For when behind reverse proxies.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "127.0.0.1"


@chat_bp.post("/api/chat/stream")
async def chat_stream_api(request: Request, payload: ChatRequest):
    """
    Server-Sent Events (SSE) Streaming endpoint for Chatbot.
    Returns real-time token stream and source citations.
    """
    client_ip = get_client_ip(request)
    allowed, retry_after = rate_limiter.is_allowed(client_ip)

    if not allowed:
        # Emit graceful SSE error informing client of rate limit
        async def rate_limit_stream():
            error_msg = f"Rate limit exceeded. Please wait {retry_after} seconds before asking another question."
            yield sse_formatter.format_error(error_msg)

        return StreamingResponse(
            rate_limit_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Retry-After": str(retry_after)
            }
        )

    pipeline = getattr(request.app.state, "rag_pipeline", None)
    service = ChatbotService(rag_pipeline=pipeline)

    return StreamingResponse(
        service.stream_chat(payload),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@chat_bp.post("/api/chat")
async def chat_json_api(request: Request, payload: ChatRequest):
    """
    Standard JSON endpoint for Chatbot queries.
    """
    client_ip = get_client_ip(request)
    allowed, retry_after = rate_limiter.is_allowed(client_ip)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Please wait {retry_after} seconds before asking another question.",
            headers={"Retry-After": str(retry_after)}
        )

    pipeline = getattr(request.app.state, "rag_pipeline", None)
    service = ChatbotService(rag_pipeline=pipeline)

    response = await service.chat(payload)
    return JSONResponse(content=response.model_dump())
