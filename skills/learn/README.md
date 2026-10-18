# learn

A portable skill for a professor-led course of study. Give it a topic and it researches a curriculum, prepares examples and contrasts, and leads lessons with room for questions. It keeps notes on what you understand and where you need help, so the course survives months of short sessions.

I made this because I couldn't study consistently after work. Textbook exercises want a full hour of deep focus and I never had that at 9pm. These lessons are short enough to do tired. The tutor remembers where you left off, you just show up.

## Install

This skill is part of [Derick Wells' skills](../../README.md). Clone the collection and link `learn` into your harness's skills directory. Any harness that supports [Agent Skills](https://agentskills.io) should work (Claude Code, opencode, Codex, Gemini CLI, ...):

```bash
git clone https://github.com/derwells/learn-skill ~/src/derwells-skills

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
| `/learn new bayesian statistics` | Researches and writes the curriculum. Expensive, done once |
| `/learn` or "today's lesson" | ~30 min session |
| `/learn status` | Progress across courses |
| `/learn review` | Revisit shaky ideas, no new material |
| `/learn curate` | No lesson. Retune how the course is run |

Courses live in `.learning/` at the project root:

```
.learning/
├── learner.md             # what the tutor knows about you, across courses
└── <course>/
    ├── curriculum.md      # units, lessons, the intuition each one must land
    ├── progress.json      # tutor's notebook: what clicked, what's shaky, why
    ├── materials/         # lesson arguments, worked examples, contrasts, applications
    ├── notebooks/         # one Jupyter notebook per lesson
    └── sessions/          # short log per session
```

Worth committing `.learning/` if the project is a repo.

## How it teaches

- Leads each lesson around a question and develops the reasoning needed to answer it.
- Uses deliberate comparisons to show what distinguishes concepts, why methods work, and where assumptions matter.
- Connects examples to the actual mathematics. Explains choices and valid steps rather than merely naming them.
- Adapts explanation length to the argument and your response. You can interrupt without having to direct the lesson yourself.
- Moves from worked examples to guided and independent application when useful. Listening and optional discussion remain valid choices.
- Uses executed notebook demonstrations and precise figures. Keeps pending prediction answers out of view.
- Preserves your questions and pace. Thirty minutes is a guideline; a lesson can span sessions.

Wrong answers are fine. What matters is you end up seeing why.

A concept entry in the notebook looks like this:

```json
"stats.clt": {
  "understanding": "settling",
  "notes": [
    "clicked via the 'many small independent nudges' framing",
    "still conflates convergence of the distribution with a sample path — try a simulation angle next"
  ]
}
```

That's what the tutor reads back three weeks later. It tracks which explanations helped and can reuse a familiar example before changing it to test a new distinction. Missing evidence is recorded as `unassessed`; a demonstrated confusion is `shaky`.

Existing courses keep their history and scope. On resumption, the tutor updates upcoming materials and retires inherited brevity limits or mandatory probe queues while preserving your explicit preferences.

## License

MIT
