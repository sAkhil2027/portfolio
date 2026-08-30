"""
FastAPI application factory module.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import os

from app.routes.pages import pages_bp, TEMPLATES_DIR, STATIC_DIR
from app.routes.chat import chat_bp
from data import get_profile
from rag.pipeline import RAGPipeline

templates = Jinja2Templates(directory=TEMPLATES_DIR)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
BM25_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "bm25_index.pkl")
VECTOR_INDEX_PATH = os.path.join(KNOWLEDGE_DIR, "vector_index.json")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan Context Manager: Pre-loads RAG Pipeline and Vector Index ONCE on server startup."""
    print("[FastAPI Lifespan] Initializing and pre-loading RAG Pipeline into app.state...")
    pipeline = RAGPipeline(knowledge_dir=KNOWLEDGE_DIR)
    
    # Fast evaluation embedder fallback check
    if os.environ.get("FAST_EVAL_MODE") == "1":
        pipeline.embedder._initialized = True
        pipeline.embedder._st_model = None

    if os.path.exists(BM25_INDEX_PATH) and os.path.exists(VECTOR_INDEX_PATH):
        print(f"[FastAPI Lifespan] Loading pre-built indices from {KNOWLEDGE_DIR}...")
        pipeline.load_indices(BM25_INDEX_PATH, VECTOR_INDEX_PATH)
    else:
        print(f"[FastAPI Lifespan] Indices not found. Building RAG indices on startup...")
        pipeline.ingest_and_index()

    app.state.rag_pipeline = pipeline
    print(f"[FastAPI Lifespan] RAG Pipeline successfully pre-loaded. Ready for sub-30ms search queries!")
    yield


def create_app() -> FastAPI:
    """Initializes and configures the FastAPI application."""
    app = FastAPI(
        title="Akhil - Data Scientist & AI/ML Portfolio",
        description="Personal Portfolio API and Web Application built with FastAPI",
        version="1.0.0",
        lifespan=lifespan
    )

    # Mount static files directory at /static
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # Include routes APIRouter
    app.include_router(pages_bp)
    app.include_router(chat_bp)

    # Custom 404 Exception Handler
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return templates.TemplateResponse(
                request=request,
                name="base.html",
                context={
                    "profile": get_profile(),
                    "title": "Page Not Found",
                    "content_404": True
                },
                status_code=404
            )
        return templates.TemplateResponse(
            request=request,
            name="base.html",
            context={
                "profile": get_profile(),
                "title": f"Error {exc.status_code}",
                "content_500": True
            },
            status_code=exc.status_code
        )

    # Custom 500 Exception Handler
    @app.exception_handler(Exception)
    async def custom_general_exception_handler(request: Request, exc: Exception):
        return templates.TemplateResponse(
            request=request,
            name="base.html",
            context={
                "profile": get_profile(),
                "title": "Server Error",
                "content_500": True
            },
            status_code=500
        )

    return app
