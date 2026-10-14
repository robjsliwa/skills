# 4. Research lives in files, not tickets

**Status:** accepted
**Date:** 2026-10-14

## Context

A ticket-per-question research map turns brainstorming into backlog
administration: every unknown becomes an issue the moment it is named, links pile
up as `#42, #43`, and nothing shows how the questions relate.

## Decision

A research trail is a folder in the repo, `docs/research/<topic>/`, with one
`map.md` (index plus a Mermaid tree of node states) and one file per node. A
tracker issue is optional and only mirrors the map with a link to it. Nothing in
a trail is a ticket.

## Consequences

- The map renders on GitHub and in the docs viewer, and diffs show how the
  thinking moved.
- Concurrent sessions on one trail have to coordinate through git, not tracker
  assignment. Trails are usually one person and one agent, so this is acceptable.
- Work that comes out of a trail becomes tickets later, through the planning or
  light loop, once it is buildable.
