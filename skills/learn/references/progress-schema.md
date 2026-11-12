# progress.json: the saved skill map

`progress.json` is the memory that keeps a long course coherent. It holds the skill map and the reasons behind it, so a later session can continue from where the learner's understanding actually is.

It records **the learner, not the subject**. The tutor already knows the material, so explanations and content summaries do not belong here. It records **judgments, not history**. Write the current level, the checks that justify it, live misconceptions in the learner's own terms, and what to ask next. What happened session by session belongs in `sessions/*.md`.

Read it at the start of every session, after `.learning/learner.md`. Checkpoint when a subskill's level changes, at a unit boundary, when the learner gives feedback about the course (same turn, always), and around the 30-minute mark. After **every** write, parse the file back (`jq empty` or equivalent). JSON does not reject duplicate keys; a repeated key shadows the earlier one. When you add to `concepts` or `seen_angles`, extend the existing entry.

```json
{
  "course": "statistics",
  "created": "2026-07-10",
  "target_level": 4,
  "estimated_total_hours": 120,
  "hours_logged": 14.5,
  "sessions_completed": 27,
  "streak": { "current": 5, "best": 12, "last_session_date": "2026-07-09" },
  "current": { "unit": 3, "lesson": "3.2", "focus": "stats.clt" },
  "lessons": {
    "1.1": { "status": "complete", "sessions_spent": 1, "completed_on": "2026-06-12" },
    "3.2": { "status": "in_progress", "sessions_spent": 2 }
  },
  "concepts": {
    "stats.clt": {
      "name": "Central Limit Theorem",
      "lesson": "2.3",
      "level": 3,
      "level_set": { "session": 24, "by": "check" },
      "last_touched_session": 24,
      "evidence": [
        {
          "session": 22,
          "task": "predict the shape of sample means drawn from a skewed distribution",
          "result": "pass",
          "unprompted": true,
          "observation": "predicted a bell shape and gave the averaging reason unaided",
          "support": "independent"
        },
        {
          "session": 24,
          "task": "explain why the spread of sample means shrinks as n grows",
          "result": "pass",
          "unprompted": true,
          "observation": "reached the 1/sqrt(n) argument after one narrower question",
          "support": "guided"
        },
        {
          "session": 24,
          "task": "say what converges as n grows (a level-4 question)",
          "result": "partial",
          "unprompted": true,
          "observation": "described one sample path settling to the mean; has not yet separated it from the distribution of means",
          "support": "independent"
        }
      ],
      "notes": [
        "still conflates convergence of the distribution with convergence of a sample path; ask about many repeated samples at fixed n",
        "the 'many small independent nudges' framing made the first prediction possible"
      ]
    }
  },
  "seen_angles": {
    "stats.clt": [
      "s24: predict shape of sample means for exp(λ)",
      "s19: predict-output numpy simulation"
    ]
  },
  "notes": "Prefers code-first exercises; avoid measure-theoretic language."
}
```

## Fields

- **`target_level`** is the level every subskill must reach before the unit or course ends: `4` by default, `5` when the learner asked for full mastery.
- **`concepts`** is keyed by the stable concept IDs in `curriculum.md`. A concept is a subskill on the map. Lessons are only the order of delivery.
- **`level`** is an integer from 0 to 5 with the meanings in `SKILL.md`. Leave it absent until the learner has been placed; the map shows that as `?/5`. Never write a level that no answer supports.
- **`level_set`** says when and how the current level was set. `by` is `"diagnostic"` for a starting placement, `"check"` for a raise earned under the evaluation rules, `"review_fail"` for a level lowered after a failed review, or `"assessment"` for a final assessment.
- **`evidence`** holds the checks that justify the current level, usually two to four. Each entry has `session`, `task`, `observation`, and:
  - `result`: `"pass"`, `"partial"`, or `"fail"`. A vague or partly correct answer is `"partial"` and does not count toward a raise.
  - `unprompted`: `true` when the learner had not just been told the answer. An answer to the re-test that follows a direct explanation is `false`.
  - `support`: `"independent"`, `"guided"` (after narrower questions or a hint), or `"demonstrated_by_tutor"` (the tutor explained it; exposure, not performance).
  - optional `kind`: `"recognition"` for a selected option without a reason, `"explanation"`, or `"application"`. Recognition alone never counts toward a raise.
  - optional `source`: a pointer to the session log entry or message that holds the actual answer.
- A raise needs two or more `"pass"` entries from different questions since the level was last set, at least one with `unprompted: true`. Level 5 also needs an edge case handled and a clear explanation. When a review fails, lower `level`, set `level_set.by` to `"review_fail"`, and keep the failed entry.
- **`notes`** (per concept) holds live misconceptions, the narrower question or framing that helped, and open questions. Keep the three or four most useful. Remove a misconception once a later check shows it is gone.
- **`seen_angles`** stores one-line fingerprints of questions already used. Independent checks need different questions, so consult it before writing a new one. Keep about five per concept.
- **`notes`** (top level) is for what is specific to this course. The course contract, if there is one, sits at the top, numbered, and is read first. Anything true of the learner in every course belongs in `.learning/learner.md`.

Optional fields that mature courses use:

- **`status`**: `"active"` (default), `"paused"`, or `"archived"`, set only by an explicit decision with the learner, with a one-line reason.
- **`glossary`**: for a course with a fluency goal, term → where the learner met it and its state.
- **`next_session`**: a few lines for the next tutor: the focus, the review question to open with, and pending decisions. Rewrite it whole at each close. Keep judgments in `concepts`.
- **`assessments`**: one entry per final mixed assessment: scope (unit or course), date, questions per concept with results, the integrative problem, and pass or fail.

## What counts as evidence

Record what the learner produced and what help came before it.

- A check is an answer in the learner's own words, or actual output from an exercise.
- Silence, "ok", "makes sense", "I know this", and agreement with an explanation are not checks. Do not record them as evidence.
- An answer given by the tutor after "just tell me" is `demonstrated_by_tutor`. It supports no level.
- A selected option without a reason is `recognition`. Ask for the reason; the reason is the check.
- A confidence rating is a self-report. Keep it with the answer if the learner gave one. It never changes a level.
- A syntax or library gap is recorded in notes, separately from the concept's level.
- Time passing and skipped questions change nothing. Only a failed check lowers a level.
- Simulated learners, demonstrations, and agent-operated inputs are excluded from evidence, session counts, and levels, even when they ran under the learner's account.

## Courses written before the skill map

Older courses carry an `understanding` label on each concept instead of a level:

```json
"stats.prior": { "name": "Prior", "lesson": "1.2", "understanding": "settling", "notes": ["..."] }
```

The labels were `"unassessed"`, `"shaky"`, `"settling"`, and `"solid"`. They are history.

- Keep `understanding`, `notes`, `evidence`, concept IDs, lesson records, and course status exactly as written. Do not delete or rewrite them.
- Do not write new `understanding` values. New judgments use `level` only.
- Do not convert a label into a level, and do not mass-migrate a course. `solid` is not 4 and `shaky` is not 1; the labels were set under different rules and often without independent checks.
- Add `level` to a concept only when the learner has been placed by a diagnostic or a check in a real session. A concept with a label and no level renders as `?/5`.
- Old evidence entries without `result` or `unprompted` stay valid as notes. They do not count as checks toward a raise.
- Use the old notes to choose questions: a recorded misconception is a good first thing to test.
- Older records may also hold answer-button and confidence events. Keep them with their original meaning; see [discord.md](discord.md#course-evidence).

Record course maintenance as maintenance. It does not add teaching sessions or hours, and it creates no learner evidence.

## Streak

Increment `streak.current` if the last session was yesterday; leave it unchanged for another session today; otherwise reset it to 1. Streaks are optional context. They are not evidence, and never a reason to guilt the learner.
