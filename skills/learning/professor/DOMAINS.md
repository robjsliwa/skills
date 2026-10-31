# Domains

The professor teaches any subject, without a skill per subject. What changes
between subjects is not how people learn (PEDAGOGY.md holds for all of them)
but four things: what counts as a **primary source**, what a **project** looks
like, what a **lab step** is, and how a claim is **verified**. Subjects fall
into five lenses that answer those four questions. Pick one in Enroll and
record it in `SYLLABUS.md`; a subject that straddles two takes its project
from one and borrows verification from the other.

## The five lenses

| Lens | Examples | Primary sources | The project | A lab step | Verified by |
|---|---|---|---|---|---|
| **Engineering** | Swift, distributed systems, databases, networking, electronics | specs, RFCs, official docs, source code at a version, datasheets | a working system built one vertical slice per lesson | type this, run this, see this output | compiler, tests, saved command output |
| **Quantitative** | statistics, linear algebra, physics, finance, economics | textbooks by recognised authors, original papers, official datasets (FRED, BLS, CERN Open Data) | a model, simulation, or analysis notebook that grows a model per lesson | compute this, plot this, compare to this value | a values script recomputes every number; plots regenerated from code |
| **Natural science** | biology, chemistry, medicine, nutrition, ecology | peer-reviewed papers and reviews, reference handbooks, official guidelines, data tables | a case series, a protocol, a lab notebook, a field log | read this case, predict, check against the data or mechanism | citations opened; numbers recomputed (stoichiometry, doses from tables); no unsafe procedures |
| **Humanities and law** | history, philosophy, law, literature, policy | primary documents (letters, statutes, opinions, treaties, first editions), scholarly editions | a casebook, an annotated source reader, an argument map, a brief or essay built a section per lesson | read this passage, answer this question about it, write this paragraph | quotes matched to a named edition; dates and citations from two authoritative sources; argument structure checked |
| **Creative craft** | music theory, screenwriting, drawing, UI design, technical writing | masterworks, canonical texts on the craft, style guides | a piece composed, written, or designed in parts, one technique per lesson | analyse this example, make this small piece, compare to this model | the technique located in named works (bar numbers, page and scene); exercises checked against the stated rules; the learner's work critiqued against a rubric |

## Lens notes

**Engineering.** The lab is code the learner types in their own project; the
professor's reference solution runs in `build/ref/` first. Figures are
architecture, state, and sequence pictures. Watch for version drift: date
every claim about an API.

**Quantitative.** Derive before you use: every formula on a slide is preceded
by the case that motivates it and followed by a worked number. Real data beats
toy data when the mission is applied. Notebooks (Python with NumPy, pandas,
SymPy, matplotlib) are the lab medium unless the learner works in another.

**Natural science.** Mechanism pictures (pathways, cycles, reaction diagrams)
carry the lectures. The project is usually analysis, not wet lab work: cases,
data, and protocols on paper. Never instruct a dangerous procedure; health
topics carry a line that the course is not medical advice.

**Humanities and law.** The worked example is a close reading: one passage,
annotated, with the question it answers. Interpretation is taught as claims
with evidence: what the source says, what scholars infer, where they disagree.
Quotes are short and exact, from the edition `RESOURCES.md` names. Law varies by
jurisdiction and date: state both.

**Creative craft.** The worked example is a masterwork analysed for one
technique. Labs alternate analysis and making. Feedback is against stated
criteria, so each lab names its rubric. Do not reproduce copyrighted works at
length; point to bar numbers, pages, or timestamps and analyse them.

## Proposing a project

When the learner has no project, propose two or three in Enroll, recommend
one, and let them choose. A good project:

1. **Serves the mission.** Finishing it demonstrates the mission's "Success
   looks like."
2. **Is real.** It produces something they would use, show, or hand in: an app
   on their phone, a notebook on live data, a brief, a finished piece.
3. **Grows a slice per lesson.** Each lesson adds a working part. It runs, or
   reads, after every lesson, not only at the end.
4. **Fits the constraints.** Their hardware, time per session, and budget.
   Name any cost up front (a paid API, a developer account).
5. **Has a first lesson that works in one sitting.**

Examples:

| Subject | Project proposals |
|---|---|
| Macroeconomics | A policy simulator in Python on FRED data, one model per lesson (Phillips curve, Taylor rule, IS-LM); or a monthly briefing notebook explaining the latest CPI release |
| Music theory | Harmonise a folk melody, one technique per lesson, ending in a four-part arrangement; or analyse one album's harmony track by track |
| Constitutional law | A casebook on one clause, one landmark case per lesson, ending in a short brief on a pending question |
| Organic chemistry | A mechanism notebook for the reactions in one drug's synthesis, one reaction class per lesson |
| Distributed systems | A key-value store that gains replication, then consensus, then recovery, one property per lesson |

## What stays the same in every lens

The lesson shape, the voice, the plan checklist, the fact-check discipline,
predictions and teach-backs, and the practice queue. If a subject seems to need
something different, write it in `NOTES.md` under `## Lens notes` (notation,
tools, conventions) so every later lesson follows it. A new skill per subject
is not needed; a note per workspace is.
