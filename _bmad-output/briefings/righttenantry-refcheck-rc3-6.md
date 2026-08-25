# Briefing: righttenantry-refcheck-rc3-6

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, base `develop` @ `a95b61d`).
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion. Perkins: **ON** (production server code + webhook security). Self-review: bmad-review-edge-case-hunter (signature verification, idempotency, objection stickiness).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down all cycle; production code — frontier-preferred, quota forces glm-5.2).
- **Perkins:** ON (glm-5.2 fallback).
- **bmad-quirk heads-up:** the create-story/dev-story tooling mis-resolves edits to the main checkout. **Verify every edit lands in YOUR worktree** (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Story **RC3.6: Verified Webhooks — Resend Events + Twilio SMS.** The refcheck sprint continues (rc3-1…rc3-5 merged). rc3-6 closes the inbound loop: **signature-verified webhook endpoints** that capture email delivery events (Resend) + process inbound SMS (Twilio) — including the **STOP/opt-out → `objected`** path. Until this, the system only SENDS (rc3-2/3-5); rc3-6 lets it HEAR back.

## Carry-forwards (read the merged work)
- **rc3-2** — the send helpers/templates; webhooks receive events for what these sent.
- **rc3-5** (the sweep) — delivery status from webhooks (bounce/failure) feeds the sweep's transition logic (e.g. a bounce → `awaiting_correction` per FR-RC8 wrong-contact).
- **rc3-4** — objection handling: inbound STOP → `objected` (**sticky**, AD-6), `reference_objection_log` written at objection time; all sends blocked.
- **rc3-4 route-registry lesson:** every new public POST route (the webhook endpoints) MUST be registered in `is_public_path` + **CSRF allowlist** + `redact_token_route` — the csrf-registry lens-guard caught a miss on rc3-3; don't repeat it.

## The story (acceptance — from the epic RC3.6 + arch)

1. **Resend webhook** (email delivery events): signature-verified endpoint capturing delivered/bounced/failed → updates the `reference_call` delivery state the sweep reads.
2. **Twilio SMS webhook** (inbound): signature-verified; an inbound **STOP** → immediately `objected` (sticky, AD-6), `next_attempt_at` NULL, all sends blocked, `reference_objection_log` row written, `reference_objected` notification. (FR-RC9.)
3. **Verification + idempotency:** verify each webhook's signature (Resend + Twilio signing) before ANY state change; dedup by event id (idempotent re-delivery).
4. **Registry:** webhook routes registered in all three registries (public path + CSRF + redact).

**Files (likely):** `server/src/reference_checks/webhooks.gleam` (+ sql) · `server/src/router.gleam` · signature-verify helpers.

## Source material (read)
1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — story RC3.6 (full AC) + FR-RC8 (wrong-contact/bounce), FR-RC9 (objection short-circuit).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — AD-6 (objection sticky), §9.2 (objection log), the webhook-verification design, §8.3 (notification values).
3. **rc3-2 / rc3-5 / rc3-4** (merged) — the send/sweep/objection machinery this plugs into.

## Constraints (RT-specific)
- **Signature verification is load-bearing** — an unverified webhook must change NOTHING (no spoofed STOP can object a reference).
- **Idempotent** — Resend/Twilio re-deliver; dedup by event id.
- **STOP → objected is sticky** (AD-6/14): a later bounce/sweep can't un-object.
- **No em-dashes** in any user-facing copy (RT CI ban).
- **External gate:** Twilio SMS webhooks need the Twilio keys (still unprovisioned) — the endpoint + verification ship; live SMS stops objecting only once keys land.
- **Route registry** — all three registries (the rc3-4 lesson).

## Verify
- Signature-verify: an unsigned/wrong-signature webhook changes nothing (test both Resend + Twilio).
- Idempotency: re-delivering the same event id doesn't double-apply.
- STOP → objected (sticky) + `reference_objection_log` written + sends blocked.
- Bounce → feeds the sweep's wrong-contact/`awaiting_correction` path.
- All webhook routes registered (public/CSRF/redact); `make test-server` green.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set righttenantry-refcheck-rc3-6 working` at start
- `bin/ledger set righttenantry-refcheck-rc3-6 in-review "PR <url>"` + `bin/ledger pr righttenantry-refcheck-rc3-6 <url>`
- `herdr notification show "refcheck-rc3-6" --body "<one-line>"` on finish
- Final message: the webhooks summary, signature/idempotency verification, whether rc3-7 (fraud signals) is next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-6 · base: develop
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: 548
