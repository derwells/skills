# Migrating from the learn-skill repository

This repo used to be called `learn-skill` and held only the `learn` skill. GitHub redirects the old URL, so existing clones still pull. You can point yours at the new name:

```bash
git -C <your clone> remote set-url origin https://github.com/derwells/skills
```

The old instructions cloned the whole repo straight into `~/.claude/skills/learn`. That worked when the repo was only `learn`. Now `learn` lives in `skills/learn/`, so a plain `git pull` in the old location leaves no `SKILL.md` at the top and the skill stops loading.

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

Back to the [README](../README.md).
