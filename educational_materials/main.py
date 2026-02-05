#!/usr/bin/env python
import asyncio
import os
import re
from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from .crew import OutlineCrew, ContentCrew
from .models import OutlinePoint, Section


class LearningMaterialState(BaseModel):
    """State for the learning material generation flow."""
    topic: str = ""
    level: str = ""  # Beginner, Intermediate, Expert
    urls: List[str] = []
    outline: List[OutlinePoint] = []
    sections: List[Section] = []
    folder_path: str = ""
    feedback: str = ""


class LearningMaterialFlow(Flow[LearningMaterialState]):
    """Flow for generating structured learning materials."""

    @start()
    def generate_outline(self):
        """Generate course outline and prompt for human approval."""
        print("\n" + "="*70)
        print("STEP 1: CURRICULUM OUTLINE GENERATION")
        print("="*70)
        
        # Create topic folder
        safe_topic = self._make_filesystem_safe(self.state.topic)
        self.state.folder_path = f"./{safe_topic}"
        os.makedirs(self.state.folder_path, exist_ok=True)
        print(f"✓ Created folder: {self.state.folder_path}")

        # Generate outline using OutlineCrew
        print("\nKickoff the Outline Crew...")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "level": self.state.level,
                    "urls": ", ".join(self.state.urls) if self.state.urls else "No URLs provided",
                }
            )
        )

        # Parse the output into outline points (robust fallback parsing)
        import json
        output_str = str(output.raw if hasattr(output, 'raw') else output)
        outline_points = []

        # 1) If pydantic output available
        if hasattr(output, 'pydantic'):
            try:
                pts = getattr(output.pydantic, 'points', None)
                if pts:
                    outline_points = [OutlinePoint(title=p.title, description=p.description) for p in pts]
            except Exception:
                outline_points = []

        # 2) If direct dict-like
        if not outline_points and isinstance(output, dict):
            pts = output.get('points') or output.get('Points')
            if isinstance(pts, list):
                for p in pts:
                    if isinstance(p, dict):
                        outline_points.append(OutlinePoint(title=p.get('title',''), description=p.get('description','')))

        # 3) Try extracting JSON blob with points
        if not outline_points:
            json_match = re.search(r'\{\s*"points"\s*:\s*\[.*?\]\s*\}', output_str, re.DOTALL)
            if json_match:
                try:
                    json_data = json.loads(json_match.group())
                    pts = json_data.get('points', [])
                    for p in pts:
                        if isinstance(p, dict):
                            outline_points.append(OutlinePoint(title=p.get('title',''), description=p.get('description','')))
                except Exception:
                    outline_points = []

        # 4) Fallback: parse human-readable lists (titles and descriptions)
        if not outline_points:
            lines = [ln.strip() for ln in output_str.splitlines()]
            current = None
            desc_lines = []
            for ln in lines:
                if not ln:
                    continue
                # heading markers or numbered items
                m = re.match(r'^(?:#{2,}\s*)?(?:\d+\.|-\s|\*\s)?\s*(.+)$', ln)
                if m:
                    title = m.group(1).strip()
                    # if we already have a current, flush it
                    if current:
                        outline_points.append(OutlinePoint(title=current, description=' '.join(desc_lines).strip()))
                    current = title
                    desc_lines = []
                else:
                    desc_lines.append(ln)
            if current:
                outline_points.append(OutlinePoint(title=current, description=' '.join(desc_lines).strip()))

        print(f"✓ Generated {len(outline_points)} outline points")

        # Save course outline to markdown (fill topic and level)
        outline_content = self._generate_outline_markdown(outline_points)
        outline_file = f"{self.state.folder_path}/course_outline.md"
        with open(outline_file, "w") as f:
            f.write(outline_content)
        print(f"✓ Saved outline to: {outline_file}")

        # persist outline to state before human approval
        self.state.outline = outline_points

        # Display outline for review
        print("\n" + "-"*70)
        print("OUTLINE PREVIEW:")
        print("-"*70)
        print(outline_content)
        print("-"*70)

        # Human-in-the-loop gate
        return self._hitl_approval_gate()

    def _hitl_approval_gate(self):
        """Prompt user for approval, rejection, or exit."""
        print("\n" + "="*70)
        print("HUMAN-IN-THE-LOOP GATE")
        print("="*70)
        print("Options:")
        print("  1. 'approved'             - Proceed to content generation")
        print("  2. 'rejected <feedback>'  - Restart outline with feedback")
        print("  3. 'exit'                 - Terminate the flow")
        print("-"*70)

        while True:
            user_input = input("\nEnter your decision: ").strip().lower()

            if user_input == "exit":
                print("✗ Exiting flow.")
                return "exit"

            elif user_input.startswith("rejected"):
                feedback = user_input[8:].strip()
                self.state.feedback = feedback
                print(f"✓ Feedback captured: {feedback}")
                print("Restarting outline generation with feedback...")
                return "restart"

            elif user_input == "approved":
                print("✓ Outline approved. Proceeding to content generation...")
                return "approved"

            else:
                print("✗ Invalid input. Please enter 'approved', 'rejected <feedback>', or 'exit'.")

    @listen(generate_outline)
    def handle_outline_result(self, result):
        """Handle outline generation result."""
        if result == "exit":
            print("\n✓ Learning material generation cancelled.")
            return None
        elif result == "restart":
            print("\nRestarting outline generation with feedback...")
            return self.generate_outline()
        elif result == "approved":
            print("\nProceeding to content generation...")
            return self.state.outline  # Pass outline to next step
        return None

    @listen(handle_outline_result)
    async def generate_content(self, outline):
        """Generate detailed content for each outline point."""
        if not outline or outline is None:
            return

        # Handle cases where the listener provided a status string (e.g. 'approved')
        if isinstance(outline, str):
            if outline.lower() in ("approved", "restart", "exit"):
                outline = self.state.outline or []
            else:
                # single-title string -> treat as a single-item outline
                outline = [outline]

        # Normalize outline items into OutlinePoint instances
        normalized = []
        for item in outline:
            if isinstance(item, OutlinePoint):
                normalized.append(item)
            elif isinstance(item, dict):
                normalized.append(OutlinePoint(title=str(item.get('title','')).strip(), description=str(item.get('description','')).strip()))
            elif isinstance(item, str):
                # Treat the string as a title when only a title was provided
                normalized.append(OutlinePoint(title=item.strip(), description=""))
            else:
                # Fallback: try to extract attributes, else stringify
                title = getattr(item, 'title', None) or (item[0] if isinstance(item, (list, tuple)) and item else None)
                desc = getattr(item, 'description', None) or ''
                if title is None:
                    title = str(item)
                normalized.append(OutlinePoint(title=str(title).strip(), description=str(desc).strip()))

        outline = normalized

        print("\n" + "="*70)
        print("STEP 2: SECTION CONTENT GENERATION")
        print("="*70)
        print(f"Generating {len(outline)} sections...\n")

        tasks = []

        async def write_single_section(index: int, point: OutlinePoint):
            """Write a single section asynchronously."""
            print(f"Generating section {index}/{len(outline)}: {point.title}...")
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

            # Robustly extract content from various output shapes
            section = None
            try:
                # 1) pydantic output (already-validated Section)
                if hasattr(output, 'pydantic'):
                    section = output.pydantic
                    # if it's a dict-like pydantic output, coerce
                    if isinstance(section, dict):
                        section = Section(title=section.get('title', point.title), content=section.get('content', ''))

                # 2) dict-like output
                elif isinstance(output, dict):
                    title = output.get('title') or point.title
                    content = output.get('content') or output.get('body') or str(output)
                    section = Section(title=str(title).strip(), content=str(content))

                # 3) plain string output (markdown or JSON blob)
                elif isinstance(output, str):
                    import json as _json
                    # try to extract JSON object from the string
                    json_match = re.search(r'\{\s*"title".*\}', output, re.DOTALL)
                    if json_match:
                        try:
                            parsed = _json.loads(json_match.group())
                            title = parsed.get('title') or point.title
                            content = parsed.get('content') or parsed.get('body') or output
                            section = Section(title=str(title).strip(), content=str(content))
                        except Exception:
                            section = Section(title=point.title, content=output)
                    else:
                        section = Section(title=point.title, content=output)

                # 4) other objects (fall back to attributes or string)
                else:
                    title = getattr(output, 'title', None) or point.title
                    content = getattr(output, 'content', None) or (getattr(output, 'raw', None) if hasattr(output, 'raw') else str(output))
                    section = Section(title=str(title), content=str(content))

            except Exception as e:
                print(f"! Warning: failed to parse section output cleanly: {e}")
                section = Section(title=point.title, content=str(output))
            
            # Ensure section is always created, even if all parsing failed
            if section is None:
                section = Section(title=point.title, content=str(output))

            print(f"✓ Section {index} completed: {getattr(section, 'title', point.title)}")
            return section

        # Generate all sections concurrently
        for idx, point in enumerate(outline, 1):
            task = asyncio.create_task(write_single_section(idx, point))
            tasks.append(task)

        # Await tasks sequentially so we can capture per-task exceptions and results
        sections = []
        for t in tasks:
            try:
                res = await t
            except Exception as e:
                print(f"! Section task failed: {e}")
                res = None
            sections.append(res)

        # Extend state with only successful sections
        self.state.sections.extend([s for s in sections if s is not None])

        # Save each section to file
        print("\nSaving sections to files...")
        for idx, section in enumerate(sections, 1):
            if section is None:
                print(f"! Skipping section {idx}: None returned")
                continue
            filename = f"{self.state.folder_path}/{idx:02d}_{self._make_filesystem_safe(section.title)}.md"
            with open(filename, "w") as f:
                f.write(section.content)
            print(f"✓ Saved: {filename}")

        print("\n" + "="*70)
        print("LEARNING MATERIALS GENERATION COMPLETE!")
        print("="*70)
        print(f"✓ Generated {len(sections)} sections")
        print(f"✓ Location: {self.state.folder_path}")
        print("✓ Files created:")
        print(f"  - course_outline.md")
        #for idx, section in enumerate(sections, 1):
        #    print(f"  - {idx:02d}_{self._make_filesystem_safe(section.title)}.md")
        for idx, section in enumerate([s for s in sections if s is not None], 1):
            print(f"  - {idx:02d}_{self._make_filesystem_safe(section.title)}.md")
            print("="*70 + "\n")

    @staticmethod
    def _make_filesystem_safe(name: str) -> str:
        """Convert string to filesystem-safe format."""
        # Replace spaces with underscores
        name = name.replace(" ", "_")
        # Remove or replace invalid characters
        name = re.sub(r"[^\w\-._]", "", name)
        # Ensure it's not empty
        return name if name else "learning_material"

    def _generate_outline_markdown(self, points: List[OutlinePoint]) -> str:
        """Generate markdown content for the outline using the current state."""
        lines = []
        lines.append("# Course Outline\n")
        lines.append(f"**Topic:** {self.state.topic}\n")
        lines.append(f"**Difficulty Level:** {self.state.level}\n\n")
        lines.append("## Curriculum Structure\n")

        if not points:
            lines.append("(No outline points were parsed from the agent output.)\n")

        for idx, point in enumerate(points, 1):
            lines.append(f"### {idx}. {point.title}\n")
            if point.description:
                lines.append(f"{point.description}\n")

        return "\n".join(lines)


def kickoff(topic: str, level: str, urls: List[str] = None):
    """Kickoff the learning material generation flow."""
    if urls is None:
        urls = []

    print("\n" + "="*70)
    print("EDUCATIONAL MATERIALS GENERATOR - CrewAI")
    print("="*70)
    print(f"Topic: {topic}")
    print(f"Level: {level}")
    print(f"URLs: {urls if urls else 'None'}")
    print("="*70 + "\n")

    flow = LearningMaterialFlow()
    # Initialize the state with values
    flow.state.topic = topic
    flow.state.level = level
    flow.state.urls = urls
    flow.kickoff()


def plot():
    """Generate and display flow diagram."""
    flow = LearningMaterialFlow()
    flow.plot()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate structured learning materials using CrewAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Machine Learning Basics" Beginner
  python main.py "Azure Fundamentals" Beginner --urls "https://learn.microsoft.com/..." "https://example.com"
  python main.py "Advanced Python" Expert --urls "https://peps.python.org"
        """
    )

    parser.add_argument(
        "topic",
        help="The topic for the learning material"
    )
    parser.add_argument(
        "level",
        choices=["Beginner", "Intermediate", "Expert"],
        help="Difficulty level for the learners"
    )
    parser.add_argument(
        "--urls",
        nargs="*",
        default=[],
        help="Optional source URLs for research"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Display the flow diagram instead of running"
    )

    args = parser.parse_args()

    if args.plot:
        plot()
    else:
        kickoff(args.topic, args.level, args.urls)
