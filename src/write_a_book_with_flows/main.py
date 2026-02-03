#!/usr/bin/env python
import asyncio
from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from write_a_book_with_flows.crews.write_book_chapter_crew.write_book_chapter_crew import (
    WriteBookChapterCrew,
)
from write_a_book_with_flows.types import Section, SectionOutline

from write_a_book_with_flows.crews.outline_book_crew.outline_crew import OutlineCrew


class LearningMaterialState(BaseModel):
    id: str = "1"
    title: str = "Learn AZ-900 Microsoft Azure fundamentals" # "The Current State of AI in July 2025"
    learning_material: List[Section] = []
    learning_material_outline: List[SectionOutline] = []
    topic: str = (
        "Exploring the latest trends in AI across different industries as of July 2025"
    )
    goal: str = """
        The goal of this learning material is to provide a comprehensive overview of the current state of artificial intelligence in July 2025.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The learning material aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """


class LearningMaterialFlow(Flow[LearningMaterialState]):
    initial_state = LearningMaterialState

    @start()
    def generate_learning_material_outline(self):
        print("Kickoff the Learning Material Outline Crew")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "goal": self.state.goal})
        )

        sections = output["sections"]
        print("Sections:", sections)

        self.state.learning_material_outline = sections
        return sections

    @listen(generate_learning_material_outline)
    async def write_sections(self):
        print("Writing Learning Material Sections")
        tasks = []

        async def write_single_section(section_outline):
            output = (
                WriteBookChapterCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": section_outline.title,
                        "chapter_description": section_outline.description,
                        "book_outline": [
                            section_outline.model_dump_json()
                            for section_outline in self.state.learning_material_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            section = Section(title=title, content=content)
            return section

        for section_outline in self.state.learning_material_outline:
            print(f"Writing Section: {section_outline.title}")
            print(f"Description: {section_outline.description}")
            # Schedule each section writing task
            task = asyncio.create_task(write_single_section(section_outline))
            tasks.append(task)

        # Await all section writing tasks concurrently
        sections = await asyncio.gather(*tasks)
        print("Newly generated sections:", sections)
        self.state.learning_material.extend(sections)

        print("Learning Material Sections", self.state.learning_material)

    @listen(write_sections)
    async def join_and_save_section(self):
        print("Joining and Saving Learning Material Sections")
        # Combine all sections into a single markdown string
        learning_material_content = ""

        for section in self.state.learning_material:
            # Add the section title as an H1 heading
            learning_material_content += f"# {section.title}\n\n"
            # Add the section content
            learning_material_content += f"{section.content}\n\n"

        # The title of the learning material from self.state.title
        learning_material_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        filename = f"./{learning_material_title.replace(' ', '_')}.md"

        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(learning_material_content)

        print(f"Learning Material saved as {filename}")
        return learning_material_content


def kickoff():
    learning_material_flow = LearningMaterialFlow()
    learning_material_flow.kickoff()


def plot():
    learning_material_flow = LearningMaterialFlow()
    learning_material_flow.plot()


if __name__ == "__main__":
    kickoff()
