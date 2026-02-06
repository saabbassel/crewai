# Educational Materials Generator - CrewAI Implementation

Multi-stage agentic educational materials generator using CrewAI and local Ollama models.

## Project Overview

This project implements a 5-stage pipeline for generating comprehensive educational materials:

1. **Discovery & Benchmarking** - Research existing courses and identify patterns
2. **Curriculum Architect** - Design pedagogically sound curriculum structure
3. **Content Factory** - Generate lessons, handouts, and examples
4. **Assessment Lab** - Create exercises, projects, and assessments
5. **Review & QA** - Quality assurance and compliance checking

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama with models installed
- 24GB+ VRAM GPU (recommended) or 64GB+ CPU RAM (minimum)

### Installation

```bash
# Clone the repository
cd staged/educational_materials_generator

# Install dependencies
pip install -e .

# Create .env file
cp .env.example .env
```

### Environment Setup

```bash
# Pull required Ollama models
ollama pull llama2:13b-chat
ollama pull mistral:7b-instruct
ollama pull mixtral:8x7b

# Start Ollama service
ollama serve
```

### Configuration

Edit `.env`:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Model Selection
DISCOVERY_MODEL=llama2:13b-chat
CURRICULUM_MODEL=llama2:13b-chat
CONTENT_MODEL=llama2:13b-chat
ASSESSMENT_MODEL=llama2:13b-chat
QA_MODEL=llama2:13b-chat

# Output Configuration
OUTPUT_DIR=./output
ARCHIVE_OUTPUTS=true

# HITL Configuration
ENABLE_HITL=true
APPROVAL_TIMEOUT=300
```

## Project Structure

```
educational_materials_generator/
├── src/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── models.py                    # Pydantic data models
│   ├── standardizer.py              # Content standardization utilities
│   ├── crews/
│   │   ├── __init__.py
│   │   ├── discovery_crew.py        # Stage 1: Research crew
│   │   ├── curriculum_crew.py       # Stage 2: Curriculum design crew
│   │   ├── content_crew.py          # Stage 3: Content factory crew
│   │   ├── assessment_crew.py       # Stage 4: Assessment lab crew
│   │   └── qa_crew.py               # Stage 5: QA review crew
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── discovery_agents.py      # Stage 1 agents
│   │   ├── curriculum_agents.py     # Stage 2 agents
│   │   ├── content_agents.py        # Stage 3 agents
│   │   ├── assessment_agents.py     # Stage 4 agents
│   │   └── qa_agents.py             # Stage 5 agents
│   ├── flows/
│   │   ├── __init__.py
│   │   └── main_flow.py             # Primary orchestration flow
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py          # File I/O utilities
│       ├── validation.py            # JSON schema & markdown validation
│       └── metrics.py               # Quality score calculation
├── schemas/
│   ├── discovery_schema.json        # Research output schema
│   ├── curriculum_schema.json       # Curriculum blueprint schema
│   ├── content_schema.json          # Lesson content schema
│   ├── assessment_schema.json       # Exercise/quiz schema
│   └── qa_schema.json               # QA report schema
├── templates/
│   ├── standards_prompt.md          # Standardization injection prompt
│   ├── lesson_template.md           # Lesson writing template
│   ├── exercise_template.json       # Exercise template
│   ├── handout_template.md          # Handout template
│   └── assessment_template.json     # Assessment template
├── output/                          # Generated materials storage
├── GLOSSARY.md                      # Master terminology reference
├── STANDARDS.md                     # Full standardization guidelines
├── README.md                        # This file
├── .env.example                     # Environment template
└── pyproject.toml                   # Project configuration
```

## Usage

### Run Complete Pipeline

```bash
# Test
/Users/b.saab/repos/.venv/bin/python test_agents.py

# create a quick visual summary of what's been scaffolded:
cd /Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator && find . -type f -name "*.py" -o -name "*.md" -o -name "*.toml" -o -name ".env*" | head -30

python -m src.flows.main_flow \
    --topic "Azure Fundamentals" \
    --level "Beginner" \
    --urls "https://learn.microsoft.com/azure/" \
    --output-dir ./output

/Users/b.saab/repos/.venv/bin/python main.py --input input/azure_fundamentals.json --stages 1 --output output

/Users/b.saab/repos/.venv/bin/python main.py --input input/azure_fundamentals.json --stages 2,3,4,5 --output output

/Users/b.saab/repos/.venv/bin/python main.py --input input/azure_fundamentals.json --stages 1,2,3,4,5 --output output 2>&1 | head -100

# Demo mode
/Users/b.saab/repos/.venv/bin/python main.py --input input/azure_fundamentals.json --stages 1,2,3,4,5 --output output 2>&1 | grep -E "(Starting|Running|demo|Pipeline|output)"

# run the full pipeline again with the correct model:
/Users/b.saab/repos/.venv/bin/python main.py --input input/azure_fundamentals.json --stages 1,2,3,4,5 --output output 2>&1 | grep -E "(Starting|Running|Stage|Pipeline|error|Error|completed|Output)"

/Users/b.saab/repos/.venv/bin/python main.py --input input/azure_fundamentals.json --stages 2 --output output 2>&1 | sed -n '1,240p'


# Debug check what models are actually available and display them:
curl -s http://localhost:11434/api/tags | /Users/b.saab/repos/.venv/bin/python -m json.tool 2>&1 | head -50

# verify all outputs were created
cd /Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator/output && ls -lh stage_*.json stage_*.md 2>&1 | grep -E "(stage_|total)"
```

### Run Individual Stages

```bash
# Stage 1: Discovery
python -m src.stages.discovery \
    --topic "Azure Fundamentals" \
    --level "Beginner" \
    --output research_dossier.json

# Stage 2: Curriculum (requires Stage 1 output)
python -m src.stages.curriculum \
    --research-file research_dossier.json \
    --output curriculum_blueprint.json

# Stage 3: Content (requires Stage 2 output)
python -m src.stages.content \
    --curriculum-file curriculum_blueprint.json \
    --output-dir ./content

# Stage 4: Assessment (requires Stage 3 output)
python -m src.stages.assessment \
    --curriculum-file curriculum_blueprint.json \
    --output-dir ./assessments

# Stage 5: QA Review (optional, reviews all materials)
python -m src.stages.qa_review \
    --materials-dir ./output \
    --output qa_report.json
```

## Standardization

All generated materials follow strict standards defined in `STANDARDS.md`:

- **Naming Convention**: `[STAGE]_[TYPE]_[DESCRIPTOR]_[VERSION].ext`
- **Metadata**: YAML frontmatter on all artifacts
- **Quality Metrics**: Completeness, Clarity, Alignment scores
- **Accessibility**: WCAG 2.1 AA compliance
- **Terminology**: Consistent with GLOSSARY.md

### Quality Gates

Each stage includes automated validation:

1. **Schema Validation**: JSON must match schema
2. **Markdown Linting**: Heading hierarchy, formatting checks
3. **Terminology Check**: Against GLOSSARY.md
4. **Accessibility Scan**: WCAG 2.1 AA compliance
5. **Readability Analysis**: Flesch–Kincaid grade level

### Generated Output Example

```
output/
├── AZURE_FUNDAMENTALS_v1.0/
│   ├── STAGE-1_RESEARCH_AZ900_v1.0.json
│   ├── STAGE-2_CURRICULUM_AZ900_v1.0.json
│   ├── STAGE-3_CONTENT/
│   │   ├── MOD-01/
│   │   │   ├── MOD-01_LESSON_v1.0.md
│   │   │   ├── MOD-01_HANDOUT_v1.0.md
│   │   │   └── MOD-01_EXAMPLES_v1.0.md
│   │   ├── MOD-02/
│   │   └── ...
│   ├── STAGE-4_ASSESSMENT/
│   │   ├── MOD-01_EXERCISES_v1.0.json
│   │   ├── MOD-01_QUIZZES_v1.0.json
│   │   └── ...
│   └── STAGE-5_QA_REPORT_v1.0.json
├── GLOSSARY.md
├── STANDARDS_APPLIED.md
└── manifest.json
```

## Configuration Options

### Model Selection

Switch models per stage by editing `.env`:

**Option 1: Lean Mode** (fastest, lowest quality)
```env
DISCOVERY_MODEL=mistral:7b-instruct
CURRICULUM_MODEL=mistral:7b-instruct
CONTENT_MODEL=mistral:7b-instruct
ASSESSMENT_MODEL=mistral:7b-instruct
QA_MODEL=mistral:7b-instruct
```

**Option 2: Standard Mode** (recommended)
```env
DISCOVERY_MODEL=llama2:13b-chat
CURRICULUM_MODEL=llama2:13b-chat
CONTENT_MODEL=llama2:13b-chat
ASSESSMENT_MODEL=llama2:13b-chat
QA_MODEL=llama2:13b-chat
```

**Option 3: Pro Mode** (best quality, highest resource usage)
```env
DISCOVERY_MODEL=llama2:13b-chat
CURRICULUM_MODEL=mixtral:8x7b
CONTENT_MODEL=mixtral:8x7b
ASSESSMENT_MODEL=deepseek-v3.2-speciale
QA_MODEL=qwen:30b
```

### HITL Configuration

```env
# Enable Human-in-the-Loop approvals
ENABLE_HITL=true

# After each stage, prompt for approval
HITL_AFTER_DISCOVERY=true
HITL_AFTER_CURRICULUM=true
HITL_AFTER_CONTENT=false

# Timeout for approval prompts (seconds)
APPROVAL_TIMEOUT=300
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/

# Type checking
mypy src/
```

### Adding Custom Agents

1. Create agent definition in `src/agents/[stage]_agents.py`
2. Define tasks in corresponding crew file
3. Update standardization prompt with new requirements
4. Add validation rules in `src/utils/validation.py`

## Troubleshooting

### Models Not Found

```bash
ollama pull llama2:13b-chat
ollama pull mistral:7b-instruct
```

### Out of Memory (OOM)

Use Lean mode or 4-bit quantization:
```env
DISCOVERY_MODEL=mistral:7b-instruct
```

### Ollama Connection Failed

```bash
# Check Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### JSON Validation Errors

Check output against schema:
```bash
python -m src.utils.validation schemas/[stage]_schema.json output_file.json
```

## Performance Benchmarks

### Hardware Requirements

| Budget | Setup | Time/Course |
|--------|-------|------------|
| **Lean** ($500) | 12GB VRAM GPU + 32GB RAM | 12–16 hours |
| **Standard** ($2K) | 24GB VRAM GPU + 64GB RAM | 6–8 hours |
| **Pro** ($5K+) | Dual 24GB GPUs + 128GB RAM | 3–4 hours |

### Stage Execution Times (Standard Setup)

- Stage 1 (Discovery): 10–15 min
- Stage 2 (Curriculum): 5–10 min
- Stage 3 (Content, 10 modules): 30–45 min
- Stage 4 (Assessment, 10 modules): 15–25 min
- Stage 5 (QA Review): 10–15 min

**Total: ~70–110 minutes per course**

## Documentation

- **[STANDARDS.md](STANDARDS.md)** - Comprehensive standardization guidelines
- **[GLOSSARY.md](GLOSSARY.md)** - Master terminology reference
- **Schemas/** - JSON output schemas for each stage
- **Templates/** - Agent prompt templates and examples

## Contributing

Please follow the [STANDARDS.md](STANDARDS.md) guidelines for all contributions.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
1. Check existing issues on GitHub
2. Review [STANDARDS.md](STANDARDS.md) for common questions
3. Create detailed issue with reproduction steps

## Roadmap

- [x] Stage 1-5 architecture
- [x] Standardization framework
- [x] WCAG 2.1 AA accessibility support
- [ ] Multi-language support
- [ ] Export to PDF/HTML
- [ ] Student feedback integration
- [ ] Performance analytics
- [ ] Web UI dashboard
