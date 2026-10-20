# Changelog

Changes to the collection as a whole. Each skill with its own history keeps it in its folder, for example [skills/learn/CHANGELOG.md](skills/learn/CHANGELOG.md).

Release headings read `## <version> - <date>`. Versions are dates, `YYYY.MM.DD`, and git tags are the same with a leading `v`. See [docs/releasing.md](docs/releasing.md).

## Unreleased

### Added

- Repository docs: install, update and pinning instructions for Claude Code and Codex, [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), issue and pull request templates, and [docs/releasing.md](docs/releasing.md). The long migration section for old `learn` clones moved to [docs/migrating-from-learn-skill.md](docs/migrating-from-learn-skill.md).
- CI checks beyond the frontmatter spec: public hygiene (no home paths, tailnet hosts or addresses, key-like strings or personal email addresses in text files), Markdown anchors, Python files compile, a CHANGELOG with an Unreleased section, and the plugin manifest's paths. CI also runs the validator's unit tests, an install test that executes the README's install commands in a temporary home directory, and the browser benchmark's `reproduce.py`.
- `.claude-plugin/marketplace.json`, so `/plugin marketplace add derwells/skills` offers the four skills as one Claude Code plugin.
- `skills/browser/benchmarks/`: dated synthetic comparison of ways to drive a browser, with per-run data and `reproduce.py` (2026-10-18).
- `access` and `browser` skills, using agent-browser, Playwright and an unlocked password manager CLI (2026-10-18).

### Changed

- The repository is now a collection: `learn` moved from the repository root to `skills/learn/`, and every skill folder carries its own `LICENSE` (2026-10-18). Existing clones of the old layout need the [migration steps](docs/migrating-from-learn-skill.md); the `learn-standalone` tag keeps the old layout.
- `model-check` now triggers on a concrete, costly ordering or concurrency failure that focused tests can't settle, a new multi-party protocol with an uncertain invariant, code an existing model describes, or an explicit request. Touching a queue, retry, timeout or state machine no longer counts. The skill opens with three questions that usually end in "No model" and ordinary tests. Routing cases and before/after results are in [skills/model-check/evals](skills/model-check/evals/README.md).
- README reorganised around a catalogue with per-skill prerequisites, install commands that CI executes, and a plain statement of scope and limits.

## learn-standalone (tag, 2026-09-29)

Not a release. Marks the last commit where `learn` was the only skill, at the repository root.

## 1.0.0 - 2026-09-01

Tag `v1.0.0`. First public version of the `learn` skill, when this repository held only that skill (then named `learn-skill`). Added CI that validates `SKILL.md` frontmatter against the Agent Skills spec. Details of the skill itself are in [skills/learn/CHANGELOG.md](skills/learn/CHANGELOG.md).
