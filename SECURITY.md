# Security

This repository holds Markdown instructions for agents plus a few small Python scripts. It has no service and handles no data of its own. The risks that fit it are:

- a skill that leads an agent to run something harmful or leak a credential
- a secret, private path or personal detail committed by mistake
- a script under `skills/` that does something it shouldn't

## Reporting

GitHub private vulnerability reporting is not turned on for this repository. Open an [issue](https://github.com/derwells/skills/issues/new) titled "security: <skill>" that says which file is affected and why, without exploit details or live secrets. I'll ask for specifics in the issue if I need them. If you found a committed secret, rotate it first; deleting it from the repository does not make it safe.

I fix what I can when I can. I make no promise about response time.

## Supported versions

Only the latest commit on `main`. There are no backported fixes.

## What the skills do

- `access` and `browser` drive real browser sessions and may fill passwords from a password manager CLI you have unlocked. They are written to keep secret values out of the model's context, but treat that as a design intent and not a guarantee. Read the skill before you use it with an account you care about.
- `model-check` and `learn` write files in your project (`.learning/`, TLA+ models). `model-check` runs Java and TLC on models it writes.
- CI scans for the common ways a secret or private path ends up in the repository (`scripts/validate.py`). It is a guard, not an audit.
