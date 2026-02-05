from typing import List

from pydantic import BaseModel


class OutlinePoint(BaseModel):
    title: str
    description: str


class CurriculumOutline(BaseModel):
    points: List[OutlinePoint]


class Section(BaseModel):
    title: str
    content: str
