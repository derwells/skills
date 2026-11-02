# Learning in a fleet Discord thread

Use this adapter only when the learner is teaching or studying in a fleet Discord effort thread. In Discord, the learner asks in an ordinary message; `/learn` names the agent skill, not a registered Discord slash command. Explore an ad hoc topic as deeply as useful across turns without creating a course, curriculum, or `.learning/` directory. For an established course, use the normal course context and persistence rules as well as this adapter.

Discord controls are optional. When the learner says they are on a phone or tired, choose the least demanding useful interaction: listening, a short chat reply, or a button. Do not infer their device or energy from Discord alone. Use an answer prompt when two to four distinct choices would make a useful prediction or reveal a specific distinction. Use ordinary text when the learner needs to explain reasoning, ask a question, or respond in their own terms. The learner may ignore a prompt, say "skip" or "continue," or reconsider an answer in chat. Follow that conversation; do not require a button before continuing or create an overdue check. A button choice gives narrow evidence about that choice; ask for reasoning only when it will change what to teach next.

If controls are unavailable, ask the question in plain text. Accept a natural free-text answer and, when useful, a confidence self-report in the learner's own words. Continue teaching from those responses; neither controls nor a course are required.

When a drawing helps, generate a rendered image and attach it beside a short explanation. Discord does not render Mermaid source or HTML diagrams inline. Use an available diagram skill for labelled objects and connections. Export its output to PNG and inspect the image before sending it. Keep labels readable at phone width. Use ASCII diagrams only when the learner requests them or image delivery fails; explain the failure.

Include the image in the first reply to the current inbox unit:

```text
fleet reply <unit-id> --text-file <reply-file> --file <diagram.png>
```

`fleet reply --file` needs a verified caller identity. Prepare the text and all attachments before this once-only reply. Check the posting receipt and, when feasible, the posted image. A recorded reply or local file alone does not prove delivery. If delivery or display verification fails, state the limit and provide a verified image link when available. Explain the essential relationship in prose. Do not require the learner to confirm display before continuing. Do not send the figure through Telegram unless asked.

To post a choice in the current lead effort thread, write the question and a JSON array of two to four option strings to files, then run:

```text
fleet learn ask --section <section-id> --question-file <file> --options-file <file> [--answer <1-based index>]
```

The optional `--answer` marks a known correct choice for feedback; omit it when the choices are positions, predictions without a single correct answer, or other non-graded responses. The command returns a prompt ID. Keep that ID with the teaching turn so a later response can be tied to the actual question. Free-text replies in the thread remain valid responses.

If a separate self-report would help pace the explanation, request a one-to-five confidence choice:

```text
fleet learn confidence --section <section-id> [--prompt <prompt-id>]
```

Link it to the relevant answer prompt when there is one. A confidence choice says how sure the learner feels; it is not a measure of demonstrated understanding. Do not turn a high score into `solid`, a low score into `shaky`, or a correct button into mastery. Use the learner's explanation, application, corrections, and the help given for course judgments under `references/progress-schema.md`.

If a new explanation changes a question or its premises, retire the stale controls and use the learner's later response in context:

```text
fleet learn retire <prompt-id>
```

Advancing to a new section also retires controls from the prior section. A learner's "skip" or "continue" needs no replacement prompt.

For a course, persist consequential learner responses and course-run feedback in the normal `sessions/<date>.md` log and update `progress.json` when a judgment or next-session pointer changes. A button response arrives as a `discord_learning` inbox unit. Record its `source_id` (the Discord interaction ID) and the payload's `prompt_id`, `kind`, `choice`, `choice_text`, `user_id`, `message_id` (the actual prompt), `channel_id`, `section`, and `event_at` in the session log. The unit's link opens the prompt. Free-text replies follow ordinary Discord message delivery; retain their message reference when they affect progress. Keep an answer and its later confidence choice as separate events. Use `source_id` to record a button response once even if it is delivered again after a restart. In `progress.json`, retain only the short observation and a source reference needed to support the current judgment; keep the event trail in the session log. For ad hoc teaching, do not create these course records unless the learner explicitly makes it part of a course.
