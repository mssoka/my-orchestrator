## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-v2-mechanics-the-box · **Reviewed sha:** ad8afca · **Reviewers:** 6/7 completed
**Verification:** 31/31 findings confirmed against the code (28/28 lens findings + 3 Perkins-mechanical) — 0 discarded as false-positive, 0 kept as [unverified]

> **MEGA-DIFF disclosure:** the canonical diff (91,477 lines / 248 files / 4 commits) was generated locally as `git diff 03dd6f8..ad8afca` (byte-verified against the saved round artifact) — `gh pr diff` is API-capped for this PR. Per the chunking protocol: the full 7-lens wave ran on the CODE chunk (27 files, 2,731 lines: core/harness/app/data/demos); the goldens/docs bulk (88,746 lines) got mechanical bulk-verification (inventory cross-check, fold-check, stats-check, econ-check, input-parity, palcheck reproduction). Chunked, not dropped.
>
> **Degraded-lens disclosure:** the blind lens failed twice (`length` output-cap on glm-5.3-flash, both attempts; re-dispatched once per protocol) → 6/7 lenses completed. Findings are plentiful and the verdict rests on verified blockers, so the degraded guard does not force a comment-only review.

### Blockers (2)

1. **`odin test app/input` SEGFAULTS at this sha — a regression this PR introduced.** `input.draw_drag_on_a_node_never_pans` dies with `Segmentation_Fault` (13 tests, 1 failed). At the base commit the same suite is 13/13 green (verified both). Mechanism: the PR adds `Input.state` and routes the draw/place commit fast paths through `pp.box_apply_edit(inp.state, …)`, which derefs `state.box_enabled` unguarded; the pre-existing camera fixture (`cam_test_ctx`, camera_input_test.odin:56-63) never wires `ictx.state`. The gate table's "`odin test app` 51/51" is the parent package only — it never runs the `app/input` subpackage suite, which is how a segfault shipped through a green gate table. [architecture, codebase; independently reproduced by Perkins]
2. **Advisory test gate: FAIL** [tests lens rubric: a P0 suite cannot execute + the flagship refusal path is both silent and untested]. Resolves when #1 is fixed and the warning-class coverage rows below land.

### Warnings (8)

1. **Box refusal on the placement path is silent** (`app/input/exec.odin:156-160`). `commit_draw` surfaces refusals as toasts ("the Box's 'no' must TEACH"); `Place_Release` swallows `err != .None` with no feedback. The PR's own era3-slope evidence shows the Era-3 bind is **piece-side** (`piece-starved=true`) — so the record's flagship "the box starts saying no when it matters" moment is invisible in the shipped app. **5-lens agreement** (edge, acceptance, architecture, codebase, tests). Mirror the `last_reject` handling; add a test row.
2. **Pre-commit surfaces validate topology only** (`app/render/assist.odin:277`): the R3 route preview and placement ghost can bless actions the Box will refuse — plan into an invisible refusal, then hear nothing (see #1). [edge]
3. **`crisis-stall` never injects a crisis** (`harness/econ.odin:358-361`): it's a different-seed era-3 run; no crisis fires, so record Q7's crisis→slower-dots seam — the exact interaction the record demands a sim run for — is asserted only where the clamp makes it trivially true. [architecture; verified]
4. **`stats_destroy` leaks `rec.box.pieces`** (`core/stats.odin:195` alloc vs `:378-384` destroy): one dynamic array per tick on box-on runs; the app emits at 20 Hz. (The 17.5 KiB leak notices in `odin test core` output are this surfacing.) [security, architecture, codebase]
5. **Same-spool resplice "never refuse on a short spool" invariant untested** (`core/box.odin:226-233`): documented as a FORGE-#2 tripwire cousin, only the cross-spool case is covered. [tests]
6. **Dead-stock spool guard has no rejection test** (`core/catalog.odin:1549-1551`): the fail-fast check that caught the era-2 fiber bug is unpinned — a revert ships green. [tests]
7. **`input-parity` gate is RED at this sha and "ALL `.t1` manifests re-blessed" is false for 2 manifests** (`goldens/input_parity_draw{,_wide}.t1` still carry the pre-PR catalog hash; the gate is absent from the gate table). Perkins re-blessed and re-ran: **27/27 PASS** — the divergence is the sanctioned catalog fold, zero input-path regression, so this is disclosure accuracy, not a defect: run `harness input-parity save`, commit the 2 manifests, add the gate to the table. [Perkins mechanical]
8. **`APP_ERA=3` leaves ruling 7's era-1/2 brush tutorial unreachable in the shipped app** (`app/main.odin:45`, verified). The PR discloses this honestly as a design-level flag — **surfacing it so the user decision happens at merge**, not after. [acceptance]

### Notes (12)

- **box_spine goldens carry 2 orphan frames** — `119500ms.png` is fully BLACK (byte-identical to what `map-preview` renders on this machine) and `120500ms.png` matches no `capture at` command; the harness verifies only commanded captures, so neither is gated. PR says "4 T2 beats"; the dir has 6 files. [Perkins mechanical]
- **`test_box_floor_pin`'s unsigned bound can't catch floor deletion** (`box_test.odin:360`): Perkins' code-level drop-the-floor mutation left this pin GREEN (u64 wrap satisfies `>=`) — the RED came from the clamp-equality and mutation-legs tests. Harden the pin. [Perkins mechanical]
- **palcheck red is environmental — independently PROVEN**: head 61 FAILED; base committed goldens 31; base + local re-bless **61 — exactly the PR's claim**. Not caused by this PR; the golden-source-of-truth decision remains open (PR disclosure #2). [acceptance + Perkins reproduction]
- Box-before-topology validation order reports the material error for doubly-invalid draws (documented intentional order). [edge]
- PR prose "two-sided bind" overstates the era-3 row (piece-side only; refusals=0). [acceptance]
- Era-3 econ scenarios can't reach the sustain/wire phases (segment budget cap) — consistent with the PR's bot-model caveat. [security]
- `Cmd_Era_Advance` validate+latch duplicated in both `box_apply_edit` branches. [architecture]
- Router short-name mapping duplicated (`draw_box_hud` / `draw_tray`). [architecture, codebase]
- Dead slot lookup in `box_charge`'s Demolish_Node case. [codebase]
- Unpriceable-command pass-through branches untested (0 rows). [tests]
- Stats box section (B/J rows, box-on CSV) has no unit coverage. [tests]
- The 2^40 wrap bound and era_introduced piece-cap catalog guards lack rejection rows. [tests]

### Reviewer agreement

- **Silent placement refusal** — 5 independent lenses (edge, acceptance, architecture, codebase, tests).
- **stats leak** — 3 lenses (security, architecture, codebase). **Segfault** — 2 lenses (architecture, codebase), then mechanically reproduced. **Short-name duplication** — 2 lenses.

### Gates re-run by Perkins (local = merge ground truth)

| Gate | Perkins re-run | PR claim |
|---|---|---|
| `odin test core` | ✅ 295/295 (5.2s) | 295/295 |
| `odin test app` | ✅ 51/51 | 51/51 |
| `odin test app/input` | ❌ **1 SIGSEGV** (base green — regression) | not in gate table |
| mutation: delete-the-cap | ✅ RED ("no brush observed") → restore GREEN | claimed |
| mutation: drop-the-floor | ✅ RED (clamp + mutation-legs) → restore GREEN | claimed |
| `econ-check` | ✅ all verdicts hold (byte-matches PR table) | claimed |
| `stats-check box_spine` | ✅ live==replay byte-identical (970,725 B) | claimed |
| `fold-check` (boot prev values) | ✅ PASS — catalog fold alone (bytes 33..40) | claimed |
| `drift-check` | ✅ 360/360 rejected | claimed |
| `input-parity` | ❌ FAIL at head → save → ✅ 27/27 (fix = 1 command) | absent from table |
| `palcheck` | 61 head / 31 base-committed / **61 base-reblessed** — environmental, disclosure reproduced | disclosed |
| goldens inventory | ✅ 219/231 = full re-bless (12 unchanged = `_reports` + the 2 stale parity manifests) | claimed |

CI note: the PR's Actions "verify" runs show the billing-block signature (5s / zero logs / runners never started) — note-only per standing ruling; local gates are the merge ground truth, which is why the subpackage suite gap matters.

**Verdict: NEEDS CHANGES**

_One blocker (the segfaulting input suite — fix the wiring or guard, then put `odin test app/input` in the gate table), plus the placement-feedback teaching gap the record's own doctrine depends on. The economy core is genuinely solid: every mutation leg bites, the fold/stats/econ evidence reproduces byte-for-byte, and the disclosures in this PR are unusually honest — fix the surface and the suite, and this lands. Push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
