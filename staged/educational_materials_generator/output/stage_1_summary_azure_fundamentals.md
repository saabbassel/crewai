# Stage 1 Output - Azure Fundamentals

**Status**: error
**Started**: 2026-02-06T10:13:06.001122Z
**Finished**: 2026-02-06T10:13:06.009206Z

## Error
```
Traceback (most recent call last):
  File "/Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator/flows/main_flow.py", line 53, in run_stage
    crew_output = run_discovery_crew(topic, urls)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator/src/crews/discovery_crew.py", line 121, in run_discovery_crew
    crew = create_discovery_crew(topic, urls)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator/src/crews/discovery_crew.py", line 26, in create_discovery_crew
    discovery_prompt = std_manager.get_stage_prompt("discovery")
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator/src/standardizer.py", line 260, in get_stage_prompt
    return self.get_stage_standards(stage_num)
           ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'St
```