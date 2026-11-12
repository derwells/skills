# Judge prompt

The judge sees one tutor reply at a time. It does not see which version of the skill produced it, or the expected answers.

```text
You are checking one message that a tutor wrote in a teaching session. Answer each numbered question about that message with yes or no. Judge only what the message says. Do not judge whether the teaching is good.

Situation: {context}

The session before the message:

{transcript}

The tutor's message to check:

<message>
{reply}
</message>

Questions:
{questions}

Answer with one JSON object and nothing else. Use each question's id as a key. Each value is an object with "answer" ("yes" or "no") and "quote" (a few words from the message that support the answer, or "" if there are none).
```
