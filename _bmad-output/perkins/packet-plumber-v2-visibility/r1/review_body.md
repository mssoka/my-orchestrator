## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-visibility · **Reviewed sha:** `8575164` · **Reviewers:** 7/7 completed
**Verification:** 19/23 findings confirmed against the code — 4 discarded as false-positive

### The spine (checked firsthand, not on the PR's word)
- **Determinism:** re-ran `tools/harness.sh run` at the reviewed sha — **29/29 demos green, T1/T2 byte-identical**. `odin test core` 184/184, `tools/lint.sh` green, `odin build app` clean.
- **App-layer by construction:** `capture_frame` (`harness/goldens.odin:60-71`) calls only `draw_world`/`draw_forecast_panel`/`draw_health_meter`/`draw_crisis_banner` — never `draw_hud`. No `goldens/` paths in the diff, no `LOG_VERSION` bump, no serialization change. The one core addition (`node_stuck_by_class`) is a pure read over the same pile `node_health_measure` sums.
- **Why-dropped invariant:** `event_emit_drop` counts SLA + appends a site; the 2.3 severed cull (`core/flow.odin:856`) counts SLA only — so `severed = dropped − pool − queue ≥ 0` by construction. The split sums **except in the W1 corner below**.
- **Marker anchoring:** `bundle_lo/hi` are the canonical (min,max) node-id pair, rebuilt from scratch each topology change (`core/bundles.odin:108-127`); the mark snapshots the pair at shed time and the draw verifies the slot's current pair before anchoring — the slot-renumber misanchor is correctly guarded, and no mid-step window exists (rebuild precedes flow in `step.odin:119`).
- **Canon amendment:** decision-log entry is dated and section-additive; `gdd.md` gets one additive M5 table row + the canon sentence. Terminology canon respected in new HUD strings ("POOL", "SHEDDING", "queue depth", "stuck:" — no pressure/strain/ladder wording).

### Blockers (0)
None.

### Warnings (3)
1. **W1 — Why-dropped split vanishes for a class whose drops are exclusively 2.3 severed culls** `[edge, acceptance, architecture, tests, codebase]` — `app/main.odin:1476`. `drop_reasons` rows grow only from Drop_Site arrivals; a severed-only class has no row, the `int(c) < len(app.drop_reasons)` guard hides the whole split, and the gauge shows "drop N" with no named cause — falsifying the PR's own "split always sums to drop N" claim in exactly the demolition corner gap 4 exists for. Fix is one line: bounds-checked zero default (or pre-grow rows at `start_run`) so "severed N" always renders.
2. **W2 — The programmatic scratch pixel-scan is self-reported; no reproducible artifact in the repo** `[security, architecture, edge, tests, codebase]`. T2-invisibility is proven (construction + my green harness re-run); what's missing is durable evidence the new surfaces *render* correctly — the spec designates the scratch as "a separate throwaway". Commit the scan script/output, or soften the claim to manually verified. (Same app-layer precedent as the 5.2 card — flagged as a transparency gap, not a defect.)
3. **W3 — Advisory test gate: CONCERNS** `[tests]` — P0 spine fully covered; the P1 app-layer surfaces carry zero durable automated coverage (driven by W1/W2).

### Notes (8)
- **N1** `[blind]` `visibility.odin:115` doc says "oldest mark anchors the fade"; the code fades from the **newest** shed (re-shedding refreshes the marker — right behavior, stale comment).
- **N2** `[acceptance]` The tracked `_pr_body.md` in the branch is the stale **story-5.2** body — it misled 4 of my 7 lenses. The real PR body (fetched from GitHub) is correct; delete the file here or in a hygiene PR.
- **N3** `[edge]` The QoS rejection toast (`qos_panel.odin:475`) draws over the new queue-depth row for its 30-tick life.
- **N4** `[blind]` `Drop_Mark.class` is written in `feed_drop_sites` but never read by either draw proc.
- **N5** `[blind]` The card cause-line loop's `int(c) >= len(cat.packet_types)` guard can never fire (slice is roster-sized; the core proc also guards).
- **N6** `[blind]` "Never overflows the 232 px frame" isn't guaranteed — `draw_text_c` doesn't clip; fine for the shipped roster, data-dependent for future long class names.
- **N7** `[tests]` The `node_stuck_by_class` pin is single-scenario (no mixed-class pile, no `waiting_ticks==0` exclusion case, no counts-size guard case).
- **N8** `[tests]` App-side wiring (depth row, cause line, feed ring) is unit-only — the expected consequence of the app-layer seam.

### Reviewer agreement
W1 and W2 were each found independently by **5 of 7 lenses** — highest-confidence items; W1 is the one worth a fix before or right after merge (one line).

### Verdict
**READY TO MERGE** — the determinism spine is verified firsthand, all five gap surfaces match the spec, and the remaining items are advisories (W1 is a cheap one-liner worth folding in).

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
