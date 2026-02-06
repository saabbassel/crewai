#!/usr/bin/env python
"""Simple stage review interface."""

import json
import subprocess
from pathlib import Path

def show_stage_output(stage_num):
    """Display stage output."""
    output_file = Path("output") / f"stage_{stage_num}_output_azure_fundamentals.json"
    
    if not output_file.exists():
        print(f"❌ Stage {stage_num} output not found: {output_file}")
        return
    
    with open(output_file) as f:
        data = json.load(f)
    
    print(f"\n{'='*80}")
    print(f"STAGE {stage_num} OUTPUT")
    print(f"{'='*80}\n")
    
    print(f"Status: {data.get('status')}")
    print(f"Topic: {data.get('topic')}")
    print(f"Started: {data.get('started_at')}")
    print(f"Finished: {data.get('finished_at')}")
    
    if data.get('status') == 'error':
        print(f"\n⚠️ ERROR:")
        print(data.get('error', 'No error details')[:500])
    elif data.get('status') == 'completed':
        output = data.get('crew_output', {})
        if isinstance(output, dict):
            print(f"\nStatus: {output.get('status')}")
            content = output.get('output', '')
            if isinstance(content, str):
                # Truncate long content
                if len(content) > 1000:
                    print(f"\nContent preview (first 1000 chars):")
                    print(content[:1000])
                    print(f"\n... ({len(content) - 1000} more characters)")
                else:
                    print(f"\nContent:")
                    print(content)
            else:
                print(f"\nOutput (JSON):")
                print(json.dumps(content, indent=2)[:1000])
        else:
            print(f"\nOutput: {str(output)[:1000]}")

def run_stage(stage_num):
    """Run a specific stage."""
    print(f"\n🔄 Running Stage {stage_num}...")
    result = subprocess.run(
        [
            "/Users/b.saab/repos/.venv/bin/python",
            "main.py",
            "--input", "input/azure_fundamentals.json",
            "--stages", str(stage_num),
            "--output", "output"
        ],
        timeout=600,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Stage {stage_num} completed!")
        show_stage_output(stage_num)
    else:
        print(f"❌ Stage {stage_num} failed!")
        print(f"STDERR: {result.stderr[-500:]}")

def main():
    """Interactive menu."""
    while True:
        print(f"\n{'='*80}")
        print("STAGE REVIEW MENU")
        print(f"{'='*80}")
        print("[1-5]  View stage output")
        print("[R1-R5] Rerun stage")
        print("[Q]    Quit")
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice in ['1', '2', '3', '4', '5']:
            show_stage_output(int(choice))
        elif choice.startswith('r') and choice[1] in '12345':
            stage = int(choice[1])
            run_stage(stage)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
