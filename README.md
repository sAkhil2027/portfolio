# Akhil's Data Science & AI/ML Portfolio (`akhil-portfolio`)

A modern, high-performance personal portfolio web application built with **Python (FastAPI)**, **Uvicorn**, **Jinja2 Templates**, dynamic data stores, and a custom **Glassmorphism CSS design system**.

---

## 📁 Project Architecture & File Directory

```
akhil-portfolio/
│
├── app/
│   ├── __init__.py          # FastAPI application factory, StaticFiles mounting & exception handlers
│   ├── main.py              # Application entrypoint runner using Uvicorn
│   │
│   ├── routes/
│   │   ├── __init__.py      # Routes package initialization
│   │   └── pages.py         # APIRouter for portfolio pages & contact submission endpoint
│   │
│   ├── templates/
│   │   ├── base.html        # Master layout, navbar, SEO tags, footer
│   │   ├── index.html       # Landing page (Hero, Profile, Skills, Experience, Projects, Contact)
│   │   └── project.html     # Dedicated project detail view
│   │
│   └── static/
│       ├── css/
│       │   └── style.css    # Dark glassmorphism CSS design system & micro-animations
│       │
│       ├── images/
│       │   └── projects/    # High-impact project preview graphics
│       │
│       └── resume/
│           └── resume.pdf   # Downloadable PDF resume
│
├── data/
│   ├── __init__.py          # Data package exports & helper getters
│   ├── projects.py          # Detailed project list, tech stacks, metrics
│   ├── skills.py            # Categorized skills matrix & proficiencies
│   ├── experience.py        # Professional career history timeline
│   ├── education.py         # Academic degree & certifications
│   └── profile.py           # Personal bio, taglines, social links
│
├── requirements.txt         # Python dependencies (fastapi, uvicorn, jinja2, etc.)
└── README.md                # Project setup and usage documentation
```

---

## ⚡ Features & Visual Highlights

- **FastAPI Engine**: Asynchronous route handlers delivering high-throughput performance with automatic OpenAPI documentation.
- **Dynamic Hero Section**: Real-time typing animation, availability status pill, and interactive model training terminal mockup.
- **Data Science Skills Matrix**: Interactive filterable tabs for Machine Learning, Data Analytics & Statistics, BI & Visualization, and AI / MLOps.
- **Interactive Experience Timeline**: Career history entries highlighting ML models deployed, data pipelines built, and ROI metrics.
- **Project Showcase & Detail Routing**: Filterable projects grid with detailed detail views (`/project/<slug>`), performance metrics, and live demo / GitHub repo links.
- **Downloadable Resume**: Direct serving of `resume.pdf` at `/resume`.
- **AJAX Contact Form**: Instant feedback toast notifications without page reloads.

---

## 🚀 Quick Start Guide

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/akhil-data/akhil-portfolio.git
cd akhil-portfolio

# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application Locally
```bash
python -m app.main
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

- Interactive Swagger API Docs: **`http://127.0.0.1:5000/docs`**
- Redoc API Documentation: **`http://127.0.0.1:5000/redoc`**

---

## ⚙️ Customizing Content

All text, projects, skills, and career history are decoupled from HTML templates and stored in python files under the `data/` folder:

- **Edit Profile & Bio**: Modify `data/profile.py`
- **Add / Remove Projects**: Update `data/projects.py`
- **Update Skills & Levels**: Edit `data/skills.py`
- **Update Work History**: Edit `data/experience.py`
- **Update Education & Certifications**: Edit `data/education.py`

---

## 📌 Repository Commit Architecture

The codebase is organized into 5 modular commits:
1. `Part 1/5`: Core data models (`data/`), skill matrix, and dependencies (`requirements.txt`).
2. `Part 2/5`: Glassmorphism design system (`style.css`), generated resume PDF, and project graphics.
3. `Part 3/5`: Jinja2 templates (`base.html`, `index.html`, `projects.html`, `project.html`).
4. `Part 4/5`: FastAPI application factory, Uvicorn runner, and APIRouter page routes.
5. `Part 5/5`: Documentation and deployment configuration.

---

## 📜 License
MIT License. Free to use and modify for personal portfolios.
