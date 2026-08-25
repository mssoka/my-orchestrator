# Briefing — righttenantry-analytics-568-617 (issues #568 + #617 — OAuth signup analytics: attribution + remaining instrumentation)

- **Job id:** `righttenantry-analytics-568-617`
- **Repo:** RightTenantry · **Base:** `develop` @ latest head (Silas resolves the exact
  sha at dispatch; RT board is clean — no sibling RT work in flight) · **Slug:** `analytics-568-617`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (analytics/attribution + marketing-consent surface —
  consent-relevant gating, behavioral change; consistent with the consent-compliance
  precedent).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr righttenantry-analytics-568-617 <url>` yourself — the pr field does NOT
  self-populate from a status note.
- **CI:** green. Full local suite must pass (`make test-all`).

## Mission — fix issues #568 and #617 in ONE PR (read both issues in full first — the issues ARE the spec)

**Baseline first (critical — do NOT duplicate shipped work):** PR #583 (merged)
already fixed the counting gap — `complete_oauth_flow` now fires `identify` +
`signup_completed` / `login_succeeded`, so Google OAuth signups ARE visible in
PostHog. VERIFY that baseline is on develop before you touch anything; your work is
the remaining attribution + instrumentation, not re-firing events.

### Part A — #617: OAuth signups lose first-touch attribution (priority: high)

**The bug:** first-touch (`first_touch_*`, #466) is captured client-side — the SPA
lifts `utm_*` / `gclid` / `fbclid` off the landing URL at init and holds them in
memory. The Google OAuth flow is a full-page redirect to accounts.google.com and
back, which destroys that in-memory state before the callback fires →
`complete_oauth_flow` writes an empty first_touch (every field `""`). Every OAuth
signup reads as unattributed; the paid-conversion story stays understated.

**The fix (issue's preferred option — implement it unless you find a blocker with
evidence):** a **short-lived cookie set before the OAuth bounce**, read back in
`complete_oauth_flow` (server-side; no consent required — same basis as #466's
URL-param capture). The PKCE `state` param is the documented alternative if the
cookie fights the redirect flow. On the created (and login) branch, write
`first_touch_*` from the recovered params; when first-touch is absent, record what
exists (e.g. `provider=google`) rather than all-empty strings.

### Part B — #568 (remaining scope after #583): the pieces the counting fix left open

1. **Meta CAPI dispatch on OAuth signup** — mirror the password path's
   `dispatch_signup_meta` from `complete_oauth_flow`'s **created** branch (the upsert
   knows inserted vs conflicted; fire only on insert), gated on marketing consent
   per Plan §5. Find the plan (likely in `docs/` or `_bmad/` — cite it in the PR).
2. **The two auto-create paths** — `login_auto_create_landlord` (auth_handler.gleam
   ~L514) and the session-middleware auto-create (~L98): decide deliberately whether
   they are a true first signup (fire) or a backfill for an already-counted account
   (don't fire). The issue's steer: auto-create implies the Supabase auth user
   already existed → likely DON'T fire — but log/metric the decision either way and
   state it in the PR body.
3. **Fire-once contract verification** — a new Google sign-in produces exactly ONE
   `signup_completed` with an identifiable person; a returning sign-in (upsert
   conflict) fires none; the password path is unchanged (still exactly once).

**Acceptance:**

1. #617: a Google OAuth signup lands with `first_touch_*` populated from the landing
   URL (or provider=google when absent); the cookie is short-lived + cleaned up.
2. #568: Meta CAPI fires on OAuth signup insert (consent-gated); auto-create paths
   decided + logged; fire-once contract verified (new → once, returning → none,
   password unchanged).
3. Tests: add/extend Gleam tests for the cookie round-trip + the fire-once contract
   where the harness allows; full local suite green (`make test-all`).
4. PR body carries: the baseline-verification note (#583 present), the cookie-vs-state
   decision + why, the auto-create decision + evidence, Plan §5 citation, and the
   fire-once evidence.

**Scope guard:** analytics/attribution ONLY. No changes to the OAuth flow itself
beyond the cookie round-trip, no UI changes, no consent-banner changes, no schema
changes (a cookie needs no DB).

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: analytics-568-617
base: develop
model: deepseek/deepseek-v4-flash
pr_review: 1
github_issue: 568
```
