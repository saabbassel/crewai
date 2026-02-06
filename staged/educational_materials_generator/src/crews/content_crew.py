"""Stage 3 Content Crew - Production."""

from crewai import Agent, Task, Crew
from src.agents import ContentAgents
from src.standardizer import StandardizationManager


def create_content_crew(topic: str, curriculum: dict):
    """Create Stage 3 Content crew."""
    
    author = ContentAgents.lesson_author()
    example_gen = ContentAgents.example_generator()
    
    std_manager = StandardizationManager()
    content_prompt = std_manager.get_stage_prompt("content")
    
    lesson_task = Task(
        description=f"""
        Write lessons for '{topic}' modules:
        
        Curriculum: {curriculum.get('summary', 'N/A')}
        
        For each module, create:
        1. Clear introduction connecting to prior knowledge
        2. Step-by-step concept explanations
        3. Analogies for abstract concepts
        4. Real-world connections
        5. Key takeaways
        6. Comprehension checks
        
        Grade level target: 9 (adjustable)
        Variants: Academic + Conversational tone
        
        {content_prompt}
        
        Return markdown files per module.
        """,
        agent=author,
        expected_output="Markdown lesson content per module, structured and clear"
    )
    
    examples_task = Task(
        description=f"""
        Generate examples for '{topic}':
        
        Create for each module:
        1. Worked examples (step-by-step solutions)
        2. Real-world scenarios
        3. Common mistakes and how to fix them
        4. Edge cases and boundary conditions
        5. Visual/textual/code representations
        
        {content_prompt}
        
        Return JSON examples file.
        """,
        agent=example_gen,
        expected_output="JSON examples with worked solutions, scenarios, mistakes"
    )
    
    crew = Crew(
        agents=[author, example_gen],
        tasks=[lesson_task, examples_task],
        verbose=True,
    )
    
    return crew


def run_content_crew(topic: str, curriculum: dict):
    """Execute content crew."""
    crew = create_content_crew(topic, curriculum)
    result = crew.kickoff()
    return {
        "status": "completed",
        "output": str(result),
    }
