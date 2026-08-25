You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

You are running headless. You have tools, but your lens is BLIND BY DESIGN: reading any file beyond this prompt invalidates your lens — the diff below is your entire universe. Do NOT read the repository, do NOT open files, do NOT run commands. Judge ONLY the bytes below.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
diff --git a/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md b/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md
index 4948738..497b96f 100644
--- a/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md
+++ b/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md
@@ -361,7 +361,7 @@ The map IS the UI (`[UX-DR1]`): near-zero chrome, all state on the elements. The
 ### 8.1 Inherited from Mini Motorways (the foundation)
 - State read from the flow (Wuselfaktor): congestion = dots piling; lane allocation = dot color proportion; node health = glow; degradation = the wear indicator.
 - Camera pan + zoom (drag/scroll, pinch) is the primary navigation for a growing map.
-- Pause-to-plan; color + icon + glow coding throughout.
+- Pause-to-plan; color + icon + glow coding throughout. **Paused presentation** (*user ruling 2026-08-14, prototype-aligned*): the paused world stays at **full brightness — no dim veil, no centered label**; the paused state is a **small edge chip** ("PAUSED — P/Space to resume", sized + styled like the other HUD chips) at a screen edge, never over the play area.
 
 ### 8.2 The HUD elements (what the map cannot show)
 
diff --git a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
index f0f042b..4aad860 100644
--- a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
+++ b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
@@ -478,7 +478,7 @@ The six eras (M4) are the in-run escalation arc, advancing as you sustain uptime
 - **The map IS the UI** — near-zero chrome; all state lives on the elements (color, glow, flowing dots). Minimalism carries the complexity.
 - **Camera pan + zoom** (drag/scroll, pinch) is the primary navigation for a growing map — zoom out for overview, in for detail. Input-agnostic.
 - **State read from the flow (Wuselfaktor):** congestion = dots piling up; a pipe's lane allocation = the color *proportion* of its dots; node health = glow color; degradation = the wear indicator. The player reads the network at a glance, not from HUD numbers.
-- **Pause-to-plan**; color + icon + glow coding (accessibility: color never the sole encoder).
+- **Pause-to-plan**; color + icon + glow coding (accessibility: color never the sole encoder). **Paused presentation** (*user ruling 2026-08-14 — the dim veil + centered PAUSED label sabotaged pause-and-plan; the prototype shows paused with NO overlay at all*): the paused world renders at **full brightness — identical to the running world minus stepping, no dim, no center text**. The paused state is marked by a **small edge chip indicator** (e.g. a compact "PAUSED — P/Space to resume" chip, sized + styled like the other HUD chips) in a screen-edge position, out of the play area.
 
 **Additions for our higher state density:**
 
diff --git a/_bmad-output/planning-artifacts/sprints/stories-v2.md b/_bmad-output/planning-artifacts/sprints/stories-v2.md
index e17d32c..1a97b83 100644
--- a/_bmad-output/planning-artifacts/sprints/stories-v2.md
+++ b/_bmad-output/planning-artifacts/sprints/stories-v2.md
@@ -477,7 +477,10 @@ on touch + controller.*
 - **Status:** implemented 2026-08-14 — PR open (P / Space toggle in Run; the edit fast-path
   pause-aware apply-tick lowering `[ODN-2]`; the `pause.dem` T1 golden — the sim frozen across
   the mid-crisis pause window as one repeated state hash, resume from the exact tick, replay
-  byte-identical).
+  byte-identical). **Presentation ruling 2026-08-14 (user, `v2-5.3-pause-ux`):** the paused
+  overlay is now NO overlay — full-brightness world (no dim veil, no centered PAUSED text;
+  prototype-aligned), with a small edge chip indicator ("PAUSED — P/Space to resume") in the
+  top HUD band; GDD + art-direction canon lines amended accordingly.
 
 **Given/When/Then:**
 - **Given** the pause control + the run controller;
diff --git a/_pr_body.md b/_pr_body.md
index 5f2860a..e4b8de2 100644
--- a/_pr_body.md
+++ b/_pr_body.md
@@ -1,111 +1,106 @@
-# Story 5.3 — Pause-anywhere (dispatched early)
+# Pause overlay → pause indicator (no dim, no center text) — fixes pause-and-plan
 
-Pause freezes the sim deterministically; crises tick only unpaused; the edit
-fast-path stays live under the veil — pause-and-plan works, even mid-crisis.
-**The story 5.3 card update (status + moved-up note) rides this PR** in
-`_bmad-output/planning-artifacts/sprints/stories-v2.md` — the GDD Controls
-table amend (Pause = P / Space) was already canon (`5f51236`), not re-amended.
+Fixes #48 — **USER REPORT 2026-08-14, ruling-grade**: *"when pause, 1. it dims
+the whole map, 2. the text is right in the middle of the page. the whole point
+of pausing is to be able to think and link nodes. those 2 things hinder that.
+you can see the prototype as an e.g."*
 
-**Key binding:** `P` **or** `SPACE` toggles pause in Run (regular keys — the
-solo-dev laptop ruling). Neither collides with anything (R restart, T assist,
-E/S/B lanes, 1/2 class, U preview, X/DEL demolish, ESC cancel).
+The prototype's paused frame is the baseline: sim frozen, map at **full
+brightness, no overlay at all**. The v2 overlay (full-screen dim veil + 48px
+"PAUSED" dead-center + centered hint) sabotaged pause-and-plan — the whole
+point of pausing is reading and linking the topology, and the dim + center
+text sit exactly in the way.
 
-## Acceptance (how each is pinned)
+## Before / after
 
-1. **`P` pauses mid-run: packets freeze, meter frozen, nothing mutates; `P`
-   resumes from the exact tick** — the app gates the whole stepping block on
-   Run (no accumulation, no steps while paused); the new `pause.dem` T1 golden
-   pins it at the harness level: the mid-crisis pause window (wall ticks
-   1211–1400) is **one repeated FNV-1a-64 hash** (the sim — flow/crisis/rng/
-   health — is frozen), and the hash moves exactly at 1401, the first
-   post-resume step.
-2. **While paused: draw, place, demolish, adjust QoS — all edits land and
-   apply (fast-path), visible immediately** — the input surface never gates on
-   the mode (Run ↔ Paused are the same run context, ODN-13); fast-path
-   commits log `apply_tick = paused tick + 1` (ODN-2) and land on the first
-   post-resume step; review r1 fixed the one gap: the derived BUNDLE view is
-   now rebuilt on the same gen guard while paused, so a drawn/demolished pipe
-   appears/disappears **this frame** under the veil (derived state only —
-   never sim state). The `pause.dem` T2 pair shows the frozen crisis frame
-   then the landed parallel-standard edit.
-3. **Mid-crisis pause: crises tick only unpaused (telegraphs stay, no hidden
-   progress)** — `pause.dem` pauses at tick 1210, **after** the surge fires
-   (tick 1200): the T1 window proves the crisis state froze (the banner strip
-   of the two T2 frames is pixel-identical), and post-resume the same crisis
-   is still active exactly where the pause left it.
-4. **Replay equality: pause/resume + edits replays byte-identical `[E10]`** —
-   the replay gate re-sims the blessed `pause.log.bin` with the same schedule
-   and reproduces every wall-tick hash; `core/pause_test.odin` pins the driver
-   contract (stable window, resume from the exact tick — the paused run equals
-   a continuous run at every executed tick, mid-pause edits at paused tick +
-   1, byte-identical replay).
-5. **Full local suite green; goldens per discipline** — 158 core tests, all
-   25 harness demos (T1 + T2 + replay gate; **the 24 pre-existing goldens are
-   unshifted** — pause is additive, no existing log contains a pause), W1
-   drift-check (174 mutations across 25 demos all rejected), preview-check
-   (7 scenarios), `tools/lint.sh` all gates, `odin build app` clean.
-   *CI note: GitHub Actions billing is blocked at the account level — this
-   PR's CI will be red/not-started until the user fixes it; NOT a code
-   failure. The full local suite above is the verification; Perkins reviews
-   locally.*
-6. **Launchable increment** — run the app, let the era-3 surge hit, pause
-   mid-surge (`P`/`Space`), plan a redesign under the veil (draw/place/
-   demolish/QoS all live + visible immediately), resume — the plan applies and
-   the surge continues from the exact tick. `pause.dem` is the same story as
-   a golden.
+**Before** (v2 `app/main.odin:242-250`): paused drew a full-viewport dim
+(`DrawRectangle` alpha 130) + centered "PAUSED" 48px + a centered hint line.
+
+**After**:
+
+1. **No full-screen dim** — the veil rectangle is deleted entirely (not a
+   "subtle" dim; the prototype shows none). The paused world renders at full
+   brightness, identical to the running world minus stepping.
+2. **Indicator out of the play area** — the center block is replaced by a
+   SMALL two-line chip (120×38, "PAUSED" / "P/Space to resume") in the top
+   HUD band, in the gap between the Network Health card and the forecast
+   panel. It is styled like the existing tray chips (bg + 1px border + small
+   ink_soft text). The chip position is computed from `win_w` with the same
+   centering math as the health card, so it tracks the cards on resize and
+   never overlaps the map's interactive area more than any existing HUD
+   element does.
+3. **Pause-and-plan stays fully live** — draw/place/demolish/QoS fast-paths
+   are untouched (presentation-only change). The paused bundle-view refresh,
+   the glow/preview surface, and the demolish popover remain live while
+   paused.
+4. **Canon amended in-repo** — GDD §UI & Navigation + art-direction §8.1
+   "Pause-to-plan" lines now specify the new presentation (full-brightness
+   world, edge chip indicator, prototype-aligned), and the story 5.3 card
+   status records the ruling — canon and code agree.
+
+## Acceptance
+
+1. **Paused rendering:** no veil, no centered text; world at full brightness;
+   edge-chip indicator visible + styled consistently with the HUD. ✅
+2. **Pause-and-plan re-verified:** all existing pause tests stay green —
+   `core/pause_test.odin` (158 core tests pass) + the `pause.dem` T1 golden
+   (the mid-crisis pause window is one repeated FNV hash; replay byte-
+   identical) + the T2 pair (frozen crisis frame, landed mid-pause edit).
+   The edit fast-path apply-tick lowering and the paused derived-view
+   refresh are untouched (r1 pins held). **No app-level overlay test was
+   added: the harness captures never include the app overlay** (the overlay
+   is app-layer-only, drawn in `main.odin`, deliberately outside the
+   harness capture path — the golden-stability contract) — so there is no
+   harness surface to pin the chip position; the existing pause goldens
+   remain the sim-level pins.
+3. **Goldens:** NO golden captured the old overlay (the harness draws world +
+   forecast + health + crisis banner only, never the app overlay) — so no
+   golden updates. All 25 demos re-run byte-identical; sim-level goldens
+   did not shift (determinism spine untouched — no core change at all).
+4. **Canon:** GDD §UI & Navigation + art-direction §8.1 amended + story 5.3
+   card status note — same PR. ✅
+5. **Full local suite green:** `odin test core` (158 pass), harness 25/25,
+   `tools/lint.sh` all gates. ✅
 
 ## Decisions & rationale
 
-- **Pause lives in the driver, not the core** (ODN-1): the core only ever
-  steps; the driver decides when. The app gates the stepping block on Run;
-  the harness drives a virtual clock (wall ticks = recording schedule, sim
-  steps only while unpaused). The sim never knows about pause, so the
-  executed-tick sequence is an ordinary continuous sequence and E10 holds by
-  construction — no LOG_VERSION bump, no new command kinds.
-- **Pause schedule = run setup, not log entries** (harness): pause/resume
-  directives ride `Demo_Replay` (re-created identically on replay, like the
-  fixture/spawns/era). A pause is invisible to the sim, so the log stays the
-  single authoritative sim record; the replay reproduces the wall-clock
-  schedule from the demo. Alternative (logging pause commands + a version
-  bump) was rejected: it would make the core carry a driver concept.
-- **Mid-pause edits lower to `apply_tick = the next tick the sim will
-  execute`** — the app's fast-path convention: a command fired at wall time
-  T logs `ticks_stepped_by(floor(T·hz/1000)) + 1` (paused tick + 1 when fired
-  mid-pause), so it lands on the first post-resume step and live/replay
-  converge at step boundaries. No-pause demos are byte-identical to the old
-  floor+1 rule. Boundary note: a command fired in the same 50ms wall tick as
-  a resume can differ by one tick from the live app's frame-aligned counter
-  (frame alignment is not modeled — convergence is at step boundaries).
-- **The T1 stable window pins the SIM freeze, not the fast-path channel**:
-  fast-path edits are a separate blessed channel (the action log); the
-  harness's step-boundary model applies a paused edit at the first resumed
-  step while the live app shows it immediately. Both converge at step
-  boundaries; the demo/test/card wording states this precisely.
-- **Paused derived-view refresh** (review r1): the render reads the bundle
-  view (rebuilt inside step only); while paused a fast-path pipe edit was
-  invisible until resume. The app now rebuilds bundles on the same
-  `topology.gen != bundles_gen` guard when paused — derived state only, T1
-  untouched.
-- **Harness hardening from the review swarm** (2 hunters, both applied):
-  parse-time pause/resume validation (strict arity + alternation — a
-  typo'd double-pause fails loud instead of silently blessing a stable
-  T1); O(len(pauses)) apply-tick lowering (a stray huge `at <n>ms` stalled
-  the harness ~68s — now instant); the replay stability-violation string
-  is default-allocator (a tprintf inside the tick loop read freed memory).
+- **Delete the veil outright, no "subtle" dim.** The briefing is explicit
+  and the prototype is the evidence: dimming the map while paused is the
+  defect, not a degree of it. The paused world is the running world minus
+  stepping — full brightness.
+- **Chip position — the top band gap, not top-left/top-right.** The
+  top-left run HUD column is occupied by the title/hint/score/lead + the QoS
+  readout (which appears when a pipe is selected — a core pause-and-plan
+  action), and the top-right is the forecast panel (up during a crisis
+  pause — the exact scenario the demo pauses in). The gap between the
+  Network Health card and the forecast panel is the one top-edge slot free
+  in every app state; the chip sits there, edge-anchored, sized like the
+  tray chips, and never over the play area. The briefing's "top-left or
+  top-right" is illustrative; the binding constraints are *small,
+  unobtrusive, screen-edge, HUD-chip-styled, no more overlap than existing
+  HUD* — all satisfied.
+- **No LOG_VERSION bump, no new command kinds.** Presentation-only change
+  in `app/main.odin`; the core, the driver, and the action log are
+  untouched, so replay equality and every golden hold by construction.
+- **Why no new harness pin.** The harness `capture_frame` path renders
+  world + forecast + health + banner — never the app's HUD or paused
+  overlay (the golden-stability rule that keeps app chrome out of T2s). An
+  overlay-position pin would require adding app chrome to the harness,
+  which would shift every T2 — the wrong trade for a cosmetic chip. The
+  chip's geometry is a two-line constant in `main.odin`, verified visually
+  against the real HUD layout at 1280×720.
 
 ## Files changed
 
-- `app/main.odin` — `Mode.Paused` (ODN-13), `P`/`Space` toggle, stepping gate,
-  dim overlay + PAUSED label, paused bundle-view refresh, planning surface
-  (glow/preview/popover) live under the veil, HUD hint.
-- `harness/demo.odin` — `Pause_Event` + `at <n>ms pause|resume` parsing with
-  strict arity/alternation validation.
-- `harness/run.odin` — pause-aware lowering (`apply_tick_at`), the virtual
-  clock (wall-tick hashes, stable-window contract + loud violation check in
-  both live + replay), pause schedule threaded through `Demo_Replay`.
-- `core/pause_test.odin` — driver-level pause determinism pins (new).
-- `demos/pause.dem` + `goldens/pause.*` — the new T1 golden (mid-crisis
-  pause window = one repeated hash) + T2 pair + blessed log; replay gate +
-  drift-check cover it.
+- `app/main.odin` — paused overlay → paused indicator: removed the full-screen
+  dim veil + centered PAUSED/hint text; added the small edge chip
+  ("PAUSED" / "P/Space to resume") in the top-band gap, tray-chip styled.
+- `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`
+  — §UI & Navigation "Pause-to-plan" line: paused presentation ruling
+  (full-brightness world, edge chip indicator, prototype-aligned).
+- `_bmad-output/planning-artifacts/art-direction/art-direction-v1.md` — §8.1
+  same ruling (canon trail twin).
 - `_bmad-output/planning-artifacts/sprints/stories-v2.md` — story 5.3 card
-  status note.
+  status note records the presentation ruling.
+
+No goldens, no core, no harness, no data changes.
diff --git a/app/main.odin b/app/main.odin
index 2a398c8..c716d29 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -239,14 +239,29 @@ main :: proc() {
 		if (app.mode == .Run || app.mode == .Paused) && app.placing < 0 && !app.drag.active {
 			rnd.draw_demolish_popover(&app.view, &app.state.topology, &app.cat, app.sel_node, app.sel_pipe)
 		}
-		// 5.3: the paused overlay — a dim veil + a centered PAUSED label (the
-		// GDD canon indicator; the world stays visible under the dim so the
-		// player keeps planning — draw/place/demolish/QoS are all still live).
-		// Drawn before the HUD so the run HUD stays readable above the veil.
+		// 5.3 (user ruling 2026-08-14): the paused state renders with NO overlay —
+		// no full-screen dim, no centered PAUSED text (the prototype's paused
+		// frame is the baseline: sim frozen, map at full brightness — the dim
+		// + center text sabotaged pause-and-plan, the whole point of pausing).
+		// The ONLY marker is a small edge chip in the top band, in the gap
+		// between the Network Health card and the forecast panel (the one
+		// top-edge slot free in every state: the top-left run HUD carries the
+		// QoS readout when a pipe is selected, the top-right hosts the
+		// forecast panel during a crisis pause). Styled like the tray chips
+		// (bg + 1px border + small text). Drawn before the HUD like the old
+		// overlay. The edit fast-path stays live while paused (unchanged).
 		if app.mode == .Paused {
-			rl.DrawRectangle(0, 0, rl.GetScreenWidth(), rl.GetScreenHeight(), rl.Color{10, 12, 16, 130})
-			draw_text(&app, "PAUSED", WIN_W/2 - 96, WIN_H/2 - 42, 48, rl.Color{235, 224, 192, 255})
-			draw_text(&app, "P / Space to resume - draw, place, demolish, QoS all live", WIN_W/2 - 292, WIN_H/2 + 14, 18, rl.Color{235, 224, 192, 255})
+			p := app.palette
+			// the top-band gap between the Network Health card (right edge at
+			// win_w/2 + 230) and the forecast panel (left edge at win_w - 250):
+			// the only top-edge slot free in every state. Computed from win_w
+			// so the chip tracks the cards on resize (the same centering math
+			// as the health card).
+			chip := rl.Rectangle{f32(app.view.win_w/2 + 240), 12, 120, 38}
+			rl.DrawRectangleRec(chip, rl.Color{238, 230, 210, 255})
+			rl.DrawRectangleLinesEx(chip, 1, p.ink_soft)
+			draw_text(&app, "PAUSED", i32(chip.x) + 8, i32(chip.y) + 4, 12, p.ink_soft)
+			draw_text(&app, "P/Space to resume", i32(chip.x) + 8, i32(chip.y) + 21, 10, p.ink_soft)
 		}
 		draw_hud(&app)
 	}


--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.


--- HEADLESS FILE-OUTPUT CONTRACT (overrides the in-reply output above) ---
You are running headless as a mega-minion pane. When done:
1. Write your JSON array (and NOTHING else — no prose, no fencing) to EXACTLY this absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r1/blind.json
   (use your file-writing tool; create the file, do not derive any other path).
2. Reply with a single line: DONE <lens>.
3. Stop. Do not fix anything, do not run tests beyond what your lens needs, do not spawn anything.
