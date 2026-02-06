"""Configuration management for educational materials generator.

This module loads configuration from `config.yaml` when present, and falls
back to environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except Exception:
    yaml = None

from dotenv import load_dotenv
try:
    from src.config_loader import ConfigLoader
except Exception:
    ConfigLoader = None

# Load environment variables
load_dotenv()


def _load_yaml_config() -> Dict[str, Any]:
    """Load config.yaml from workspace root if available."""
    # Walk up from this file to find config.yaml
    p = Path(__file__).resolve()
    for parent in list(p.parents)[:6]:
        candidate = parent / "config.yaml"
        if candidate.exists():
            if yaml:
                with open(candidate, "r") as fh:
                    return yaml.safe_load(fh) or {}
            else:
                # minimal parser: very limited, prefer installing pyyaml
                return {}
    return {}


class Config:
    """Central configuration manager.

    Attributes are loaded from `config.yaml` when present, otherwise from
    environment variables.
    """

    _yaml = _load_yaml_config()

    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", _yaml.get("ollama_base_url", "http://localhost:11434"))
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", str(_yaml.get("ollama_timeout", 120))))

    # Models (yaml under `models:` or env vars)
    DISCOVERY_MODEL: str = os.getenv("DISCOVERY_MODEL", _yaml.get("models", {}).get("discovery", "llama2:13b"))
    CURRICULUM_MODEL: str = os.getenv("CURRICULUM_MODEL", _yaml.get("models", {}).get("curriculum", "llama2:13b"))
    CONTENT_MODEL: str = os.getenv("CONTENT_MODEL", _yaml.get("models", {}).get("content", "llama2:13b"))
    ASSESSMENT_MODEL: str = os.getenv("ASSESSMENT_MODEL", _yaml.get("models", {}).get("assessment", "llama2:13b"))
    QA_MODEL: str = os.getenv("QA_MODEL", _yaml.get("models", {}).get("qa", "llama2:13b"))

    # Output
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", _yaml.get("output_dir", "./output"))
    ARCHIVE_OUTPUTS: bool = (os.getenv("ARCHIVE_OUTPUTS") or str(_yaml.get("archive_outputs", True))).lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", _yaml.get("log_level", "INFO"))

    # HITL
    ENABLE_HITL: bool = (os.getenv("ENABLE_HITL") or str(_yaml.get("hitl", {}).get("enable", True))).lower() == "true"
    HITL_AFTER_DISCOVERY: bool = (os.getenv("HITL_AFTER_DISCOVERY") or str(_yaml.get("hitl", {}).get("after_discovery", True))).lower() == "true"
    HITL_AFTER_CURRICULUM: bool = (os.getenv("HITL_AFTER_CURRICULUM") or str(_yaml.get("hitl", {}).get("after_curriculum", True))).lower() == "true"
    HITL_AFTER_CONTENT: bool = (os.getenv("HITL_AFTER_CONTENT") or str(_yaml.get("hitl", {}).get("after_content", False))).lower() == "true"
    APPROVAL_TIMEOUT: int = int(os.getenv("APPROVAL_TIMEOUT", str(_yaml.get("hitl", {}).get("approval_timeout", 300))))

    # Standardization
    ENFORCE_STANDARDS: bool = (os.getenv("ENFORCE_STANDARDS") or str(_yaml.get("standardization", {}).get("enforce", True))).lower() == "true"
    VALIDATE_SCHEMA: bool = (os.getenv("VALIDATE_SCHEMA") or str(_yaml.get("standardization", {}).get("validate_schema", True))).lower() == "true"
    CHECK_ACCESSIBILITY: bool = (os.getenv("CHECK_ACCESSIBILITY") or str(_yaml.get("standardization", {}).get("check_accessibility", True))).lower() == "true"

    # Performance
    PARALLEL_CONTENT_GENERATION: bool = (os.getenv("PARALLEL_CONTENT_GENERATION") or "true").lower() == "true"
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    CACHE_RESPONSES: bool = (os.getenv("CACHE_RESPONSES") or "true").lower() == "true"

    # Feature flags
    ENABLE_LEARNING_VARIANTS: bool = (os.getenv("ENABLE_LEARNING_VARIANTS") or "true").lower() == "true"
    GENERATE_FAILED_EXAMPLES: bool = (os.getenv("GENERATE_FAILED_EXAMPLES") or "true").lower() == "true"
    INCLUDE_QA_STAGE: bool = (os.getenv("INCLUDE_QA_STAGE") or "true").lower() == "true"

    @staticmethod
    def load_yaml():
        return Config._yaml


# ====================================
# LLM Configuration for CrewAI
# ====================================

class LLMConfig:
    """LLM configuration for CrewAI agents.
    
    Temperature settings per stage:
    - Stage 1 (Discovery): 0.7 - Analytical with some creativity
    - Stage 2 (Curriculum): 0.6 - Structured, focused design
    - Stage 3 (Content): 0.8 - Creative, varied writing styles
    - Stage 4 (Assessment): 0.7 - Rigorous, varied assessment types
    - Stage 5 (QA): 0.5 - Conservative, focused review
    
    All stages use Ollama with configurable base URL and timeout.
    """
    
    @staticmethod
    def get_llm_config(model: str, base_url: str = None, temperature: float = 0.7, top_p: float = 0.9):
        """Get LLM configuration for CrewAI.
        
        Args:
            model: Model name (e.g., "llama2:13b-chat")
            base_url: Ollama base URL (uses Config.OLLAMA_BASE_URL if None)
            temperature: Temperature for generation (0.0-1.0)
            top_p: Top-p sampling parameter (0.0-1.0)
            
        Returns:
            LLM instance configured for CrewAI
        """
        from crewai import LLM
        
        if base_url is None:
            base_url = Config.OLLAMA_BASE_URL
        
        return LLM(
            model=f"ollama/{model}",
            base_url=base_url,
            temperature=temperature,
            top_p=top_p,
            timeout=Config.OLLAMA_TIMEOUT,
        )
    
    @staticmethod
    def get_discovery_llm():
        """Get LLM for Stage 1: Discovery & Benchmarking.
        
        Temperature: 0.7 (analytical with creativity for gap analysis)
        Focus: Research, analysis, trend identification
        """
        return LLMConfig.get_llm_config(
            Config.DISCOVERY_MODEL,
            temperature=0.7,
            top_p=0.9,
        )
    
    @staticmethod
    def get_curriculum_llm():
        """Get LLM for Stage 2: Curriculum Architecture.
        
        Temperature: 0.6 (focused, structured curriculum design)
        Focus: Learning objectives, module sequencing, Bloom's alignment
        """
        # allow per-stage overrides from YAML (config/agents_stage2.yaml)
        if ConfigLoader:
            cfg = ConfigLoader.get_llm_config_for_stage(2) or {}
            temp = cfg.get('temperature', 0.6)
            top_p = cfg.get('top_p', 0.85)
            timeout = cfg.get('timeout', Config.OLLAMA_TIMEOUT)
            return LLMConfig.get_llm_config(
                Config.CURRICULUM_MODEL,
                temperature=temp,
                top_p=top_p,
            )
        return LLMConfig.get_llm_config(
            Config.CURRICULUM_MODEL,
            temperature=0.6,
            top_p=0.85,
        )
    
    @staticmethod
    def get_content_llm():
        """Get LLM for Stage 3: Content Production.
        
        Temperature: 0.8 (creative for varied writing styles)
        Focus: Lesson writing, examples, analogies, engaging content
        """
        return LLMConfig.get_llm_config(
            Config.CONTENT_MODEL,
            temperature=0.8,
            top_p=0.95,
        )
    
    @staticmethod
    def get_assessment_llm():
        """Get LLM for Stage 4: Assessment & Hands-On.
        
        Temperature: 0.7 (balanced rigor and variety)
        Focus: Exercises, quizzes, rubrics, project specs
        """
        return LLMConfig.get_llm_config(
            Config.ASSESSMENT_MODEL,
            temperature=0.7,
            top_p=0.9,
        )
    
    @staticmethod
    def get_qa_llm():
        """Get LLM for Stage 5: QA Review.
        
        Temperature: 0.5 (conservative, rigorous review)
        Focus: Quality checking, consistency, accessibility verification
        """
        return LLMConfig.get_llm_config(
            Config.QA_MODEL,
            temperature=0.5,
            top_p=0.8,
        )


if __name__ == "__main__":
    # Print current configuration
    print("Current Configuration:")
    print(f"OLLAMA_BASE_URL: {Config.OLLAMA_BASE_URL}")
    print(f"DISCOVERY_MODEL: {Config.DISCOVERY_MODEL}")
    print(f"CURRICULUM_MODEL: {Config.CURRICULUM_MODEL}")
    print(f"CONTENT_MODEL: {Config.CONTENT_MODEL}")
    print(f"ASSESSMENT_MODEL: {Config.ASSESSMENT_MODEL}")
    print(f"QA_MODEL: {Config.QA_MODEL}")
    print(f"OUTPUT_DIR: {Config.OUTPUT_DIR}")
