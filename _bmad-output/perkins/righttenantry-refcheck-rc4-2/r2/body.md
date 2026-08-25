## 🤖 Perkins automated review — round 2 of 3

**Job:** righttenantry-refcheck-rc4-2 · **Reviewed sha:** `e0f9fa7` · **Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests — 3 chunks each: spec+client/src / client tests / server+shared)

**Verification:** 16/27 findings confirmed against the code — 1 discarded as false-positive (the "Next reminder" trailing-period/batches<3 note, both halves already rejected at r1 for identical reasons: UX §7.4 verbatim has no period inside the quotes and `< 4` is correct), 10 duplicates merged. Every r1 finding re-read at the cited location in this worktree.

**Build gates (run at `e0f9fa7`):** `make build` OK · `make test-client` 521 passed · `make test-shared` 108 passed · `make test-server` 1476 passed (499 integration skipped)

### r1 fix audit (21/22 landed; 2 carried as findings below)

- ✅ **B1 (blocker)** — hook-driven terminality: `is_terminal(call) = !call.hooks.can_record_manual`; no client-side status set remains.
- ✅ W2 — `"landlord" -> "Their landlord"` mapped + total-match word-map test (29 values).
- ✅ W3 — `relationship_other` renders as its own row + verbatim-text test.
- ✅ W5 — objected copy is gender-neutral ("asked us not to be contacted").
- ✅ W7 — character slot counts 6-of-6 (`free_text_signals` excluded) + test.
- ✅ W8 — auto-expand handler tests (first-view, not-consumed-without-summary, route reset) + total-match word-map test.
- ✅ Cheap notes — dead const removed, `month_abbr` deduped, keyed mini-timeline, `answered_count` mirrors the renderer, auto-expand gated on expandable rows, never-red full-token test, integration wire pins (null + populated), v2/malformed/aria-expanded tests.
- ⚠️ **W1 — PARTIAL** (finding below) · ⚠️ **W4 — WRONG FIX** (finding below) · ℹ️ W6 landed but inert (finding below) · ℹ️ N2 datetime offset and N10 geo sentence partial (notes below).

### Blockers (0)

None. No red pill, no §4.2/§7.4 copy deviation, no guessed values, no contract break (back-compat decoders + untouched RC4.1 strip assertions verified), no client-side re-derivation of hook rules, no a11y break.

### Warnings (2)

1. **W4 fix is wrong for production data — same-day form-open renders ABOVE the invitation** [blind, edge, acceptance]
   `client/src/components/reference_panel.gleam:543` sorts the timeline with `string.compare(a.at, b.at)` on mixed formats: attempts `at` are RFC3339 (`2026-08-01T10:04:00Z`) while `form_opened_at` rides Postgres `::text` (`2026-08-01 21:12:00+00` — space at index 10). Since `' ' < 'T'` lexically, a form opened the same day as the invite — the §7.2 canonical case (invite Tue 10:04, opened Tue 21:12) — sorts *above* "Invitation sent". The pin test feeds RFC3339 (`form_opened_at: Some("2026-08-03T18:00:00Z")`), a format the server never sends (the integration test pins the space form at `reference_detail_payload_integration_test.gleam:307`), so the suite is green while production inverts. Fix: normalize both sides before comparing and pin with the real wire format.
2. **W1 fix incomplete — em-dash ban pin never extended; a render-time em-dash still ships in the nudge-skipped line** [blind, edge, acceptance, architecture, codebase, tests — 6 lenses]
   The two r1-flagged consts were rewritten clean (verified), but the claimed `no_em_dash_test` extension never landed — `copy_test.gleam` is untouched by the rework and still scans toast/page codes only. And `reference_panel.gleam:633` still composes `refcheck_timeline_nudge_skipped <> " — " <> skipped.detail` → "Applicant nudge skipped — co-nudge skipped: form already opened", an implementer-authored em-dash (plus duplicated internal reason) that fires whenever the T+24h co-nudge gate skips — a normal state. Fix: extend the ban test to refcheck copy *and* the timeline composition sites; drop the ` — ` join.

### Notes (14)

1. B1's hook-driven sub-line has no distinguishing test — a revert to status-derived terminality (r1's exact bug, omitting v2 `Completed`) would pass everything, because the test fixture derives hooks from the client's own `is_terminal_status` list.
2. W6 landed but inert: `refcheck_explainer_dismissed` is persisted + hydrated but never consumed by any view or update — behavior is identical with or without it.
3. N2 fix partial: `normalize_datetime` swaps the space for `T` but leaves the colon-less `+00` offset — still not a valid HTML datetime value.
4. N10 partial: 6 of 7 worth-knowing signal sentences pinned; the geo-mismatch sentence has no fixture (`geo_vs_claimed_property` is `"unknown"` everywhere in tests).
5. `reference_panel.gleam` GREW in the rework (1263 → 1309 lines); the r1 module-split recommendation was not taken.
6. Off state renders the heading "Reference Checks (0)" and the §7.8 explainer, whose copy describes completed written references the off state can never produce.
7. Panel-test fixtures still use the phantom `"their_landlord"` wire value r1 W2 was about — the render path for the real `"landlord"` value is only pinned at word-map level.
8. Stale duplicated doc comment on `answered_count` (leftover from the r1 rework).
9. `worth_knowing_signals` comment overclaims: `flags` rows "map here too", but no `flags` field is ever decoded.
10. `nudge_label`'s skipped/failed arms are untested — the W1-rewritten timeline labels have no pin at all.
11. `normalize_datetime` has zero test coverage.
12. First-view auto-expand tests cover only the FormCompleted branch — ManualRecorded/Partial arms of the `summary_ids` filter untested.
13. Notable-quotes truncation boundary untested — `list.take(3)` never exercised with >3 quotes (RC5.1 will ship quotes).
14. Advisory test gate: CONCERNS (demoted from warning — repo convention rejects coverage-ladder gating; the named P1 gaps are items 1 and 2 above).

### Reviewer agreement

- **W1 incomplete** — 6 lenses (blind, edge, acceptance, architecture, codebase, tests). Highest-confidence finding of the round; the fix map's claimed test extension demonstrably never landed.
- **W4 wrong fix** — 3 lenses (blind, edge, acceptance) + byte-level verification of the two wire formats.

### Verdict

**READY TO MERGE**

All r1 findings verified: the blocker and 6 of 8 warnings are genuinely fixed, and the two carried warnings (W1 pin gap + render-time em-dash, W4 mixed-format sort) are non-blocking defects with small, named fixes. All four build/test gates green at `e0f9fa7`. Recommend addressing the two warnings (plus notes 1–2) in the RC4.3 round or a small follow-up.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
