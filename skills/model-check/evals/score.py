#!/usr/bin/env python3
"""Recompute the routing eval table in README.md from cases.json and
results/*.jsonl, and check it against the table as published.

Standard library only. Run from anywhere:  python3 score.py
Exit code 0 if every number matches, 1 otherwise.

"Loaded" means the judge would load model-check from the routing line and
description alone. "Modelled" means it answered "yes" or "conditional" to
writing a formal model. Cases marked "either" are listed but not scored.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

RUNS = {
    "routing-before": "Routing, before",
    "routing-after": "Routing, after",
    "forced-before": "Forced load, before",
    "forced-after": "Forced load, after",
}


def published_rows():
    """README table cells per run label, e.g. ["7 of 9", "0 of 9", ...]."""
    rows = {}
    for line in (HERE / "README.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] in RUNS.values():
            rows[cells[0]] = cells[1:]
    return rows


def cell(count, n):
    return "n/a" if count is None else f"{count} of {n}"


def load_rows(path):
    return {r["tid"]: r for r in map(json.loads, path.read_text().splitlines()) if r}


def summarize(cases, rows):
    out = {}
    for expected in ("tests", "model"):
        tids = [c["tid"] for c in cases if c["expected"] == expected and c["tid"] in rows]
        loaded = sum(1 for t in tids if rows[t].get("load")) if all("load" in rows[t] for t in tids) else None
        modelled = sum(1 for t in tids if rows[t]["model"] in ("yes", "conditional"))
        out[expected] = (loaded, modelled)
    return out


def main():
    cases = json.loads((HERE / "cases.json").read_text())
    by_tid = {c["tid"]: c for c in cases}
    published = published_rows()
    mismatches = []
    for name, label in RUNS.items():
        path = HERE / "results" / f"{name}.jsonl"
        if not path.exists():
            mismatches.append(f"{name}: missing {path.name}")
            continue
        rows = load_rows(path)
        unknown = set(rows) - set(by_tid)
        if unknown:
            mismatches.append(f"{name}: answers for unknown cases {sorted(unknown)}")
            continue
        got = summarize(cases, rows)
        cells = []
        print(name)
        for expected, (loaded, modelled) in got.items():
            n = sum(1 for t in rows if by_tid[t]["expected"] == expected)
            cells += [cell(loaded, n), cell(modelled, n)]
            print(f"  expected {expected:5}  loaded {cell(loaded, n):7}  modelled {cell(modelled, n)}")
        if published.get(label) != cells:
            mismatches.append(f"{label}: recomputed {cells}, README has {published.get(label)}")
    for m in mismatches:
        print(f"MISMATCH {m}")
    if not mismatches:
        print("OK: every number matches README.md")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
