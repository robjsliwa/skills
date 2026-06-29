---
name: story-decompose
description: >-
  Take a story bible produced by narrative-grill and break its arc into a folder
  of small, individually grillable beat files: acts to beats, one file per beat,
  each pointing back to the bible. This is the to-issues analog for narrative, but
  the file tree is the work-item store instead of GitHub. Use whenever the user
  has a story bible and wants to "break it into beats", "decompose the story",
  "split the arc into pieces", "turn the bible into beat files", or "grill it by
  parts". Trigger after a bible exists and the user wants manageable units to work
  one at a time. The output is a beats/ folder of stub files, each a unit that
  beat-grill later expands. Do not use this to write the story bible itself (that
  is narrative-grill) or to fill a beat's branching dialog (that is beat-grill).
---

# Story Decompose

Take a story bible and explode its structural spine into a folder of small beat
files, one per beat, each a self-contained unit that beat-grill can pick up and
expand on its own. This is the "grill it by parts" step: it turns one big arc into
a sequence of manageable pieces while the bible stays the center that keeps them
coherent.

The bible already did the hard structural work. Decomposition is mostly a faithful
explosion of the bible's numbered spine, plus a light pass with the user on
granularity and act boundaries. It is not a deep interview; do not re-grill the
story. Propose the breakdown in one pass, let the user adjust, then write the
files.

## Step 0: Read the bible

Read the whole story bible first. The numbered **structural spine** is what you
explode. The **flag list** and **factions** travel with each beat as context.
Confirm the bible's layout: by default beat files go in a `beats/` folder next to
the bible. If the user has a different project layout, follow it.

If there is no bible, stop and say so. This skill consumes one; it does not invent
the story.

## Step 1: Propose the breakdown

In a single pass, propose the act-to-beat breakdown drawn from the spine:

- **Acts** group beats; reflect them in the numbering and the file header, not in
  separate folders.
- **Beats** are the unit. One file per beat. Number them in spine order
  (`01-`, `02-`, ...) so a plain sort gives reading order.
- **Scenes** are the finer grain inside a beat. Do not make scene files. List the
  scenes a beat contains as a checklist inside the beat file for beat-grill to
  work through. File equals beat keeps the mapping clean.

Present the proposed list of beat files with a one-line summary each, and ask the
user two light questions, at most: does the granularity feel right (any beat that
should split into two, or two that should merge), and do the act boundaries land
where they expect. Recommend your own answer to both. Then incorporate their
adjustments.

## Step 2: Write the beat files

Write one file per beat into the beats folder, following
`references/beat-file-template.md`. Each file is a **stub**: it carries enough
context to be grilled on its own (its place in the spine, a link back to the
bible, the beat's job, the scenes it contains, and the forks the bible already
named for it), but it does not yet contain the branching dialog. That is
beat-grill's job.

Keep each stub pointing back to the bible by relative path, so anyone opening a
beat file can reach the shared context in one hop. The bible stays the main
context; the beat files are the pieces.

## Step 3: Hand off

Present the beats folder and the list of files. Tell the user the natural next
step is to run beat-grill on the first beat. Do not start grilling beats yourself;
decompose's job ends at the stubs.

## Conventions

- **Faithful, not creative.** Decompose reflects the bible's spine. If you find
  yourself inventing plot, you have drifted into narrative-grill's job; note the
  gap to the user instead and let them decide whether to re-grill the bible.
- **One file per beat.** Resist scene files and status state machines. If a beat's
  later grilled output gets unwieldy, that is the moment to split that one beat
  into a folder, and it is a future refactor, not something to set up now.
- **The tree is the tracker.** There is no issue tracker. The folder and the
  filenames are the work list. You can see what exists by listing the folder.
- **Default to prose. Avoid em dashes.**
