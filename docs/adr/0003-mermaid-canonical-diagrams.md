# 3. Mermaid in the artifact is the canonical diagram

**Status:** accepted
**Date:** 2026-10-13

## Context

Browser-based brainstorming tools show helpful pictures, but they are throwaway HTML that never reaches the spec. Pictures that matter should be reviewable in a PR and live next to the words they explain.

## Decision

Every diagram is a Mermaid block inside the markdown artifact it belongs to. C4 levels 1 to 3 are drawn as flowcharts with a shared class definition block, because Mermaid's native C4 types are experimental, fixed in style, and have no layout control. Wireframes are HTML mockup sidecars under `mockups/`, and a Mermaid screen flow linking to them is the canonical record.

## Consequences

- GitHub renders every diagram in place; diffs show diagram changes.
- Wireframes are low fidelity by design.
- The agent needs `mmdc` to validate; without it, diagrams are marked unvalidated.
