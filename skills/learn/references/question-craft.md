# Preparing questions and running the Socratic loop

Use this when you prepare a subskill, write a diagnostic, or need an example of a move in the teaching loop. The loop itself is in `SKILL.md`. The exchanges below are invented for illustration. None is a learner record.

## Prepare a subskill before teaching it

For each subskill, know these before the first question:

- **What each level looks like here.** Write one line for levels 3, 4, and 5: what the learner can do with help, alone, and on an edge case. Without this, a level is a mood.
- **Questions of several kinds.** A prediction, a "why", a plausible but wrong claim to find the flaw in, a new case to apply the idea to, and a connection to an earlier subskill. Two checks count as independent only when they use different questions, so prepare more than one.
- **The likely wrong answers.** For each, write the narrower question that makes the contradiction visible. A narrower question holds the example fixed and asks about one step.
- **The new material.** List the definitions, notation, units, and conventions the learner cannot derive. Write the few sentences that state them. These are told, not asked.
- **The fallback explanation and its re-test.** After 2-3 failed attempts you explain directly. Prepare that explanation and a question on the same idea from a different angle to ask straight after it.
- **A practical exercise** where tools allow, with the output you will check.
- **An edge case or adversarial question** for level 5.
- **The checked answer** to every question, with its calculation or source.

Show only the next question. The rest is tutor preparation, not a script.

## Choose questions that reveal a distinction

A contrasting case is a pair of examples chosen so that their difference shows one thing. Contrasts make strong questions because the learner must say what changed and why it matters:

- Two similar cases with different outcomes: "Only this input changed. What happens to the result, and why?"
- A valid example and a near miss: "Which of these meets the definition? What does the other one lack?"
- A working method and a plausible failure: "This version looks fine. On which input does it break?"
- Two cases that look different but share a structure: "What do these two have in common?"

Keep the setup legible: say what is held fixed and what changes. Ask for a prediction only when the learner has what they need to reason; otherwise state the missing piece first.

## Write the diagnostic

Write 3-5 questions that run from easy to hard and together touch every subskill at least indirectly. For each question, note what a strong answer, a partial answer, and "no idea" would place. Ask in words and take answers in words. Do not teach, correct, or react to correctness between questions; say only what moves to the next one.

Place each subskill from what the answers showed. Where no answer bears on a subskill, leave it `?/5` and check it when it becomes the focus. The diagnostic is a starting estimate; later checks correct it.

## The moves, with examples

The examples share one topic. The learner is studying what makes a recursive function terminate. The subskill is "a stopping case must be reachable".

### One question, then stop

> Here is a function on whole numbers:
>
> ```python
> def count(n):
>     if n == 0:
>         return 0
>     return 1 + count(n - 2)
> ```
>
> What happens when you call `count(5)`? Walk me through the calls.

The message ends there. No hint follows the question, no "think about odd numbers", no list of options.

### A wrong answer gets a narrower question

> **Learner:** it returns something like 2 or 3, it counts down by twos until it hits zero

Do not say "it never reaches zero". Hold the example and ask about one step:

> Write out the value of `n` in each call, starting from 5. Stop after five calls.

If the learner writes `5, 3, 1, -1, -3`, they have found the contradiction themselves. Then ask what that means for the stopping case.

### A vague answer gets a probe, not credit

> **Learner:** because the base case is wrong

That might be understanding, or it might be a phrase. Do not complete the thought for them:

> Wrong in what way? The function does have a line that stops at zero.

Credit the subskill only when the learner says that the stopping case exists but the calls step over it. Never record an insight the learner did not express.

### After 2-3 failed attempts, explain and re-test

Suppose the learner still says the function stops. Explain in a few sentences, then test the same idea from a different side in the same message:

> The calls go 5, 3, 1, -1, -3 and keep falling. The stopping case is `n == 0`, and an odd start never lands on 0, so the function never stops. Having a stopping case is not enough; the calls must reach it.
>
> Now a different function: it halves a positive whole number each call, rounding down, and stops when the number equals 1. Does it stop for every positive start? Say why.

The answer to this re-test comes straight after the explanation, so it is not unprompted recall. It can count as one check. A raise still needs another check later.

### A right answer sometimes gets pushed

> **Learner:** it stops for any positive number, halving always gets to 1 eventually

> Are you sure? What about a start of 1 itself, or 0?

The learner should defend the claim for 1 and notice that 0 is outside the stated domain, or that it would loop if allowed. Use this sparingly. Every answer challenged is noise.

### "Just tell me" covers one question

> **Learner:** just tell me

> It never stops for odd `n`: the calls skip over 0 and go negative. A stopping case only helps if the calls reach it.
>
> Next question. Change one line of `count` so that it stops for every whole number from 0 up. Which line, and to what?

Give the answer plainly, without a lecture about effort. Then return to questioning. The told answer earns no level. Ask about the same idea again later in the session, unannounced; that later answer can be unprompted recall.

### "Wait, what is X?" is answered directly

> **Learner:** wait what do you mean by stopping case

> The stopping case is the branch that returns without calling the function again. In `count` it is the `if n == 0: return 0` line.

Answer that one thing on the example in play. Add no new terms and no second question. The earlier question is still open, and this exchange is not a failed attempt.

### A missing fact is new material

If the question depends on something the learner cannot derive, such as what integer division does in this language, state it in a sentence before asking. Asking a learner to guess a convention teaches nothing and reads as a trick.

### A derivation can be led by questions

When the learner has the prerequisites, lead a derivation one step per question. To reach `SD(mean) = s / sqrt(n)` for `n` independent observations with variance `s^2`:

1. "What is the variance of the sum of two independent quantities, in terms of their variances?"
2. "So what is the variance of the sum of `n` of them?"
3. "The mean divides that sum by `n`. What does dividing a quantity by `n` do to its variance?"
4. "Put those together. What is the variance of the mean, and its standard deviation?"

If step 1 or step 3 uses a rule the learner has never met, that rule is new material: state it, then continue. A simulation can confirm the result afterwards; numerical agreement is not the derivation.

## When the learner asks for options

Free-text answers are the default because they show reasoning. Offer options only when the learner asks for them or the channel's controls are what they chose to use. Then:

- Give two to four plausible options. Each wrong option should match a specific confusion. Do not pad to four.
- Treat the selected option as recognition. Ask for the reason in words before you count it as a check: "B. What makes it B and not A?"
- A tapped or typed letter with no reason raises no level.

## Before you say "not quite"

Check the question wording and rework the answer. If the wording was ambiguous, fix the question and discard the attempt. If you were wrong, say so plainly and credit the learner's correction as the strong evidence it is. Label simulated data as simulated, and do not turn a teaching scenario into a claim about a real organization.

## Review the prepared material

- Does every question have a checked answer and the material it depends on?
- Is each unfamiliar definition or convention stated, not hidden in a question?
- Are there at least two different questions per subskill, plus a later one for unprompted recall?
- Is there a narrower question ready for each likely wrong answer?
- Is the level-5 edge case really beyond level 4, not just longer?
