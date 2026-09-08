# Skills

Skills for Claude Code and other AI coding agents. Each skill is a directory with a
`SKILL.md` that the agent loads on demand, either when you type `/<skill>` or when
the agent decides the skill applies.

## Install

```bash
npx skills@latest add robjsliwa/skills
```

Restart Claude Code after installing. The planning loop below also uses a few
skills from Matt Pocock's set:

```bash
npx skills@latest add mattpocock/skills
```

Then, once per repo, run `/setup-matt-pocock-skills`. It writes
`docs/agents/issue-tracker.md`, which tells the loop whether requirements and
stories go to GitHub, GitLab, Jira, or local files.

## The planning loop

Takes one feature from idea to shipped code, one artifact per step. Every artifact
is a file under `docs/planning/<feature-slug>/`, so you can clear context after any
step; the next skill reads the previous artifact from disk.

| Step | Run | Produces |
|---|---|---|
| 1. Align | `/grill-with-docs` | shared understanding; `CONTEXT.md` and ADRs as you go |
| 2. Requirements | `/write-requirements` | `requirements.md` (the WHAT), or a tracker issue |
| 3. Design | `/solution-design` pointed at the requirements | `design.md` (the HOW), `CLAUDE.md` contract, ADRs |
| 4. Phase | `/vertical-slice-phasing` | `phases.md` (the ORDER), walking skeleton first |
| 5. Stories | `/elaborate-current-phase` | stories for the current phase only, via `to-story` |
| 6. Build | `/tdd` pointed at one story | the code; mark the story done |
| 7. Next phase | `/elaborate-current-phase` again | the next phase's stories, re-derived from the real code |

Repeat step 6 until every story in the phase is done, then step 7, until the last
phase ships. Clear context between any two steps and between stories. If you lose
track, `/planning-loop` reads `docs/planning/` and names the next step.

### A session, end to end

```
/grill-with-docs                       # one question at a time until aligned
/write-requirements                    # -> docs/planning/acme-auth/requirements.md
/clear
/solution-design docs/planning/acme-auth/requirements.md
/clear                                 # -> design.md, CLAUDE.md, docs/adr/0007-*.md
/vertical-slice-phasing docs/planning/acme-auth/design.md
/clear                                 # -> phases.md
/elaborate-current-phase docs/planning/acme-auth/phases.md
/clear                                 # -> stories/01-01-*.md, 01-02-*.md, ...
/tdd docs/planning/acme-auth/stories/01-01-tenant-port.md
/clear                                 # repeat per story; flip its Status to done
/elaborate-current-phase docs/planning/acme-auth/phases.md   # phase 2, and so on
```

### Where things go

```
docs/
  planning/<feature-slug>/
    requirements.md      write-requirements      (or a tracker issue / epic)
    design.md            solution-design
    phases.md            vertical-slice-phasing  (Status per phase, traceability table)
    stories/NN-MM-*.md   to-story                (or tracker issues)
  adr/NNNN-*.md          grill-with-docs, solution-design
CONTEXT.md               grill-with-docs (the domain glossary)
CLAUDE.md                solution-design (the agent contract; merged if it exists)
```

If `docs/agents/issue-tracker.md` names a real tracker (GitHub, GitLab, Jira,
Linear), the requirements and the stories are filed there instead of as files.
The design and the phases are always files in the repo. With the local-markdown
tracker, or no setup at all, everything is a file.

### Light path

A single vertical slice with no real design choice does not need the loop:
`/grill-with-docs`, `/to-story`, `/tdd`. Judge by architectural weight, not diff
size. If you cannot name the ports without thinking, or a wrong call now means a
rewrite later, take the full loop.

### Which skill comes from where

| From this repo | From `mattpocock/skills` |
|---|---|
| `write-requirements`, `solution-design`, `vertical-slice-phasing`, `elaborate-current-phase`, `to-story`, `design-interview`, `planning-loop` | `grill-with-docs` (with `grilling` and `domain-modeling`), `tdd`, `setup-matt-pocock-skills`; optionally `code-review` and `implement` |

## Engineering skills

### `write-requirements`

Turns a finished grilling into a template-driven requirements document: the WHAT
and the WHY, never the mechanism. Non-goals, non-functional rows (latency,
durability, trust boundaries, retention), failure modes, and acceptance criteria
are all mandatory, so the dimensions that usually cause rewrites are visibly
present or visibly struck. Requirements are numbered (R1, R2, ...) and every later
artifact references them by id. Refuses to write from a cold start; if no grilling
happened, it sends you to do that first. Publishes to `requirements.md` or the
configured tracker.

### `solution-design`

Turns the requirements into the design document: ports before adapters, the domain
model, data and persistence, the deterministic-versus-probabilistic split, a
stdlib-first dependency policy, designed seams, trust boundaries, a testing
strategy, and the few hard-to-reverse decisions that become ADRs. Invokes
`design-interview` for genuinely coupled decisions instead of guessing. Writes
`design.md` with typed interface sketches, schemas, and diagrams that `to-story`
later carries into each story, and writes or merges `CLAUDE.md`: the agent
contract (stack, layering, persistence and auth rules, public surface, definition
of done) that every story inherits.

### `vertical-slice-phasing`

Runs `design-interview` on build order alone, one sequencing decision at a time,
judged by ten phasing heuristics, and writes `phases.md`. Phase one is a thin
walking skeleton that proves the riskiest claim; every later phase thickens it with
demoable capability. Names the seams placed early so later phases are a swap, not a
rewrite, and maps requirements to phase boundaries twice: as an end-to-end
definition-of-done script, one line per capability, tagged by phase, and as a
traceability table, one row per requirement id, that `to-story` fills with story
ids so a requirement with no story is visible before the phase is built. Each phase
carries a Status line that `elaborate-current-phase` updates.

### `elaborate-current-phase`

Details exactly one phase into stories, through `to-story`, and refuses to detail
the rest. It is also the loop's return arrow: run it again when a phase ships, and
it reads the built code as ground truth, reconciles the next phase against it,
records any drift in `phases.md`, and recommends re-phasing if the drift reaches
later phases.

### `to-story`

The exploder. Slices a phase (or a whole design, on the light path) into
tracer-bullet stories, each a complete vertical slice sized for one PR and one
context window, with blocking edges declared. Unlike a plain ticket, each story
carries its design: interfaces and types, data, algorithm, a Mermaid diagram when a
picture beats prose, a sample-code sketch, the files it touches, a RED-first test
plan, acceptance criteria tied to requirement ids, and verification commands. It
quizzes you on granularity, edges, and any requirement of the phase that no story
serves before writing, then publishes to `stories/NN-MM-<slug>.md` or the
configured tracker and fills the traceability table in `phases.md`.

### `design-interview`

A general one-question-at-a-time interview for any space of coupled decisions.
Every question carries a recommendation, the tradeoff, and the soft spot where you
might overrule it. Tracks what is settled, deferred, and which seams were designed
for later. `solution-design` and `vertical-slice-phasing` call it; you can also run
it on its own for architecture, data-model, or scope questions.

### `planning-loop`

The router. Reads `docs/planning/` and tells you which step to run next. It
points; it never does the step.

### `go-boilerplate`

Scaffolds a new Go REST API service from a fixed boilerplate using Chi,
OpenTelemetry, and Swagger: Go module and router, tracing and metrics wiring,
code-first OpenAPI via swaggo, Makefile, Dockerfile, docker-compose, and a GitHub
Actions workflow.

| Parameter | Required | Default | Description |
|---|---|---|---|
| `project_name` | Yes | | Project name in kebab-case, e.g. `my-service` |
| `github_user` | Yes | | GitHub username or org that will own the repo |
| `description` | Yes | | One-sentence description of the service |
| `dest_dir` | No | `.` | Directory to install the project files into |
| `module_path` | No | `github.com/{github_user}/{project_name}` | Go module path override |

```
Run go-boilerplate with project_name=widget-svc, github_user=acme,
description="Service for managing inventory widgets."
```

Missing required parameters are asked for one at a time. Headless:

```bash
mkdir my-service && cd my-service
claude -p --permission-mode bypassPermissions \
  "Run go-boilerplate skill non-interactively:
   project_name=my-service github_user=acme
   description='Service for tracking certificate lifecycles.'"
```

See `skills/engineering/go-boilerplate/INSTALL.md` for details.

### `let-me-code`

Writes a TDD-structured tutorial (`TUTORIAL.md`) that guides you to type each line
yourself, one RED-to-GREEN cycle per step, with code blocks sized for typing rather
than pasting. Trigger with "teach me to build X" or "don't write the code for me".

## Gamedev skills

Four skills that take a game-story idea and turn it into an authored, branching
story you build one piece at a time while keeping the whole coherent. Story content
lives in git next to the code. The chain is `narrative-grill`, then
`story-decompose`, then `beat-grill` one beat at a time, with `subquest-fill`
branching off once the bible exists.

```
narrative-grill ──► story-bible.md ──► story-decompose ──► beats/*.md
                        ▲   ▲                                  │
                        │   └──────────── beat-grill ◄─────────┘ (one beat at a time)
                        │                     │ appends new flags
                        │
                  subquest-fill ──► beats/subquests/<faction>/*.md
```

### `narrative-grill`

A one-question-at-a-time interview that turns a premise into `story-bible.md`:
premise, theme, world rules, factions, protagonist arc, tone, and a numbered
structural spine, plotted against James Scott Bell's LOCK and two doorways by
default (swappable). The bible also holds the single list of world-state flags.
Name a tone comp up front ("Disco Elysium, but colder") so the recommendations
have an anchor.

### `story-decompose`

Breaks the bible's spine into a `beats/` folder of stub files, one per beat in spine
order, each linking back to the bible. The folder is the work list. Asks at most two
light questions (granularity, act boundaries) and refuses to invent plot; if it would
have to, it tells you to re-grill the bible.

### `beat-grill`

Expands one beat from a stub into full branching content: for each player choice,
which flag guards it and what consequence it writes back, plus the dialog in the
bible's voice. Flips the beat to `Status: grilled` and appends any new flags to the
bible. Usage: `/beat-grill beats/03-first-doorway.md`. One beat per session keeps
each grill small and the dialog consistent.

### `subquest-fill`

Seeds side quests that hang off existing factions and flags, as stubs under
`beats/subquests/<faction>/` in the same shape `story-decompose` produces, so
`beat-grill` expands them with no special case. Skips generic errands that anchor to
nothing.

Three rules hold the chain together: the bible is the center and every skill reads
it first; the `beats/` folder is the pieces; flags have exactly one home, the bible.

## Deprecated

Kept for reference under `skills/deprecated/`. They are not linked by
`scripts/link-skills.sh` and are user-invoked only, so they never fire on their own.

- `init-go-project`: superseded by `go-boilerplate`.
- `phased-implementation-plan`: exploded a whole proposal into a phase/story bundle
  in one pass. Superseded by `vertical-slice-phasing` plus `to-story` via
  `elaborate-current-phase`, which detail one phase at a time. Its `CLAUDE.md`
  contract now comes from `solution-design`; its definition-of-done script from
  `vertical-slice-phasing`.

## Repository layout

```
skills/
  engineering/     planning-loop, write-requirements, design-interview, solution-design,
                   vertical-slice-phasing, elaborate-current-phase, to-story,
                   go-boilerplate, let-me-code
  gamedev/         narrative-grill, story-decompose, beat-grill, subquest-fill
  productivity/    (reserved, none yet)
  deprecated/      init-go-project, phased-implementation-plan
scripts/
  link-skills.sh   symlink every non-deprecated skill into ~/.claude/skills/
  list-skills.sh   list skill directories
```

## License

MIT
