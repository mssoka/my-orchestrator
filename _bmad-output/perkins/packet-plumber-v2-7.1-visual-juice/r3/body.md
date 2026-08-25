## 🤖 Perkins automated review — round 3 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-7.1-visual-juice · **Reviewed sha:** `5c482df` · **Reviewers:** 7/7 completed
**Verification:** 23/24 findings confirmed against the code — 1 discarded as false-positive (0 kept as [unverified])

**Fix audit (the r2 mandate):** r2-B1 (the post-#63 lane collision) is **mechanically dead** — the branch contains #63 (merge-base = `ebd02cb` = v2 tip), GitHub reports the PR MERGEABLE (the 15 binary golden conflicts resolved), and a Perkins-run `tools/ci-local.sh --mac` at this sha is **10/10 green** with gate 4 passing on the merged tree (the r2 scratch-merge drift of 6 demos at 218–12,311 px/frame is gone) and palcheck all-green including the B1 canary. T1/replay identity holds at file level (the only `.t1`/`.log.bin` entries vs v2 are the new juice additions). The cause chain (#63 catalog change → `catalog_hash` shift → re-bless on the merged tree) is accurate and recorded — in commit `5c482df`'s message, not the PR body (see W-3). r1 B1/B2 both re-verified still fixed. No r2 W/N was folded (the code is byte-identical to `cb3bf2d`) — per the round charter that was optional; the full fold set carries below for r4.

### Blockers (0)

None.

### Warnings (5)
- **W-1** Third SLA focus row's hit rect overlaps the tray chips' top 4px — and the press order runs `sla_focus_click` *before* the tray loop, so a press in the band toggles class focus instead of arming the chip. `app/main.odin:1247` + `app/render/tray.odin:44` + `app/input/mouse.odin:216` *(edge)*
- **W-2** Crisis banner + SLA rects joined the press-side hit-test but not the release-side: `effect_ui_release` covers popover/QoS/tray only, so a ≤6px straddle press (outside) released inside the new chrome click-selects — and focus-zooms — the node beneath. `app/main.odin:739` + `app/input/exec.odin:132,435` *(edge)*
- **W-3** PR body never updated for the rebase: the catalog-drift cause chain lives only in commit `5c482df`, the body still attributes all 74 re-blesses solely to the juice, and its Verification bullet says "9/9 gates" (the suite is 10). Add a rebase addendum + fix the count. *(acceptance)*
- **W-4** The selection-halo rewrite (the 4th `band_width` consumer) has zero coverage — `sel` stays −1 in every committed artifact, so `draw_selection` never executes in any gate. `app/render/view.odin:804` *(tests)*
- **W-5** The sprites.json roster has three unenforced homes (hardcoded `files` array ↔ JSON `order` array ↔ index constants) with no reconciliation — a regenerated/reordered sidecar silently mis-crops while passing every structural + range check. `app/render/sprites.odin:47,98,176` *(security + architecture)*

### Notes (11)
- **N-1** palcheck calls `count_exact`/`count_near` twice per check (condition + printed count) — every golden rescanned. `harness/palcheck.odin:144` *(blind)*
- **N-2** palcheck's banner check derives its rect from a fabricated one-row `Crisis_State` — the blessed frame's real crisis count is never derived, so banner-height drift passes undetected. `harness/palcheck.odin:155` *(blind)*
- **N-3** `sprite_target_w` doc header names a proc that exists nowhere (the split left the old name). `app/render/sprites.odin:163` *(blind + codebase)*
- **N-4** palcheck swallows the `juice.dem` read error — a missing demo silently degrades the banner oracle instead of failing setup. `harness/palcheck.odin:162` *(security)*
- **N-5** palcheck hand-restates the camera transform for the zoomed canary — a third copy of the fit/offset math. `harness/palcheck.odin:211` *(architecture)*
- **N-6** palcheck's `fails := 0` is harness/'s only package-level mutable — against ODN-13 conduct and the `check_golden` threading precedent. `harness/palcheck.odin:35` *(architecture)*
- **N-7** bbox range check hardcodes 256 while ignoring the sidecar's `res` field. `app/render/sprites.odin:117` *(security)*
- **N-8** ci-local's gate-5 label ("— 7.1" suffix) drifts from the workflow step name, against its own step-for-step mirror invariant. `tools/ci-local.sh:59` vs `ci.yml:90` *(codebase)*
- **N-9** The zoomed lane read pins only lane_express — standard/best-effort full-alpha pixels exist in no committed artifact. `harness/palcheck.odin:221` *(tests)*
- **N-10** The B1 invariant (content_bbox == alpha bbox, exactly) has no durable automated pin — reviewers re-derive it each round. *(tests)*
- **N-11** PR body overclaims click coverage: the parity hook wires only the popover demolish path; `crisis_banner_click`/`sla_focus_click` bodies run in no committed test. *(tests)*

**Carry-forward (unchanged since r2 — zero code folds this round):** W-A route-glow halo pre-band formula · W-B palcheck header/dead consts · W-C last_sel bypass · W-D normalize dup · W-E..W-I coverage cluster (extended by W-4) · W-K puck canaries aggregate · W-L advisory gate CONCERNS (refreshed: P1 ~40% direct) · N-A..N-M · r1 leftovers (crisis consts, kx/ky, banner_y, camera-fit restatement, parity-pin → 7.3).

### Reviewer agreement
- **W-5** (security + architecture) — the roster's unenforced pairing is the highest-confidence new finding.
- **N-3** (blind + codebase) — the stale `sprite_target_w` doc.
- **W-3** independently corroborated by the orchestrator's own mechanical pass (body-vs-commit grep + gate-count check) before the wave ran.

**Verdict:** READY TO MERGE

The merged tree is green on every leg of the r2 prescription — contains #63, gate 4 clean, T1/replay byte-identical, cause chain sound, r1 B1/B2 held. The 5 warnings are polish-grade (small-band chrome edges, a docs addendum, coverage hardening) and per the cap-lifted charter do not block; fold-worthy in a follow-up, re-checked at r4 if pushed.

_Address findings and push — I re-review automatically on the new sha._
