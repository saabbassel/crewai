# Educational Materials Generator - Architecture Overview

## 🏗️ Project Architecture

```
EDUCATIONAL MATERIALS GENERATOR
├─ 5-Stage Pipeline
├─ 15+ Specialized Agents
├─ Standardization Framework
└─ Quality Assurance System
```

---

## 📊 Data Flow Architecture

```
USER INPUT
│
├─ Topic: "Azure Fundamentals"
├─ Level: "Beginner"
└─ URLs: [resource links]
│
▼
┌─────────────────────────────────────┐
│ STAGE 1: DISCOVERY & BENCHMARKING   │
├─────────────────────────────────────┤
│ Agents:                              │
│ • Course Researcher                  │
│ • Trends Analyst                     │
│ • Persona Builder                    │
│                                      │
│ Output: ResearchDossier (JSON)       │
│ Validation: Schema ✓ Accessibility ✓ │
└─────────────────────────────────────┘
│
▼ [HITL: Review & Approve]
│
┌─────────────────────────────────────┐
│ STAGE 2: CURRICULUM ARCHITECT       │
├─────────────────────────────────────┤
│ Agents:                              │
│ • Curriculum Designer                │
│ • Instructional Designer             │
│ • Content Organizer                  │
│                                      │
│ Input: ResearchDossier               │
│ Output: CurriculumBlueprint (JSON)   │
│ Validation: Bloom's ✓ Prerequisites ✓ │
└─────────────────────────────────────┘
│
▼ [HITL: Review & Approve]
│
┌─────────────────────────────────────┐
│ STAGE 3: CONTENT FACTORY            │
├─────────────────────────────────────┤
│ Agents (per Module):                 │
│ • Lesson Author                      │
│ • Example Generator                  │
│ • Handout Creator                    │
│ • Teaching Tone Adapter              │
│ • Interactive Content Generator      │
│                                      │
│ Input: CurriculumBlueprint           │
│ Output: ContentMaterial (MD/JSON)    │
│ 📦 Variants: Academic/Conversational │
│ Validation: Clarity ✓ Accessibility ✓ │
└─────────────────────────────────────┘
│
▼ [Optional: Manual Review]
│
┌─────────────────────────────────────┐
│ STAGE 4: ASSESSMENT LAB             │
├─────────────────────────────────────┤
│ Agents (per Module):                 │
│ • Exercise Designer                  │
│ • Project Architect                  │
│ • Assessment Builder                 │
│ • Solution Explainer                 │
│ • Lab Environment Generator          │
│                                      │
│ Input: CurriculumBlueprint           │
│ Output: Assessment (JSON)            │
│ Contains: Exercises, Quizzes, Labs   │
│ Validation: Bloom's ✓ Schema ✓       │
└─────────────────────────────────────┘
│
▼ [Optional: Manual Review]
│
┌─────────────────────────────────────┐
│ STAGE 5: REVIEW & QA (Optional)     │
├─────────────────────────────────────┤
│ Agents:                              │
│ • Pedagogical Reviewer               │
│ • Clarity & Bias Checker             │
│ • Difficulty Calibration Agent       │
│ • Consistency Auditor                │
│ • Accessibility Reviewer             │
│                                      │
│ Input: All materials from Stages 1-4 │
│ Output: QAReport (JSON/MD)           │
│ Checks: Alignment ✓ Clarity ✓        │
│         Consistency ✓ Accessibility ✓ │
└─────────────────────────────────────┘
│
▼
FINAL ARTIFACTS (Organized by Stage)
├── STAGE-1_RESEARCH_[COURSE]_v1.0.json
├── STAGE-2_CURRICULUM_[COURSE]_v1.0.json
├── STAGE-3_CONTENT/
│   ├── MOD-01_LESSON_v1.0.md
│   ├── MOD-01_HANDOUT_v1.0.md
│   ├── MOD-02_LESSON_v1.0.md
│   └── ...
├── STAGE-4_ASSESSMENT/
│   ├── MOD-01_EXERCISES_v1.0.json
│   ├── MOD-01_QUIZZES_v1.0.json
│   └── ...
├── STAGE-5_QA_REPORT_[COURSE]_v1.0.json
├── GLOSSARY.md
└── manifest.json
```

---

## 🤖 Agent Roles & Responsibilities

### Stage 1: Discovery (Research)
| Agent | Role | Output |
|-------|------|--------|
| **Course Researcher** | Analyze existing courses across platforms | Course summaries, module structures |
| **Trends Analyst** | Identify skill gaps and trends | Market analysis, skills matrix |
| **Persona Builder** | Create learner profiles | Audience segments, learning needs |

### Stage 2: Curriculum Design
| Agent | Role | Output |
|-------|------|--------|
| **Curriculum Designer** | Design module sequences with learning objectives | Module blueprint, Bloom's alignment |
| **Instructional Designer** | Map instruction to objectives | Task breakdown, assessment alignment |
| **Content Organizer** | Organize modules logically | Module grouping, prerequisite chains |

### Stage 3: Content Production
| Agent | Role | Output |
|-------|------|--------|
| **Lesson Author** | Write clear explanations | Markdown lessons with examples |
| **Example Generator** | Create worked examples | Code samples, scenarios, mistakes |
| **Handout Creator** | Make quick references | 1-page summaries, cheat sheets |
| **Teaching Tone Adapter** | Vary presentation style | 3 content variants (Academic/Conv./Corp) |
| **Interactive Generator** | Suggest interactions | Discussion prompts, quiz ideas |

### Stage 4: Assessment & Hands-On
| Agent | Role | Output |
|-------|------|--------|
| **Exercise Designer** | Create scaffolded tasks | Exercises with hints & solutions |
| **Project Architect** | Design capstone projects | Real-world project specifications |
| **Assessment Builder** | Create assessments | Quizzes, rubrics, checklists |
| **Solution Explainer** | Explain solutions | Step-by-step solutions, debugging tips |
| **Lab Environment Generator** | Setup lab environments | Tech stack, cost estimates |

### Stage 5: Quality Assurance
| Agent | Role | Output |
|-------|------|--------|
| **Pedagogical Reviewer** | Check learning alignment | Issues, improvement suggestions |
| **Clarity Checker** | Verify accessibility & bias | Readability analysis, bias fixes |
| **Difficulty Calibration** | Validate progression | Level alignment checks |
| **Consistency Auditor** | Check consistency | Terminology, formatting issues |
| **Accessibility Reviewer** | Verify WCAG 2.1 AA | Accessibility audit report |

---

## 📦 Data Models & Flow

```python
# Stage 1 Input
{
  "topic": "Azure Fundamentals",
  "level": "Beginner",
  "urls": ["https://..."]
}

# Stage 1 Output → Stage 2 Input
ResearchDossier {
  popular_courses: List[Course],
  common_modules: List[str],
  skill_gaps: List[str],
  audience_personas: List[Persona]
}

# Stage 2 Output → Stage 3 Input
CurriculumBlueprint {
  modules: List[ModuleBlueprint],
  learning_outcomes: List[str],
  total_duration: int
}

# Stage 3 Output (per Module)
ContentMaterial {
  lessons: List[Lesson],
  handouts: List[Handout],
  examples: List[Example]
}

# Stage 4 Output (per Module)
Assessment {
  exercises: List[Exercise],
  projects: List[Project],
  quizzes: List[Quiz]
}

# Stage 5 Output
QAReport {
  quality_scores: Dict[str, float],
  issues: List[Issue],
  recommendations: List[str]
}
```

---

## 🎯 Standardization Framework

### Naming Convention
```
[STAGE]_[TYPE]_[DESCRIPTOR]_[VERSION].ext

Examples:
- STAGE-1_RESEARCH_AZ-900_v1.0.json
- STAGE-2_CURRICULUM_AZURE_v1.0.json
- STAGE-3_LESSON_MOD-01_INTRO_v1.0.md
- STAGE-4_EXERCISE_MOD-02_EX-1_v1.0.json
- STAGE-5_QA-REPORT_AZURE_v1.0.json
```

### Metadata (All Artifacts)
```yaml
---
title: Module Title
version: 1.0
date_generated: 2026-02-05T14:30:00Z
stage: 3
module_id: MOD-01
author: Lesson Author Agent
language: en
encoding: utf-8
---
```

### Quality Metrics
```json
{
  "completeness": 0.95,        // 0-1
  "clarity_score": 8.5,        // 1-10
  "alignment_score": 0.95,     // 0-1
  "validation_status": "PASS", // PASS|WARNING|FAIL
  "flesch_kincaid_grade": 8.5,
  "accessibility_level": "AA"  // A|AA|AAA
}
```

---

## ⚙️ Configuration & Deployment Modes

### Model Selection Presets

**Lean Mode** (12GB VRAM)
```
All stages → Mistral-7B-Instruct
Speed: Fast | Quality: ⭐⭐⭐ | Cost: $
```

**Standard Mode** (24GB VRAM) - Recommended
```
All stages → Llama2-13B-Chat
Speed: Medium | Quality: ⭐⭐⭐⭐ | Cost: $$
```

**Pro Mode** (32GB+ VRAM)
```
Stage 1,2,3 → Llama2-13B
Stage 4     → DeepSeek V3.2
Stage 5     → Qwen3-Thinking
Speed: Slow | Quality: ⭐⭐⭐⭐⭐ | Cost: $$$
```

---

## 📈 Processing Timeline

| Stage | Time | Tasks | Output Size |
|-------|------|-------|-------------|
| **Stage 1** | 10-15 min | Research, analysis, personas | ~100KB |
| **Stage 2** | 5-10 min | Curriculum design | ~50KB |
| **Stage 3** | 30-45 min | 10 modules × 5 agents | ~5MB |
| **Stage 4** | 15-25 min | Exercises, quizzes, projects | ~2MB |
| **Stage 5** | 10-15 min | QA review, reporting | ~100KB |
| **TOTAL** | 70-110 min | Full pipeline | ~7MB |

---

## 🔍 Quality Gates

```
Input Validation
    ↓
Schema Validation (JSON)
    ↓
Markdown Linting
    ↓
Terminology Check (vs GLOSSARY.md)
    ↓
Accessibility Scan (WCAG 2.1 AA)
    ↓
Readability Analysis (Flesch–Kincaid)
    ↓
Quality Metrics ✓
    ↓
Output Validation
```

---

## 📊 Project Statistics

- **Total Agents**: 15
- **Total Crews**: 5
- **Data Models**: 20+
- **Validation Rules**: 50+
- **Standardization Standards**: 12
- **Quality Metrics**: 7
- **Supported Output Formats**: JSON, Markdown
- **Accessibility Standard**: WCAG 2.1 AA
- **Max Modules per Course**: 20+
- **Supported Difficulty Levels**: 3 (Beginner, Intermediate, Advanced)

---

## 🚀 Next Implementation Steps

1. ✅ **Infrastructure** - Core files created
2. 📋 **Crews** - Define Stage 1-5 tasks
3. 📋 **Utilities** - File handling, validation
4. 📋 **Schemas** - JSON validation schemas
5. 📋 **Templates** - Prompt & content templates
6. 📋 **Orchestration** - Main flow with HITL gates
7. 📋 **CLI** - Command-line interface
8. 📋 **Testing** - Unit & integration tests

---

**Last Updated**: February 5, 2026  
**Version**: 1.0.0 (Architecture)  
**Status**: Scaffolding Complete ✅
