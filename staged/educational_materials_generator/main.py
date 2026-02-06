"""CLI runner for the educational materials pipeline.

Example:
  python main.py --input input/azure_fundamentals.json --stages 1
"""
import argparse
from typing import List
import json
from src.config import Config
from src.utils.file_handler import read_json, ensure_dir
from flows.main_flow import run_pipeline


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="Path to input manifest (JSON)")
    p.add_argument("--stages", "-s", default="1", help="Comma-separated stages to run (e.g., 1 or 1,2,3)")
    p.add_argument("--output", "-o", default=Config.OUTPUT_DIR, help="Output directory")
    return p.parse_args()


def main():
    args = parse_args()
    manifest = read_json(args.input)
    stages = [int(s) for s in args.stages.split(",")]
    ensure_dir(args.output)

    print(f"📚 Starting pipeline for {manifest.get('topic')} (stages: {stages})")
    results = run_pipeline(manifest, stages, args.output)

    print("✅ Pipeline finished. Stage outputs written to:")
    for st, out in results.items():
        print(f" - Stage {st}: output file in {args.output}")

    # If HITL was triggered, remind user where to review
    if Config.ENABLE_HITL:
        print("HITL is enabled — please review outputs in the output directory before continuing next stages.")


if __name__ == "__main__":
    main()
