# learn

A portable skill for a Socratic tutor. Give it a topic and it asks what you already know, draws a skill map with a level from 0 to 5 for each subskill, and then teaches by asking one question at a time. You answer in your own words. For a long course it researches a curriculum and saves the map, so the course survives months of short sessions.

I made this because I couldn't study consistently after work. Textbook exercises want a full hour of deep focus and I never had that at 9pm. The tutor remembers where you left off, you just show up.

The teaching method is adapted from Jane Street's [`socratic-tutor`](https://github.com/janestreet/agent_skills/blob/7c6715c29548a3b39d4a9545c698ee4fd17a7213/socratic-tutor/SKILL.md) skill (MIT). Saved courses, notebooks, figures and the Discord adapter are additions. [NOTICE.md](NOTICE.md) says which rule comes from where.

## Install

This skill is part of [Derick Wells' skills](../../README.md). Clone the collection and link `learn` into your harness's skills directory. Any harness that supports [Agent Skills](https://agentskills.io) should work (Claude Code, opencode, Codex, Gemini CLI, ...):

```bash
git clone https://github.com/derwells/skills ~/src/derwells-skills

# Claude Code (opencode reads this path too)
ln -s ~/src/derwells-skills/skills/learn ~/.claude/skills/learn

# Codex and others
ln -s ~/src/derwells-skills/skills/learn ~/.agents/skills/learn
```

If you cloned this repo straight into `~/.claude/skills/learn` before it became a collection, see [the migration steps](../../README.md#if-you-installed-learn-before-the-move).

Needs web search (curriculum research), `jq` or `python3` (notebook validation), and Jupyter via `uv` for lesson notebooks.

## Use

| Say | What happens |
|---|---|
| `/learn bayes' rule` or "teach me bayes' rule" | Tutors the topic in the conversation. No files |
| `/learn new bayesian statistics` | Researches and writes a saved course. Expensive, done once |
| `/learn` or "today's lesson" | Continues the current topic or course, about 30 minutes |
| `/learn status` | Skill maps across courses |
| `/learn review` | Re-tests earlier subskills, no new material |
| `/learn curate` | No lesson. Retune how the course is run |

During a session you can say "show progress", "harder", "easier", "just tell me" (for the current question only), or "save state". A plain "explain X" gets a plain answer and no quiz.

Courses live in `.learning/` at the project root:

```
.learning/
├── learner.md             # what the tutor knows about you, across courses
└── <course>/
    ├── curriculum.md      # goal, target level, units and their subskills
    ├── progress.json      # the saved skill map and the checks behind each level
    ├── materials/         # prepared questions and short explanations per unit
    ├── notebooks/         # one Jupyter notebook per lesson, for exercises
    └── sessions/          # short log per session
```

Worth committing `.learning/` if the project is a repo.

## How it teaches

- Starts with three to five diagnostic questions and teaches nothing until they are done.
- Asks one question at a time and stops. You predict, explain why, find the flaw in a wrong claim, or apply the idea to a new case.
- When you are wrong it asks a narrower question that shows the contradiction. It explains directly only after two or three failed attempts, then tests the same idea from another side.
- States what you could not work out yourself, such as definitions, notation and library calls, in a few sentences.
- Raises a level only after two independent checks, one of them without having just been told the answer. A vague answer does not count, and neither do "ok", "I know this" or a tapped option without a reason.
- Re-tests earlier subskills without warning. A failed review lowers the level. Time away does not.
- Ends a topic when every subskill reaches the target (4/5 by default) and you pass a mixed final assessment.

The map looks like this:

```text
Topic: recursion                        overall: ██████░░░░ 60%
-----------------------------------------------------------------
base cases            [████████░░]  4/5  * at target
reachable stop        [██████░░░░]  3/5  <- current focus
call stack            [████░░░░░░]  2/5
tail calls            [..........]  ?/5  not placed yet
-----------------------------------------------------------------
```

A concept in `progress.json` keeps its level and the checks behind it:

```json
"stats.clt": {
  "level": 3,
  "evidence": [
    { "session": 24, "task": "predict the shape of sample means", "result": "pass", "unprompted": true }
  ],
  "notes": [
    "still conflates convergence of the distribution with a sample path"
  ]
}
```

Courses written before the skill map keep everything they recorded. Their old labels (`shaky`, `settling`, `solid`) stay as history and are not converted to levels; the tutor places you again with a short diagnostic. Rules an older version recorded about how to teach, such as reading-first lessons or a course style, give way to the questions; the tutor says so once and notes the date. Preferences about presentation stay.

## Evals

[`evals/`](evals/README.md) has scripted teaching exchanges with free-text answers, run against the previous version of this skill and this one, and the judged results.

## License

MIT
