# MISSION.md Format

`MISSION.md` lives at the workspace root. It holds the reason the learner wants
this and where they are starting from. Every teaching decision (what comes
next, which project, which analogy, how much to explain) traces back to it.

It is the same file `teach-me` writes, plus one section, `## Starting point`,
which a teaching skill fills from the intake and keeps current.

## Template

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal. What changes in their life or
work when they have this? Push past "to understand X" to the outcome.}

## Success looks like
- {A specific, observable thing the learner will be able to do}
- {Another}

## Starting point
- **Knows well:** {what they can already do, with depth: "writes Go daily,
  goroutines and channels in production"}
- **Knows a little:** {"read about actors once"}
- **New:** {"never used Xcode"}
- **Anchors:** {familiar domains to borrow analogies from: Go, cooking, chess}

## Constraints
- {Time per session, budget, hardware, preferences: "evenings, 45 minutes",
  "has a Mac and an iPhone", "prefers reading code to watching"}

## Out of scope
- {Adjacent topics they do not want to chase now}
```

## Rules

- **One mission per workspace.**
- **Concrete over abstract.** "Make calls from my own iPhone app over Twilio"
  beats "learn iOS."
- **Push back on vagueness.** If the learner cannot say why, interview them
  before writing anything. A bad mission is worse than none.
- **Starting point comes from the learner.** Ask; do not infer from their job
  title. Update it when a learning record shows the floor moved.
- **Anchors are for analogies.** The professor maps new ideas onto these
  first, then says where the analogy breaks.
- **Keep it to a screen.** Past that it has become a plan; the plan is
  `SYLLABUS.md`.
