"""Stage 2 Curriculum Crew - Architecture and design."""

from crewai import Agent, Task, Crew
from src.agents import CurriculumAgents
from src.standardizer import StandardizationManager


def create_curriculum_crew(topic: str, research_dossier: dict):
    """Create Stage 2 Curriculum crew.
    
    Args:
        topic: Course topic
        research_dossier: Output from Stage 1 discovery
        
    Returns:
        Crew instance
    """
    
    designer = CurriculumAgents.curriculum_designer()
    id_expert = CurriculumAgents.instructional_designer()
    
    std_manager = StandardizationManager()
    curr_prompt = std_manager.get_stage_prompt("curriculum")
    
    design_task = Task(
        description=f"""
        Design curriculum for '{topic}' using Stage 1 research:
        
        Research summary: {research_dossier.get('summary', 'N/A')}
        
        Create a well-structured curriculum with:
        1. 8-12 modules organized logically
        2. Clear learning objectives per module aligned to Bloom's taxonomy
        3. Prerequisite mapping and dependencies
        4. Time allocation per module
        5. Spiral learning approach (revisit concepts in depth)
        6. Cognitive load progression
        7. Assessment checkpoints
        
        {curr_prompt}
        
        Return JSON curriculum blueprint.
        """,
        agent=designer,
        expected_output="JSON curriculum blueprint with modules, objectives, sequence"
    )
    
    instructional_task = Task(
        description=f"""
        Design instructional strategies for curriculum:
        
        For each module, specify:
        1. Instructional method (Lecture/Demo/Discussion/Hands-on/Project)
        2. Practice opportunities and scaffolding
        3. Example types needed (worked, non-worked, misconception)
        4. Assessment strategy (formative/summative)
        5. Differentiation approaches
        6. Media and modalities
        7. Estimated duration
        
        {curr_prompt}
        
        Return JSON with instructional strategy map.
        """,
        agent=id_expert,
        expected_output="JSON instructional design map with methods, practice, assessment"
    )
    
    crew = Crew(
        agents=[designer, id_expert],
        tasks=[design_task, instructional_task],
        verbose=True,
    )
    
    return crew


def run_curriculum_crew(topic: str, research_dossier: dict):
    """Execute curriculum crew."""
    crew = create_curriculum_crew(topic, research_dossier)
    result = crew.kickoff()
    return {
        "status": "completed",
        "output": str(result),
    }
