# Perkins briefing — round 1: righttenantry-refcheck-rc3-6

- **PR:** https://github.com/solarity-services/RightTenantry/pull/602 (targets `develop`)
- **Reviewed sha:** `6751de1e3bec78bf411a389bc346e0cc0d789962` (short `6751de1`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-6.md` + story RC3.6 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (FR-RC8 wrong-contact/bounce, FR-RC9 objection) + the architecture `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (AD-6 objection sticky, AD-14 transitions, AD-15 liveness, AD-16 the new audit row, §9.2 objection log, the webhook-verification design, §8.3 notification values) + GitHub issue #548 (dumped at `_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/issue-548.json`).
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out notes (it ran a lavish clarify, corrected a stale AC, self-reviewed) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**RC3.6: Verified Webhooks — Resend + Twilio SMS.** Two signature-verified inbound webhook endpoints that let the system HEAR back from email/SMS delivery:
- **POST /webhooks/resend-events** (svix-verified, reuses `inbound_email/svix.gleam`): email `bounced`/`complained`/`failed` → `awaiting_correction`.
- **POST /webhooks/twilio-sms** (X-Twilio-Signature-verified, new `notification/twilio_webhook.gleam`): SMS `failed`/`undelivered` → `awaiting_correction`.
- On a real transition: NULLs `next_attempt_at`, writes an **AD-16 audit row**, fires an **in-app `reference_awaiting_correction` notification** (Q3=B2 — in-app only, NO email). Load-bearing signature verification, idempotent, sticky.
- 8 modified + 11 new files (webhooks.gleam, twilio_webhook.gleam, 3 SQL, 2 migrations, 3 test files; router.gleam 2 arms, csrf.gleam new arm, notification_dispatch, event_type, sql.gleam regen).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

Production server code + webhook security. The design is PINNED; review the implementation.

- **SIGNATURE VERIFICATION IS LOAD-BEARING.** An unverified webhook MUST change NOTHING — no spoofed bounce/correction can mutate a reference row or send a notification. Verify the Resend (svix) + Twilio (X-Twilio-Signature) verifiers reject EVERY mutation (wrong token / wrong url / wrong/empty params) with 401/403 and mutate nothing; a correctly-computed signature is accepted. A path that mutates state BEFORE or WITHOUT verifying is a blocker.
- **🚨 STALE-AC CORRECTION — DO NOT flag "missing inbound STOP→objected."** The original briefing AC #2 ("inbound STOP→objected on the Twilio webhook") was **STALE and impossible** — Twilio's alphanumeric sender ID is one-way (no inbound reply), and rc3-4 already ships a stop-LINK route + the 2026-08-08 architecture amendment removed the STOP-reply path. The minion surfaced this as the #1 lavish clarify question; **the USER confirmed the correction (Q1=A): the Twilio webhook is DELIVERY CALLBACKS ONLY** (bounce/complaint/failed/undelivered → `awaiting_correction`), NOT inbound STOP. Flagging "missing STOP→objected" is a FALSE POSITIVE — that path is deliberately absent (the correction FLOW for bad contact is RC4.3). Review what the PR DOES (delivery callbacks → awaiting_correction), not what the stale AC said.
- **IDEMPOTENT (dedup by event id).** Resend + Twilio re-deliver; a re-delivered event MUST NOT double-apply (no double-transition, no double-notification, no double audit row). Verify the dedup (the `claim_webhook_event` SQL / event-id guard) is real + tested.
- **OBJECTION STICKINESS (AD-6/14 carry-forward from rc3-4).** A delivery event on an ALREADY-`objected` row is a **sticky no-op** — a bounce/complaint cannot un-object or re-transition an objected reference. Verify the sticky guard holds (the webhook respects rc3-4's terminal states).
- **BOUNCE → awaiting_correction feeds the sweep (FR-RC8).** The transition NULLs `next_attempt_at` + writes the AD-16 audit row; verify the sweep (rc3-5) will correctly NOT re-select an `awaiting_correction` row (it's a terminal-ish state the sweep respects).
- **ROUTE REGISTRY — all THREE (rc3-4 lesson).** Every new public POST route (`/webhooks/resend-events`, `/webhooks/twilio-sms`) MUST be in `is_public_path` + the **CSRF allowlist** (new arm) + `redact_token_route`. The minion flagged it added the CSRF arm; verify ALL THREE registries cover both new routes. A route missing from any registry is a real defect.
- **In-app-only notification (Q3=B2, user-confirmed).** The `reference_awaiting_correction` notification is in-app ONLY (no email) — do NOT flag "should also email."
- **No em-dashes** in user-facing copy (the RT CI ban — APPLIES to RightTenantry, unlike Packet-Plumber).
- **External gate:** live Twilio callbacks need the Twilio keys (still unprovisioned) — the endpoint + signature verification SHIP + are tested; live SMS delivery events only flow once keys land. Do NOT flag "can't verify live without keys" — that's the external gate, not a code gap.
- **AD-16 audit row** — the new audit-table write on the transition; verify it's written with the right shape (terminal-ish transition recorded for traceability).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas synced it). Review the PR content as-is at the sha.
- **Do NOT re-open rc3-1…rc3-5 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- A webhook that **mutates state without/before verifying the signature** (spoof path) — a blocker (the load-bearing invariant).
- A **non-idempotent re-delivery** (double-transition/audit/notification) — a blocker.
- A bounce that **un-objects or re-transitions an objected row** (violates stickiness) — a blocker.
- A new route **missing from any of the 3 registries** (public/CSRF/redact) — a real defect.
- A **bounce that doesn't feed the sweep correctly** (e.g. `next_attempt_at` not NULLed → the sweep re-selects an awaiting_correction row).
- An **em-dash in user-facing copy** (RT CI ban).
- A `make test` / `make build` / migration failure at `6751de1` (the minion reported 481 integration green; verify).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 602 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `6751de1`), `spec_files` = this briefing + the job briefing + RC3.6/FR-RC8/FR-RC9 + the architecture (AD-6/14/15/16, §9.2, webhook-verification, §8.3) + issue #548, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 602 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 602 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `6751de1`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc3-6 / **Reviewed sha:** 6751de1 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-6-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. If a lens 429s mid-turn, one `continue` may revive it; if it hard-fails, note the degraded lens.
