#!/usr/bin/env python3
"""Test script for agent definitions and LLM configuration."""

from src.agents import get_all_agents, get_stage_agents

def test_agents():
    """Test all agent definitions."""
    print("=" * 80)
    print("EDUCATIONAL MATERIALS GENERATOR - AGENT CONFIGURATION TEST")
    print("=" * 80)
    
    try:
        all_agents = get_all_agents()
        total_agents = sum(len(a) for a in all_agents.values())
        
        print(f"\n✅ Successfully loaded {total_agents} agents across 5 stages\n")
        
        for stage_name, agents in all_agents.items():
            stage_num = stage_name.split("_")[1]
            print(f"📍 STAGE {stage_num}: {stage_name.upper()}")
            
            for agent in agents:
                print(f"   🤖 {agent.role}")
                if hasattr(agent, 'llm') and agent.llm:
                    model = agent.llm.model if hasattr(agent.llm, 'model') else 'configured'
                    print(f"      LLM: {model}")
            print()
        
        print("=" * 80)
        print("Agent Configuration Details:")
        print("-" * 80)
        
        # Test factory function
        stage_3_agents = get_stage_agents(3)
        print(f"✅ Stage 3 agents retrieved: {len(stage_3_agents)} agents")
        
        print("\n✅ All tests passed!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agents()
    exit(0 if success else 1)
