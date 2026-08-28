"""
Data Normalization & Export Script for Akhil Portfolio.
Reads raw data modules from data/, normalizes all skills and technical terms via CANONICAL_TERMS_MAP,
validates them with Pydantic schemas, and exports normalized JSON files to knowledge/structured/.
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
    Project,
    Experience,
    SkillCategory,
    Education,
    CertificationSchema,
    AchievementSchema,
)

# Comprehensive Canonical Term Normalization Mapping Dictionary
CANONICAL_TERMS_MAP = {
    # Programming Languages
    "python": "Python",
    "c++": "C++", "cpp": "C++", "c plus plus": "C++",
    "sql": "SQL",

    # Generative AI & LLMs
    "generative ai": "Generative AI & LLMs", "genai": "Generative AI & LLMs", "gen ai": "Generative AI & LLMs",
    "rag": "Retrieval-Augmented Generation (RAG)", "retrieval augmented generation": "Retrieval-Augmented Generation (RAG)",
    "langchain": "LangChain", "lang chain": "LangChain",
    "langgraph": "LangGraph", "lang graph": "LangGraph",
    "mcp": "Model Context Protocol (MCP)", "fastmcp": "FastMCP", "fast mcp": "FastMCP",
    "groq": "Groq",
    "llama": "Llama 3.3 70B", "llama 3": "Llama 3.3 70B", "llama 3.3 70b": "Llama 3.3 70B",
    "gpt 4o mini": "GPT-4o-mini", "gpt-4o-mini": "GPT-4o-mini",
    "openrouter": "OpenRouter",
    "prompt engineering": "Prompt Engineering & Embeddings",
    "fine tuning": "Model Fine-Tuning", "finetuning": "Model Fine-Tuning",

    # Vector Search & Databases
    "faiss": "FAISS",
    "chromadb": "ChromaDB", "chroma db": "ChromaDB", "chroma": "ChromaDB",
    "huggingface": "HuggingFace Embeddings", "hugging face": "HuggingFace Embeddings",
    "sentencetransformers": "SentenceTransformers", "sentence transformers": "SentenceTransformers",
    "semantic search": "Semantic Search",

    # Machine Learning & Deep Learning
    "pytorch": "PyTorch", "py torch": "PyTorch",
    "scikit-learn": "Scikit-Learn", "scikit learn": "Scikit-Learn", "sklearn": "Scikit-Learn",
    "xgboost": "XGBoost", "xg boost": "XGBoost",
    "random forest": "Random Forest", "randomforest": "Random Forest",
    "yolov8": "YOLOv8", "yolo v8": "YOLOv8", "yolo": "YOLOv8",
    "computer vision": "Computer Vision",
    "shap": "SHAP Explainability",
    "optuna": "Optuna",
    "mlflow": "MLflow",
    "eda": "Exploratory Data Analysis (EDA)", "exploratory data analysis": "Exploratory Data Analysis (EDA)",

    # Data Engineering & Libraries
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",
    "prophet": "Prophet",

    # Databases & Cloud
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "duckdb": "DuckDB",
    "sqlite": "SQLite",

    # Business Intelligence & Tools
    "power bi": "Power BI", "powerbi": "Power BI",
    "tableau": "Tableau",
    "streamlit": "Streamlit",
    "dash": "Plotly Dash",
    "fastapi": "FastAPI", "fast api": "FastAPI",
    "docker": "Docker",
    "git": "Git & GitHub", "github": "Git & GitHub",
}

def canonicalize_term(term: str) -> str:
    """Returns the canonicalized technical term if present in map, otherwise stripped original term."""
    cleaned = term.strip()
    return CANONICAL_TERMS_MAP.get(cleaned.lower(), cleaned)

def normalize_list(items: list[str]) -> list[str]:
    """Normalizes a list of technology or skill terms preserving order without duplicates."""
    normalized = []
    for item in items:
        canon = canonicalize_term(item)
        if canon not in normalized:
            normalized.append(canon)
    return normalized

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

    # Normalize projects technical terms
    normalized_projects = []
    for p in PROJECTS:
        p_copy = dict(p)
        if "technologies" in p_copy:
            p_copy["technologies"] = normalize_list(p_copy["technologies"])
        if "tags" in p_copy:
            p_copy["tags"] = normalize_list(p_copy["tags"])
        normalized_projects.append(p_copy)

    # Normalize experience technical terms
    normalized_experience = []
    for e in EXPERIENCE:
        e_copy = dict(e)
        if "technologies" in e_copy:
            e_copy["technologies"] = normalize_list(e_copy["technologies"])
        normalized_experience.append(e_copy)

    # Validate using Pydantic schemas before dumping
    profile_model = ProfileSchema(**PROFILE)
    projects_model = [Project(**p) for p in normalized_projects]
    experience_model = [Experience(**e) for e in normalized_experience]
    skills_model = [SkillCategory(**s) for s in SKILLS]
    education_model = [Education(**e) for e in EDUCATION]
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
