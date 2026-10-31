# Ledger Format

## claims.json

A JSON list, one object per claim, in the order the page makes them.

```json
[
  {
    "id": "C07",
    "kind": "behaviour",
    "text": "Removing @MainActor from CountdownTests makes Swift 6 reject `let countdown = Countdown()`.",
    "where": "lab §5, 'Why @MainActor'",
    "source": "build/run/no-mainactor.txt",
    "status": "verified",
    "evidence": "xcodebuild test: error: main actor-isolated default value in a nonisolated context",
    "checked": "2026-10-28"
  },
  {
    "id": "C12",
    "kind": "quote",
    "text": "SwiftUI updates a view only when an observable property changes and the view's body reads the property directly.",
    "where": "lecture slide 'observe'",
    "source": "https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro",
    "status": "verified",
    "evidence": "sentence matched on the page, fetched 2026-10-28",
    "checked": "2026-10-28"
  },
  {
    "id": "C19",
    "kind": "claim",
    "text": "A paid team's development build never shows the 'untrusted developer' prompt.",
    "status": "unverifiable",
    "note": "Said to the reader as uncertain; no primary source found.",
    "checked": "2026-10-28"
  }
]
```

| Field | Required | Holds |
|---|---|---|
| `id` | yes | `C01`, `C02`, … stable across rebuilds |
| `kind` | yes | one of the kinds below |
| `text` | yes | the claim as the page will make it |
| `where` | no | the section or slide that makes it |
| `source` | when verified | URL, file in `build/`, or `values.json:<name>` |
| `status` | yes | `pending`, `verified`, `failed`, `unverifiable` |
| `evidence` | when verified or failed | what was seen: output line, matched sentence, computed value |
| `note` | when unverifiable | how the page tells the reader |
| `checked` | yes | date |

## How each kind is verified

| Kind | Verified by | Lens examples |
|---|---|---|
| `code` | runs in `build/ref/` with the real toolchain; tests pass; output saved | Swift package builds, Python notebook cell runs |
| `output` | the saved run in `build/run/` contains it verbatim | test log line, compiler error, CLI output |
| `value` | computed by `values.py` and written to `values.json` | a hash, an elasticity, a p-value, a frequency ratio, a count |
| `quote` | the exact words found in the source fetched now, in the named edition | a spec sentence, a court opinion, a letter, a style guide |
| `citation` | the link or reference opened; it says what the page says it says | RFC section, case reporter page, archive item |
| `behaviour` | done for real and the result saved | "the compiler rejects this," "the reaction is exothermic" (from a primary data table) |
| `date` / `fact` | two independent primary or authoritative sources agree | a treaty's date, an author's birth year |
| `claim` | a general statement: reduced to one of the kinds above, or `unverifiable` | "most teams do X" |

A humanities or craft lesson has no code but still has a ledger: quotes,
dates, citations, and analysed examples (a chord progression named in a score,
a structural beat located in a screenplay) are claims with sources.

## values.py

A plain script, standard library plus whatever the subject's tools are, that
recomputes every number the page will quote and writes them to
`values.json` as `{name: value}`. It imports or shells out to the verified
code where it can, so the value comes from the same code the learner will
run.

```python
#!/usr/bin/env python3
"""Every value lesson 2 quotes. Run from build/."""
import json, subprocess

def hint_after(keys):            # runs the verified Swift parser on a prefix
    out = subprocess.run(["swift", "run", "--package-path", "ref/TimerCore", "timersim", "hint", keys],
                         capture_output=True, text=True, check=True).stdout.strip()
    return out

values = {
    "hint_3": hint_after("123"),
    "hint_4": hint_after("1230"),
    "hint_5": hint_after("12305"),
    "zero_trap": hint_after("0000"),
}
assert values["hint_4"] == "Start 12:30", values["hint_4"]
json.dump(values, open("values.json", "w"), indent=2)
print(f"{len(values)} values")
```

Assert the values the lesson's argument depends on, so a change in the code
breaks the build instead of silently changing the story.
