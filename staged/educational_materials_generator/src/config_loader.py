"""YAML configuration loader for agents and tasks."""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

CONFIG_DIR = Path(__file__).parent.parent / "config"


class ConfigLoader:
    """Load and manage YAML configuration files."""
    
    @staticmethod
    def load_yaml(filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file.
        
        Args:
            filename: Name of the YAML file in config/ directory
            
        Returns:
            Parsed YAML content as dictionary
        """
        filepath = CONFIG_DIR / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_agents_for_stage(stage: int) -> Dict[str, Any]:
        """Load agent configurations for a specific stage.
        
        Args:
            stage: Stage number (1-5)
            
        Returns:
            Agent configurations with metadata
        """
        filename = f"agents_stage{stage}.yaml"
        return ConfigLoader.load_yaml(filename)
    
    @staticmethod
    def load_tasks_for_stage(stage: int) -> Dict[str, Any]:
        """Load task configurations for a specific stage.
        
        Args:
            stage: Stage number (1-5)
            
        Returns:
            Task configurations
        """
        filename = f"tasks_stage{stage}.yaml"
        return ConfigLoader.load_yaml(filename)
    
    @staticmethod
    def get_agent_config(stage: int, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific agent.
        
        Args:
            stage: Stage number (1-5)
            agent_id: Agent identifier
            
        Returns:
            Agent configuration or None if not found
        """
        agents_config = ConfigLoader.load_agents_for_stage(stage)
        
        for agent in agents_config.get('agents', []):
            if agent.get('id') == agent_id:
                return agent
        
        return None
    
    @staticmethod
    def get_task_config(stage: int, task_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific task.
        
        Args:
            stage: Stage number (1-5)
            task_id: Task identifier
            
        Returns:
            Task configuration or None if not found
        """
        tasks_config = ConfigLoader.load_tasks_for_stage(stage)
        
        for task in tasks_config.get('tasks', []):
            if task.get('id') == task_id:
                return task
        
        return None
    
    @staticmethod
    def list_agents_by_stage(stage: int) -> List[str]:
        """Get list of agent IDs for a stage.
        
        Args:
            stage: Stage number (1-5)
            
        Returns:
            List of agent IDs
        """
        agents_config = ConfigLoader.load_agents_for_stage(stage)
        return [agent.get('id') for agent in agents_config.get('agents', [])]
    
    @staticmethod
    def list_tasks_by_stage(stage: int) -> List[str]:
        """Get list of task IDs for a stage.
        
        Args:
            stage: Stage number (1-5)
            
        Returns:
            List of task IDs
        """
        tasks_config = ConfigLoader.load_tasks_for_stage(stage)
        return [task.get('id') for task in tasks_config.get('tasks', [])]
    
    @staticmethod
    def get_llm_config_for_stage(stage: int) -> Dict[str, Any]:
        """Get LLM configuration for a stage.
        
        Args:
            stage: Stage number (1-5)
            
        Returns:
            LLM configuration (temperature, top_p, timeout)
        """
        agents_config = ConfigLoader.load_agents_for_stage(stage)
        return agents_config.get('llm_config', {})
    
    @staticmethod
    def get_output_config_for_stage(stage: int) -> Dict[str, Any]:
        """Get output configuration for a stage.
        
        Args:
            stage: Stage number (1-5)
            
        Returns:
            Output format, schema, and validation config
        """
        tasks_config = ConfigLoader.load_tasks_for_stage(stage)
        return tasks_config.get('output', {})


if __name__ == "__main__":
    # Test loader
    print("=" * 80)
    print("YAML CONFIGURATION LOADER TEST")
    print("=" * 80)
    
    try:
        for stage in range(1, 6):
            print(f"\n📍 Stage {stage}:")
            
            # Load agents
            agents = ConfigLoader.list_agents_by_stage(stage)
            print(f"   Agents: {', '.join(agents)}")
            
            # Load tasks
            tasks = ConfigLoader.list_tasks_by_stage(stage)
            print(f"   Tasks: {', '.join(tasks)}")
            
            # Get LLM config
            llm_config = ConfigLoader.get_llm_config_for_stage(stage)
            print(f"   Temperature: {llm_config.get('temperature')}, Top-p: {llm_config.get('top_p')}")
        
        print("\n" + "=" * 80)
        print("✅ All configuration files loaded successfully")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
