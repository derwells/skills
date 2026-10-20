#!/usr/bin/env python3
"""Recompute the routing eval tables in README.md from cases.json and
results/*.jsonl, and check them against the published numbers.

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

# Published in README.md: (loaded, modelled) per expected outcome.
PUBLISHED = {
    "routing-before": {"tests": (7, 0), "model": (5, 5)},
    "routing-after": {"tests": (0, 0), "model": (5, 5)},
    "forced-before": {"tests": (None, 0), "model": (None, 1)},
    "forced-after": {"tests": (None, 0), "model": (None, 1)},
}


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
    mismatches = []
    for name, want in PUBLISHED.items():
        path = HERE / "results" / f"{name}.jsonl"
        if not path.exists():
            mismatches.append(f"{name}: missing {path.name}")
            continue
        rows = load_rows(path)
        got = summarize(cases, rows)
        print(f"{name}")
        for expected, (loaded, modelled) in got.items():
            n = sum(1 for t in rows if by_tid[t]["expected"] == expected)
            shown = "-" if loaded is None else f"{loaded}/{n}"
            print(f"  expected {expected:5}  cases {n:2}  loaded {shown:5}  modelled {modelled}/{n}")
            if (loaded, modelled) != want[expected]:
                mismatches.append(f"{name} {expected}: got {(loaded, modelled)}, published {want[expected]}")
    for m in mismatches:
        print(f"MISMATCH {m}")
    if not mismatches:
        print("OK: every number matches README.md")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
