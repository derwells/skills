# Derick Wells' skills

These are the agent skills I wrote for my own work with Claude Code and Codex. Each one is a folder with a `SKILL.md` that tells the agent when to use it and how. They follow the [Agent Skills](https://agentskills.io) format, so other harnesses that read that format should pick them up too.

This repo started as just the `learn` skill. It now holds a few more that I've made general enough to share. Take whichever are useful to you.

## What's here

| Skill | What it does | How it starts |
|---|---|---|
| [learn](skills/learn) | Runs a long course of study: researches a curriculum, leads short lessons, keeps notes on what you understand. | `/learn`, or asking for a lesson |
| [access](skills/access) | Gets an agent past logins, consent screens and dashboards with no API. Tries an official API or CLI first, then a saved browser script, then exploring the page, and asks you only for MFA, CAPTCHA or a locked vault. Fills passwords from your password manager without showing them to the model. | A task behind a login |
| [browser](skills/browser) | Drives web pages: explores with agent-browser, saves flows that work as Playwright scripts, and keeps test browsers separate from anything real. Pairs with `access`. | Before an agent drives a web page |
| [model-check](skills/model-check) | Writes a small TLA+ model of real code, checks it with TLC, and replays it against real runs before trusting it. For queues, retries, locks, timeouts and similar ordering bugs. | Changes to concurrency or protocol code, or asking for a model check |

## Install

Clone the repo once, then link the skills you want into your harness's skills folder.

```bash
git clone https://github.com/derwells/skills ~/src/derwells-skills

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

If you'd rather not keep a clone, copy a whole folder from `skills/` into your skills directory instead. Each folder has its own `LICENSE`, so keep it with the copy. You'll have to copy the folder again to get changes.

### If you installed learn before the move

This repo used to be called `learn-skill`. GitHub redirects the old URL, so existing clones still pull, but you can point yours at the new name:

```bash
git -C <your clone> remote set-url origin https://github.com/derwells/skills
```

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
- `access` and `browser` need [agent-browser](https://github.com/vercel-labs/agent-browser) and Python [Playwright](https://playwright.dev/python/). Password fills need a password manager CLI you've unlocked yourself, such as Bitwarden's `bw`. `model-check` needs Java 17+ and `tla2tools.jar`.
- I change these as I use them. Pin a commit if you want them to hold still.

## Credits

Sources the skills draw on are cited inside them. The main ones:

- `learn` bases its teaching choices on Schwartz and Bransford's [A Time for Telling](https://www.wright.edu/sites/www.wright.edu/files/uploads/2017/Feb/event/Schwartz_Bransford_1998_TimeForTelling.pdf) and the IES practice guide [Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1).
- `model-check` is built on Leslie Lamport's [TLA+](https://lamport.azurewebsites.net/tla/tla.html) and its model checker TLC. Its warning about textbook drift comes from [SysMoBench](https://arxiv.org/abs/2509.23130), and Boris Cherny's [post](https://x.com/bcherny/status/2102543349102338309) on Lean and TLA+ is its example of the approach.
- `browser` uses Vercel's [agent-browser](https://github.com/vercel-labs/agent-browser) (Apache-2.0) and Microsoft's [Playwright](https://playwright.dev/python/). Neither is bundled here.

## License

MIT. See [LICENSE](LICENSE); each skill folder carries the same notice.
