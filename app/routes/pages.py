"""
Page routes APIRouter for Akhil's FastAPI Portfolio application.
"""

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Parse .env file natively if present
ENV_FILE = os.path.join(os.path.dirname(BASE_DIR), ".env")
if os.path.exists(ENV_FILE):
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

# SMTP Configuration from Environment Variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "sakhil2027@gmail.com")


def send_contact_email(name: str, email: str, subject: str, message: str):
    """Sends email notification using Python SMTP in background task."""
    print(f"[CONTACT FORM] From: {name} ({email}) | Subject: {subject} | Msg: {message}")

    if not SMTP_USER or not SMTP_PASSWORD:
        print(
            "[SMTP NOTE] SMTP_USER or SMTP_PASSWORD not set in environment. "
            "Set SMTP_USER and SMTP_PASSWORD environment variables to deliver emails directly to inbox."
        )
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = NOTIFICATION_EMAIL
        msg['Subject'] = f"🚀 Portfolio Contact: {subject or 'New Inquiry'} from {name}"

        body = (
            f"You received a new message from your portfolio contact form!\n\n"
            f"----------------------------------------\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject or 'N/A'}\n"
            f"----------------------------------------\n\n"
            f"Message:\n{message}\n\n"
            f"----------------------------------------\n"
            f"Reply directly to: {email}"
        )
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"[SMTP SUCCESS] Contact notification email delivered to {NOTIFICATION_EMAIL}")
    except Exception as e:
        print(f"[SMTP ERROR] Failed to send email: {e}")

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
async def download_resume(type: str = "aiml"):
    """Serves specialized PDF resume files (aiml or data-analyst)."""
    filename = "resume-data-analyst.pdf" if type == "data-analyst" else "resume-aiml.pdf"
    resume_path = os.path.join(STATIC_DIR, "resume", filename)

    if not os.path.exists(resume_path):
        fallback_path = os.path.join(STATIC_DIR, "resume", "resume.pdf")
        if os.path.exists(fallback_path):
            resume_path = fallback_path

    if not os.path.exists(resume_path):
        raise HTTPException(status_code=404, detail="Resume PDF not found")

    return FileResponse(resume_path, media_type="application/pdf", content_disposition_type="inline")


@pages_bp.post("/api/contact")
async def contact_submit(payload: ContactPayload, background_tasks: BackgroundTasks):
    """Handles contact form submission and dispatches background email notification."""
    if not payload.name.strip() or not payload.email.strip() or not payload.message.strip():
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "Please fill out all required fields (Name, Email, Message)."
        })

    background_tasks.add_task(
        send_contact_email,
        name=payload.name.strip(),
        email=payload.email.strip(),
        subject=payload.subject.strip() if payload.subject else "Portfolio Inquiry",
        message=payload.message.strip()
    )

    return JSONResponse(content={
        "success": True,
        "message": f"Thank you, {payload.name}! Your message has been sent directly to my inbox. I will get back to you shortly."
    })
