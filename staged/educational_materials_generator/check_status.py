#!/usr/bin/env python
"""Quick status check."""
import json
from pathlib import Path

print("\n" + "="*80)
print("PRODUCTION-READY OUTPUT REVIEW")
print("="*80 + "\n")

for s in [1,2,3,4,5]:
    f = Path('output') / f'stage_{s}_output_azure_fundamentals.json'
    
    if not f.exists():
        print(f"Stage {s}: ⏸️  NOT RUN YET")
        continue
    
    with open(f) as fp:
        data = json.load(fp)
    
    status = data.get('status')
    crew_output = data.get('crew_output', {})
    crew_status = crew_output.get('status') if isinstance(crew_output, dict) else 'N/A'
    
    if status == 'error':
        print(f"Stage {s}: ❌ ERROR")
    elif crew_status == 'demo':
        print(f"Stage {s}: ⚠️  DEMO MODE (not production-ready)")
    elif crew_status == 'completed':
        # Show content preview
        output = crew_output.get('output', '')
        if isinstance(output, str):
            preview = output[:200].replace('\n', ' ')
            print(f"Stage {s}: ✅ COMPLETED - {len(output)} chars")
            print(f"        Preview: {preview}...")
        else:
            print(f"Stage {s}: ✅ COMPLETED (JSON output)")
    else:
        print(f"Stage {s}: ❓ UNKNOWN STATUS ({status})")

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("[ ] Run Stage 2 (Curriculum Design)")
print("[ ] Run Stage 4 (Assessment Design)")  
print("[ ] Review all outputs for quality")
print("[ ] Export to production")
