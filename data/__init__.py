"""
Data package initialization and helper utilities.
"""

from data.profile import PROFILE
from data.skills import SKILLS
from data.experience import EXPERIENCE
from data.education import EDUCATION, CERTIFICATIONS
from data.projects import PROJECTS


def get_profile():
    return PROFILE


def get_skills():
    return SKILLS


def get_experience():
    return EXPERIENCE


def get_education():
    return {
        "degrees": EDUCATION,
        "certifications": CERTIFICATIONS
    }


def get_projects(featured_only=False, category=None):
    projects = PROJECTS
    if featured_only:
        projects = [p for p in projects if p.get("featured")]
    if category:
        projects = [p for p in projects if p.get("category") == category]
    return projects


def get_project_by_id_or_slug(project_id):
    """Lookup project by integer ID or string slug."""
    project_id_str = str(project_id).strip()
    for project in PROJECTS:
        if str(project.get("id")) == project_id_str or project.get("slug") == project_id_str:
            return project
    return None
