# Sheep shard — field-notes (dream-2026-08-29)

Read (full unless noted):
- packet-plumber-v2-look-zoom-language.md (6 lines)
- packet-plumber-v2-viscomm-regression-audit.md (5 lines)
- packet-plumber-v2-congestion-read-a1.md (5 lines)
- packet-plumber-v2-mechanics-the-box.md (27 lines)
- packet-plumber-lang-safety-research.md (15 lines)
- packet-plumber-v2-box-crash-third-spawn.md (5 lines)
- dream-2026-08-27.md (13 lines — file is shorter than the ~15-line tail window, read whole)

Live store grepped read-only: docs/minion-field-notes.md (1002 lines, read in full), AGENTS.md.

## Candidates

### C1 — Demo-directive zero-value trap: normalize absent numerics AT PARSE TAIL
- Example: packet-plumber-v2-look-zoom-language, 2026-08-27 — "a new numeric Demo field with '1.0 = default' semantics still zero-inits to 0.0; `zoom 0` drove `scale = fit*0` and the map grid loop drew ~forever (2.5h silent 'suite run')".
- Two facets: (a) any numeric directive with a nonzero default must be normalized at the parse tail (zero-init betrays "absent"); (b) forensic signature — a hung `harness run` with an EMPTY log = sample the process, look for an unbounded render loop.
- Novel? NOVEL. The store has zero-default traps (zeroed thresholds 08-13; MIRROR-FIXTURE 08-21) but not the parse-tail-normalize rule or the hung-run-empty-log signature.
- Target: minion-field-notes.md.

### C2 — Starved-fixture vacuity via zero geometry data (bbox-dependent Views)
- Example: packet-plumber-v2-look-zoom-language, 2026-08-27 — "unit-test Views that call sprite_puck_target … MUST hand-set `v.sprites.bboxes[6..8][2]` — zero bboxes make every ROUTER endpoint's drawn size 0, which zeroes the covenant cap and VACUATES the whole sweep (it passed crushed at cap 0)".
- Novel? NEW FLAVOR of a covered class — the starved-gate vacuity lineage (08-19 "a concentration pin needs a CREDIT-RICH fixture… a starved gate, vacuous"). This is the geometry-data variant: zero fixture data zeroes the cap the sweep is measured against. Addendum line, not a new entry.
- Target: minion-field-notes.md (vacuous-pin entry).

### C3 — Trimmed-blit hides under-sprite decoration; blend scans need the TRUE underlay
- Example: packet-plumber-v2-look-zoom-language, 2026-08-27 — "DrawTexturePro blits the CONTENT bbox tight, so any dot smaller than the footprint hides completely … The read is a HALO: radius > 0.5× footprint. Also: predicted blend scans need the actual UNDERLAY color — probe map-preview with the correct fit offset (OX=(win−world×fit)/2), the seed-7 land tint is (239,228,186), not canvas."
- Novel? NOVEL — extends the "render-surface realities defeat pixel gates" entry (08-25/26) with the trimmed-blit invisibility + the underlay-color/offset prediction rule.
- Target: minion-field-notes.md (render-surface entry addendum).

### C4 — Visual-regression audits resolve MECHANICALLY: motion-strip + per-era goldens
- Example: packet-plumber-v2-viscomm-regression-audit, 2026-08-27 — "'did effect X die' audits on PP resolve mechanically with `harness motion-strip` + a fixed-pixel time-series … golden PNGs in per-era worktrees are free BEFORE/AFTER evidence (each worktree's `goldens/` is its own era's blessed render — compare those before building anything)".
- Novel? NOVEL. Grep: no "motion-strip" or "per-era" in either store file.
- Target: minion-field-notes.md.

### C5 — A user's "it used to pulse" memory can be PERCEPTION of static code
- Example: packet-plumber-v2-viscomm-regression-audit, 2026-08-27 — "the 4.1 congestion halo never pulsed; the read came from level-flicker (amber↔red re-tint) + ribbon mass. Trace the MECHANISM and the CANVAS separately or you audit the wrong thing (severed-code hunt found nothing…)".
- Novel? NOVEL as stated — sibling of root-cause-first, but the user-perception-vs-code split + the two-track (mechanism/canvas) audit rule is new.
- Target: minion-field-notes.md.

### C6 — Lavish per-row ruling craft: one radio form + one Queue button per row
- Example: packet-plumber-v2-viscomm-regression-audit, 2026-08-27 — "lavish input playbook per-row radio forms + one Queue button each collected a clean per-row ruling (R1 restore-via-A1 arrived as a single tagged keep-leave prompt); a Send-&-End session delivers the final feedback once on the next poll — no extra polling rounds needed after it."
- Novel? NOVEL input-side lavish craft (the store's lavish entries cover verdict ground-truth in state.json + mock galleries, not per-row form design).
- Target: minion-field-notes.md (lavish section).

### C7 — Palcheck legs returning exactly the scan window = measuring ALONG the feature
- Example: packet-plumber-v2-congestion-read-a1, 2026-08-28 — "when a band-measure palcheck leg returns exactly your scan half-window count (2·half+1), the scanner is measuring ALONG the feature, not across it — assert a predicted pixel count from the draw's own math first (dump the column) before trusting the leg."
- Novel? NOVEL measurement-direction signature; the "predict the count from first principles before trusting the leg" precept generalizes.
- Target: minion-field-notes.md.

### C8 — Stride a BEFORE harness first, then mutate (single-worktree evidence ordering)
- Example: packet-plumber-v2-congestion-read-a1, 2026-08-28 — "stride the evidence harness FIRST (bin/harness_before from HEAD + view-only extension), then mutate — the corpus-freshness + mutation-leg ordering (before-strips → change → re-bless → after-strips) made every A1 claim mechanically checkable without a second worktree."
- Novel? NOVEL — the bin/harness_before pattern isn't in the store (the per-commit re-bless loop of 08-22/23 is adjacent but different).
- Target: minion-field-notes.md.

### C9 — Odin `#partial switch`: a `case:` below the default silently never runs
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "Odin `case:` in a `#partial switch` swallows EVERYTHING after it — a case inserted below the default silently never runs (a demolish refund priced zero and the tests still mostly passed). Keep special cases ABOVE the default; a grep for `case:` adjacency belongs in review."
- Novel? NOVEL (the 08-19/21 addendum mentions `#partial switch` exists; the case-order trap is new). Belongs with the Odin micro-traps collection.
- Target: minion-field-notes.md.

### C10 — Never price from POST-apply topology; refund tests must demolish a NON-ZERO id
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "pipe_slot/node_slot SKIP DEAD entities and fall back to slot 0 — tombstone-then-price refunds the wrong tier/span (or nothing)… validate snapshots the pre-edit facts… A test demolishing pipe id 0 MASKS the bug (slot 0 is the accidental right answer) — always demolish a non-zero id in refund tests."
- Novel? NOVEL hazard class (sibling of the 08-26 index-keyed-derived-state entry but distinct: pricing-snapshot + id-0-masking fixture flavor).
- Target: minion-field-notes.md.

### C11 — T2/palcheck goldens are ENVIRONMENT-BOUND: reproduce the BASE before blaming your diff
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "the pristine base (03dd6f8) re-blessed locally reproduces palcheck 61-fail exactly (committed base goldens: 32)… Before chasing a palcheck/T2 regression, re-bless the BASE in a scratch worktree and compare — if base reproduces, it's the render environment, not your diff; disclose and let the human/CI decide the golden source of truth."
- Novel? NOVEL — the base-reproduction control for environment drift is not in the store.
- Target: minion-field-notes.md.

### C12 — `.gitignore` trailing-slash patterns don't match SYMLINKS
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "`.gitignore`'s `_bmad/` does NOT match the worktree bootstrap SYMLINK (trailing slash matches directories only) — `git add -A` stages the symlink; the repo .gitignore now carries a bare `_bmad` line too."
- Novel? NOVEL (git-semantics trap; the AGENTS.md `_bmad` symlink gotcha is about rsync bootstrap, different surface).
- Target: minion-field-notes.md.

### C13 — Fail-fast TEST TABLES can be vacuously green; audit by mutating one expectation to nonsense
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "a per-file reject helper that omits ONE catalog source makes the loader die in an EARLIER file, and the helper's 'wrong file' branch returns without ever checking the rule — every row passes forever… Fixing the helper then exposed ~40 stale expectations (rows written against the key NAME, the loader rejects with the MESSAGE substring)."
- Novel? NEW FLAVOR of the covered vacuity lineage (fail-fast short-circuit + unchecked wrong-file branch). The mutation audit ("if the suite stays green, the table is dead") is the standing mutation-leg doctrine applied to tables; the stale-expectation fallout sub-lesson (want = the MESSAGE substring, copied from loader source) is new.
- Target: minion-field-notes.md (vacuous-pin entry addendum).

### C14 — Python needle/patch craft: verify "applied" by grepping for the INSERTED comment
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "a python needle with copied alignment silently no-ops across helpers. When a patch 'applies' but grep finds no trace, the needle matched a DIFFERENT helper's block; verify by grepping for the inserted comment." Plus three needle-brittleness modes: "`replace1`'s 4th arg is a COUNT, not an occurrence index; …old needles stop matching and their rows silently no-op… loader messages carry EM-DASHES."
- Novel? NEW FACETS on the covered edit-anchor craft (08-13/08-23 em-dash + replace traps). The "grep for the inserted comment" verification + replace1-count + retune-breaks-needles are new.
- Target: minion-field-notes.md (edit/anchor craft entry addendum).

### C15 — Cross-machine blessing splits the corpus (R/B conventions) — re-bless ALL from ONE machine
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 — "two machines blessing the same corpus with different R/B raster conventions splits the corpus (Perkins census: 116/117 swapped vs 1 warm) — after ANY cross-machine merge, re-bless the ENTIRE corpus from ONE machine and run the full T2 loop twice consecutively before trusting it."
- Novel? NOVEL ops rule (rides the T2/rlsw entry as an addendum).
- Target: minion-field-notes.md.

### C16 — The R/B-swapped-backend trap has a SILENT self-consistent-green flavor (ADDENDUM to existing entry)
- Example: packet-plumber-v2-mechanics-the-box, 2026-08-28 (THE BIG ONE) — "NEVER bless T2 goldens with `odin run harness` directly… the frames render, the T2 compare is self-consistent, the suite goes green, and NOTHING looks wrong until a blob-level census finds every frame carrying the swapped convention… Symptoms: palcheck raster legs fail with 0 px of EVERY canon hex; 'stale' goldens that re-bless to byte-identical wrong frames… The fold-check/T1 gates stay valid… which is exactly why the trap is invisible to the T1-only sweep."
- Novel? ALREADY COVERED for the LOUD flavor at minion-field-notes.md lines 288–303 (08-11 + 08-13 addendum: "produces R/B-SWAPPED golden frames (921600/921600 pixel diffs that look like a render bug, aren't)"). The SILENT flavor (a whole corpus blessed wrong passes its own T2; T1-sweep invisibility; the symptom list) is NOT in the store — and the trap RECURRED 08-28 despite the note, so the addendum should be prominent, not buried.
- Target: minion-field-notes.md (T2/rlsw entry addendum).

### C17 — Odin invalid-free crash forensics cluster (recipes, not vibes)
- Examples: packet-plumber-lang-safety-research, 2026-08-28 — "macOS libmalloc aborts lose the stack above `_heap_free` in the .ips — a -debug build + `breakpoint set -n malloc_error_break` under lldb recovers the full Odin stack in one run"; "Odin dynamic arrays carry their allocator in the header… a missed field in shadow_clone alias-frees the LIVE buffers silently; the class is caught deterministically by core:mem Tracking_Allocator (bad_free_callback carries file:line), not by waiting for the abort." And packet-plumber-v2-box-crash-third-spawn, 2026-08-28 — "grep the repro surface for by-value dynamic-array/struct copies feeding a destroy — `clone := src^` + `run_destroy(&shadow)` was the whole bug; `odin test` beats libmalloc for localizing invalid frees."
- Novel? PARTIALLY covered — the 08-26 shadow_clone entry name-drops malloc_error_break in passing; the full recipes (-debug+lldb, Tracking_Allocator bad_free_callback, grep-for-by-value-copies-feeding-destroy) are new.
- Target: minion-field-notes.md (08-26 entry addendum or a small forensics cluster entry).

### C18 — The shadow_clone rule grows a PIN-LINE half (box-ON fixture + raw_data pins)
- Example: packet-plumber-v2-box-crash-third-spawn, 2026-08-28 — "EVERY new Run_State dynamic array must add a clone line AND a pin line in test_spawn_fx_shadow_clone_box_owns_every_array — the box-ON fixture + raw_data pointer pins are what make a missed field CI-visible (box-OFF fixtures hide it: nil headers delete harmlessly; skip only raw_data==nil in the pin, len==0 hides allocated backings)."
- Novel? NEW FACETS on the covered 08-26 shadow_clone clone-list rule (the pin test, box-ON vs box-OFF visibility, len==0-hides-allocated-backings).
- Target: minion-field-notes.md (08-26 entry addendum).

### C19 — Memory-ownership mutation gates pin OWNERSHIP directly, never allocator behavior
- Example: packet-plumber-v2-box-crash-third-spawn, 2026-08-28 — "`odin test` bad frees are REPORTED not fatal, and temp_allocator frees are no-ops the leak report cannot see — a mutation gate must pin ownership directly (pointer compares), never depend on allocator abort/leak behavior."
- Novel? NOVEL vacuity flavor (allocator-behavior-dependent gates are vacuous-by-construction) — rides the vacuous-pin lineage.
- Target: minion-field-notes.md (vacuous-pin entry addendum).

### C20 — READ-ONLY repro recipe: rsync to /tmp + env-gated frame-script driver
- Example: packet-plumber-lang-safety-research, 2026-08-28 — "rsync the repo to /tmp (exclude _bmad), env-gate a frame-script driver in app/main.odin copying the PP_NOC_E2E injection pattern (append Device_Events after polls, before dispatch_frame) — drove real drag-connects and caught the box crash RED, then proved the 2-line fix GREEN (8 connects) same evening."
- Novel? NOVEL minion-facing pattern (the AGENTS.md rsync-`--exclude='_bmad'` gotcha is the orchestrator bootstrap sibling; the read-only-job repro recipe is new).
- Target: minion-field-notes.md.

### C21 — palcheck render-only fixtures: arrays are len 0 until warnings_update; E26 fixture limits
- Example: packet-plumber-v2-congestion-read-a1, 2026-08-28 — "`crisis.pipe_congestion` has len 0 until warnings_update runs; `resize()` + explicitly zero the grown slots to `.None`, and remember E26 rejects terminal→terminal pipes in fixtures (mirror §7: terminal→router)."
- Novel? NOVEL specifics; same family as the 08-21 PP fixture-traps entry — a one-line addendum there, or an anecdote. Borderline.
- Target: minion-field-notes.md (fixture-traps entry addendum) — small.

### C22 — herdr pane resize --amount is a FLOAT fraction (0–1)
- Example: dream-2026-08-27 (Bob's shard) — "herdr pane resize --amount is a FLOAT fraction (0-1): integer amounts clamp the split to extremes (0.1 / 0.6 ratios observed) — 0.27 moved the boundary cleanly; verify with `herdr pane layout` after each call."
- Novel? NOVEL detail — the AGENTS.md lens-tab layout doctrine ("resize semantics are empirical…") lacks the float-fraction fact. Addendum to that gotcha.
- Target: AGENTS.md (lens-tab layout doctrine addendum).

### C23 — Dream coverage-gap detection: marker jumps + content-dating, never mtimes
- Example: dream-2026-08-27 (Bob's shard) — "A marker that jumps WITHOUT a dream row (the 08-25 DSH-interlude advance) flags a coverage-gap window — date sources by CONTENT (git log per file, shard headers), never mtimes: a git checkout/restore normalizes every mtime to the same minute."
- Novel? NOVEL dream-process craft — belongs in the dream template/playbook dream section (Bob-facing), not the two stores.
- Target: playbook 'Dreaming' section / `_template-dream.md` (Bob-facing) — neither store.

### C24 — Sheep handovers via brief-FILES + one-line pointers
- Example: dream-2026-08-27 (Bob's shard) — "Sheep handovers via brief-FILES + one-line pointers: 3/3 delivered clean, first try, zero quoting-class incidents (the KYLE spawn-craft law applied to sheep dispatch)."
- Novel? ALREADY COVERED by extension — the AGENTS.md KYLE craft law ("prompts to FILES (shell quoting eats multi-line)") generalizes; this is just the sheep application. Optional one-clause addendum to the dream template, nothing more.
- Target: neither (covered).

## Stale/duplicate live entries this supersedes

None contradicted outright. Three live entries earn ADDENDA (quoted live text):

1. minion-field-notes.md lines 288–303 (T2/rlsw entry): the live framing covers only the LOUD flavor — "renders a SOLID BLACK frame headless" / "produces R/B-SWAPPED golden frames (921600/921600 pixel diffs that look like a render bug, aren't)". C16 adds the SILENT self-consistent-green flavor + symptom list; C15 adds the cross-machine split rule. NOTE: the trap recurred 08-28 despite the entry — a prominence problem, not a coverage problem; consider leading the entry with the NEVER-bless-direct rule.
2. minion-field-notes.md 08-26 shadow_clone entry ("EVERY new step()-touched dynamic array must be added to spawn_fx.odin's shadow_clone clone list AND its flow_init mirror… (malloc_error_break backtrace finds it…)"): C17/C18 add the pin-line half, box-ON fixture visibility, raw_data-vs-len==0 pinning, and the Tracking_Allocator deterministic catcher.
3. minion-field-notes.md 08-13 golden-discipline (a) ("catalog edits are GOLDEN-POISONED — `cat.hash` folds every catalog byte… wire new rules as core consts until a legitimate re-bless"): the mechanics-the-box shard's "NEVER edit data/*.json comments after a re-bless — settle all data edits FIRST, then bless once, then freeze" is the same rule restated (comments ARE catalog bytes). Already covered; the shard confirms it. Optional strengthening: name comments explicitly + the settle→bless→freeze ordering.

## Anecdotes (single-sighting — watch items)

- look-zoom-language 08-27: clearing `app.pullback` does NOT stop autonomous camera motion — camera_update's ease runs unconditionally (the flag only sets the rate); a "stop the breath" site must freeze cam_zoom_to/cam_wx_to/cam_wy_to at live values (the pre-existing N11 toggle still carries the latent behavior — deferred). Repo-mechanism fact; watch for the N11 follow-up.
- mechanics-the-box 08-28: harness `stats-check <demo>` writes its streams under `bin/` — a fresh worktree has no `bin/` dir and fails "cannot read live stream: Not_Exist"; `mkdir -p bin` first. Small worktree-bootstrap fact.
- mechanics-the-box 08-28: hand-rolled PNG de-filter works but the channel-stride must match the color type (ch=4 RGBA vs 3 RGB) — a step-3 walk over RGBA fabricates phantom diffs. Use PIL when available; pin the tool. Small craft; sibling of "compare DECODED PIXELS, never file bytes".
