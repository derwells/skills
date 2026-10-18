# Create a course and prepare teaching materials

## Establish the destination

Read `.learning/learner.md` and check for overlapping courses first. Infer what the conversation establishes; ask only for missing information that changes the course. Establish the learner's background, what they want to understand or do, intended depth, available time, and any deadline.

Default to a professor-led tutorial. Participation can range from mostly listening to substantial problem solving without changing the intellectual level. Use `design-partner` when the user wants learning centered on their own work. Do not force a choice between being drilled and being briefed.

## Research the course

Use real university syllabi, textbooks, primary research, and well-developed lectures to establish prerequisites, scope, and examples. Select a coherent source backbone and explain what each source contributes. Verify precise claims before teaching them. For broad gathering, use available subagents when authorized; the main tutor remains responsible for the synthesis and checked sources.

Research the difficult distinctions as well as the topic list: what learners commonly confuse, which comparisons reveal the difference, and what prerequisite makes a derivation understandable. A source's reputation alone does not establish that its example fits this learner. Keep useful sources attached to the relevant teaching notes.

## Write the curriculum

`curriculum.md` contains the course goal, course mode and level, expected workload, prerequisite map, then units and lessons. Give honest estimates and let lessons span sessions when needed. For each lesson, record:

- Its central question and the reasoning or task the learner should be able to perform afterward.
- Stable concept IDs and prerequisites, including connections to earlier lessons.
- Where code matters, the unfamiliar library operations or coding ideas to teach in that lesson, and a small input-to-output bridge to its real example. Distinguish reading code from writing it independently; select libraries by course need. Read [code-reading.md](code-reading.md) when preparing these examples.
- The essential distinction or argument, with a promising example or contrast.
- The mathematical or conceptual starting point, and which definitions must precede the example. For a learner who prefers math first, plan the equation or derivation before its instances; do not impose analogy-first ordering.
- A suitable application that can reveal understanding. Scale its independence and difficulty to the intended level.

Plan later opportunities to use important ideas in different contexts and choose between methods without being told which one to apply. Include derivations, readings, problem sets, or projects when the course goals need them. An advanced course should reach the intended depth, with prerequisite support along the way.

## Prepare the first two units

Write `materials/unit-NN-<slug>.md` as notes a tutor can teach from. For each lesson, prepare:

1. **Question and argument.** The problem being answered, why earlier ideas are insufficient, and the path through the explanation. Include the reasoning between steps, not just headings.
2. **Worked example.** A tractable case with a checked solution. Explain the choices, not only the operations. Connect the result to the general claim, including the actual mathematics when relevant.
3. **Contrasts and boundaries.** Select a useful neighboring concept, near miss, changed assumption, or alternative method. Specify what is held fixed, what changes, the expected result, and why. Include the tutor's explanation and identify what the learner can infer before hearing it. Do not force every type into every lesson.
4. **Representations.** The figure, equation, code, or source passage that makes the argument visible. State how the representations connect. For code, include the relevant intermediate values and shapes, the mapping from concept to API, and enough explanation to read it without a documentation detour. For comparable figures, specify consistent scales and labels where appropriate.
5. **Likely confusions and responses.** What a mistaken answer could mean, how to distinguish plausible causes, and which explanation or prerequisite repair would help. Avoid a queue of questions the learner must answer.
6. **Practice with decreasing help.** A consequential step the learner could supply, followed by an unfamiliar case or choice of method when ready. Include worked answers and hints for the tutor. In `design-partner`, keep these as optional discussion material.
7. **Sources and limits.** Links for technical claims; assumptions, approximations, and open disagreements where relevant.

These are preparation requirements, not a seven-part script to recite in chat. Use the learner's response to choose which pieces to teach. If an idea genuinely needs no contrast, explain it directly rather than inventing a misleading comparison.

For mathematical lessons, use [lesson-craft.md](lesson-craft.md). Prepare natural stopping points that leave an example or equation available for private thought. An application can occur later; a fully explained comparison followed immediately by a required answer is not the only form of participation.

A compact example of useful preparation: for recursive termination, hold the integer input fixed and compare self-calls with unchanged input, decreasing input without a stopping condition, and decreasing input that reaches a stopping condition. Trace each. Then test the apparent fix with a decrement of two and a stopping condition at zero: on positive odd input it never reaches zero. The tutor's explanation must connect the stopping condition, progress, and input domain. A new application could use a shrinking list rather than an integer.

## Make the first lesson ready

Where code or figures help, prepare a lesson notebook using `references/notebooks.md`. Execute and inspect demonstrations; keep prediction answers separate from the learner's view until the comparison is discussed. Do not create a notebook merely to satisfy a format.

Initialize `progress.json` using `references/progress-schema.md`. Concepts without evidence are `unassessed`, or absent until taught. Present the course's purpose, level, workload, and first lesson. Run the lesson in the same sitting only if requested.

Prepare later units when the learner is within one unit of needing them. For an existing course, apply this preparation standard to the current and next lessons first. Preserve the course's scope and identifiers; expand useful existing notes instead of replacing the entire syllabus. Use `references/freshness.md` for current-practice topics.
