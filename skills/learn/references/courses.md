# Saved courses

Read this before any session in a saved course. The teaching method is in `SKILL.md`; this file covers what persists between sessions.

## Files

```text
.learning/
├── learner.md             # background, preferences, delivery, across courses
└── <course-slug>/
    ├── curriculum.md      # goal, target level, skill tree: units and concepts
    ├── progress.json      # levels, evidence, misconceptions, next pointer
    ├── materials/         # prepared questions and short explanations per unit
    ├── notebooks/         # exercises and figures per lesson
    └── sessions/          # short session logs
```

At session start, read `learner.md`, then `progress.json` (course contract first), the current unit in the curriculum, and its materials. Read [progress-schema.md](progress-schema.md) before the first progress write in a conversation, and parse the JSON after each write. Checkpoint at each level change that ends a subskill, at a unit boundary, and around the half-hour mark. Persist feedback about how the course is run in the turn it is given. Suggest committing course files if useful; never commit unasked.

## Resuming

Show the saved map. Open with one unannounced review question on an earlier subskill, then continue at the current focus. After a long gap, expect slower recall; a failed review still lowers the level, and elapsed time alone does not.

## Courses written before the skill map

Older courses record an `understanding` label per concept (`unassessed`, `shaky`, `settling`, `solid`) instead of a level. Keep those labels, notes, evidence, concept IDs, and session history exactly as they are. Do not convert a label into a level. Run the diagnostic on the current unit, place levels from the answers, and leave every other concept at `?/5` until it is checked. Use the old notes to choose which questions to ask.

## Recorded preferences

`learner.md` and the course contract hold choices the learner made. Preferences about presentation stay in force: language, order of mathematics, figures, pace, energy. A recorded choice that conflicts with this method, such as reading-first lessons, no required questions, or an older course style (`tutor`, `tutorial`, `design-partner`), is neither silently obeyed nor silently dropped. Name the conflict once at the start of the resumed session, ask which should govern this course, and record the dated answer in the contract.

## Close a course session

- Update levels, evidence, live misconceptions, and the next-session pointer. Validate the JSON. Separate what you explained from what the learner demonstrated.
- Write a short `sessions/<date>.md` log: subskills worked, each level change and the checks behind it, consequential learner answers, tutor mistakes, and where to resume.
- Show the map and name the weakest areas. Do not claim something clicked without a check that shows it.
- If the course is within one unit of unprepared material, prepare it now with [create-course.md](create-course.md). Keep fast-moving material current with [freshness.md](freshness.md).

Thirty minutes is a guide to energy, not a quota. A subskill may span sessions. Read [notebooks.md](notebooks.md) before creating or using an exercise notebook.

## Status and curation

`/learn status` reads each course's progress and shows its overall bar, current focus, and weakest subskills. Flag a course dormant for about three weeks as a candidate to resume, pause, merge, or archive. Record a status change only when the learner chooses it.

`/learn curate` is maintenance done with the learner; read [curate.md](curate.md). Fix the questions and materials that caused friction, not only the contract.
