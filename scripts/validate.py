"""Validate the skills repository.

Usage: python3 scripts/validate.py [repo-root]

Checks, each returning a list of error strings:

- every skills/<name>/SKILL.md against the Agent Skills spec
- the README catalogue against skills/, plus a LICENSE in every skill folder
- relative Markdown links and in-page anchors
- public hygiene: no private paths, hosts, keys or personal emails in text files
- every bundled Python file compiles
- CHANGELOG.md has an Unreleased section
- .claude-plugin/marketplace.json, when present, is well formed and points at real paths

Exit code 1 if any check reports an error. Needs Python 3 and PyYAML.
"""

import json
import pathlib
import re
import subprocess
import sys

import yaml

DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BUNDLED = re.compile(r"(?<![\w/.-])((?:references|scripts|assets|agents|examples|benchmarks)/[\w./-]+\.\w+)")
LINK = re.compile(r"\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)
CATALOGUE_ROW = re.compile(r"^\| \[([\w-]+)\]\(skills/\1\)", re.M)

# Generic patterns for things that must not appear in a public repository.
# Written so that this file does not match its own patterns.
_PRIVATE_IPV4 = r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b"
HYGIENE_PATTERNS = [
    ("absolute home path", re.compile(r"(?<![\w~.])/(?:home|Users)/[A-Za-z_][\w.-]*")),
    ("tailnet host name", re.compile(r"\b[\w-]+(?:\.[\w-]+)*\.ts\.net\b")),
    ("tailnet-range IP address", re.compile(_PRIVATE_IPV4)),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]
EMAIL = re.compile(r"[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
ALLOWED_EMAIL_DOMAINS = {"users.noreply.github.com", "noreply.github.com", "example.com", "example.org"}
SKIP_DIRS = {".git", "__pycache__", "node_modules"}


def tracked_files(root):
    """Files git tracks or would track under root (ignored files excluded);
    every file outside .git if root is not a repository."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True, check=True,
        ).stdout.decode()
        names = [n for n in out.split("\0") if n]
        if names:
            return sorted(root / n for n in names if (root / n).is_file())
    except (OSError, subprocess.CalledProcessError):
        pass
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and not SKIP_DIRS & set(p.relative_to(root).parts)
    )


def read_text(path):
    """File contents, or None for binary files."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def find_skills(root):
    return sorted(p.parent for p in root.glob("skills/*/SKILL.md"))


def parse_frontmatter(text):
    parts = text.split("---\n")
    if len(parts) < 3 or parts[0]:
        return None
    return yaml.safe_load(parts[1]) or {}


def check_skill(root, skill):
    rel = skill.relative_to(root)
    text = (skill / "SKILL.md").read_text()
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{rel}: SKILL.md must start with YAML frontmatter"]

    errors = []
    extra = set(fm) - SPEC_FIELDS
    if extra:
        errors.append(f"{rel}: non-spec frontmatter fields (break claude.ai packaging): {sorted(extra)}")
    name = fm.get("name", "")
    if name != skill.name:
        errors.append(f"{rel}: name {name!r} does not match its directory")
    if not NAME.match(str(name)) or len(str(name)) > 64:
        errors.append(f"{rel}: name {name!r} is not lowercase-hyphenated or is over 64 chars")
    if not fm.get("description"):
        errors.append(f"{rel}: description is required")
    elif len(fm["description"]) > 1536:
        errors.append(f"{rel}: description is {len(fm['description'])} chars (limit 1536)")
    if fm.get("compatibility") and len(fm["compatibility"]) > 500:
        errors.append(f"{rel}: compatibility exceeds 500 chars")
    for ref in sorted(set(BUNDLED.findall(text))):
        if not (skill / ref).is_file():
            errors.append(f"{rel}: SKILL.md points at missing file: {ref}")
    if not (skill / "LICENSE").is_file():
        errors.append(f"{rel}: missing LICENSE, so copied folders lose the notice")
    return errors


def check_skills(root):
    skills = find_skills(root)
    if not skills:
        return ["no skills/<name>/SKILL.md found"]
    errors = []
    for skill in skills:
        errors += check_skill(root, skill)
    return errors


def check_catalogue(root):
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md is missing"]
    listed = set(CATALOGUE_ROW.findall(readme.read_text()))
    present = {s.name for s in find_skills(root)}
    if listed != present:
        return [f"README catalogue {sorted(listed)} does not match skills/ {sorted(present)}"]
    return []


def github_slug(heading):
    """Anchor GitHub generates for a heading."""
    text = re.sub(r"`|\*|_(?=\S)|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", heading)
    text = re.sub(r"[^\w\- ]", "", text.lower())
    return text.replace(" ", "-")


def anchors_in(path, cache):
    if path not in cache:
        text = re.sub(r"^```.*?^```", "", path.read_text(), flags=re.M | re.S)
        cache[path] = {github_slug(h) for h in HEADING.findall(text)}
    return cache[path]


def strip_code(text):
    """Markdown text without fenced blocks and inline code spans."""
    text = re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def check_links(root):
    errors = []
    anchor_cache = {}
    for md in (p for p in tracked_files(root) if p.suffix == ".md"):
        text = strip_code(md.read_text())
        for target in LINK.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue
            path, _, anchor = target.partition("#")
            resolved = (md.parent / path) if path else md
            if not resolved.exists():
                errors.append(f"{md.relative_to(root)}: broken link {target}")
            elif anchor and resolved.suffix == ".md" and anchor not in anchors_in(resolved, anchor_cache):
                errors.append(f"{md.relative_to(root)}: no heading for anchor {target}")
    return errors


def check_hygiene(root):
    errors = []
    for path in tracked_files(root):
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root)
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pattern in HYGIENE_PATTERNS:
                if pattern.search(line):
                    errors.append(f"{rel}:{lineno}: {label}")
            for match in EMAIL.finditer(line):
                domain = match.group(0).rsplit("@", 1)[1].lower()
                if domain not in ALLOWED_EMAIL_DOMAINS:
                    errors.append(f"{rel}:{lineno}: email address")
    return errors


def check_python_compiles(root):
    errors = []
    for path in (p for p in tracked_files(root) if p.suffix == ".py"):
        try:
            compile(path.read_text(), str(path), "exec")
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(root)}: does not compile: {exc}")
    return errors


def check_changelog(root):
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return ["CHANGELOG.md is missing"]
    if not re.search(r"^## Unreleased\s*$", changelog.read_text(), re.M):
        return ["CHANGELOG.md has no '## Unreleased' section"]
    return []


def check_marketplace(root):
    manifest = root / ".claude-plugin" / "marketplace.json"
    if not manifest.is_file():
        return []
    try:
        data = json.loads(manifest.read_text())
    except json.JSONDecodeError as exc:
        return [f".claude-plugin/marketplace.json: invalid JSON: {exc}"]
    errors = []
    for key in ("name", "owner", "plugins"):
        if not data.get(key):
            errors.append(f".claude-plugin/marketplace.json: missing {key!r}")
    for plugin in data.get("plugins") or []:
        source = plugin.get("source")
        if not plugin.get("name") or not isinstance(source, str):
            errors.append(f".claude-plugin/marketplace.json: plugin needs a name and a relative-path source: {plugin}")
        elif not (root / source).is_dir():
            errors.append(f".claude-plugin/marketplace.json: source {source!r} is not a directory")
        elif not (root / source / "skills").is_dir():
            errors.append(f".claude-plugin/marketplace.json: source {source!r} has no skills/ directory")
    return errors


CHECKS = [
    check_skills,
    check_catalogue,
    check_links,
    check_hygiene,
    check_python_compiles,
    check_changelog,
    check_marketplace,
]


def run_checks(root):
    errors = []
    for check in CHECKS:
        errors += check(root)
    return errors


def main(argv):
    root = pathlib.Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_ROOT
    errors = run_checks(root)
    for err in errors:
        print(f"ERROR: {err}")
    print(f"checked {len(find_skills(root))} skills, {len(CHECKS)} checks, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
