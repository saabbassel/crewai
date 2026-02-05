# Installation
- install ollama
brew install ollama

# prompet
enhance the following prompt to generate a crew python application
The application should be able to generate learning materials to be used for courses

Prompt:
using the example application, I want to update the agents and tasks to search and design learning materials for a given topic passed a parameter, on a given level (beginner, meduim, expert) passed a parameter, optional URL List parameter could be provided 
The agent will be following crewai agent yaml schema as in config folder
the first step is to generate the course outlines/sections as 3-10 polted points.
The outline will be generated as md file  saved in a generted folder named as the topic name, and the flow showud wait for human in the loop response, the response could be: 
1- exit: stop the flow
2- rejected: then the flow will start over. the response could contains additional instruction
3- approved: the flow will continue to genrate the text for each section
The section generation should save the generated text with all the used references in a md file under the course folder

## prompt chatgpt
Nice idea—this is a solid use case for CrewAI. Below is a **clean, enhanced, and production-ready prompt** you can directly use to generate a CrewAI Python application. I’ve clarified the flow, tightened the requirements, and made it unambiguous for agents + tasks while staying framework-friendly.

---

## Enhanced Prompt for Generating a CrewAI Learning Material Application

**Objective**
Create a Python application using **CrewAI** that automatically generates structured learning materials for educational courses.

---

### Application Overview

The application generates course content based on:

* **Topic** (required, string)
* **Learning level** (required, one of: `beginner`, `medium`, `expert`)
* **Optional URL list** (optional, list of reference URLs)

The system uses CrewAI agents defined via **YAML schemas** located in the `config/` folder.

---

### Agent & Task Requirements

* All agents must follow the **CrewAI agent YAML schema**
* Tasks must be modular and reusable
* Agents may perform:

  * Web research
  * Content design
  * Outline structuring
  * Section-level content generation
  * Reference extraction and citation

---

### Workflow Steps

#### 1. Course Outline Generation

* The first task generates a **course outline** for the given topic and level
* The outline must contain **3–10 bullet-point sections**
* Output format: **Markdown (`.md`)**
* Save location:

  ```
  generated/<topic_name>/outline.md
  ```

---

#### 2. Human-in-the-Loop Approval Gate

After the outline is generated, the system **pauses execution** and waits for human feedback.

The human response can be one of the following:

1. **`exit`**

   * Terminates the workflow immediately

2. **`rejected`**

   * Restarts the outline generation step
   * May include **additional instructions or constraints** that must be applied in the next attempt

3. **`approved`**

   * Continues the workflow to full content generation

---

#### 3. Section Content Generation

* For each approved outline section:

  * Generate detailed instructional content appropriate to the selected learning level
  * Incorporate knowledge from:

    * Agent research
    * Optional provided URLs
    * Credible external references (if needed)
* Each section must include a **References** subsection listing all sources used

---

#### 4. Content Storage

* Each section is saved as a separate Markdown file:

  ```
  generated/<topic_name>/<section_name>.md
  ```
* Files must include:

  * Section title
  * Well-structured educational content
  * Reference list with URLs or citations

---

### Additional Constraints

* Use clear, pedagogical language appropriate for the selected learning level
* Maintain consistent Markdown formatting
* Folder and file names must be filesystem-safe
* The application must be easily extensible for additional agents or steps

---

### Expected Outcome

A fully functional CrewAI-based Python application that:

* Generates structured, reviewable course outlines
* Supports human approval before content expansion
* Produces high-quality, reference-backed learning materials in Markdown format

---

If you want, I can also:

* Convert this into **agent/task YAML files**
* Generate a **CrewAI flow diagram**
* Write a **starter Python project structure**
* Optimize it for **RAG or vector DB integration**

## gemini
This is a great use case for CrewAI! You're essentially building an **Automated Instructional Designer**. To get the best results from an LLM, the prompt needs to be more structured, defining the specific responsibilities of the agents and the technical architecture of the "Human-in-the-Loop" (HITL) flow.

Here is an enhanced, "pro-grade" version of your prompt that you can feed into an LLM to generate the Python application.

---

## Enhanced Prompt for CrewAI Learning Material Generator

**Goal:** Create a CrewAI Python application that generates structured learning materials based on a **Topic**, **Difficulty Level**, and optional **Source URLs**.

### 1. Technical Requirements

* **Framework:** Use `crewai` and `crewai[tools]`.
* **Configuration:** Agent and Task definitions must be stored in `src/project_name/config/agents.yaml` and `tasks.yaml`.
* **State Management:** Implement a **CrewAI Flow** to handle the logic between the outline generation and the content expansion.
* **Input Parameters:** `topic` (string), `level` (Beginner, Intermediate, Expert), and `urls` (optional list of strings).

### 2. Agent Definitions (YAML Schema)

* **The Researcher:** Specialized in deep-diving into the `topic` and `urls`. Their goal is to find high-authority references and ensure technical accuracy for the specific `level`.
* **The Curriculum Designer:** Responsible for taking research and structuring it into a 3-10 point logical outline.
* **The Content Writer:** Responsible for expanding each outline point into a comprehensive, Markdown-formatted lesson with citations.

### 3. Task Workflow & Human-in-the-Loop Logic

* **Task 1: Outline Generation**
* Create a folder named after the `topic`.
* Generate a `course_outline.md` file within that folder.
* **Logic Gate (HITL):** The application must pause and prompt the user for input.
* If **"exit"**: Terminate the flow.
* If **"rejected"**: Capture the user's feedback/instructions and restart the Outline Generation task.
* If **"approved"**: Proceed to Task 2.

* **Task 2: Section Expansion**
* Iterate through each outline point.
* Generate detailed content and a "References" section for each.
* Save each section as an individual Markdown file (e.g., `01_introduction.md`) inside the topic folder.

### 4. Code Structure Request

Please generate:

1. `agents.yaml` and `tasks.yaml` with detailed backstories and descriptions.
2. `crew.py` to initialize the agents and tasks.
3. `main.py` using **CrewAI Flows** to manage the state, the HITL prompt, and the directory creation logic.

* Generates structured, reviewable course outlines
* Supports human approval before content expansion
* Produces high-quality, reference-backed learning materials in Markdown format

# example
for the project structure use simmlar structure as in the github repo
https://github.com/crewAIInc/crewAI-examples

the generated project should saved under educational_materials
---

### Why this version works better:

* **Specificity:** It explicitly mentions **CrewAI Flows**, which is the modern way to handle "If/Then" logic and loops in CrewAI.
* **Separation of Concerns:** By defining the Researcher vs. Designer vs. Writer, you ensure the content isn't just a generic summary but a structured educational journey.
* **File I/O:** It clarifies exactly where and how files should be saved, preventing the code from just printing to the console.

> [!TIP]
> When you run this, make sure your environment variables for your LLM (like `OPENAI_API_KEY`) are set, as the Researcher agent will likely need a search tool (like SerperDev) to handle those URL parameters effectively.

**Would you like me to generate the actual Python code for the `main.py` flow logic based on this prompt?**



# Write a Book Flow

Welcome to the Book Writing Flow, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Overview

This flow will guide you through the process of writing a book by leveraging multiple AI agents, each with specific roles. Here's a brief overview of what will happen in this flow:

1. **Generate Book Outline**: The flow starts by using the `OutlineCrew` to create a comprehensive outline for your book. This crew will search the internet, define the structure, and main topics of the book based on the provided goal and topic.

2. **Write Book Chapters**: Once the outline is ready, the flow will kick off a new crew, `WriteBookChapterCrew`, for each chapter outlined in the previous step. Each crew will be responsible for writing a specific chapter, ensuring that the content is detailed and coherent.

3. **Join and Save Chapters**: In the final step, the flow will combine all the chapters into a single markdown file, creating a complete book. This file will be saved in the root folder of your project.

By following this flow, you can efficiently produce a well-structured and comprehensive book, leveraging the power of multiple AI agents to handle different aspects of the writing process.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. First, if you haven't already, install CrewAI:

```bash
pip install crewai==0.130.0
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:

```bash
crewai install
```

### Customizing & Dependencies

**Add your `OPENAI_API_KEY` into the `.env` file**  
**Add your `SERPER_API_KEY` into the `.env` file**

To customize the behavior of the book writing flow, you can update the agents and tasks defined in the `OutlineCrew` and `WriteBookChapterCrew`. If you want to adjust the flow itself, you will need to modify the flow in `main.py`.

- **Agents and Tasks**: Modify `src/write_a_book_with_flows/config/agents.yaml` to define your agents and `src/write_a_book_with_flows/config/tasks.yaml` to define your tasks. This is where you can customize how the book outline is generated and how chapters are written.

- **Flow Adjustments**: Modify `src/write_a_book_with_flows/main.py` to adjust the flow. This is where you can change how the flow orchestrates the different crews and tasks.

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai flow kickoff
```

This command initializes the write_a_book_with_flows Crew, assembling the agents and assigning them tasks as defined in your configuration.

When you kickstart the flow, it will orchestrate multiple crews to perform the tasks. The flow will first generate a book outline, then create and run a crew for each chapter, and finally join all the chapters into a single markdown file.

## Understanding Your Flow

The write_a_book_with_flows Flow is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your flow.

### Flow Structure

1. **OutlineCrew**: This crew is responsible for generating the book outline. It defines the structure and main topics of the book based on the provided goal and topic.

2. **WriteBookChapterCrew**: For each chapter outlined by the `OutlineCrew`, a new `WriteBookChapterCrew` is created. Each of these crews is responsible for writing a specific chapter, ensuring detailed and coherent content.

3. **Join and Save**: After all chapters are written, the flow combines them into a single markdown file, creating a complete book.

By understanding the flow structure, you can see how multiple crews are orchestrated to work together, each handling a specific part of the book writing process. This modular approach allows for efficient and scalable book production.

## Support

For support, questions, or feedback regarding the {{crew_name}} Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

# Instructional design
The CrewAI application for generating structured learning materials has been created. Here's a summary of the implementation:

Generated Files and Structure
agents.yaml - Defines three agents:

Researcher: Gathers high-authority information for the specified topic and difficulty level
Curriculum Designer: Creates logical 3-10 point outlines
Content Writer: Expands outlines into comprehensive Markdown sections with citations
tasks.yaml - Defines three tasks:

research_topic: Gathers information using provided URLs and topic
design_curriculum: Structures research into an outline
write_section: Expands individual outline points into full content
types.py - Pydantic models for data structures:

OutlinePoint: Title and description for outline points
CurriculumOutline: List of outline points
Section: Title and content for generated sections
crew.py - Two CrewAI crews:

OutlineCrew: Handles research and curriculum design
ContentCrew: Handles content writing
main.py - CrewAI Flow implementation with HITL:

Task 1: Generates outline, creates topic folder, saves course_outline.md, prompts for approval
HITL Logic:
"approved": Proceeds to content generation
"rejected <feedback>": Currently logs feedback (can be extended for restart)
"exit": Terminates
Task 2: Generates individual Markdown files for each section (e.g., 01_introduction.md)

Usage
Run the application with command-line arguments:
python -m write_a_book_with_flows.main "Machine Learning Basics" Beginner --urls "https://example.com/ml-intro" "https://example.com/ml-concepts"
Or using the script entry point:
generate "Machine Learning Basics" Beginner --urls "https://example.com/ml-intro"
The application creates a folder named after the topic (filesystem-safe), generates the outline for review, and upon approval, produces detailed learning material sections with proper Markdown formatting and references.


python3 -m main.py "AZURE FUNDAMANTALS" Beginner --urls "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/?practice-assessment-type=certification" "https://learn.microsoft.com/en-us/training/paths/prepare-teach-az-900-microsoft-academic-programs/" 

/Users/b.saab/repos/.venv/bin/python -u -m src.educational_materials.main "AZURE FUNDAMENTALS" Beginner --urls "https://learn.microsoft.com/"

