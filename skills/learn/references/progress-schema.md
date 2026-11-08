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
- For fleet Discord evidence, keep a source event or prompt reference so a future tutor can find the actual response. Keep the full event trail in the session log. Confidence is a self-report, separate from demonstrated understanding; it never sets `understanding` by itself.
- **`notes`** (per concept) records live misconceptions, which explanations helped, and relevant unresolved questions. Keep the three or four most useful entries and remove resolved misconceptions. When a lesson closes, compact its notes to the current judgment, useful explanations, and open questions. Session history belongs in the logs.
- **`seen_angles`** stores one-line fingerprints (session + gist) of problems and framings already used. Reuse a familiar case when it helps reconnect the argument; vary the important feature when assessing application beyond memorization. Cap at about five per concept, oldest dropped.
- **`notes`** (top level) is free-form tutor memory — but only for what's *course-specific*: how this course is run, its goals and grounding, environment recipes it alone needs. If the course has a **contract** (see SKILL.md), it sits at the top of this field, numbered, and is read before everything else. Anything true of the learner in every course (environment, energy patterns, math background, analogy rules, probe craft) belongs in `.learning/learner.md`, not here — never duplicate it. Update sparingly; read always.

Optional fields that mature courses have found useful (add them when the course needs them, in this shape):

- **`status`** (course-level): `"active"` (default when absent), `"paused"`, or `"archived"` — set from an explicit decision with the user (usually via `/learn status` flagging dormancy). Include a one-line note saying why and what would reactivate it. Paused/archived courses are skipped by session mode.
- **`glossary`** — for courses with a fluency goal: term → where the learner met it + state + any learner-specific hook. Never a re-teaching (generate glosses fresh at drill time); prune entries that go solid.
- **`next_session`** — a few lines of pointers for the next session's tutor: what to open with and why, decisions pending. Pointers, not a script: cap at roughly ten lines, rewrite it whole at each close (never append), and keep judgments out of it — they live in `concepts`.

## Choosing warm-up items

For the initial trial, use at most one optional revisit at the next relevant lesson. Use a changed example. Use the existing `next_session` pointer when useful.
Choose a distinction that supports the lesson or addresses an important unresolved confusion. Missing evidence creates no testing backlog.
In `design-partner` courses, use natural callbacks and optional discussion. When prerequisite gaps impede progress, suggest focused review.
Do not add due dates, reminders, or a scheduler without a separate request. A skip or long gap alone never downgrades understanding.

## Distinguish response evidence

Record what the learner demonstrated and what help preceded it. Keep these observations distinct:

- Recognition: selecting a supplied correct answer. This supports a narrow claim about that choice in that context.
- Explanation: giving the relevant reason. Record whether it was spontaneous, prompted, or supplied after feedback.
- Independent application: using the idea in a changed example without supplied choices or help with the relevant step.

A revealing question or spontaneous correction can also change a judgment. Preserve it with its context and source.
Neither a correct button choice nor high confidence establishes independent application. Low confidence does not establish a misconception.
A pending selection is ungraded context. A skip has no correctness value. Silence and assent add no assessment evidence.

Use optional `kind` and `source` fields when they help distinguish new evidence. Existing entries without them remain valid:

```json
{
  "session": 28,
  "task": "compare combined volumes before and after a transfer",
  "kind": "recognition",
  "observation": "selected the equal-total option; supplied no reason",
  "support": "independent",
  "source": "sessions/2026-07-11.md#volume-check"
}
```

Here, `independent` describes the support given for recognition. It does not turn recognition into independent application.
Use `explanation` or `application` for those evidence kinds when appropriate. Describe questions and corrections directly in the observation.
Keep only the observations needed to support the current judgment. Do not fill new fields retrospectively from guesses.

## Answer-specific confidence and session events

Keep detailed interaction records in the existing session log. See [discord.md](discord.md#course-evidence) for the transport fields.
A new combined submission holds one answer and its optional confidence, with separate source references for each observation.
Retain the prompt and question revision, selected option ID/text, answer revision, and source interaction/message/channel references.
Record the help and feedback context. Deduplicate repeated delivery of the same source event.

Confidence about a selected answer has scope `answer`. Preserve its `before_feedback`, `after_feedback`, or `unknown` timing.
Use explicit interaction state and source context; nearby timestamps do not prove timing.
Changing the pending answer clears its pending rating. Missing confidence stays missing; never supply a default value.
For feedback, 1 and 2 mean uncertain, 3 means middle, and 4 and 5 mean confident.
These ordered labels are neither probabilities nor understanding levels.

Historical separate confidence prompts have scope `section`, including those paired with an answer prompt.
Keep their original values and meaning. Do not infer answer-specific or pre-feedback confidence from pairing alone.
If the historical timing is unavailable, leave it unknown. Add optional fields only when new evidence needs them.

When chat or retirement closes a pending check, retain `selected_not_submitted` context without a grade.
Record a free-text answer separately with its source and help or feedback context. Preserve later corrections as later observations.
Do not count the pending selection as a second submitted attempt.

Exclude synthetic demonstrations and agent-operated taps from learner evidence, session counts, and progress judgments.
Use data-level demo markers and source provenance. A learner account can also operate a synthetic test.
Keep demonstration evidence in implementation records, outside course records.

## Compatibility with existing courses

Keep existing concept IDs, histories, course statuses, and demonstrated understanding. Add evidence only as useful observations become available; missing `evidence` is valid. An old `shaky` judgment may mean actual confusion or simply "not probed." Inspect its notes before changing it. Use `unassessed` only when insufficient evidence was the sole basis; preserve `shaky` when a documented misconception remains unresolved. Do not infer mastery from lesson completion or mass-migrate judgments.

Preserve legacy section confidence and immediate-submit event history. Missing revisions, confidence, timing, or new evidence fields remain valid.
Do not mass-migrate courses or synthesize historical values. Keep paused courses paused.

Read legacy course style `tutor` as `tutorial`. Retire inherited probe floors and mandatory make-up checks in the current contract, while preserving explicit learner choices and useful revisit pointers. Record course maintenance as maintenance; it does not increment teaching sessions or hours.

## Streak

Increment `streak.current` if the last session was yesterday; leave it unchanged for another session today; otherwise reset it to 1. Preserve existing history. Streaks are optional context, not evidence of understanding, and never a reason to guilt the learner.
