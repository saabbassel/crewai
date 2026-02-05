# Educational Materials Generator

A CrewAI-powered Python application that generates **structured, peer-reviewed learning materials** for educational courses.

## Overview

This tool leverages **multi-agent AI** to systematically create comprehensive course outlines and detailed lesson content based on:
- **Topic** (e.g., "Azure Fundamentals", "Machine Learning Basics")
- **Difficulty Level** (Beginner, Intermediate, Expert)
- **Optional Source URLs** for research grounding

### Key Features

✅ **Structured Curriculum Generation** - Creates logical 3-10 point outlines  
✅ **Human-in-the-Loop Approval** - Review and reject outlines with feedback  
✅ **Reference-Backed Content** - Each section includes citations and sources  
✅ **Markdown Output** - Professional, publication-ready course materials  
✅ **Asynchronous Processing** - Sections generated concurrently for speed  
✅ **Extensible Architecture** - Easily add new agents or tasks  

---

## Agent Architecture

The application uses three specialized agents, each with distinct responsibilities:

### 1. **Researcher**
- Deep-dives into the topic and provided URLs
- Identifies high-authority references
- Ensures technical accuracy for the specified difficulty level
- Extracts key concepts and real-world applications

### 2. **Curriculum Designer**
- Transforms research into a logical learning progression
- Creates 3-10 outline points appropriate for the difficulty level
- Structures content with proper pedagogical scaffolding
- Ensures each section builds on prior knowledge

### 3. **Content Writer**
- Expands outline points into comprehensive lessons (1000-2000 words each)
- Uses pedagogical techniques: definitions, analogies, examples, case studies
- Includes citations and a References section
- Maintains consistent Markdown formatting

---

## Workflow

### Phase 1: Outline Generation

```
USER INPUT (topic, level, urls)
    ↓
RESEARCHER → Gathers information and references
    ↓
CURRICULUM DESIGNER → Creates structured outline
    ↓
SAVE → course_outline.md
    ↓
HUMAN-IN-THE-LOOP GATE
    ├─ "approved" → Proceed to Phase 2
    ├─ "rejected <feedback>" → Regenerate outline
    └─ "exit" → Terminate flow
```

### Phase 2: Content Generation

```
APPROVED OUTLINE
    ↓
FOR EACH SECTION (asynchronous):
    ├─ CONTENT WRITER generates detailed lesson
    ├─ SAVE → 01_section_title.md, 02_section_title.md, etc.
    └─ CONTINUE
    ↓
COMPLETE → Folder with all materials
```

---

## Installation

### Prerequisites
- Python 3.10 - 3.13
- Ollama running locally (for LLM inference)
- Git
Installed Complete Dependencies - Successfully installed CrewAI 1.9.3 and all dependencies including:
crewai-tools 1.9.3
tiktoken 0.8.0 (now works with Python 3.12)
litellm for Ollama support
### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd /Users/b.saab/repos/crewai_bsaab/src/educational_materials
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install crewai crewai[tools]
   ```

4. **Configure environment:**
   - Copy `.env.example` to `.env` (already provided)
   - Update API keys if using OpenAI or Serper instead of local Ollama

---

## Usage

### Basic Usage

Generate materials for a topic at Beginner level:

```bash
python main.py "Python Basics" Beginner
```

### With Source URLs

Provide URLs for research grounding:

```bash
python main.py "Azure Fundamentals" Beginner \
  --urls "https://learn.microsoft.com/en-us/training/paths/prepare-teach-az-900-microsoft-academic-programs/" \
         "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/"
```

### Different Difficulty Levels

```bash
# Beginner
python main.py "Machine Learning Basics" Beginner

# Intermediate
python main.py "Machine Learning Algorithms" Intermediate

# Expert
python main.py "Deep Learning Architecture" Expert

# Basic usage
python main.py "Machine Learning Basics" Beginner

# With research URLs
python main.py "Azure Fundamentals" Beginner \
  --urls "https://learn.microsoft.com/..." "https://..."

# Different levels
python main.py "Python Advanced" Expert --urls "..."

# View flow diagram
python main.py "Topic" Beginner --plot

/Users/b.saab/repos/.venv/bin/python -m src.educational_materials.main "AZURE FUNDAMENTALS" Beginner --urls "https://learn.microsoft.com/" 2>&1 | tail -300‚
```

### View Flow Diagram

```bash
python main.py "Topic Name" Beginner --plot
```

---

## Output Structure

Generated materials are organized in a folder named after the topic:

```
Azure_Fundamentals/
├── course_outline.md              # Reviewed outline (3-10 sections)
├── 01_introduction.md             # Section 1
├── 02_core_services.md            # Section 2
├── 03_advanced_topics.md          # Section 3
└── ...
```

Each section file includes:
- **Title** (as H2 heading)
- **Content** (1000-2000 words)
- **Examples and case studies**
- **References section** with citations and URLs

---

## Customization

### Modify Agents
Edit `config/agents.yaml` to adjust agent roles, goals, and backstories:

```yaml
researcher:
  role: >
    Research Specialist and Content Analyst
  goal: >
    Conduct in-depth research on {topic}...
```

### Modify Tasks
Edit `config/tasks.yaml` to refine task descriptions and outputs:

```yaml
research_topic:
  description: >
    Conduct comprehensive research on the topic "{topic}"...
```

### Adjust LLM Configuration
In `crew.py`, change the LLM model or base URL:

```python
llm = LLM(model="gpt-4", api_key="YOUR_KEY")  # For OpenAI
# OR
llm = LLM(model="ollama/neural-chat", base_url="http://localhost:11434")  # For local Ollama
```

---

## Advanced Usage

### Programmatic Usage

```python
from educational_materials.main import kickoff

kickoff(
    topic="Quantum Computing Fundamentals",
    level="Intermediate",
    urls=["https://example.com/quantum", "https://arxiv.org/quantum"]
)
```

### Access Generated Materials

```python
from educational_materials.types import Section, OutlinePoint

# Access section content after generation
sections = flow_state.sections
for section in sections:
    print(f"Section: {section.title}")
    print(f"Content: {section.content}")
```

---

## Troubleshooting

### Ollama Connection Error
Ensure Ollama is running:
```bash
ollama serve
ollama pull mistral  # Download the model
```

### Timeout Issues
Increase timeout in `crew.py`:
```python
llm = LLM(model="ollama/mistral", base_url="http://localhost:11434", timeout=60)
```

### Empty Output
- Verify the topic is well-defined
- Check that URLs are accessible
- Try with a simpler topic first

---

## Project Structure

```
educational_materials/
├── __init__.py
├── main.py                        # CrewAI Flow and orchestration
├── crew.py                        # Agent and crew definitions
├── types.py                       # Pydantic data models
├── config/
│   ├── agents.yaml               # Agent configurations
│   └── tasks.yaml                # Task configurations
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

---

## Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| crewai | >=0.152.0 | Agent orchestration framework |
| crewai[tools] | >=0.152.0 | Built-in tools for agents |
| pydantic | Latest | Data validation and modeling |
| python | 3.10-3.13 | Runtime environment |

---

## Future Enhancements

- [ ] Integration with vector databases for RAG
- [ ] Support for multiple output formats (PDF, HTML, Jupyter notebooks)
- [ ] Automatic plagiarism checking
- [ ] Interactive web UI for flow management
- [ ] Content versioning and collaboration features
- [ ] Support for multimedia (images, diagrams, videos)

---

## Support & Documentation

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI Examples Repository](https://github.com/crewAIInc/crewAI-examples)
- [GitHub Issues](https://github.com/crewAIInc/crewai/issues)

---

## License

This project is part of the crewai_bsaab repository.

---

## Contributing

Contributions welcome! Please ensure:
- Code follows PEP 8 style guide
- All methods are documented
- Changes maintain backward compatibility

---

**Happy Learning Material Generation! 🚀**
