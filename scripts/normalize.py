"""
Data Normalization & Export Script for Akhil Portfolio.
Reads data modules from data/, validates them with Pydantic schemas,
and exports normalized JSON files to knowledge/structured/.
"""

import json
import os
import sys

# Ensure root workspace is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.profile import PROFILE
from data.projects import PROJECTS
from data.experience import EXPERIENCE
from data.skills import SKILLS
from data.education import EDUCATION, CERTIFICATIONS
from knowledge.schemas import (
    ProfileSchema,
    ProjectSchema,
    ExperienceSchema,
    SkillCategorySchema,
    EducationSchema,
    CertificationSchema,
    AchievementSchema,
)

ACHIEVEMENTS = [
    {
        "id": 1,
        "title": "Smart India Hackathon (SIH) National Finalist Selection",
        "organization": "IIIT Bhagalpur / Ministry of Education",
        "year": "2025 & 2026",
        "description": "Selected twice by IIIT Bhagalpur to represent the institute at the Smart India Hackathon national competition."
    },
    {
        "id": 2,
        "title": "National Data Science & AI Hackathon Winner",
        "organization": "National Data Science Competition",
        "year": "2025",
        "description": "Secured 1st place among 120+ participant teams for building an end-to-end automated ML & time-series forecasting pipeline."
    },
    {
        "id": 3,
        "title": "Top 10 Rank - Intra-College Hackathon",
        "organization": "IIIT Bhagalpur",
        "year": "2025",
        "description": "Secured Top 10 position out of 500+ participants in an intensive competitive hackathon."
    },
    {
        "id": 4,
        "title": "Gold Medalist - Mathematics Olympiad",
        "organization": "School Level Mathematics Olympiad",
        "year": "2022",
        "description": "Awarded Gold Medal demonstrating exceptional mathematical reasoning and analytical problem-solving skills."
    },
    {
        "id": 5,
        "title": "500+ Data Structures & Algorithms Solved",
        "organization": "LeetCode / Coding Platforms",
        "year": "2023 - Present",
        "description": "Solved over 500 DSA problems strengthening core computational thinking and algorithm optimization."
    }
]

def normalize_and_export():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge", "structured"))
    os.makedirs(output_dir, exist_ok=True)

    # Validate using Pydantic schemas before dumping
    profile_model = ProfileSchema(**PROFILE)
    projects_model = [ProjectSchema(**p) for p in PROJECTS]
    experience_model = [ExperienceSchema(**e) for e in EXPERIENCE]
    skills_model = [SkillCategorySchema(**s) for s in SKILLS]
    education_model = [EducationSchema(**e) for e in EDUCATION]
    certifications_model = [CertificationSchema(**c) for c in CERTIFICATIONS]
    achievements_model = [AchievementSchema(**a) for a in ACHIEVEMENTS]

    export_map = {
        "profile.json": profile_model.model_dump(),
        "projects.json": [p.model_dump() for p in projects_model],
        "experience.json": [e.model_dump() for e in experience_model],
        "skills.json": [s.model_dump() for s in skills_model],
        "education.json": [e.model_dump() for e in education_model],
        "certifications.json": [c.model_dump() for c in certifications_model],
        "achievements.json": [a.model_dump() for a in achievements_model],
    }

    for filename, data in export_map.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[Exported & Validated]: {filepath}")

if __name__ == "__main__":
    normalize_and_export()
