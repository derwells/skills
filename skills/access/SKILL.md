---
name: access
description: Use when a task needs something behind a login, a consent screen, a dashboard with no API, or another step that normally needs the user clicking around. Picks API, script or browser, fills passwords without exposing them, and pulls the user in only for MFA and CAPTCHA.
license: MIT
compatibility: Shell access. Browser steps use the browser skill (agent-browser or Python Playwright). Password fills need a password manager CLI the user has already unlocked, such as Bitwarden's bw.
---

# access

Goal: automate the steps that normally need a human and have no API key. The user steps in only for MFA and CAPTCHA, and their effort should be a code or a tap.

## Order

Stop at the first rung that works.

1. **Official API or CLI.** `gh`, `gcloud`, Linear, Stripe, Slack manifests, Atlassian tokens, and so on. If it needs a one-time grant, prefer a device-code or OAuth consent the user approves once over clicking through the UI. Check what access already exists before asking for new access; a new grant, account or paid plan is the user's decision.
2. **Saved script** for a known browser flow: a Playwright script that logs in, does the task and checks the outcome in code (`browser`).
3. **agent-browser** to work out a new flow or fix a broken one, then save it as a script (`browser`).
4. **The user**, only for MFA, CAPTCHA, a locked vault, or a page the agent cannot read.

Before acting on a site, write down the origins you are allowed to act on (for example `https://app.example.com`). Leave that list only with the user's approval.

## Credentials

Passwords never enter model context. Read them from the password manager inside the script that types them, check the page's origin first, and print status only. With Bitwarden's CLI, the user unlocks the vault in their own terminal and exports `BW_SESSION`; you never ask for the master password.

```python
import subprocess
from urllib.parse import urlsplit

ALLOWED = {"https://app.example.com"}

def fill_secret(page, item_id, label, field="password"):
    u = urlsplit(page.url)
    if f"{u.scheme}://{u.netloc}" not in ALLOWED:
        raise SystemExit(f"refusing to fill on {u.scheme}://{u.netloc}")
    value = subprocess.run(["bw", "get", field, item_id],
                           capture_output=True, text=True, check=True).stdout.strip()
    page.get_by_label(label).fill(value)
    print(f"filled {label}")
```

`bw get totp <item>` works only for items that store a TOTP seed; otherwise the code comes from the user. If the vault is locked or `bw` is not logged in, stop and ask the user to unlock it in their terminal. Never ask for a password in chat.

## Pulling the user in

Ask in one message for the single step you need, then wait:

- **Code:** the user types it into the page themselves. If they send it in chat instead, fill it at once and do not repeat it in later messages or files.
- **Takeover:** run the browser headed, ask the user to solve the check in that window and tell you when they are done.
- **Consent:** give the exact screen and button ("Allow Acme CLI access").

After the user's step, check the page yourself; "done" means submitted, not accepted. If a code was rejected, ask again.

## Never

- CAPTCHA solving services, MFA bypass, or anti-detection tools.
- Touching a browser, profile, cookies or debugging port that you did not start for this task.
- Creating accounts, buying plans, or adding grants or vault items without the user.
- Recording passwords, tokens or codes in transcripts, state, messages or logs. Never print a debugging endpoint that carries a token.

## Residual risk

An agent can script the page it drives, so a password typed into that page is only as safe as the agent's own scripts. Submit the form as part of the fill so the login clears the field, and do not inject page scripts before a fill.
