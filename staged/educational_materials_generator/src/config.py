"""Configuration management for educational materials generator."""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Central configuration manager."""
    
    # ====================================
    # Ollama Configuration
    # ====================================
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))
    
    # ====================================
    # Model Selection by Stage
    # ====================================
    DISCOVERY_MODEL: str = os.getenv("DISCOVERY_MODEL", "llama2:13b-chat")
    CURRICULUM_MODEL: str = os.getenv("CURRICULUM_MODEL", "llama2:13b-chat")
    CONTENT_MODEL: str = os.getenv("CONTENT_MODEL", "llama2:13b-chat")
    ASSESSMENT_MODEL: str = os.getenv("ASSESSMENT_MODEL", "llama2:13b-chat")
    QA_MODEL: str = os.getenv("QA_MODEL", "llama2:13b-chat")
    
    # ====================================
    # Output Configuration
    # ====================================
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./output")
    ARCHIVE_OUTPUTS: bool = os.getenv("ARCHIVE_OUTPUTS", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # ====================================
    # HITL Configuration
    # ====================================
    # Disable HITL by default for unattended pipeline runs; can be enabled via env var
    ENABLE_HITL: bool = os.getenv("ENABLE_HITL", "false").lower() == "true"
    HITL_AFTER_DISCOVERY: bool = os.getenv("HITL_AFTER_DISCOVERY", "false").lower() == "true"
    HITL_AFTER_CURRICULUM: bool = os.getenv("HITL_AFTER_CURRICULUM", "false").lower() == "true"
    HITL_AFTER_CONTENT: bool = os.getenv("HITL_AFTER_CONTENT", "false").lower() == "true"
    APPROVAL_TIMEOUT: int = int(os.getenv("APPROVAL_TIMEOUT", "300"))
    
    # ====================================
    # Standardization Configuration
    # ====================================
    ENFORCE_STANDARDS: bool = os.getenv("ENFORCE_STANDARDS", "true").lower() == "true"
    VALIDATE_SCHEMA: bool = os.getenv("VALIDATE_SCHEMA", "true").lower() == "true"
    CHECK_ACCESSIBILITY: bool = os.getenv("CHECK_ACCESSIBILITY", "true").lower() == "true"
    GRADE_LEVEL_TARGET: int = int(os.getenv("GRADE_LEVEL_TARGET", "9"))
    
    # ====================================
    # Performance Configuration
    # ====================================
    PARALLEL_CONTENT_GENERATION: bool = os.getenv("PARALLEL_CONTENT_GENERATION", "true").lower() == "true"
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    CACHE_RESPONSES: bool = os.getenv("CACHE_RESPONSES", "true").lower() == "true"
    
    # ====================================
    # Feature Flags
    # ====================================
    ENABLE_LEARNING_VARIANTS: bool = os.getenv("ENABLE_LEARNING_VARIANTS", "true").lower() == "true"
    GENERATE_FAILED_EXAMPLES: bool = os.getenv("GENERATE_FAILED_EXAMPLES", "true").lower() == "true"
    INCLUDE_QA_STAGE: bool = os.getenv("INCLUDE_QA_STAGE", "true").lower() == "true"
    
    # ====================================
    # Model Presets
    # ====================================
    
    @staticmethod
    def get_lean_preset():
        """Configure for lean mode (fastest, lowest quality)."""
        return {
            "DISCOVERY_MODEL": "mistral:7b-instruct",
            "CURRICULUM_MODEL": "mistral:7b-instruct",
            "CONTENT_MODEL": "mistral:7b-instruct",
            "ASSESSMENT_MODEL": "mistral:7b-instruct",
            "QA_MODEL": "mistral:7b-instruct",
        }
    
    @staticmethod
    def get_standard_preset():
        """Configure for standard mode (recommended)."""
        return {
            "DISCOVERY_MODEL": "llama2:13b-chat",
            "CURRICULUM_MODEL": "llama2:13b-chat",
            "CONTENT_MODEL": "llama2:13b-chat",
            "ASSESSMENT_MODEL": "llama2:13b-chat",
            "QA_MODEL": "llama2:13b-chat",
        }
    
    @staticmethod
    def get_pro_preset():
        """Configure for pro mode (best quality, high resource usage)."""
        return {
            "DISCOVERY_MODEL": "llama2:13b-chat",
            "CURRICULUM_MODEL": "mixtral:8x7b",
            "CONTENT_MODEL": "mixtral:8x7b",
            "ASSESSMENT_MODEL": "deepseek-v3.2-speciale",
            "QA_MODEL": "qwen:30b",
        }
    
    @staticmethod
    def apply_preset(preset_name: str):
        """Apply a model preset."""
        presets = {
            "lean": Config.get_lean_preset(),
            "standard": Config.get_standard_preset(),
            "pro": Config.get_pro_preset(),
        }
        
        if preset_name not in presets:
            raise ValueError(f"Unknown preset: {preset_name}")
        
        preset = presets[preset_name]
        for key, value in preset.items():
            setattr(Config, key, value)


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
