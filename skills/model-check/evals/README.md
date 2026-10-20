# Routing evals

These cases check when `model-check` gets picked up and whether reading it leads to a model or to ordinary tests. They were written for the 2026-10-20 change that narrowed the skill. Before that, the skill and the routing line I kept in my agent instructions both fired on any change that touched a queue, retry, approval, lock, timeout or state machine.

## Cases

[`cases.json`](cases.json) has 16 coding requests. Each has an expected outcome and a one-line reason:

- 9 expect `tests`: a toast queue, an order status enum, an approve button, a backoff helper, a gunicorn timeout, a sort tiebreak, a Sidekiq retry cap, a cron lock and a search debounce. Each has a keyword the old trigger matched.
- 5 expect `model`: an unexplained duplicate chat message, a new edit-lock handoff protocol, an explicit TLA+ request, a recurring production double count, and a change to code that already has a model.
- 2 are `either` and not scored: an idempotent payment retry and a Postgres job queue.

None of the cases repeats the examples in `SKILL.md`.

## Runs

A judge model played an agent starting a session and answered in JSONL. The judges never saw the expected outcomes, and the two versions were labelled with neutral names. Prompts are in [`judge-prompt.md`](judge-prompt.md).

- **Routing.** The judge saw one routing sentence, the skill's description and three unrelated skills, decided whether to load `model-check`, and read the body only if it did. Four runs: Claude Sonnet 5.5, one per version per half of the cases.
- **Forced load.** The judge was told the skill was already loaded and read the whole body, then decided. This checks that the body alone gives a fast no-model answer. Nine of the cases, one run per version on Codex `gpt-6-sol` (a different provider from the routing judges).

Routing sentences:

- Before: "Load `model-check` before designing, changing or debugging queues, retries, approvals, locks, replay, concurrency caps, rate limits, timeouts, state machines or service protocols."
- After: "Load `model-check` for a concrete, costly ordering or concurrency failure that focused tests can't settle, a new multi-party protocol whose invariant is genuinely uncertain, code an existing formal model describes, or when I ask for a model check. Merely touching queues, retries, approvals, timeouts or state machines is not a reason."

The before skill is `SKILL.md` at commit `88b7b49`. The after skill is the one in this folder's parent. The judges read my private copy, which has the same description and decision section; it differs only in naming the projects in the pitfalls section.

## Results

| Run | Expected `tests`: loaded | Expected `tests`: modelled | Expected `model`: loaded | Expected `model`: modelled |
|---|---|---|---|---|
| Routing, before | 7 of 9 | 0 of 9 | 5 of 5 | 5 of 5 |
| Routing, after | 0 of 9 | 0 of 9 | 5 of 5 | 5 of 5 |
| Forced load, before | n/a | 0 of 6 | n/a | 1 of 1 |
| Forced load, after | n/a | 0 of 6 | n/a | 1 of 1 |

"Modelled" counts `yes` and `conditional`. With the old trigger, the agent loaded the skill for seven of the nine ordinary tasks and then talked itself out of a model each time. That cost a skill load and a decision per task, and it is the over-application the change targets. After the change none of them loaded, and all five model cases still loaded and planned the same checks: constants cited from code, counterexamples turned into real tests, replay against real runs, bounded claims and a deliberately broken config. The one exception was the existing-model case, which skipped replay and bounded claims because it was only updating a model.

Under forced load, both versions rejected the six ordinary tasks in one or two minutes. The old body also chose a model for the payment retry, a case with a standard fix that a fake-provider test can force. The new body chose tests. Both chose a model for the Postgres queue.

Recompute the table from the raw answers in [`results/`](results):

```bash
python3 score.py
```

It exits 1 if the numbers no longer match this README.

## Limits

- One judge run per version per case. That is enough to see the routing change at 7 of 9 against 0 of 9. It is not enough to estimate a rate.
- The judges role-played a session start. A real session also has the conversation, the repository and other skills competing for the same task.
- Both judge models had my current agent instructions in their own context. The prompt told them to ignore those. I can't rule out that some leaked into the before runs, and if any did, they would push the before numbers toward the after ones.
- I wrote the cases and the skill change. The judges were independent of both, but the case selection was not.
- Nothing here runs in CI except `score.py`, which only checks that this README matches the saved answers. Rerunning the judges needs model access.
