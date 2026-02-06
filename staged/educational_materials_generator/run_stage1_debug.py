#!/usr/bin/env python
"""Debug runner for Stage 1 with full logging."""

import json
import traceback
import time
import os
import sys

# Set NO_FALLBACK for this run
os.environ['NO_FALLBACK'] = '1'

from src.crews.discovery_crew import run_discovery_crew

p = 'input/azure_fundamentals.json'
with open(p) as f:
    manifest = json.load(f)

print('=' * 80)
print('STAGE 1 BATCHED RUN WITH LOGGING')
print('=' * 80)
print(f"Topic: {manifest.get('topic')}")
print(f"URLs: {manifest.get('urls')}")
print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print('=' * 80 + '\n')

start = time.time()
try:
    res = run_discovery_crew(manifest.get('topic'), manifest.get('urls'))
    elapsed = time.time() - start
    print('\n' + '=' * 80)
    print(f'✅ SUCCESS in {elapsed:.1f}s')
    print('=' * 80)
    print(f"Status: {res.get('status')}")
    print(f"Output type: {type(res.get('output'))}")
    if isinstance(res.get('output'), dict):
        print(f"Output keys: {list(res['output'].keys())}")
        for key, val in res['output'].items():
            if isinstance(val, str):
                print(f"  {key}: {len(val)} chars")
            elif isinstance(val, dict):
                print(f"  {key}: {list(val.keys())}")
            else:
                print(f"  {key}: {type(val)}")
    else:
        out_str = str(res['output'])
        print(f"Output (first 500 chars):\n{out_str[:500]}")
except Exception as e:
    elapsed = time.time() - start
    print('\n' + '=' * 80)
    print(f'❌ FAILED after {elapsed:.1f}s')
    print('=' * 80)
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception message:\n{str(e)[:1000]}")
    print('\nTraceback:')
    traceback.print_exc()

print('\n' + '=' * 80)
print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print('=' * 80)
