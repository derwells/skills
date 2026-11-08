# Preparing a lesson that leaves room to think

Prepare the mathematical argument and checked examples in full. The learner sees a sequence
of useful pieces, with time to connect them. Tutor notes are not a script to recite.

## Choose the gap deliberately

For each example, know its purpose, the prerequisites already available, and the next inference
the learner could make. Supply definitions, unfamiliar notation, and essential assumptions.
Leave familiar algebra, a comparison, or a consequence open when the learner can reach it.
If they ask for the missing step, give it directly. A request for explanation is not a failed test.

## Example: a definition before its interpretation

The learner has asked what drift means in a weekly random walk. A poor response introduces
parameter uncertainty, the square-root rule, a histogram, and a sample-size question. None of
those establishes the object they asked about.

A useful first segment is:

> Let `y_t` be the level in week `t`. The model is
> `y_t = y_(t-1) + d + e_t`, with independent errors `e_t` drawn from `Normal(0, s^2)`.
> Here the second Normal argument is variance. `d` is the expected change over one
> weekly step; `s` is the spread of those changes. For `d = 2`, a realized error of `-3` takes
> a level of `100` to `99`.

End there. The example puts expected change and actual change in the same equation. There is
no need to append a quiz, a second analogy, or every consequence for the forecast.

The tutor's next prepared segment can contrast the path with a straight line plus independent
noise. Reuse the same first error and zero later errors in both models. The equations and two
short paths make the persistence of a shock visible. Let that comparison sit before explaining
its consequence for forecast uncertainty. Do not require the learner to type the inference.

## Example: a request for why needs a derivation

If the learner asks why averaging `n` independent observations with variance `s^2` reduces
uncertainty, have this derivation ready:

`Var(mean) = Var((X_1 + ... + X_n)/n) = (n*s^2)/n^2 = s^2/n`.

The first scaling uses `Var(aX) = a^2 Var(X)`; the sum uses independence. Standard deviation
is the square root of variance, hence `SD(mean) = s/sqrt(n)`. If either variance rule is
unfamiliar, show why it holds before using it. A simulation can then show the result; numerical
agreement alone is not a derivation. Distinguish this sampling uncertainty from a Bayesian
posterior width, which also depends on the prior and what else is unknown.

## Repair an explanation without expanding the lesson

If the tutor called `s` the scatter of levels around a trend line, correct the referent:
it is the scatter of one-step changes around `d`. Use one existing transition to show the
subtraction. Stop before introducing the full distribution of accumulated errors unless
that is the learner's question. Record the tutor's error as such; don't turn it into an
unsupported claim that the learner lacks the prerequisite.

## Review the prepared lesson

- Can the learner identify the quantities and assumptions before interpreting the output?
- Does each example reveal one planned distinction, with checked arithmetic and provenance?
- Is there a natural stopping point before the tutor states a reachable consequence?
- Can the learner continue without answering a compulsory question?
- Are proofs, approximations, simulations, and empirical claims labeled accurately?

These are preparation checks, not a visible checklist or a fixed lesson rhythm. Preserve the
course's intellectual depth and independent practice goals while adapting participation.

## Prepare useful checks

Prepare a short series before teaching: a distinction, a changed example, and a later application when useful.
Show only the next useful question. Stop the series for learner questions or missing prerequisites.
During sustained teaching, try a check after roughly two or three short explanations.
Adjust that frequency to the learner and the value of the answers. It is not a completion requirement.

For each check, prepare these notes:

- The distinction the answer should reveal.
- The definitions, assumptions, and visible reference values the learner needs.
- The correct answer and its reason.
- The specific confusion behind each wrong option, called a distractor.
- The verified source when the answer depends on current project behavior or another external factual claim.

Use two to four plausible options. Do not add weak distractors to fill four positions.
Keep opinions and questions without one correct answer ungraded. Repair ambiguous wording before drawing an assessment from it.
Check a disputed answer against the actual source or calculation. Correct a tutor error explicitly and preserve the learner's correction.
Supply a missing definition or step directly. Do not append another quiz to that repair by default.

## Response paths

These invented responses illustrate feedback. They are not learner records or evidence that this question measures broad understanding.

The example has two tanks containing 100 and 50 litres. After a transfer, they contain 80 and 70 litres.
Ask what happened to their combined volume:

> A. It increased.
> B. It stayed the same.
> C. It decreased.

The intended distinction is a change in distribution versus a change in total.
B is correct: both totals equal 150 litres. A considers only the second tank; C considers only the first.
State that the figures are final volumes before asking. No knowledge of the transfer mechanism is required.

| Response | Feedback | Next action and evidence |
|---|---|---|
| B, confidence 5 | "Both totals are 150 litres. The distribution changed." | Move to a useful contrast. Record recognition in this example, without a mastery claim. |
| B, confidence 2 | "B is right. Compare 100 + 50 with 80 + 70. Both totals are 150 litres." | Keep this example briefly. Offer another comparison only if useful; require no justification. |
| A, confidence 5 | "The second tank gained 20 litres; the first lost 20. The combined volume stayed at 150 litres." | Check the wording and arithmetic first. Repair the distinction; require no immediate retry. |
| Skip or "just tell me" | "The total stayed at 150 litres. Only the distribution changed." | Continue with no correctness judgment, downgrade, or replacement question. |
| "B because both add to 150" | "Yes. The equal totals are the relevant reason." | Record an explanation within this example, which gives more evidence than the letter alone. |
| "What does combined mean?" | "Combined volume means the volume in both tanks added together." | Repair the definition. Keep the question open if its premises remain valid. |

For confidence 3 or no rating, confirm the correct answer and reason without assuming confidence or uncertainty.
Missing confidence stays unknown. Treat 1 and 2 as uncertain, 3 as middle, and 4 and 5 as confident.
These labels guide feedback; they do not estimate probabilities or determine understanding.

A prepared contrast keeps the first tank at 100 litres and changes the second from 50 to 100 litres.
Ask whether the total stayed fixed. No is correct: it rose from 150 to 200 litres.
Later, invite another pair of volumes totaling 150 litres without supplied choices.
An answer such as "90 and 60" shows limited independent application if the learner received no help.
It does not establish general mastery. Keep these follow-ups optional and accept ordinary words throughout.
