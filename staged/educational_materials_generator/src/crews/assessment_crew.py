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
        Design hands-on exercises for '{topic}' modules.
        
        Create 3-5 exercises with:
        1. Exercise title and difficulty level (Beginner/Intermediate/Advanced)
        2. Clear instructions (50-100 words)
        3. Success criteria (2-3 bullet points)
        4. Estimated duration
        5. Tools/resources needed
        
        Return as JSON array of exercises.
        """,
        agent=exercise_designer,
        expected_output="JSON array of exercises with instructions, criteria, duration",
    )
    
    assessment_task = Task(
        description=f"""
        Create quizzes and rubrics for '{topic}'.
        
        Design:
        1. Quiz with 5-10 multiple choice questions
        2. Exercise rubric with 4-point scale (Novice to Advanced)
        3. Self-assessment checklist (3-5 items)
        
        Return as structured JSON.
        """,
        agent=assessment_builder,
        expected_output="JSON with quizzes, rubrics, self-assessment",
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
        import traceback
        print(f"❌ Stage 4 Assessment Crew Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        if "not found" in str(e).lower() or "connection" in str(e).lower():
            print(f"⚠️  Using demo mode for Stage 4 (model unavailable)")
        else:
            print(f"⚠️  Using demo mode for Stage 4 (crew execution failed)")
            
        return {
            "status": "demo",
            "output": {
                "exercises": ["EX-001_basics", "EX-002_intermediate", "EX-003_advanced"],
                "quizzes": [{"id": "QUIZ-01", "questions": 20}, {"id": "QUIZ-02", "questions": 15}],
                "projects": [{"title": "Capstone Project", "duration_hours": 10}]
            }
        }
