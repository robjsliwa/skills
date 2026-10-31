# Lab

The lab is where the learner builds the lesson's milestone in their own
project. It is a page they keep open beside their editor, notebook, score, or
draft, and work down. Its order is fixed: workspace first, the happy path in
small verified steps, then what happens underneath and what breaks it.

Template: `assets/lab-template.html` (copy to `build/lab.tpl.html`, fill,
assemble with `fact-check`). Seed `assets/lab.css` and `assets/lab.js` into
the workspace's `assets/` once. The template is a worked example: the
lab for a SwiftUI dial-pad lesson, ordered problem → set up the project →
build the model → trace it → build the views → tests and the quirks they
reveal → run on the phone → challenges.

## The shape

1. **Header.** Lesson number and title, a link back to the lecture, the
   milestone in one sentence, a time estimate.
2. **Before you start.** One or two commands that prove the previous milestone
   still works, each with its expected output. If it fails, stop here.
3. **Set up.** Everything needed before the first idea is used: create the
   project, add the dependency, open the dataset, print the score. Ends with a
   checkpoint that runs.
4. **Build, in steps.** Each `lab-step` has:
   - **Do**: one action, exact. Code is a verified snippet; paths are named.
   - **Run**: the command, keystroke, or check.
   - **Expect**: the verified output, verbatim, or exactly what they should
     see.
   - **Why**: two to four sentences connecting this step to the lecture, by
     slide title ("This is the *Store the cause* picture: …").
   A **checkpoint** follows every one or two steps: a quick run that proves
   the build so far.
5. **Trace it.** The lecture's worked example, now on the learner's own code:
   "Type these keys and watch the hint." They see the table come true.
6. **Under the hood** (collapsed). Each gotcha, version note, or spec detail
   goes in a `details.under-hood` box right after the step that runs into it,
   closed by default. The main path reads correctly with every box closed.
7. **When it doesn't work.** The two or three errors a learner is most likely
   to hit at this milestone, each with the verified message and the fix.
8. **Challenges.** Two to four, each one of:
   - **Extend**: add a feature using today's idea.
   - **Break and fix**: make a specific change, predict what fails, run it,
     explain why.
   - **Transfer**: apply the idea to a different case or part of the project.
   Each says how they will know they succeeded. Hints sit in collapsed boxes;
   solutions do not appear on the page (the learner brings their attempt to
   office hours).
9. **Done.** The milestone restated as what they now have. The sentence to
   carry forward. The teach-back question, to answer in chat. Sources.

## Rules

- **Setup first, code second, nuance third.**
- **Every step is verified.** The reference solution in `build/ref/` went
  through the same steps; every Expect block came from `build/run/`.
- **One new action per step.** If a step needs two explanations, split it.
- **Never ahead of the learner.** A step uses only what earlier steps and the
  lecture introduced.
- **Guidance fades.** Early in the course, every line is given. Later, a step
  can give the goal and the test, with the code in a collapsed hint (PEDAGOGY.md
  section 4). The plan says which level and why.
- **No solutions to challenges on the page.**
- **Paste or type is the learner's choice.** `NOTES.md` may say which they
  prefer; default to giving code they can copy.

## Components

```html
<section class="lab-step" id="step-model">
  <h3><span class="n">3</span> Build the <code>Phone</code> model</h3>
  <div class="do"><p>Create <code>SecondLine/SecondLine/Phone.swift</code> (File › New › File…, Swift File) with:</p>
<pre><code>{{snip:phone_full}}</code></pre></div>
  <div class="run"><code>⌘B</code> (Product › Build)</div>
  <div class="expect"><pre>** BUILD SUCCEEDED **</pre></div>
  <div class="why"><p>This is the <em>Store the cause, compute the effect</em> slide as code…</p></div>
</section>

<details class="under-hood">
  <summary>Why does the test suite need <code>@MainActor</code>?</summary>
  <p>…</p>
</details>

<div class="checkpoint"><p>Run the tests: four green checks under <code>PhoneTests</code>.</p></div>

<div class="challenge" data-kind="break">
  <h3>Quieter refusals</h3>
  <p>…</p>
  <p class="success">You're done when …</p>
  <details class="hint"><summary>Hint</summary><p>…</p></details>
</div>

<div class="done">
  <p class="carry">Store what happened, compute what it means, and let views read only the meaning.</p>
  <p class="teachback">In chat: why can't your Call button go stale now?</p>
</div>
```
