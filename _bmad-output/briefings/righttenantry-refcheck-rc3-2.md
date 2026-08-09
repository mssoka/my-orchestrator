# Briefing: righttenantry-refcheck-rc3-2

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (develop now has rc3-1's sms_client + Lookup). PR targets develop.
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion (the learning-loop pattern: Gru orchestrates, one fresh minion per story, own field-note shard → dream consolidation). Perkins: **ON** (code; r1 on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; one round).

## Mission

Story **RC3.2: message templates + send helpers.** The refcheck sprint is at 6/18 (rc1-1, rc1-2, rc2-1, rc2-2, rc2-3, rc3-1 done — rc3-1's sms_client just merged). rc3-2 builds the **SMS message templates + the send helpers** that the cadence sweep (rc3-5) will fire — using rc3-1's sms_client (the Alpha Sender ID "RTenantry" client). **CRITICAL: every template includes the stop-link** (per AD-6 corrected — the one-way Alpha Sender ID means objections go via a web stop-link, NOT reply-STOP).

## The story (acceptance — from the epics + architecture)

1. **The SMS message templates** (FR-RC5's messages, but rc3-2 owns the TEMPLATES + helpers, NOT the cadence sweep — that's rc3-5):
   - **T0 invite** (the reference-check invite, email + SMS carrying the **Art 14 notice**).
   - **T+24h applicant co-nudge**.
   - **T+48h reminder 1**.
   - **T+96h reminder 2 + landlord warm-handoff notification** (with attempt log).
   - (T+144h terminal `unreachable` is silent — no template needed.)

2. **Every SMS template includes the STOP-LINK** (AD-6 corrected, #593): the token-gated stop-link web route (`/reference/:token/stop`) — the referee taps it to decline/object. **NOT "reply STOP"** (the Alpha Sender ID is one-way; the referee can't reply). The Art 14 notice + the opt-out both point to the stop-link.

3. **Send helpers** — the functions the cadence sweep (rc3-5) calls to send each template (via rc3-1's sms_client, FROM "RTenantry", with the status-callback URL). Graceful no-op without keys (like rc3-1).

4. **The capability-token link** in each template points to the reference form (`/reference/:token`) per AD-3.

## Source material (read — the spec + patterns)

1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — rc3-2 + FR-RC5 (the cadence messages — but note the SWEEP is rc3-5; rc3-2 is the templates + helpers) + the Art 14 notice requirement.
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — **AD-6 (CORRECTED in #593): the stop-link web route for objections (one-way Alpha Sender ID).** AD-5 (the sender). AD-3 (the capability-token form link). The sms_client row.
3. **rc3-1 (just merged)** — the `sms_client.gleam` you're calling (send + callback, Alpha Sender ID, no-op-without-keys). Match its structure.
4. **`_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`** — the message copy/flows (the invite + reminder wording, the decline route).
5. **`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`** — update rc3-2 → in-progress → done.

## Flow

1. **Create the story spec** (bmad-create-story) — rc3-2 with the templates + helpers + stop-link context. Update the tracker.
2. **Dev the story** (bmad-dev-story): the SMS templates (T0/T+24/T+48/T+96, each with the stop-link + Art 14 notice) + the send helpers (calling rc3-1's sms_client). Graceful no-op without keys.
3. **Test:** templates render correctly (stop-link present, Art 14 notice, the token links), send helpers call the sms_client with the right payloads (mocked), no-op-without-keys. `make test-server` + `make test-integration` green.
4. **Update the tracker:** rc3-2 → done/review.

## Constraints (RT-specific — APPLY here)
- **No em-dashes in user-facing copy** (RT global ban, CI-guarded). The SMS copy — em-dash-free.
- **Every SMS template includes the stop-link** (`/reference/:token/stop`), NOT "reply STOP" (AD-6 corrected — one-way sender).
- **The Art 14 notice** in the T0 invite (the GDPR requirement).
- Send FROM "RTenantry" via rc3-1's sms_client (no from-number).
- **Code no-ops without keys** (graceful skip without Twilio creds — like rc3-1).
- The cadence sweep is rc3-5 — don't build the sweep here; just the templates + helpers it calls.

## Acceptance
- SMS templates (T0/T+24/T+48/T+96) with stop-link + Art 14 notice + token links.
- Send helpers (calling rc3-1's sms_client, Alpha Sender ID, no-op-without-keys).
- `make test-server` + `make test-integration` green.
- No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-2 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-2 in-review "PR <url>"` when PR opens
- `herdr notification show "refcheck-rc3-2" --body "<one-line>"` on finish
- Final message: the templates + helpers summary, the stop-link presence in each, test results, the story-spec path, PR URL, + whether rc3-3 (referee form session) is the natural next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-2 · base: develop
