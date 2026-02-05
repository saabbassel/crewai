from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from write_a_book_with_flows.types import CurriculumOutline, Section


@CrewBase
class OutlineCrew:
    """Outline Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = LLM(model="ollama/mistral", base_url="http://localhost:11434")

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def curriculum_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["curriculum_designer"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def research_topic(self) -> Task:
        return Task(
            config=self.tasks_config["research_topic"],
        )

    @task
    def design_curriculum(self) -> Task:
        return Task(
            config=self.tasks_config["design_curriculum"], output_pydantic=CurriculumOutline
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Outline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


@CrewBase
class ContentCrew:
    """Content Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = LLM(model="ollama/mistral", base_url="http://localhost:11434")

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["content_writer"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def write_section(self) -> Task:
        return Task(config=self.tasks_config["write_section"], output_pydantic=Section)

    @crew
    def crew(self) -> Crew:
        """Creates the Content Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )