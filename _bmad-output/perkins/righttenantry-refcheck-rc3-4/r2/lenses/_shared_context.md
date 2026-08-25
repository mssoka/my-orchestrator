# Perkins r2 fix-audit — SHARED CONTEXT for all lenses

You are a reviewer in a **round-2 fix-audit** of PR #599 (solarity-services/RightTenantry), story RC3.4 (referee form exit routes). Round 1 returned CHANGES_REQUESTED (1 blocker B1, 6 warnings W1-W6, 14 notes N1-N14 — 25 findings, all verified). This round reviews the **rework delta** (commit 13ae750 → 8c9c87e) that claims to fix them.

## Your job
Find **NEW** problems introduced by the rework delta. Do **NOT** re-litigate the prior findings listed below — the lead reviewer (Perkins) has already verified each against the worktree and dispositioned it (FIXED / PARTIAL / DEFERRED). If you independently confirm a prior finding is *still present* despite a claimed fix, that IS reportable (note `still present since r1`).

## Worktree (read code here)
`/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r2` — detached at exactly `8c9c87e`.

## The delta under review
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/r1-to-r2-delta.patch` (542 lines, 7 files: form_handler.gleam, form_pages.gleam, form_copy.gleam, result.gleam, the exit_routes integration test +374, reference_form_integration_test, form_copy_test). The full PR diff is at `../diff.patch` for context only — do not re-review it wholesale.

## Prior findings + Perkins's verified disposition (DO NOT re-litigate unless still-present)
- **B1 (blocker) — FIXED:** `notify_reference_event` (form_handler.gleam ~1310) now passes raw `row.origin_domain` to all three `notify_reference_completed/declined/objected`. `origin_from_domain` kept ONLY for the invite `base_url` (line 694). `dispatch_reference_notification` → `build_entity_url(origin_domain:, ...)` prepends https:// itself. No double-scheme on ANY path.
- **W1 — FIXED:** `view_review` (form_pages.gleam) renders hidden `_focus_seconds` (data-focus-seconds). Flow test POSTs 240 → asserts `result->'fraud_signals'->'form_session'->>'focus_seconds_reported'` == "240" (real, not tautological).
- **W2 — FIXED:** `apply_decline` pipes `decline_reason` through `string.slice(0, 200)` (grapheme-correct; equivalent to the private `application_handler.truncate` which is `string.slice(value, 0, max)`).
- **W3 — FIXED:** AC7 honeypot tests on all 4 exit POSTs; `honeypot_filled_stop_post_does_not_object_test` asserts status stays "contact_initiated" AND objection_log_count == 0 (critical branch pinned).
- **W4 — PARTIAL:** completed notification row + late-after-handoff "after all" copy pinned; declined/objected notification rows NOT specifically pinned (share the notify_reference_event wrapper, exercised by the completed pin — low risk).
- **W5 — FIXED:** all 4 audit terminal events pinned (completed/declined/objected/wrong_person).
- **W6 — FIXED:** coverage gate lifted; suite green (1403 unit + 441 integration, 0 failures).
- **N1 FIXED** (character free_text_signals emitted), **N2 FIXED** (headline dead arm collapsed), **N3 FIXED** (view_objected distinct page + truthful copy + rc3-3 test updated to reference-objected), **N5 FIXED** (CSRF {200} reachability w/ fresh rows), **N6 FIXED** (channel CHECK 'web' ok / 'telegram' rejected).
- **DEFERRED (rationale holds — do not re-raise):** N4 (completion_seconds null → rc3-7), N7 (focus_seconds no clamp — crafted-POST-only, rc3-7 not shipped), N8/N11 (purge_after/evidence atomicity — no sweep yet), N9 (discarded dispatch Result — mitigated by W4 pin), N10 (ObjectionChannel enum lacks 'web' — documented drift, inert), N12/N13/N14 (lower-risk coverage).

## Lens-guards confirmed holding (do not re-litigate)
Objection stickiness (AD-6/14), single-writer evidence (apply_objection sole writer), deterministic result (result.gleam pure), one-submission (AD-3), registry prefix-match + router arms (untouched by delta).

## Project conventions
Gleam/Lustre + Wisp/Mist + Postgres (Squirrel). No `let assert` in prod. No JS FFI. No em-dashes in USER-FACING copy (server log messages are NOT user-facing). Explicit HTTP timeouts. See AGENTS.md.

## OUTPUT CONTRACT (mandatory)
Write ONE valid JSON array to your assigned file path (given in your lens brief). Schema per element:
```json
{"source":"<your source>","severity":"blocker|warning|note","category":"<tag>","title":"<one line>","location":"<file:line|N/A>","evidence":"<exact lines READ from the file, verbatim>","detail":"<=40 words","recommended_fix":"<=40 words"}
```
- `[]` is valid and expected when the rework is clean. **Do not invent findings to fill a quota.**
- Every finding will be independently re-verified against the worktree; unverifiable claims are discarded. Quote exact lines in `evidence`.
- Write the file, then stop. Do not print prose.
