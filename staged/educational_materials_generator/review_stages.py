#!/usr/bin/env python
"""Interactive stage review and approval system."""

import json
import os
import sys
from pathlib import Path
from flows.main_flow import run_pipeline

def load_json(filepath):
    """Load JSON file safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def show_output_summary(stage_num, output_data):
    """Display a readable summary of stage output."""
    if not output_data:
        return
    
    print(f"\n{'='*80}")
    print(f"STAGE {stage_num} OUTPUT REVIEW")
    print(f"{'='*80}\n")
    
    status = output_data.get("status", "unknown")
    print(f"Status: {status}")
    
    if status == "demo":
        print("⚠️  WARNING: Stage returned DEMO/FALLBACK output (crew execution failed)")
    elif status == "completed":
        print("✅ Stage produced output")
    
    # Show a preview of the output
    output = output_data.get("output", output_data.get("crew_output", {}))
    
    if isinstance(output, dict):
        print(f"\nOutput Preview (JSON):")
        try:
            preview = json.dumps(output, indent=2)
            lines = preview.split('\n')[:50]  # First 50 lines
            print('\n'.join(lines))
            if len(preview.split('\n')) > 50:
                print(f"\n... ({len(preview.split('\n')) - 50} more lines)")
        except:
            print(str(output)[:500])
    else:
        # String output
        preview = str(output)[:1000]
        print(f"\nOutput Preview (Text):")
        print(preview)
        if len(str(output)) > 1000:
            print(f"\n... ({len(str(output)) - 1000} more characters)")

def get_approval():
    """Get user approval for stage output."""
    while True:
        response = input("\n[A]pprove and continue | [R]erun this stage | [S]kip to next | [Q]uit: ").strip().lower()
        if response in ['a', 'r', 's', 'q']:
            return response
        print("Invalid choice. Please enter A, R, S, or Q")

def main():
    """Run interactive stage review."""
    input_file = "input/azure_fundamentals.json"
    output_dir = "output"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    # Load input manifest
    manifest = load_json(input_file)
    if not manifest:
        sys.exit(1)
    
    print(f"📚 Running stages for: {manifest.get('topic', 'Unknown')}")
    print(f"Level: {manifest.get('difficulty', 'Unknown')}")
    print(f"Duration: {manifest.get('duration_hours', 'Unknown')} hours\n")
    
    stages = [1, 2, 3, 4, 5]
    completed_stages = []
    
    for stage_num in stages:
        print(f"\n{'='*80}")
        print(f"Running Stage {stage_num}...")
        print(f"{'='*80}")
        
        # Run the pipeline for this stage
        try:
            run_pipeline(manifest, stages=[stage_num], base_output_dir=output_dir)
        except Exception as e:
            print(f"Error running stage {stage_num}: {e}")
            response = get_approval()
            if response == 'q':
                break
            elif response == 's':
                continue
            else:
                continue  # Retry
        
        # Load and show output
        output_file = f"{output_dir}/stage_{stage_num}_output_{manifest['topic'].lower().replace(' ', '_')}.json"
        output_data = load_json(output_file)
        
        if output_data:
            show_output_summary(stage_num, output_data)
            
            # Get approval
            while True:
                response = get_approval()
                
                if response == 'a':
                    print(f"✅ Stage {stage_num} approved!")
                    completed_stages.append(stage_num)
                    break
                elif response == 'r':
                    print(f"🔄 Rerunning Stage {stage_num}...")
                    try:
                        run_pipeline(manifest, stages=[stage_num], base_output_dir=output_dir)
                        output_data = load_json(output_file)
                        show_output_summary(stage_num, output_data)
                    except Exception as e:
                        print(f"Error rerunning stage: {e}")
                elif response == 's':
                    print(f"⏭️  Skipping Stage {stage_num}...")
                    break
                elif response == 'q':
                    print(f"\n⏹️  Stopping review process.")
                    return completed_stages
        else:
            print(f"Error: Could not load output file {output_file}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"REVIEW COMPLETE")
    print(f"{'='*80}")
    print(f"Approved stages: {completed_stages}")
    print(f"Total approved: {len(completed_stages)}/5")
    
    return completed_stages

if __name__ == "__main__":
    completed = main()
    sys.exit(0 if len(completed) == 5 else 1)
