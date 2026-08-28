"""
Pydantic Schemas for Akhil Portfolio Data Entities & RAG Metadata.
Provides strict type-checking, schema validation, and metadata tagging for vector RAG workflows.
"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Stat(BaseModel):
    label: str
    value: str


class ProfileSchema(BaseModel):
    name: str
    full_name: str
    title: str
    tagline: str
    bio: str
    email: Optional[str] = None
    location: str
    status: Optional[str] = None
    avatar_text: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    stats: List[Stat] = Field(default_factory=list)
    highlights: List[str] = Field(default_factory=list)


class ProjectMetric(BaseModel):
    value: str
    label: str


class Project(BaseModel):
    id: Union[int, str]
    name: str
    description: str
    problem: Optional[str] = None
    solution: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    role: Optional[str] = None
    challenges: Union[List[str], str] = Field(default_factory=list)
    results: Union[List[ProjectMetric], List[str]] = Field(default_factory=list)
    github: Optional[str] = None
    demo: Optional[str] = None

    # Metadata & UI compatibility fields
    slug: Optional[str] = None
    category: Optional[str] = "General"
    featured: Optional[bool] = False
    image: Optional[str] = None
    long_description: Optional[str] = None
    architecture_highlights: Optional[str] = None

    @property
    def title(self) -> str:
        return self.name

    @property
    def tags(self) -> List[str]:
        return self.technologies

    @property
    def key_features(self) -> List[str]:
        return self.features

    @property
    def my_contribution(self) -> Optional[str]:
        return self.role

    @property
    def repo_url(self) -> Optional[str]:
        return self.github

    @property
    def demo_url(self) -> Optional[str]:
        return self.demo


# Alias for backward compatibility
ProjectSchema = Project


class Experience(BaseModel):
    company: str
    role: str
    type: Optional[str] = "Hackathon"
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = "India"
    description: str
    technologies: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)

    # UI & Backward Compatibility fields
    year: Optional[str] = None
    period: Optional[str] = None


# Alias for backward compatibility
ExperienceSchema = Experience


class SkillItem(BaseModel):
    name: str
    level: Optional[int] = 90
    icon: Optional[str] = "fa-code"
    color: Optional[str] = "#38bdf8"


class SkillCategory(BaseModel):
    category: str
    icon: Optional[str] = "fa-layer-group"
    skills: Union[List[str], List[SkillItem]]


# Alias for backward compatibility
SkillCategorySchema = SkillCategory


class Education(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)

    # UI & Backward Compatibility field
    period: Optional[str] = None


# Alias for backward compatibility
EducationSchema = Education


class CertificationSchema(BaseModel):
    title: str
    issuer: str
    date: str
    credential_url: str


class AchievementSchema(BaseModel):
    id: int
    title: str
    organization: str
    year: str
    description: str


class DocumentMetadata(BaseModel):
    source: str
    doc_id: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    github: Optional[str] = None
    demo: Optional[str] = None


class RAGDocument(BaseModel):
    content: str
    metadata: DocumentMetadata
