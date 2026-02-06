"""Convenience wrapper to run the main flow from code or CLI."""
import json
from typing import List
from src.utils.file_handler import read_json, ensure_dir
from flows.main_flow import run_pipeline


def run_from_manifest(manifest_path: str, stages: List[int] = None, output_dir: str = "output"):
    manifest = read_json(manifest_path)
    ensure_dir(output_dir)
    if stages is None:
        stages = [1, 2, 3, 4, 5]
    return run_pipeline(manifest, stages, output_dir)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.flows.run_pipeline <manifest.json> [stages comma separated]")
        sys.exit(1)
    manifest_path = sys.argv[1]
    stages = None
    if len(sys.argv) >= 3:
        stages = [int(s) for s in sys.argv[2].split(",")]
    run_from_manifest(manifest_path, stages)
