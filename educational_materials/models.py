from typing import List
from pydantic import BaseModel


class OutlinePoint(BaseModel):
    """Represents a single point in the curriculum outline."""
    title: str
    description: str


class CurriculumOutline(BaseModel):
    """Represents the complete curriculum outline."""
    points: List[OutlinePoint]


class Section(BaseModel):
    """Represents a generated section/lesson."""
    title: str
    content: str
