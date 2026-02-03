from typing import List

from pydantic import BaseModel


class SectionOutline(BaseModel):
    title: str
    description: str


class LearningMaterialOutline(BaseModel):
    sections: List[SectionOutline]


class Section(BaseModel):
    title: str
    content: str
