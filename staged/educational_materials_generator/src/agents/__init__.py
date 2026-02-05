"""Agents for educational materials generation across 5 stages.

This module loads agent configurations from YAML files in the config/ directory:
- config/agents_stage1.yaml - Discovery agents
- config/agents_stage2.yaml - Curriculum agents
- config/agents_stage3.yaml - Content agents
- config/agents_stage4.yaml - Assessment agents
- config/agents_stage5.yaml - QA agents

Each agent is configured with:
- Specialized role, goal, and backstory
- Stage-specific LLM with optimized temperature
- Standardization prompts injected into agent instructions
"""

from crewai import Agent, LLM
from src.config import LLMConfig, Config
from src.config_loader import ConfigLoader


# ====================================
# Stage 1: Discovery & Benchmarking
# ====================================

class DiscoveryAgents:
    """Stage 1 agents for research and course benchmarking.
    
    Goal: Analyze existing courses and create research dossier
    Key Activities:
    - Search major platforms (Coursera, Udemy, edX, YouTube)
    - Identify module structures and learning patterns
    - Extract common skills and gaps
    - Build learner personas
    
    Output: ResearchDossier with courses, skills, and personas
    Temperature: 0.7 (balanced analysis + creativity)
    
    Loads configurations from: config/agents_stage1.yaml
    """
    
    @staticmethod
    def _create_agent_from_config(agent_config: dict) -> Agent:
        """Create an Agent from YAML configuration.
        
        Args:
            agent_config: Agent configuration dictionary from YAML
            
        Returns:
            Configured Agent instance
        """
        model_key = agent_config.get('model_key', 'DISCOVERY_MODEL')
        
        if model_key == 'DISCOVERY_MODEL':
            llm = LLMConfig.get_discovery_llm()
        elif model_key == 'CURRICULUM_MODEL':
            llm = LLMConfig.get_curriculum_llm()
        elif model_key == 'CONTENT_MODEL':
            llm = LLMConfig.get_content_llm()
        elif model_key == 'ASSESSMENT_MODEL':
            llm = LLMConfig.get_assessment_llm()
        elif model_key == 'QA_MODEL':
            llm = LLMConfig.get_qa_llm()
        else:
            llm = LLMConfig.get_discovery_llm()
        
        return Agent(
            role=agent_config.get('role'),
            goal=agent_config.get('goal'),
            backstory=agent_config.get('backstory'),
            llm=llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False),
            cache=Config.CACHE_RESPONSES if agent_config.get('cache', True) else False,
        )
    
    @staticmethod
    def course_researcher() -> Agent:
        """Research existing courses and extract patterns."""
        config = ConfigLoader.get_agent_config(1, 'course_researcher')
        return DiscoveryAgents._create_agent_from_config(config)
    
    @staticmethod
    def trends_analyst() -> Agent:
        """Identify skills trends and gaps in market."""
        config = ConfigLoader.get_agent_config(1, 'trends_analyst')
        return DiscoveryAgents._create_agent_from_config(config)
    
    @staticmethod
    def persona_builder() -> Agent:
        """Create learner personas and audience profiles."""
        config = ConfigLoader.get_agent_config(1, 'persona_builder')
        return DiscoveryAgents._create_agent_from_config(config)


# ====================================
# Stage 2: Curriculum Architecture
# ====================================

class CurriculumAgents:
    """Stage 2 agents for curriculum architecture.
    
    Goal: Design pedagogically sound curriculum structure
    Key Activities:
    - Map learning objectives using Bloom's taxonomy
    - Design module sequencing and prerequisites
    - Define assessment strategies
    - Plan instruction strategies per module
    
    Output: CurriculumBlueprint with modules, objectives, duration
    Temperature: 0.6 (structured, consistent curriculum design)
    
    Loads configurations from: config/agents_stage2.yaml
    """
    
    @staticmethod
    def curriculum_designer() -> Agent:
        """Design pedagogically sound curriculum structure."""
        config = ConfigLoader.get_agent_config(2, 'curriculum_designer')
        return CurriculumAgents._create_agent_from_config(config)
    
    @staticmethod
    def _create_agent_from_config(agent_config: dict) -> Agent:
        """Create an Agent from YAML configuration."""
        model_key = agent_config.get('model_key', 'CURRICULUM_MODEL')
        
        if model_key == 'CURRICULUM_MODEL':
            llm = LLMConfig.get_curriculum_llm()
        elif model_key == 'CONTENT_MODEL':
            llm = LLMConfig.get_content_llm()
        elif model_key == 'ASSESSMENT_MODEL':
            llm = LLMConfig.get_assessment_llm()
        elif model_key == 'QA_MODEL':
            llm = LLMConfig.get_qa_llm()
        else:
            llm = LLMConfig.get_curriculum_llm()
        
        return Agent(
            role=agent_config.get('role'),
            goal=agent_config.get('goal'),
            backstory=agent_config.get('backstory'),
            llm=llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False),
            cache=Config.CACHE_RESPONSES if agent_config.get('cache', True) else False,
        )
    
    @staticmethod
    def instructional_designer() -> Agent:
        """Map instructional design elements and align assessments."""
        config = ConfigLoader.get_agent_config(2, 'instructional_designer')
        return CurriculumAgents._create_agent_from_config(config)


# ====================================
# Stage 3: Content Production
# ====================================

class ContentAgents:
    """Stage 3 agents for content production.
    
    Goal: Generate lesson content, examples, and handouts
    Key Activities:
    - Write clear lesson explanations
    - Create worked examples and scenarios
    - Develop handout materials
    - Generate learning variants
    
    Output: ContentMaterial with lessons, examples, handouts (MD)
    Temperature: 0.8 (creative, varied writing styles + clarity)
    
    Loads configurations from: config/agents_stage3.yaml
    """
    
    @staticmethod
    def lesson_author() -> Agent:
        """Write clear, engaging lesson content."""
        config = ConfigLoader.get_agent_config(3, 'lesson_author')
        return ContentAgents._create_agent_from_config(config)
    
    @staticmethod
    def _create_agent_from_config(agent_config: dict) -> Agent:
        """Create an Agent from YAML configuration."""
        model_key = agent_config.get('model_key', 'CONTENT_MODEL')
        
        if model_key == 'CONTENT_MODEL':
            llm = LLMConfig.get_content_llm()
        elif model_key == 'ASSESSMENT_MODEL':
            llm = LLMConfig.get_assessment_llm()
        elif model_key == 'QA_MODEL':
            llm = LLMConfig.get_qa_llm()
        else:
            llm = LLMConfig.get_content_llm()
        
        return Agent(
            role=agent_config.get('role'),
            goal=agent_config.get('goal'),
            backstory=agent_config.get('backstory'),
            llm=llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False),
            cache=Config.CACHE_RESPONSES if agent_config.get('cache', True) else False,
        )
    
    @staticmethod
    def example_generator() -> Agent:
        """Generate diverse examples and scenarios."""
        config = ConfigLoader.get_agent_config(3, 'example_generator')
        return ContentAgents._create_agent_from_config(config)


# ====================================
# Stage 4: Assessment & Hands-On
# ====================================

class AssessmentAgents:
    """Stage 4 agents for assessments and hands-on labs.
    
    Goal: Create exercises, quizzes, and project specifications
    Key Activities:
    - Design scaffolded exercises
    - Create assessment items at appropriate Bloom's levels
    - Build project specifications
    - Develop rubrics and success criteria
    
    Output: Assessment with exercises, quizzes, projects, labs (JSON)
    Temperature: 0.7 (balanced assessment rigor + creativity)
    
    Loads configurations from: config/agents_stage4.yaml
    """
    
    @staticmethod
    def exercise_designer() -> Agent:
        """Design progressive hands-on exercises."""
        config = ConfigLoader.get_agent_config(4, 'exercise_designer')
        return AssessmentAgents._create_agent_from_config(config)
    
    @staticmethod
    def _create_agent_from_config(agent_config: dict) -> Agent:
        """Create an Agent from YAML configuration."""
        model_key = agent_config.get('model_key', 'ASSESSMENT_MODEL')
        
        if model_key == 'ASSESSMENT_MODEL':
            llm = LLMConfig.get_assessment_llm()
        elif model_key == 'QA_MODEL':
            llm = LLMConfig.get_qa_llm()
        else:
            llm = LLMConfig.get_assessment_llm()
        
        return Agent(
            role=agent_config.get('role'),
            goal=agent_config.get('goal'),
            backstory=agent_config.get('backstory'),
            llm=llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False),
            cache=Config.CACHE_RESPONSES if agent_config.get('cache', True) else False,
        )
    
    @staticmethod
    def assessment_builder() -> Agent:
        """Create quizzes, rubrics, and assessments."""
        config = ConfigLoader.get_agent_config(4, 'assessment_builder')
        return AssessmentAgents._create_agent_from_config(config)


# ====================================
# Stage 5: Quality Assurance & Review
# ====================================

class QAAgents:
    """Stage 5 agents for quality assurance and review.
    
    Goal: Review and validate all generated materials
    Key Activities:
    - Check pedagogical alignment
    - Verify clarity and accessibility
    - Validate schema and formats
    - Audit consistency across stages
    
    Output: QAReport with issues and recommendations
    Temperature: 0.5 (consistent, rigorous QA review)
    
    Loads configurations from: config/agents_stage5.yaml
    """
    
    @staticmethod
    def pedagogical_reviewer() -> Agent:
        """Review pedagogical alignment and quality."""
        config = ConfigLoader.get_agent_config(5, 'pedagogical_reviewer')
        return QAAgents._create_agent_from_config(config)
    
    @staticmethod
    def _create_agent_from_config(agent_config: dict) -> Agent:
        """Create an Agent from YAML configuration."""
        model_key = agent_config.get('model_key', 'QA_MODEL')
        llm = LLMConfig.get_qa_llm()
        
        return Agent(
            role=agent_config.get('role'),
            goal=agent_config.get('goal'),
            backstory=agent_config.get('backstory'),
            llm=llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False),
            cache=Config.CACHE_RESPONSES if agent_config.get('cache', True) else False,
        )
    
    @staticmethod
    def clarity_checker() -> Agent:
        """Check clarity, accessibility, and bias."""
        config = ConfigLoader.get_agent_config(5, 'clarity_checker')
        return QAAgents._create_agent_from_config(config)


# ====================================
# Agent Factory Functions
# ====================================

def get_stage_agents(stage: int) -> list[Agent]:
    """Get all agents for a specific stage.
    
    Args:
        stage: Stage number (1-5)
        
    Returns:
        List of Agent instances for the stage
    """
    if stage == 1:
        return [
            DiscoveryAgents.course_researcher(),
            DiscoveryAgents.trends_analyst(),
            DiscoveryAgents.persona_builder(),
        ]
    elif stage == 2:
        return [
            CurriculumAgents.curriculum_designer(),
            CurriculumAgents.instructional_designer(),
        ]
    elif stage == 3:
        return [
            ContentAgents.lesson_author(),
            ContentAgents.example_generator(),
        ]
    elif stage == 4:
        return [
            AssessmentAgents.exercise_designer(),
            AssessmentAgents.assessment_builder(),
        ]
    elif stage == 5:
        return [
            QAAgents.pedagogical_reviewer(),
            QAAgents.clarity_checker(),
        ]
    else:
        raise ValueError(f"Invalid stage: {stage}. Must be 1-5.")


def get_all_agents() -> dict:
    """Get all agents organized by stage.
    
    Returns:
        Dictionary with agents grouped by stage
    """
    return {
        "stage_1_discovery": [
            DiscoveryAgents.course_researcher(),
            DiscoveryAgents.trends_analyst(),
            DiscoveryAgents.persona_builder(),
        ],
        "stage_2_curriculum": [
            CurriculumAgents.curriculum_designer(),
            CurriculumAgents.instructional_designer(),
        ],
        "stage_3_content": [
            ContentAgents.lesson_author(),
            ContentAgents.example_generator(),
        ],
        "stage_4_assessment": [
            AssessmentAgents.exercise_designer(),
            AssessmentAgents.assessment_builder(),
        ],
        "stage_5_qa": [
            QAAgents.pedagogical_reviewer(),
            QAAgents.clarity_checker(),
        ],
    }


if __name__ == "__main__":
    # Test agent creation and display info
    print("=" * 80)
    print("EDUCATIONAL MATERIALS GENERATOR - AGENT SUMMARY")
    print("=" * 80)
    
    all_agents = get_all_agents()
    
    for stage_name, agents in all_agents.items():
        stage_num = stage_name.split("_")[1]
        print(f"\n📍 STAGE {stage_num}: {stage_name.upper()}")
        print("-" * 80)
        
        for agent in agents:
            print(f"\n  🤖 {agent.role}")
            print(f"     Goal: {agent.goal[:70]}...")
            if hasattr(agent, 'llm') and agent.llm:
                print(f"     LLM: {agent.llm.model if hasattr(agent.llm, 'model') else 'configured'}")
    
    print("\n" + "=" * 80)
    print("✅ All agents initialized successfully")
    print("=" * 80)
