# Briefing: righttenantry-refcheck-rc2-3

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (develop now has rc2-2's `viewed` status — #590 merged). PR targets develop.
- **Workflow:** **bmad-create-story** (generate the rc2-3 spec from the epics) → **bmad-dev-story** (implement). Fresh minion (the learning-loop pattern: Gru orchestrates, one fresh minion per story, own field-note shard → dream consolidation). Perkins: **ON** (code; r1 on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; one round).

## Mission

Story **RC2.3: trigger reference-check creation on `viewed` + manual start/skip APIs.** The refcheck sprint is at 4/18 (rc1-1, rc1-2, rc2-1, rc2-2 done). rc2-3 is the TRIGGER story — it connects rc2-2's `viewed` status to rc2-1's `reference_call` schema: when a landlord marks the viewing done, the system auto-creates the reference-check rows.

## The story (acceptance — from the epics + FRs)

**Core: FR-RC3 (auto-create on `viewed`):** when the application status transitions to `viewed` (rc2-2's status), the system AUTO-CREATES `reference_call` rows (`status: queued`, `next_attempt_at: now()`, nothing sent) for:
- the primary applicant's **landlord-ref slot** (OR **character-ref slot** when `never_rented_before`)
- the **employer-ref slot**
- **skipping slots with no contact data**
- **SUPPRESSED when the applicant declined the attestation** (`reference_contact_choice = 'declined'`)

**FR-RC4 (manual start/skip):** landlord can **manually start** a check for a non-shortlisted application (pre-viewing) AND **skip/re-enable** individual references before trigger.

**A6 (`skipped` enum):** add `'skipped'` to `reference_call_status` (landlord excludes a reference at/before trigger; re-enable transitions back to `queued`). Treated as live for the slot unique index.

**The hook site:** `server/src/application/application_detail_handler.gleam:679` — the `maybe_send_shortlist_notification` call site is EXACTLY where rc2-2 landed the `viewed` transition. Hook the auto-create there (the trigger fires on entering `viewed`).

## Source material (read — the spec + patterns)

1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — rc2-3 + FR-RC3/RC4 + amendments A5 (trigger is the viewing, not the shortlist) + A6 (skipped enum).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — AD-13 (shortlist trigger, AMENDED to viewed per A5), AD-1 (the reference_call_status enum — add `skipped`).
3. **Prior stories for PATTERNS:**
   - **rc2-1 (#558)** — the `reference_call` + `reference_objection_log` schema YOU'RE creating rows in + extending (`skipped` enum). Match its schema conventions.
   - **rc2-2 (#590, just merged)** — the `viewed` status transition you're hooking. Read where it lands the transition (application_detail_handler.gleam:679) — that's your trigger point.
   - **rc1-1 (#557)** — the attestation capture (`reference_contact_choice = 'declined'` is your suppression check).
4. **`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`** — update rc2-3 → in-progress → done.

## Flow

1. **Create the story spec** (bmad-create-story) at `_bmad-output/implementation-artifacts/` — rc2-3 with the FR-RC3/RC4 + A5/A6 context + the hook site. Update the tracker: rc2-3 → in-progress.
2. **Dev the story** (bmad-dev-story):
   - Migration: `ALTER TYPE reference_call_status ADD VALUE 'skipped'` (A6).
   - Auto-create logic on `viewed` transition (FR-RC3): create the reference_call rows for the right slots, skip no-contact, suppress if attestation declined. Hook at the viewed-transition call site.
   - Manual start API (FR-RC4): landlord can start a check pre-viewing (non-shortlisted).
   - Skip/re-enable APIs (FR-RC4 + A6): skip a reference (→ `skipped`), re-enable (→ `queued`).
3. **Test:** the auto-create on viewed (right slots, skip no-contact, suppress-if-declined), the manual start, the skip/re-enable transitions. `make test-server` + `make test-integration` green.
4. **Update the tracker:** rc2-3 → done/review.

## Constraints (RT-specific — APPLY here)
- **No em-dashes in user-facing copy** (RT global ban, CI-guarded).
- Follow rc2-1's schema conventions (the reference_call rows you create + the enum you extend).
- The auto-create is a **guarded transaction** (one update per row; match the cadence-engine's guarded-update discipline that rc3-5 will own — don't pre-empt it, just the creation).
- The attestation-declined suppression is a hard rule (never auto-create if `reference_contact_choice = 'declined'`).

## Acceptance
- FR-RC3 (auto-create on viewed, right slots, skip no-contact, suppress-if-declined) + FR-RC4 (manual start + skip/re-enable) + A6 (skipped enum) all met.
- Hooked at the rc2-2 viewed-transition call site.
- Story spec created + sprint-status tracker updated.
- `make test-server` + `make test-integration` green.
- No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-3 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-3 in-review "PR <url>"` when PR opens
- `herdr notification show "refcheck-rc2-3" --body "<one-line>"` on finish
- Final message: the auto-create logic + manual APIs + skipped enum summary, test results, the story-spec path, PR URL, + whether rc3-1 (the Twilio-gated SMS slice) is the natural next (it's the external-gate halt point).

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc2-3 · base: develop
