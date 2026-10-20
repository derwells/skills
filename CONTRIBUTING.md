# Contributing

This is a personal collection, and I'm the only maintainer. Issues and small pull requests are welcome. I read them when I can and make no promise about when I'll answer. If a change doesn't fit how I use the skills, I may decline it; you're free to fork under the MIT license.

For a bug, say which skill, which harness and version, and what the agent did versus what you expected. For a larger change, open an issue first so you don't spend time on something I won't merge.

## Skill layout

Each skill is a folder `skills/<name>/`:

- The folder name equals the `name` in `SKILL.md`: lowercase letters, digits and single hyphens, at most 64 characters.
- `SKILL.md` starts with YAML frontmatter that uses only fields from the [Agent Skills spec](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Anything else breaks packaging for some harnesses. The description is required and at most 1536 characters. It says when to use the skill, since that is what the agent reads to decide.
- A `LICENSE` file sits in the folder, so a copied folder keeps its notice.
- Files the skill bundles (`references/`, `scripts/`, `assets/`, `examples/`, `benchmarks/`) are referenced from `SKILL.md` by relative path, and each reference points at a file that exists.
- Nothing private: no absolute home paths, internal hosts or addresses, credentials, client or employer names, or personal email addresses. Examples use made-up data. `scripts/validate.py` catches the common patterns, not everything, so read your diff.

## Checks

Python 3 and PyYAML are all you need (`pip install pyyaml`). From the repository root:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 skills/browser/benchmarks/reproduce.py
python3 skills/model-check/evals/score.py
```

`validate.py` checks:

- each `SKILL.md`: frontmatter fields, name matches folder, description length, bundled files exist
- the README catalogue rows match the folders in `skills/`, and every skill has a `LICENSE`
- relative Markdown links and `#anchors` resolve
- text files contain no home paths, tailnet hosts or addresses, private keys, token-like strings or personal email addresses
- every Python file compiles
- `CHANGELOG.md` has an `## Unreleased` section
- `.claude-plugin/marketplace.json` is valid and its source path exists

The unit tests in `tests/` run the validator against small fixture trees, one deliberately broken per check, and `tests/test_install.py` runs the README's install commands in a temporary home directory. CI runs all of this on every push and pull request (`.github/workflows/validate.yml`). If you use Claude Code, `claude plugin validate .` also checks the plugin manifest.

## Adding a skill

1. Create `skills/<name>/SKILL.md` and `skills/<name>/LICENSE` (copy the MIT text from another skill's folder).
2. Add a row to the README catalogue. Keep the `| [name](skills/name) |` form; the validator parses it. Include what it needs installed.
3. Add the name to the `for skill in ...` loops in the README install blocks, so the install test links it.
4. Add a line under `## Unreleased` in `CHANGELOG.md`.
5. Run the checks above.

If the skill claims results, such as speed or accuracy, put the data in the skill's folder with a script that recomputes the numbers, as `skills/browser/benchmarks/` does, and state the limits.

## Pull requests

Keep them small and about one thing. Describe what changed and why in the first lines. Use plain sentences in docs and skill text; no marketing, and no claims you didn't test.
