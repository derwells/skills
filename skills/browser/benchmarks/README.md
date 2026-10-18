# Browser access benchmark evidence

Data dated 2026-10-17. Exported from the author's private research notes on 2026-10-18. Raw transcripts, screenshots and run logs are not published. This directory holds per-run numbers, the exclusion counts, an offline Jev evaluation, and a script that recomputes the published aggregates from them.

The test site is synthetic: a made-up developer portal with fake users, a fake client secret and a fake TOTP code. Nothing here touches a real service or account.

## What was compared

Every arm does the same job on the same synthetic portal. Frontier arms use Claude Sonnet 5.5 (`claude-sonnet-5-5`, medium effort) in Claude Code.

| Arm | Approach |
| --- | --- |
| A | Pixel clicks: screenshots and coordinate clicks only |
| B | Current practice: Python Playwright over CDP with a screenshot per step |
| C | Playwright MCP, accessibility snapshot mode |
| D | agent-browser CLI |
| E | Saved deterministic Playwright script (agent-browser as fallback) |
| F | Official documented API with OAuth device grant, human approves consent |
| F-warm | Same as F with a refresh token already saved |
| G | Custom Jev per-step runner. A hand-written intent list drives the steps; Jev answers page state, target, step done and needs-human questions after each observation. No frontier model calls in the measured runs. |
| H | Upstream `jev-ultrafast` unchanged, pinned at commit `1231850a0bf1a0c0341fe408ef1668dbbfdfac46` (MIT): https://github.com/browser-use/jev-ultrafast/tree/1231850a0bf1a0c0341fe408ef1668dbbfdfac46 . A thin adapter attaches it to the test browser. |

Tasks, all on the same portal:

- T1 forms: log in as one user, create an app with two scopes, accept the consent screen (inside an iframe), pick the `eu-west` region, store the client secret, report the client ID. The scope checkboxes sit in shadow DOM.
- T2 layout: same as T1 on an alternate page layout.
- T3 MFA: same as T1 as a second user whose login needs a TOTP code obtained through a handoff.
- T4 revoked session: same as T3, and the harness revokes the session once the app form opens. The agent must sign in again and finish without creating a duplicate app.

Success is checked against the site's own ground truth: exactly one app with the expected user, scopes, consent and region, a matching stored-secret receipt and the reported client ID. T4 also requires a recorded revocation.

## Results

Cells are successes/runs and median wall seconds. n is the number of counted runs per cell. Medians and ranges for all metrics are in `runs.csv`; `reproduce.py` prints them.

| Arm | T1 | T2 | T3 | T4 | T1 turns | T1 tokens |
| --- | --- | --- | --- | --- | --- | --- |
| A pixel clicks | 3/3, 43.7 | 3/3, 40.4 | 3/3, 57.8 | 0/3, 73.9 (turn cap) | 45 | 621,990 |
| B current practice | 3/3, 65.7 | 3/3, 55.8 | 3/3, 73.5 | 3/3, 114.2 | 18 | 419,775 |
| C Playwright MCP | 4/4, 37.5 | 3/3, 43.8 | 4/5, 71.9 | 4/5, 110.9 | 21 | 571,612 |
| D agent-browser | 3/3, 25.6 | 3/3, 26.7 | 3/3, 41.8 | 3/3, 60.6 | 9 | 261,710 |
| E saved script | 4/4, 4.55 | 3/3, 4.6 | 3/3, 16.8 | 3/3, 28.4 | 0 | 0 |
| F API + device consent | 3/3, 42.0 | 3/3, 44.3 | 3/3, 40.3 | 3/3, 53.6 | 9 | 284,087 |
| F-warm | 2/2, 25.15 | not run | not run | not run | 7.5 | 233,398 |
| G Jev per step | 5/5, 11.2 | 5/5, 10.9 | 5/5, 21.5 | 5/5, 39.8 | 0 | 0 (frontier) |
| H jev-ultrafast | 0/5, 3.1 | 0/5, 2.9 | 0/5, 24.8 | 0/5, 25.1 | 0 | 0 (frontier) |

The C failures were turn-cap hits (60 turns). A in T4 hit the turn cap in all three runs. Jev calls and tokens for G and H, summed over each task's five runs:

| Arm | Task | Jev calls | Jev input tokens | Jev output tokens |
| --- | --- | ---: | ---: | ---: |
| G | T1 | 105 | 118,975 | 19,925 |
| G | T2 | 105 | 121,600 | 19,925 |
| G | T3 | 115 | 128,305 | 21,735 |
| G | T4 | 190 | 215,820 | 36,265 |
| H | T1 | 35 | 60,045 | 3,560 |
| H | T2 | 28 | 48,273 | 2,899 |
| H | T3 | 22 | 35,039 | 2,143 |
| H | T4 | 24 | 38,853 | 2,371 |

G had zero escalations to a frontier model in its pinned batch. Its only retries were one per T4 run (5 in total). Neither G nor H created a duplicate app.

Every aggregate above was recomputed from `runs.csv` and matches the original summaries. No mismatches.

## Files

- `runs.csv`: one row per counted run (120 rows). Arms A to F-warm: valid runs that the original summary counts. Arms G and H: exactly the 20 run IDs each that were pinned as the measured batches.
- `excluded.csv`: counts of excluded runs by reason. No payloads.
- `jev-offline-eval.csv`: per-case results of the offline Jev evaluation (92 rows).
- `reproduce.py`: recomputes the tables from the two CSVs and compares them with values copied from the original summaries.

## Metric definitions

- `wall_s`: seconds from run start to end. The summary rounds to 0.1 s before taking the median, and `reproduce.py` does the same.
- `turns`, `tool_calls`: Claude Code turns and tool calls. Zero for E, G and H.
- `tokens`: frontier tokens, the sum of the four recorded fields: input, cache read, cache create and output. The component columns `tokens_input`, `tokens_cache_read`, `tokens_cache_create` and `tokens_output` are included so you can recompute another definition. Note: the original write-up described the figure as input + cache read + output. The summary code also adds cache create (about 6 percent of the total in arm A, T1). The published numbers use the four-field sum, and so does this package.
- `jev_input_tokens`, `jev_output_tokens`: tokens billed by the Jev API. Jev input tokens and frontier tokens are different units from different models. Do not compare or add them.
- `screenshots`, `screenshot_bytes`: screenshots returned to the model, and their size.
- `retries`, `duplicates`: harness-counted retries after a revoked session, and apps created more than once. `jev_calls` is the number of Jev requests. `escalations` is Jev-to-frontier handoffs; recorded for G only.
- `cohort`: which batch the run belongs to (below). Blank where the source does not say.
- `failure_reason`: a category only: `turn cap`, or `agent blocked; ground truth incomplete` (H).

Cohort values:

- `initial-matrix`: first matrix of A, B, D, E cells, run with the earlier result-page control.
- `corrected-result-page`: arm C, and the reruns of A and B on T4. The result control was changed to keep the synthetic secret out of Playwright MCP snapshots, and these cells were rerun on the corrected page.
- `amendment-1`: arms F and F-warm, added later by an amendment. The source does not say which result-page control they used.
- `g-pinned-batch`, `h-pinned-batch`: the pinned 20 runs of G and H.
- blank: one extra E T1 run (replicate number 100) whose cohort the source does not state.

Columns not published: human taps and typed characters (all zero, because the MFA responder was a stub), notes, version blobs, paths, prompts and transcripts.

## Tested versions

| Component | Version |
| --- | --- |
| Node Playwright | 1.64.1 |
| Python Playwright (arm B, arms G and H runner) | 1.64.0 (1.64.1 was unavailable on PyPI) |
| @playwright/mcp | 0.0.83 |
| agent-browser | 0.39.1 |
| Chromium | 155.0.8059.79 (snap) |
| Claude Code CLI | 2.1.302 |
| Frontier model | claude-sonnet-5-5, medium effort |
| Jev (response model, requested `jev-preview`) | jev-1.14.0 |
| jev-ultrafast (arm H) | commit 1231850a0bf1a0c0341fe408ef1668dbbfdfac46 |

Claude Code 2.1.302 had no `--max-turns` option. Corrected runs enforce a 60-turn cap from stream events. Playwright MCP ran in its default accessibility snapshot mode over a CDP endpoint.

## Limitations

- Synthetic site only. Compatibility with any real service is not shown.
- These are development cohorts, not a frozen evaluation. The site's result-page masking changed between arms (see cohorts), and G's measured batch predates later runner changes.
- n is 3 to 5 per cell (2 for F-warm). That shows feasibility, not unattended reliability. A 5/5 is not a measured failure rate.
- G ran from an intent list written once by hand after reading the site. The frontier arms planned their own steps. G's speed includes that advantage. A frontier model would have to write the list once per new flow.
- MFA used a fixed 10 s synthetic responder and a stub broker, not a person. There are no human-time metrics, and T3 and T4 timings include the 10 s delay.
- H failed because of snapshot coverage gaps, per the exported `jev-ultrafast` snapshot probe: its action list had no scope checkboxes (open shadow root), listed only `New app` on the consent page (the checkbox and Continue button are in an iframe), and at the OTP step it chose `New app` instead of Verify. All five T1 runs and four of five T2 runs ended in scope errors; one T2 run stopped at login; all ten T3 and T4 runs stopped at OTP, so T4 never tested revocation. These are outside the upstream project's own stated scope and say little about it on other sites. It has no human handoff.
- The F arm is slow because each Claude Code turn carries a large context. It would pay off most when a script, not an agent, calls the API.
- Excluded secret-bearing runs: 13 Playwright MCP (arm C) runs were excluded because the accessibility snapshot carried the synthetic client secret into model context. The site was then changed to mask the secret and C was rerun. This matches public issue microsoft/playwright-mcp#1566. Only the count and reason are published; no snapshot or secret value is included.
- Other exclusions are setup and harness problems (smoke tests, a CLI that did not enforce the turn cap, a stream parser line limit, and similar). See `excluded.csv`. The 14 G pilot and validation exclusions are counts from the Jev notes; their run records are not in `runs.csv`.

## Offline Jev evaluation

Captured from the synthetic site on 2026-10-17. Labels come from the known page route and visible target. 27 page-state cases from masked page text (`text`), the same 27 from screenshots (`image`), 26 element-pick cases (`pick`), and 12 Box region cases (`box`). Box rows have no `expected`/`got`; `correct` is whether the returned region hit the target and `box_present` is the paired presence probability.

| Mode | Cases | Correct | Accuracy | Median latency s | Input tokens | Output tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| text | 27 | 26 | 96.3% | 0.209 | 15,902 | 2,396 |
| image | 27 | 24 | 88.9% | 0.249 | 74,079 | 2,396 |
| pick | 26 | 26 | 100.0% | 0.211 | 11,173 | 1,702 |
| box | 12 | 10 | 83.3% | 0.238 | 30,792 | 432 |

All four errors in the text and image modes had confidence of 0.90 or higher: an expired-session page read as `login` (0.97 text, 0.98 image), and two `loading` pages read as `unknown` in the image mode (0.90, 0.92). High confidence did not mean correct, so code should verify outcomes instead of trusting confidence alone.

Caveats: this is a small prototype evaluation on one synthetic site, not production calibration. The 0.55 act threshold was chosen before these results. Image and Box inputs go through TypeSafe's danger-zone header; TypeSafe labels them "dreamer-ready, not production" (https://docs.typesafe.ai/images.md). Box returns a region even when the target is absent, so it needs the paired presence check.

## Reproduce the tables

```sh
python3 skills/browser/benchmarks/reproduce.py
```

It needs only the Python standard library, reads `runs.csv`, `jev-offline-eval.csv` and `excluded.csv`, prints the per-arm and per-task table, the G and H Jev sums and the offline eval table, and exits non-zero if any value differs from the numbers copied from the original summaries. It does not rerun any benchmark.
