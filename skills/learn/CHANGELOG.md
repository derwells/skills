# Changelog

## Unreleased

- Moved to `skills/learn/` when the repository became a collection of skills. Existing clones need the migration steps in the top-level README. The `learn-standalone` tag keeps the old single-skill layout.
- Rebuilt teaching around professor-led lessons with a central question, developed reasoning, contrasts, and guided application.
- Removed the fixed explanation length, mandatory stops, delayed-question rules, and automatic probe backlog.
- Expanded course preparation to include worked solutions, comparisons, assumptions, and tasks with decreasing help.
- Added `unassessed` understanding and optional evidence records; preserved existing course histories and explicit preferences.
- Updated notebook guidance to keep prediction answers separate from executed demonstrations.
- Added migration guidance for existing courses and revised curation to repair teaching materials as well as contracts.

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
