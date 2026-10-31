# The Security axis

These skills run on more than one agent, so the axis cannot assume any one
tool. It is a fixed slot in the review, filled from the best source available.
Read `Review / Security` in `docs/agents/profile.md`; a missing profile or
field means `auto`.

| Value | What fills the axis |
|---|---|
| `auto` | The agent's own security review, if it has one you can invoke, such as Claude Code's `/security-review`. Otherwise the built-in brief below. |
| A command or skill | Run it, then give its output to the built-in brief as evidence, in the same sub-agent. |
| `off` | Nothing. The report says `Security: off by profile`, so nobody reads silence as a pass. |

Whatever the source, the sub-agent reports in the review's own shape: `X1..`,
with file and line. The findings then go through verification and tagging like
any other axis, so a tool's false positives get the same check.

**Using a host's review or a scanner:**

- It may pick its own base, or scan the whole repo. Keep only what falls in the
  pinned diff; a hit elsewhere is reported only if this change makes it
  reachable.
- If it cannot be run (not installed, not logged in, fails), fall back to the
  built-in brief and name the failure in the report. A broken tool must never
  read as a clean result.
- Name the source in the report: `Security: /security-review`, or
  `Security: built-in brief, semgrep 1.x`.

## The built-in brief

Give this to the Security sub-agent along with the diff commands.

> Review this diff as someone trying to abuse it. Trace untrusted input (HTTP,
> files, env, queue messages, tool or model output) from where it enters to
> where it is used, reading code outside the diff when the trail leaves it. Look
> for:
>
> 1. **Injection:** SQL, shell, template, path traversal, deserialization of
>    untrusted data, prompt injection into an agent with tools.
> 2. **Access:** a missing or weakened authentication or authorization check, a
>    new route or tool with none, one user reaching another's data.
> 3. **Secrets:** credentials in code, config, logs, or error messages.
> 4. **Data exposure:** sensitive fields in logs, responses, or client code.
> 5. **Crypto:** home-made crypto, weak algorithms, disabled certificate checks,
>    predictable tokens.
> 6. **Dependencies:** a new package that is unpinned, unmaintained, or does more
>    than this change needs.
> 7. **Unsafe defaults:** permissive CORS, debug modes, a check that fails open.
>
> Report only what you can trace: where the input enters, where it does harm,
> and what an attacker gets. Skip theoretical hardening and anything that needs
> an attacker who already owns the machine. Say what you checked if you found
> nothing.
