#!/usr/bin/env python3
"""Run the learn evals: get one tutor reply per case, then judge each reply.

Standard library only. Needs a logged-in `claude` or `codex` command line.

  python3 run.py tutor LABEL --skill-dir DIR --cli claude --model MODEL [--effort E]
  python3 run.py judge LABEL --model MODEL

`tutor` copies the skill at DIR into a scratch workspace under a neutral name,
asks the model for the tutor's next message in each case, runs the mechanical
checks, and writes results/LABEL.jsonl. `judge` asks a second model the yes/no
questions for each reply and adds its answers to the same file. The judge never
sees the label or the expected answers. score.py turns the files into tables.
"""
import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
SYSTEM = "You are an agent in a chat session."
DIAGNOSED = {"git.branch-pointer", "git.head", "git.fast-forward"}
CODEX_SANDBOX = None  # set by --codex-sandbox when Codex's own sandbox cannot start on the machine


def prompt_template(name):
    text = (HERE / name).read_text()
    return re.search(r"```text\n(.*?)\n```", text, re.S).group(1)


def render_transcript(turns):
    return "\n\n".join(f"[{t['role']}]\n{t['text']}" for t in turns)


def call_claude(prompt, cwd, model, effort, tools):
    cmd = ["claude", "-p", "--model", model, "--setting-sources", "", "--disable-slash-commands",
           "--strict-mcp-config", "--tools", tools, "--no-session-persistence",
           "--system-prompt", SYSTEM, "--output-format", "json"]
    if effort:
        cmd += ["--effort", effort]
    if "Write" in tools:
        cmd += ["--permission-mode", "acceptEdits"]
    out = subprocess.run(cmd + [prompt], cwd=cwd, capture_output=True, text=True,
                         stdin=subprocess.DEVNULL, timeout=900)
    data = json.loads(out.stdout)
    if data.get("is_error"):
        raise RuntimeError(str(data.get("result"))[:300])
    return data["result"].strip()


def call_codex(prompt, cwd, model, effort, tools):
    last = Path(cwd) / ".last-message.txt"
    cmd = ["codex", "exec", "-C", str(cwd), "--skip-git-repo-check", "--ephemeral", "--ignore-rules",
           "-m", model, "-s", CODEX_SANDBOX or ("workspace-write" if "Write" in tools else "read-only"),
           "-o", str(last)]
    if effort:
        cmd += ["-c", f"model_reasoning_effort={effort}"]
    out = subprocess.run(cmd + [prompt], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=900)
    if out.returncode != 0 or not last.exists():
        raise RuntimeError(out.stderr[-300:])
    text = last.read_text().strip()
    last.unlink()
    return text


CALLS = {"claude": call_claude, "codex": call_codex}


# Mechanical checks. Each returns True or False.

def _progress(ws):
    return ws / "project" / ".learning" / "git-internals" / "progress.json"


def _fixture_progress():
    return FIXTURES / "legacy-course" / ".learning" / "git-internals" / "progress.json"


def has_block_chars(reply, ws):
    return "█" in reply


def legacy_untouched(reply, ws):
    return _progress(ws).read_bytes() == _fixture_progress().read_bytes()


def progress_valid_json(reply, ws):
    try:
        json.loads(_progress(ws).read_text())
        return True
    except ValueError:
        return False


def _load_pair(ws):
    return json.loads(_fixture_progress().read_text()), json.loads(_progress(ws).read_text())


def legacy_labels_kept(reply, ws):
    old, new = _load_pair(ws)
    for cid, concept in old["concepts"].items():
        now = new.get("concepts", {}).get(cid)
        if now is None or now.get("understanding") != concept["understanding"] or now.get("name") != concept["name"]:
            return False
        if any(note not in now.get("notes", []) for note in concept.get("notes", [])):
            return False
    return True


def no_level_outside_diagnostic(reply, ws):
    _, new = _load_pair(ws)
    return all(c.get("level") is None for cid, c in new["concepts"].items() if cid not in DIAGNOSED)


def diagnosed_levels_present(reply, ws):
    _, new = _load_pair(ws)
    branch = new["concepts"]["git.branch-pointer"].get("level")
    head = new["concepts"]["git.head"].get("level")
    if not isinstance(branch, int) or isinstance(branch, bool) or not 0 <= branch <= 5:
        return False
    return head is None or (isinstance(head, int) and branch > head)


def _notes_text(progress):
    notes = progress.get("notes", "")
    if isinstance(notes, str):
        return notes
    return "\n".join(map(str, notes)) if isinstance(notes, list) else json.dumps(notes, ensure_ascii=False)


def contract_text_kept(reply, ws):
    """Every line of the original course contract is still in the course notes.
    This says nothing about what was added; the judge reads the added text."""
    old, new = _load_pair(ws)
    notes = _notes_text(new)
    return all(line in notes for line in old["notes"].split("\n"))


def added_course_text(case, ws):
    """Text the tutor added to the course notes and the curriculum, for the judge to read."""
    old, new = _load_pair(ws)
    added = _notes_text(new)
    for line in old["notes"].split("\n"):
        added = added.replace(line, "")
    before = (FIXTURES / case["workspace"] / ".learning" / "git-internals" / "curriculum.md").read_text().split("\n")
    after = (ws / "project" / ".learning" / "git-internals" / "curriculum.md").read_text().split("\n")
    extra = "\n".join(line for line in after if line not in before)
    return (added.strip() + ("\n" + extra.strip() if extra.strip() else "")).strip()


CHECKS = {f.__name__: f for f in (has_block_chars, legacy_untouched, progress_valid_json, legacy_labels_kept,
                                  no_level_outside_diagnostic, diagnosed_levels_present, contract_text_kept)}


def run_mechanical(case, reply, ws):
    out = {}
    for crit in case["criteria"]:
        if crit.get("type") != "mechanical":
            continue
        try:
            out[crit["id"]] = "yes" if CHECKS[crit["check"]](reply, ws) else "no"
        except (OSError, ValueError, KeyError, TypeError):
            out[crit["id"]] = "no"
    return out


def changed_files(case, ws):
    """Course files the tutor created or changed, kept so the checks can be inspected."""
    before = FIXTURES / case["workspace"] / ".learning"
    after = ws / "project" / ".learning"
    out = {}
    for path in sorted(p for p in after.rglob("*") if p.is_file()):
        rel = path.relative_to(after)
        original = before / rel
        text = path.read_text(errors="replace")
        if not original.exists() or original.read_text() != text:
            out[str(rel)] = text
    return out


def tutor_one(case, args, template):
    with tempfile.TemporaryDirectory(prefix="learn-eval-") as tmp:
        ws = Path(tmp)
        shutil.copytree(args.skill_dir, ws / "skill" / "learn", ignore=shutil.ignore_patterns("evals"))
        (ws / "project").mkdir()
        if case.get("workspace"):
            shutil.copytree(FIXTURES / case["workspace"] / ".learning", ws / "project" / ".learning")
        prompt = (template.replace("{skill_dir}", "skill/learn").replace("{context}", case["context"])
                  .replace("{transcript}", render_transcript(case["transcript"])))
        reply = CALLS[args.cli](prompt, ws, args.model, args.effort, case.get("tools", "Read"))
        row = {"case": case["id"], "reply": reply, "mechanical": run_mechanical(case, reply, ws), "verdicts": {}}
        if case.get("workspace"):
            row["files"] = changed_files(case, ws)
            try:
                row["added_course_text"] = added_course_text(case, ws)
            except (OSError, ValueError, KeyError, TypeError):
                row["added_course_text"] = ""
        return row


def judge_one(case, row, args, template):
    judged = [c for c in case["criteria"] if c.get("type") != "mechanical"]
    questions = "\n".join(f"{c['id']}. {c['q']}" for c in judged)
    extra = ""
    if any(c.get("about") == "added_course_text" for c in judged):
        extra = ("\nIn the same turn the tutor added this text to the course's notes file. Some questions are about it:\n\n"
                 "<added>\n" + (row.get("added_course_text") or "(nothing was added)") + "\n</added>\n")
    prompt = (template.replace("{context}", case["context"]).replace("{transcript}", render_transcript(case["transcript"]))
              .replace("{reply}", row["reply"]).replace("{extra}", extra).replace("{questions}", questions))
    with tempfile.TemporaryDirectory(prefix="learn-judge-") as tmp:
        text = CALLS[args.cli](prompt, tmp, args.model, args.effort, "")
    data = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
    if set(data) != {c["id"] for c in judged} and len(data) == len(judged):
        # The judge sometimes relabels ids as a, b, c. Its answers are in question order.
        data = dict(zip((c["id"] for c in judged), data.values()))
    row["verdicts"] = {c["id"]: {"answer": str(data[c["id"]]["answer"]).lower(), "quote": data[c["id"]].get("quote", "")}
                       for c in judged}
    return row


def with_retry(fn, *a):
    try:
        return fn(*a)
    except Exception as first:  # one retry for a transient CLI failure
        print(f"retry after: {first}")
        return fn(*a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["tutor", "judge"])
    ap.add_argument("label")
    ap.add_argument("--skill-dir", type=Path)
    ap.add_argument("--cli", choices=sorted(CALLS), default="claude")
    ap.add_argument("--model", required=True)
    ap.add_argument("--effort")
    ap.add_argument("--cases", help="comma-separated case ids; default all")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--codex-sandbox", help="override the Codex sandbox mode, for example danger-full-access")
    args = ap.parse_args()
    global CODEX_SANDBOX
    CODEX_SANDBOX = args.codex_sandbox

    cases = json.loads((HERE / "cases.json").read_text())
    wanted = set(args.cases.split(",")) if args.cases else {c["id"] for c in cases}
    path = HERE / "results" / f"{args.label}.jsonl"
    rows = {}
    if path.exists():
        rows = {r["case"]: r for r in map(json.loads, path.read_text().splitlines()) if r}

    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        if args.stage == "tutor":
            template = prompt_template("tutor-prompt.md")
            jobs = {c["id"]: pool.submit(with_retry, tutor_one, c, args, template) for c in cases if c["id"] in wanted}
        else:
            template = prompt_template("judge-prompt.md")
            jobs = {c["id"]: pool.submit(with_retry, judge_one, c, rows[c["id"]], args, template)
                    for c in cases if c["id"] in wanted and c["id"] in rows}
        for cid, job in jobs.items():
            rows[cid] = job.result()
            print(f"{args.stage} {args.label} {cid} done")

    order = [c["id"] for c in cases]
    path.write_text("".join(json.dumps(rows[cid], ensure_ascii=False) + "\n" for cid in order if cid in rows))


if __name__ == "__main__":
    main()
