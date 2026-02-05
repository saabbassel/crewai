"""Standardization utilities for educational content."""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class StandardizationManager:
    """Manages content standardization and metadata."""
    
    # ====================================
    # Naming Conventions
    # ====================================
    
    @staticmethod
    def generate_file_name(
        stage: int,
        content_type: str,
        descriptor: str,
        version: str = "1.0",
        extension: str = "json"
    ) -> str:
        """
        Generate standardized filename.
        
        Format: [STAGE]_[TYPE]_[DESCRIPTOR]_[VERSION].ext
        Example: STAGE-3_LESSON_MOD-01_INTRO_v1.0.md
        """
        return f"STAGE-{stage}_{content_type}_{descriptor}_v{version}.{extension}"
    
    @staticmethod
    def generate_module_id(index: int) -> str:
        """Generate module identifier: MOD-01, MOD-02, etc."""
        return f"MOD-{index:02d}"
    
    @staticmethod
    def generate_exercise_id(module_index: int, exercise_index: int) -> str:
        """Generate exercise identifier: MOD-02-EX-1"""
        return f"{StandardizationManager.generate_module_id(module_index)}-EX-{exercise_index}"
    
    @staticmethod
    def generate_quiz_id(module_index: int, quiz_index: int) -> str:
        """Generate quiz identifier: MOD-02-QUIZ-1"""
        return f"{StandardizationManager.generate_module_id(module_index)}-QUIZ-{quiz_index}"
    
    # ====================================
    # Metadata Generation
    # ====================================
    
    @staticmethod
    def create_metadata_header(
        title: str,
        stage: int,
        module_id: Optional[str] = None,
        version: str = "1.0",
        author: str = "Educational Materials Generator"
    ) -> Dict[str, Any]:
        """Create YAML frontmatter metadata."""
        return {
            "title": title,
            "version": version,
            "date_generated": datetime.now().isoformat(),
            "stage": stage,
            "module_id": module_id,
            "author": author,
            "language": "en",
            "encoding": "utf-8",
        }
    
    @staticmethod
    def create_metadata_footer(
        module_id: str,
        version: str = "1.0",
        author: str = "Educational Materials Generator"
    ) -> str:
        """Create markdown metadata footer."""
        return f"\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d')} | Module: {module_id} | Version: {version} | Author: {author}*"
    
    @staticmethod
    def yaml_to_markdown(metadata: Dict[str, Any]) -> str:
        """Convert metadata dict to YAML frontmatter."""
        lines = ["---"]
        for key, value in metadata.items():
            if isinstance(value, str):
                lines.append(f"{key}: {value}")
            else:
                lines.append(f"{key}: {json.dumps(value)}")
        lines.append("---\n")
        return "\n".join(lines)
    
    # ====================================
    # Quality Metrics
    # ====================================
    
    @staticmethod
    def create_quality_metrics(
        completeness: float = 1.0,
        clarity_score: float = 8.0,
        alignment_score: float = 0.95,
        validation_status: str = "PASS"
    ) -> Dict[str, Any]:
        """Create standardized quality metrics."""
        return {
            "completeness": min(1.0, max(0.0, completeness)),
            "clarity_score": min(10.0, max(1.0, clarity_score)),
            "alignment_score": min(1.0, max(0.0, alignment_score)),
            "validation_status": validation_status,
        }
    
    # ====================================
    # Standardization Prompts
    # ====================================
    
    @staticmethod
    def get_standards_prompt() -> str:
        """Get universal standardization prompt for all agents."""
        return """You are generating educational content. Follow these STRICT standards:

NAMING CONVENTION:
- Use format: [STAGE]_[TYPE]_[DESCRIPTOR]_[VERSION].ext
- Example: STAGE-3_LESSON_MOD-01_INTRO_v1.0.md
- Replace spaces with underscores

METADATA HEADER (All Artifacts):
Include YAML frontmatter at the top:
---
title: [Title]
version: 1.0
date_generated: [ISO 8601 date]
stage: [1-5]
module_id: [MOD-XX or null]
author: [Your name]
language: en
encoding: utf-8
---

MARKDOWN FORMATTING:
- Use ONLY heading levels: # → ## → ### (no skipping levels)
- Define ALL acronyms on first mention: "Cloud Service Provider (CSP)"
- Keep paragraphs ≤3 sentences for readability
- Use **bold** for key terms, *italic* for book titles
- Tables must have headers with proper formatting
- Code blocks must include language identifier

JSON STRUCTURE:
- All JSON must include "metadata" and "quality_metrics" fields
- Include version number: "version": "1.0"
- Use ISO 8601 dates: "generated_at": "2026-02-05T14:30:00Z"
- Validate against provided JSON schema

TERMINOLOGY:
- Check GLOSSARY.md for approved definitions
- Maintain consistent terminology across all content
- First use format: "Term (abbreviation)"
- Use Title Case for concepts: "Resource Groups", "Virtual Machines"

LEARNING OUTCOMES:
Follow Bloom's taxonomy: [LEVEL]: [Action Verb] [Content]
Examples:
- REMEMBER: Define cloud computing and its characteristics
- UNDERSTAND: Explain differences between IaaS, PaaS, SaaS
- APPLY: Deploy a virtual machine on Azure Portal
- ANALYZE: Compare pricing models
- EVALUATE: Judge when to use VMs vs. App Services
- CREATE: Design scalable architecture

QUALITY REQUIREMENTS:
- Flesch–Kincaid grade level: Match target level ± 1
- Clarity score target: 8+/10
- Completeness: All required sections filled
- No jargon without explanation
- Links are descriptive (not "click here")

ACCESSIBILITY (WCAG 2.1 AA):
- All images have alt-text: ![Description](path.png)
- Heading hierarchy correct (no skips)
- Color contrast ≥4.5:1
- Lists use proper markdown formatting (- or 1.)
- No auto-playing media
- Reading level appropriate for audience

METADATA FOOTER (Markdown):
Include at bottom:
---
*Generated: [Date] | Module: [MOD-XX] | Version: [X.Y] | Author: [Name]*

BEFORE YOU RESPOND:
1. Confirm you understand these standards
2. Plan your output structure
3. Generate content following ALL requirements
4. Validate against standards
5. Include quality metrics in your output

If any requirement is unclear, ask for clarification."""
    
    @staticmethod
    def get_stage_specific_prompt(stage: int) -> str:
        """Get stage-specific standardization requirements."""
        stage_prompts = {
            1: """Additional Stage 1 (Discovery) Standards:
- Research data must include: platforms, duration, ratings, key modules
- Personas must include: background, goals, learning time, difficulty level
- Skill gaps should identify 5+ gaps with industry relevance
- All sources must be citeable with URLs
- Include completeness and clarity metrics""",
            
            2: """Additional Stage 2 (Curriculum) Standards:
- All objectives must map to Bloom's taxonomy levels
- Prerequisites must form valid chains (no circular dependencies)
- Module duration: 30-90 minutes optimal
- Each objective linked to ≥1 assessment
- Include learning progression narrative
- Difficulty must increase gradually across modules""",
            
            3: """Additional Stage 3 (Content) Standards:
- Include worked examples (at least 1 per concept)
- Add "Common Mistakes" sections
- Handouts must fit on 1 page (8.5" x 11")
- Include 2+ learning style variants if enabled
- References must be formatted consistently
- Include visual descriptions for accessibility""",
            
            4: """Additional Stage 4 (Assessment) Standards:
- Exercises must have 2-5 success criteria
- Quizzes include explanation for ALL answers
- Rubrics use 4-point scale: Novice→Developing→Proficient→Advanced
- Projects include realistic industry scenarios
- Cost estimates provided for cloud resources
- Solution explanations show common wrong paths""",
            
            5: """Additional Stage 5 (QA) Standards:
- Issues tracked with unique IDs: ISSUE-001
- Severity levels: critical > high > medium > low
- Quality scores: 0-1 (completeness, alignment) or 1-10 (clarity)
- Accessibility audit includes WCAG 2.1 AA checklist
- Terminology consistency verified against GLOSSARY.md
- Formatting violations documented with specific fixes""",
        }
        
        return stage_prompts.get(stage, "")


class AccessibilityChecker:
    """Checks content for WCAG 2.1 AA compliance."""
    
    @staticmethod
    def check_heading_hierarchy(content: str) -> bool:
        """Verify heading levels don't skip (no # → ### without ##)."""
        import re
        headings = re.findall(r'^(#{1,6})\s', content, re.MULTILINE)
        if not headings:
            return True
        
        levels = [len(h) for h in headings]
        for i in range(1, len(levels)):
            if levels[i] - levels[i-1] > 1:
                return False  # Skipped level
        return True
    
    @staticmethod
    def check_link_text(content: str) -> list:
        """Find non-descriptive link text like 'click here'."""
        import re
        bad_links = re.findall(r'\[(click here|here|link)\]\(', content, re.IGNORECASE)
        return bad_links
    
    @staticmethod
    def check_alt_text(content: str) -> list:
        """Find images without alt-text."""
        import re
        # Valid: ![alt text](path)
        # Invalid: ![](path)
        invalid_alts = re.findall(r'!\[\]\(', content)
        return invalid_alts


if __name__ == "__main__":
    # Test standardization functions
    print("Testing Standardization:")
    print(f"Module ID: {StandardizationManager.generate_module_id(3)}")
    print(f"Exercise ID: {StandardizationManager.generate_exercise_id(2, 1)}")
    print(f"File name: {StandardizationManager.generate_file_name(3, 'LESSON', 'MOD-01_INTRO')}")
    print("\nQuality Metrics:")
    print(json.dumps(StandardizationManager.create_quality_metrics(), indent=2))
