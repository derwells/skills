# progress.json — the tutor's notebook

`progress.json` is the persistent memory that keeps a months-long course coherent. It is a *notebook*, not a scorecard: its job is to let a future session pick up exactly where understanding actually is — which ideas have clicked, which are still shaky and *why*, and which explanations worked — without the user having to re-explain themselves.

It records **the learner, not the subject** — the tutor already knows the material, so explanations, definitions, and content summaries never belong here. And it records **judgments, not history**: a future session brings the same judgment you have now and can re-derive anything derivable from a current assessment plus the curriculum. So write down only what can't be re-derived: the current understanding level, live misconceptions stated precisely in the learner's terms, pointers to the framings that landed (name the analogy, don't re-explain it), and what to try next. What happened session by session belongs in `sessions/*.md` — if a concept's notes read like a chronicle ("s4 delivered X… s5 broke… s6 landed") or like a textbook, they're duplicating something the next session already has and should be collapsed.

Read it at the start of every session (after `.learning/learner.md`, the cross-course profile). Don't wait for the close to write it: checkpoint at every natural boundary — a lesson closing, any course-run feedback from the user (same turn, always), the ~30-minute mark — and finish the write at the close. After **every** write, parse the file back (`jq empty` or equivalent): a corrupt notebook silently loses weeks of judgment, and JSON's duplicate keys don't error — they shadow earlier entries, so when adding to `concepts` or `seen_angles`, extend the existing key's array rather than re-adding the key.

```json
{
  "course": "statistics",
  "created": "2026-07-10",
  "estimated_total_hours": 120,
  "hours_logged": 14.5,
  "sessions_completed": 27,
  "streak": { "current": 5, "best": 12, "last_session_date": "2026-07-09" },
  "current": { "unit": 3, "lesson": "3.2" },
  "lessons": {
    "1.1": { "status": "complete", "sessions_spent": 1, "completed_on": "2026-06-12" },
    "3.2": { "status": "in_progress", "sessions_spent": 2 }
  },
  "concepts": {
    "stats.clt": {
      "name": "Central Limit Theorem",
      "lesson": "2.3",
      "understanding": "settling",
      "last_touched_session": 24,
      "evidence": [
        {
          "session": 24,
          "task": "interpret simulation of sample means",
          "observation": "recognized the distributional pattern with a prompt; confused it with a single sample path",
          "support": "guided"
        }
      ],
      "notes": [
        "clicked via the 'many small independent nudges' framing; the galton board analogy landed",
        "still conflates convergence of the distribution with convergence of a sample path — revisit with a simulation angle"
      ]
    }
  },
  "seen_angles": {
    "stats.clt": [
      "s24: galton board analogy + derive sampling dist of mean for exp(λ)",
      "s19: predict-output numpy simulation"
    ]
  },
  "notes": "Prefers code-first sessions; analogies land well; shaky on measure-theoretic language, avoid it."
}
```

Field notes:

- **`concepts`** is keyed by the stable concept IDs defined in `curriculum.md`. Concepts are the unit of understanding; lessons are just the delivery order.
- **`understanding`** is the tutor's judgment, with four values:
  - `"unassessed"`: insufficient evidence about understanding. Delivery, silence, or "okay" alone does not show either mastery or confusion.
  - `"shaky"`: the learner demonstrated a confusion or could not yet reason through the relevant step. Record the specific evidence and repair it when it matters.
  - `"settling"`: the learner reasoned correctly with help, or demonstrated understanding in a limited context. Seek a useful opportunity for independent application.
  - `"solid"`: the learner explained and applied the idea independently, with its relevant assumptions or limits. Later application can strengthen confidence that it persisted.
  Judge the whole conversation, including revealing questions and spontaneous corrections. A formal probe is not required. Self-report helps set pace but does not manufacture evidence of independent application. Move a judgment when evidence changes; do not downgrade solely because time passed or a check was declined.
- **`evidence`** is an optional array of brief observations. Each entry has `session`, `task`, `observation`, and `support` (`"independent"`, `"guided"`, or `"demonstrated_by_tutor"`). Keep only observations that explain the current judgment, usually one to three. Tutor demonstration records exposure, not learner mastery. Do not invent historical evidence to populate this field; existing notes can suffice until new evidence appears.
- **`notes`** (per concept) records live misconceptions, which explanations helped, and relevant unresolved questions. Keep the three or four most useful entries and remove resolved misconceptions. When a lesson closes, compact its notes to the current judgment, useful explanations, and open questions. Session history belongs in the logs.
- **`seen_angles`** stores one-line fingerprints (session + gist) of problems and framings already used. Reuse a familiar case when it helps reconnect the argument; vary the important feature when assessing application beyond memorization. Cap at about five per concept, oldest dropped.
- **`notes`** (top level) is free-form tutor memory — but only for what's *course-specific*: how this course is run, its goals and grounding, environment recipes it alone needs. If the course has a **contract** (see SKILL.md), it sits at the top of this field, numbered, and is read before everything else. Anything true of the learner in every course (environment, energy patterns, math background, analogy rules, probe craft) belongs in `.learning/learner.md`, not here — never duplicate it. Update sparingly; read always.

Optional fields that mature courses have found useful (add them when the course needs them, in this shape):

- **`status`** (course-level): `"active"` (default when absent), `"paused"`, or `"archived"` — set from an explicit decision with the user (usually via `/learn status` flagging dormancy). Include a one-line note saying why and what would reactivate it. Paused/archived courses are skipped by session mode.
- **`glossary`** — for courses with a fluency goal: term → where the learner met it + state + any learner-specific hook. Never a re-teaching (generate glosses fresh at drill time); prune entries that go solid.
- **`next_session`** — a few lines of pointers for the next session's tutor: what to open with and why, decisions pending. Pointers, not a script: cap at roughly ten lines, rewrite it whole at each close (never append), and keep judgments out of it — they live in `concepts`.

## Choosing warm-up items

Choose a short revisit when it supports today's lesson or addresses an important unresolved confusion. A warm-up is optional. Unassessed concepts do not automatically become a testing backlog. In `design-partner` courses, use natural callbacks and optional discussion instead of deferred drills. When several prerequisite gaps impede progress, suggest focused review.

## Compatibility with existing courses

Keep existing concept IDs, histories, course statuses, and demonstrated understanding. Add evidence only as useful observations become available; missing `evidence` is valid. An old `shaky` judgment may mean actual confusion or simply "not probed." Inspect its notes before changing it. Use `unassessed` only when insufficient evidence was the sole basis; preserve `shaky` when a documented misconception remains unresolved. Do not infer mastery from lesson completion or mass-migrate judgments.

Read legacy course style `tutor` as `tutorial`. Retire inherited probe floors and mandatory make-up checks in the current contract, while preserving explicit learner choices and useful revisit pointers. Record course maintenance as maintenance; it does not increment teaching sessions or hours.

## Streak

Increment `streak.current` if the last session was yesterday; leave it unchanged for another session today; otherwise reset it to 1. Preserve existing history. Streaks are optional context, not evidence of understanding, and never a reason to guilt the learner.
