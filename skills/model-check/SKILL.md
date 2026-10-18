---
name: model-check
description: >
  Catch ordering and concurrency bugs by writing a small TLA+ model of the real
  code, checking it with TLC, and replaying it against real executions before
  trusting it. Use when a change touches queues, retries, approvals, locks or
  leases, replay or reconnect, concurrency caps, rate limits, timeouts or
  expiry, state machines, or a protocol between processes or services; when a
  stress run or production shows a rare ordering failure; or when asked for a
  TLA+, formal or model-checked design.
license: MIT
---

# model-check

A model checker explores every interleaving of a small, finite version of the
system and reports the shortest path to a broken property. Agents write TLA+
quickly; the expensive failures come from what goes into the model. A model
that checks clean but is wrong about the code or the upstream service is worse
than no model, because it reads as proof.

So replay every model against real executions before trusting it. If it
rejects some real runs, rewrite the model until it accepts them all, and treat
its results as provisional until then. Boris Cherny's
[post](https://x.com/bcherny/status/2102543349102338309) on using Lean and
TLA+ with Claude to find bugs in the Claude Agent SDK is a good example of the
approach.

Skip it for pure functions (use tests or property-based tests), UI layout, and
code with no interleaving, retry or time bound.

## Workflow

1. **One question per model.** Name the state machine and the failure you are
   looking for ("a slot leaks on the failure path", "an approval counts as
   taken before the service acts on it"). Model only what can change that
   answer.

2. **Read every input from the code, not from memory.** Each constant (caps,
   queue bounds, timeouts, expiry, debounce and render intervals, batch sizes,
   retry counts, rate limits) and each transition cites `file:line` or a
   vendor doc. Anything uncited goes in an assumptions table marked
   unsupported. What an upstream service does, and when, is an assumption
   until a contract test or a real log shows it. Keep a table mapping each
   model action to the function that implements it.

3. **Write the smallest model that can show the bug.** An action boundary is
   wherever the real code can be interleaved: an `await`, a lock release, a
   network call, a transaction commit. Everything between two boundaries is
   one atomic action, exactly as in the code; a model that is more atomic than
   the code hides races. Shrink the constants but keep the orderings that
   decide behavior (cap > 1 so slots are shared, global bound below the sum of
   tenant bounds), and write the scaling down in a table.

4. **State the properties.** Invariants for safety (no double start, counters
   equal reality, within caps, card says what happened). A few temporal
   properties for liveness (every queued item resolves, every slot returns),
   with the fairness each one relies on written next to it. Check liveness
   with the timeout safeguard off, or it hides stranding.

5. **Add deliberately broken configs.** For every fix or design choice, keep a
   config of the pre-fix code or the rejected design that must produce a
   counterexample, and a witness config for each "only reachable when" claim.
   A clean result means something only next to an unsafe one that shows the
   model can see the bug.

6. **Run it in CI.** A registry (`formal/expected.tsv` style) pins each
   config's expected verdict (`clean`, `violates:<Name>`) and its
   distinct-state count. Run TLC with one worker so counts are reproducible.
   Fail on a parse or semantic error, an unexpected deadlock, a changed count,
   or 0 states. Guard each run with a timeout and a metadir size cap. Trigger
   the job on changes to the model and to the code files it describes.

7. **Replay before trusting.** Confront the model with reality, cheapest first:
   - Each counterexample becomes a test against the real code that fails
     before the fix and passes after. If it will not reproduce, the model or
     the fake is wrong; find out which.
   - Contract tests against the upstream service (staging) for every
     behavior the model assumes from it, and the same scenarios against the
     project's fake; a difference is a bug in the fake and probably the model.
   - Trace validation: map real event histories or structured logs (staging,
     stress runs, production) to model steps and check the model accepts every
     one. Rewrite the model until it does. Log the events the model needs
     (queued, visible, consumed, expired, closed), not just what is convenient.
   Report results as provisional until a replay step has passed.

8. **Keep the model next to the code**, e.g. `formal/<area>/` with the spec,
   the configs and a README: purpose, action-to-code table, constants and
   scaling, properties, results table, counterexamples in plain words,
   assumptions with sources, and what is not modelled. Update it in the same
   PR as the code it describes.

## Pitfalls seen in practice (October 2026)

- **Constant from memory.** A chat bot's webhook model assumed one
  card edit per turn per render window: 200 active turns meant 200 requests
  per window against a global allowance of 100. The card editor already
  debounced edits (10 s Discord, 5 s Slack), so the real rate was about 20
  edits/s, not 100. A whole adaptive-rate
  change was built on the false alarm before a human read the code; it was
  closed. Reading the debounce from the editor would have caught it.
- **Visible is not acted on.** An approvals model treated a
  confirmation in the session history as taken. The service lists it as soon
  as it is queued and consumes a batch one per pause. In stress run 4, six
  expired cards plus a stream close made the driver count six queued denies
  as taken and read the next pause as a re-ask: 1 of 57 approval turns failed.
  The fix added a separate driver-belief variable to the model, and the old
  rule now has its own failing config.
- **Trace validation cannot catch over-approximation.** Real traces pass a
  model that allows too much; the webhook model would have accepted them all.
  Counterexample replay and constant citations catch that case; trace
  validation catches a model that allows too little.
- **Correcting the model to fit the code can copy the code's bug.** Acceptance
  of real runs shows fit, not correctness; the properties and the broken
  configs carry the correctness claim.
- **Vacuous models pass.** An empty `Init` or over-constrained `Next` reports
  "No error has been found". Pin state counts and keep witnesses.
- **State explosion fills disks.** One local TLC run wrote 16 GB of metadir.
  Cap it and delete it per run.
- **Textbook drift.** LLM-written specs tend to model the paper or the
  developer's belief (SysMoBench: asked for a spec of etcd's Raft, Claude
  wrote the Raft paper's; [SIGOPS post](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/),
  [paper](https://arxiv.org/abs/2509.23130)). Citing `file:line` per transition is the countermeasure.
- **Bounded assumptions stay labelled.** "The service consumes or drops queued
  confirmations within two quiet cycles" came from observed logs, not a
  guarantee; say so wherever the clean result is reported.

## Reporting

Write for someone who will not read TLA+. Lead with what can go wrong for a
user, then the evidence.

- Verdicts in a table: config, verdict, states, what it shows.
- Each counterexample as a short numbered story in domain words: "A slot frees
  and the dispatcher starts the third turn but has not popped it yet. That
  turn ends before the pop, its release dispatches again, and the same turn
  starts twice."
- One line on scope: "checked within these bounds, not proved for the
  production numbers", the assumptions that are unsupported, and the replay
  status (counterexample tests, contract tests, traces accepted N of M).
- For an incident: the user-visible symptom with a count, the cause in one
  sentence, then the fix. "1 of 57 approval turns failed: six expired cards
  and a stream close made the driver count queued denies as taken, then read
  the next pause as a re-ask."

## Tools

TLA+ with TLC is the default (`tla2tools.jar` pinned to a release, Java 17+).
Quint is TLA+ with a typed syntax and a test-driver story; P suits
message-passing services and log monitors; Apalache handles larger integer
domains symbolically; Lean proves unbounded properties but costs more. The
model-to-reality gap, not the bound, is what failed in the cases above, so
pick the tool you can replay against.
