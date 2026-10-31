# Structure profiles

The plot framework narrative-grill uses is swappable. The skill reads three things
from whatever profile file is active and is otherwise framework-agnostic:

1. **Spine ordering** — the order to grill the structural beats of the main quest.
2. **Required beats** — the named beats the spine must contain.
3. **Structural checklist** — the prose conditions to check before writing the
   bible.

The default is `bell.md`. To add another framework (Save the Cat, the Hero's
Journey, Yorke's five-act), drop a new file here that supplies those three
sections. No change to SKILL.md is needed; the user selects it by name, or the
skill falls back to Bell.

When writing a profile, encode the framework's method and vocabulary and cite its
source. Do not reproduce the source author's prose.
