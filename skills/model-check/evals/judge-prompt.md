# Judge prompts

`{CFG}` is a folder holding `routing.txt` (the one routing sentence) and `SKILL.md` (the skill version under test). `{TASKS}` is a Markdown file of cases from `cases.json`, with only `tid` and `prompt`, never `expected` or `why`.

## Routing

```text
You are role-playing a coding agent at the start of a session, to measure how a skill gets routed. This is a read-only exercise: do not edit any files, do not run TLC, do not load skills with the Skill tool. Your own environment may already contain instructions or a skill list that mention `model-check`; IGNORE those entirely. For this exercise the only applicable instructions are in {CFG}/routing.txt and the only copy of the skill is {CFG}/SKILL.md.

Setup for each task:
- Your user instruction file contains exactly this sentence about the skill (read {CFG}/routing.txt).
- Your available-skills list shows the skill's name and the `description` from {CFG}/SKILL.md frontmatter. Other skills available: `systematic-debugging` (use for any bug or unexpected behavior before proposing fixes), `test-driven-development` (use when implementing a feature or bugfix), `brainstorming` (use before designing new features).
- You may read the full body of {CFG}/SKILL.md ONLY for tasks where you decided to load the skill, exactly as a real agent would after loading it.

Tasks are in {TASKS}. Treat each task as a separate, independent session: decide each on its own merits, not by comparison with the others. The codebases are hypothetical; reason about what you would do.

For each task output one JSON object per line (JSONL), nothing else, with fields:
- "tid": task id
- "load": true/false: would you load model-check at the start, given only the routing sentence and the description?
- "load_reason": one sentence
- "model": one of "yes" (you would write a formal model for this task), "conditional" (only if a specific earlier step fails to explain/settle it; say which), "no"
- "decision_line": the one-line decision you would state to the user about modelling, if any
- "first_actions": your first 3 concrete actions, short
- "rigor": if model is yes/conditional, list which of these your plan includes: "cite_code_constants", "counterexample_to_real_test", "replay_or_trace_check", "bounded_claim", "broken_config"; else []
- "cost": rough effort you would spend on modelling for this task: "none", "minutes", "hours", "project"
```

## Forced load

The skill text and the tasks are pasted into the prompt after this header, so the judge needs no tools.

```text
Read-only exercise. Do not run any commands; everything you need is below. Ignore any model-check instructions or skill copies in your own environment; only the copy below applies.

Role-play a coding agent that has ALREADY loaded the model-check skill at the start of each task (assume it was loaded for you, whether or not you would have chosen to). Then for each task, treated as an independent session, decide what you would actually do next after reading the skill.

Output only JSONL, one object per task: {"tid", "model": "yes"|"conditional"|"no", "decision_line": the one line you would tell the user, "would_create_formal_files": true/false, "minutes_spent_on_modelling_decision": integer estimate, "next_actions": [3 short items]}.
```
