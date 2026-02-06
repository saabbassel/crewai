"""Stage 1 Discovery Crew - Research and benchmarking."""

from crewai import Agent, Task, Crew
from src.agents import DiscoveryAgents
from src.standardizer import StandardizationManager


def create_discovery_crew(topic: str, urls: list):
    """Create and return a Stage 1 Discovery crew.
    
    Args:
        topic: Course topic (e.g., "Azure Fundamentals")
        urls: List of reference URLs
        
    Returns:
        Crew instance ready to execute
    """
    
    # Get agents
    researcher = DiscoveryAgents.course_researcher()
    analyst = DiscoveryAgents.trends_analyst()
    persona_builder = DiscoveryAgents.persona_builder()
    
    # Get standardization prompt
    std_manager = StandardizationManager()
    discovery_prompt = std_manager.get_stage_prompt("discovery")
    
    # Define tasks
    research_task = Task(
        description=f"""
        Analyze online courses on '{topic}' from major platforms:
        - Coursera
        - Udemy
        - edX
        - YouTube
        - GitHub
        
        Reference URLs provided: {', '.join(urls)}
        
        For each course found, extract and document:
        1. Course structure and module breakdown
        2. Learning outcomes and objectives
        3. Duration and pacing
        4. Target audience
        5. Assessment strategies
        6. Key topics covered
        7. Pedagogical approaches used
        
        {discovery_prompt}
        
        Return a structured analysis JSON with findings.
        """,
        agent=researcher,
        expected_output="JSON structured course analysis with platforms, modules, outcomes"
    )
    
    trends_task = Task(
        description=f"""
        Analyze skill trends and gaps for '{topic}':
        
        1. Most commonly taught skills across courses
        2. Skills gaps between courses and industry needs
        3. Emerging technologies and trends in the space
        4. Certification requirements
        5. Prerequisite skills needed
        6. Geographic/demographic variations
        
        Use the course data gathered to identify:
        - Overcovered topics
        - Undercovered skills
        - Hot/emerging areas
        
        {discovery_prompt}
        
        Return structured JSON with skill matrix and trend analysis.
        """,
        agent=analyst,
        expected_output="JSON with skill matrix, gaps, trends, and market analysis"
    )
    
    persona_task = Task(
        description=f"""
        Create detailed learner personas for '{topic}':
        
        Based on course research, create 2-5 distinct personas including:
        
        For each persona:
        1. Experience level (Beginner/Intermediate/Advanced)
        2. Learning goals (Career/Academic/Hobby)
        3. Time availability (hours per week)
        4. Prior knowledge and prerequisites
        5. Learning style preferences (Visual/Hands-on/Reading)
        6. Technology comfort level
        7. Accessibility needs
        8. Pain points and motivations
        
        {discovery_prompt}
        
        Return JSON with persona profiles including demographics, learning goals, constraints.
        """,
        agent=persona_builder,
        expected_output="JSON with 2-5 learner personas including goals, constraints, preferences"
    )
    
    # Create and return crew
    crew = Crew(
        agents=[researcher, analyst, persona_builder],
        tasks=[research_task, trends_task, persona_task],
        verbose=True,
    )
    
    return crew


def run_discovery_crew(topic: str, urls: list):
    """Execute discovery crew and return results.
    
    Falls back to demo mode if Ollama model not available.
    
    Returns:
        Dict with course_analysis, trends_analysis, personas
    """
    try:
        crew = create_discovery_crew(topic, urls)
        result = crew.kickoff()
        return {
            "status": "completed",
            "output": str(result),
        }
    except Exception as e:
        # Fallback to demo/mock mode
        error_str = str(e).lower()
        if "not found" in error_str or "connection" in error_str:
            print(f"⚠️  Ollama model not available, using demo mode for Stage 1")
            return {
                "status": "demo",
                "output": {
                    "courses_analyzed": [
                        {
                            "platform": "Microsoft Learn",
                            "title": f"{topic} Learning Path",
                            "modules": 10,
                            "duration_hours": 50,
                            "rating": 4.8
                        },
                        {
                            "platform": "Coursera",
                            "title": f"Introduction to {topic}",
                            "modules": 8,
                            "duration_hours": 40,
                            "rating": 4.7
                        }
                    ],
                    "skill_gaps": [
                        "Cloud architecture design",
                        "Cost optimization",
                        "Security best practices",
                        "DevOps integration"
                    ],
                    "personas": [
                        {"name": "IT Professional", "experience": "Intermediate", "goal": "Cloud migration"},
                        {"name": "Developer", "experience": "Beginner", "goal": "Cloud-native apps"}
                    ]
                }
            }
        raise
