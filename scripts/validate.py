"""Check each skills/<name>/SKILL.md against the Agent Skills spec, and check
that relative links in the repository's Markdown files point at real files."""

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BUNDLED = re.compile(r"(?<![\w/.-])((?:references|scripts|assets|agents|examples)/[\w./-]+\.\w+)")
LINK = re.compile(r"\]\(([^)\s]+)\)")

errors = []

skills = sorted(p.parent for p in ROOT.glob("skills/*/SKILL.md"))
if not skills:
    errors.append("no skills/<name>/SKILL.md found")

for skill in skills:
    rel = skill.relative_to(ROOT)
    text = (skill / "SKILL.md").read_text()
    parts = text.split("---\n")
    if len(parts) < 3 or parts[0]:
        errors.append(f"{rel}: SKILL.md must start with YAML frontmatter")
        continue
    fm = yaml.safe_load(parts[1])

    extra = set(fm) - SPEC_FIELDS
    if extra:
        errors.append(f"{rel}: non-spec frontmatter fields (break claude.ai packaging): {sorted(extra)}")
    name = fm.get("name", "")
    if name != skill.name:
        errors.append(f"{rel}: name {name!r} does not match its directory")
    if not NAME.match(name) or len(name) > 64:
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

for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for target in LINK.findall(md.read_text()):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        path = target.split("#")[0]
        if path and not (md.parent / path).exists():
            errors.append(f"{md.relative_to(ROOT)}: broken link {target}")

for err in errors:
    print(f"ERROR: {err}")
print(f"checked {len(skills)} skills")
sys.exit(1 if errors else 0)
