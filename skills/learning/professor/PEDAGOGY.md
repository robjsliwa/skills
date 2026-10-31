# Pedagogy

What the learning-science evidence says, and the rule each finding becomes in
this skill. Each section is short on purpose: the finding, the source, the
rule. The sources are primary papers or their authors' own summaries; read
them when a rule seems wrong for a case.

## 1. Organise around a real task

**Finding.** Instruction works best when it is organised around authentic
problems that grow from simple to complex, with knowledge activated,
demonstrated, applied, and integrated in that context: Merrill's first
principles ([Merrill 2002](https://doi.org/10.1007/BF02505024),
*ETR&D* 50(3), 43–59). The 4C/ID model builds whole courses the same way:
whole learning tasks, with supportive information, procedural information,
and part-task practice arranged around them
([van Merriënboer, Clark & de Croock 2002](https://doi.org/10.1007/BF02504993)).

**Rule.** Every course has a project, and every lesson is one milestone of it.
The lecture exists to make the lab make sense. Supportive information (the
mental model) goes in the lecture; procedural information (exact steps) goes
in the lab, at the moment it is needed.

## 2. Start from what they know

**Finding.** Activation of prior knowledge is a first principle (Merrill
2002). Effective teachers open with a short review of earlier material
([Rosenshine 2012](https://www.aft.org/sites/default/files/periodicals/Rosenshine.pdf),
*American Educator* 36(1), principle 1).

**Rule.** Each session opens with due practice prompts. Each lecture's second
slide recalls where the last lesson left off. New ideas are anchored to the
domains in `MISSION.md`'s Anchors ("in Go you would…"), then the professor
says where the analogy breaks.

## 3. Working memory is small: one new idea at a time

**Finding.** Novel information is processed by a working memory that is
limited in capacity and duration; instruction that adds unnecessary load
hinders learning ([Sweller, van Merriënboer & Paas 2019](https://doi.org/10.1007/s10648-019-09465-5),
*Educational Psychology Review* 31, 261–292). Present new material in small
steps and check understanding after each (Rosenshine 2012, principle 2).
People learn better when extraneous material is left out (coherence) and when
they already know the names and characteristics of the key concepts
(pre-training) ([Mayer 2020](https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf)).

**Rule.** One idea per lesson, one idea per slide, one new action per lab
step. Edge cases, version trivia, and spec history are deferred: to an Under
the hood box after the step that meets them, to a challenge, or to a later
lesson. The plan's parking lot lists each one and where it went. Names the
lab will use are introduced in the lecture first.

*Seen in the teach-me lesson this skill replaces:* actor-isolation defaults,
package deployment targets, number-format rules, and an observation quirk
all arrived inside the explanation of `@Observable`, before any code existed.

## 4. Worked examples first, then fade the help

**Finding.** Novices learn more from studying worked examples than from
solving the same problems; as knowledge grows, the advantage reverses, and
guidance that helps novices hinders more experienced learners (the expertise
reversal effect, [Kalyuga, Ayres, Chandler & Sweller 2003](https://doi.org/10.1207/S15326985EP3801_4),
*Educational Psychologist* 38, 23–31). Model a task before asking learners to
do a similar one, and remove scaffolds as competence grows (Rosenshine 2012,
principles 4, 5, 8).

**Rule.** Each lecture walks one worked example end to end (a trace, a
derivation, an annotated passage) before the lab asks the learner to do the
same. Guidance fades across the course: early labs give every line; later labs
give the goal, the test, and hints in collapsed boxes. The learning records
decide the level, not the lesson number.

## 5. Concrete, then picture, then abstract

**Finding.** Instruction that starts with concrete materials and explicitly,
gradually fades to abstract ones combines the benefits of both: concrete
grounding helps learners interpret abstract symbols, and fading helps them
drop irrelevant detail and transfer
([Fyfe, McNeil, Son & Goldstone 2014](https://doi.org/10.1007/s10648-014-9249-3),
*Educational Psychology Review* 26, 9–25).

**Rule.** Every idea arrives in this order: a specific case with real values
(the stale `isValid` flag, after ten keys and after one backspace), then a
picture of the structure, then the name and the general rule ("store the
cause, compute the effect"). A trace is never shown before the thing it
traces.

*Seen in the teach-me lesson:* key-by-key trace tables and an observation
loop for a class the reader had not yet been shown.

## 6. Pictures and words, together, in learner-paced pieces

**Finding.** Mayer's principles: people learn better from words and pictures
than from words alone; when corresponding words and pictures are near each
other and presented together; when cues highlight the organisation of the
essential material (signalling); from learner-paced segments rather than a
continuous unit; and from a conversational rather than formal style (Mayer
2020).

**Rule.** The lecture is a deck: one picture per slide, built in steps, with
the transcript paragraph for each step appearing with it. The canvas carries
almost no prose. Colour has fixed meanings. The learner advances; nothing
auto-plays. The transcript is conversational (VOICE.md).

## 7. Make the learner generate

**Finding.** Learning increases as engagement goes from passive to active to
constructive to interactive: producing ideas beyond the material (explaining,
predicting, comparing) beats receiving or merely manipulating it
([Chi & Wylie 2014](https://doi.org/10.1080/00461520.2014.965823),
*Educational Psychologist* 49(4), 219–243). Prompting learners to explain to
themselves has an average effect of g = 0.55 across 64 studies, and
self-explanation beat explanations given by an instructor; formats where
learners pick an explanation from a list showed the weakest effects, though
the authors note that evidence on format is limited
([Bisra et al. 2018](https://doi.org/10.1007/s10648-018-9434-x)).

**Rule.** The learner produces something at every stage: a prediction at each
predict slide, a result at each lab checkpoint, an answer to each challenge,
a teach-back at the debrief. The chat makes the interactive mode cheap: the
professor responds to what the learner actually said.

## 8. Let them try before telling, then tell well

**Finding.** A meta-analysis of 53 studies found that problem solving followed
by instruction outperformed instruction followed by problem solving for
conceptual knowledge and transfer, more so for secondary and university
students than for primary students, which the authors attribute partly to
prior knowledge ([Sinha & Kapur 2021](https://doi.org/10.3102/00346543211019105),
*Review of Educational Research* 91(5)). Unsuccessful retrieval attempts,
followed by the answer, enhance learning ([Kornell, Hays & Bjork 2009](https://pubmed.ncbi.nlm.nih.gov/19586265/)).
The evidence is not uniform: prequestions before a lesson did not help in one
live STEM classroom ([Geller et al. 2017](https://doi.org/10.1186/s41235-017-0078-z)).

**Rule.** Predict slides come *before* the reveal, and the answer always
follows at once. For a learner whose records show solid prerequisites, the
hook can be a short problem to attempt before the mechanism is taught. For a
true novice, keep attempts small and the worked example close (section 4).
Never leave a learner's wrong prediction without the correct answer and why.

## 9. Retrieve, spaced over time

**Finding.** Of ten common learning techniques, practice testing and
distributed practice received the highest utility ratings
([Dunlosky et al. 2013](https://doi.org/10.1177/1529100612453266),
*Psychological Science in the Public Interest* 14(1), 4–58). The best gap
between study sessions grows with how long the learning must last
([Cepeda et al. 2006](https://doi.org/10.1037/0033-2909.132.3.354),
*Psychological Bulletin* 132(3), 354–380). Weekly and monthly review is a
principle of effective instruction (Rosenshine 2012, principle 10).

**Rule.** `PRACTICE.md` holds open prompts for each central idea, due at later
lessons, with gaps that grow when answers are solid and shrink when they are
not (the `learner` skill's PRACTICE-FORMAT.md). Sessions open with them.

## 10. Feedback, and why there is no multiple-choice quiz

**Finding.** With corrective feedback, an intervening short-answer test led to
the best final-test performance, ahead of multiple-choice and of re-reading;
without feedback, multiple choice did better than short answer
([Kang, McDermott & Roediger 2007](https://doi.org/10.1080/09541440601056620),
*European Journal of Cognitive Psychology* 19(4/5), 528–558). That is one
laboratory study, not a law: well-built multiple-choice questions can also
produce retrieval benefits. The point is narrower: when feedback is cheap,
producing the answer is at least as good, and usually better.

**Rule.** Feedback is always available here, in chat, so every check is open
response: the learner writes the prediction, the answer, the explanation, and
gets a reply to what they wrote. A quiz at the end of a page is taken
minutes after the lesson; the practice queue asks again lessons later, which
is where spacing (section 9) does its work.

## 11. Check understanding, aim for high success

**Finding.** Effective teachers check understanding often, and aim for a
success rate around 80% before moving on (Rosenshine 2012, principles 6, 7).

**Rule.** If the learner gets most predictions wrong, stop before the lab:
reteach the model with a second example, and record the misconception. If
they get everything right easily, say so and move faster next time (section 4).

## 12. Integrate: carry it into their world

**Finding.** Learners integrate new knowledge by applying it in their own
context, reflecting on it, and explaining it to others (Merrill 2002).

**Rule.** Challenges apply the idea to a new case or to the learner's own
project. The debrief asks for the idea in their words, applied to what they
built. The lesson's one sentence to carry forward ends the lab.

---

## Plan checklist

Run against `plan.md` before building anything. Every line must pass.

- [ ] The objective is one observable thing the learner will be able to do,
      and it serves the mission.
- [ ] The prerequisites are in the learning records, or the plan says how the
      lecture covers them (or the lesson moves later).
- [ ] There is exactly one new idea, and it fits in one sentence.
- [ ] The hook is concrete: a real failure, puzzle, or case with real values.
- [ ] The model is introduced concrete → picture → name.
- [ ] The anchor maps the idea onto something in `MISSION.md`'s Anchors and
      says where the analogy breaks.
- [ ] One worked example runs end to end, with verified values.
- [ ] There are two or three predict points, each with its answer.
- [ ] Nothing is traced, named, or used before it is shown.
- [ ] The lab's first step gets the workspace running; every step has an
      expected result; the milestone is something the learner can run or show.
- [ ] Every edge case and aside is in the parking lot with its destination.
- [ ] Guidance level matches the records (section 4).
- [ ] The teach-back question and the practice prompts are written.
- [ ] Every fact has a source in `RESOURCES.md` or `research/`.
