# Voice and Shape

## The voice

A chapter talks to one reader across a desk: **we** build, **you** try, and every idea arrives as a motive, a picture and a small slice of code.

- **Motive before mechanism.** Every section opens with why a reader in the mission's world would care (what a monitor loses, what an attacker gains), then the rule. "Why would a monitor need a third kind of proof at all?" comes before `SUBPROOF`.
- **Derive, don't assert.** Show where a number or rule comes from before using it. "Proof size is log₂ n" is preceded by the halving picture; "at most ⌈log₂ n⌉ + 1" is preceded by the seam walk that counts them.
- **Concrete before general.** A worked example with real values (`h01 = 83571100ed5e`), then the statement in symbols. Hand-trace tables carry the example; the general rule is one sentence after the table.
- **One idea per section, one sentence per idea.** Short paragraphs, two to four sentences. A section that needs a second idea gets a §N.x.y subsection.
- **Algorithm before code.** Each algorithm is given in numbered plain-language steps, traced by hand in a table, drawn as a storyboard figure, and offered as a try-it, before the code appears. The code is then presented as the answer key, with a note mapping each branch back to a step number.
- **Light humour, sparingly.** One dry aside per section at most ("If every old size were a power of two we could stop here. They aren't, so we can't."). Definitions stay straight.
- **Honesty in the margins.** Citations, history, what the spec actually says, and confessions ("the old lesson showed a placeholder here") go in `aside.margin`. The main column stays a single line of argument.
- **Sentences.** Prefer a colon or a new sentence to a dash. Code font for identifiers and values, italics for the stressed word, bold for the claim the section exists to make. Every claim about a spec quotes it or links it.

Dry and chapter, side by side:

| Dry | Chapter |
|---|---|
| "Consistency proofs verify that a tree of size n is an append-only extension of a tree of size m." | "Look for `root3` in the new tree. **It isn't there.** Once `cert-D` arrived, `h2` took a new partner, and the pair that made `root3` was never hashed together again. So what *does* survive an append?" |
| "The proof has O(log n) size." | "Both trees agree everywhere except along one seam. Walk down toward it: one node per level, one sibling hanging off each, plus the fragment at the bottom. Three levels crossed plus one fragment is the four hashes you traced." |
| A 90-line file after the prose. | Three 15-line slices, each under a `code-loc` label saying where it goes, each followed by the sentence that maps its branches to the steps above. |

## The shape

In order. Section numbers use the lesson number (`5.1`, `5.1.1`).

1. `p.lesson-kicker`, `h1`, `p.lesson-summary` (unchanged from the workspace's convention).
2. `blockquote.epigraph`: one quotation that the chapter earns by its end (Orwell on controlling the past for a chapter about rewriting history; Strunk on unnecessary parts for a chapter about the shortest proof). Attribute with `span.who`.
3. **Intro**: where the previous lesson left off, the question this chapter answers, then "here is the whole machine" and Figure 1.
4. **§N.1 The motive**: the problem, shown as an attack or a loss, with a figure. Then the claim to prove, made precise, with a figure.
5. **§N.2…** The concept in simple pieces: the gentle case first, the hard case second, each with its figure; the derivation of the cost (size, time) with its figure and an aside giving the exact numbers for small cases.
6. **Algorithm 1** (the producer's job): steps, hand-trace table, storyboard figure, unwind paragraph, `div.try-it` with answers you verified.
7. **Algorithm 2** (the consumer's job): the same treatment; the payoff paragraph that names the values the reader has now seen three times.
8. **§N.x Now Try It, Then Check Against Mine**: `div.try-it` inviting the attempt, then subsections per slice: `p.code-loc` + `pre`, the mapping note, `main`, run output, the analysis of what the output shows (with a figure for the failure case), the stretch (spec's own example) with its figure, `details.listing` with the complete file.
9. **Who runs this, and when**: the endpoint, the state a real client keeps, the composition argument, the forward hook to a later phase. Figure.
10. **Why this is the keystone**: the chain of lessons so far. Figure.
11. `h2 Check yourself` + `div.quiz#quiz` (the quiz is unchanged on a rewrite).
12. `div.challenges`: four, each an implementation or proof the reader can actually do, each citing the spec section or code it comes from, each ending in a question.
13. `div.design-note` with an `h2 Design Note: <Title Case>`: one design decision the chapter touched, the alternative, the trade, and the sentence to carry forward.
14. `div.win`, `h2 Go deeper` (primary sources + the workspace reference), `p.ask-teacher`, `div.lesson-nav` (previous · cheat sheet · glossary | next), scripts (`figures.js`, `quiz.js`, the quiz).

## The components

```html
<blockquote class="epigraph">
  “Who controls the past controls the future: who controls the present controls the past.”
  <span class="who">— George Orwell, <em>Nineteen Eighty-Four</em></span>
</blockquote>

<aside class="margin">
  §4.4 takes two decimal inputs, <code>first</code> and <code>second</code>, and returns one array, <code>consistency</code>.
</aside>

<p class="code-loc">ct-lab/main.go · add after <code>rootFromProof</code></p>
<pre><code>@@C_PROVECONS@@</code></pre>

<details class="listing">
  <summary>ct-lab/main.go — the complete file after this lesson</summary>
<pre><code>@@C_FULL@@</code></pre>
</details>

<div class="try-it">
  <p>Before reading on, form the proof from <code>m = 2</code> on paper. You should get <code>[h23, h4]</code>, that is <code>[838bae825be4, 9db0c283a20c]</code>.</p>
</div>

<table>
  <tr><th>Call</th><th>n, k</th><th>Branch</th><th>Emits (after recursing)</th><th>Recurse into</th></tr>
  <tr><td>A,B,C,D,E · m=3 · b=true</td><td>5, 4</td><td>3 ≤ 4 → old is left</td><td><code>mth(E) = h4</code></td><td>A,B,C,D · m=3 · b=true</td></tr>
</table>

<div class="challenges">
  <h2>Challenges</h2>
  <ol>
    <li>… Implement it and check it against <code>rootsFromConsistency</code> for every <code>1 ≤ m ≤ n ≤ 16</code>.</li>
  </ol>
</div>

<div class="design-note">
  <h2>Design Note: The Flag Is About the Verifier, Not the Tree</h2>
  <p>…</p>
</div>
```

Figures are `figure.fig` blocks generated by figlib.py; see FIGURES.md.

## Rewrites keep everything

A rewrite is a change of voice and structure, never of content. Every fact, citation, hand-trace value, code snippet, link and quiz question of the original survives, and the build asserts it. Add only what step 2 verified: a placeholder replaced by the real value, an edge case computed, a spec sentence quoted after fetching it.
