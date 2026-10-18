# Derick Wells' skills

These are the agent skills I wrote for my own work with Claude Code and Codex. Each one is a folder with a `SKILL.md` that tells the agent when to use it and how. They follow the [Agent Skills](https://agentskills.io) format, so other harnesses that read that format should pick them up too.

This repo started as just the `learn` skill. It now holds the rest of the ones that are general enough to share. Take whichever are useful to you.

## What's here

| Skill | What it does | How it starts |
|---|---|---|
| [learn](skills/learn) | Runs a long course of study: researches a curriculum, leads short lessons, keeps notes on what you understand. | `/learn`, or asking for a lesson |
| [spell-out](skills/spell-out) | Writes full, careful explanations for when you want to understand a topic in depth. `learn` uses it. | "spell it out", "walk me through", "teach me" |
| [handoff](skills/handoff) | Prints a one-paragraph prompt you paste into a fresh session so it picks up where you left off. | Only when you type `/handoff` |
| [model-check](skills/model-check) | Writes a small TLA+ model of real code, checks it with TLC, and replays it against real runs before trusting it. For queues, retries, locks, timeouts and similar ordering bugs. | Changes to concurrency or protocol code, or asking for a model check |
| [ai-image](skills/ai-image) | Generates and edits images with OpenAI GPT Image 2 or Google Gemini over plain `curl`, plus prompt templates and post-processing commands. Uses the provider you name and asks if you don't. | `/ai-image`, or asking for an image from either provider |
| [claudex](skills/claudex) | Runs Claude Code headless against Xiaomi MiMo models for wide, cheap reading (many files, many repos). It only gathers; your main agent decides and edits. Wrapper scripts are in `scripts/`. | `/claudex`, or a big search task |
| [jev](skills/jev) | Uses Jev, TypeSafe's judging model, through my [sieve](https://github.com/derwells/sieve) MCP server to score or filter a list of items against a question. | Before a broad grep or research fan-out, or with a long list to triage |

## Install

Clone the repo once, then link the skills you want into your harness's skills folder.

```bash
git clone https://github.com/derwells/learn-skill ~/src/derwells-skills

# Claude Code (opencode reads this path too)
mkdir -p ~/.claude/skills
ln -s ~/src/derwells-skills/skills/learn ~/.claude/skills/learn

# Codex and others
mkdir -p ~/.agents/skills
ln -s ~/src/derwells-skills/skills/learn ~/.agents/skills/learn
```

Swap `learn` for any other skill name. To update, pull:

```bash
git -C ~/src/derwells-skills pull
```

If you'd rather not keep a clone, copy a single folder from `skills/` into your skills directory instead. You'll just have to copy it again to get changes.

### If you installed learn before the move

The old instructions cloned this whole repo straight into `~/.claude/skills/learn`. That worked when the repo was only `learn`. Now `learn` lives in `skills/learn/`, so a plain `git pull` in the old location leaves no `SKILL.md` at the top and the skill stops loading.

Move the clone out, pull, and link the skill back:

```bash
mkdir -p ~/src
mv ~/.claude/skills/learn ~/src/derwells-skills
git -C ~/src/derwells-skills pull
ln -s ~/src/derwells-skills/skills/learn ~/.claude/skills/learn
```

Use `~/.agents/skills/learn` instead if that's where you installed it. These commands also fix things if you already pulled and `learn` disappeared. Your courses aren't affected; they live in `.learning/` inside your projects, not in the skill folder.

To stay on the old single-skill layout, check out the `learn-standalone` tag:

```bash
git -C ~/.claude/skills/learn fetch --tags
git -C ~/.claude/skills/learn checkout learn-standalone
```

## Things to know

- I write and test these on Linux with Claude Code and Codex. Other harnesses should work if they read `SKILL.md` folders, but I don't test them.
- Some skills call paid services: `ai-image` (OpenAI or Gemini API keys), `claudex` (a Xiaomi MiMo plan) and `jev` (a TypeSafe API key). Each `SKILL.md` lists what it needs.
- I change these as I use them. Pin a commit if you want them to hold still.
- A few skills I use aren't here because they depend on my own accounts or private tooling: an email and calendar assistant, the skills that coordinate my agent sessions, and some work-specific ones.

## Credits

Sources the skills draw on are cited inside them. The main ones:

- `learn` bases its teaching choices on Schwartz and Bransford's [A Time for Telling](https://www.wright.edu/sites/www.wright.edu/files/uploads/2017/Feb/event/Schwartz_Bransford_1998_TimeForTelling.pdf) and the IES practice guide [Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1).
- `model-check` is built on Leslie Lamport's [TLA+](https://lamport.azurewebsites.net/tla/tla.html) and its model checker TLC, and its warning about textbook drift comes from the SysMoBench results.

Skills by other people that I use, linked here so you get their current versions and their own licenses:

- [humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT), based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide from WikiProject AI Cleanup.
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) by Conor Bronsdon (MIT).
- [make-film](https://github.com/clsandoval/make-film) by Carlos Sandoval (MIT).
- [shadcn and migrate-radix-to-base](https://github.com/shadcn/ui/tree/main/skills) from the shadcn/ui project (MIT).

## License

MIT. See [LICENSE](LICENSE).
