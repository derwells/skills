# Teaching through readable code

Use this when unfamiliar libraries or notation obstruct a lesson. The aim is to let the learner reason about an example without first reconstructing a library manual. Teach only the operations that the current argument needs, then return to the argument.

## Prepare the bridge

Choose the smallest example that retains the mechanism. Establish the mathematical or conceptual relationship before translating it into unfamiliar syntax. Start with concrete values or a short plain-Python calculation when that clarifies a compact library call. Keep the same quantities and variable names when translating into the library. Identify inputs, output, and the line that implements the concept; separate setup and plotting from that line.

For unfamiliar arrays, label the axes in domain terms, print a few values, and show the input and output shapes. Teach indexing as selecting positions, not specifying counts. Explain broadcasting as how differently shaped inputs align, and reductions as which axis is combined and which remains. Expand method chains into named intermediates. For unfamiliar framework objects, explain what the object represents before showing its attributes; a model declaration, a numerical draw, and a fitted result are different things.

The learner should have enough information to answer a subject question. A useful prompt asks which expression answers it or how changing one value affects the result. Looking up the spelling of a method is not evidence about conceptual understanding. Offer small edits or independent construction when the learner wants practice or the course's goal needs them, after the example is readable.

## A worked reading example

Suppose two simulated futures contain three weekly levels each:

```python
import numpy as np

paths = np.array([[100, 80, 95], [100, 110, 105]])
below = paths < 90
failed_path = below.any(axis=1)
fraction = failed_path.mean()
```

`paths` has shape `(2, 3)`: two futures, three weeks. Comparing every entry with `90` produces `below`, also `(2, 3)`, with rows `[False, True, False]` and `[False, False, False]`. `any(axis=1)` combines the week axis, leaving one answer per future: `[True, False]`, shape `(2,)`. The mean counts `True` as one and `False` as zero, yielding `0.5`. This is the fraction of these simulated futures that ever fall below 90; two paths would be too few for a useful probability estimate.

Contrast `below.mean(axis=0)`: it combines futures and leaves one fraction per week, `[0.0, 0.5, 0.0]`. A learner who can choose the first calculation for an "ever" question has connected the code to the concept. They need not memorize the axis number. At teaching time, show the worked case before asking about a changed case; do not reveal a pending prediction's answer.

## Adapt to the course

- NumPy and probability: concrete values, arrays and indexing, elementwise arithmetic, sums and normalization, then axes, broadcasting, and random draws as the lesson needs them.
- PyMC: a numerical generative calculation, the corresponding model declarations and `observed` data, then fitting and reading returned draws. Explain the difference between constructing a symbolic model and executing numerical operations. Teach named dimensions when reading actual outputs requires them.
- PyTorch: establish the loss and parameter update mathematically, then map a tiny token example to tensors with labeled axes, slicing, and reshaping. Explain which operation changes values, shape, or gradient state before using a compact training loop. Array mechanics support reading the training objective; they need not precede its meaning.
- SDKs, manifests, and other libraries: trace a small request or configuration through its concrete result. Teach unfamiliar fields and conventions at the point of use. A course without code need not acquire a coding strand.

Keep this support inside the planned lessons. The curriculum names where each operation first matters; it need not allocate a new unit. On resumption, repair the current example instead of restarting completed units. Preserve course-specific hands-on goals and listening preferences.

## Preparation and evidence

Execute runnable demonstrations in the course environment and inspect the results. Verify version-sensitive APIs against the installed version and official documentation. Supply setup so the learner can read immediately; documentation links provide optional depth, not missing steps in the explanation. Do not install a large new stack for a reading example when the course already has a working environment or a plain calculation suffices.

Track familiarity with an operation only when it changes the next teaching choice. Use an existing note, or a separate stable concept ID if code fluency is itself a course outcome. Do not downgrade subject mastery merely because the learner cannot decode unfamiliar syntax. Maintenance establishes a plan, not evidence that the learner has learned it.

Tutor references: [NumPy basics](https://numpy.org/doc/stable/user/absolute_beginners.html), [PyMC overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html), [PyTorch tensors](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html). Check the course's installed versions before adapting examples.
