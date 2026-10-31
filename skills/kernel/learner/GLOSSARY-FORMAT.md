# GLOSSARY.md Format (teaching workspace)

`GLOSSARY.md` is the canonical language of a teaching workspace: every lecture,
lab, prompt, and record uses its terms. Building it is part of learning:
compressing an idea into a tight definition is evidence of understanding. (In
a code repo the `glossary` skill owns a different `GLOSSARY.md`, the
product's language. A workspace may render this one as
`reference/glossary.html` for printing; the markdown stays the source.)

## Template

```md
# {Topic} Glossary

{One or two sentences on what the topic covers.}

## {Cluster, e.g. Observation}

**Observable object**:
A class whose stored properties record each read and announce each write, so
SwiftUI knows which views depend on it.
_Avoid_: model object, store, view model
_Added:_ L2, after the learner explained why typing re-runs only DialerView.
```

## Rules

- **Add a term only when the learner uses it correctly**, in their own words,
  not when they first read it.
- **Be opinionated.** Several words for one idea: pick one, list the rest under
  `_Avoid_`.
- **Define what it is**, in one or two sentences, using earlier glossary terms.
- **Flag field ambiguity.** "In this workspace, 'state' always means
  `CallState`; SwiftUI's `@State` is spelled with the `@`."
- **Revise in place** as understanding deepens.
