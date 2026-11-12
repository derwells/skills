# Create a course and prepare its questions

A saved course is the Socratic method in `SKILL.md` with a researched skill tree and files that survive between sessions. Creating one is expensive and done once.

## Establish the destination

Read `.learning/learner.md` and check for overlapping courses first. Infer what the conversation establishes; ask only for missing information that changes the course. Establish what the learner wants to be able to do, the target level (4/5 by default, 5/5 for full mastery), available time, and any deadline.

Do not ask the learner to rate their own level. The diagnostic places it.

## Research the course

Use real university syllabi, textbooks, primary research, and well-developed lectures to establish prerequisites, scope, and examples. Select a coherent source backbone and say what each source contributes. Verify precise claims before you build a question on them. For broad gathering, use available subagents when authorized; the tutor remains responsible for the synthesis and the checked sources.

Research the hard distinctions as well as the topic list: what learners commonly confuse, which comparison shows the difference, and which prerequisite makes a derivation reachable. These become questions. Keep useful sources attached to the relevant material.

## Write the skill tree

`curriculum.md` holds the course goal, target level, expected workload, prerequisite map, and the skill tree. The tree has two levels: units are branches, and each unit has 4-10 concepts, which are the subskills on the map. Give each concept a stable ID. Give honest estimates; a concept may span sessions.

For each concept, record:

- What the learner can do at levels 3, 4, and 5, in one line each.
- Its prerequisites, including concepts in earlier units.
- The distinction that learners most often miss, with a promising contrast.
- The definitions, notation, and conventions that must be told before any question uses them.
- Where code matters, the unfamiliar library operations the exercise needs. Read [code-reading.md](code-reading.md) when preparing these.

Plan where important concepts return in later units. Those returns are the spaced review, and they let the learner choose a method without being told which one applies.

A `Course mode` section records the target level and any choices the learner made about pace or delivery. Record a learner's explicit request for a different way of working there, dated, in their words.

## Prepare the first two units

Write `materials/unit-NN-<slug>.md` as notes a tutor can ask from. For each concept, prepare what [question-craft.md](question-craft.md) lists:

1. **Diagnostic questions** for the unit: 3-5, easy to hard, with what each answer places.
2. **Questions of several kinds**: a prediction, a "why", a flawed claim, a new case, a connection. Include the checked answer and the material each question must show.
3. **Likely wrong answers**, each with the narrower question that exposes the contradiction.
4. **New material**: the few sentences that state what cannot be derived.
5. **Fallback explanation and re-test**: the direct explanation for use after 2-3 failed attempts, and a question from a different angle.
6. **A practical exercise** where tools allow, with the output to check.
7. **A level-5 question**: an edge case or adversarial claim.
8. **Unit assessment**: at least one question per concept and one integrative problem, held back until every concept is at target.
9. **Sources and limits**: links for technical claims; assumptions, approximations, and open disagreements.

These are preparation, not a script. Show the learner one question at a time.

A compact example: for recursive termination, hold the integer input fixed and compare a self-call on unchanged input, a decreasing input with no stopping case, and a decreasing input that reaches a stopping case. The flawed claim is "it has a base case, so it stops", tested with a decrement of two and a stopping case at zero on an odd input. The narrower question asks the learner to list the value of `n` in each call. The level-5 question moves the idea to a shrinking list.

## Make the first session ready

Where code or figures help, prepare an exercise notebook using `references/notebooks.md`. Execute and inspect it; keep answers to pending questions out of the learner's view. Do not create a notebook merely to satisfy a format.

Initialize `progress.json` using `references/progress-schema.md`. Every concept starts with no `level`. Present the course's purpose, target level, workload, and first unit. Run the first session, starting with the diagnostic, only if the learner asks for it in the same sitting.

Prepare later units when the learner is within one unit of needing them. For an existing course, apply this standard to the current and next units first. Preserve the course's scope and identifiers; expand useful existing notes instead of replacing the syllabus. Use `references/freshness.md` for fast-moving topics.
