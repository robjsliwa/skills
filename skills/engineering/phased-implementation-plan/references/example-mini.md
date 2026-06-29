# Example: a tiny worked phase

This is a short illustration of what one phase + one story file looks like, so the pattern is concrete. The hypothetical proposal is for a URL shortener service called "shrt" — small enough to fit on a page.

## Hypothetical proposal excerpt

> shrt is a URL shortener with per-user namespaces. Users authenticate via API key. Short links can be created via REST or CLI. Lookups happen via a public redirect endpoint.

## Hypothetical MVP scope

- A user can create an API key (one per user, returned once).
- The user can create short links via CLI: `shrt create <url>` returns `https://shrt.example/<slug>`.
- The redirect endpoint resolves the slug to the URL with a 302.
- All data is per-user-isolated.
- No analytics, no expiry, no custom slugs in MVP.

## Phase 2 README example

```markdown
# Phase 2 — Short link CRUD

## What this phase delivers

By the end of Phase 2, an authenticated user can create, list, and
delete short links from the CLI. The redirect endpoint resolves a
slug to the original URL.

This phase introduces:

- The `Link` domain type and its Postgres repository.
- `POST /v1/links`, `GET /v1/links`, `DELETE /v1/links/{slug}`.
- The public `GET /{slug}` redirect endpoint (no auth required).
- `shrt create`, `shrt list`, `shrt delete` CLI commands.

## Why this ordering

- 02-01 puts the domain and repo in place. Tests can exercise storage
  in isolation.
- 02-02 wires REST. After this story, the API works end-to-end with
  curl.
- 02-03 adds the CLI as a thin client over the REST API. Same code
  path as a third-party would use.
- 02-04 adds the public redirect endpoint. Out of order alphabetically
  but it's the demo moment — it's the user-facing payoff for the phase.

## Stories

| ID    | Title                            |
|-------|----------------------------------|
| 02-01 | Link domain and Postgres repo     |
| 02-02 | Link REST API                     |
| 02-03 | CLI: create, list, delete         |
| 02-04 | Public redirect endpoint          |

## Exit criteria

- [ ] All story-level criteria met.
- [ ] End-to-end script: create a link via CLI, hit the redirect URL,
      get a 302 to the original URL.
- [ ] Two users can't see each other's links via the API or CLI.

## Out of scope (deferred)

- Custom slugs — post-MVP.
- Click analytics — post-MVP.
- Link expiry — post-MVP.
- Rate limiting on the redirect endpoint — Phase 4.
```

## Phase 2 story-02-04 example

```markdown
# Story 02-04 — Public redirect endpoint

## Narrative

The user's payoff for the whole phase: paste a short link in a
browser, land on the original URL. This is the only public,
unauthenticated endpoint in the API surface.

We keep it dumb on purpose. No click tracking, no rate limiting, no
custom error pages. Phase 4 will revisit hardening; for MVP a clean
302 is enough.

## Pre-requisites

- 02-01 (domain + repo) complete.

## Description

`GET /{slug}` resolves a slug to its target URL.

Behaviour:

- Slug found → 302 with `Location: <target>`.
- Slug not found → 404 with a minimal HTML body
  (`<h1>Not Found</h1><p>This short link doesn't exist.</p>`).
- Slug malformed (non-alphanumeric, longer than 16 chars) → 404.
  Don't leak whether a slug *could* exist.

The endpoint is mounted on the same router as the API but with no
auth middleware. All other routes still require auth — be careful
to scope this exemption tightly.

`internal/adapters/primary/http/redirect.go`:

```go
func (h *Handler) Redirect(w http.ResponseWriter, r *http.Request) {
    slug := chi.URLParam(r, "slug")
    if !validSlug(slug) {
        http.Error(w, notFoundHTML, http.StatusNotFound)
        return
    }
    link, err := h.repo.LookupBySlug(r.Context(), slug)
    if errors.Is(err, ports.ErrNotFound) {
        http.Error(w, notFoundHTML, http.StatusNotFound)
        return
    }
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    http.Redirect(w, r, link.TargetURL, http.StatusFound)
}
```

The `validSlug` regex is `^[a-zA-Z0-9]{1,16}$`.

## TDD plan

1. **Redirect_KnownSlug_302WithLocation** — insert a link, GET the
   slug, response is 302 with the right Location.
2. **Redirect_UnknownSlug_404HTML** — GET `/notreal`, response is
   404 with the HTML body.
3. **Redirect_MalformedSlug_404** — GET `/has spaces`, response is
   404 (not 400). Don't leak validity.
4. **Redirect_NoAuthRequired** — request has no Authorization header;
   request still succeeds.
5. **AuthenticatedRoutes_StillRequireAuth** — a request to
   `/v1/links` without auth still fails. Ensures the unauth exemption
   for the redirect didn't bleed.

## Implementation hints

- Mount the redirect on the root router *after* the `/v1/*` subrouter
  is mounted with auth middleware. chi's routing is precise enough
  that `/v1/...` won't be caught by `/{slug}`.
- Use `http.StatusFound` (302), not 301. Permanent redirects are
  cached aggressively by browsers and we want flexibility to change
  the target later.
- The Postgres lookup uses an index on `slug` (created in 02-01) —
  verify the index exists before merging this story.

## Acceptance criteria

- [ ] All 5 tests pass.
- [ ] `GET /{slug}` works end-to-end for a known link.
- [ ] Unknown slug returns 404 with HTML body.
- [ ] Authenticated routes are unaffected.
- [ ] No new lint errors.

## README updates

Add to top-level README under "How it works":

> Short links resolve via `GET /{slug}` on the public root path. No
> auth is required for redirects; the link itself is the credential.

## Verification

```bash
go test ./internal/adapters/primary/http/... -count=1

# End-to-end
shrt login
SLUG=$(shrt create https://example.com -o slug)
curl -sI http://localhost:8080/$SLUG
# Expect: HTTP/1.1 302 Found  +  Location: https://example.com
```
```

## What this example demonstrates

- The phase README is short (40 lines) but covers all five required sections.
- The story file is around 90 lines — on the lower end for a story, because the work is mechanically simple. A more complex story (DAG executor, OAuth flow) would be 250–350 lines.
- The TDD plan has 5 tests in a sensible order — happy path first, edge cases next, regression test last.
- "Implementation hints" is short and only includes things the agent might miss.
- Verification has both a unit-test invocation and an end-to-end smoke that produces visible output.
- The narrative names what's deliberately omitted ("no click tracking, no rate limiting"). This prevents the agent from inventing scope.

When you write a real plan, follow this shape but expect the substance to be deeper. The Faktotum plan that motivated this skill has stories that are 250–450 lines because the underlying work — DAG execution, OAuth device flow, OPA policy integration — is substantively complex. The shape is the same; the length scales with the actual work.
