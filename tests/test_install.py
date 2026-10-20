"""Run the README's install commands in a temporary home directory.

The commands come from fenced blocks in README.md that are preceded by an HTML
comment such as `<!-- install:clone -->`, so the README cannot drift from this
test. The clone URL is rewritten to a snapshot of the working tree, committed
on a `main` branch, so the test covers uncommitted files and works from a
detached checkout such as a CI pull request merge. Then every skill in
skills/ must resolve to a directory with a SKILL.md for both Claude Code and
Codex, and the copy alternative must keep SKILL.md and LICENSE.

Run: python3 tests/test_install.py   (or python3 -m unittest discover -s tests)
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO_URL = re.compile(r"https://github\.com/derwells/skills(?:\.git)?")
BLOCK = re.compile(r"<!-- install:(\w+) -->\s*\n```\w*\n(.*?)\n```", re.S)
SKILLS_DIRS = {"claude": ".claude/skills", "codex": ".agents/skills"}


def install_blocks(readme_text):
    """Map block name to shell script for every marked block in the README."""
    return {name: script for name, script in BLOCK.findall(readme_text)}


def run_script(script, home, repo):
    """Run a shell script with HOME set to a temp dir; repo URL points at repo."""
    local = REPO_URL.sub(str(repo), script)
    env = {
        "HOME": str(home),
        "PATH": os.environ["PATH"],
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
    }
    result = subprocess.run(
        ["bash", "-euo", "pipefail", "-c", local],
        env=env, capture_output=True, text=True, cwd=home,
    )
    if result.returncode:
        raise AssertionError(f"install block failed:\n{local}\n{result.stdout}{result.stderr}")


GIT_ENV = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_AUTHOR_NAME": "install-test",
    "GIT_AUTHOR_EMAIL": "install-test@example.com",
    "GIT_COMMITTER_NAME": "install-test",
    "GIT_COMMITTER_EMAIL": "install-test@example.com",
}


def snapshot_repo(repo, dest):
    """Copy the files git would track into dest and commit them on main."""
    listed = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True, check=True,
    ).stdout.decode().split("\0")
    for name in filter(None, listed):
        source = repo / name
        if source.is_file():
            target = dest / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    env = {**os.environ, **GIT_ENV}
    for cmd in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "-m", "snapshot"]):
        subprocess.run(["git", "-C", str(dest), *cmd], env=env, check=True, capture_output=True)
    return dest


def skill_names(repo):
    return sorted(p.parent.name for p in repo.glob("skills/*/SKILL.md"))


def check_install(repo, readme_text):
    """Return a list of problems with the README's install blocks against repo."""
    blocks = install_blocks(readme_text)
    missing = {"clone", "claude", "codex", "update", "copy"} - blocks.keys()
    if missing:
        return [f"README has no install block for: {sorted(missing)}"]
    if not REPO_URL.search(blocks["clone"]):
        return ["the clone block does not clone https://github.com/derwells/skills"]

    errors = []
    names = skill_names(repo)
    with tempfile.TemporaryDirectory() as tmp:
        source = pathlib.Path(tmp) / "source"
        source.mkdir()
        snapshot_repo(repo, source)
        home = pathlib.Path(tmp) / "home"
        home.mkdir()
        try:
            for name in ("clone", "claude", "codex", "update"):
                run_script(blocks[name], home, source)
        except AssertionError as exc:
            return [str(exc)]
        for harness, rel in SKILLS_DIRS.items():
            for skill in names:
                target = home / rel / skill
                if not (target / "SKILL.md").is_file():
                    errors.append(f"{harness}: {rel}/{skill} does not resolve to a folder with SKILL.md")

        copy_home = pathlib.Path(tmp) / "copy-home"
        copy_home.mkdir()
        try:
            run_script(blocks["clone"], copy_home, source)
            run_script(blocks["copy"], copy_home, source)
        except AssertionError as exc:
            return errors + [str(exc)]
        copied = [p for p in (copy_home / ".claude/skills").iterdir() if p.is_dir() and not p.is_symlink()]
        if not copied:
            errors.append("copy block did not copy a skill folder")
        for folder in copied:
            for required in ("SKILL.md", "LICENSE"):
                if not (folder / required).is_file():
                    errors.append(f"copy: {folder.name} is missing {required}")
    return errors


class ReadmeInstallTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "needs git and bash")
    def test_readme_install_commands_work(self):
        self.assertEqual(check_install(ROOT, (ROOT / "README.md").read_text()), [])


class BrokenReadmeTest(unittest.TestCase):
    """A README that drifts from the repository must fail."""

    def readme(self):
        return (ROOT / "README.md").read_text()

    @unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "needs git and bash")
    def test_skill_left_out_of_the_loop_fails(self):
        broken = self.readme().replace("learn access browser model-check", "learn access browser")
        errors = check_install(ROOT, broken)
        self.assertTrue(any("model-check" in e for e in errors), errors)

    def test_missing_marker_fails(self):
        broken = self.readme().replace("<!-- install:codex -->", "")
        self.assertIn("codex", " ".join(check_install(ROOT, broken)))

    @unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "needs git and bash")
    def test_wrong_link_target_fails(self):
        broken = self.readme().replace("/skills/$skill", "/skill/$skill")
        self.assertTrue(check_install(ROOT, broken))


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
