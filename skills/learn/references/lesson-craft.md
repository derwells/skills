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
