# Briefing: righttenantry-csp-posthog-allowlist

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (RT uses develop → main; PR targets develop)
- **Skills policy:** quick-dev (small surgical change). Self-review before PR: bmad-review-edge-case-hunter (CSP is a security control — verify no allowlist over-broadening, no nonce weakening). Perkins: **ON** (security-sensitive code).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (CSP = security control; one round).

## Mission

The production site (`righttenantry.ie`) ships CSP in **Report-Only** mode. Before the user flips `CSP_ENFORCE=true`, PostHog analytics must be allowlisted — or the flip will silently break event ingestion.

PostHog loads client-side via a JS stub-loader + `posthog.init` (see `server/src/content/tracking_snippets.gleam`, consent-gated, `ui_host: 'https://eu.posthog.com'`). It needs `https://eu.posthog.com` in TWO CSP directives:

### Changes (all in `server/src/csp.gleam`)

1. **`script-src`** — add `https://eu.posthog.com` (the array_loader fetches the real script from there).
2. **`connect-src`** (currently line ~121: `"connect-src 'self' https://www.google.com https://mpc2-prod-23-is5qnl632q-ue.a.run.app"`) — add `https://eu.posthog.com` (event ingestion API calls).
3. **Update the allowlist comment block** (~lines 73-78) to document the PostHog additions and WHY (consent-gated analytics; required for enforce flip).

### Tests

Update `server/test/middleware/middleware_test.gleam` CSP assertions:
- The enforcing CSP header (when `CSP_ENFORCE=true`) must include `https://eu.posthog.com` in both `script-src` and `connect-src`.
- The report-only header must likewise include it.
- Verify the nonce mechanism still works (PostHog is an external script — it should be allowlisted by domain, NOT by nonce; the nonce is for inline scripts only).

## Acceptance

- `gleam test` passes (server dir).
- CSP header (both report-only and enforcing variants) contains `https://eu.posthog.com` in script-src AND connect-src.
- No other directive changes (don't touch img-src, style-src, frame-src — those are unaffected).
- The nonce-based inline-script protection is intact (script-src keeps `'self' 'nonce-...'` PLUS the posthog domain).
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Context (do not re-investigate — confirmed by Gru)

- PostHog EU instance: `https://eu.posthog.com` (confirmed in tracking_snippets.gleam:66 `ui_host`).
- PostHog is consent-gated (only loads after user consents to analytics) — that's why CSP violations were low-volume and didn't surface in top Sentry issues.
- Server-side `posthog_client` (Gleam) is server-to-server — NOT affected by browser CSP. Only the client-side JS snippet matters here.
- The enforce flip (`CSP_ENFORCE=true` in Cloud Run) is a SEPARATE deploy-time action the user will do AFTER this PR merges. This PR only fixes the allowlist.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-csp-posthog-allowlist working` at start
- `/Users/moses/code/bin/ledger set righttenantry-csp-posthog-allowlist in-review "PR <url>"` when PR opens
- `herdr notification show "csp-posthog-allowlist" --body "<one-line>"` on finish
- Final message: summary, PR URL, confirmation that gleam test passes + which directives changed.
