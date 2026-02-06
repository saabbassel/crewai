"""Stage 4 Assessment Crew - Hands-on and evaluation."""

from crewai import Agent, Task, Crew
from src.agents import AssessmentAgents
from src.standardizer import StandardizationManager


def create_assessment_crew(topic: str, curriculum: dict):
    """Create Stage 4 Assessment crew."""
    
    exercise_designer = AssessmentAgents.exercise_designer()
    assessment_builder = AssessmentAgents.assessment_builder()
    
    std_manager = StandardizationManager()
    assess_prompt = std_manager.get_stage_prompt("assessment")
    
    exercise_task = Task(
        description=f"""
        Design exercises for '{topic}':
        
        Curriculum: {curriculum.get('summary', 'N/A')}
        
        Create per module:
        1. Guided practice exercises
        2. Open-ended challenges
        3. Progressive difficulty levels
        4. Clear success criteria
        5. Step-by-step hints
        6. Common mistakes and fixes
        7. Real-world connections
        
        {assess_prompt}
        
        Return JSON exercises with solutions.
        """,
        agent=exercise_designer,
        expected_output="JSON exercises per module with solutions, hints, rubrics"
    )
    
    assessment_task = Task(
        description=f"""
        Create assessments for '{topic}':
        
        Per module, create:
        1. Quiz items at multiple Bloom's levels
        2. Self-assessment checklists
        3. Rubrics for projects
        4. Answer keys with explanations
        5. Difficulty ratings
        
        {assess_prompt}
        
        Return JSON assessments file.
        """,
        agent=assessment_builder,
        expected_output="JSON quizzes, rubrics, self-assessment tools"
    )
    
    crew = Crew(
        agents=[exercise_designer, assessment_builder],
        tasks=[exercise_task, assessment_task],
        verbose=True,
    )
    
    return crew


def run_assessment_crew(topic: str, curriculum: dict):
    """Execute assessment crew. Falls back to demo mode if Ollama unavailable."""
    try:
        crew = create_assessment_crew(topic, curriculum)
        result = crew.kickoff()
        return {"status": "completed", "output": str(result)}
    except Exception as e:
        if "not found" in str(e).lower() or "connection" in str(e).lower():
            print(f"⚠️  Using demo mode for Stage 4")
            return {
                "status": "demo",
                "output": {
                    "exercises": ["EX-001_basics", "EX-002_intermediate", "EX-003_advanced"],
                    "quizzes": [{"id": "QUIZ-01", "questions": 20}, {"id": "QUIZ-02", "questions": 15}],
                    "projects": [{"title": "Capstone Project", "duration_hours": 10}]
                }
            }
        raise
