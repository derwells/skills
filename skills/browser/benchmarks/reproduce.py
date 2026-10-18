#!/usr/bin/env python3
"""Recompute the benchmark aggregates from runs.csv and jev-offline-eval.csv
and compare them with the values published in the original result summaries.

Standard library only. Run from anywhere:  python3 reproduce.py
Exit code 0 if every value matches, 1 otherwise.

Rules copied from the original summarizer: runs.csv holds only counted runs;
wall time is rounded to 0.1 s before taking the median; "tokens" is the sum of
the four recorded frontier token fields (input, cache read, cache create,
output); numbers use Python's "g" format; ranges are (min-max).
"""
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
mismatches = []


def check(label, got, want):
    if got != want:
        mismatches.append(f"{label}: got {got!r}, expected {want!r}")


def medrange(values):
    if not values:
        return "-"
    return f"{statistics.median(values):g} ({min(values):g}-{max(values):g})"


def num(x):
    return float(x) if x not in ("", None) else None


# Expected values, copied from the original summaries (en dashes written as "-").
# Matrix arms A-F-warm: summary.md. Columns: n, success, wall s, turns, tool
# calls, tokens, screenshots, screenshot bytes, retries, duplicates, failures.
EXPECTED_MATRIX = {
    ('A', 'T1'): dict(n=3, success='3/3', wall='43.7 (43.6-53)', turns='45 (42-45)', tool_calls='44 (41-44)', tokens='621990 (621143-622294)', screenshots='11 (11-11)', screenshot_bytes='222000 (221859-222180)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('A', 'T2'): dict(n=3, success='3/3', wall='40.4 (39.7-59.9)', turns='48 (48-49)', tool_calls='47 (47-48)', tokens='898141 (843023-899850)', screenshots='16 (16-16)', screenshot_bytes='326004 (324825-327252)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('A', 'T3'): dict(n=3, success='3/3', wall='57.8 (51.3-69.4)', turns='48 (44-49)', tool_calls='47 (43-48)', tokens='769280 (709004-826026)', screenshots='13 (12-14)', screenshot_bytes='264033 (247503-283413)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('A', 'T4'): dict(n=3, success='0/3', wall='73.9 (70-83.5)', turns='60 (60-60)', tool_calls='53 (52-53)', tokens='2.50284e+06 (2.45565e+06-2.52988e+06)', screenshots='15 (14-15)', screenshot_bytes='282201 (281952-302112)', retries='1 (1-1)', duplicates='0 (0-0)', failures='turn cap'),
    ('B', 'T1'): dict(n=3, success='3/3', wall='65.7 (53.2-69.9)', turns='18 (17-18)', tool_calls='17 (16-17)', tokens='419775 (403537-429281)', screenshots='10 (8-11)', screenshot_bytes='198854 (152989-221973)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('B', 'T2'): dict(n=3, success='3/3', wall='55.8 (54-57.8)', turns='17 (17-18)', tool_calls='16 (16-17)', tokens='409427 (402519-418738)', screenshots='12 (7-12)', screenshot_bytes='234697 (132703-246328)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('B', 'T3'): dict(n=3, success='3/3', wall='73.5 (72.4-78.6)', turns='21 (20-21)', tool_calls='20 (19-20)', tokens='439824 (438932-480697)', screenshots='10 (9-10)', screenshot_bytes='194745 (174122-194848)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('B', 'T4'): dict(n=3, success='3/3', wall='114.2 (109-123.2)', turns='21 (19-31)', tool_calls='20 (18-30)', tokens='521597 (485798-793454)', screenshots='16 (13-19)', screenshot_bytes='324416 (267937-377084)', retries='1 (1-1)', duplicates='0 (0-0)', failures='-'),
    ('C', 'T1'): dict(n=4, success='4/4', wall='37.5 (35.6-49.5)', turns='21 (19-22)', tool_calls='20 (18-21)', tokens='571612 (449555-626645)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('C', 'T2'): dict(n=3, success='3/3', wall='43.8 (35.8-67.3)', turns='22 (18-23)', tool_calls='21 (17-22)', tokens='556522 (480957-697542)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('C', 'T3'): dict(n=5, success='4/5', wall='71.9 (66.3-121)', turns='25 (22-60)', tool_calls='24 (21-45)', tokens='669900 (629233-2.2141e+06)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-2)', duplicates='0 (0-0)', failures='turn cap'),
    ('C', 'T4'): dict(n=5, success='4/5', wall='110.9 (95.7-160.8)', turns='32 (32-60)', tool_calls='31 (31-44)', tokens='1.04507e+06 (1.00804e+06-2.21604e+06)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='1 (1-2)', duplicates='0 (0-0)', failures='turn cap'),
    ('D', 'T1'): dict(n=3, success='3/3', wall='25.6 (24.8-26.5)', turns='9 (9-10)', tool_calls='8 (8-9)', tokens='261710 (261676-292563)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('D', 'T2'): dict(n=3, success='3/3', wall='26.7 (25-28.8)', turns='9 (9-10)', tool_calls='8 (8-9)', tokens='262914 (262141-293325)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('D', 'T3'): dict(n=3, success='3/3', wall='41.8 (37.4-43.9)', turns='11 (10-12)', tool_calls='10 (9-11)', tokens='326124 (294898-359521)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('D', 'T4'): dict(n=3, success='3/3', wall='60.6 (59.9-73.2)', turns='13 (13-15)', tool_calls='12 (12-14)', tokens='395888 (394741-460328)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='1 (1-1)', duplicates='0 (0-0)', failures='-'),
    ('E', 'T1'): dict(n=4, success='4/4', wall='4.55 (3.6-6.1)', turns='0 (0-0)', tool_calls='0 (0-0)', tokens='0 (0-0)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('E', 'T2'): dict(n=3, success='3/3', wall='4.6 (3.7-4.8)', turns='0 (0-0)', tool_calls='0 (0-0)', tokens='0 (0-0)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('E', 'T3'): dict(n=3, success='3/3', wall='16.8 (14.7-17.3)', turns='0 (0-0)', tool_calls='0 (0-0)', tokens='0 (0-0)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('E', 'T4'): dict(n=3, success='3/3', wall='28.4 (27.9-31)', turns='0 (0-0)', tool_calls='0 (0-0)', tokens='0 (0-0)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='1 (1-1)', duplicates='0 (0-0)', failures='-'),
    ('F', 'T1'): dict(n=3, success='3/3', wall='42 (37.2-43.5)', turns='9 (9-10)', tool_calls='8 (8-9)', tokens='284087 (283369-318281)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('F', 'T2'): dict(n=3, success='3/3', wall='44.3 (39.8-45)', turns='11 (9-11)', tool_calls='10 (8-10)', tokens='345897 (279201-345965)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('F', 'T3'): dict(n=3, success='3/3', wall='40.3 (36-45.6)', turns='10 (9-11)', tool_calls='9 (8-10)', tokens='283772 (278600-354913)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
    ('F', 'T4'): dict(n=3, success='3/3', wall='53.6 (52.3-61.3)', turns='10 (10-13)', tool_calls='9 (9-12)', tokens='319260 (311864-386301)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='1 (1-1)', duplicates='0 (0-0)', failures='-'),
    ('F-warm', 'T1'): dict(n=2, success='2/2', wall='25.15 (21.5-28.8)', turns='7.5 (6-9)', tool_calls='6.5 (5-8)', tokens='233398 (181824-284971)', screenshots='0 (0-0)', screenshot_bytes='0 (0-0)', retries='0 (0-0)', duplicates='0 (0-0)', failures='-'),
}

# Arms G and H: jev/summary.md. success, median wall s, Jev calls,
# Jev input tokens, Jev output tokens, escalations, retries, duplicates.
EXPECTED_G = {
    "T1": dict(success="5/5", wall=11.2, calls=105, jin=118975, jout=19925, esc=0, retries=0, dups=0),
    "T2": dict(success="5/5", wall=10.9, calls=105, jin=121600, jout=19925, esc=0, retries=0, dups=0),
    "T3": dict(success="5/5", wall=21.5, calls=115, jin=128305, jout=21735, esc=0, retries=0, dups=0),
    "T4": dict(success="5/5", wall=39.8, calls=190, jin=215820, jout=36265, esc=0, retries=5, dups=0),
}
EXPECTED_H = {
    "T1": dict(success="0/5", wall=3.1, calls=35, jin=60045, jout=3560),
    "T2": dict(success="0/5", wall=2.9, calls=28, jin=48273, jout=2899),
    "T3": dict(success="0/5", wall=24.8, calls=22, jin=35039, jout=2143),
    "T4": dict(success="0/5", wall=25.1, calls=24, jin=38853, jout=2371),
}
EXPECTED_H_TOTALS = dict(calls=109, jin=182210, dups=0)
EXPECTED_G_TOTAL_JIN = 584700

# Offline Jev evaluation: jev/eval.md.
# mode: cases, correct, accuracy %, median latency s, input tokens, output tokens
EXPECTED_EVAL = {
    "text": (27, 26, 96.3, 0.209, 15902, 2396),
    "image": (27, 24, 88.9, 0.249, 74079, 2396),
    "pick": (26, 26, 100.0, 0.211, 11173, 1702),
    "box": (12, 10, 83.3, 0.238, 30792, 432),
}
EXPECTED_EVAL_INPUT_TOTAL = 131946
# (mode, bucket) -> (cases, accuracy %)
EXPECTED_BUCKETS = {
    ("text", "0.9-1.0"): (25, 96.0),
    ("text", "0.75-0.9"): (2, 100.0),
    ("image", "0.9-1.0"): (26, 88.5),
    ("image", "0.5-0.75"): (1, 100.0),
    ("pick", "0.9-1.0"): (20, 100.0),
    ("pick", "0.75-0.9"): (5, 100.0),
    ("pick", "0.5-0.75"): (1, 100.0),
}
EXPECTED_ERRORS = {
    ("text", "session_expired-bob-login", "session_expired", "login", 0.97),
    ("image", "loading-a-create", "loading", "unknown", 0.90),
    ("image", "loading-b-create", "loading", "unknown", 0.92),
    ("image", "session_expired-bob-login", "session_expired", "login", 0.98),
}

# Excluded runs: summary.md "Excluded runs" and jev/summary.md pilot list.
EXPECTED_EXCLUDED_MATRIX = {
    "CLI did not enforce turn cap": 3,
    "CLI prompt delimiter error": 1,
    "isolated consent stub used wrong site origin": 1,
    "revocation monitor ended before form opened": 3,
    "secret exposed in Playwright MCP snapshot before site correction": 13,
    "setup smoke test": 9,
    "stream parser line limit": 4,
}
EXPECTED_EXCLUDED_G_PILOT = 14


def bucket(conf):
    if conf >= 0.9:
        return "0.9-1.0"
    if conf >= 0.75:
        return "0.75-0.9"
    return "0.5-0.75"


# ---------------------------------------------------------------- runs.csv
with open(HERE / "runs.csv", newline="") as f:
    runs = list(csv.DictReader(f))

groups = defaultdict(list)
for r in runs:
    groups[(r["arm"], r["task"])].append(r)

print("Frontier arms (A-F-warm): n, success, median wall s (range), turns, tokens")
print(f"{'arm':7} {'task':4} {'n':>2} {'ok':>5}  {'wall s':22} {'turns':14} {'tokens':32}")
for (arm, task), want in EXPECTED_MATRIX.items():
    g = groups.get((arm, task), [])
    ok = sum(int(r["success"]) for r in g)
    cols = {
        "wall": medrange([round(float(r["wall_s"]), 1) for r in g]),
        "turns": medrange([int(r["turns"]) for r in g]),
        "tool_calls": medrange([int(r["tool_calls"]) for r in g]),
        "tokens": medrange([int(r["tokens"]) for r in g]),
        "screenshots": medrange([int(r["screenshots"]) for r in g]),
        "screenshot_bytes": medrange([int(r["screenshot_bytes"]) for r in g]),
        "retries": medrange([int(r["retries"]) for r in g]),
        "duplicates": medrange([int(r["duplicates"]) for r in g]),
    }
    fails = "; ".join(sorted({r["failure_reason"] for r in g if r["failure_reason"]})) or "-"
    got = dict(n=len(g), success=f"{ok}/{len(g)}", failures=fails, **cols)
    for k, v in want.items():
        check(f"{arm} {task} {k}", got[k], v)
    print(f"{arm:7} {task:4} {got['n']:>2} {got['success']:>5}  {cols['wall']:22} {cols['turns']:14} {cols['tokens']:32}")
extra = set(groups) - set(EXPECTED_MATRIX) - {(a, t) for a in "GH" for t in ("T1", "T2", "T3", "T4")}
check("unexpected arm/task groups in runs.csv", sorted(extra), [])

# Sanity: component token columns add up to the tokens column.
for r in runs:
    parts = sum(int(r[k]) for k in ("tokens_input", "tokens_cache_read", "tokens_cache_create", "tokens_output"))
    check(f"{r['run_id']} token parts", parts, int(r["tokens"]))

print()
print("Jev arms G and H (20 pinned runs each): success, median wall s, Jev calls, Jev in/out tokens")
for arm, table in (("G", EXPECTED_G), ("H", EXPECTED_H)):
    tot_calls = tot_in = tot_dups = 0
    for task, want in table.items():
        g = groups.get((arm, task), [])
        got = dict(
            success=f"{sum(int(r['success']) for r in g)}/{len(g)}",
            wall=round(statistics.median(round(float(r["wall_s"]), 1) for r in g), 1),
            calls=sum(int(r["jev_calls"]) for r in g),
            jin=sum(int(r["jev_input_tokens"]) for r in g),
            jout=sum(int(r["jev_output_tokens"]) for r in g),
        )
        if arm == "G":
            got["esc"] = sum(int(r["escalations"]) for r in g)
            got["retries"] = sum(int(r["retries"]) for r in g)
            got["dups"] = sum(int(r["duplicates"]) for r in g)
        for k, v in want.items():
            check(f"{arm} {task} {k}", got[k], v)
        tot_calls += got["calls"]
        tot_in += got["jin"]
        tot_dups += sum(int(r["duplicates"]) for r in g)
        print(f"{arm} {task} n={len(g)} ok={got['success']} wall={got['wall']} calls={got['calls']} jev_in={got['jin']} jev_out={got['jout']}")
    check(f"{arm} run count", sum(len(groups.get((arm, t), [])) for t in table), 20)
    if arm == "G":
        check("G total Jev input tokens", tot_in, EXPECTED_G_TOTAL_JIN)
    else:
        check("H total Jev calls", tot_calls, EXPECTED_H_TOTALS["calls"])
        check("H total Jev input tokens", tot_in, EXPECTED_H_TOTALS["jin"])
        check("H duplicates", tot_dups, EXPECTED_H_TOTALS["dups"])

# ------------------------------------------------------ jev-offline-eval.csv
with open(HERE / "jev-offline-eval.csv", newline="") as f:
    cases = list(csv.DictReader(f))
by_mode = defaultdict(list)
for c in cases:
    by_mode[c["mode"]].append(c)

print()
print("Offline Jev eval: mode, cases, correct, accuracy, median latency s, input/output tokens")
total_in = 0
for mode, want in EXPECTED_EVAL.items():
    g = by_mode[mode]
    n, ok = len(g), sum(int(c["correct"]) for c in g)
    acc = round(100 * ok / n, 1)
    lat = round(statistics.median(float(c["latency_s"]) for c in g), 3)
    tin = sum(int(c["input_tokens"]) for c in g)
    tout = sum(int(c["output_tokens"]) for c in g)
    total_in += tin
    for k, got, w in zip(("cases", "correct", "accuracy", "latency", "input", "output"), (n, ok, acc, lat, tin, tout), want):
        check(f"eval {mode} {k}", got, w)
    print(f"{mode:6} {n:3} {ok:3} {acc:6.1f}% {lat:.3f} {tin:7} {tout:5}")
check("eval total input tokens", total_in, EXPECTED_EVAL_INPUT_TOTAL)

buckets = defaultdict(list)
errors = set()
for c in cases:
    if c["mode"] in ("text", "image", "pick"):
        buckets[(c["mode"], bucket(float(c["confidence"])))].append(int(c["correct"]))
        if c["correct"] == "0":
            errors.add((c["mode"], c["case_id"], c["expected"], c["got"], float(c["confidence"])))
got_b = {k: (len(v), round(100 * sum(v) / len(v), 1)) for k, v in buckets.items()}
check("eval confidence buckets", got_b, EXPECTED_BUCKETS)
check("eval errors", errors, EXPECTED_ERRORS)
print(f"errors: {len(errors)} (all with confidence >= 0.90)" if all(e[4] >= 0.9 for e in errors) else f"errors: {len(errors)}")

# ------------------------------------------------------------- excluded.csv
with open(HERE / "excluded.csv", newline="") as f:
    ex = list(csv.DictReader(f))
by_reason = defaultdict(int)
pilot = 0
for e in ex:
    if e["source"] == "benchmark-matrix":
        by_reason[e["reason"]] += int(e["count"])
    else:
        pilot += int(e["count"])
check("excluded matrix runs by reason", dict(by_reason), EXPECTED_EXCLUDED_MATRIX)
check("excluded G pilot runs", pilot, EXPECTED_EXCLUDED_G_PILOT)
print()
print(f"Excluded: {sum(by_reason.values())} matrix runs, {pilot} G pilot/validation runs")

print()
if mismatches:
    print(f"MISMATCH ({len(mismatches)}):")
    for m in mismatches:
        print("  " + m)
    sys.exit(1)
print("OK: every aggregate matches the published summaries")
