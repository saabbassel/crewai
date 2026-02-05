#!/usr/bin/env python
import asyncio
from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from write_a_book_with_flows.crew import OutlineCrew, ContentCrew
from write_a_book_with_flows.types import OutlinePoint, Section


class LearningMaterialState(BaseModel):
    topic: str
    level: str  # Beginner, Intermediate, Expert
    urls: List[str] = []
    outline: List[OutlinePoint] = []
    sections: List[Section] = []
    folder_path: str = ""


class LearningMaterialFlow(Flow[LearningMaterialState]):

    @start()
    def generate_outline(self):
        print("Generating Course Outline")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "level": self.state.level, "urls": self.state.urls})
        )

        outline = output["points"]
        print("Outline Points:", outline)

        # Create folder
        import os
        safe_topic = self.state.topic.replace(' ', '_').replace('/', '_')
        self.state.folder_path = f"./{safe_topic}"
        os.makedirs(self.state.folder_path, exist_ok=True)

        # Save course_outline.md
        outline_content = f"# {self.state.topic} - {self.state.level} Level\n\n"
        for i, point in enumerate(outline, 1):
            outline_content += f"{i}. **{point.title}**\n   {point.description}\n\n"

        with open(f"{self.state.folder_path}/course_outline.md", "w") as f:
            f.write(outline_content)

        self.state.outline = outline

        # HITL
        print("Outline generated. Please review course_outline.md")
        user_input = input("Enter 'approved' to proceed, 'rejected <feedback>' to restart, or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Exiting.")
            return None
        elif user_input.lower().startswith('rejected'):
            feedback = user_input[8:].strip()
            print(f"Restarting with feedback: {feedback}")
            # Restart, perhaps by calling again, but for simplicity, raise or something
            # Since flow, perhaps return and listen handles
            self.state.outline = []
            return "restart"
        else:
            print("Proceeding to content generation.")
            return outline
    @listen(generate_outline)
    async def write_sections(self, outline):
        if outline is None or outline == "restart":
            return
        print("Writing Sections")
        tasks = []

        async def write_single_section(point):
            output = (
                ContentCrew()
                .crew()
                .kickoff(
                    inputs={
                        "topic": self.state.topic,
                        "level": self.state.level,
                        "section_title": point.title,
                        "section_description": point.description,
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            section = Section(title=title, content=content)
            return section

        for point in self.state.outline:
            print(f"Writing Section: {point.title}")
            task = asyncio.create_task(write_single_section(point))
            tasks.append(task)

        sections = await asyncio.gather(*tasks)
        print("Newly generated sections:", sections)
        self.state.sections.extend(sections)

        # Save each section
        for i, section in enumerate(sections, 1):
            filename = f"{self.state.folder_path}/{i:02d}_{section.title.replace(' ', '_').lower()}.md"
            with open(filename, "w") as f:
                f.write(f"# {section.title}\n\n{section.content}")

        print("Sections saved.")


def kickoff(topic: str, level: str, urls: List[str] = []):
    state = LearningMaterialState(topic=topic, level=level, urls=urls)
    flow = LearningMaterialFlow(state=state)
    flow.kickoff()


def plot():
    flow = LearningMaterialFlow()
    flow.plot()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate learning materials")
    parser.add_argument("topic", help="The topic for the learning material")
    parser.add_argument("level", choices=["Beginner", "Intermediate", "Expert"], help="Difficulty level")
    parser.add_argument("--urls", nargs="*", default=[], help="Optional source URLs")
    args = parser.parse_args()
    kickoff(args.topic, args.level, args.urls)
