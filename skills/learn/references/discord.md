# Tutoring in a fleet Discord thread

Use this adapter only when the session runs in a fleet Discord effort thread. The learner writes ordinary messages; `/learn` names the agent skill, not a registered Discord slash command. An ad hoc topic needs no course, curriculum, or `.learning/` directory. For a saved course, the normal course rules apply as well.

## Questions and answers are messages

Ask each question as an ordinary message and end the message at the question. The learner answers in their own words. Short answers, fragments, and phone typing are fine; judge the reasoning.

Put the skill map in a code block so the bars line up. Keep one question open at a time. If several messages make it unclear which question an answer belongs to, ask one short clarification.

## Figures

When a drawing helps, generate a rendered image and attach it beside a short explanation. Discord does not render Mermaid source or HTML diagrams inline. Use an available diagram skill for labelled objects and connections. Export to PNG and inspect the image before sending it. Keep labels readable at phone width. Use a text drawing only when the learner asks for one or image delivery fails, and say what failed.

Include the image in the first reply to the current inbox unit:

```text
fleet reply <unit-id> --text-file <reply-file> --file <diagram.png>
```

`fleet reply --file` needs a verified caller identity. Prepare the text and all attachments before this once-only reply. Check the posting receipt and, when feasible, the posted image. A recorded reply or a local file does not prove delivery. If delivery cannot be verified, say so and give a verified image link when one exists. Do not send the figure through another channel unless asked.

## Answer buttons are optional

The thread has answer buttons. They are not the default. Use them only when the learner asks for options or says they want to tap, for example on a phone. Prepare the options under [question-craft.md](question-craft.md#when-the-learner-asks-for-options).

Write the question and a JSON array of two to four option strings to files, then post the check in the current lead effort thread:

```text
fleet learn ask --interaction combined-v1 --section <section-id> --question-file <file> --options-file <file> [--answer <1-based index>]
```

Use `--answer` only when one option is correct. Keep the returned prompt ID with the teaching turn. A/B/C/D map to the one-based option indices. Use ordinary message text for the question and option text; the controls appear below it. Keep internal IDs out of visible content.

Selecting an option stores a pending choice that the learner can change. "Check answer" submits it. "Skip" closes the check with no judgment. An unfinished selection creates no deadline or reminder.

A submitted option is recognition, not a check. After it arrives, ask for the reason in words ("B. What makes it B and not A?"). The reason is what the evaluation rules count. A tapped letter with no reason raises no level, and a wrong tap gets a narrower question like any other wrong answer.

The controls also show an optional confidence dropdown. Do not ask the learner to use it. If they do, keep the rating with the answer as a self-report. It never changes a level.

## Chat alongside the controls

Accept letters, numbers, explanations, and corrections in ordinary chat. An ordinary chat message does not submit or erase a pending selection.

Inspect the current state when pending context matters:

```text
fleet learn state <prompt-id>
```

Mark a narrower question or a direct explanation before sending it, with the available message or inbox reference as the source:

```text
fleet learn state <prompt-id> --mark help --source <reference>
fleet learn state <prompt-id> --mark feedback --source <reference>
```

Use `help` for a narrower question, a hint, or a definition. Use `feedback` when you reveal correctness or the answer. A marker records the tutor's action; it does not prove the learner read the message.

Close the controls when a free-text answer finishes the question, or the learner says "skip", "continue", or "just tell me":

```text
fleet learn state <prompt-id> --mark chat-complete --source <reference>
```

Use the chat answer as the evidence. Keep any pending button selection as `selected_not_submitted` context, ungraded, and tell the learner it was not submitted.

Retire controls when the question's premises change or the session moves to another subskill:

```text
fleet learn retire <prompt-id>
```

The command returns pending context for combined prompts. Preserve it without a grade. Session, lead, or section changes make old controls stale; ordinary chat remains available. A stale or rejected action is not learner evidence.

## Older controls

The original commands remain available:

```text
fleet learn ask --section <section-id> --question-file <file> --options-file <file> [--answer <1-based index>]
fleet learn confidence --section <section-id> [--prompt <prompt-id>]
```

Without `--interaction combined-v1`, answer buttons submit immediately. The separate confidence command asks about the section, including when `--prompt` pairs it with an answer. Do not start new confidence prompts. Do not infer support on another surface from this adapter.

## Course evidence

For a saved course, keep consequential answers in `sessions/<date>.md` and update `progress.json` under [progress-schema.md](progress-schema.md). A free-text answer keeps its actual message reference as `source`.

Button submissions arrive as `discord_learning` inbox units with `kind=understanding_attempt` and `interaction=combined-v1`. When you record one, keep these payload fields when present:

- `prompt_id`, `question_revision`, `answer_revision`, and `selected_option_id` / `selected_option_text`.
- `answer_source`, including its `interaction_id`, `channel_id`, `message_id`, `user_id`, `answer_revision`, and `event_at`.
- Optional `confidence`, including its `value`, source fields, and `timing` (`before_feedback`, `after_feedback`, or `unknown`); keep `confidence_scope=answer`.
- `help_sources`, `feedback_sources`, `chat_sources`, `outgoing_sources`, and the `synthetic` marker.

Keep the inbox `source_id` and prompt link, and deduplicate repeated delivery by source identity. Record the submission as `kind: "recognition"`; record the reason the learner then gives as its own entry. A `learning_skip` records a skip with no judgment.

**Existing records.** Earlier sessions stored answer and confidence events under older rules. Legacy events keep their `source_id`, `prompt_id`, `kind`, `choice`, `choice_text`, `user_id`, `message_id`, `channel_id`, `section`, and `event_at`. Historical confidence prompts sent with the separate command are about the section, not about a selected answer; keep their values and that meaning. Do not delete, regrade, or reinterpret any of these, and do not derive levels from them.

Exclude synthetic demos and agent-operated taps from learner records. Use `--synthetic` for control demonstrations. Check data-level markers and demo provenance; a user identity alone does not establish a real learner response. Historical demos can lack a marker; exclude them when their source identifies them as demonstrations.
