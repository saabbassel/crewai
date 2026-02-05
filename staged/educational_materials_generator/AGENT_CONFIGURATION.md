# Agent Configuration Guide

## Overview

The educational materials generator uses **9 specialized agents** across **5 stages**, each configured with optimized LLM parameters, personalities, and capabilities.

---

## 🏗️ Agent Topology

```
STAGE 1: DISCOVERY & BENCHMARKING (3 agents)
├── CourseResearcher (analyzes existing courses)
├── TrendsAnalyst (identifies market trends & skills gaps)
└── PersonaBuilder (creates learner personas)

STAGE 2: CURRICULUM ARCHITECTURE (2 agents)
├── CurriculumDesigner (designs module sequences)
└── InstructionalDesigner (maps instruction strategies)

STAGE 3: CONTENT PRODUCTION (2 agents)
├── LessonAuthor (writes explanations)
└── ExampleGenerator (creates examples & scenarios)

STAGE 4: ASSESSMENT & HANDS-ON (2 agents)
├── ExerciseDesigner (creates exercises & labs)
└── AssessmentBuilder (creates quizzes & rubrics)

STAGE 5: QA & REVIEW (2 agents)
├── PedagogicalReviewer (checks alignment)
└── ClarityChecker (verifies accessibility & bias)
```

---

## 🤖 Stage 1: Discovery & Benchmarking

**Goal**: Research existing courses and create comprehensive research dossier

**LLM Configuration**:
- Model: `DISCOVERY_MODEL` (default: llama2:13b-chat)
- Temperature: 0.7 (analytical + creative)
- Top-p: 0.9 (diverse responses)
- Timeout: 120 seconds

### CourseResearcher

```yaml
Role: Course Researcher
Goal: Search and analyze popular courses on {topic} from major platforms
      (Coursera, Udemy, edX, YouTube, GitHub) to identify structure, 
      modules, and best practices

Responsibilities:
  - Search major learning platforms
  - Extract module structures and progression
  - Identify common topics and organization patterns
  - Analyze time allocations and pacing
  - Review student feedback and ratings
  - Document pedagogical approaches
  
Output: Course summaries, module lists, structural patterns
Quality Focus: Accuracy, comprehensiveness, platform coverage
```

### TrendsAnalyst

```yaml
Role: Trend & Skills Analyst
Goal: Identify {topic} skills that are frequently taught, missing, or in 
      high demand across all available courses and job market

Responsibilities:
  - Analyze job postings for required skills
  - Identify emerging technologies and trends
  - Compare skills taught vs. skills needed
  - Validate certification requirements
  - Identify skill gaps and duplications
  - Research industry demand patterns

Output: Skills matrix, trends report, gap analysis
Quality Focus: Market alignment, forward-looking trends
```

### PersonaBuilder

```yaml
Role: Audience Persona Builder
Goal: Create detailed learner personas for {topic} including:
      beginner/intermediate/advanced, academic vs industry, 
      time constraints, and learning preferences

Responsibilities:
  - Create experience-level personas (3+ levels)
  - Define learning goals per persona
  - Document time availability and constraints
  - Identify prior knowledge needs
  - Map learning style preferences
  - Note accessibility considerations
  - Consider cultural and demographic factors

Output: Persona profiles (2-5 personas), needs assessment
Quality Focus: Practical, actionable insights
```

---

## 🎓 Stage 2: Curriculum Architecture

**Goal**: Design pedagogically sound curriculum structure with Bloom's alignment

**LLM Configuration**:
- Model: `CURRICULUM_MODEL` (default: llama2:13b-chat)
- Temperature: 0.6 (structured, consistent)
- Top-p: 0.85 (focused responses)
- Timeout: 120 seconds

### CurriculumDesigner

```yaml
Role: Curriculum Designer
Goal: Design a well-sequenced curriculum for {topic} following Bloom's 
      taxonomy, with clear learning objectives progressing from 
      foundational to advanced concepts

Responsibilities:
  - Map learning objectives to Bloom's taxonomy levels
  - Design prerequisite chains and dependencies
  - Create module progression logic
  - Plan spiral learning approach
  - Allocate time per module
  - Identify assessment checkpoints
  - Ensure cognitive load progression

Output: Curriculum blueprint with objectives, modules, sequence
Quality Focus: Bloom's alignment, logical progression
```

### InstructionalDesigner

```yaml
Role: Instructional Design Expert
Goal: Map learning objectives to instructional strategies, examples, 
      practice opportunities, and aligned assessments for {topic}

Responsibilities:
  - Select instructional methods (lecture, demo, discussion, hands-on)
  - Plan practice opportunities and scaffolding
  - Design formative assessments
  - Map cognitive complexity to depth
  - Create examples and counter-examples
  - Plan differentiation strategies
  - Specify media and modalities

Output: Instructional strategy map, task breakdown
Quality Focus: Objective alignment, instructional variety
```

---

## 📝 Stage 3: Content Production

**Goal**: Generate engaging lesson content, examples, and handouts

**LLM Configuration**:
- Model: `CONTENT_MODEL` (default: llama2:13b-chat)
- Temperature: 0.8 (creative, varied)
- Top-p: 0.95 (diverse, flowing content)
- Timeout: 180 seconds (longer for content)

### LessonAuthor

```yaml
Role: Lesson Author
Goal: Write clear, well-structured lessons for {topic} modules with 
      concept explanations, analogies, step-by-step breakdowns, and 
      worked examples

Responsibilities:
  - Write engaging lesson introductions
  - Explain concepts simply and clearly
  - Create analogies for abstract concepts
  - Break processes into digestible steps
  - Include comprehension checks
  - Connect theory to practice
  - Use active, inclusive language
  - Target specified reading level

Output: Markdown lessons with structured content
Quality Focus: Clarity, engagement, accessibility (WCAG 2.1 AA)
Target Grade Level: Configurable (default: 9)
```

### ExampleGenerator

```yaml
Role: Example Generator
Goal: Create worked examples, real-world scenarios, and common mistakes 
      for {topic} that illustrate concepts from simple to complex

Responsibilities:
  - Create simple, concrete examples
  - Develop real-world use cases
  - Show common misconceptions
  - Provide step-by-step solutions
  - Illustrate edge cases
  - Multiple representations (visual, text, code)
  - Connect to familiar domains
  - Show what NOT to do

Output: Worked examples, scenarios, mistake analysis
Quality Focus: Relevance, variety, progressive difficulty
```

---

## ✅ Stage 4: Assessment & Hands-On

**Goal**: Create scaffolded exercises, quizzes, and project specifications

**LLM Configuration**:
- Model: `ASSESSMENT_MODEL` (default: llama2:13b-chat)
- Temperature: 0.7 (balanced rigor + creativity)
- Top-p: 0.9 (diverse assessment types)
- Timeout: 180 seconds

### ExerciseDesigner

```yaml
Role: Exercise Designer
Goal: Create scaffolded, hands-on exercises for {topic} progressing from 
      guided practice to open-ended challenges, with clear success criteria

Responsibilities:
  - Design guided to open-ended progression
  - Create multiple difficulty levels
  - Write clear success criteria
  - Provide step-by-step guidance
  - Include hints and troubleshooting
  - Show common mistakes and fixes
  - Connect to real-world applications
  - Estimate completion time
  - Create rubrics

Output: Exercise specifications with solutions
Quality Focus: Scaffolding, clarity, real-world relevance
```

### AssessmentBuilder

```yaml
Role: Assessment Builder
Goal: Create quizzes, rubrics, and self-assessment tools for {topic} with 
      questions at appropriate Bloom's levels and clear scoring criteria

Responsibilities:
  - Write test items at multiple Bloom's levels
  - Create clear, unambiguous questions
  - Develop plausible distractors (multiple choice)
  - Design detailed rubrics
  - Create self-assessment checklists
  - Write answer keys with explanations
  - Rate item difficulty and discrimination
  - Plan feedback strategies
  - Ensure accessibility

Output: Assessments (quizzes, rubrics, checklists)
Quality Focus: Validity, reliability, Bloom's alignment
```

---

## 🔍 Stage 5: QA & Review

**Goal**: Review and validate all generated materials for quality

**LLM Configuration**:
- Model: `QA_MODEL` (default: llama2:13b-chat)
- Temperature: 0.5 (conservative, rigorous)
- Top-p: 0.8 (focused review)
- Timeout: 120 seconds

### PedagogicalReviewer

```yaml
Role: Pedagogical Reviewer
Goal: Review {topic} materials for pedagogical alignment: learning 
      objectives clarity, assessment alignment, prerequisite validity, 
      and appropriate cognitive load

Responsibilities:
  - Validate learning objective clarity
  - Check objective-instruction-assessment alignment
  - Assess cognitive load appropriateness
  - Validate prerequisite accuracy
  - Verify Bloom's level appropriateness
  - Check pedagogical soundness
  - Verify outcome coverage
  - Identify gaps or duplications

Output: QA report with issues and suggestions
Quality Focus: Alignment, completeness, pedagogical rigor
```

### ClarityChecker

```yaml
Role: Clarity & Bias Checker
Goal: Review {topic} materials for clarity, reading level, jargon, 
      accessibility, and cultural/gender bias

Responsibilities:
  - Assess reading level (Flesch-Kincaid)
  - Identify and simplify jargon
  - Detect gender bias and stereotypes
  - Check cultural representation
  - Verify WCAG 2.1 AA compliance
  - Validate color contrast
  - Check alt-text quality
  - Verify heading hierarchy
  - Apply plain language principles

Output: Accessibility audit, bias report
Quality Focus: Accessibility (WCAG 2.1 AA), inclusivity, clarity
Target Grade Level: Verified against config (default: 9)
```

---

## 🎛️ LLM Configuration Reference

### Temperature Settings

```
Stage 1 (Discovery):    0.7  ← Analytical with creative analysis
Stage 2 (Curriculum):   0.6  ← Structured, focused design
Stage 3 (Content):      0.8  ← Creative, varied writing
Stage 4 (Assessment):   0.7  ← Balanced rigor and variety
Stage 5 (QA):           0.5  ← Conservative, rigorous review
```

### Top-p Sampling

```
Stage 1 (Discovery):    0.9  ← Diverse analytical perspectives
Stage 2 (Curriculum):   0.85 ← Focused curriculum alternatives
Stage 3 (Content):      0.95 ← Maximum writing variety
Stage 4 (Assessment):   0.9  ← Diverse assessment types
Stage 5 (QA):           0.8  ← Focused QA checks
```

### Model Presets

**Lean Mode** (Fast, Lower Quality)
```yaml
All Stages: mistral:7b-instruct
Memory: 12GB VRAM
Speed: ⚡⚡⚡ Fast
Quality: ⭐⭐ Basic
Cost: $
Use Case: Quick prototyping, testing
```

**Standard Mode** (Recommended)
```yaml
All Stages: llama2:13b-chat
Memory: 24GB VRAM
Speed: ⚡⚡ Medium
Quality: ⭐⭐⭐⭐ Good
Cost: $$
Use Case: Production use, balanced quality/speed
```

**Pro Mode** (Best Quality)
```yaml
Stage 1,2,3: llama2:13b-chat (or mixtral:8x7b)
Stage 4:     deepseek-v3.2 (or qwen:30b)
Stage 5:     qwen:30b (rigorous review)
Memory: 32GB+ VRAM
Speed: ⚡ Slow
Quality: ⭐⭐⭐⭐⭐ Excellent
Cost: $$$
Use Case: High-stakes materials, premium quality
```

---

## 🔧 Configuration Usage

### Via Environment Variables

```bash
# Select models per stage
export DISCOVERY_MODEL="llama2:13b-chat"
export CURRICULUM_MODEL="llama2:13b-chat"
export CONTENT_MODEL="mixtral:8x7b"
export ASSESSMENT_MODEL="mistral:7b-instruct"
export QA_MODEL="qwen:30b"

# Ollama configuration
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_TIMEOUT="120"

# Run application
python main.py
```

### Via Python Code

```python
from src.config import Config, LLMConfig

# Apply preset
Config.apply_preset("standard")  # lean | standard | pro

# Or configure individually
Config.DISCOVERY_MODEL = "llama2:13b-chat"
Config.CONTENT_MODEL = "mixtral:8x7b"

# Get LLM for specific stage
discovery_llm = LLMConfig.get_discovery_llm()
content_llm = LLMConfig.get_content_llm()
qa_llm = LLMConfig.get_qa_llm()

# Create agents
from src.agents import DiscoveryAgents, ContentAgents
researcher = DiscoveryAgents.course_researcher()
author = ContentAgents.lesson_author()
```

---

## 🎯 Agent Selection Guidelines

### When to Use Each Stage

**Use Stage 1 (Discovery)** when:
- Starting a new course topic
- Conducting market research
- Creating learner personas
- Building research dossier
- Benchmarking against competitors

**Use Stage 2 (Curriculum)** when:
- Designing module structure
- Creating learning objectives
- Mapping prerequisites
- Planning time allocations
- Ensuring Bloom's alignment

**Use Stage 3 (Content)** when:
- Writing lesson explanations
- Creating examples
- Generating handouts
- Developing variants (academic/conversational)
- Building content library

**Use Stage 4 (Assessment)** when:
- Creating exercises
- Designing quizzes
- Building projects
- Writing rubrics
- Planning labs

**Use Stage 5 (QA)** when:
- Reviewing completed materials
- Checking alignment
- Validating accessibility
- Auditing consistency
- Preparing for publication

---

## 📊 Agent Capabilities Matrix

| Capability | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5 |
|------------|---------|---------|---------|---------|---------|
| Research & Analysis | ✅ | ✅ | ⚠️ | ⚠️ | ✅ |
| Design & Planning | ✅ | ✅ | ✅ | ✅ | ✅ |
| Creative Writing | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ |
| Assessment Design | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |
| Quality Review | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Accessibility Check | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| Bias Detection | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |

**Legend**: ✅ = Primary capability | ⚠️ = Secondary/partial capability

---

## 🚀 Running Agents

### Individual Agent Test

```python
from src.agents import DiscoveryAgents

# Create agent
researcher = DiscoveryAgents.course_researcher()

# Display info
print(f"Role: {researcher.role}")
print(f"Goal: {researcher.goal}")
print(f"Model: {researcher.llm.model}")
```

### All Agents by Stage

```python
from src.agents import get_stage_agents

# Get Stage 3 agents
stage_3_agents = get_stage_agents(3)
for agent in stage_3_agents:
    print(f"- {agent.role}")

# Get all agents
all_agents = get_all_agents()
for stage, agents in all_agents.items():
    print(f"\n{stage}:")
    for agent in agents:
        print(f"  - {agent.role}")
```

### Run Agent Script

```bash
# Test all agents
python -m src.agents

# Output:
# ================================================================================
# EDUCATIONAL MATERIALS GENERATOR - AGENT SUMMARY
# ================================================================================
#
# 📍 STAGE 1: STAGE_1_DISCOVERY
# ────────────────────────────────────────────────────────────────────────────────
#
#   🤖 Course Researcher
#      Goal: Search and analyze popular courses...
#      LLM: ollama/llama2:13b-chat
#
#   🤖 Trend & Skills Analyst
#      Goal: Identify Azure Fundamentals skills...
#      LLM: ollama/llama2:13b-chat
#
#   [... continues for all stages ...]
#
# ================================================================================
# ✅ All agents initialized successfully
# ================================================================================
```

---

## ⚙️ Advanced Configuration

### Custom LLM Parameters

```python
from src.config import LLMConfig

# Override temperature for specific use case
custom_llm = LLMConfig.get_llm_config(
    model="mistral:7b-instruct",
    temperature=0.5,  # More deterministic
    top_p=0.75,       # Focused responses
)
```

### Environment-Specific Configs

```bash
# Development
export OLLAMA_BASE_URL="http://localhost:11434"
export DISCOVERY_MODEL="mistral:7b-instruct"
export LOG_LEVEL="DEBUG"

# Production
export OLLAMA_BASE_URL="http://gpu-server:11434"
export DISCOVERY_MODEL="llama2:13b-chat"
export LOG_LEVEL="INFO"
```

---

## 📈 Performance Tuning

### For Speed

```python
# Use smaller models
Config.apply_preset("lean")

# Reduce temperature (faster convergence)
# → Stage 5: 0.5 is already optimized
# → Adjust others down if needed
```

### For Quality

```python
# Use larger models
Config.apply_preset("pro")

# Use different models per stage
Config.CONTENT_MODEL = "mixtral:8x7b"     # More creative
Config.QA_MODEL = "qwen:30b"              # More rigorous
```

### For Cost

```python
# Use lean preset
Config.apply_preset("lean")

# Or mix presets
Config.DISCOVERY_MODEL = "mistral:7b-instruct"  # Fast
Config.CURRICULUM_MODEL = "mistral:7b-instruct" # Fast
Config.CONTENT_MODEL = "llama2:13b-chat"        # Quality
```

---

## ✅ Checklist: Agent Configuration

- [ ] Ollama server running on configured `OLLAMA_BASE_URL`
- [ ] All required models available: `ollama pull llama2:13b-chat`, etc.
- [ ] Environment variables set or `.env` file created
- [ ] Temperature settings appropriate for your use case
- [ ] Model presets selected (lean/standard/pro)
- [ ] HITL gates configured for your workflow
- [ ] Output directory configured
- [ ] Standardization enforcement enabled
- [ ] Accessibility checks enabled (WCAG 2.1 AA)
- [ ] Agent test run successful

---

**Last Updated**: February 5, 2026  
**Version**: 1.0  
**Status**: Production Ready ✅
