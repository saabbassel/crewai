"""Main flow orchestration for the 5-stage pipeline.

This module orchestrates the execution of crews across 5 stages with
actual task execution via CrewAI.
"""
from typing import Dict, Any, List
import json
from datetime import datetime
import traceback

from src.config import Config
from src.utils.file_handler import ensure_dir, write_json, write_markdown
from src.agents import get_stage_agents
from src.crews.discovery_crew import run_discovery_crew
from src.crews.curriculum_crew import run_curriculum_crew
from src.crews.content_crew import run_content_crew
from src.crews.assessment_crew import run_assessment_crew
from src.crews.qa_crew import run_qa_crew


def _timestamp():
    return datetime.utcnow().isoformat() + "Z"


def run_stage(stage: int, manifest: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    """Run a single stage by executing its crew.

    Args:
        stage: Stage number (1-5)
        manifest: Parsed input manifest dict
        output_dir: Directory to write outputs

    Returns:
        stage_output: Dict containing aggregated outputs and metadata
    """
    ensure_dir(output_dir)
    stage_started = _timestamp()
    stage_result = {
        "stage": stage,
        "topic": manifest.get("topic"),
        "course_id": manifest.get("course_id"),
        "started_at": stage_started,
        "finished_at": None,
        "status": "running",
        "crew_output": None,
        "error": None,
    }

    try:
        topic = manifest.get("topic", "Unknown Topic")
        
        if stage == 1:
            urls = manifest.get("urls", [])
            crew_output = run_discovery_crew(topic, urls)
            stage_result["crew_output"] = crew_output
            stage_result["status"] = "completed"
            
        elif stage == 2:
            # In real scenario, pass Stage 1 results
            research_dossier = {"summary": "Stage 1 research (placeholder in this run)"}
            crew_output = run_curriculum_crew(topic, research_dossier)
            stage_result["crew_output"] = crew_output
            # If task expects strict JSON, attempt to parse the LLM output into JSON
            try:
                import json
                # crew_output may be dict with {'status':..., 'output': str}
                output_val = crew_output.get('output') if isinstance(crew_output, dict) else None
                if isinstance(output_val, str):
                    # Try direct parse
                    try:
                        parsed = json.loads(output_val)
                        stage_result['crew_output']['output'] = parsed
                    except Exception:
                        # Try to extract first JSON array substring
                        s = output_val
                        start = s.find('[')
                        end = s.rfind(']')
                        if start != -1 and end != -1 and end > start:
                            sub = s[start:end+1]
                            try:
                                parsed = json.loads(sub)
                                stage_result['crew_output']['output'] = parsed
                            except Exception:
                                stage_result['error'] = 'Stage 2: unable to parse JSON output from agent.'
                                stage_result['status'] = 'warning'
                        else:
                            stage_result['error'] = 'Stage 2: no JSON array found in agent output.'
                            stage_result['status'] = 'warning'
                else:
                    stage_result['status'] = 'completed'
            except Exception as e:
                stage_result['error'] = f'Post-processing error: {e}'
                stage_result['status'] = 'warning'
            
        elif stage == 3:
            curriculum = {"summary": "Stage 2 curriculum (placeholder in this run)"}
            crew_output = run_content_crew(topic, curriculum)
            stage_result["crew_output"] = crew_output
            stage_result["status"] = "completed"
            
        elif stage == 4:
            curriculum = {"summary": "Stage 2 curriculum (placeholder in this run)"}
            crew_output = run_assessment_crew(topic, curriculum)
            stage_result["crew_output"] = crew_output
            stage_result["status"] = "completed"
            
        elif stage == 5:
            all_materials = {"summary": "All materials from stages 1-4"}
            crew_output = run_qa_crew(topic, all_materials)
            stage_result["crew_output"] = crew_output
            stage_result["status"] = "completed"
            
        else:
            raise ValueError(f"Invalid stage: {stage}")

    except Exception as e:
        stage_result["status"] = "error"
        stage_result["error"] = traceback.format_exc()
        print(f"Error in stage {stage}: {e}")

    stage_result["finished_at"] = _timestamp()

    # Write stage artifact
    artifact_name = f"stage_{stage}_output_{manifest.get('course_id', 'course')}.json"
    artifact_path = f"{output_dir}/{artifact_name}"
    write_json(stage_result, artifact_path)

    # Create readable summary markdown
    md_lines = [f"# Stage {stage} Output - {manifest.get('topic')}", ""]
    md_lines.append(f"**Status**: {stage_result['status']}")
    md_lines.append(f"**Started**: {stage_result['started_at']}")
    md_lines.append(f"**Finished**: {stage_result['finished_at']}")
    
    if stage_result.get("crew_output"):
        md_lines.append("")
        md_lines.append("## Crew Output")
        md_lines.append("```json")
        try:
            md_lines.append(json.dumps(stage_result["crew_output"], indent=2, ensure_ascii=False))
        except Exception:
            md_lines.append(str(stage_result["crew_output"]))
        md_lines.append("```")
    
    if stage_result.get("error"):
        md_lines.append("")
        md_lines.append("## Error")
        md_lines.append("```")
        md_lines.append(stage_result["error"][:1000])
        md_lines.append("```")

    md_path = f"{output_dir}/stage_{stage}_summary_{manifest.get('course_id', 'course')}.md"
    write_markdown("\n".join(md_lines), md_path)

    return stage_result


def run_pipeline(manifest: Dict[str, Any], stages: List[int], base_output_dir: str) -> Dict[int, Dict[str, Any]]:
    """Run multiple stages sequentially and optionally pause for HITL.

    Returns a dict mapping stage number to stage_output.
    """
    ensure_dir(base_output_dir)
    outputs = {}

    for stage in stages:
        print(f"Running Stage {stage}...")
        out = run_stage(stage, manifest, base_output_dir)
        outputs[stage] = out

        # If HITL is enabled and the pipeline requests a pause after this stage, stop
        if Config.ENABLE_HITL:
            if (stage == 1 and Config.HITL_AFTER_DISCOVERY) or (stage == 2 and Config.HITL_AFTER_CURRICULUM) or (stage == 3 and Config.HITL_AFTER_CONTENT):
                print(f"HITL enabled and configured to pause after stage {stage}. Output written to {base_output_dir}.")
                return outputs

    return outputs
