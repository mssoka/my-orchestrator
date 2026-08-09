# Perkins briefing — round 1: righttenantry-refcheck-rc3-2

- **PR:** https://github.com/solarity-services/RightTenantry/pull/595 (targets `develop`)
- **Reviewed sha:** `f5e827d1886aad16b439c6f4fb27a821cec63149` (head `refcheck-rc3-2`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-2-r1` — pinned at the reviewed sha.
- **Spec:** the job briefing + the story spec. No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner:** `solarity-services`

## What the PR does

RC3.2: SMS message templates + send helpers (T0 invite w/ Art 14 notice, T+24 co-nudge, T+48 reminder 1, T+96 reminder 2 + landlord warm-handoff). Every SMS carries the stop-link `/reference/:token/stop` (AD-6 corrected — one-way Alpha Sender ID). Send helpers call rc3-1's sms_client (FROM "RTenantry", no from-number) + email_client. No-op-safe without keys. Tests green (server 1289, integration 419).

## ⚠️ CRITICAL lens-guard

- **Do NOT flag "should use reply-STOP instead of a stop-link."** The Alpha Sender ID is one-way (AD-6 corrected, #593); the referee can't reply. The stop-link web route is the CORRECT pattern. Absence of "reply STOP" is intentional (test-pinned).
- **Do NOT flag "no real Twilio API calls in unit tests"** — no-op-without-keys is REQUIRED (creds in Secret Manager; code builds + tests without them).
- **Do NOT flag "T+24 co-nudge missing an SMS template"** — by design (email only, to the applicant, not the notice's subject).
- **Do NOT flag "no token minting in the helpers"** — DB-free is deliberate; the sweep (rc3-5) mints tokens. rc3-2 owns templates + helpers only.
- **Do NOT flag "send from 'RTenantry' instead of a number"** — AD-5 corrected (Alpha Sender ID, no from-number).

### Legitimate findings: a template missing the stop-link or the Art 14 notice; a send helper passing a wrong payload to the sms_client (wrong sender); the no-op path breaking the build (HTTP/Sentry on absent keys); em-dashes in SMS copy (RT CI ban); credential leakage; a test that doesn't actually pin the stop-link presence or the no-reply-STOP absence; broken Gleam/JS parse.

## Perkins standing orders (standard — follow exactly)

- You review; never fix/push/merge. Save the canonical diff: `gh pr diff 595 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-2/r1/diff.patch`.
- Headless mode (dedicated tab, `mm-<lens>-r1`), `<lens>.json`, one retry, big-diff chunking, verification pass, `consolidated.json`. Close every lens pane.
- **Verdict:** 0B → `--approve`; 1-3 → `--request-changes`; 4+ → MAJOR REWORK. Degraded guard → `--comment`.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; fallback `gh pr comment 595 --repo solarity-services/RightTenantry --body-file <body.md>`; else `GH_TOKEN=$TOKEN gh pr review 595 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Re-fetch `headRefOid` before posting.
- Self-report: `bin/ledger set righttenantry-refcheck-rc3-2-perkins-r1 working` at start.
- Skip Step 5.
