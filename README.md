# Akhil's Data Science & AI/ML Portfolio (`sAkhil2027/portfolio`)

A modern, high-performance personal portfolio web application built with **Python (FastAPI)**, **Uvicorn**, **Jinja2 Templates**, decoupled data modules, and a custom **Dark Glassmorphism CSS Design System**.

---

## 📁 Project Architecture & File Directory

```text
portfolio/
│
├── app/
│   ├── __init__.py          # FastAPI application factory, StaticFiles mounting & exception handlers
│   ├── main.py              # Application entrypoint runner using Uvicorn
│   │
│   ├── routes/
│   │   ├── __init__.py      # Routes package initialization
│   │   └── pages.py         # APIRouter for portfolio pages, inline resume viewer, & SMTP contact endpoint
│   │
│   ├── templates/
│   │   ├── base.html        # Master Jinja2 layout, navbar, SEO metadata, footer
│   │   ├── index.html       # Landing page (Hero, Profile, Skills, Experience, Featured Work, Education, Contact)
│   │   ├── projects.html    # Dedicated Projects catalog gallery page (/projects)
│   │   └── project.html     # Deep-dive individual project detail page (/projects/{project_id})
│   │
│   └── static/
│       ├── css/
│       │   └── style.css    # Dark glassmorphism design system, responsive breakpoints, custom scrollbars
│       │
│       ├── images/
│       │   └── projects/    # High-impact project preview graphics
│       │
│       └── resume/
│           ├── resume-aiml.pdf          # Specialized AI / ML Resume
│           └── resume-data-analyst.pdf  # Specialized Data Analyst Resume
│
├── data/
│   ├── __init__.py          # Data package exports & helper getters (get_project_by_id_or_slug)
│   ├── projects.py          # Detailed project models (Problem, Solution, Contribution, Challenges, Tech, Metrics)
│   ├── skills.py            # Categorized 40+ Skills matrix with unique brand icons & custom color glows
│   ├── experience.py        # Vertical career timeline (Full-Time, Internships & Hackathons)
│   ├── education.py         # Academic degree & Industry Certifications with Google Drive links
│   └── profile.py           # Personal bio, taglines, social links, and metrics
│
├── .env.example             # Template for SMTP Gmail notification credentials
├── .gitignore               # Excludes secrets (.env), virtualenv, and build artifacts
├── requirements.txt         # Python dependencies (fastapi, uvicorn, jinja2, python-multipart)
└── README.md                # Comprehensive repository documentation
```

---

## ⚡ Features & Visual Highlights

- **FastAPI Engine**: Asynchronous route handlers delivering high-throughput performance with automatic OpenAPI documentation.
- **Dynamic Hero Section**: Interactive terminal mockup, live stats, and social links (GitHub, LinkedIn, Email).
- **Dual Specialized Resumes**: Instant in-browser PDF viewing for:
  - 🧠 **AI / ML CV** (`/resume?type=aiml`)
  - 📊 **Data Analyst CV** (`/resume?type=data-analyst`)
- **40+ Skills Matrix**: Unique brand icons (Python, SQL, RAG, MCP, LangChain, FAISS, Power BI, Streamlit, Docker, etc.) with custom neon progress glows.
- **Vertical Experience Timeline**: Grouped by Year (2026, 2025, 2024), covering Full-Time engineering roles, Research Internships, and National Hackathons.
- **Deep-Dive Project Detail Pages (`/projects/{project_id}`)**:
  - 🔴 **Problem Statement**
  - 💡 **Proposed Solution**
  - ⚙️ **My Contribution**
  - 🛡️ **Technical Challenges & Solutions**
  - 🏗️ **Architecture & System Design**
  - ✅ **Key Features**
  - 📊 **Key Performance Metrics Grid**
- **Scrollable Education & Certifications Block**: Compact, fixed-height cards with custom vertical scrollbars and direct Google Drive certificate links.
- **Background Gmail SMTP Contact Engine**: Form submissions asynchronously send email notifications directly to your Gmail inbox via `POST /api/contact` using BackgroundTasks.

---

## 🚀 Quick Start Guide

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/sAkhil2027/portfolio.git
cd portfolio

# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables (`.env`)
Create a `.env` file in the root directory:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_digit_gmail_app_password
NOTIFICATION_EMAIL=your_email@gmail.com
```

### 4. Run Application Locally
```bash
python -m app.main
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

- Interactive Swagger API Docs: **`http://127.0.0.1:5000/docs`**
- Redoc API Documentation: **`http://127.0.0.1:5000/redoc`**

---

## ⚙️ Customizing Content

All text, projects, skills, and career history are decoupled from HTML templates and stored in Python data modules:

- **Edit Profile & Bio**: Modify `data/profile.py`
- **Add / Remove Projects**: Update `data/projects.py`
- **Update Skills & Levels**: Edit `data/skills.py`
- **Update Work History**: Edit `data/experience.py`
- **Update Education & Certifications**: Edit `data/education.py`

---

## 📜 License
MIT License. Free to use and modify for personal portfolios.
