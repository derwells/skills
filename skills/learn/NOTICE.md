# Notice

The teaching method in this skill is adapted from Jane Street's `socratic-tutor` skill.

- Source: <https://github.com/janestreet/agent_skills>, file `socratic-tutor/SKILL.md`
- Commit: `7c6715c29548a3b39d4a9545c698ee4fd17a7213` (branch `master`, 2026-11-03)
- License: MIT, reproduced at the end of this file

Text in `SKILL.md` under "Confirm intent before starting", "Session start", "Skill map", "Teaching loop", "Evaluation rules", "Mastery and completion" and "Commands the learner can use anytime" is adapted from that file. Everything else in this folder is covered by [LICENSE](LICENSE).

## What comes from Jane Street

| Rule | Status here |
|---|---|
| Guard: answer one-off questions normally; confirm unclear intent with one short question | Kept. `/learn <topic>` is added to the phrases that count as a clear request |
| Break the topic into 4-10 subskills; a two-level tree for broad topics | Kept. In a saved course, units are the branches and concepts are the subskills |
| Announce the diagnostic; 3-5 questions from easy to hard; teach nothing until it is done | Kept. Added: do not correct or explain between diagnostic questions |
| Show the map and propose where to start; the learner may override | Kept |
| Levels 0-5 and their meanings | Kept |
| Text map with block-character bars, rendered after every level change and on request | Kept. Added: `?/5` for a subskill with no level, a stated formula for the overall percentage, and a code block where the font is not fixed-width |
| One question at a time; end the message at the question | Kept |
| Question kinds: predict, explain why, find the flaw, apply to a new case, connect two ideas | Kept |
| Wrong answer: do not give the answer; ask a narrower question; explain only after 2-3 failed attempts, then re-test from a different angle | Kept |
| Right answer: occasionally play devil's advocate | Kept |
| Short explanations only for new material the learner could not derive | Kept |
| Practical exercises; check actual output, not a description | Kept. Notebooks are where a saved course does this |
| Levels are earned: 2+ independent checks, at least one unprompted recall | Kept |
| A vague or partial answer is not correct; attribute no insight the learner did not express | Kept |
| Spaced review without warning; a failed review lowers the level | Kept. Added: lower by one unless the answer shows more, and time alone lowers nothing |
| Level 5 needs an edge case and a teachable explanation | Kept |
| Do not flatter | Kept |
| End only when every subskill is at target (4/5, or 5/5 on request), then a final mixed assessment | Kept. A saved course applies it per unit and again across units |
| Commands: show progress, harder, easier, just tell me, save state, resume from | Kept. In a saved course, "save state" writes the course files |

## What is added or changed here

These are choices made in this collection. Jane Street's skill does not contain them.

- **Free text by default.** Answers are in the learner's own words. Options are offered only when the learner asks. A selected option counts as recognition and needs a stated reason before it is a check.
- **A list of what is not a check**: silence, assent, "I know this", a confidence rating, a told answer, a bare selection.
- **Saved courses**: the `.learning/` layout, `progress.json` with `level`, `level_set` and per-check evidence, session logs, course research, and the freshness policy.
- **Older course records**: the `understanding` labels are kept as history and never converted to levels. A conflict between a recorded learner choice and this method is put to the learner once.
- **What a question needs**: the material in the message, new material stated before it is used, a direct answer to "wait, what is X?", checking the answer key before correcting the learner, figures, and teaching the code an exercise needs.
- **Reading or listening on request**: honored as the learner's choice, earns no levels, creates no make-up queue.
- **Channel support**: the fleet Discord adapter, where answer buttons are optional and a confidence rating is never used to set a level.
- **Review, curate and status modes.**
- **No simulated evidence**: demonstrations and agent-operated inputs never count as a learner's answers.

Two rules of the previous version of this skill were dropped because they conflict with the source: multiple choice as the default form of a check with an optional 1-5 confidence rating, and the four understanding labels as the current measure of progress.

## Jane Street license

```text
The MIT License

Copyright (c) 2026 Jane Street Group, LLC <opensource-contacts@janestreet.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
