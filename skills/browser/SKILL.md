---
name: browser
description: Use before driving a web page from an agent, for a task or for testing. Repeats known flows as saved Playwright scripts, can use Jev for an uncertain element choice inside a script, and explores or escalates with agent-browser. Keeps throwaway Chromium profiles for no-login testing.
license: MIT
compatibility: Python Playwright for saved flows; agent-browser (npm package agent-browser) for exploration; a local Chromium. The optional Jev step needs your own runner and a TypeSafe API key.
---

# browser

Load `access` first when a task involves login, consent, MFA, CAPTCHA, or an account. Its API-first order decides whether a browser is needed.

Use three tools, cheapest first:

1. **A saved script** for a known flow. It runs without a model.
2. **A Jev step** inside that script, only when one element choice is uncertain or a step broke because the page changed. Code still checks the outcome.
3. **agent-browser** to explore a new flow, or when a script or Jev step gives up.

## Save known flows

Once a flow works, save it as a Python [Playwright](https://playwright.dev/python/) script and run it without a model next time. A saved flow:

- takes its inputs as arguments, not edits to the file;
- gets credentials through the `access` fill pattern and never prints them;
- ends with an outcome check in code (`expect(page.get_by_text("App created")).to_be_visible()`) and exits non-zero when it fails;
- hands MFA, CAPTCHA and consent steps to the user, as `access` describes.

## Jev for uncertain steps (optional)

[Jev](https://docs.typesafe.ai/introduction.md) is TypeSafe's model for fast, structured decisions. Here a script asks it one closed question: which listed accessibility control performs this intent, or none. Act only on a confident answer, re-check that the control has not moved, then let code verify the outcome. Anything else goes to agent-browser. Never send secrets, codes or private values to Jev.

This repo does not ship a Jev step runner. Read [references/jev-steps.md](references/jev-steps.md) before building one; it covers the design, thresholds, prerequisites, and why an autonomous Jev browser agent is a different thing.

## Explore and escalate with agent-browser

[agent-browser](https://github.com/vercel-labs/agent-browser) is a browser CLI built for agents. Install it with `npm install -g agent-browser`, then `agent-browser install` to download Chrome for Testing.

```sh
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e3
```

Use the accessibility tree and role or label locators. Use screenshots only when the tree cannot answer the question. Keep any debugging endpoint inside scripts; never print one that carries a token. When exploration succeeds, save the steps as a script. When a saved flow breaks, use agent-browser to find what changed, then fix the script.

## Never

- Touch a browser, profile, cookies, storage, process or debugging port that you did not start for this task.
- Expose a debugging endpoint or its token.
- Solve CAPTCHAs, bypass MFA, or use stealth or anti-detection tools.
- Use Playwright MCP on pages that receive secrets. Its accessibility snapshots have carried password values into model context ([microsoft/playwright-mcp#1566](https://github.com/microsoft/playwright-mcp/issues/1566)).

## Testing

For no-login tests, a local throwaway Chromium is fine. Keep its profile in your own scratch directory, bind its debugging port to `127.0.0.1`, use a free port, and stop only the process you started. Keep Chromium's sandbox enabled. Run saved Playwright flows without a model and check the outcome in code. Use agent-browser for exploration.

## Evidence

The October 2026 comparison behind these choices, on a synthetic site, is in [benchmarks/README.md](benchmarks/README.md): data, method and limits. Read it only when you need to justify or revisit a choice.
