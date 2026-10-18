# Jev steps in browser scripts

Read this before adding Jev to a saved flow. The data behind it is in [../benchmarks/README.md](../benchmarks/README.md).

## Where Jev fits

A saved script is the default for a known flow: it is fast, needs no model, and checks its own outcome. Most steps should use plain Playwright locators. Jev helps with one narrow problem: a step where the script cannot be sure which control to use, usually because the page changed a label or layout. In this integration Jev answers one closed question in a fraction of a second: which candidate control performs the intent. The saved script keeps control of the workflow and of the outcome check. Jev can make other kinds of decisions too, and arm H below lets it choose operations from a goal; this step deliberately uses it for one choice.

The pieces do different jobs. Playwright and agent-browser observe the page and act on it; Jev supplies a fast decision over compact state; a frontier agent supplies judgment when neither code nor Jev is sure. When Jev is unsure, the step stops and the agent takes over with agent-browser. That is the intended path, not a failure of the design.

## One step, as I run it

My private runtime exposes this as `ctx.step(intent, expect=...)` inside saved flows. It is not published here, so treat the following as a design to copy.

1. **Candidates.** List visible interactive controls from the page's accessibility tree (role, accessible name, nearby form labels), up to about 60. Include iframes and open shadow roots if the page uses them.
2. **Refuse secrets before asking.** If the intent or any candidate text looks like a password, token, one-time code, API key, email address, URL or long opaque string, do not call Jev; hand the step to the agent.
3. **Ask one Choice question.** State: the intent (200 characters or fewer). Options: one per candidate ("button named Continue in a form with labels Region, Scopes"), plus `none`: "No listed control can perform the requested action." See TypeSafe's [Choice](https://docs.typesafe.ai/primitives/choice.md) and [confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing.md) docs.
4. **Act only on a clear answer.** My thresholds: the chosen probability is at least 0.60, and it beats `none` by at least 0.20. Otherwise escalate.
5. **Re-check, then act.** Before clicking, confirm the chosen element is still connected and visible, with the same role, name, tag and position (within a few pixels). If it changed, escalate.
6. **Check the outcome in code.** A step without an expected outcome is refused. After the click, wait for the expected text, URL or locator. If it does not appear, escalate.

Needs: Python Playwright, a Chrome DevTools Protocol session on the page (to resolve and click the exact accessibility node), and a TypeSafe API key. Jev is a paid API; at October 2026 list prices one call costs a small fraction of a cent.

## What the benchmark tested, and what it didn't

The comparison did not test this exact one-question step.

- **Arm G** was a heavier custom runner: a hand-written intent list for the whole flow, four questions per observation (page state, target, step done, needs human), thresholds 0.45 and 0.55, and a Claude escalation path. It completed 20 of 20 synthetic runs at 11 to 40 s median per task, with no escalations in the measured batch. The intent list was written by hand after reading the site, which a frontier model would otherwise have to do once per flow.
- **Arm H** ran [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) (MIT) pinned and unchanged, as an autonomous agent that chooses its own next operation. It completed 0 of 20. Its page snapshot did not list controls inside a shadow root or the consent iframe, and at the OTP step it reloaded the page instead of clicking Verify. That is a coverage and policy result for that project at that commit, not a verdict on Jev's choices.
- **The offline evaluation** asked Jev to pick the right control from labelled page captures: 26 of 26 correct. Page-state classification was 26 of 27 from text. This shows the choice works on that synthetic site. It is not production calibration.

The step above keeps G's useful parts (closed choice, confidence gate, code-checked outcome, escalation) and drops the parts a saved script already handles: planning the flow and deciding when it is done.
