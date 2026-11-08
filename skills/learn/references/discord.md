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

## Answer and optional confidence

Prepare the question under [lesson-craft.md](lesson-craft.md). Hold one check open at a time.
Send the explanation before creating the check, or include it in the question file.
Unclassified tutor messages after creation make later confidence timing unknown.
Write the question and a JSON array of two to four option strings to files.
Post the check in the current lead effort thread:

```text
fleet learn ask --interaction combined-v1 --section <section-id> --question-file <file> --options-file <file> [--answer <1-based index>]
```

Use `--answer` only when one option is correct. Omit it for an ungraded discussion prompt.
Keep the returned prompt ID with the teaching turn. A/B/C/D map to the one-based option indices.

Use ordinary message text for the explanation, question, and option text. Controls appear below it with letter-only answer buttons.
The combined controls include an optional confidence dropdown and Check answer / Skip actions.
Keep decorative separators and internal learning IDs out of visible content. Do not require a card, embed, or separate application.

Selecting an answer stores a pending choice. The acknowledgement names it as selected but not submitted.
The learner can change it; changing the answer clears its pending confidence.
Check answer submits the choice and optional confidence together. Give feedback only after submission or a free-text answer.
Confidence can be absent. Skip closes the check without a correctness judgment.
An unfinished selection creates no deadline, reminder, or review debt.

The dropdown asks about the selected answer. Treat 1 and 2 as uncertain, 3 as middle, and 4 and 5 as confident.
Missing confidence stays unknown. Use these self-reports to choose feedback, not to assign mastery.
The [lesson-craft.md response examples](lesson-craft.md#response-paths) cover correct/confident, correct/uncertain, wrong/confident, and skip/free-text responses.

## Chat, help, and closure

Accept letters, numbers, explanations, and corrections in ordinary chat. Use the active question and reply reference to identify the answer.
If several questions make the reference ambiguous, ask one short clarification.
A definition question can leave the check open when its premises remain valid.
An ordinary chat message does not submit or erase a pending selection.

Inspect the current state when pending context matters:

```text
fleet learn state <prompt-id>
```

Mark help or feedback before sending it. Supply the available message or inbox reference as the source:

```text
fleet learn state <prompt-id> --mark help --source <reference>
fleet learn state <prompt-id> --mark feedback --source <reference>
```

Use `help` for a hint or prerequisite explanation. Use `feedback` when exposing correctness or the solution.
Chat or unclassified tutor text makes later confidence timing unknown unless explicit feedback state establishes it as after feedback.
A marker records the tutor's action; it does not prove that the learner read the message.
Do not infer timing from nearby timestamps. A later rating must not become initial confidence retroactively.

Close the controls when a free-text answer finishes the check, or the learner says "skip" or "continue":

```text
fleet learn state <prompt-id> --mark chat-complete --source <reference>
```

Use the chat answer as evidence when appropriate. Keep any pending button selection as `selected_not_submitted` context, without grading it.
Tell the learner that the pending button selection was not submitted or graded. Do not treat it as a competing answer event.
Preserve later corrections with their source and feedback context.

Retire controls when the question's premises change or teaching moves to another section:

```text
fleet learn retire <prompt-id>
```

The command returns pending context for combined prompts. Preserve that context without a grade and explain the closure.
A resumed tutor can reuse the wording in a fresh prompt. Old selections cannot become new attempts.
The current lead can read older prompt state in the same effort. Changes still require the original session.
Session, lead, or section changes make old controls stale; ordinary chat remains available.
A stale or rejected action is not learner assessment evidence. A skip or closure needs no replacement question.

## Compatibility

The original commands remain available:

```text
fleet learn ask --section <section-id> --question-file <file> --options-file <file> [--answer <1-based index>]
fleet learn confidence --section <section-id> [--prompt <prompt-id>]
```

Without `--interaction combined-v1`, answer buttons submit immediately. Existing prompts retain that behavior.
The separate confidence command asks about the section, including when `--prompt` pairs it with an answer.
Keep historical paired ratings section-level. Never reinterpret them as confidence about a selected answer.
For new checks, prefer the combined flow. If it is unavailable, use plain conversation or the existing controls with their stated meaning.
Do not infer support on another surface from an HTML prototype or this Discord adapter.

## Course evidence

For an established course, keep consequential responses in `sessions/<date>.md` under [progress-schema.md](progress-schema.md).
Update `progress.json` only when a judgment or next-session pointer changes. Keep ad hoc teaching in the conversation.

Combined submissions arrive as `discord_learning` inbox units with `kind=understanding_attempt` and `interaction=combined-v1`.
Record one complete attempt, retaining these payload fields when present:

- `prompt_id`, `question_revision`, `answer_revision`, and `selected_option_id` / `selected_option_text`.
- `answer_source`, including its `interaction_id`, `channel_id`, `message_id`, `user_id`, `answer_revision`, and `event_at`.
- Optional `confidence`, including its `value`, source fields, and `timing`; retain `confidence_scope=answer`.
- `help_sources`, `feedback_sources`, `chat_sources`, `outgoing_sources`, and the `synthetic` marker.

Keep the inbox `source_id` and prompt link. Deduplicate delivery by source identity, including retries after a restart.
Do not split one submission into competing answer and confidence events. Preserve their separate source references within the attempt.
Timing values are `before_feedback`, `after_feedback`, or `unknown`. Missing observations stay missing.
A `learning_skip` records a skip without correctness or an understanding judgment.

Legacy events retain their `source_id`, `prompt_id`, `kind`, `choice`, `choice_text`, `user_id`, `message_id`, `channel_id`, `section`, and `event_at`.
Keep legacy answer and separate confidence events distinct. Free-text evidence keeps its actual message reference.
Store only short observations and source pointers in `progress.json`; keep the full trail in the session log.

Exclude synthetic demos and agent-operated taps from learner records. Use `--synthetic` for combined control demonstrations.
Check data-level markers and demo provenance; user identity alone does not establish a genuine learner response.
Historical demos can lack a marker. Exclude them from assessment when their source identifies them as demonstrations.
