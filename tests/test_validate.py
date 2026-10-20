"""Unit tests for scripts/validate.py and scripts/release_notes.py.

Each test builds a small fixture repository in a temporary directory. A valid
tree passes every check, and each deliberately broken variant must fail the
check that is meant to catch it. Strings that look like leaked private data are
assembled at run time so this file does not trip the hygiene check itself.
"""

import contextlib
import io
import json
import pathlib
import sys
import tempfile
import textwrap
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import release_notes  # noqa: E402
import validate  # noqa: E402

SKILL_MD = textwrap.dedent(
    """\
    ---
    name: demo
    description: Use when a test needs a demo skill.
    license: MIT
    ---

    # demo

    Read references/guide.md for details.
    """
)
README = textwrap.dedent(
    """\
    # Fixture

    | Skill | What |
    |---|---|
    | [demo](skills/demo) | A demo. |

    ## Install
    """
)
CHANGELOG = "# Changelog\n\n## Unreleased\n\n- Something.\n"


def build_repo(root):
    """Write a valid fixture repository under root."""
    skill = root / "skills" / "demo"
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text(SKILL_MD)
    (skill / "LICENSE").write_text("MIT License\n")
    (skill / "references" / "guide.md").write_text("# Guide\n")
    (root / "README.md").write_text(README)
    (root / "CHANGELOG.md").write_text(CHANGELOG)


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = pathlib.Path(self._tmp.name)
        build_repo(self.root)

    def edit(self, rel, old, new):
        path = self.root / rel
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def assertFails(self, check, fragment):
        errors = check(self.root)
        self.assertTrue(any(fragment in e for e in errors), f"{fragment!r} not in {errors}")
        self.assertTrue(validate.run_checks(self.root))


class ValidTreeTest(FixtureCase):
    def test_valid_tree_passes_every_check(self):
        self.assertEqual(validate.run_checks(self.root), [])

    def test_main_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(validate.main(["validate.py", str(self.root)]), 0)
            (self.root / "skills" / "demo" / "LICENSE").unlink()
            self.assertEqual(validate.main(["validate.py", str(self.root)]), 1)


class SkillChecksTest(FixtureCase):
    def test_name_not_matching_directory(self):
        self.edit("skills/demo/SKILL.md", "name: demo", "name: other")
        self.assertFails(validate.check_skills, "does not match its directory")

    def test_bad_name_characters(self):
        (self.root / "skills" / "demo").rename(self.root / "skills" / "Demo_Skill")
        self.edit("skills/Demo_Skill/SKILL.md", "name: demo", "name: Demo_Skill")
        self.assertFails(validate.check_skills, "lowercase-hyphenated")

    def test_extra_frontmatter_field(self):
        self.edit("skills/demo/SKILL.md", "license: MIT", "license: MIT\nversion: 2")
        self.assertFails(validate.check_skills, "non-spec frontmatter fields")

    def test_missing_license(self):
        (self.root / "skills" / "demo" / "LICENSE").unlink()
        self.assertFails(validate.check_skills, "missing LICENSE")

    def test_missing_frontmatter(self):
        (self.root / "skills/demo/SKILL.md").write_text("# no frontmatter\n")
        self.assertFails(validate.check_skills, "must start with YAML frontmatter")

    def test_description_too_long(self):
        self.edit("skills/demo/SKILL.md", "Use when a test needs a demo skill.", "x" * 1600)
        self.assertFails(validate.check_skills, "limit 1536")

    def test_missing_bundled_file(self):
        (self.root / "skills/demo/references/guide.md").unlink()
        self.assertFails(validate.check_skills, "missing file: references/guide.md")


class CatalogueTest(FixtureCase):
    def test_skill_missing_from_readme(self):
        self.edit("README.md", "| [demo](skills/demo) | A demo. |", "")
        self.assertFails(validate.check_catalogue, "does not match skills/")

    def test_readme_row_without_skill(self):
        self.edit("README.md", "| A demo. |", "| A demo. |\n| [ghost](skills/ghost) | None. |")
        self.assertFails(validate.check_catalogue, "does not match skills/")


class LinkTest(FixtureCase):
    def test_broken_relative_link(self):
        self.edit("README.md", "## Install", "See [guide](docs/nope.md).")
        self.assertFails(validate.check_links, "broken link docs/nope.md")

    def test_broken_anchor(self):
        self.edit("README.md", "## Install", "See [it](#not-a-heading).")
        self.assertFails(validate.check_links, "no heading for anchor")

    def test_good_anchor_and_external_link_pass(self):
        self.edit("README.md", "## Install", "## Install\n\nSee [it](#install) and [web](https://example.com/x).")
        self.assertEqual(validate.check_links(self.root), [])

    def test_link_inside_inline_code_is_ignored(self):
        self.edit("README.md", "## Install", "Write `[x](missing.md)` like this.")
        self.assertEqual(validate.check_links(self.root), [])

    def test_link_inside_code_block_is_ignored(self):
        self.edit("README.md", "## Install", "```\n[x](missing.md)\n```")
        self.assertEqual(validate.check_links(self.root), [])


class HygieneTest(FixtureCase):
    def leak(self, text):
        (self.root / "notes.txt").write_text(text + "\n")

    def test_home_path_is_flagged(self):
        self.leak("see " + "/hom" + "e/alice/projects/x")
        self.assertFails(validate.check_hygiene, "absolute home path")

    def test_macos_home_path_is_flagged(self):
        self.leak("see " + "/Use" + "rs/alice/Desktop")
        self.assertFails(validate.check_hygiene, "absolute home path")

    def test_tailnet_host_is_flagged(self):
        self.leak("ssh box." + "tail1234." + "ts" + ".net")
        self.assertFails(validate.check_hygiene, "tailnet host")

    def test_tailnet_range_ip_is_flagged(self):
        self.leak("host 100" + ".101.2.3")
        self.assertFails(validate.check_hygiene, "tailnet-range IP")

    def test_ip_outside_the_range_is_fine(self):
        self.leak("host 100" + ".63.2.3 and 100" + ".128.0.1")
        self.assertEqual(validate.check_hygiene(self.root), [])

    def test_private_key_is_flagged(self):
        self.leak("-----BEGIN " + "RSA PRIVATE" + " KEY-----")
        self.assertFails(validate.check_hygiene, "private key")

    def test_token_like_strings_are_flagged(self):
        for prefix, label in (("gh" + "p_", "GitHub token"), ("s" + "k-", "API key"), ("xox" + "b-", "Slack token")):
            with self.subTest(label=label):
                self.leak("token " + prefix + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8")
                self.assertFails(validate.check_hygiene, label)

    def test_personal_email_is_flagged_and_allowlist_passes(self):
        self.leak("mail " + "someone" + "@" + "gmail.com")
        self.assertFails(validate.check_hygiene, "email address")
        self.leak("1234+user@users.noreply.github.com and a@example.com")
        self.assertEqual(validate.check_hygiene(self.root), [])

    def test_version_pins_are_not_emails(self):
        self.leak("npm i pkg@2.0.0 and plugin@marketplace")
        self.assertEqual(validate.check_hygiene(self.root), [])

    def test_binary_files_are_skipped(self):
        (self.root / "image.png").write_bytes(b"\x89PNG\xff\xfe" + b"/hom" + b"e/alice")
        self.assertEqual(validate.check_hygiene(self.root), [])


class OtherChecksTest(FixtureCase):
    def test_python_syntax_error(self):
        (self.root / "skills/demo/broken.py").write_text("def f(:\n")
        self.assertFails(validate.check_python_compiles, "does not compile")

    def test_changelog_without_unreleased(self):
        self.edit("CHANGELOG.md", "## Unreleased", "## 2026.01.01 - 2026-01-01")
        self.assertFails(validate.check_changelog, "Unreleased")

    def test_missing_changelog(self):
        (self.root / "CHANGELOG.md").unlink()
        self.assertFails(validate.check_changelog, "missing")

    def write_manifest(self, source):
        (self.root / ".claude-plugin").mkdir()
        manifest = {"name": "m", "owner": {"name": "o"}, "plugins": [{"name": "p", "source": source}]}
        (self.root / ".claude-plugin" / "marketplace.json").write_text(json.dumps(manifest))

    def test_marketplace_manifest_valid(self):
        self.write_manifest("./")
        self.assertEqual(validate.check_marketplace(self.root), [])

    def test_marketplace_source_missing(self):
        self.write_manifest("./nowhere")
        self.assertFails(validate.check_marketplace, "not a directory")

    def test_marketplace_invalid_json(self):
        (self.root / ".claude-plugin").mkdir()
        (self.root / ".claude-plugin" / "marketplace.json").write_text("{")
        self.assertFails(validate.check_marketplace, "invalid JSON")


class ReleaseNotesTest(unittest.TestCase):
    TEXT = textwrap.dedent(
        """\
        # Changelog

        ## Unreleased

        ### Added

        - New thing.

        ## 2026.10.20 - 2026-10-20

        - Older thing.

        ## 1.0.0 - 2026-09-01

        - First.
        """
    )

    def test_extracts_section_without_heading(self):
        self.assertEqual(release_notes.section(self.TEXT, "2026.10.20"), "- Older thing.")

    def test_accepts_tag_form(self):
        self.assertEqual(release_notes.section(self.TEXT, "v1.0.0"), "- First.")

    def test_unreleased_keeps_subheadings(self):
        self.assertEqual(release_notes.section(self.TEXT, "Unreleased"), "### Added\n\n- New thing.")

    def test_prefix_of_another_version_does_not_match(self):
        self.assertIsNone(release_notes.section(self.TEXT, "2026.10"))

    def test_unknown_version(self):
        self.assertIsNone(release_notes.section(self.TEXT, "3000.01.01"))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "CHANGELOG.md"
            path.write_text(self.TEXT)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(release_notes.main(["r", "v1.0.0", str(path)]), 0)
                self.assertEqual(release_notes.main(["r", "9999", str(path)]), 1)


if __name__ == "__main__":
    unittest.main()
