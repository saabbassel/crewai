"""Educational Materials Generator - Main Package."""

__version__ = "1.0.0"
__author__ = "Educational AI Team"

from src.models import (
    ResearchDossier,
    CurriculumBlueprint,
    ContentMaterial,
    Assessment,
    QAReport,
)
from src.config import Config, LLMConfig
from src.standardizer import StandardizationManager

__all__ = [
    "ResearchDossier",
    "CurriculumBlueprint",
    "ContentMaterial",
    "Assessment",
    "QAReport",
    "Config",
    "LLMConfig",
    "StandardizationManager",
]
