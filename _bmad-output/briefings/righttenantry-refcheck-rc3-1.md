# Briefing: righttenantry-refcheck-rc3-1

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (develop now has rc2-3's trigger + the AD-5 corrected sender). PR targets develop.
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion (the learning-loop pattern: Gru orchestrates, one fresh minion per story, own field-note shard → dream consolidation). Perkins: **ON** (code; r1 on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; one round).

## Mission

Story **RC3.1: SMS client + Twilio Lookup infrastructure slice.** The refcheck sprint is at 5/18 (rc1-1, rc1-2, rc2-1, rc2-2, rc2-3 done). rc3-1 is the **Twilio infrastructure** — the minimal SMS client (send + status callback) + the Lookup API (line-type fraud signals). This was the external-gate halt point, but the gate is now CLEARED (the user has the Twilio creds; AD-5 corrected the sender to a Registered Alpha Sender ID; the registration runs in parallel for delivery).

## The story (acceptance — from the epics + architecture)

**Core: the Twilio infrastructure slice (no cadence/sends-logic yet — that's rc3-5):**

1. **`server/src/notification/sms_client.gleam`** (AD-5) — a minimal Twilio REST helper:
   - **Send SMS** via the Twilio REST API, FROM the **Registered Alphanumeric Sender ID "RTenantry"** (NOT a from-number — per AD-5 corrected: `TWILIO_ALPHA_SENDER`, no `TWILIO_FROM`).
   - **Status callback URL** support (for delivery-status webhooks — rc3-6 narrows the inbound webhook to delivery callbacks per AD-6).
   - Auth via **Account SID + Auth Token** (`TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN`).

2. **`reference_lookup` module** (AD-10) — Twilio **Lookup API** for line-type intelligence at capture:
   - `line_type` + `voip_or_burner` per the fraud-signals honesty table (AD-10). These populate the fraud-lens signals (display/confidence content only — never auto-reject).
   - Uses the SAME Twilio creds (Account SID + Auth Token) — no separate provisioning.

3. **Graceful no-op without keys** — the code MUST build + unit-test without real Twilio creds (the user has them, but they live in Secret Manager at runtime; the code no-ops/skips sends + lookups when creds absent). This is critical: rc3-1 BUILDS + UNIT-TESTS without the registration/creds; live DELIVERY waits on the Alpha Sender ID registration.

## Source material (read — the spec + patterns)

1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — rc3-1 acceptance + FR-RC12 (the fraud-signals table, line_type/voip_or_burner) + FR-RC5 (note: rc3-1 is the CLIENT INFRA, not the cadence sweep — rc3-5 owns sends).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — **AD-5 (CORRECTED in #592): Alpha Sender ID "RTenantry", no from-number, via a Twilio Messaging Service.** AD-10 (Lookup line-type at capture). The sms_client + reference_lookup rows in the dependencies table.
3. **Prior stories for PATTERNS:** rc2-1 (#558, the reference_call schema the SMS targets), rc1-1 (#557, the attestation/capture columns the Lookup fraud-comparator uses). Match the established notification/REST conventions (the existing `email_client.gleam` uses Resend — mirror its structure).
4. **`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`** — update rc3-1 → in-progress → done.

## Flow

1. **Create the story spec** (bmad-create-story) — rc3-1 with the client-infra scope + the AD-5/AD-10 context. Update the tracker: rc3-1 → in-progress.
2. **Dev the story** (bmad-dev-story): the sms_client (send + callback, Alpha Sender ID) + the reference_lookup (line-type) + graceful no-op-without-keys. Match email_client.gleam's REST-helper structure.
3. **Test:** unit tests (mocked Twilio — no real API calls in unit tests; verify the send payload uses the Alpha Sender ID, the Lookup parses line_type, the no-op-without-keys path). `make test-server` + `make test-integration` green. (Live integration test against real Twilio is OPTIONAL — the creds are in Secret Manager; flag if you do it.)
4. **Update the tracker:** rc3-1 → done/review.

## Constraints (RT-specific — APPLY here)
- **No em-dashes in user-facing copy** (RT global ban, CI-guarded).
- **Send FROM `TWILIO_ALPHA_SENDER` ("RTenantry") — NO from-number** (per AD-5 corrected). This is the one-way Alpha Sender ID reality.
- **Code no-ops without keys** — the build + unit tests MUST pass without real Twilio creds (graceful skip). Live delivery waits on the registration.
- Follow `email_client.gleam`'s REST-helper conventions (Resend) — mirror the structure for consistency.
- The Lookup fraud signals are **display/confidence only — never auto-reject** (AD-10).

## Acceptance
- sms_client.gleam (send + callback, Alpha Sender ID, no from-number) + reference_lookup (line_type/voip_or_burner) implemented.
- Graceful no-op without keys (build + unit tests pass without real creds).
- `make test-server` + `make test-integration` green.
- No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-1 in-review "PR <url>"` when PR opens
- `herdr notification show "refcheck-rc3-1" --body "<one-line>"` on finish
- Final message: the sms_client + Lookup summary, the no-op-without-keys verification, test results, the story-spec path, PR URL, + whether rc3-2 (message templates) is the natural next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-1 · base: develop
