# Briefing: righttenantry-refcheck-rc4-1

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, base `develop` **after #603 merges**).
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion. Perkins: **ON** (API boundary + privacy stripping). Self-review: bmad-review-edge-case-hunter (the §4.2 stripping completeness, hook-logic edge states, codec round-trips).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **Perkins:** ON (glm-5.2 fallback).
- **bmad-quirk heads-up:** the create-story/dev-story tooling mis-resolves edits to the main checkout. **Verify every edit lands in YOUR worktree** (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Story **RC4.1: Detail Payload Extension (Backend Contract)** — opens **Epic RC4 (Landlord Reference Panel)**. Build the `reference_calls[]` payload contract so the panel (RC4.2–4.4) renders from **one stable server-computed contract** and never re-derives state rules client-side. This is the bridge from the collection engine (RC1–3, now complete) to the UI — it surfaces templates/sweep/webhook/fraud-signal data, **strips internal-only fields at the boundary**, and computes the hooks + disclaimers the panel needs.

## The story (acceptance — from epic Story RC4.1 + arch §8.1/§8.2/§9.5)

1. **`reference_calls[]`** in `GET /api/v1/vacancies/:vid/applications/:aid` per §8.1: `reference_call_id`, `ref_slot`, `owner_label`, `status`, `outcome`, `attempt_count`, `next_attempt_at`, the attempt log, the stored `result`, + the **hooks** object.
2. **§4.2 stripping at the boundary** — internal-only fields never leave the server: `form_token`, `objection_detail.payload_ref`, **raw IPs/UAs inside `fraud_signals.form_session`** (the rc3-7 fraud signals — only the derived booleans transit, never the raw comparators).
3. **`display_disclaimer`** server-rendered per channel (§9.5: written-channel results carry the call-encouragement note — calibration copy per §8.1, provenance framing never invalidation); **hooks** computed per §8.2 — `can_record_manual` (any non-terminal), `can_substitute_referee` (terminal `objected`/`unreachable`), `can_retry` (`failed`).
4. **Application-level fields** — `attestation_on_file` + `reference_contact_choice` (A4) + the referee trios, so the panel renders the Off + pre-trigger states without extra fetches.
5. **Compilation boundary (AR21)** — types in the shared package with JSON codecs (snake_case unbroken DB → JSON → Gleam), **round-trip tests**.

**Files:** `server/src/application/application_detail_handler.gleam` + sql · `shared/src/shared/application_detail.gleam` · `shared/src/shared/reference_call.gleam`.

## Carry-forwards (read the merged work)
- **RC1–RC3** (all in develop) — the reference-check data this surfaces: templates (RC2), sweep + terminals (RC3.3–3.5), webhooks (RC3.6), **fraud signals (RC3.7)**.
- **rc3-7 fraud_signals** — RC4.1 strips the internal IP/UA from `fraud_signals.form_session` at the boundary (§4.2). The §4.2 containment rc3-7 enforced server-side is COMPLETED by RC4.1's boundary strip.
- **rc3-7 advisory notes** (ride RC4.1 — same area, trivial): module doc, metadata, test-helper idiom, orphaned table — sweep while you're in `reference_checks`. (The NULLIF-convention note is **NOT** yours — RC4.3 owns it.)

## Source material (read)
1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — Story RC4.1 (full AC, line ~607) + the RC4 epic narrative (line 605) + FR-RC13 (the payload).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — §8.1 (`reference_calls[]` fields + calibration copy), §8.2 (hooks), §9.5 (`display_disclaimer`), §4.2 (internal-only IP/UA — the stripping rule), A4/A5 (attestation/contact-choice), AR21 (compilation-boundary codec convention).
3. **rc3-7** (merged) — the `fraud_signals` shape you strip from at the boundary.

## Constraints (load-bearing — RT-specific)
- **§4.2 stripping is load-bearing** — raw IPs/UAs + `form_token` + `objection_detail.payload_ref` MUST NOT reach the client. Server tests with **explicit stripping assertions** (the §4.2 lens-guard). A spoofed/malformed payload can't leak internals.
- **One stable contract** — the panel renders ONLY from this payload; no client-side state-rule re-derivation (AR-RC13). Hooks + disclaimers are server-computed.
- **AR21 codecs** — shared types + JSON codecs, snake_case end-to-end, **round-trip tests** (DB → JSON → Gleam unbroken).
- **Hook logic edge states** — `can_record_manual` / `can_substitute_referee` / `can_retry` correct across every lifecycle state (incl. terminal `objected`/`unreachable`/`failed`).
- **No em-dashes** in user-facing copy (RT CI ban) — the §8.1/§9.5 disclaimers are verbatim canon.

## Verify
- `reference_calls[]` present with all §8.1 fields; hooks + `display_disclaimer` computed per §8.2/§9.5.
- §4.2 stripping: server tests assert `form_token`, `objection_detail.payload_ref`, raw IPs/UAs are absent from the serialized payload.
- Shared round-trip tests pass (AR21); `make test-server` + `make test-shared` green.
- rc3-7 advisory notes swept (doc/metadata/test-idiom/orphaned-table).
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set righttenantry-refcheck-rc4-1 working` at start
- `bin/ledger set righttenantry-refcheck-rc4-1 in-review "PR <url>"` + `bin/ledger pr righttenantry-refcheck-rc4-1 <url>`
- `herdr notification show "refcheck-rc4-1" --body "<one-line>"` on finish
- Final message: the payload summary, the §4.2 stripping verification, whether RC4.2 (the panel UI) is next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc4-1 · base: develop
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: 548
