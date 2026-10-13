# 1. A story owns its tasks, in one file

**Status:** accepted
**Date:** 2026-10-13

## Context

v1 sized a story to one agent context window and one PR. That made stories read like agent work orders: "tenant port," "Postgres adapter." The agent needs small units; the person reading the plan needs units they can see.

## Decision

Two units. A **story** is one change a person can see, with a scenario, a demo, a picture, and acceptance criteria. A **task** is one context window of agent work with the design detail. Tasks live inside their story's file under `## Tasks`, not as separate files or issues.

## Consequences

- Story files get longer; the human part stays at the top.
- One PR per story is the default, which suits review.
- Parallel agents working one story's tasks at once would want tasks as separate files. When that arrives, split them out; the format already names them `T1`, `T2`.
