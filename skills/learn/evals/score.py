#!/usr/bin/env python3
"""Recompute the eval tables in README.md from cases.json and results/*.jsonl.

Standard library only. Run from anywhere:

  python3 score.py          check the README tables; exit 1 if they differ
  python3 score.py --write  rewrite the tables in README.md

A criterion is met when the recorded answer equals the expected answer in
cases.json. Judged answers come from the judge model; mechanical answers come
from the checks in run.py.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
START, END = "<!-- results:start -->", "<!-- results:end -->"
RUNS = [
    ("before-opus", "Previous skill, Claude Opus 5.5"),
    ("after-opus", "This skill, Claude Opus 5.5"),
    ("after-astra", "This skill, Codex gpt-6-astra"),
]


def load(label):
    path = HERE / "results" / f"{label}.jsonl"
    if not path.exists():
        return None
    return {r["case"]: r for r in map(json.loads, path.read_text().splitlines()) if r}


def met(case, row):
    """(criteria met, criteria total) for one case in one run."""
    hits = 0
    for crit in case["criteria"]:
        source = row["mechanical"] if crit.get("type") == "mechanical" else row["verdicts"]
        answer = source.get(crit["id"])
        if isinstance(answer, dict):
            answer = answer.get("answer")
        hits += answer == crit["expect"]
    return hits, len(case["criteria"])


def tables():
    cases = json.loads((HERE / "cases.json").read_text())
    runs = [(label, title, load(label)) for label, title in RUNS]
    runs = [r for r in runs if r[2] is not None]
    lines = ["| Run | Criteria met | Cases with every criterion met |", "|---|---|---|"]
    for label, title, rows in runs:
        scored = [met(c, rows[c["id"]]) for c in cases if c["id"] in rows]
        lines.append(f"| {title} | {sum(h for h, _ in scored)} of {sum(n for _, n in scored)} "
                     f"| {sum(h == n for h, n in scored)} of {len(scored)} |")
    lines += ["", "| Case | " + " | ".join(title for _, title, _ in runs) + " |", "|---|" + "---|" * len(runs)]
    for case in cases:
        cells = []
        for _, _, rows in runs:
            if case["id"] in rows:
                cells.append("{} of {}".format(*met(case, rows[case["id"]])))
            else:
                cells.append("not run")
        lines.append(f"| {case['id']} {case['name']} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    readme = HERE / "README.md"
    text = readme.read_text()
    head, rest = text.split(START, 1)
    published, tail = rest.split(END, 1)
    fresh = "\n" + tables() + "\n"
    if "--write" in sys.argv:
        readme.write_text(head + START + fresh + END + tail)
        print("README.md tables rewritten")
        return 0
    if published != fresh:
        print("README.md tables differ from results/. Recomputed tables:\n" + fresh)
        return 1
    print("README.md tables match results/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
