---
name: test-along
description: 'Write a test guide that lets an independent developer validate code that someone else (or an agent) wrote for one story, from a PR or branch plus a story link. Use when the user says "test along", "write a test guide", "how do I test this story", "how do I validate this PR/branch", "independent verification", or "QA this story", or runs /test-along. Works in any repo and stack. Needs a story (file, Jira, issue, or pasted text) and a PR link or branch per repo.'
argument-hint: "Story link or file, and PR link or branch"
---

# Test Along

Write a **test guide** for one story. The reader is an independent developer who did not write the code and does not trust it yet. The guide helps them prove, from outside, that the story's behaviour exists and works.

This skill depends on no other skill and assumes no stack. You work out how to run the code by reading the repo. This file gives hints and defaults only.

## Inputs

Ask for what is missing, one question at a time, before any work. Do not guess.

1. **The story.** A file path, a URL (Jira, GitHub or GitLab issue, wiki page), or pasted text. Read a URL with whatever tool the harness gives you (`gh`, an MCP connector, a fetch tool). If you cannot read it, ask the user to paste it.
2. **The implementation.** A PR link, or a local branch name, for each repo the story touches. If the story or diff shows more repos, ask for each.
3. **Format.** Markdown or HTML. Default: HTML. If `tech-writer` is available, load it and ask its format and conformance questions (default: "Optimize for brevity"). If it is not available, write short, direct sentences in plain English, with no figures of speech.

## Evidence rules

Build the guide from only:

- the story text: the goal, the acceptance criteria (whatever the story calls them), the demo or scenario, out-of-scope notes, and any test plan it states;
- the source changes: the diff against the base, and the files it adds or changes, read at that ref;
- the repo's build and run files at that ref, quoted so commands are correct.

Do not rely on: the author's notes or journal, the PR description or commit messages as proof of behaviour, status fields or ticked boxes in the story, or design documents. If the story cites a requirement id, copy it as a label only. A guide that repeats the author's claims cannot find the author's mistakes.

If the diff has nothing for a criterion, report a gap. Do not invent a check.

## Procedure

1. **Gather inputs.**
2. **Fetch the change before anything else.** PR: `gh pr view`, `gh pr diff` (or the host's equivalent). Branch: `git diff <base>...<branch>`, `git show <branch>:<path>`. Never switch the user's working branch. To run anything, use a `git worktree` in the scratchpad.
3. **Map change to story.** Table: each criterion, the diff files and tests that deliver it, and a verdict: `covered`, `test only` (a test exists, no way to run the behaviour), or `gap` (nothing in the diff).
4. **Check the test plan, if the story has one.** For each test it names, look for a test with that name or intent in the diff. A missing test is a finding.
5. **Locate the code.** Report which ref holds each part of the story. If it spans refs or repos, test that they combine with `git merge-tree --write-tree <a> <b>`, report conflicts, and give commands for a throw-away integration branch.
6. **Work out how to run it.** See [Finding how to run it](#finding-how-to-run-it).
7. **Derive checks.** For each criterion: the command or UI action, the expected result, and a second, independent way to see the same fact. Observe the system from outside. Do not rely on the author's own test helper as the only check.
8. **Add negative and boundary checks** the diff implies (bad input, repeat request, empty value). Label each "extra check, not an acceptance criterion".
9. **Write the guide** with the sections below.
10. **Verify what you can.** Run tests or the app only if the user allows it. Mark each command `run by author` or `not run`. Never show expected output as observed output.
11. **Save, then report.** Give the user the path, the gaps, and the open questions. Offer to commit or open a PR. Do not do either unprompted.

## Finding how to run it

Assume nothing is running. Read the repo at the ref and decide. Report every run path the repo supports, and say what is missing. Hints, not rules:

| Signal in the repo | Likely means |
| --- | --- |
| `README` run or "getting started" section | Start here. It is the repo's own statement. |
| `Makefile`, `justfile`, `Taskfile`, `package.json` scripts, `pyproject` scripts, `build.gradle`, `pom.xml` | Named build, test and run commands |
| `docker-compose*.yml`, `compose.yaml`, `Tiltfile`, `skaffold.yaml`, Helm or k8s manifests | Local multi-service stack |
| `.env.example`, config templates | Variables the tester must set |
| CI files (`.github/workflows`, `.gitlab-ci.yml`) | The commands that build and test, with versions |
| `Dockerfile`, `devcontainer.json` | A reproducible environment |
| OpenAPI or schema files, route definitions | Endpoints to call |
| Storybook, dev server config, mobile project files | UI or app to open |
| No run files, only a library | Test through a small script or the test suite |

Rules:

- Adapt the guide to the project type: service (start, health check, call, stop), CLI (build, run with arguments), library (test suite plus a small consumer script), UI (start dev server, steps to click), job or pipeline (trigger, inspect output).
- If the repo has several run paths (for example Compose and Tilt), write one tab for each. If it has one, write one section.
- Quote commands from the repo. If you must infer a command, mark it `inferred` and name the file you inferred it from.
- Name each external dependency (database, queue, secret, account) and how the tester gets it.
- If the code cannot run from the given refs, say exactly why and which ref or file is missing.

## Guide sections

Use this order. If a section does not apply (for example no stack for a library), keep the heading and write one line saying why.

1. **What you test.** One paragraph. One Mermaid sequence diagram of the happy path.
2. **Where the code is.** Table: repo, branch or PR, parts of the story it holds. A warning box if no single ref holds everything.
3. **Prerequisites.** Tools and versions, credentials, free ports, repos to clone.
4. **Prepare.** Check out refs. Clean old state (generated files, local databases, volumes, caches).
5. **Automated tests.** Command per repo, expected result, named tests to find. Warn that tests can skip when a dependency is down, and show how to count skips.
6. **Run it.** Start, check, stop. Tabs when there is more than one run path.
7. **Run the end-to-end check.** Command or steps per path. Expected output, with the lines that matter.
8. **Acceptance checklist.** Table: tick box, criterion, requirement id (label), how to see it. Long checks go in collapsible details.
9. **Coverage gaps.** Criteria with no code. Plan tests that are missing. Story and code disagreements.
10. **Out of scope.** What the story does not do, so the tester does not report it as a defect.
11. **Troubleshooting.** Symptom and fix, from what the config shows.
12. **Clean up and report.** Teardown commands. What to send back (outputs, refs, logs).

## Output rules

- Save where the repo keeps planning docs. If the story lives in `docs/planning/<feature>/stories/`, save to `docs/planning/<feature>/test-guides/`. Otherwise use `docs/test-guides/`. If the repo has no `docs/` folder, ask. Name: `<story-id>-<slug>-test-guide.<ext>`.
- Open with: "Written for: an independent developer who did not build this story."
- Link to the story: a relative path for a file, the URL for a ticket.
- Every command must be copy-pasteable from the directory the guide names.
- HTML guides are self-contained, work in light and dark themes, and have collapsible sections, tabs for alternative run paths, and copy buttons. Start from [guide-template.html](./references/guide-template.html). Delete parts that do not apply.
- Do not change source code, tests, run files or the story. The skill only reads, and writes the guide.

## Honesty rules

- Do not say a check passes unless you ran it. Write `not run`.
- Do not trust the story's status. If it disagrees with the code, report it.
- Report story and code disagreements as findings: a criterion with no code, a plan test that is missing, a command in the story that the repo does not have.

## Anti-patterns

- Reading the author's journal, notes or PR description as evidence.
- Copying acceptance criteria as if they were checks. A check has a command or action and an expected result.
- Treating a skipped test as a pass.
- Testing only through the author's helper script.
- Writing the guide before fetching the change.
- Assuming the stack (Make, Docker, Tilt) instead of reading the repo.
- Showing expected output as if it was observed.
- Switching the user's working branch.

## Worked example 1: web service, Jira story, one PR

User: "/test-along PAY-212, PR https://github.com/acme/pay/pull/41, use defaults."

1. Read PAY-212 with the Jira connector. Four acceptance criteria.
2. `gh pr diff 41` shows a handler and two tests. Map: three `covered`, one `gap` (retry after failure).
3. The ticket lists test `TestRefundIdempotent`. It is not in the diff. Record a finding.
4. The repo has `compose.yaml` and a README "Run locally" section, but no `Tiltfile`. Write one Compose section and say Tilt is absent.
5. Save `docs/test-guides/PAY-212-refund-webhook-test-guide.html`. Report the gap and the missing test.

## Worked example 2: CLI plus library, two branches

User: "/test-along story file `stories/01-05-rotate-keys.md`. `lib`: branch `feat/keys`. `cli`: branch `feat/rotate`."

1. Read the story. Run `git diff main...<branch>` in each repo. The library holds key generation. The CLI holds the `rotate` command.
2. Run `git merge-tree --write-tree` for the refs. Add a warning box: the CLI needs the library branch. Give the commands to build the integration branch in a throw-away clone.
3. The CLI repo has a `package.json` script `build` and no compose files. Write build, run (`./bin/cli rotate --dry-run`) and cleanup steps. Mark them `inferred` if only CI shows them.
4. Check each criterion with the CLI output and a second observation (`openssl` on the key file). Mark all `not run`.
