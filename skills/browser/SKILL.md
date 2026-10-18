---
name: browser
description: Use before driving a web page from an agent, for a task or for testing. Explores with agent-browser, repeats known flows as saved Playwright scripts, and keeps throwaway Chromium profiles for no-login testing.
license: MIT
compatibility: agent-browser (npm package agent-browser) for exploration; Python Playwright for saved flows; a local Chromium.
---

# browser

Load `access` first when a task involves login, consent, MFA, CAPTCHA, or an account. Its API-first order decides whether a browser is needed.

## Explore with agent-browser

[agent-browser](https://github.com/vercel-labs/agent-browser) is a browser CLI built for agents. Install it with `npm install -g agent-browser`, then `agent-browser install` to download Chrome for Testing.

```sh
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e3
```

Use the accessibility tree and role or label locators. Use screenshots only when the tree cannot answer the question. Keep any debugging endpoint inside scripts; never print one that carries a token.

## Save known flows

Once a flow works, save it as a Python [Playwright](https://playwright.dev/python/) script and run it without a model next time. A saved flow:

- takes its inputs as arguments, not edits to the file;
- gets credentials through the `access` fill pattern and never prints them;
- ends with an outcome check in code (`expect(page.get_by_text("App created")).to_be_visible()`) and exits non-zero when it fails;
- hands MFA, CAPTCHA and consent steps to the user, as `access` describes.

If a saved flow breaks, use agent-browser to find what changed, then fix the script.

## Never

- Touch a browser, profile, cookies, storage, process or debugging port that you did not start for this task.
- Expose a debugging endpoint or its token.
- Solve CAPTCHAs, bypass MFA, or use stealth or anti-detection tools.
- Use Playwright MCP on pages that receive secrets. Its accessibility snapshots have carried password values into model context ([microsoft/playwright-mcp#1566](https://github.com/microsoft/playwright-mcp/issues/1566)).

## Testing

For no-login tests, a local throwaway Chromium is fine. Keep its profile in your own scratch directory, bind its debugging port to `127.0.0.1`, use a free port, and stop only the process you started. Keep Chromium's sandbox enabled. Run saved Playwright flows without a model and check the outcome in code. Use agent-browser for exploration.

## Evidence

In my own comparison on a synthetic test site (October 2026, medians of three or four runs), agent-browser completed the form task 3 of 3 times at 25.6 s and 262k tokens per run, and a saved script completed it 4 of 4 times at 4.6 s with no model. In 13 Playwright MCP runs the snapshot carried the site's synthetic client secret into model context.
