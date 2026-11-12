# Teaching evals

These cases check what the tutor writes next at particular moments of a session: a wrong answer in the learner's own words, a vague answer, a third failed attempt, "just tell me", a claim to already know something, a failed review, and an old saved course being resumed. They were written for the 2026-11-12 change that rebuilt the skill on Jane Street's `socratic-tutor`.

Every learner message here is scripted. None of it is evidence about a real learner.

## Cases

[`cases.json`](cases.json) has 20 cases. Each has a situation, the session so far, and yes/no criteria with the answer the current skill should produce. Most use one topic, how Git stores history, so the tutor's facts are easy to check.

- C01-C03: the start. A request to be taught, a one-off question, and an unclear request.
- C04-C08: one answer. Wrong, wrong for the third time, vague, "just tell me", and correct.
- C09, C10, C14, C15: the skill map. A second independent check, "show progress", a failed review, and every subskill at target.
- C13, C16-C19: learner moves. A picked option, "wait, what is HEAD", a request to only read, a claim to know the material, and a wrong answer inside the diagnostic.
- C20: the same loop in a Discord thread.
- C11, C12: a saved course written by an older version of the skill, in [`fixtures/legacy-course`](fixtures/legacy-course/.learning/learner.md). C11 resumes it. C12 saves state after a diagnostic, and [`run.py`](run.py) then checks the files: the old `understanding` labels and notes are unchanged, only diagnosed concepts have a `level`, and the learner's dated choice is added without removing the original contract text.

## Runs

[`run.py`](run.py) gives a tutor model one version of the skill under a neutral folder name and asks for the tutor's next message ([`tutor-prompt.md`](tutor-prompt.md)). A judge model then answers the yes/no questions about each message ([`judge-prompt.md`](judge-prompt.md)). The judge sees neither the version nor the expected answers. Criteria marked `mechanical` are checked by code.

- **Previous skill**: `skills/learn` at commit `63b5951`, tutor Claude Opus 5.5 at high effort.
- **This skill**: tutor Claude Opus 5.5 at high effort, and again with Codex `gpt-6-astra` at high effort.
- **Judge**: Claude Sonnet 5.5 for every run.

The Claude runs loaded no user settings, instructions, skills or MCP servers. The Codex run used an empty Codex home, and ran without Codex's own sandbox (`--codex-sandbox danger-full-access`) because that sandbox could not start on the test machine.

Two things were redone after the first pass, and the saved results are the second pass:

- C09 first asked two questions that both turned on deleting a branch. The tutor refused the raise and said the two answers were one check, which is what the skill asks for. The case now uses a second question about what a commit moves. C06, C09 and C20 were rerun in all three runs after their shared question was reworded to say the branch was already merged.
- The first Codex run could not read any file, so its replies never saw the skill. All 20 Codex cases were rerun.
- A review found that the C12 check for the learner's recorded choice could pass on an unrelated dated note. The check now looks only at added text, and the course files a tutor changes are saved in each result row under `files`.
- The saved-course rules then moved from `SKILL.md` to `references/courses.md`, so both runs of this skill were repeated in full on the final text.

## Results

<!-- results:start -->
| Run | Criteria met | Cases with every criterion met |
|---|---|---|
| Previous skill, Claude Opus 5.5 | 31 of 62 | 5 of 20 |
| This skill, Claude Opus 5.5 | 61 of 62 | 19 of 20 |
| This skill, Codex gpt-6-astra | 62 of 62 | 20 of 20 |

| Case | Previous skill, Claude Opus 5.5 | This skill, Claude Opus 5.5 | This skill, Codex gpt-6-astra |
|---|---|---|---|
| C01 start-diagnostic | 1 of 4 | 4 of 4 | 4 of 4 |
| C02 one-off-question | 2 of 2 | 2 of 2 | 2 of 2 |
| C03 unclear-intent | 1 of 2 | 2 of 2 | 2 of 2 |
| C04 wrong-answer | 1 of 4 | 4 of 4 | 4 of 4 |
| C05 third-failed-attempt | 2 of 4 | 3 of 4 | 4 of 4 |
| C06 vague-answer | 1 of 3 | 3 of 3 | 3 of 3 |
| C07 just-tell-me | 3 of 4 | 4 of 4 | 4 of 4 |
| C08 correct-answer | 3 of 3 | 3 of 3 | 3 of 3 |
| C09 second-independent-check | 0 of 3 | 3 of 3 | 3 of 3 |
| C10 show-progress | 2 of 2 | 2 of 2 | 2 of 2 |
| C11 legacy-course-resume | 2 of 4 | 4 of 4 | 4 of 4 |
| C12 legacy-course-save | 3 of 6 | 6 of 6 | 6 of 6 |
| C13 picked-an-option | 1 of 2 | 2 of 2 | 2 of 2 |
| C14 failed-review | 1 of 3 | 3 of 3 | 3 of 3 |
| C15 all-at-target | 0 of 2 | 2 of 2 | 2 of 2 |
| C16 what-is-x | 3 of 3 | 3 of 3 | 3 of 3 |
| C17 read-only-request | 2 of 3 | 3 of 3 | 3 of 3 |
| C18 claims-to-know | 2 of 2 | 2 of 2 | 2 of 2 |
| C19 diagnostic-wrong-answer | 1 of 3 | 3 of 3 | 3 of 3 |
| C20 discord-thread | 0 of 3 | 3 of 3 | 3 of 3 |
<!-- results:end -->

Recompute the tables from the raw replies and verdicts in [`results/`](results):

```bash
python3 score.py
```

It exits 1 if the recomputed tables differ from the ones above.

## Reading the results

The previous skill met half the criteria because it taught a different way. On a wrong answer it gave the correct result and explained it (C04). It taught hash tables before asking anything (C01), corrected an answer in the middle of the diagnostic (C19), accepted a picked option without asking for a reason (C13), and declared the topic finished without an assessment (C15). In the Discord case it posted answer buttons with an optional confidence rating (C20). When saving the old course it kept the old labels but rewrote the notes on two concepts, and it replaced the original contract text where the current skill adds a dated entry beside it (C12). It already answered a one-off question plainly, honored "just tell me", and declined to mark a subskill done on the learner's word.

The current skill missed one criterion with Opus: after the third failed attempt its explanation ran longer than the six or so sentences the case allows (C05). Everything else passed in both runs. In C12 both tutors kept every old label and note, wrote levels only for the three diagnosed concepts, and recorded the learner's dated choice next to the original reading-first rule.

## Limits

- One tutor reply per case per run. That shows a difference between versions; it does not estimate a rate.
- Each case tests one message. The earlier tutor messages in a case are scripted in the new style, including the skill map, so the previous skill is judged on a conversation it would not have produced.
- The criteria describe what the current skill intends. A low score for the previous skill means it behaves differently, which was its design, not that it was broken.
- No case measures whether anyone learns more. The cases measure whether the tutor follows the method.
- The cases and the skill change have the same author. The judge was independent of both, but the case selection was not.
- The Codex run could still see the name and description of an installed `learn` skill. The prompt told it to use only the copy under test.
- Nothing here runs in CI except `score.py`, which checks that this README matches the saved results. Rerunning the tutors and the judge needs model access.
