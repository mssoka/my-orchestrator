# Briefing: righttenantry-oauth-posthog-fix

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`oauth-posthog-fix` worktree, branch `oauth-posthog-fix`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders). Review pass: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes.
- **Model policy:** `deepseek-v4-flash` (kimi walled until 08-08T21:57Z).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start.
- **Perkins:** `pr_review: true`.

## Mission (Gru-diagnosed root cause)

The Google OAuth callback path is **missing PostHog tracking entirely** — landlords who sign in via Google are invisible in analytics. The email/password login path has full PostHog integration (identify + capture); the OAuth path has none.

## The three gaps (verified in code by Gru)

### Gap 1: No `posthog` parameter in the OAuth callback chain

```
handle_oauth_callback(req, db, config, sentry, resend_api_key)
// ↑ no `posthog` param — compare with handle_login which HAS it
```

The OAuth callback chain (`handle_oauth_callback` → `process_oauth_callback` → `complete_oauth_flow`) never receives a PostHog client. Thread it through from the router, the same way `handle_login` gets it.

### Gap 2: No server-side identify or event capture

The email/password signup path (line ~258) does:
```gleam
posthog_client.identify_with_set_once(posthog, row.id, [#("email", ...)], attribution.first_touch_set_once(...))
posthog_client.capture(posthog, row.id, "signup_completed", [])
```

The OAuth `complete_oauth_flow` (line ~1080+) does **nothing** — no identify, no capture. Mirror the email/password path:
- `identify_with_set_once` with the landlord's `row.id` + email + first-touch attribution
- `capture` a `signup_completed` (first OAuth sign-in) or `login_succeeded` (returning OAuth sign-in) event — check `welcome.maybe_send_welcome`'s first-time logic to distinguish

### Gap 3: 10-second identify cookie may expire before the SPA reads it

The OAuth path's only tracking mechanism is `set_landlord_identify_cookie` (a 10s cookie the SPA reads post-redirect). On a cold JS load (>10s), the cookie expires first and the client-side `$identify` never fires. With the server-side identify (Gap 2 fix), this becomes belt-and-braces rather than the sole mechanism — but still extend the cookie lifetime or have the SPA check it synchronously on first load.

## Requirements

1. Thread `posthog: PostHog` through the router → `handle_oauth_callback` → `process_oauth_callback` → `complete_oauth_flow`.
2. In `complete_oauth_flow`, after the landlord is created/found: call `posthog_client.identify_with_set_once` (same pattern as email/password) + `capture` the appropriate event (`signup_completed` for first OAuth sign-in, `login_succeeded` for returning).
3. Extend the identify cookie lifetime (or note in the PR why the server-side identify makes the cookie non-critical).
4. Verify: the anonymous-to-identified merge works — a user who browses anonymously, then signs in via Google OAuth, has their pre-login events merged with their landlord ID in PostHog.

## Acceptance

- OAuth Google sign-in fires server-side PostHog `identify` + event capture (same as email/password).
- The router passes `posthog` to the OAuth callback chain without breaking existing callers.
- `make test` + `make test-integration` green.
- Real-flow verification: if staging has Google OAuth configured, verify the identify fires (check PostHog for the event). If not, unit-test the identify call path.
- Commit on `oauth-posthog-fix`, push, `gh pr create --base develop` titled "fix: OAuth callback PostHog tracking (identify + capture on Google sign-in)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only.

## Self-report

- `bin/ledger set righttenantry-oauth-posthog-fix working` at start
- `bin/ledger set righttenantry-oauth-posthog-fix in-review "PR <url>"` when PR opens
- `herdr notification show "righttenantry-oauth-posthog-fix" --body "<one-line>"` on finish
- Final message: summary, files changed, PR URL, what events now fire on OAuth, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-oauth-posthog-fix
- base: develop
- pr_review: true
