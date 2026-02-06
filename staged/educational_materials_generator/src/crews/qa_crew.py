"""Stage 5 QA Crew - Quality assurance and review."""

from crewai import Agent, Task, Crew
from src.agents import QAAgents
from src.standardizer import StandardizationManager


def create_qa_crew(topic: str, all_materials: dict):
    """Create Stage 5 QA crew."""
    
    reviewer = QAAgents.pedagogical_reviewer()
    clarity_checker = QAAgents.clarity_checker()
    
    std_manager = StandardizationManager()
    qa_prompt = std_manager.get_stage_prompt("qa")
    
    pedagogical_task = Task(
        description=f"""
        Review pedagogical alignment for '{topic}':
        
        All materials summary: {str(all_materials)[:500]}...
        
        Check:
        1. Learning objectives clarity and measurability
        2. Alignment: objectives → instruction → assessment
        3. Appropriate cognitive load and challenge
        4. Prerequisite validity and sequencing
        5. Bloom's taxonomy level appropriateness
        6. Coverage of all intended outcomes
        
        {qa_prompt}
        
        Return JSON QA report with issues and suggestions.
        """,
        agent=reviewer,
        expected_output="JSON QA report with alignment issues and improvement suggestions"
    )
    
    clarity_task = Task(
        description=f"""
        Review clarity and accessibility for '{topic}':
        
        Check:
        1. Reading level (Flesch-Kincaid target: grade 9)
        2. Jargon and technical term explanations
        3. Gender and cultural bias
        4. WCAG 2.1 AA compliance
        5. Color contrast and visual clarity
        6. Alt-text quality for images
        7. Heading hierarchy
        8. Plain language principles
        
        {qa_prompt}
        
        Return JSON accessibility audit and bias report.
        """,
        agent=clarity_checker,
        expected_output="JSON accessibility audit with clarity issues and fixes"
    )
    
    crew = Crew(
        agents=[reviewer, clarity_checker],
        tasks=[pedagogical_task, clarity_task],
        verbose=True,
    )
    
    return crew


def run_qa_crew(topic: str, all_materials: dict):
    """Execute QA crew."""
    crew = create_qa_crew(topic, all_materials)
    result = crew.kickoff()
    return {
        "status": "completed",
        "output": str(result),
    }
