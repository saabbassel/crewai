"""Stage 2 Curriculum Crew - Architecture and design."""

from crewai import Agent, Task, Crew
from src.agents import CurriculumAgents
from src.standardizer import StandardizationManager
from src.config_loader import ConfigLoader
import json
import math


def create_curriculum_crew(topic: str, research_dossier: dict):
    """Create Stage 2 Curriculum crew."""
    
    designer = CurriculumAgents.curriculum_designer()
    id_expert = CurriculumAgents.instructional_designer()
    
    std_manager = StandardizationManager()
    curr_prompt = std_manager.get_stage_prompt("curriculum")
    
    # Load task configurations from YAML
    design_cfg = ConfigLoader.get_task_config(2, 'design_curriculum_task') or {}
    instr_cfg = ConfigLoader.get_task_config(2, 'map_instruction_task') or {}

    # Determine target module count and batch size
    min_modules = int(design_cfg.get('min_modules', 8))
    max_modules = int(design_cfg.get('max_modules', 12))
    batch_size = int(design_cfg.get('batch_size', 4))
    # Choose target_count = max_modules to aim for full coverage
    target_count = max_modules

    # Helper to run a single task (one batch) and parse JSON array output
    def _run_batch(agent, batch_desc):
        task = Task(description=batch_desc, agent=agent, expected_output="JSON array of modules")
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        res = crew.kickoff()
        # Extract textual answer from res - prefer dictionary access when available
        text = None
        try:
            # Attempt to find answer in usual structures
            if isinstance(res, dict):
                # Crew result may contain tasks outputs; join any string outputs
                for v in res.values():
                    if isinstance(v, str) and v.strip():
                        text = v
                        break
                    if isinstance(v, dict) and 'output' in v:
                        text = v.get('output')
                        break
            if not text:
                text = str(res)
        except Exception:
            text = str(res)

        # Try to parse JSON directly, else extract first JSON array substring
        try:
            parsed = json.loads(text)
            return parsed
        except Exception:
            s = text
            start = s.find('[')
            end = s.rfind(']')
            if start != -1 and end != -1 and end > start:
                sub = s[start:end+1]
                try:
                    parsed = json.loads(sub)
                    return parsed
                except Exception:
                    return None
            return None

    # Build batch descriptions and run sequentially
    modules = []
    batches = []
    i = 1
    while i <= target_count:
        end_i = min(i + batch_size - 1, target_count)
        batches.append((i, end_i))
        i = end_i + 1

    for (start_i, end_i) in batches:
        # Build instruction for this batch
        ids_note = f"Generate modules {start_i} through {end_i}."
        if design_cfg.get('output_instructions'):
            batch_desc = f"{design_cfg.get('output_instructions')}\n\n{ids_note}\n\nContext: Generate curriculum for '{topic}'."
        else:
            batch_desc = f"Produce a JSON array of modules {start_i}-{end_i} for '{topic}'. Each module: id,title,duration_hours,learning_objectives,prerequisites,teaching_methods,practice_activities,assessment_type,estimated_time_hours."

        batch_res = _run_batch(designer, batch_desc)
        if isinstance(batch_res, list):
            modules.extend(batch_res)
        else:
            # If parsing failed, fallback to demo for now and break
            print(f"⚠️  Batch {start_i}-{end_i} returned non-JSON output; falling back to demo for Stage 2")
            return {
                "status": "demo",
                "output": {
                    "modules": [
                        {"id": "MOD-01", "title": "Fundamentals", "duration": 4},
                        {"id": "MOD-02", "title": "Core Services", "duration": 6},
                        {"id": "MOD-03", "title": "Advanced Topics", "duration": 5}
                    ]
                }
            }

    # Trim or validate module count
    if len(modules) < min_modules or len(modules) > max_modules:
        print(f"⚠️  Generated {len(modules)} modules (expected {min_modules}-{max_modules})")
        status = "warning"
    else:
        status = "completed"

    # Now create instructional mapping task using instructional designer
    # Instructional task will receive the merged modules
    instr_desc = instr_cfg.get('output_instructions', '') + f"\n\nContext: For the modules provided, map instructional strategies for '{topic}'."
    # Use id_expert agent to run mapping
    instr_task = Task(description=instr_desc, agent=id_expert, expected_output=instr_cfg.get('expected_output', 'JSON mapping'))
    instr_crew = Crew(agents=[id_expert], tasks=[instr_task], verbose=False)
    instr_res = instr_crew.kickoff()

    return {"status": status, "output": {"modules": modules, "instructional_mapping": instr_res}}
    
    crew = Crew(
        agents=[designer, id_expert],
        tasks=[design_task, instructional_task],
        verbose=True,
    )
    
    return crew


def run_curriculum_crew(topic: str, research_dossier: dict):
    """Execute curriculum crew. Falls back to demo mode if Ollama unavailable."""
    try:
        crew_or_result = create_curriculum_crew(topic, research_dossier)
        # If the creator already executed batches and returned a result dict, return it directly
        if isinstance(crew_or_result, dict):
            return crew_or_result
        # Otherwise it's a Crew instance - run it
        result = crew_or_result.kickoff()
        return {"status": "completed", "output": str(result)}
    except Exception as e:
        import traceback
        print(f"❌ Stage 2 Curriculum Crew Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        if "not found" in str(e).lower() or "connection" in str(e).lower():
            print(f"⚠️  Using demo mode for Stage 2 (model unavailable)")
        else:
            print(f"⚠️  Using demo mode for Stage 2 (crew execution failed)")
            
        return {
            "status": "demo",
                "output": {
                    "modules": [
                        {"id": "MOD-01", "title": "Fundamentals", "duration": 4},
                        {"id": "MOD-02", "title": "Core Services", "duration": 6},
                        {"id": "MOD-03", "title": "Advanced Topics", "duration": 5}
                    ]
                }
            }
