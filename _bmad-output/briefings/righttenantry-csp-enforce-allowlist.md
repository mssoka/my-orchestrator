# Briefing: righttenantry-csp-enforce-allowlist

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`csp-enforce-allowlist` worktree, branch `csp-enforce-allowlist`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true` — CSP is security-sensitive; the string must be well-formed.

## Mission (user ruling: A1 — enforce globally + allowlist the third-party tracker domains)

The CSP is currently Report-Only (`csp.gleam`: `CSP_ENFORCE=true` flips to enforcing). Sentry violation data (8 issues, all third-party — zero from our code) shows what would break on enforce. **Add the violating origins to the CSP allowlist** so enforcement doesn't kill marketing tracking.

## The additions (from Sentry violation data, verified by Gru via sentry-cli)

File: `server/src/csp.gleam`, function `policy/1`.

| Directive | Current | Add | Source (Sentry issue) |
|---|---|---|---|
| `connect-src` | `'self' https://www.google.com` | `https://mpc2-prod-23-is5qnl632q-ue.a.run.app` | RT-PROD-6/E — Google Tag Manager server-side (Cloud Run) |
| `img-src` | `'self' data: https://www.google.com https://www.facebook.com` | `https://www.google.ie https://www.google.com.gh` | RT-PROD-7/G — Google Ads regional pixels (IE, GH). NOTE: more regional Google domains (google.co.uk, etc.) will surface as users from other countries hit the site — each is a one-line addition; flag in PR |
| `style-src` | `'self' 'unsafe-inline'` | `https://www.gstatic.com` | RT-PROD-F — Google Fonts/widgets CSS |
| `frame-src` | `'self' https://www.facebook.com` | `https://toolytics.pa.clients6.google.com` | RT-PROD-A — Google Analytics iframe |

## Three items to INVESTIGATE (do NOT blindly allowlist — report findings in the PR)

| Issue | Blocked source | Why investigate |
|---|---|---|
| ☁️ RT-PROD-D | `5z-2b6b7616f94640c2840d1841e1ac24c3.ecs.us-east-1.on.aws` | Obfuscated AWS ECS hostname — unknown third-party. Grep client code + check what loads this (browser extension? Sentry SDK? ad service?). If legitimate, add to connect-src with a comment naming the service; if unknown, flag as a parked question |
| 🐛 RT-PROD-9 | `properties` (bare word) | Not a valid hostname — almost certainly a client-side bug (a relative URL or variable used as a fetch target). Grep client code for bare `properties` in fetch/API calls. Fix the bug if found; do NOT add `properties` to CSP |
| 🔄 RT-PROD-5 | `righttenantry.ie` (self-origin!) | Blocked by script-src-elem despite `'self'`. Likely a subdomain mismatch (www vs apex) or protocol (http vs https). Check the `Origin`/`Host` header vs the script's src. If it's a www-vs-apex redirect, the fix may be adding the apex explicitly OR ensuring the app serves from one canonical origin |

## Do NOT flip CSP_ENFORCE

The `CSP_ENFORCE=true` env flip is a **deploy-time action the user takes after staging testing** — your PR ships the allowlist additions only. The user deploys to staging with `CSP_ENFORCE=true`, watches Sentry for zero new violations, then flips prod.

## Acceptance

- All four directive additions land; CSP string well-formed (no trailing semicolons, no missing quotes); the three investigation items reported with findings + any fixes.
- A staging-test runbook in the PR body: deploy with `CSP_ENFORCE=true` → hit the form + a marketing page → check Sentry for zero new violations → flip prod.
- `make test` green; a unit test asserting the CSP policy string includes each allowlisted domain (regression guard).
- Commit on `csp-enforce-allowlist`, push, `gh pr create --base develop` titled "fix: CSP allowlist for enforcement (Google/Facebook tracker domains) + violation investigations" with **Decisions & rationale** + the investigation findings. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-csp-enforce-allowlist working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-csp-enforce-allowlist in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-csp-enforce-allowlist <url>`
- On blocked/finished: `herdr notification show "righttenantry-csp-enforce-allowlist" --body "<one-line>"`
- Final message: summary, files changed, PR URL, investigation findings (3 items), staging runbook, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-csp-enforce-allowlist
- base: develop
- pr_review: true
