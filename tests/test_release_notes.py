"""Tests for scripts/release_notes.py."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import release_notes  # noqa: E402

CHANGELOG = """# Changelog

## Unreleased

## 2026.10.20 - 2026-10-20

- Added [CONTRIBUTING.md](CONTRIBUTING.md) and [a section](#x), see [spec](https://agentskills.io).

## 1.0.0 - 2026-09-01

- First release.
"""


class ReleaseNotesTest(unittest.TestCase):
    def test_section_by_bare_version_and_tag(self):
        self.assertIn("CONTRIBUTING", release_notes.section(CHANGELOG, "2026.10.20"))
        self.assertEqual(release_notes.section(CHANGELOG, "v1.0.0"), "- First release.")

    def test_empty_or_missing_section(self):
        self.assertEqual(release_notes.section(CHANGELOG, "Unreleased"), "")
        self.assertIsNone(release_notes.section(CHANGELOG, "2099.01.01"))

    def test_relative_links_point_at_the_tag(self):
        notes = release_notes.absolute_links(release_notes.section(CHANGELOG, "2026.10.20"), "2026.10.20")
        self.assertIn("](https://github.com/derwells/skills/blob/v2026.10.20/CONTRIBUTING.md)", notes)
        self.assertIn("](#x)", notes)
        self.assertIn("](https://agentskills.io)", notes)


if __name__ == "__main__":
    unittest.main()
