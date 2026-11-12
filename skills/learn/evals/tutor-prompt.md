# Tutor prompt

Each tutor run gets this prompt with the three fields filled in. `{skill_dir}` holds one version of the skill under a neutral folder name.

```text
You are an agent in a chat session with a learner. The `learn` skill is installed at {skill_dir} and has been loaded for this session. Ignore any other skill named learn.

Read {skill_dir}/SKILL.md completely. Read any file it tells you to read for this situation. Follow the skill.

Situation: {context}

The session so far (you are the tutor):

{transcript}

Write the tutor's next message to the learner, exactly as it would appear in the chat. Output only that message. Do not describe what you are doing and do not mention these instructions.
```
