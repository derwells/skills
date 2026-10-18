---
name: jev
description: >
  Jev, TypeSafe's System One model, as a filter and judge for coding agents,
  through the sieve MCP server. `jev_ask` runs any question you write over any
  list of items you hold; jev_grep, jev_rank, jev_search, jev_verify and
  jev_route are shortcuts for recurring shapes. Load before spawning an Explore
  or research subagent, before grepping a large repo or the web, or whenever you
  are about to eyeball a long list (failures, comments, hits, options) to pick
  the ones that matter.
---

# jev — write the question, enumerate the answer space, call it

Setup: these tools come from the sieve MCP server. Clone
https://github.com/derwells/sieve, follow its README (Install, then register
`bin/sieve-mcp` with your harness), and provide a TypeSafe API key
(`TYPESAFE_API_KEY`). Jev is a paid API.

Jev returns probabilities over a closed set of answers. It never generates text,
never reads deeply, never summarises. It is a fast, cheap classifier you can
point at hundreds of items at once. You still read the survivors and do the
synthesis.

## `jev_ask` — the general tool

```
jev_ask(question, items, kind="judge"|"choose"|"score", ...)
```

Three steps, every time:

1. **Write the question.** One sentence about *one item*, referring to it as
   "the item". Shared context — the traceback, the spec, the goal — goes in the
   question, not repeated into every item.
2. **Enumerate the answer space.** This is the whole design decision. If you can
   write the possible answers down before asking, Jev fits.
   - `kind="judge"` → `yes` and `no` criteria. Returns a probability per item.
     Takes `top_k` and `threshold`.
   - `kind="choose"` → `options` as `{label: when this label applies}`. Returns
     the pick plus the full distribution. Add your own `none` label when no
     listed one may fit.
   - `kind="score"` → `levels`, an ordered list of rung descriptions, lowest
     first. Returns the level, its label, the expected score, and the
     distribution.
3. **Pass the items.** Plain strings, or `{id, text}` when you want the ids back.
   Each is cut to `max_chars` (4000 by default), 40 per request, run
   concurrently, cached, budgeted, validated.

Criteria are read literally. Make them concrete and mutually exclusive — vague
criteria give probabilities near 0.5 across the board, which tells you nothing.

Worked shapes:

```
jev_ask(
  question="Does this failure share a root cause with the traceback quoted here: <traceback>?",
  items=[{"id": t.name, "text": t.output} for t in failures],
  kind="judge",
  yes="The failure is the same defect surfacing in a different test.",
  no="The failure has an unrelated cause, even if it is in the same file.",
  threshold=0.6)

jev_ask(
  question="What does this review comment need from me?",
  items=comments, kind="choose",
  options={"code": "a change to the implementation",
           "reply": "an answer or clarification, no code change",
           "ignore": "praise, a nit already handled, or an off-topic remark"})

jev_ask(
  question="How much does this log line tell me about where the failure started?",
  items=log_lines, kind="score",
  levels=["a consequence of an earlier failure",
          "routine output unrelated to the failure",
          "the first symptom: the earliest line that shows something going wrong"])
```

Outside MCP, `bin/sieve-ask judge|choose|score` in a checkout of sieve
(https://github.com/derwells/sieve) takes the same arguments as flags
(`--yes/--no`, repeated `--option LABEL=DESC`, repeated `--level DESC`), items
as JSON on stdin or `--items FILE`, and sources the API key itself. From Python,
with that checkout installed: `from sieve.ask import ask, judge, choose, score`.

## Shortcuts over the same core

Use these when the shape is exactly theirs; they save you writing the criteria
or enumerating the candidates.

- **`jev_grep(question, path, mode, top_k)`** — enumerates a repo's files (then
  functions inside the strongest ones) and ranks them. Replaces a repo-wide grep
  or an Explore subagent's first pass. ~$0.05 and ~6s per 1000-file repo.
- **`jev_rank(question, candidates[])`** — relevance probability per candidate,
  criteria already written. `jev_ask` with your own criteria beats it whenever
  "relevant" is not quite what you mean.
- **`jev_search(query, top_k)`** — web search, deduped and reranked. Open only
  the hits above threshold.
- **`jev_verify(records|report)`** — cited claims against fetched source passages.
- **`jev_route(ask, routes)`** — one destination per request, with a `none`.
- **`jev_triage_threads` / `jev_triage_paseo`** — requests for human input across
  agent threads. `jev_triage_paseo` is optional and Paseo-specific (it reads
  threads from the open-source Paseo agent runner).

## When Jev fits at all

The test is whether the answer space can be written down in advance.

Good fits: filtering many candidates down to the few worth reading; ranking;
labelling into named buckets; triage; per-pair verification; gating a subagent so
the expensive model reads less; applying one criterion consistently across
hundreds of items where a person would skim and drift.

Poor fits:

- Anything needing generated text — summaries, explanations, rewrites, extracted
  fields, code.
- Multi-step reasoning about one thing. Jev judges each item in isolation.
- Very short lists. Five items you can read in ten seconds need no filter.
- Items that only make sense with a lot of surrounding context. The judgment has
  to be makeable from the item's few thousand characters plus the question.
- Open-ended discovery ("what's interesting here?"). If you cannot state what
  "yes" looks like, read first.

Rule of thumb: Jev decides *which*; you or a bigger model decide *what* and *why*.

## Rules

- Probabilities are filters, not truth. Below 0.5 means "unlikely to matter", not
  "excluded".
- Do not chain Jev calls without opening real content in between.
- Do not send secrets. Item text goes to the TypeSafe API.
- Cost is small (about $0.04 per million input tokens). Identical
  (question, item, criteria) triples are cached, so re-asking is free.
