"""
FastAPI application factory module.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import os

from app.routes.pages import pages_bp, TEMPLATES_DIR, STATIC_DIR
from data import get_profile

templates = Jinja2Templates(directory=TEMPLATES_DIR)


def create_app() -> FastAPI:
    """Initializes and configures the FastAPI application."""
    app = FastAPI(
        title="Akhil - Data Scientist & AI/ML Portfolio",
        description="Personal Portfolio API and Web Application built with FastAPI",
        version="1.0.0"
    )

    # Mount static files directory at /static
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # Include routes APIRouter
    app.include_router(pages_bp)

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
