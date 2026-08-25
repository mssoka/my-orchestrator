## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-5.8-qos-panel · **Reviewed sha:** `ea1026d` · **Reviewers:** 7/7 completed
**Verification:** 25/25 findings confirmed against the code — 0 discarded as false-positive, 0 kept as [unverified] (2 severity adjustments, both downward, rationale inline)
**Diff handling:** canonical diff = 33,723 lines / 80 files; the golden churn (~30.9k lines: 27 `.t1` manifests, 27 `.log.bin`, 4 `.png`) was split out of the lens diff and verified **mechanically by Perkins at byte level** instead — see Verification log below. All lenses reviewed the identical 2,599-line code diff.

### Verification log (Perkins, run at the reviewed sha)
- `odin test core` → **167 tests green** · `tools/harness.sh run` → **27/27 demos green incl. the replay gate** · `tools/lint.sh` green · `odin build app` clean.
- **Golden fold (byte-level, vs merge-base `38929d2`):** all 24 pre-existing no-QoS `.log.bin` differ at exactly the version byte (@4, 3→4) + the 8 catalog-hash bytes (@17–24) — nothing else. `qos_emphasis.log.bin` additionally re-encodes its 2 `SET_EMPHASIS` records — decoded record-by-record: v3 presets {1,2} → v4 weights {(4,2,1),(1,2,4)} = **exact preset equivalence** (the documented payload evolution, no semantic drift). New logs: `qos_auto` = 50/30/20 (+2 lane assigns), `qos_manual` = 60/25/15. All pre-existing PNGs byte-identical; only the 2 new demos' 4 PNGs added. All `.t1` header changes = `catalog_hash` only.
- **Load-bearing guards:** replay equality [E10] holds by construction (auto-ladder + manual editor both write through the one `Cmd_Set_Emphasis`; v3 logs rejected by the v4 version gate); ladder semantics exact (in-play = assigned ∪ Standard; 70/30; 50/30/20; untouched pipes keep the default preset — pinned in `qos_test.odin`); E6 never-drop by construction on the auto path (never-drop lanes folded into in-play, incl. catalog defaults — pinned with a banking-class test); no cycle deadlock on zeroed lanes; scope guard holds (no new command kinds).

### Blockers (0)

### Warnings (6)
1. **[tests] App-side panel lifecycle has zero automated pins** — clobber gate (manual pipe keeps weights on assignment), derived AUTO/MANUAL mode, revert-to-auto, auto-follow trigger. Verified: no pin at any tier (the demos hand-pin outcomes). Demoted from the tests lens's blocker per this repo's own precedent (5.7 r1: app-side zero coverage = warning; the app layer's test story is T2 goldens) and because the P0 core contract is 100% pinned and Perkins verified the gate logic correct by direct read. Still worth extracting the mode/gate decision into a pure, pinnable proc — the clobber bug class already happened once during development.
2. **[blind] PR body overstates the golden fold** — "every existing `.log.bin` diff = version byte + catalog-hash only" is false for `qos_emphasis.log.bin` (its action-log records legitimately re-encode). Scope the claim to no-QoS-edit runs, as `serialize.odin`'s comment already does.
3. **[codebase+tests] No v3-log rejection pin** — every prior LOG_VERSION bump added an old-version pin; 5.8 is the first same-tag payload reinterpretation, so a future v3-compat shim would pass the existing v2/v99 pins. Cheap, precedent-following fix.
4. **[tests] Panel edge behaviors unpinned** — never-drop cycle guard, ±5 nudge clamp, preset bounds.
5. **[tests] Advisory test gate: CONCERNS** (lens graded FAIL; re-graded — its own evidence shows P0 = 100%, overall ≥80%; the P1 gap is the app-panel logic of warnings 1/4).
6. **[blind] Committed review transcripts are stale snapshots** — `_bmad-output/reviews/5.8-qos-panel/{adversarial-general,edge-case-hunter}.md` describe pre-fix bugs (manual clobber, dead `Invalid_Preset`, raylib-sw symlink) in present tense with merge-blocking verdicts that no longer apply to this tree.

### Notes (16)
1. Spec bookkeeping: the goldens re-bless task is unchecked, `review_loop_iteration: 0`, empty change log — while the PR ships the re-bless.
2. Spec drift: says `0 ≤ w ≤ MAX_WEIGHT` + "sums" validation + a 4-param `qos_auto_weights(t, cat, pipe_slot, pipe_id)`; the loader enforces 1..MAX_WEIGHT, no sum check, and the proc is 3-param. Also names `app/render/qos_panel.odin`; it lives at `app/qos_panel.odin`.
3. `qos_auto.dem` hand-pins the ladder output (`weights 1 50 30 20` authored, not computed) — by design (computation is core-tested), but retuning the ladder leaves this golden green with stale splits.
4. Harness lowers same-tick `weights` before `lane` intents (run.odin order), inverting demo-file and app order — benign for all-positive sets (E6 validation unaffected); latent ordering nit.
5. Right-click is not swallowed by the panel rect (left-click is) — right-clicking over the panel re-selects the pipe beneath and closes the editor.
6. **[blind+codebase]** Right-click select resets `sel_class`; left-click `click_select` preserves it — the highlighted 1/2-key row differs by selection path.
7. `reject_label` hardcodes "0..1000" (== MAX_WEIGHT today — accurate, but duplicates the constant in player-facing copy).
8. **[blind+tests]** Ladder upper-bound branch (`> MAX_WEIGHT`) has no fail-fast test case.
9. The "second pipe is independent" assertion in `test_qos_auto_weights_ladder` can't fail — an unknown/untouched pipe id returns the default preset either way.
10. The rejection toast draws over the panel's bottom button row (y = bottom−18 inside the actions band).
11. Never-drop lane cycle can log a redundant self-assignment when the current lane is the only positive one (`1..=LANE_COUNT` reaches `next == cur`).
12. Panel buttons render at 13px and preset chips at 12px vs the PR body/spec "≥ 14px" legibility claim.
13. `MANUAL` label flips on editor-open with zero weight changes — the file's own header comment says `qos_editing` "only controls whether the editor rows are expanded," contradicting `qos_mode_manual`.
14. The `weights` directive range-checks weight values before narrowing but casts the u64 pipe id to u32 unchecked (silent-wrap class the same hunk guards against for weights).
15. The validate→apply→append→toast emit block is duplicated 4× in `qos_panel.odin` (plus main.odin's sites) — extract one `app_emit_cmd` helper.
16. `serialize.odin`'s version-history header block and the `CMD_TAG_SET_EMPHASIS` tag comment weren't extended for the v4 weights payload.

### Reviewer agreement
- Right-click/left-click `sel_class` asymmetry — [blind, codebase]
- v3-log rejection pin missing — [codebase, tests]
- Ladder `> MAX_WEIGHT` branch untested — [blind, tests]

**Verdict:** READY TO MERGE

_All load-bearing guards verified: replay equality [E10] by construction + mechanical fold proof; exact ladder semantics; E6 never-drop by construction; no cycle deadlock; scope guard holds; full local suite green at the sha. The 6 warnings are doc-accuracy and coverage-pin follow-ups — none block._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
