"""Stage 1 Discovery Crew - Research and benchmarking (Batched by Platform)."""

from crewai import Agent, Task, Crew
from src.agents import DiscoveryAgents
from src.standardizer import StandardizationManager
import os
import json


def _run_platform_research_batch(topic: str, platform: str, urls: list, researcher_agent):
    """Run a focused research task for a single platform to avoid timeout.
    
    Args:
        topic: Course topic
        platform: Single platform (e.g., "Coursera", "Udemy")
        urls: Reference URLs
        researcher_agent: Agent instance to use
        
    Returns:
        String result from the research task
    """
    task_desc = f"""
    Research and analyze courses on '{platform}' for the topic '{topic}'.
    
    Focus ONLY on {platform} courses in this search.
    
    Reference URLs: {', '.join(urls)}
    
    Extract and document for each course found:
    1. Course title and structure
    2. Learning outcomes
    3. Duration and pacing
    4. Target audience
    5. Assessment methods
    6. Key topics covered
    7. Teaching approaches
    
    Return findings as JSON array of course objects.
    Keep response concise and focused on {platform} only.
    """
    
    task = Task(
        description=task_desc,
        agent=researcher_agent,
        expected_output=f"JSON array of {platform} courses with structure, outcomes, duration"
    )
    
    crew = Crew(agents=[researcher_agent], tasks=[task], verbose=False)
    result = crew.kickoff()
    return str(result)


def create_discovery_crew(topic: str, urls: list):
    """Create Stage 1 Discovery crew with batched platform research.
    
    Args:
        topic: Course topic (e.g., "Azure Fundamentals")
        urls: List of reference URLs
        
    Returns:
        Dict with batched research results or Crew instance (legacy compat)
    """
    
    # Get agents
    researcher = DiscoveryAgents.course_researcher()
    analyst = DiscoveryAgents.trends_analyst()
    persona_builder = DiscoveryAgents.persona_builder()
    
    # Get standardization prompt
    std_manager = StandardizationManager()
    discovery_prompt = std_manager.get_stage_prompt("discovery")
    
    # Platforms to research in batches (each gets its own small task to avoid timeout)
    platforms = ["Coursera", "Udemy", "edX", "YouTube", "GitHub"]
    all_courses = []
    
    print(f"🔍 Stage 1: Batching research across {len(platforms)} platforms...")
    
    # Run research for each platform separately
    for platform in platforms:
        try:
            print(f"  → Researching {platform}...")
            platform_result = _run_platform_research_batch(topic, platform, urls, researcher)
            # Try to extract JSON from result
            try:
                # Simple attempt to find JSON array in response
                start = platform_result.find('[')
                end = platform_result.rfind(']')
                if start != -1 and end != -1:
                    json_str = platform_result[start:end+1]
                    courses = json.loads(json_str)
                    if isinstance(courses, list):
                        all_courses.extend(courses)
                        print(f"    ✓ Found {len(courses)} courses")
                    else:
                        print(f"    ⚠ Non-array JSON found, skipping")
                else:
                    print(f"    ⚠ No JSON found in response, skipping")
            except json.JSONDecodeError:
                print(f"    ⚠ Failed to parse JSON for {platform}")
        except Exception as e:
            print(f"    ✗ Error researching {platform}: {str(e)[:80]}")
    
    # Merge all platform research into a single analysis
    merged_research = {
        "total_courses_found": len(all_courses),
        "platforms_researched": platforms,
        "courses": all_courses,
        "summary": f"Analyzed {len(all_courses)} courses across {len(platforms)} platforms for {topic}"
    }
    
    # Now run trends and persona tasks with merged research context
    print(f"🔄 Analyzing trends across {len(all_courses)} courses...")
    
    trends_task = Task(
        description=f"""
        Based on the following course research data for '{topic}':
        {json.dumps(merged_research, indent=2)[:2000]}  (truncated)
        
        Analyze skill trends and gaps:
        1. Most commonly taught skills
        2. Gaps between courses and industry
        3. Emerging technologies and trends
        4. Certification requirements
        5. Prerequisite skills
        
        {discovery_prompt}
        
        Return structured JSON with skill matrix and trend analysis.
        """,
        agent=analyst,
        expected_output="JSON with skill matrix, gaps, trends"
    )
    
    trends_crew = Crew(agents=[analyst], tasks=[trends_task], verbose=False)
    trends_result = trends_crew.kickoff()
    
    print(f"👥 Building learner personas...")
    
    persona_task = Task(
        description=f"""
        Based on course analysis for '{topic}' with {len(all_courses)} courses analyzed:
        
        Create 2-5 distinct learner personas including:
        - Experience level (Beginner/Intermediate/Advanced)
        - Learning goals
        - Time availability
        - Prior knowledge
        - Learning style preferences
        - Technology comfort
        - Accessibility needs
        - Pain points and motivations
        
        {discovery_prompt}
        
        Return JSON with persona profiles.
        """,
        agent=persona_builder,
        expected_output="JSON with 2-5 learner personas"
    )
    
    persona_crew = Crew(agents=[persona_builder], tasks=[persona_task], verbose=False)
    personas_result = persona_crew.kickoff()
    
    # Return merged results as dict (not Crew instance)
    return {
        "status": "completed",
        "output": {
            "research_summary": merged_research,
            "trends_analysis": str(trends_result),
            "personas": str(personas_result)
        }
    }


def run_discovery_crew(topic: str, urls: list):
    """Execute discovery crew with batching and return results.
    
    Falls back to demo mode if Ollama model not available.
    
    Returns:
        Dict with course_analysis, trends_analysis, personas
    """
    try:
        result = create_discovery_crew(topic, urls)
        # If we got here with batching, return the dict
        if isinstance(result, dict) and "status" in result:
            return result
        # Else it's a Crew instance (legacy path)
        crew_result = result.kickoff() if hasattr(result, 'kickoff') else result
        return {
            "status": "completed",
            "output": str(crew_result),
        }
    except Exception as e:
        # During debugging allow disabling fallback by setting NO_FALLBACK=1
        if os.getenv('NO_FALLBACK', '').lower() in ('1','true','yes'):
            print('🔎 NO_FALLBACK set — re-raising exception for debugging')
            raise
        # Fallback to demo/mock mode
        error_str = str(e).lower()
        if "not found" in error_str or "connection" in error_str or "timeout" in error_str:
            print(f"⚠️  Error querying LLM model, using demo mode for Stage 1")
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

