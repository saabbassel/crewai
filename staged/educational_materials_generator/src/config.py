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
    ENABLE_HITL: bool = os.getenv("ENABLE_HITL", "true").lower() == "true"
    HITL_AFTER_DISCOVERY: bool = os.getenv("HITL_AFTER_DISCOVERY", "true").lower() == "true"
    HITL_AFTER_CURRICULUM: bool = os.getenv("HITL_AFTER_CURRICULUM", "true").lower() == "true"
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
    """LLM configuration for CrewAI agents."""
    
    @staticmethod
    def get_llm_config(model: str, base_url: str = None):
        """Get LLM configuration for CrewAI."""
        from crewai import LLM
        
        if base_url is None:
            base_url = Config.OLLAMA_BASE_URL
        
        return LLM(
            model=f"ollama/{model}",
            base_url=base_url,
            temperature=0.7,
            top_p=0.9,
        )
    
    @staticmethod
    def get_discovery_llm():
        """Get LLM for Stage 1."""
        return LLMConfig.get_llm_config(Config.DISCOVERY_MODEL)
    
    @staticmethod
    def get_curriculum_llm():
        """Get LLM for Stage 2."""
        return LLMConfig.get_llm_config(Config.CURRICULUM_MODEL)
    
    @staticmethod
    def get_content_llm():
        """Get LLM for Stage 3."""
        return LLMConfig.get_llm_config(Config.CONTENT_MODEL)
    
    @staticmethod
    def get_assessment_llm():
        """Get LLM for Stage 4."""
        return LLMConfig.get_llm_config(Config.ASSESSMENT_MODEL)
    
    @staticmethod
    def get_qa_llm():
        """Get LLM for Stage 5."""
        return LLMConfig.get_llm_config(Config.QA_MODEL)


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
