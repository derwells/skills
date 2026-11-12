# Changelog

## Unreleased

- Rebuilt teaching on the Socratic method from Jane Street's `socratic-tutor` skill (MIT, commit `7c6715c`): a guard against one-off questions, a diagnostic before any teaching, a skill map with levels 0-5, one question at a time, narrower questions after a wrong answer, strict evaluation, spaced review, and a final mixed assessment. `NOTICE.md` holds the license and lists what was kept and what was added.
- Answers are in the learner's own words. Multiple choice is no longer the default form of a check, and the tutor no longer asks for a 1-5 confidence rating. A selected option counts as recognition and needs a stated reason.
- `progress.json` records a `level` per concept with the checks behind it. The older `understanding` labels stay in existing courses as history and are never converted to levels. Older teaching-method rules in a course (course styles, reading-first, optional questions) are superseded without asking the learner again; the old text stays beside a dated note.
- `SKILL.md` is about half its former size. Saved-course rules moved to `references/courses.md`, which loads only for a course session.
- Replaced `references/lesson-craft.md` with `references/question-craft.md`. Course creation now prepares a skill tree, diagnostic questions, and question sets in place of lesson notes.
- Removed the `tutorial` and `design-partner` course styles for new courses, the professor-led lesson structure, the two-or-three-explanations check rhythm, and the limit of one optional revisit.
- The Discord adapter keeps its answer buttons as an option the learner can ask for. Existing prompts and course records keep their meaning.
- Added `evals/`: scripted teaching exchanges with free-text answers, run against the previous version and this one.
- Simulated and agent-operated interactions never count as learner evidence.
- Moved to `skills/learn/` when the repository became a collection of skills. Existing clones need the migration steps in the top-level README. The `learn-standalone` tag keeps the old single-skill layout.
- Notebook guidance keeps answers to open questions out of the learner's view, and an exercise counts only when the tutor sees the learner's actual output.

## 1.1.0 — 2026-09-16

- New "explanation standard": fit test for examples (minimal instance, or an analogy with its map written), two-registers-one-claim check, mechanism before machinery, one vetted canonical example per key intuition chosen at research time
- Turn shape: explain, then stop. No probe, question or menu attached to an explanation turn; probes come after the idea has sat, one per idea at most
- 30 minutes is a guideline for energy, not a target or coverage quota
- Lesson notebooks: one Jupyter notebook per lesson for code and figures, executed before any cell is referenced (`references/notebooks.md`)
- `spell-out` length permission waived inside lessons; design-partner style no longer "a colleague thinking out loud"
- SKILL.md cut by about a third: rule justifications trimmed to a clause

## 1.0.0 — 2026-09-01

First public release.

- Intuition-first tutoring: analogies and dialogue first, exercises as probes rather than gates
- Persistent tutor notebook (`progress.json`) plus a cross-course learner profile (`learner.md`)
- Write integrity rules: mid-session checkpoints, JSON validated after every write
- Modes: `new`, session (default), `review`, `status`, `curate`
- Two course styles: `tutor` (probed) and `design-partner` (briefed)
- Course contract: earned, numbered rules read first every session
- Freshness policy for fast-moving topics, with lazy per-unit research
- Mode playbooks split into `references/` so sessions load only what they need
- Frontmatter kept to the Agent Skills open-spec fields — portable across Claude Code, opencode, Codex, Gemini CLI
