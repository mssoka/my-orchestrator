## 🤖 Perkins automated review — round 4 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-7.1-visual-juice · **Reviewed sha:** `d9db462` · **Reviewers:** 7/7 completed
**Verification:** 17/19 findings confirmed against the code — 2 discarded as false-positive (0 kept as [unverified])

**Fix audit (the r4 mandate — the post-approval fold delta):** the delta `5c482df..d9db462` is **exactly the declared fold set** — 7 files, +42/−23, item-for-item with commit `d9db462`'s declaration, **zero golden churn** (binary manifest byte-identical to r3's). Each fold lands on its primary path: **W-A** both glow halos now derive from the ×2.2 `band_width` (the committed-bundle site now identical to the selection-halo formula; the candidate halo == `band_width(tier,1)`) — the missed 5th consumer is uniform; **W-C** by an alternate, in-code-documented mechanism (click hooks: `on_node_selected` fires on every junction click, `effect_pipe_selected`/`effect_node_selected` re-home unconditionally) — the r2 "re-click after banner nav" symptom is dead for mouse/touch; **W-B** consts deleted repo-wide, const-block header accurate; **N-G** ordering; **N-J** strings. The **r3-APPROVED core is untouched**: #63 containment holds, Perkins-run `tools/ci-local.sh --mac` at this sha is **10/10 green** (gate 4: 32/32 demos, zero drift from the fold; palcheck + B1 canary green), T1/replay byte-identical, r1 B1/B2 re-verified held, PR MERGEABLE. The PR body's post-r3 Review-trail section resolves r3's W-3 (its claims verified true against the head).

### Blockers (0)

None.

### Warnings (3)
- **W-1** The W-C re-home fires only in `click_select` — `right_click_select`'s pipe leg (`exec.odin:619`) and the pad `Node_Select` mirror (`:199`) write selection without the hooks, so a same-object re-select after a banner nav never re-homes on those two paths (recoverable via ESC/left-click). *(edge + acceptance + architecture)*
- **W-2** The folded W-A halo resize has zero coverage — `draw_route_glow` is reachable only from the live app loop (`main.odin:441/445`); gate 4 passed under the old AND new formulas against identical goldens, proving nothing pins the halo. *(tests)*
- **W-3** The folded W-C click-re-home has zero coverage — parity wires only 2 hooks (`parity.odin:161`), goldens run `sel=-1`; `camera_set_selection` executes in no committed artifact. *(tests)*

### Notes (7)
- **N-1** W-B fold incomplete on docs: the palcheck **file** header (`:6-7`) still claims it scans "house bodies AND roofs" — the const block was fixed, the file header wasn't. *(codebase)*
- **N-2** N-B fold incomplete: `draw_bundles`' 3.3-canon paragraph still documents the removed fiber-core draw (`:225, :229-231`; `pipe_fiber` survives only as a palette color) and "single-member renders at exactly its tier width" is false post-`band_width` (count=1 draws ×2.2). *(architecture + codebase)*
- **N-3** N-A fold incomplete: `draw_packets`' first paragraph still says "at-node packets sit on the node" beside the doorstep-fan code (`view.odin:592`). *(codebase)*
- **N-4** N-J fold incomplete: the `.memlog.md` badge still says "ci-local 9/9". *(blind)*
- **N-5** `gen_sprites.py` `aim()`: unscaled z + fixed target → tilt varies 53.5°–61.4° across pads 1.12–1.55, never the commented "~66 deg" (output was style-gate-approved; tool-comment + geometry nit). *(blind)*
- **N-6** The band−2·gutters inner width is restated inline in the rider path (`view.odin:301` vs `:674`, an acknowledged "mirrors exactly" copy) — extract `band_inner_width`. *(blind)*
- **N-7** N-G's reorder is unpinned and currently inert — `effect_cancel` → `camera_set_fit` reads no selection; pin it when a selection-reading consumer lands. *(tests)*

**Carry-forward (unchanged, to the next story by declared choice — not re-filed):** r3 W-1/W-2/W-4/W-5 + N-1..N-11 · r2 W-D, W-E..W-I, W-K, W-L (gate CONCERNS refreshed), N-C, N-D, N-F, N-H, N-K, N-L, N-M · r1 leftovers. **Fixed this round:** r2 W-A/W-B/W-C/N-G (+N-A/N-B/N-J partially), r3 W-3, r2 N-I's gate-count half.

### Reviewer agreement
- **W-1** (edge + acceptance + architecture) — the hook-coverage residue is the highest-confidence new finding.
- **N-2** (architecture + codebase) — the fiber-comment residue.
- Rejected on verification: a blind "start_run auto-zoom" claim (start_run clears input selection at `main.odin:531-532` before the `last_sel` reset) and the third occurrence of the "harness.sh palcheck" claim (generic pass-through; verb lives in `harness/main.odin:58`; gate 5 green through the wrapper in this round's Perkins run).

**Verdict:** READY TO MERGE

The fold delta is exactly the declared set, each fold lands on its primary path, and the approved core is mechanically untouched (10/10 gates, 32/32 demos, zero golden churn, B1/B2 held, MERGEABLE). The 3 warnings are fold-residue grade (two non-click select paths + unpinned fold visuals) — per the cap-lifted charter they do not block; fold-worthy in a follow-up story alongside the carried set.

_Address findings and push — I re-review automatically on the new sha._
