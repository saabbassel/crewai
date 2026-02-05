"""Pydantic models for educational materials generator."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# ====================================
# Stage 1: Discovery Models
# ====================================

class ResearchCourse(BaseModel):
    """Single course research data."""
    title: str
    platform: str
    duration_hours: float
    rating: Optional[float] = None
    key_modules: List[str]
    url: Optional[str] = None


class AudiencePersona(BaseModel):
    """Learner profile."""
    name: str
    background: str
    goals: List[str]
    learning_time_weeks: int
    difficulty_level: str  # Beginner, Intermediate, Advanced


class ResearchDossier(BaseModel):
    """Stage 1 output: Research findings."""
    topic: str
    research_date: datetime
    popular_courses: List[ResearchCourse]
    common_modules: List[str]
    skill_gaps: List[str]
    audience_personas: List[AudiencePersona]
    quality_metrics: Dict[str, float]


# ====================================
# Stage 2: Curriculum Models
# ====================================

class LearningObjective(BaseModel):
    """Single learning objective following Bloom's taxonomy."""
    bloom_level: str  # Remember, Understand, Apply, Analyze, Evaluate, Create
    action_verb: str
    content: str
    condition: Optional[str] = None

    @property
    def formatted(self) -> str:
        return f"{self.bloom_level.upper()}: {self.action_verb} {self.content}"


class ModuleBlueprint(BaseModel):
    """Single curriculum module."""
    module_id: str
    title: str
    bloom_level: str
    duration_minutes: int
    learning_objectives: List[LearningObjective]
    prerequisites: List[str] = Field(default_factory=list)
    key_concepts: List[str]
    assessment_type: str  # MCQ, Practical, Project, etc.


class CurriculumBlueprint(BaseModel):
    """Stage 2 output: Curriculum design."""
    course_title: str
    course_code: str
    total_duration_hours: int
    target_proficiency: str
    learning_outcomes: List[str]
    modules: List[ModuleBlueprint]
    quality_metrics: Dict[str, float]


# ====================================
# Stage 3: Content Models
# ====================================

class Lesson(BaseModel):
    """Single lesson content."""
    lesson_id: str
    module_id: str
    title: str
    overview: str
    key_concepts: Dict[str, str]
    worked_examples: List[str]
    common_mistakes: List[str]


class Handout(BaseModel):
    """Quick reference handout."""
    handout_id: str
    module_id: str
    title: str
    difficulty_level: str
    learning_time_minutes: int
    key_concepts: List[str]
    essential_facts: Dict[str, str]
    resources: List[Dict[str, str]]


class ContentMaterial(BaseModel):
    """Stage 3 output: Content artifact."""
    module_id: str
    lessons: List[Lesson]
    handouts: List[Handout]
    version: str
    generated_at: datetime
    quality_metrics: Dict[str, float]


# ====================================
# Stage 4: Assessment Models
# ====================================

class QuizQuestion(BaseModel):
    """Multiple choice question."""
    id: str
    question: str
    options: Dict[str, str]  # A, B, C, D
    correct_answer: str
    explanation: str
    learning_resource: str


class Quiz(BaseModel):
    """Assessment quiz."""
    assessment_id: str
    type: str  # multiple_choice, short_answer, etc.
    difficulty_level: str
    bloom_level: str
    questions: List[QuizQuestion]
    passing_score: int
    time_limit_minutes: int


class Exercise(BaseModel):
    """Hands-on exercise."""
    exercise_id: str
    module_id: str
    title: str
    bloom_level: str
    difficulty: str
    duration_minutes: int
    learning_objectives: List[str]
    instructions: str
    success_criteria: List[str]
    hints: List[str] = Field(default_factory=list)
    solution_steps: List[str]
    common_mistakes: List[str]


class Project(BaseModel):
    """Capstone project."""
    project_id: str
    module_id: str
    title: str
    duration_hours: int
    real_world_context: str
    milestones: List[str]
    rubric: Dict[str, Dict[str, str]]
    cost_estimate: Optional[str] = None


class Assessment(BaseModel):
    """Stage 4 output: Exercises and assessments."""
    module_id: str
    exercises: List[Exercise]
    quizzes: List[Quiz]
    projects: List[Project]
    version: str
    generated_at: datetime
    quality_metrics: Dict[str, float]


# ====================================
# Stage 5: QA Models
# ====================================

class QAIssue(BaseModel):
    """Single quality issue found."""
    issue_id: str
    module_id: str
    severity: str  # critical, high, medium, low
    issue_type: str  # clarity, formatting, accessibility, alignment, terminology
    section: str
    description: str
    suggestion: str
    status: str = "open"


class QAReport(BaseModel):
    """Stage 5 output: Quality assurance results."""
    review_date: datetime
    course_id: str
    modules_reviewed: int
    total_issues: int
    critical_issues: int
    
    quality_scores: Dict[str, float]  # overall, pedagogical, clarity, accessibility, consistency
    issues: List[QAIssue]
    
    consistency_report: Dict[str, Any]
    accessibility_report: Dict[str, Any]
    
    recommendations: List[str]
    pass_fail: str  # PASS, WARNING, FAIL
    ready_for_publication: bool


# ====================================
# Metadata Models
# ====================================

class DocumentMetadata(BaseModel):
    """Universal metadata for all artifacts."""
    title: str
    version: str
    date_generated: datetime
    stage: int
    course_id: str
    module_id: Optional[str] = None
    author: str
    language: str = "en"
    encoding: str = "utf-8"


class QualityMetrics(BaseModel):
    """Standard quality scoring."""
    completeness: float = Field(ge=0, le=1)  # 0-1
    clarity_score: float = Field(ge=1, le=10)  # 1-10
    alignment_score: float = Field(ge=0, le=1)  # 0-1
    validation_status: str  # PASS, WARNING, FAIL
    flesch_kincaid_grade: Optional[float] = None
    accessibility_level: Optional[str] = None  # A, AA, AAA


# ====================================
# Flow State Model
# ====================================

class FlowState(BaseModel):
    """State tracking for multi-stage flow."""
    topic: str
    level: str
    urls: List[str]
    course_id: str
    output_dir: str
    
    research_dossier: Optional[ResearchDossier] = None
    curriculum_blueprint: Optional[CurriculumBlueprint] = None
    content_materials: List[ContentMaterial] = Field(default_factory=list)
    assessments: List[Assessment] = Field(default_factory=list)
    qa_report: Optional[QAReport] = None
    
    start_time: datetime = Field(default_factory=datetime.now)
    last_update: datetime = Field(default_factory=datetime.now)
