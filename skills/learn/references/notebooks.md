# Exercise notebooks

Practical exercises, runnable demonstrations, and persistent figures live in Jupyter notebooks, one per lesson, at
`.learning/<course>/notebooks/<unit>-<lesson>-<slug>.ipynb`. The learner can open the notebook
(VS Code, JupyterLab, or a browser over SSH) to do an exercise; show figures inline
in the conversation so that following a question does not require opening it. Short inline code and equations
can carry a question without a notebook. Use a notebook when the learner must run or write
something, or when a figure should persist; do not create one to satisfy a format.

An exercise is a check only when you see the learner's actual output: the code they wrote, the
value they got, the plot they produced. Ask them to paste it. Their description of what they
did is not the output.

A course may declare a different notebook tool in its "Course mode" section (marimo `.py`
notebooks, for instance, when the learner wants git-diffable, reactive files). Default to
Jupyter when unstated. The rules below apply either way.

## Moving between chat and the notebook

Treat opening a notebook, finding a cell, scrolling, and rerunning code as learner actions that
take time. For discussion, put the relevant excerpt or displayed figure in chat. For an actual
notebook task, identify the file or verified link and a stable heading or recognizable cell,
then state one action and wait for the result needed next. Use labels such as the cell beginning
`summary = az.summary(...)`, not an unexplained "row 7" or a cell number that may have shifted.
Do not assume the learner is still looking at output from an earlier run. Tutor execution and
material saved to disk do not establish what is visible to the learner.

## Rules

1. **Execute demonstrations before you point.** Run completed demonstration cells and
   inspect their outputs before referring to them. For a notebook containing only completed
   demonstrations, use `jupyter nbconvert --to notebook --execute --inplace <path>`.
   Keep unfinished exercises and answers to pending predictions out of bulk execution.
   Validate prediction results in a separate scratch execution, without publishing the answer
   in the learner's notebook. A failed demonstration must be repaired before teaching from it.
2. **Figures are claims.** Label the axes, mark anything that must line up (a tick, a guide
   line, a label). Look at the rendered output before pointing at it and confirm it shows
   the thing you're about to say. No decorative or approximate geometry.
3. **Make the argument visible.** Introduce the lesson's question, explain why each code
   step is needed, and connect the output to the general claim. Keep cells small enough to
   inspect. Use consistent variable names across chat, code, and figures. For unfamiliar code,
   follow [code-reading.md](code-reading.md): show concrete inputs, intermediate values and shapes,
   and the mapping from the lesson's concept to the library operation. Supply incidental setup.
   Reading outputs and choosing the relevant calculation can be the learner's whole task.
4. **Compare deliberately.** Where a distinction matters, show cases with the same setup
   and change the relevant feature. Align plots and scales where comparison requires it.
   Ask for the prediction before the cell runs, when the learner has what they need to
   reason; state the missing definition first when they do not. Keep solutions out of the
   learner's notebook until the question is closed.
5. **Reduce help as the level rises.** A partly completed cell suits level 3; a new
   application with only the setup supplied suits level 4. Leave the consequential decision
   to the learner. A walkthrough that the tutor runs is exposure and earns no level; an
   exercise the learner skipped is not a failed check.
6. **Keep notebooks per lesson, not per session.** A revisit adds cells to the lesson's
   notebook under a dated heading; it doesn't create a new file. Use sections so a lesson
   spanning sessions remains navigable.
7. **Write with the host's notebook tool** (`NotebookEdit` in Claude Code) rather than
   hand-editing `.ipynb` JSON. If none exists, generate with `nbformat` from Python.

## Toolchain

`python3 -m venv` may be broken on the learner's machine; use `uv`.

```
uv tool install jupyterlab            # once per machine
uv venv .learning/<course>/.venv       # once per course
uv pip install --python .learning/<course>/.venv/bin/python ipykernel numpy matplotlib <course packages>
.learning/<course>/.venv/bin/python -m ipykernel install --user --name <course-slug>
```

Set the notebook's kernel to `<course-slug>` so execution uses the course venv. Course-specific
pins (e.g. `arviz<1.0`) live in the course's `progress.json` notes. Add `.venv/` to
`.gitignore`; notebooks themselves are worth committing with outputs, since the outputs are
the figures the learner saw.

## Figure delivery

Show figures inline in Paseo using the host's supported image display mechanism. Save and
inspect the rendered image, then display it alongside the explanation; merely saving a file
or giving its path does not make the figure visible. The notebook remains the record.

Older learner notes and example transcripts may refer to pushing figures through Telegram.
Those are not the current delivery default. Use Telegram or another external channel only
when the learner explicitly requests it, under the host's authorization rules. If inline
display fails, provide a link to the saved figure and explain the limitation; do not
automatically switch to Telegram.
