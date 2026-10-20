# Releasing

A release is a git tag plus a GitHub release whose notes come from [CHANGELOG.md](../CHANGELOG.md). I cut one when there is something worth pinning, not on a schedule.

## Version scheme

Tags are dates: `vYYYY.MM.DD`, for example `v2026.10.20`. A second release on the same day appends `.1`, then `.2`.

The only existing release tag, `v1.0.0`, predates the collection and covers the `learn` skill alone. I switched to dates because a skills collection has no API to break in the semantic-versioning sense, and each skill changes on its own. A date says how old your copy is. What changed is in the changelog. Old tags stay as they are; I don't rewrite them.

## Steps

Run from a clean checkout of `main`, with [`gh`](https://cli.github.com) logged in.

1. Run every check and make sure CI is green on `main`:

   ```bash
   python3 scripts/validate.py
   python3 -m unittest discover -s tests -v
   python3 skills/browser/benchmarks/reproduce.py
   python3 skills/model-check/evals/score.py
   ```

2. In `CHANGELOG.md`, rename `## Unreleased` to `## <version> - <date>` (for example `## 2026.10.20 - 2026-10-20`) and add a fresh empty `## Unreleased` heading above it. Check that the notes read well:

   ```bash
   python3 scripts/release_notes.py 2026.10.20
   ```

3. Commit the changelog and push it. This repo has no deploy step, so pushing `main` publishes nothing beyond the files.

   ```bash
   git add CHANGELOG.md
   git commit -m "Release 2026.10.20"
   git push
   ```

4. Tag that commit and push the tag:

   ```bash
   git tag -a v2026.10.20 -m "2026.10.20"
   git push origin v2026.10.20
   ```

5. Create the GitHub release with the notes from the changelog:

   ```bash
   python3 scripts/release_notes.py 2026.10.20 > /tmp/release-notes.md
   gh release create v2026.10.20 --title "2026.10.20" --notes-file /tmp/release-notes.md
   ```

6. Verify. The release page should show the same notes and the tag should point at the release commit:

   ```bash
   gh release view v2026.10.20
   git ls-remote --tags origin v2026.10.20
   ```

`validate.py` fails if `CHANGELOG.md` has no `## Unreleased` section, which catches a skipped step 2 on the next change.
