"""Print one version's section of CHANGELOG.md, for release notes.

Usage: python3 scripts/release_notes.py <version> [changelog-path]

<version> is "Unreleased", a bare version such as 2026.10.20, or a tag such as
v2026.10.20. Exits 1 if the section is missing or empty. Relative links are
rewritten to point at the files under that tag on GitHub, since a release page
does not resolve them.
"""

import pathlib
import re
import sys

DEFAULT_CHANGELOG = pathlib.Path(__file__).resolve().parent.parent / "CHANGELOG.md"
REPO_URL = "https://github.com/derwells/skills"
RELATIVE_LINK = re.compile(r"\]\((?![a-z]+:|#)([^)\s]+)\)")


def absolute_links(notes, version):
    """Point relative links at the tag's files, or at main for Unreleased."""
    ref = "main" if version == "Unreleased" else "v" + version.removeprefix("v")
    return RELATIVE_LINK.sub(lambda m: f"]({REPO_URL}/blob/{ref}/{m.group(1)})", notes)


def section(changelog_text, version):
    """Body of the '## <version>' section, without its heading, or None."""
    version = version.removeprefix("v") if version != "Unreleased" else version
    sections = re.split(r"^## ", changelog_text, flags=re.M)[1:]
    for body in sections:
        heading, _, rest = body.partition("\n")
        if re.match(rf"{re.escape(version)}(\s|$)", heading):
            return rest.strip()
    return None


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = pathlib.Path(argv[2]) if len(argv) == 3 else DEFAULT_CHANGELOG
    notes = section(path.read_text(), argv[1])
    if not notes:
        print(f"no notes for {argv[1]!r} in {path}", file=sys.stderr)
        return 1
    print(absolute_links(notes, argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
