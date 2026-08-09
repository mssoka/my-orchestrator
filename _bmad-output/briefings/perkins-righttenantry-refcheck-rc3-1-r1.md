# Perkins briefing — round 1: righttenantry-refcheck-rc3-1

- **PR:** https://github.com/solarity-services/RightTenantry/pull/594 (targets `develop`)
- **Reviewed sha:** `2a2b063824116ce1c4d13430cd3cb8aea4d9601a` (head `refcheck-rc3-1`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-1-r1` — pinned at the reviewed sha.
- **Spec:** the job briefing + the story spec. No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner:** `solarity-services`

## What the PR does

RC3.1: the Twilio infrastructure slice — sms_client.gleam (send + callback, FROM Alpha Sender ID "RTenantry") + reference_lookup (Twilio Lookup line-type). Graceful no-op without keys.

## ⚠️ CRITICAL lens-guard

- **Do NOT flag "should use a from-number"** — AD-5 corrected: the sender IS the Alpha Sender ID ("RTenantry"), no TWILIO_FROM (Twilio Irish numbers are voice-only).
- **Do NOT flag "no real Twilio API calls in unit tests"** — graceful no-op without keys is the REQUIREMENT (creds in Secret Manager at runtime; code builds + tests without them).
- **Do NOT flag "should auto-reject VoIP/burner"** — AD-10: Lookup fraud signals are display/confidence only, never auto-reject.
- **Do NOT flag "missing cadence/sweep logic"** — rc3-1 is the CLIENT INFRA; rc3-5 owns sends/cadence.

### Legitimate findings: credential leakage in logs/errors; the send payload doesn't use the Alpha Sender ID correctly; the Lookup doesn't parse line_type; the no-op path breaks the build; auth wrong; broken Gleam parse; em-dashes in copy (RT CI ban); tests don't pin the behavior.

## Perkins standing orders (standard — follow exactly)

- You review; never fix/push/merge. Save the canonical diff: `gh pr diff 594 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-1/r1/diff.patch`.
- Headless mode (dedicated tab, `mm-<lens>-r1`), `<lens>.json`, one retry, big-diff chunking, verification pass, `consolidated.json`. Close every lens pane.
- **Verdict:** 0B → `--approve`; 1-3 → `--request-changes`; 4+ → MAJOR REWORK. Degraded guard → `--comment`.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; fallback `gh pr comment 594 --repo solarity-services/RightTenantry --body-file <body.md>`; else `GH_TOKEN=$TOKEN gh pr review 594 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Re-fetch `headRefOid` before posting.
- Self-report: `bin/ledger set righttenantry-refcheck-rc3-1-perkins-r1 working` at start.
- Skip Step 5.
