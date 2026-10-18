---
name: handoff
description: >
  End-of-session checkpoint: prints a compact resumption prompt the user
  pastes after /clear, and commits pending work only if the user asked.
  Trigger ONLY when the user types /handoff or $handoff. Do NOT infer it from phrases
  like "I'll clear context", "give me a prompt", or mentions of a next
  session — if they want it, they type the command.
---

# handoff — resumption prompt for the next session

The user explicitly invoked handoff and is about to clear or start a new session. Your job: make the next
session start warm in one paste. The output is throwaway — it only has to
survive until the next session reads it.

## 1. Do NOT create files

Never create a status doc, STATUS.md, notes file, or any other file
for the handoff. The resumption prompt carries the state.

The one exception: if this session was already reading and updating a
working doc as its source of truth (a `.planning/` doc, a scope doc), update
that existing file with what got DONE, what's NEXT (ordered, first item = the
very next action), and any landmines. Keep it terse and current-state-only.

## 2. Commit — only if asked

If the user's message included commit/push intent ("commit", "push to origin
main"), do it: conventional message, no AI attribution, push exactly where
they said. If they didn't mention it and there are uncommitted changes, say so
in one line — don't commit unprompted.

## 3. Print the resumption prompt

End your reply with a fenced block the user can copy verbatim.

If an existing working doc was updated in step 1, point at it:

```
Read <working-doc path>. We're at <one-line state>. Next: <the single next
action>. <One constraint that matters, if any.>
```

If there is no working doc, the prompt carries the state inline:

```
Context: <what we were doing, 2-3 sentences>. Done: <concrete items — files,
PRs, decisions>. Next: <the single next action>. <Constraints that matter.>
```

Rules for the prompt:
- ONE paragraph. Under ~60 words when pointing at a doc; up to ~150 words
  when inline. Enough to resume, nothing more.
- Name any file the next session must open with a full path.
- If the next step is discussion (not implementation), say so explicitly in
  the prompt: "Discuss only, no code changes."
