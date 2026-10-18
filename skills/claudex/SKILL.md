---
name: claudex
description: >
  En-masse parallel research via `claudex` — Claude Code routed to
  token-efficient MiMo models. Use for any breadth task (scouring a codebase,
  surveying docs, reading many files/repos) where fan-out reading would burn
  the main context or Anthropic quota: shell out headless (`claudex -p "..."`)
  and let it spawn many subagents on the cheap plan. Gather-only — claudex
  collects and reports; the main agent makes all decisions and does all
  editing. Trigger: /claudex, or proactively for broad scouring tasks.
metadata:
  compatibility: Claude Code, Codex, or OpenCode with shell access, the claudex scripts installed on PATH (bundled in scripts/), and a Xiaomi MiMo token plan or pay-as-you-go key
allowed-tools:
  - Bash
  - Read
---

# claudex — en-masse parallel research harness

`claudex` is Claude Code with the API rerouted to Xiaomi MiMo's
token plan. The default and all model tiers map to `mimo-v2.6-flash`; a run
selects `mimo-v2.6-pro` only when it explicitly requests Pro. Tokens it burns
come off the MiMo plan,
**not** the main Anthropic quota — that is the entire point.

If you use Paseo (an open-source agent runner), the wrapper can also be set up
as a provider, with a Flash profile and a Pro profile, for long research runs
you want to watch in a sidebar; use the CLI below for one-shots from inside
another agent. Treat it as a disposable search harness: cheap context, cheap
subagents, cheap re-runs.

## Setup

The wrapper and its search bridge ship in this skill's `scripts/` directory:
`scripts/claudex` and `scripts/claudex-mimo-search`. Install both side by side
on your `PATH`:

```bash
install -m 755 scripts/claudex scripts/claudex-mimo-search ~/.local/bin/
# or system-wide: sudo install -m 755 scripts/claudex scripts/claudex-mimo-search /usr/local/bin/
```

It also needs the `claude` CLI (Claude Code), `python3` for the search bridge,
and a Xiaomi MiMo account with either a token plan or a pay-as-you-go API key.
**Both cost money**: runs draw down the plan or balance, and each web search is
billed separately. See Preflight for where the keys go.

## The contract

- **Gather-only.** claudex researches and reports. It does NOT make decisions,
  weigh trade-offs, or edit files. The main agent reads its report and decides.
- **Prefer it for breadth.** Any task shaped like "read a lot, return a
  little" — mapping a codebase, surveying docs, finding every call site,
  summarizing many files — goes to claudex instead of reading in main context.
- **Keep depth here.** Single-file lookups you can answer in one Read/Grep are
  faster done directly.

## Preflight

- Token: `MIMO_API_KEY` env var, else `~/.claude/mimo_token` (a `tp-…` token
  plan key; base URL `https://token-plan-sgp.xiaomimimo.com/anthropic`; the plan key is regional, override with `CLAUDEX_PLAN_URL`). The
  wrapper errors clearly if neither exists.
- Plan exhausted? claudex can run on MiMo pay-as-you-go instead (same
  `sk-...` key as the search bridge: `MIMO_PAYGO_KEY` or
  `~/.claude/mimo_paygo_token`). Per run: `claudex --paygo -p "..."`.
  Persistent: `echo paygo > ~/.claude/claudex_backend` (write `plan` or
  delete the file to switch back when the plan renews). If no plan token
  exists at all, it falls back to PAYG automatically.
- Web search: use the MCP tool `mcp__mimo__web_search`, which the wrapper adds
  to every run (main agent and subagents). It calls MiMo's
  OpenAI-protocol `web_search` once per call and returns real URLs, titles,
  snippets, route and `web_search_usage`. Built-in `WebSearch` stays denied:
  it is an Anthropic server tool and MiMo returns only query echoes for it.
  Each call is billed (about $0.005 plus tokens), one keyword per call, capped
  at 40 per session (`CLAUDEX_SEARCH_MAX_CALLS`). Route: token plan first,
  PAYG if the plan has search disabled (`CLAUDEX_SEARCH_ROUTE=plan|paygo` to
  pin). Failures come back as tool errors with the HTTP status; treat them as
  "no search", not as "nothing found". Candidates
  can be reranked in the calling agent (for example with the `jev` skill's
  `jev_rank` / `jev_search`, if installed).
- **Both backends dead (402 Insufficient account balance on plan AND paygo)?**
  Don't retry and don't block the task — fall back to the host's native subagents
  (standing fallback policy). In Claude Code, use
  `general-purpose`/`Explore` agents with `model: "haiku"` for mechanical
  breadth or `model: "sonnet"` when gathering needs judgment. In Codex or
  OpenCode, use supported native agent types and inherit the current model
  unless the user configured a suitable research model. If delegation is
  unavailable, perform bounded research directly. Same contract applies:
  gather-only, report back, main agent decides. Start independent agents
  without waiting between launches, within the host's concurrency limit. Mention
  to the user that claudex is out of balance so they can top it up.

## Headless cookbook

**Basic one-shot** (prints the answer and exits):
```bash
claudex -p "Map every place this repo touches the Telegram API. Return file:line + one-line role for each."
```

**Read-only research run** — headless mode can't prompt for permissions, so
allowlist the read tools it needs; anything else silently fails
(`mcp__mimo__web_search` is already allowlisted by the wrapper):
```bash
claudex -p "Survey how error handling works across src/. Report patterns with file:line evidence." \
  --allowedTools "Read Glob Grep WebFetch Bash(rg:*) Bash(fd:*) Bash(ls:*) Bash(git log:*) Bash(git show:*) Bash(git diff:*)"
```
Belt-and-braces if the task tempts it to fix things:
`--disallowedTools "Edit Write NotebookEdit"`.

**GOTCHA — prompt position.** `--allowedTools` and `--disallowedTools` are
*variadic*: they greedily consume every following bare argument as a tool
rule. A prompt placed after them is eaten word-by-word ("Permission deny rule
"Scan" matches no known tool" × every word, exit 1, empty output). Always put
the prompt **immediately after `-p`**, all flags after the prompt.

**Web research** — search, then read:
```bash
claudex -p "Find the official release schedule for Python 3.15. Use mcp__mimo__web_search
(one precise query per call, at most 5 calls), then WebFetch the best 2 URLs.
Report each URL with title and the facts it supports." --allowedTools "WebFetch"
```

**Fan-out inside one claudex** — tell it explicitly to parallelize; subagent
spawning needs no permission grants:
```bash
claudex -p "Spawn one Explore subagent per top-level directory in this repo, in parallel.
Each maps its directory's purpose, key files, and external dependencies.
Synthesize into a single markdown report."
```

**Fan-out of claudex processes** — for independent research questions, launch
several in the background, each writing to the scratchpad, then read the files:
```bash
d="$(mktemp -d)"   # scratch directory for this research run
claudex -p "Research question A..." --no-session-persistence > "$d/a.md" 2>"$d/a.err" &
claudex -p "Research question B..." --no-session-persistence > "$d/b.md" 2>"$d/b.err" &
wait
```
From inside Claude Code, prefer one Bash call per claudex with
`run_in_background: true` over `&`/`wait` — you get notified as each finishes.
In Codex or OpenCode, use the host's resumable/background shell execution
and poll for completion; Claude's `run_in_background` and timeout fields
are not portable tool arguments.

**Structured output** for parsing instead of prose:
```bash
claudex -p --output-format json "..." | jq -r .result      # answer text
claudex -p --output-format json "..." | jq .total_cost_usd  # spend check
```
Or force a shape: `--json-schema '{"type":"object",...}'`.

**Pipe context in** rather than describing it:
```bash
git diff main... | claudex -p "Summarize what this change does, file by file."
```

**Model choice**: the default, `--model sonnet`/`haiku`, and built-in Explore
subagents run on `mimo-v2.6-flash`. A 2026-09-25 Explore run exposed that
Claude Code selects its Opus tier for some built-in agents, so the wrapper
routes that tier to Flash by default too. Select Pro explicitly for harder
gathering with `--model opus`/`fable`, `--model mimo-v2.6-pro`, or
`CLAUDEX_MODEL=mimo-v2.6-pro`; subagents may then use Pro. This does not change
the gather-only contract. Both models have a 1M context window, which the
wrapper declares with `CLAUDE_CODE_MAX_CONTEXT_TOKENS`. Claude Code may still
log `[claude-code:unrecognized_model]` because its catalog lacks the MiMo IDs;
the declared window prevents its 200K fallback. Override subagents separately
with `CLAUDEX_SUBAGENT_MODEL` only when needed.

**Follow-ups** reuse the previous run's context instead of re-reading:
```bash
claudex -p -c "Now list only the call sites that lack a timeout."
```
(Continues the most recent conversation in the cwd — don't combine with
`--no-session-persistence` on the first run if you'll want this.)

**Scope**: claudex sees the directory it's launched from. `cd` to the target
repo root first; add extra roots with `--add-dir /path/other-repo`.

## Prompting claudex well

Every prompt should state, in one block: the question, where to look, how to
parallelize ("spawn N subagents, one per X"), and the **output contract** —
structured markdown or JSON with `file:line` references so the main agent can
spot-verify claims cheaply without re-reading. claudex output is a lead
sheet, not ground truth: verify load-bearing claims before acting on them.
