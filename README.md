# Derick Wells' skills

These are the agent skills I wrote for my own work with Claude Code and Codex. Each one is a folder with a `SKILL.md` that tells the agent when to use it and how. They follow the [Agent Skills](https://agentskills.io) format, so other harnesses that read that format should pick them up too.

This repo started as just the `learn` skill. It now holds a few more that I've made general enough to share. Take whichever are useful to you.

## What's here

| Skill | Use it for | How it starts | Needs |
|---|---|---|---|
| [learn](skills/learn) | A long course of study: researches a curriculum, leads short lessons, keeps notes on what you understand. | `/learn`, or asking for a lesson | Web search and file write access. `jq` or `python3` to validate notes; Jupyter via `uv` for notebook lessons. |
| [access](skills/access) | Getting an agent past logins, consent screens and dashboards with no API. Tries an official API or CLI first, then a saved browser script, then exploring the page, and asks you only for MFA, CAPTCHA or a locked vault. | A task behind a login | Shell access. For browser steps, the `browser` skill's tools. For password fills, a password manager CLI you have already unlocked, such as Bitwarden's `bw`. |
| [browser](skills/browser) | Driving web pages: explores with agent-browser, saves flows that work as Playwright scripts, and keeps test browsers separate from anything real. Pairs with `access`. | Before an agent drives a web page | [agent-browser](https://github.com/vercel-labs/agent-browser), Python [Playwright](https://playwright.dev/python/) and a local Chromium. The optional Jev step also needs your own runner and a TypeSafe API key. |
| [model-check](skills/model-check) | Writes a small TLA+ model of real code, checks it with TLC, and replays it against real runs. For a concrete ordering or concurrency bug that focused tests can't settle, or when you ask for a model check. | A rare ordering failure, an uncertain multi-service protocol, or asking for TLA+ | Java 17+ and `tla2tools.jar`. |

## Install

Clone the repo once, then link the skills you want into your harness's skills folder. The blocks below are the same commands `tests/test_install.py` runs in CI, against a temporary home directory.

<!-- install:clone -->
```bash
git clone https://github.com/derwells/skills ~/src/derwells-skills
```

Claude Code (opencode reads this path too):

<!-- install:claude -->
```bash
mkdir -p ~/.claude/skills
for skill in learn access browser model-check; do
  ln -sfn ~/src/derwells-skills/skills/$skill ~/.claude/skills/$skill
done
```

Codex and other harnesses that read `~/.agents/skills`:

<!-- install:codex -->
```bash
mkdir -p ~/.agents/skills
for skill in learn access browser model-check; do
  ln -sfn ~/src/derwells-skills/skills/$skill ~/.agents/skills/$skill
done
```

Drop any name from the loop that you don't want. Start a new session afterwards so the harness rescans its skills folder.

If you'd rather not keep a clone, copy a skill folder instead. Each folder has its own `LICENSE`, so keep it with the copy. You'll have to copy again to get changes.

<!-- install:copy -->
```bash
mkdir -p ~/.claude/skills
cp -R ~/src/derwells-skills/skills/learn ~/.claude/skills/learn
```

### As a Claude Code plugin

The repo also has a plugin marketplace manifest (`.claude-plugin/marketplace.json`) that offers all four skills as one plugin:

```text
/plugin marketplace add derwells/skills
/plugin install derwells-skills@derwells-skills
```

I checked this with `claude plugin validate` and an install from a local checkout using Claude Code 2.1.304. Claude Code namespaces plugin skills with the plugin name, so they appear as `derwells-skills:learn` and so on. The symlink install above keeps the short names.

### If you installed learn before the move

`learn` used to live alone in `learn-skill`, cloned straight into the skills folder. If your copy stopped loading after a pull, follow [the migration steps](docs/migrating-from-learn-skill.md).

## Using a skill

A skill starts one of two ways. The agent reads each skill's `description` and loads the skill when your task matches it. Or you name it: `/learn` in Claude Code, `$learn` in Codex. The "How it starts" column above says what to expect for each one.

A skill's instructions only load when it starts, so an idle skill adds only its short description to the session.

## Updating and pinning

With a clone, pull to get changes:

<!-- install:update -->
```bash
git -C ~/src/derwells-skills pull
```

To hold still at a release, check out a tag instead (tags are listed on the [releases page](https://github.com/derwells/skills/releases) once I cut one; see [docs/releasing.md](docs/releasing.md) for how):

```bash
git -C ~/src/derwells-skills fetch --tags
git -C ~/src/derwells-skills checkout <tag>
```

Without a tag, pin a commit hash the same way. Run `git checkout main` and pull to follow the latest again. Changes are listed in [CHANGELOG.md](CHANGELOG.md).

## Scope and limits

- I write and test these on Linux with Claude Code and Codex. Other harnesses should work if they read `SKILL.md` folders, but I haven't tested them. macOS and Windows are untested.
- CI checks structure, not behavior: the frontmatter, links, bundled files, license notices, that no private paths or secrets slipped in, that the install commands above work, and that the browser benchmark tables recompute. It cannot tell you whether a skill makes an agent do the right thing. [`skills/browser/benchmarks`](skills/browser/benchmarks/README.md) holds the one set of measurements I have, on a synthetic site.
- Skills steer an agent that can run commands and drive a browser. Read a skill before you install it, the same as any script you let an agent follow. [SECURITY.md](SECURITY.md) says how to report a problem.
- I change these as I use them, and this is a personal collection. Issues and small pull requests are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). I make no promise about response time.

## Credits

Sources the skills draw on are cited inside them. The main ones:

- `learn` bases its teaching choices on Schwartz and Bransford's [A Time for Telling](https://www.wright.edu/sites/www.wright.edu/files/uploads/2017/Feb/event/Schwartz_Bransford_1998_TimeForTelling.pdf) and the IES practice guide [Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1).
- `model-check` is built on Leslie Lamport's [TLA+](https://lamport.azurewebsites.net/tla/tla.html) and its model checker TLC. Its warning about textbook drift comes from [SysMoBench](https://arxiv.org/abs/2509.23130), and Boris Cherny's [post](https://x.com/bcherny/status/2102543349102338309) on Lean and TLA+ is its example of the approach.
- `browser` uses Vercel's [agent-browser](https://github.com/vercel-labs/agent-browser) (Apache-2.0) and Microsoft's [Playwright](https://playwright.dev/python/). Neither is bundled here.

## License

MIT. See [LICENSE](LICENSE); each skill folder carries the same notice.
