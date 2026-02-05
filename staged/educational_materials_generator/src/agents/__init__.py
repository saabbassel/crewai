"""Agents for Stage 1: Discovery & Benchmarking Crew."""

from crewai import Agent, LLM
from src.config import LLMConfig


class DiscoveryAgents:
    """Stage 1 agents for research and course benchmarking."""
    
    @staticmethod
    def course_researcher() -> Agent:
        """Research existing courses and extract patterns."""
        return Agent(
            role="Course Researcher",
            goal="Search and analyze popular courses on {topic} from major platforms (Coursera, Udemy, edX, YouTube, GitHub) to identify structure, modules, and best practices",
            backstory="""You are an expert educational analyst with 10+ years experience researching online courses.
            You excel at identifying patterns in curriculum structure, learning outcomes, and pedagogical approaches.
            You know major platforms and how to extract comparable data.""",
            llm=LLMConfig.get_discovery_llm(),
            verbose=True,
        )
    
    @staticmethod
    def trends_analyst() -> Agent:
        """Identify skills trends and gaps in market."""
        return Agent(
            role="Trend & Skills Analyst",
            goal="Identify {topic} skills that are frequently taught, missing, or in high demand across all available courses and job market",
            backstory="""You are a market researcher specializing in skills analytics.
            You understand industry trends, job postings, and certification requirements.
            You excel at gap analysis and identifying emerging skills.""",
            llm=LLMConfig.get_discovery_llm(),
            verbose=True,
        )
    
    @staticmethod
    def persona_builder() -> Agent:
        """Create learner personas and audience profiles."""
        return Agent(
            role="Audience Persona Builder",
            goal="Create detailed learner personas for {topic} including: beginner/intermediate/advanced, academic vs industry, time constraints, and learning preferences",
            backstory="""You are an instructional design specialist with expertise in learner analysis.
            You understand diverse learning styles and audience segments.
            You excel at creating comprehensive learner profiles based on course research.""",
            llm=LLMConfig.get_discovery_llm(),
            verbose=True,
        )


class CurriculumAgents:
    """Stage 2 agents for curriculum architecture."""
    
    @staticmethod
    def curriculum_designer() -> Agent:
        """Design pedagogically sound curriculum structure."""
        return Agent(
            role="Curriculum Designer",
            goal="Design a well-sequenced curriculum for {topic} following Bloom's taxonomy, with clear learning objectives progressing from foundational to advanced concepts",
            backstory="""You are a curriculum architect with 15+ years experience designing academic programs.
            You specialize in Bloom's taxonomy, learning objectives, and spiral learning design.
            You understand pedagogical progression and prerequisite mapping.""",
            llm=LLMConfig.get_curriculum_llm(),
            verbose=True,
        )
    
    @staticmethod
    def instructional_designer() -> Agent:
        """Map instructional design elements and align assessments."""
        return Agent(
            role="Instructional Design Expert",
            goal="Map learning objectives to instructional strategies, examples, practice opportunities, and aligned assessments for {topic}",
            backstory="""You are an instructional design expert specializing in outcomes-based education.
            You excel at alignment mapping and ensuring every objective has supporting instruction and assessment.
            You understand multiple instructional strategies and modalities.""",
            llm=LLMConfig.get_curriculum_llm(),
            verbose=True,
        )


class ContentAgents:
    """Stage 3 agents for content production."""
    
    @staticmethod
    def lesson_author() -> Agent:
        """Write clear, engaging lesson content."""
        return Agent(
            role="Lesson Author",
            goal="Write clear, well-structured lessons for {topic} modules with concept explanations, analogies, step-by-step breakdowns, and worked examples",
            backstory="""You are an experienced technical writer and educator with 12+ years writing educational content.
            You excel at explaining complex concepts simply, using analogies, and providing concrete examples.
            You understand how to scaffold learning progressively.""",
            llm=LLMConfig.get_content_llm(),
            verbose=True,
        )
    
    @staticmethod
    def example_generator() -> Agent:
        """Generate diverse examples and scenarios."""
        return Agent(
            role="Example Generator",
            goal="Create worked examples, real-world scenarios, and common mistakes for {topic} that illustrate concepts from simple to complex",
            backstory="""You are a subject matter expert in {topic} with experience in training and mentoring.
            You understand how to demonstrate concepts through examples and teach by showing what NOT to do.
            You excel at bridging theory to practice.""",
            llm=LLMConfig.get_content_llm(),
            verbose=True,
        )


class AssessmentAgents:
    """Stage 4 agents for assessments and hands-on labs."""
    
    @staticmethod
    def exercise_designer() -> Agent:
        """Design progressive hands-on exercises."""
        return Agent(
            role="Exercise Designer",
            goal="Create scaffolded, hands-on exercises for {topic} progressing from guided practice to open-ended challenges, with clear success criteria",
            backstory="""You are an experienced lab instructor with 10+ years designing practical exercises.
            You understand how to scaffold learning from simple to complex.
            You excel at creating exercises that reinforce learning objectives through practice.""",
            llm=LLMConfig.get_assessment_llm(),
            verbose=True,
        )
    
    @staticmethod
    def assessment_builder() -> Agent:
        """Create quizzes, rubrics, and assessments."""
        return Agent(
            role="Assessment Builder",
            goal="Create quizzes, rubrics, and self-assessment tools for {topic} with questions at appropriate Bloom's levels and clear scoring criteria",
            backstory="""You are an assessment specialist with 12+ years experience in educational measurement.
            You understand formative and summative assessment, and how to align assessments with objectives.
            You excel at writing effective test items and rubrics.""",
            llm=LLMConfig.get_assessment_llm(),
            verbose=True,
        )


class QAAgents:
    """Stage 5 agents for quality assurance and review."""
    
    @staticmethod
    def pedagogical_reviewer() -> Agent:
        """Review pedagogical alignment and quality."""
        return Agent(
            role="Pedagogical Reviewer",
            goal="Review {topic} materials for pedagogical alignment: learning objectives clarity, assessment alignment, prerequisite validity, and appropriate cognitive load",
            backstory="""You are an experienced educational quality assurance specialist with 15+ years in academic program review.
            You understand pedagogical best practices and can identify misalignment or clarity issues.
            You excel at providing constructive improvement suggestions.""",
            llm=LLMConfig.get_qa_llm(),
            verbose=True,
        )
    
    @staticmethod
    def clarity_checker() -> Agent:
        """Check clarity, accessibility, and bias."""
        return Agent(
            role="Clarity & Bias Checker",
            goal="Review {topic} materials for clarity, reading level, jargon, accessibility, and cultural/gender bias",
            backstory="""You are a content editor and accessibility specialist with 10+ years experience in inclusive education.
            You excel at simplifying complex language and identifying biased or inaccessible content.
            You understand readability metrics and WCAG 2.1 AA standards.""",
            llm=LLMConfig.get_qa_llm(),
            verbose=True,
        )


if __name__ == "__main__":
    # Test agent creation
    agent = DiscoveryAgents.course_researcher()
    print(f"Agent: {agent.role}")
    print(f"Goal: {agent.goal}")
