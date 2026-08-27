"""
Page routes APIRouter for Akhil's FastAPI Portfolio application.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

from data import (
    get_profile,
    get_skills,
    get_experience,
    get_education,
    get_projects,
    get_project_by_id_or_slug
)

pages_bp = APIRouter()

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


class ContactPayload(BaseModel):
    name: str
    email: str
    subject: str = ""
    message: str


@pages_bp.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    """GET / - Renders main portfolio landing page."""
    profile = get_profile()
    skills = get_skills()
    experience = get_experience()
    education = get_education()
    projects = get_projects()
    featured_projects = get_projects(featured_only=True)
    categories = sorted(list(set(p["category"] for p in projects)))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": profile,
            "skills": skills,
            "experience": experience,
            "education": education,
            "projects": projects,
            "featured_projects": featured_projects,
            "categories": categories
        }
    )


@pages_bp.get("/projects", response_class=HTMLResponse, name="projects_list")
async def projects_list(request: Request, category: str = None):
    """GET /projects - Renders dedicated Projects catalog page."""
    profile = get_profile()
    projects = get_projects(category=category)
    all_projects = get_projects()
    categories = sorted(list(set(p["category"] for p in all_projects)))

    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            "profile": profile,
            "projects": projects,
            "categories": categories,
            "selected_category": category
        }
    )


@pages_bp.get("/projects/{project_id}", response_class=HTMLResponse, name="project_detail")
async def project_detail(request: Request, project_id: str):
    """GET /projects/{project_id} - Renders detailed view for a specific project by ID or Slug."""
    project = get_project_by_id_or_slug(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    profile = get_profile()
    all_projects = get_projects()
    current_index = next((i for i, p in enumerate(all_projects) if str(p["id"]) == str(project["id"]) or p["slug"] == project["slug"]), 0)
    prev_project = all_projects[current_index - 1] if current_index > 0 else all_projects[-1]
    next_project = all_projects[current_index + 1] if current_index < len(all_projects) - 1 else all_projects[0]

    return templates.TemplateResponse(
        request=request,
        name="project.html",
        context={
            "project": project,
            "profile": profile,
            "prev_project": prev_project,
            "next_project": next_project
        }
    )


@pages_bp.get("/resume", name="download_resume")
async def download_resume():
    """Serves the PDF resume file."""
    resume_path = os.path.join(STATIC_DIR, "resume", "resume.pdf")
    if not os.path.exists(resume_path):
        raise HTTPException(status_code=404, detail="Resume PDF not found")
    return FileResponse(resume_path, media_type="application/pdf", filename="resume.pdf")


@pages_bp.post("/api/contact")
async def contact_submit(payload: ContactPayload):
    """Handles contact form submission."""
    if not payload.name.strip() or not payload.email.strip() or not payload.message.strip():
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "Please fill out all required fields (Name, Email, Message)."
        })

    print(f"[CONTACT FORM] From: {payload.name} ({payload.email}) | Subject: {payload.subject} | Msg: {payload.message}")

    return JSONResponse(content={
        "success": True,
        "message": f"Thank you, {payload.name}! Your message has been received. I will get back to you shortly."
    })
