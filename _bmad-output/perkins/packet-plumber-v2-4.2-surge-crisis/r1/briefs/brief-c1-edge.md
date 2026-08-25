You are a code-review specialist reviewing ONE chunk of a larger code diff (chunk c1 of 7 — the canonical diff was 15,003 lines, split by file group per the review protocol; findings from every chunk are merged before verification). You have read-only access to the repository at the worktree path below and may verify the diff's claims against the actual codebase using read/grep/bash (read-only). NEVER modify any file, in the repo or elsewhere.

--- WORKTREE ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r1

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r1/project-context.md — it is the project's mandatory conventions (core purity, integer-only sim, determinism spine, no-globals, arena discipline, golden harness rules). Follow it when judging the diff.

--- DIFF (chunk c1) ---
diff --git a/_bmad-output/implementation-artifacts/spec-4-2-surge-crisis.md b/_bmad-output/implementation-artifacts/spec-4-2-surge-crisis.md
new file mode 100644
index 0000000..30161c0
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-4-2-surge-crisis.md
@@ -0,0 +1,156 @@
+---
+title: 'Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair)'
+type: 'feature'
+created: '2026-08-14'
+status: 'in-review'
+baseline_commit: 44ceeea
+review_loop_iteration: 0
+context:
+  - '{project-root}/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md'
+  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
+---
+
+<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">
+
+## Intent
+
+**Problem:** The forecast panel (4.1) names the surge but nothing FIRES it: there is no Crisis Engine, no `Crisis_Triggered` event, no structured root cause — the fair-crisis loop (`[FORGE #3]`: "I should have seen this coming") has no consequence half.
+
+**Approach:** Add the Surge archetype + the Crisis Engine (story 4.2, slice 4): `crises.json` archetype table (ODN-4/ODN-5) + `crisis_evaluate` in the spine (downstream of flow, read-only topology view `[ODN-4, REVIEW M1]`). When the surge set-piece activates on schedule, the engine measures the flow's saturation: a healthy within-capacity topology passes clean (no crisis, `[AC-E13]`); an unprepared one gets `Crisis_Triggered{Surge, root_cause}` naming the bottleneck bundle + a `preventive_redesign` — one crisis per root cause per activation, re-trigger only after `Crisis_Resolved` `[E13]`. The Director never reads crisis state (structural: `scripted_plan_pressure` keeps its `(cat, era, tick)` signature).
+
+## Boundaries & Constraints
+
+**Always:**
+- **Core eval** (`core/crisis.odin`, NEW): `crisis_evaluate(state, tick, cat)` called inside `core.step` AFTER `warning_evaluate`, BEFORE `win_lose_eval` (spine: flow → crisis → win/lose). Pure (ODN-1), integer-only (ODN-10), arrays only (ODN-10), no new commands (**LOG_VERSION stays 3**).
+- **The engine READS only:** the era set-piece schedule (catalog), Topology/Bundles/Flow state (queues, pool, drops). It never mutates flow/topology and never touches the director's signature — the `[ODN-7, REVIEW M1]` rule stays structural.
+- **Trigger contract (the pinned definition):** while the surge set-piece is ACTIVE (`[start_tick, start_tick+duration)` — deterministic from the seed), a crisis triggers on the FIRST tick where the surge class's flow is measurably saturated: (a) a surge-class lane queue on some bundle is at the E9 bound (`bundle_lane_count >= lane_queue_packets` with ≥1 surge-class packet on that bundle), OR (b) a surge-class `Queue_Overflow` drop occurred this tick. Root cause = the first saturated bundle in slot order (a → first hit; b → first any-lane-at-bound fallback — a drop implies a bound lane). A healthy topology never queues to bound → no crisis `[AC-E13]`.
+- **Root cause (structured):** `Root_Cause_Kind { Saturated_Bundle, Pool_Exhaustion }`. Saturated_Bundle carries `bundle` + first member `pipe` + the surge `class` + `multiplier`. Pool_Exhaustion = the global pool at cap AND any `Pool_Exhaustion` drop this tick (map-wide flaw; no element ref). `preventive_redesign` = the archetype's catalog string, rendered with the element refs.
+- **Dedup `[E13]`:** `Crisis_State.active` holds at most one crisis per (archetype, set-piece activation). While ACTIVE, the condition is never re-emitted. `Crisis_Resolved` fires on the first tick the condition is absent (the named bundle's queue below bound / no pool drop); after Resolved the same cause may re-trigger (an optional `cooldown_ticks` from `crises.json` gates re-fire; MVP data = 0). Resolved bookkeeping is DERIVED from the event stream (never serialized).
+- **Data (`ODN-5`, single source):** the surge SCHEDULE stays in `demand.json` (the director consumes it — `effective_volume`); `crises.json` (NEW) is the ARCHETYPE table: `id, display_name, root_cause_pattern, failure_effect, preventive_redesign, cooldown_ticks`. The set-piece names its archetype via `archetype_id` (fail-fast cross-ref at load). `crises.json` folds into `catalog_hash` → the documented mechanical re-bless (the 3.2/4.1 precedent).
+- **Events (ODN-14, append-only):** `EVENT_TAG_CRISIS_TRIGGERED :: u8(8)` / `EVENT_TAG_CRISIS_RESOLVED :: u8(9)`; payload `{archetype, cause(kind), class, target(bundle), pipe}` via new Event fields `archetype: u8`, `cause: u8`, `pipe: u32` — tag-conditional serialization, pre-4.2 streams byte-identical.
+- **Serialization:** new `crises` section in `state_writer`, ABSENT-WHEN-EMPTY: active rows `{archetype, set_piece, kind, bundle, pipe, class, multiplier, triggered_tick}` — zero crisis → zero bytes (golden stability). The resolved bookkeeping is NOT serialized (rebuilt from the event stream).
+- **Render (never color alone):** `app/render/crisis.odin` (NEW) — a HUD banner per active crisis (`⚠️ <archetype>: <set-piece> ACTIVE — bottleneck bundle <n> (pipe <id>)` + the preventive_redesign line, catalog display strings) + a red pulsing outline over the named bundle's member pipes (pinned PULSE16, deterministic). **Zero pixels when no crisis is active** (the capture-stability contract). Shared by the app HUD + the harness capture (like forecast.odin).
+- **Golden:** NEW `demos/surge.dem` (unprepared narrow-pipe fan: trigger @window start, a mid-run capacity fix, resolve after the window ends); the event-stream golden pins `Crisis_Triggered{Surge}` at the exact tick within the scheduled window. Re-bless = ALL `.t1`/`.log.bin` (catalog_hash fold, mechanical) + cause-documented T2 shifts (era-3 demos whose post-window captures gain the banner); zero-traffic demos stay pixel-identical — **STOP + flag any other shift**.
+- **App session:** stays era 3 / goal 0 / cap 0 (4.1 sandbox); HUD gains the banner; title → story 4.2.
+
+**Ask First:** none expected — the surge schedule (demand.json `streaming_surge`: x10 @ [1200, 3000), lead 600) is pinned canon; thresholds/lead times are already in balance.json.
+
+**Never:** NOT the other four archetypes (post-fun-gate content), NOT 4.3 (health meter / win-lose / E30), NOT a second schedule copy in crises.json (single-source — the director's demand.json is the timeline), NO new player commands, NO crisis-driven sim mutation (drops/saturation are the flow's own E9/E22 consequences — the engine only names them), no floats in core, no maps in core, no changes to `scripted_plan_pressure`.
+
+## I/O & Edge-Case Matrix
+
+| Scenario | Input / State | Expected Output / Behavior | Error Handling |
+|----------|--------------|---------------------------|----------------|
+| HAPPY_PATH (unprepared) | era 3, surge active @1200, single narrow bundle | `Crisis_Triggered{Surge, Saturated_Bundle{bundle, pipe}}` at the exact first-saturated tick; stays active through the window | n/a |
+| HEALTHY within capacity `[AC-E13]` | surge active, multi-route fan with spare capacity | zero crisis events, zero surge-class drops — the surge passes | n/a |
+| Dedup `[E13]` | condition persists tick after tick | exactly ONE `Crisis_Triggered` per activation | n/a |
+| Resolve + re-trigger | player adds capacity → queue drains → demolishes it again | `Crisis_Resolved` at the drain tick; re-`Crisis_Triggered` after (cooldown 0) | n/a |
+| Pool exhaustion | tiny pool, surge active | `Crisis_Triggered{Surge, Pool_Exhaustion}` (no element refs) | n/a |
+| Pre-window / post-window | tick < start_tick, or window ended | no crisis events (the engine only fires inside the active span) | n/a |
+| Legacy / era 0 | no set-pieces | no-op (no events, no section) | n/a |
+| Terminal (E17) | run frozen | crisis state frozen — `crisis_evaluate` skipped by the step barrier | n/a |
+| Replay (E10) | blessed log re-sim | identical crisis state + identical event stream | replay gate rejects divergence |
+| Catalog validation | unknown `archetype_id`, duplicate archetype ids, empty `preventive_redesign`, cooldown < 0 | load aborts with a named error | fail-fast (ODN-5) |
+
+## Code Map
+
+- `core/types.odin` -- `Root_Cause_Kind`, `Root_Cause` refs on `Active_Crisis`, `Crisis_State.active`, Event fields `archetype`/`cause`/`pipe`, tags 8/9, `crisis_make`/`crisis_destroy` wiring
+- `core/crisis.odin` (NEW) -- `crisis_evaluate`: active-set-piece scan, saturation scan (queue-at-bound, class-filtered + drop-event fallback), trigger/resolve transitions + cooldown bookkeeping
+- `core/step.odin` -- the `crisis_evaluate` call (after `warning_evaluate`, before `win_lose_eval`)
+- `core/serialize.odin` -- the crises section (absent-when-empty) + tag-conditional 8/9 payloads
+- `core/catalog.odin` -- `Crisis_Archetype` row parse + fail-fast; `Set_Piece.archetype_idx` cross-ref; `Catalog_Sources.crises` + hash fold
+- `data/crises.json` (NEW) -- the surge archetype table
+- `data/demand.json` -- `streaming_surge` gains `archetype_id` (the catalog_hash fold)
+- `core/crisis_test.odin` (NEW) -- every I/O-matrix row + the replay pin
+- `core/catalog_test.odin` -- the crises validation rows
+- `app/render/crisis.odin` (NEW) -- the crisis banner + bottleneck outline (zero pixels when empty)
+- `app/main.odin` -- HUD banner call + title
+- `harness/goldens.odin` -- capture adds the banner draw
+- `harness/catalogs.odin` + `app/main.odin` loaders -- read `data/crises.json`
+- `demos/surge.dem` (NEW) -- the launchable golden
+- `goldens/*` -- documented re-bless (ALL `.t1`/`.log.bin`; era-3 shifted T2s; `surge.dem` new)
+
+## Tasks & Acceptance
+
+**Execution:**
+- [x] `core/types.odin` -- the kinds + `Active_Crisis` + `Crisis_State.active` + Event fields/tags + init/destroy
+- [x] `core/crisis.odin` (NEW) -- `crisis_evaluate` (trigger/resolve/dedup/cooldown)
+- [x] `core/step.odin` -- the eval call in spine order
+- [x] `core/serialize.odin` -- the crises section + tag-conditional payloads
+- [x] `core/catalog.odin` + `data/crises.json` + `data/demand.json` -- the archetype table + cross-ref + hash fold
+- [x] `core/crisis_test.odin` (NEW) -- every I/O-matrix row + the replay pin
+- [x] `core/catalog_test.odin` -- validation rows
+- [x] `app/render/crisis.odin` (NEW) + `app/main.odin` + `harness/goldens.odin` -- the banner + outline + capture
+- [x] loaders -- `data/crises.json` in both harness + app `load_catalogs`
+- [x] `demos/surge.dem` (NEW) -- author → run → READ the actual crisis stream → pin ticks in comments + tests
+- [x] Golden pass -- re-bless ALL (catalog_hash fold with proof), cause-document shifted T2s, `drift-check` green
+
+**Acceptance Criteria:**
+- Given the era-3 surge schedule, when the window opens on an unprepared topology, then `Crisis_Triggered{Surge, root_cause}` fires at the exact first-saturated tick (inside `[1200, 3000)`), carrying the structured flaw ref + `preventive_redesign`; the same seed reproduces it (E10).
+- Given a healthy within-capacity topology, when the surge activates, then no crisis fires and the surge class drops nothing `[AC-E13]`.
+- Given a persistent flaw, when saturation continues tick after tick, then exactly one `Crisis_Triggered` per activation `[E13]`; after the player's fix drains the queue, `Crisis_Resolved` fires, and a re-break re-triggers (cooldown 0).
+- Given any run, when it replays from the action log, then identical crisis state + event stream (E10); post-terminal ticks stay frozen (E17).
+- Given the golden pass, when the harness runs, then every shifted golden has a documented cause (catalog_hash fold; era-3 demos' post-window banner); zero-traffic demos' T2s are pixel-identical; any other shift STOPS the line.
+
+## Spec Change Log
+
+- 2026-08-14 (implementation findings, pre-review): three mechanism refinements, all within the frozen
+  contract's spirit, recorded here for the review trail:
+  1. **The drop event now carries the shed bundle** (`Event.target` for `Packet_Dropped`; E9 = the bundle
+     whose lane was at bound, E22 = `NO_BUNDLE`). Finding: the settled queue alone oscillates ±1-2 around
+     the E9 bound on the service/completion phase, so an eval-time scan could not reliably attribute the
+     drop's location (and could miss saturation entirely when service ≥ 1 packet/tick — the queue settles
+     below the bound while shedding every tick). The drop's bundle IS the admission-time evidence — the
+     trigger now names it exactly. Cost: the serialized drop payload grows by 4 bytes (all T1 manifests
+     re-blessed — a documented cause alongside the catalog_hash fold).
+  2. **Resolve hysteresis** (`CRISIS_RESOLVE_MARGIN = 2`): a crisis resolves only when the named bundle's
+     class backlog falls strictly below (bound − margin) AND no lane of the bundle is at the E9 bound
+     (a lane held at bound by ANOTHER class still means "no spare capacity" — review: without this, a
+     resolved surge crisis could re-trigger the same tick via the settled scan and chatter, [E13]) AND
+     the ladder stopped shedding on it. The pool-exhaustion cause gets the same margin (the pool must
+     sit meaningfully below its cap). Finding: without the margins, a marginal network chattered
+     trigger/resolve every few ticks — the golden discipline pins ONE trigger per persistent flaw [E13].
+  3. **Fixtures respect the 4-port router limit**: the healthy-topology pin ([AC-E13]) uses the mult2 test
+     catalog (surge = 2/tick — the contract is magnitude-independent: the engine keys on measurable
+     saturation, never the schedule's numbers) on a 2-wide path; the resolve/cooldown tests swap the
+     narrows for wides (demolish-first, port swap) instead of adding pipes to a full router.
+- 2026-08-14 (review round 1 — 2-hunter swarm): patch-class findings only (no intent gaps, no bad specs):
+  1. **`jint_strict` hardened** (shared helper): out-of-i32-range integers and wrong-typed values
+     (string/bool/null) now reject instead of wrapping through the i32 cast / defaulting to `def` — the
+     crises `cooldown_ticks` (and every pre-existing caller) can no longer silently accept a huge value
+     as a small number or a string as 0.
+  2. **crises parse fail-fast**: a non-object archetype row rejects (was `or_continue`), and the roster
+     caps at 255 rows (the Event payload's u8 archetype byte — a larger table would truncate the
+     serialized event stream).
+  3. **Pool banner branch**: a `.Pool_Exhaustion` crisis renders "network at capacity (pool exhausted)"
+     — the unconditional bundle ref would have printed `4294967295` (NO_BUNDLE) on the flagship "WHY"
+     surface. The ⚠ glyph became ASCII "!!" (the draw helper truncates runes to bytes; a non-ASCII
+     symbol rendered as garbage) and the title was shortened to fit the card — the frozen text's "⚠️"
+     template is a documented cosmetic deviation.
+  4. **Step tick-monotonicity latch**: a backward tick sets `replay_error` (never silent) — the crisis
+     scans depend on the tick-ordered event buffer (the app never drains it).
+  5. **Coverage**: era-0 no-op test; crises validation rows (empty failure_effect, non-object row,
+     wrong-typed / i32-wrapping cooldown, 256-row cap); leak hygiene in crisis_record_run callers.
+  KEEP: the drop-first root-cause attribution, the resolve margins, the absent-when-empty serialization,
+  the exact-tick golden pins, and the slot-order determinism — all survived the adversarial pass intact.
+
+## Design Notes
+
+- **Why saturation-based triggering (and not "fire on schedule, period"):** `[AC-E13]` FORCES the check — a prepared player's surge must NOT fire a crisis. The queue-at-bound condition is the flow's own E9 state (deterministic, already hashed); the forecast (4.1) is the lead-time telegraph. The E9 bound (6 packets/lane) means a single lane admits ≤6/tick regardless of pipe capacity — the surge's 20/tick REQUIRES multi-route redundancy (ECMP, 2.2) or lane-splitting; that IS the GDD "no bundled redundancy" root cause.
+- **Why `archetype_id` on the demand set-piece:** the schedule must stay in demand.json (the director multiplies spawns from it — single source, ODN-5). `crises.json` holds the archetype only; the cross-ref joins them. The epic-context's sketch field list (warning_curve, lead_time_ticks) is deliberately NOT carried — the set-piece's `forecast_lead_ticks` + balance.json `warnings` leads ARE the reaction window (a second number would drift). The `preventive_redesign` string is display content (rendered by the app) — sim-determinism rides the refs, not the string.
+- **The demo's narrative (author → run → pin):** `surge.dem` = narrow-pipe host→router→res (unprepared; saturated at base demand). `Crisis_Triggered` lands at the window's first tick (20 arrivals → 6 join the bound lane → saturated); a parallel wide drawn mid-run pools into the same bundle (the fix); the queue drains after the window ends (base demand 2/tick ≤ 2.67 service) → `Crisis_Resolved` at the exact drain tick — read from the run, pinned in the demo comment + tests.
+- **warn.dem's post-60s frames shift cause-documented:** its fixture saturates under the surge, so its
+  `NOW` capture gains the banner + bottleneck outline (the 4.1 spec already documented its surge-strain
+  content); qos.dem's 65s capture gains the same banner + outline (era 3, inside the surge window, its
+  fixture saturated at the capture — the 4.1 spec's "qos.dem 65s capture" shift line covers the strain;
+  the banner is the 4.2 addition, cause-documented here). qos_emphasis's captures (1s/5s/12s, pre-surge)
+  stay pixel-identical — the negative proof.
+
+## Verification
+
+**Commands:**
+- `odin test core` -- all suites green incl. the new crisis_test pins
+- `tools/lint.sh` -- all 5 gates green
+- `tools/harness.sh run` -- green after the documented re-bless; the negative proof = zero-traffic demos' T2 pixels byte-identical
+- `tools/harness.sh save <all>` -- the catalog_hash fold re-bless + cause-documented T2 shifts; `tools/harness.sh save surge` -- the new golden; `tools/harness.sh drift-check` -- every mutation rejected
+- `odin build app` + run -- era-3 session: the panel counts the surge down; the surge hits on cue; an unprepared network shows the crisis banner with the WHY (bundle + preventive redesign)
diff --git a/app/main.odin b/app/main.odin
index 6e29fa7..c60e78c 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -117,6 +117,13 @@ main :: proc() {
 			for app.accum >= tick_seconds && steps < max_steps {
 				if app.state.terminal { break } // a dead run steps no further
 				app.tick += 1
+				// NOTE (4.2 tripwire): the app NEVER drains state.events (the
+				// harness drains per tick). The crisis engine's drop scans rely
+				// on the buffer being tick-ordered (tail-first with an
+				// e.tick < tick break — see crisis.odin) and step now latches
+				// non-monotonic ticks. Any FUTURE consumer that scans the
+				// buffer forward without a tick filter will see a whole
+				// session's worth of stale events — drain here or filter.
 				pp.step(&app.state, app.tick, {}, &cat) // edits land via the fast-path
 				app.accum -= tick_seconds
 				steps += 1
@@ -509,7 +516,7 @@ node_pos :: proc(app: ^App, id: u32) -> [2]i32 {
 draw_hud :: proc(app: ^App) {
 	p := app.palette
 	// title
-	draw_text(app, "Packet Plumber — v2 story 4.1 (warning signs + forecast)", 12, 10, 22, p.ink)
+	draw_text(app, "Packet Plumber — v2 story 4.2 (surge + crisis engine)", 12, 10, 22, p.ink)
 
 	// the game-over screen: the WIN/LOSE toast (the terminal-event barrier
 	// guarantees exactly one outcome). The world still draws behind it; retry hint.
@@ -547,6 +554,10 @@ draw_hud :: proc(app: ^App) {
 	// 20 s at logic_hz; the player must see the leads, or they are dead
 	// config). Seconds = lead_ticks / logic_hz (integer).
 	rnd.draw_forecast_panel(&app.view, &app.state.crisis, &app.cat, app.state.era)
+	// 4.2: the crisis banner (top-center) — names the ACTIVE surge + the WHY
+	// (bottleneck bundle + pipe) + the preventive redesign. Zero pixels when
+	// no crisis is active.
+	rnd.draw_crisis_banner(&app.view, &app.state.crisis, &app.cat, app.state.era)
 	wb := &app.cat.balance.warnings
 	hz := i64(max(1, app.cat.balance.logic_hz))
 	lead_s := fmt.tprintf("node strain ~%ds to critical · node critical ~%ds · pipe ~%ds to saturation — ring + glyph, never color alone",
@@ -797,11 +808,16 @@ load_catalogs :: proc(cat: ^pp.Catalogs) -> string {
 	if e5 != nil {
 		return fmt.tprintf("cannot read data/demand.json: %v", e5)
 	}
+	cris, e6 := os.read_entire_file_from_path("data/crises.json", context.temp_allocator)
+	if e6 != nil {
+		return fmt.tprintf("cannot read data/crises.json: %v", e6)
+	}
 	src.node_types = nt
 	src.pipe_tiers = pt
 	src.balance = bal
 	src.packet_types = pkt // 3.1
 	src.demand = dem       // 3.1
+	src.crises = cris      // 4.2
 	cerr := pp.catalogs_load(cat, &src)
 	if cerr.file != "" {
 		return pp.catalog_error_string(cerr)
diff --git a/app/render/crisis.odin b/app/render/crisis.odin
new file mode 100644
index 0000000..e5e6e72
--- /dev/null
+++ b/app/render/crisis.odin
@@ -0,0 +1,118 @@
+package render
+
+// crisis.odin — the 4.2 crisis surface (the S4 launchable increment: "the
+// surge hits on cue; you can see WHY — the root cause"): a HUD banner naming
+// the active crisis — archetype display + set-piece id + the bottleneck
+// (bundle + member pipe, or "pool exhausted" for the map-wide cause) + the
+// archetype's preventive redesign — and a pulsing red outline over the named
+// bundle's member pipes. Never color alone: outline shape + banner caption +
+// the "!!" glyph carry the state (the colorblind-safe canon; the glyph is
+// ASCII — the draw helper truncates every rune to a byte, so a non-ASCII
+// symbol would render as garbage). Reads the serialized active rows only
+// (read-only — the draw never steps the sim, ODN-1). Draws ZERO pixels when
+// no crisis is active (the capture-stability contract: a resolved crisis
+// returns the frame to byte-identical).
+
+import "core:fmt"
+import pp "../../core"
+import rl "vendor:raylib"
+
+// draw_crisis_banner — the top-center crisis card (clear of the top-left run
+// HUD + the top-right forecast panel). One title line + one redesign line per
+// active crisis; catalog display strings throughout (a future archetype
+// labels itself — never a hardcoded "SURGE"). Draws NOTHING when the registry
+// is empty (the capture-stability contract).
+draw_crisis_banner :: proc(v: ^View, crisis: ^pp.Crisis_State, cat: ^pp.Catalogs, era: u8) {
+	if len(crisis.active) == 0 {
+		return
+	}
+	p := v.palette
+	card_w := i32(440)
+	pad := i32(10)
+	title_h := i32(20)
+	line_h := i32(17)
+	x := (v.win_w - card_w) / 2
+	y := i32(10)
+	rows := 2 * len(crisis.active)
+	h := title_h + i32(rows) * line_h + pad
+	card := rl.Color{255, 244, 236, 240}
+	rl.DrawRectangle(x - pad, y - pad, card_w + 2 * pad, h, card)
+	rl.DrawRectangleLines(x - pad, y - pad, card_w + 2 * pad, h, p.state_critical)
+		ty := y
+	for ac in crisis.active {
+		arch := "crisis"
+		if int(ac.archetype) < len(cat.crises) {
+			arch = cat.crises[ac.archetype].display_name
+		}
+		sp_name := "setpiece"
+		if era > 0 && int(era) <= len(cat.demand.eras) {
+			de := &cat.demand.eras[era-1]
+			if int(ac.set_piece) < len(de.set_pieces) {
+				sp_name = de.set_pieces[ac.set_piece].id
+			}
+		}
+		// the WHY line branches on the root-cause kind: the Saturated_Bundle
+		// cause names its element; the Pool_Exhaustion cause is map-wide (no
+		// element ref — rendering NO_BUNDLE as a number would be nonsense).
+		// The glyph is ASCII "!!" (the draw helper truncates every rune to a
+		// byte, so a non-ASCII ⚠ would render as garbage in the raylib font).
+		title := ""
+		if ac.kind == .Saturated_Bundle {
+			title = fmt.aprintf("!!  %s: %s ACTIVE — bundle %d (pipe %d)",
+				arch, sp_name, ac.bundle, ac.pipe, allocator = context.temp_allocator)
+		} else {
+			title = fmt.aprintf("!!  %s: %s ACTIVE — network at capacity (pool exhausted)",
+				arch, sp_name, allocator = context.temp_allocator)
+		}
+		draw_text_c(v, title, x, ty, 15, p.state_critical)
+		ty += line_h
+		redesign := "Add capacity before the countdown ends."
+		if int(ac.archetype) < len(cat.crises) {
+			redesign = cat.crises[ac.archetype].preventive_redesign
+		}
+		draw_text_c(v, redesign, x, ty, 12, p.ink)
+		ty += line_h
+	}
+}
+
+// draw_crisis_outlines — the bottleneck highlight: every member pipe of an
+// active crisis's named bundle draws a state-colored OUTER stroke (shape +
+// outline — never color alone), radius modulated by the pinned PULSE16 table
+// (the same no-transcendentals pulse the health rings use; phase from
+// tick + bundle so sibling crises do not pulse in lockstep). Called from
+// draw_world AFTER the pipe pass (the outline sits on top of the pipes).
+draw_crisis_outlines :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, crisis: ^pp.Crisis_State, tick: u64) {
+	if len(crisis.active) == 0 {
+		return
+	}
+	p := v.palette
+	col := p.state_critical
+	col.a = 190
+	for i in 0..<len(topo.pipe_alive) {
+		if !topo.pipe_alive[i] { continue }
+		if int(i) >= len(bundles.pipe_bundle) { continue }
+		b := bundles.pipe_bundle[i]
+		named := false
+		for ac in crisis.active {
+			if ac.kind == .Saturated_Bundle && ac.bundle == b {
+				named = true
+				break
+			}
+		}
+		if !named { continue }
+		a_slot, oka := pp.node_slot(topo, topo.pipe_a[i])
+		b_slot, okb := pp.node_slot(topo, topo.pipe_b[i])
+		if !oka || !okb { continue }
+		a := node_screen(v, topo.node_pos[a_slot])
+		bb := node_screen(v, topo.node_pos[b_slot])
+		// the pinned pulse (deterministic — captures at exact ticks are
+		// golden-stable): width swells by the pulse factor.
+		table := PULSE16
+		phase := (tick + u64(b)) % 16
+		factor := table[phase]
+		width := 7.0 * v.scale + 6.0 * v.scale * factor
+		rl.DrawLineEx(a, bb, width, col)
+		rl.DrawCircleV(a, width * 0.5, col)
+		rl.DrawCircleV(bb, width * 0.5, col)
+	}
+}
diff --git a/app/render/view.odin b/app/render/view.odin
index 04c85ac..a42389c 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -86,6 +86,9 @@ draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp
 	draw_bundles(v, topo, bundles, flow, crisis)
 	draw_nodes(v, topo, crisis, tick)
 	draw_packets(v, topo, bundles, flow)
+	// 4.2: the crisis bottleneck outline — the named bundle's member pipes
+	// (pulsing red stroke, on top of the pipes so the highlight reads).
+	draw_crisis_outlines(v, topo, bundles, crisis, tick)
 	if drag.active && drag.placing < 0 {
 		draw_ghost(v, topo, drag)
 	}
diff --git a/core/catalog.odin b/core/catalog.odin
index 3daa2d2..1eb6865 100644
--- a/core/catalog.odin
+++ b/core/catalog.odin
@@ -135,6 +135,10 @@ Demand_Entry :: struct {
 // The Streaming Surge (streaming x10) is the MVP one. class is resolved at load.
 // 3.1 carries the DATA + the effective_volume multiplier; the crisis engine +
 // forecast UI that consume the same set-pieces land in slice 4.
+// 4.2: `archetype_idx` joins the set-piece to its crisis archetype (crises.json
+// cross-ref, fail-fast — -1 = pure demand event, no crisis on activation). The
+// SCHEDULE stays here (the director multiplies spawns from it, single source);
+// the archetype table holds the root-cause/failure/redesign content.
 Set_Piece :: struct {
 	id:                 string,
 	class:              u16,        // packet_types index (resolved at load)
@@ -142,6 +146,7 @@ Set_Piece :: struct {
 	start_tick:         u64,
 	duration_ticks:     u64,
 	forecast_lead_ticks: u64,
+	archetype_idx:      i32,        // 4.2: crises.json index; -1 = none (load-time resolved)
 }
 
 // Demand_Era — one era's base demand (always-active entries + set-pieces).
@@ -209,11 +214,29 @@ Lane_Preset :: struct {
 	weights: [3]i32,
 }
 
+// Crisis_Archetype — one crisis archetype row (4.2, crises.json — ODN-4/ODN-5):
+// the root-cause pattern the engine evaluates + the failure effect + the
+// preventive redesign (the fairness contract's "what the player could have
+// built"). `id` is the cross-ref key (set_piece.archetype_id); display_name /
+// root_cause_pattern / failure_effect / preventive_redesign are display
+// content (the app renders them — determinism rides the structured refs, never
+// the strings); cooldown_ticks is the re-fire gate after a Crisis_Resolved
+// (arch §6.4; 0 = re-fire allowed immediately). Sim values are integers (ODN-10).
+Crisis_Archetype :: struct {
+	id:                  string,
+	display_name:        string,
+	root_cause_pattern:  string,
+	failure_effect:      string,
+	preventive_redesign: string,
+	cooldown_ticks:      u64,
+}
+
 Catalogs :: struct {
 	node_types:   [dynamic]Node_Type,
 	pipe_tiers:   [dynamic]Pipe_Tier,
 	packet_types: [dynamic]Packet_Type, // 3.1: the packet class roster (email + streaming)
 	demand:       Demand_Catalog,       // 3.1: per-era DemandSpecs + SetPieces (the demand director's data)
+	crises:       [dynamic]Crisis_Archetype, // 4.2: the archetype table (crises.json) — the crisis engine's data
 	balance:      Balance,
 	hash:         u64, // FNV-1a-64 over the sim-relevant source bytes (fixed order)
 }
@@ -225,6 +248,7 @@ Catalog_Sources :: struct {
 	pipe_tiers:   []byte,
 	packet_types: []byte, // 3.1
 	demand:       []byte, // 3.1
+	crises:       []byte, // 4.2
 	balance:      []byte,
 }
 
@@ -387,6 +411,56 @@ catalogs_load :: proc(cat: ^Catalogs, src: ^Catalog_Sources, allocator := contex
 		if len(cat.packet_types) == 0 { return {"packet_types.json", "entries", "empty"} }
 	}
 
+	// crises (4.2) — the archetype table (crises.json). Parsed BEFORE demand:
+	// the set-piece rows cross-ref it (archetype_id -> index). Fail-fast on
+	// every row (ODN-5): a non-object entry rejects (a stray row must never
+	// silently reshape the table), id/display/pattern/effect/redesign
+	// non-empty, unique ids, cooldown >= 0 (range-checked before the u64
+	// cast — a negative or out-of-i32 value must reject, never wrap), and
+	// the roster caps at 255 (the Event payload's archetype byte — a larger
+	// table would truncate the serialized event stream).
+	{
+		v, e := json.parse(src.crises, parse_integers = true)
+		if e != nil { return {"crises.json", "$", "invalid JSON"} }
+		obj, ok := v.(json.Object)
+		if !ok { return {"crises.json", "$", "root must be an object"} }
+		entries, oke := obj["archetypes"].(json.Array)
+		if !oke { return {"crises.json", "archetypes", "missing array"} }
+		if len(entries) > 255 {
+			return {"crises.json", "archetypes", "at most 255 archetypes (the event payload's u8 archetype byte)"}
+		}
+		cat.crises = make([dynamic]Crisis_Archetype, 0, 4, allocator)
+		for ev in entries {
+			eo, eok := ev.(json.Object)
+			if !eok {
+				return {"crises.json", "<row>", "archetype entry must be an object"}
+			}
+			a: Crisis_Archetype
+			a.id = jstr(eo, "id")
+			a.display_name = jstr(eo, "display_name")
+			a.root_cause_pattern = jstr(eo, "root_cause_pattern")
+			a.failure_effect = jstr(eo, "failure_effect")
+			a.preventive_redesign = jstr(eo, "preventive_redesign")
+			cd, okc := jint_strict(eo, "cooldown_ticks", 0)
+			if !okc { return {"crises.json", a.id, "cooldown_ticks must be an integer (no decimals)"} }
+			if a.id == "" || a.display_name == "" || a.root_cause_pattern == "" ||
+				a.failure_effect == "" || a.preventive_redesign == "" {
+				return {"crises.json", a.id, "id/display_name/root_cause_pattern/failure_effect/preventive_redesign must be non-empty"}
+			}
+			if cd < 0 { return {"crises.json", a.id, "cooldown_ticks must be >= 0"} }
+			a.cooldown_ticks = u64(cd)
+			append(&cat.crises, a)
+		}
+		if len(cat.crises) == 0 { return {"crises.json", "archetypes", "empty"} }
+		for i in 0..<len(cat.crises) {
+			for j in i+1..<len(cat.crises) {
+				if cat.crises[i].id == cat.crises[j].id {
+					return {"crises.json", cat.crises[i].id, "duplicate archetype id"}
+				}
+			}
+		}
+	}
+
 	// demand (3.1) — per-era DemandSpecs + SetPieces. eras is an ARRAY
 	// (insertion-ordered, map-free — ODN-10). Each row carries its `era`; the
 	// catalog stores it indexed by era-1 (padded). class refs in entries +
@@ -470,6 +544,23 @@ catalogs_load :: proc(cat: ^Catalogs, src: ^Catalog_Sources, allocator := contex
 					sp.start_tick = u64(st)
 					sp.duration_ticks = u64(dt)
 					sp.forecast_lead_ticks = u64(fl)
+					// 4.2: the optional archetype_id cross-ref (crises.json). An
+					// unknown ref is a content bug (fail-fast — a set-piece that
+					// names no archetype is a pure demand event, -1).
+					sp.archetype_idx = -1
+					if aid := jstr(seo, "archetype_id"); aid != "" {
+						found := false
+						for ai in 0..<len(cat.crises) {
+							if cat.crises[ai].id == aid {
+								sp.archetype_idx = i32(ai)
+								found = true
+								break
+							}
+						}
+						if !found {
+							return {"demand.json", sp.id, fmt.tprintf("unknown archetype_id %q (crises.json)", aid)}
+						}
+					}
 					append(&de.set_pieces, sp)
 				}
 			}
@@ -656,6 +747,7 @@ catalogs_destroy :: proc(cat: ^Catalogs) {
 	delete(cat.node_types)
 	delete(cat.pipe_tiers)
 	delete(cat.packet_types)
+	delete(cat.crises) // 4.2
 	for i in 0..<len(cat.demand.eras) {
 		delete(cat.demand.eras[i].entries)
 		delete(cat.demand.eras[i].set_pieces)
@@ -677,6 +769,7 @@ catalogs_hash_sources :: proc(src: ^Catalog_Sources) -> u64 {
 	fold(&h, src.pipe_tiers)
 	fold(&h, src.packet_types) // 3.1: sim-relevant (drives spawns) — folds into the replay-binding hash
 	fold(&h, src.demand)       // 3.1: sim-relevant (the demand director's data)
+	fold(&h, src.crises)       // 4.2: sim-relevant (the crisis engine's archetype table)
 	fold(&h, src.balance)
 	return h
 }
@@ -743,12 +836,23 @@ jint :: proc(o: json.Object, key: string, def: i32) -> i32 {
 // jint_strict — like jint but a json.Float (a decimal in the file) is a
 // fail-fast rejection (ok=false), never a silent truncation — the 3.1
 // integer-only bar for the NEW catalogs (ODN-5; the old loaders keep jint).
-// Missing -> (def, true).
+// Missing -> (def, true). 4.2 hardening (review): an out-of-i32-range integer
+// (|v| > i32::MAX) and ANY other JSON type (string/bool/null) also reject —
+// a huge value must never wrap through the i32 cast (e.g. a cooldown of
+// 2^32+4 silently becoming 4) and a wrong-typed field must never default.
 jint_strict :: proc(o: json.Object, key: string, def: i32) -> (i32, bool) {
 	if v, ok := o[key]; ok {
 		#partial switch x in v {
-		case json.Integer: return i32(x), true
-		case json.Float:   return 0, false
+		case json.Integer:
+			i := i64(x)
+			if i < i64(min(i32)) || i > i64(max(i32)) {
+				return 0, false // out of range — reject, never wrap
+			}
+			return i32(i), true
+		case json.Float:
+			return 0, false
+		case:
+			return 0, false // wrong-typed (string/bool/null) — reject, never default
 		}
 	}
 	return def, true
diff --git a/core/catalog_test.odin b/core/catalog_test.odin
index 23738b1..88f0e08 100644
--- a/core/catalog_test.odin
+++ b/core/catalog_test.odin
@@ -65,11 +65,39 @@ DEM_ERA :: string(`{"era": 1, "entries": [` + DEM_SPEC + `], "set_pieces": []}`)
 DEM_VALID :: string(`{"eras": [` + DEM_ERA + `]}`)
 
 // SP_DEM_VALID — era 1 with a streaming surge set-piece (streaming exists in
-// PKT_VALID). Used by the set-piece negative rows.
+// PKT_VALID). Used by the set-piece negative rows. 4.2: the surge set-piece
+// names its crisis archetype (crises.json cross-ref).
 SP_ERA :: string(`{"era": 1, "entries": [` + DEM_SPEC + `], "set_pieces": [
-  {"id": "surge", "class_id": "streaming", "multiplier": 10, "start_tick": 1200, "duration_ticks": 1800, "forecast_lead_ticks": 600}]}`)
+  {"id": "surge", "class_id": "streaming", "multiplier": 10, "start_tick": 1200, "duration_ticks": 1800, "forecast_lead_ticks": 600, "archetype_id": "surge"}]}`)
 SP_DEM_VALID :: string(`{"eras": [` + SP_ERA + `]}`)
 
+// CRISES_VALID — the 4.2 archetype table baseline (mirrors data/crises.json).
+CRISES_VALID :: `{"archetypes": [
+  {"id": "surge", "display_name": "Surge", "root_cause_pattern": "saturation", "failure_effect": "cascade_saturation", "preventive_redesign": "Build spare capacity.", "cooldown_ticks": 0}]}`
+
+// CRISES_ROW_VALID — one valid archetype row (the non-object-row test's
+// companion).
+CRISES_ROW_VALID :: `{"id": "surge", "display_name": "Surge", "root_cause_pattern": "saturation", "failure_effect": "cascade_saturation", "preventive_redesign": "Build spare capacity.", "cooldown_ticks": 0}`
+
+// crises_256_doc — a 256-archetype document (the roster-cap fail-fast test:
+// the Event payload's archetype byte holds at most 255).
+crises_256_doc :: proc(allocator := context.allocator) -> string {
+	b := strings.builder_make(allocator)
+	strings.write_string(&b, `{"archetypes": [`)
+	for i in 0..<256 {
+		if i > 0 {
+			strings.write_string(&b, ",")
+		}
+		// Odin fmt treats format strings specially — JSON braces never ride a
+		// printf format; the id number is the only interpolated part.
+		strings.write_string(&b, `{"id": "arch_`)
+		strings.write_string(&b, fmt.aprintf("%d", i, allocator = allocator))
+		strings.write_string(&b, `", "display_name": "A", "root_cause_pattern": "p", "failure_effect": "f", "preventive_redesign": "r", "cooldown_ticks": 0}`)
+	}
+	strings.write_string(&b, `]}`)
+	return strings.to_string(b)
+}
+
 // check_reject — feed (pkt, dem) into catalogs_load and assert the NAMED
 // rejection: file must match + rule must be a substring of the reason.
 check_reject :: proc(t: ^testing.T, pkt, dem, want_file, want_rule: string) {
@@ -82,6 +110,7 @@ check_reject :: proc(t: ^testing.T, pkt, dem, want_file, want_rule: string) {
 		balance      = transmute([]u8)string(BAL_VALID),
 		packet_types = transmute([]u8)pkt,
 		demand       = transmute([]u8)dem,
+		crises       = transmute([]u8)string(CRISES_VALID), // 4.2
 	}
 	cerr := catalogs_load(cat, &src)
 	testing.expectf(t, cerr.file != "", "expected a rejection (rule %q) — catalog loaded clean", want_rule)
@@ -105,6 +134,7 @@ check_ok :: proc(t: ^testing.T) {
 		balance      = transmute([]u8)string(BAL_VALID),
 		packet_types = transmute([]u8)string(PKT_VALID),
 		demand       = transmute([]u8)string(DEM_VALID),
+		crises       = transmute([]u8)string(CRISES_VALID), // 4.2
 	}
 	cerr := catalogs_load(cat, &src)
 	testing.expectf(t, cerr.file == "", "valid docs must load clean, got %q %q", cerr.file, cerr.rule)
@@ -114,6 +144,32 @@ check_ok :: proc(t: ^testing.T) {
 	testing.expect(t, ok, "streaming class must resolve")
 	testing.expectf(t, len(cat.demand.eras) == 1 && len(cat.demand.eras[0].entries) == 1,
 		"era 1 demand must parse, got %d eras", len(cat.demand.eras))
+	testing.expectf(t, len(cat.crises) == 1 && cat.crises[0].id == "surge",
+		"the surge archetype must parse, got %d rows", len(cat.crises))
+}
+
+// check_reject_crises — feed a BAD crises.json doc (the other four valid) and
+// assert the named rejection. 4.2.
+check_reject_crises :: proc(t: ^testing.T, crises_doc, want_rule: string) {
+	cat_storage: Catalogs
+	cat := &cat_storage
+	defer catalogs_destroy(cat)
+	src := Catalog_Sources{
+		node_types   = transmute([]u8)string(NT_VALID),
+		pipe_tiers   = transmute([]u8)string(TIER_VALID),
+		balance      = transmute([]u8)string(BAL_VALID),
+		packet_types = transmute([]u8)string(PKT_VALID),
+		demand       = transmute([]u8)string(DEM_VALID),
+		crises       = transmute([]u8)crises_doc,
+	}
+	cerr := catalogs_load(cat, &src)
+	testing.expectf(t, cerr.file != "", "expected a rejection (rule %q) — catalog loaded clean", want_rule)
+	if cerr.file == "" {
+		return
+	}
+	testing.expectf(t, cerr.file == "crises.json", "rejection file: got %q want crises.json", cerr.file)
+	testing.expectf(t, strings.contains(cerr.rule, want_rule),
+		"rejection rule: got %q want substring %q", cerr.rule, want_rule)
 }
 
 @(test)
@@ -198,6 +254,42 @@ test_catalogs_load_failfast :: proc(t: ^testing.T) {
 		check_reject(t, PKT_VALID, r.doc, "demand.json", r.rule)
 	}
 
+	// --- 4.2 crises.json negative rows --------------------------------------
+	crises_rows := []struct {
+		label, doc, rule: string
+	}{
+		{"bad json", `{`, "invalid JSON"},
+		{"root not object", `[1]`, "root must be an object"},
+		{"missing archetypes", `{}`, "missing array"},
+		{"empty archetypes", `{"archetypes": []}`, "empty"},
+		{"empty id", replace1(CRISES_VALID, `"id": "surge"`, `"id": ""`, 1), "must be non-empty"},
+		{"empty display", replace1(CRISES_VALID, `"display_name": "Surge"`, `"display_name": ""`, 1), "must be non-empty"},
+		{"empty pattern", replace1(CRISES_VALID, `"root_cause_pattern": "saturation"`, `"root_cause_pattern": ""`, 1), "must be non-empty"},
+		{"empty effect", replace1(CRISES_VALID, `"failure_effect": "cascade_saturation"`, `"failure_effect": ""`, 1), "must be non-empty"},
+		{"empty redesign", replace1(CRISES_VALID, `"preventive_redesign": "Build spare capacity."`, `"preventive_redesign": ""`, 1), "must be non-empty"},
+		{"cooldown decimal", replace1(CRISES_VALID, `"cooldown_ticks": 0`, `"cooldown_ticks": 1.5`, 1), "cooldown_ticks must be an integer"},
+		{"cooldown negative", replace1(CRISES_VALID, `"cooldown_ticks": 0`, `"cooldown_ticks": -1`, 1), "cooldown_ticks must be >= 0"},
+		// 4.2 review hardening: a wrong-typed or out-of-i32-range value must
+		// reject (the old jint_strict silently defaulted strings to 0 and
+		// wrapped huge integers through the i32 cast).
+		{"cooldown string", replace1(CRISES_VALID, `"cooldown_ticks": 0`, `"cooldown_ticks": "abc"`, 1), "cooldown_ticks must be an integer"},
+		{"cooldown wraps i32", replace1(CRISES_VALID, `"cooldown_ticks": 0`, `"cooldown_ticks": 4294967300`, 1), "cooldown_ticks must be an integer"},
+		{"non-object row", `{"archetypes": [` + CRISES_ROW_VALID + `, 42]}`, "archetype entry must be an object"},
+		{"too many archetypes", crises_256_doc(), "at most 255 archetypes"},
+		{"duplicate id", `{"archetypes": [
+  {"id": "surge", "display_name": "A", "root_cause_pattern": "p", "failure_effect": "f", "preventive_redesign": "r", "cooldown_ticks": 0},
+  {"id": "surge", "display_name": "B", "root_cause_pattern": "p", "failure_effect": "f", "preventive_redesign": "r", "cooldown_ticks": 0}]}`, "duplicate archetype id"},
+	}
+	for r in crises_rows {
+		check_reject_crises(t, r.doc, r.rule)
+	}
+
+	// --- 4.2 the archetype_id cross-ref (demand → crises) -------------------
+	// an unknown archetype_id is a content bug — fail-fast (a set-piece that
+	// would silently never fire a crisis)
+	check_reject(t, PKT_VALID, replace1(SP_DEM_VALID, `"archetype_id": "surge"`, `"archetype_id": "flood"`, 1),
+		"demand.json", "unknown archetype_id")
+
 	// --- balance.json lane_presets negative rows (3.2) ---------------------
 	bal_rows := []struct {
 		label, doc, rule: string
diff --git a/core/crisis.odin b/core/crisis.odin
new file mode 100644
index 0000000..c57dfc2
--- /dev/null
+++ b/core/crisis.odin
@@ -0,0 +1,376 @@
+package core
+
+// crisis.odin — Story 4.2: the Crisis Engine (arch §6.4 S4, ODN-4). The
+// consequence half of the [FORGE #3] fairness contract: when the surge
+// set-piece activates on schedule (deterministic — the demand director's
+// schedule), the engine measures the flow's ACTUAL saturation and fires
+// Crisis_Triggered{archetype, root_cause} only when the topology cannot carry
+// it — no crisis on a healthy within-capacity topology [AC-E13]. Every crisis
+// carries a structured root_cause (the bottleneck bundle + member pipe, or the
+// exhausted pool) + the archetype's preventive_redesign (display, rendered by
+// the app).
+//
+// Boundaries (structural): the engine is DOWNSTREAM of flow — it reads
+// Topology/Bundles/Flow/catalog only, mutates nothing (the saturation + drops
+// are the flow's own E9/E22 consequences; the engine NAMES them). It never
+// owns the demand timeline — the Director (ODN-7) is upstream with its
+// read-only (cat, era, tick) signature, so "[REVIEW M1]: the Director must
+// never read crisis state" holds by construction.
+//
+// The trigger (the pinned contract): while the surge set-piece is ACTIVE
+// ([start_tick, start_tick+duration)), a crisis fires on the FIRST tick where
+// the surge class's flow is measurably saturated — (a) the surge class has
+// packets queued on a bundle whose lane queue is at the E9 bound
+// (bundle_lane_count >= lane_queue_packets — the state the drop ladder sheds
+// from), or (b) a surge-class Queue_Overflow drop occurred this tick (the
+// ladder just shed). Root cause = the first saturated bundle in slot order
+// (pass 1) / the first any-lane-at-bound bundle (pass 2 — the drop-fallback: a
+// drop implies a bound lane). A healthy within-capacity topology never queues
+// to bound → the surge passes silently [AC-E13]. The E9 bound (6 packets/lane)
+// means a single lane admits ≤ 6 packets/tick regardless of pipe capacity —
+// the surge's 20/tick REQUIRES multi-route redundancy (ECMP) or lane-splitting:
+// that IS the GDD "no bundled redundancy" root cause.
+//
+// Resolution: the FIRST tick the named bundle is no longer saturated (queue
+// below bound) — the player's fix (a parallel pipe / higher tier pools into
+// the same bundle, 2.1) drains it; the pool-exhaustion cause resolves when the
+// pool's shedding stops.
+//
+// Dedup [E13]: Crisis_State.active holds ONE crisis per (archetype, set-piece)
+// activation; while ACTIVE the condition is never re-emitted. Re-trigger only
+// after Crisis_Resolved; the archetype's cooldown_ticks gates re-fire of the
+// same root cause (0 = immediate — the MVP data). The cooldown bookkeeping is
+// DERIVED engine memory (same status as sla_breach — its only observable
+// effect is the serialized event/state stream, so replay recomputes it
+// identically; never serialized).
+//
+// Integer-only (ODN-10); arrays only, no maps (ODN-10); no file/clock reads
+// (ODN-1). The active rows ride the T1 hash (serialize.odin `crises` section,
+// absent-when-empty); the trigger/resolve events ride the event stream.
+
+// CRISIS_RESOLVE_MARGIN — the resolve hysteresis (4.2): a crisis ends only
+// when the named bottleneck's class backlog falls strictly below
+// (bound - margin) AND the ladder stopped shedding on it that tick. The
+// settled queue oscillates ±1-2 around the bound on the service/completion
+// phase, so without the margin a marginal network (service just under
+// arrivals) chatters trigger/resolve every few ticks — the golden discipline
+// pins: a persistent flaw emits ONE trigger per activation [E13].
+CRISIS_RESOLVE_MARGIN :: u32(2)
+
+// Cooldown_Entry — a recently-resolved root cause (the re-fire gate, arch
+// §6.4). Engine memory, never serialized; pruned once stale.
+Cooldown_Entry :: struct {
+	archetype:   u16,
+	kind:        Root_Cause_Kind,
+	bundle:      u32,
+	resolve_tick: u64,
+}
+
+// event_emit_crisis — append a Crisis_Triggered / Crisis_Resolved event with
+// the full root-cause payload (archetype, cause kind, class, bundle, pipe).
+// Both tags share the payload shape (the resolved event carries the ending
+// crisis's refs — the render + the cooldown bookkeeping consume them).
+event_emit_crisis :: proc(state: ^Run_State, tick: u64, tag: u8, ac: Active_Crisis) {
+	append(&state.events, Event{
+		tick = tick,
+		tag = tag,
+		class = ac.class,
+		target = ac.bundle,
+		archetype = u8(ac.archetype),
+		cause = u8(ac.kind),
+		pipe = ac.pipe,
+	})
+}
+
+// bundle_class_queue — the number of on-edge packets of `class` queued on
+// bundle `bi` (the surge class's own backlog on the bottleneck — any lane;
+// the class rides its per-pipe lane, so the backlog is the bundle-wide load).
+// Array-order walk (deterministic, ODN-10).
+bundle_class_queue :: proc(state: ^Run_State, cat: ^Catalogs, bi: u32, class: u16) -> u32 {
+	n: u32 = 0
+	for i in 0..<len(state.flow.packets) {
+		p := &state.flow.packets[i]
+		if p.delivered || !p.on_edge { continue }
+		if p.class != class { continue }
+		b, ok := bundle_of_pipe(state, p.edge)
+		if !ok || b != bi { continue }
+		n += 1
+	}
+	return n
+}
+
+// bundle_lane_at_bound — any (bundle, lane) queue at the E9 bound (the state
+// the drop ladder sheds from). bundle_lane_count counts ALL classes in a lane
+// — the ladder's own measure.
+bundle_lane_at_bound :: proc(state: ^Run_State, cat: ^Catalogs, bi: u32) -> bool {
+	for lane in u8(0)..<LANE_COUNT {
+		if bundle_lane_count(state, cat, bi, lane) >= u32(cat.balance.lane_queue_packets) {
+			return true
+		}
+	}
+	return false
+}
+
+// crisis_bundle_saturated — the per-bundle saturation predicate (the trigger +
+// resolve measure): the surge class has packets queued on the bundle AND some
+// lane of the bundle is at the E9 bound. The class backlog keeps the crisis
+// attributable to the surge (a bundle full of email alone never fires it).
+crisis_bundle_saturated :: proc(state: ^Run_State, cat: ^Catalogs, bi: u32, class: u16) -> bool {
+	if bundle_class_queue(state, cat, bi, class) == 0 { return false }
+	return bundle_lane_at_bound(state, cat, bi)
+}
+
+// first_member_pipe — the first LIVE member pipe id of a bundle (slot order —
+// deterministic; the root-cause ref the render highlights).
+first_member_pipe :: proc(state: ^Run_State, bi: u32) -> u32 {
+	for ps in 0..<len(state.topology.pipe_alive) {
+		if !state.topology.pipe_alive[ps] { continue }
+		if int(ps) >= len(state.bundles.pipe_bundle) { continue }
+		if state.bundles.pipe_bundle[ps] == bi {
+			return state.topology.pipe_id[ps]
+		}
+	}
+	return 0
+}
+
+// drop_of_class_this_tick — did a Packet_Dropped event for `class` with
+// `reason` land this tick, on `bundle`? The events buffer is appended in tick
+// order, so the scan runs TAIL-FIRST and stops at the first older-tick event —
+// O(this tick's events) in every path (the harness drains per tick; the app
+// never drains, so the bounded scan keeps a long session cheap). `bundle`
+// filters the shed site: E9 drops carry the bundle whose lane was at bound;
+// E22 pool drops carry NO_BUNDLE (match any bundle).
+drop_of_class_this_tick :: proc(state: ^Run_State, tick: u64, class: u16, reason: Drop_Reason, bundle: u32) -> bool {
+	for i := len(state.events) - 1; i >= 0; i -= 1 {
+		e := state.events[i]
+		if e.tick < tick { break } // events are tick-ordered — older ticks cannot match
+		if e.tick != tick { continue }
+		if e.tag != EVENT_TAG_PACKET_DROPPED { continue }
+		if e.class != class || e.reason != u8(reason) { continue }
+		if bundle != NO_BUNDLE && e.target != bundle { continue }
+		return true
+	}
+	return false
+}
+
+// crisis_drop_bundle_this_tick — the bundle of the FIRST E9 Queue_Overflow
+// drop of `class` this tick (event order = shed order — deterministic), or
+// NO_BUNDLE. The drop's bundle is the exact admission site — the sharpest
+// root-cause evidence (the settled queue alone dips below the bound on the
+// completion phase, so the drop is what makes saturation attributable).
+// Backward scan with overwrite: the LAST match seen is the EARLIEST drop of
+// the tick (events are tick-ordered; the scan stops at older ticks —
+// O(this tick's events) even in the never-draining app path).
+crisis_drop_bundle_this_tick :: proc(state: ^Run_State, tick: u64, class: u16) -> u32 {
+	bundle := NO_BUNDLE
+	for i := len(state.events) - 1; i >= 0; i -= 1 {
+		e := state.events[i]
+		if e.tick < tick { break }
+		if e.tick != tick { continue }
+		if e.tag != EVENT_TAG_PACKET_DROPPED { continue }
+		if e.class != class || e.reason != u8(Drop_Reason.Queue_Overflow) { continue }
+		bundle = e.target
+	}
+	return bundle
+}
+
+// crisis_find_saturated_bundle — the root-cause element scan for the SETTLED
+// state (slot order, deterministic): the first bundle where the surge class's
+// own queue sits on a bound lane (the pre-drop saturation — the queue at the
+// E9 bound with the class backlog). Returns (bundle, pipe, ok).
+crisis_find_saturated_bundle :: proc(state: ^Run_State, cat: ^Catalogs, class: u16) -> (u32, u32, bool) {
+	for bi in u32(0)..<state.bundles.n {
+		if crisis_bundle_saturated(state, cat, bi, class) {
+			return bi, first_member_pipe(state, bi), true
+		}
+	}
+	return NO_BUNDLE, 0, false
+}
+
+// crisis_active_for — is there an active crisis for this (archetype, set-piece)
+// activation? The [E13] dedup key: one crisis per root cause per activation.
+crisis_active_for :: proc(state: ^Run_State, archetype, set_piece: u16) -> bool {
+	for ac in state.crisis.active {
+		if ac.archetype == archetype && ac.set_piece == set_piece {
+			return true
+		}
+	}
+	return false
+}
+
+// crisis_cooldown_blocked — a same-cause re-trigger blocked by the archetype's
+// cooldown? (tick - resolve_tick) < cooldown gates re-fire (arch §6.4).
+crisis_cooldown_blocked :: proc(state: ^Run_State, tick: u64, cat: ^Catalogs, archetype: u16, kind: Root_Cause_Kind, bundle: u32) -> bool {
+	cd := u64(0)
+	if int(archetype) < len(cat.crises) {
+		cd = cat.crises[archetype].cooldown_ticks
+	}
+	if cd == 0 { return false }
+	for c in state.crisis.cooldowns {
+		if c.archetype == archetype && c.kind == kind && c.bundle == bundle {
+			if tick - c.resolve_tick < cd {
+				return true
+			}
+		}
+	}
+	return false
+}
+
+// crisis_remove_at — ordered removal from the active registry (index order
+// preserved — the trigger/resolve sequence stays deterministic).
+crisis_remove_at :: proc(cr: ^Crisis_State, idx: int) {
+	for j := idx; j < len(cr.active)-1; j += 1 {
+		cr.active[j] = cr.active[j+1]
+	}
+	pop(&cr.active)
+}
+
+// crisis_evaluate — the per-tick crisis pass (called inside core.step AFTER
+// warning_evaluate, BEFORE win_lose_eval — the spine's flow → crisis →
+// win/lose order). Two passes, deterministic order: RESOLUTION first (active
+// crises whose named flaw cleared — the queue drained / the shedding stopped),
+// then TRIGGER (active set-pieces whose class saturates — first tick only,
+// dedup [E13]). A set-piece without an archetype (archetype_idx < 0) never
+// fires anything (a pure demand event). Era 0 / beyond-catalog eras are no-ops
+// (legacy runs unaffected).
+crisis_evaluate :: proc(state: ^Run_State, tick: u64, cat: ^Catalogs) {
+	if state.era == 0 || int(state.era) > len(cat.demand.eras) {
+		return
+	}
+	de := &cat.demand.eras[state.era-1]
+	cr := &state.crisis
+
+	// prune stale cooldown rows. A row with a ZERO cooldown (the MVP data) is
+	// never queried (crisis_cooldown_blocked returns immediately) — pruning it
+	// keeps the registry from growing with every resolve; a nonzero-cooldown
+	// row lives until its window passes. Deterministic order.
+	if len(cr.cooldowns) > 0 {
+		keep := 0
+		for c in cr.cooldowns {
+			cd := u64(0)
+			if int(c.archetype) < len(cat.crises) {
+				cd = cat.crises[c.archetype].cooldown_ticks
+			}
+			if cd > 0 && tick - c.resolve_tick < cd {
+				cr.cooldowns[keep] = c
+				keep += 1
+			}
+		}
+		resize(&cr.cooldowns, keep)
+	}
+
+	// --- 1. RESOLUTION pass (active-list order) ------------------------------
+	i := 0
+	for i < len(cr.active) {
+		ac := &cr.active[i]
+		cleared := false
+		#partial switch ac.kind {
+		case .Saturated_Bundle:
+			// the named bundle is RELIEVED (hysteresis): the class backlog fell
+			// below (bound - CRISIS_RESOLVE_MARGIN) AND NO lane of the bundle is
+			// at the E9 bound (a lane held at bound by ANOTHER class still means
+			// "no spare capacity on this bundle" — without this, a resolved
+			// surge crisis could re-trigger the same tick via the settled scan
+			// and chatter, [E13]) AND the ladder stopped shedding the class on
+			// it this tick (the admission evidence — both must clear, or the
+			// flaw persists).
+			bound := u32(cat.balance.lane_queue_packets)
+			// the margin clamps to bound-1 so a tiny catalog bound (1-2 packets)
+			// can never make resolution unreachable (bound <= margin would
+			// otherwise block a resolve forever). The MVP data pins bound 6.
+			margin := CRISIS_RESOLVE_MARGIN
+			if bound > 0 && bound <= margin { margin = bound - 1 }
+			relieved := bound > 0 &&
+				bundle_class_queue(state, cat, ac.bundle, ac.class) + margin < bound &&
+				!bundle_lane_at_bound(state, cat, ac.bundle)
+			cleared = relieved &&
+				!drop_of_class_this_tick(state, tick, ac.class, .Queue_Overflow, ac.bundle)
+		case .Pool_Exhaustion:
+			// the pool's shedding of the class stopped AND the pool is
+			// meaningfully below its cap (the same hysteresis the E9 path gets
+			// from CRISIS_RESOLVE_MARGIN — a pool hovering at cap oscillates
+			// ±1 and would otherwise chatter trigger/resolve every other tick).
+			cleared = len(state.flow.packets) + int(CRISIS_RESOLVE_MARGIN) < int(cat.balance.pool_max_packets) &&
+				!drop_of_class_this_tick(state, tick, ac.class, .Pool_Exhaustion, NO_BUNDLE)
+		case:
+			cleared = true // defensive — an unknown kind can never linger
+		}
+		if cleared {
+			event_emit_crisis(state, tick, EVENT_TAG_CRISIS_RESOLVED, ac^)
+			append(&cr.cooldowns, Cooldown_Entry{
+				archetype = ac.archetype,
+				kind = ac.kind,
+				bundle = ac.bundle,
+				resolve_tick = tick,
+			})
+			crisis_remove_at(cr, i)
+		} else {
+			i += 1
+		}
+	}
+
+	// --- 2. TRIGGER pass (set-piece order) -----------------------------------
+	for si in 0..<len(de.set_pieces) {
+		sp := &de.set_pieces[si]
+		if sp.archetype_idx < 0 { continue } // a pure demand event — no crisis
+		if !set_piece_active(sp, tick) { continue } // fires on schedule ONLY (the seed's timeline)
+		ai := u16(sp.archetype_idx)
+		if crisis_active_for(state, ai, u16(si)) { continue } // [E13] dedup — one per activation
+
+		// (a/b) the per-element E9 saturation — priority (the sharper root
+		// cause: a named bottleneck). The drop's bundle is the exact admission
+		// site (the sharpest evidence — fires even when the settled queue is a
+		// tick past the dip); the settled scan covers the pre-drop state (the
+		// queue at the bound with the class backlog).
+		bundle := crisis_drop_bundle_this_tick(state, tick, sp.class)
+		if bundle != NO_BUNDLE {
+			pipe := first_member_pipe(state, bundle)
+			if crisis_cooldown_blocked(state, tick, cat, ai, .Saturated_Bundle, bundle) { continue }
+			append(&cr.active, Active_Crisis{
+				archetype = ai,
+				set_piece = u16(si),
+				kind = .Saturated_Bundle,
+				bundle = bundle,
+				pipe = pipe,
+				class = sp.class,
+				multiplier = sp.multiplier,
+				triggered_tick = tick,
+			})
+			event_emit_crisis(state, tick, EVENT_TAG_CRISIS_TRIGGERED, cr.active[len(cr.active)-1])
+			continue
+		}
+		if b, pipe, ok := crisis_find_saturated_bundle(state, cat, sp.class); ok {
+			if crisis_cooldown_blocked(state, tick, cat, ai, .Saturated_Bundle, b) { continue }
+			append(&cr.active, Active_Crisis{
+				archetype = ai,
+				set_piece = u16(si),
+				kind = .Saturated_Bundle,
+				bundle = b,
+				pipe = pipe,
+				class = sp.class,
+				multiplier = sp.multiplier,
+				triggered_tick = tick,
+			})
+			event_emit_crisis(state, tick, EVENT_TAG_CRISIS_TRIGGERED, cr.active[len(cr.active)-1])
+			continue
+		}
+		// (c) the pool-exhaustion backstop: the global pool at cap + the class
+		// shedding (E22 drops) — a map-wide capacity shortfall (no element
+		// ref; the whole network is the flaw).
+		if len(state.flow.packets) >= int(cat.balance.pool_max_packets) &&
+			drop_of_class_this_tick(state, tick, sp.class, .Pool_Exhaustion, NO_BUNDLE) {
+			if crisis_cooldown_blocked(state, tick, cat, ai, .Pool_Exhaustion, NO_BUNDLE) { continue }
+			append(&cr.active, Active_Crisis{
+				archetype = ai,
+				set_piece = u16(si),
+				kind = .Pool_Exhaustion,
+				bundle = NO_BUNDLE,
+				pipe = 0,
+				class = sp.class,
+				multiplier = sp.multiplier,
+				triggered_tick = tick,
+			})
+			event_emit_crisis(state, tick, EVENT_TAG_CRISIS_TRIGGERED, cr.active[len(cr.active)-1])
+		}
+	}
+}
diff --git a/core/crisis_test.odin b/core/crisis_test.odin
new file mode 100644
index 0000000..a270e00
--- /dev/null
+++ b/core/crisis_test.odin
@@ -0,0 +1,432 @@
+package core
+
+// crisis_test.odin — pins the 4.2 crisis engine (crisis.odin):
+//   (a) the surge fires on schedule from the seed — Crisis_Triggered at the
+//       exact first-saturated tick inside the window [1200, 3000), carrying
+//       the structured root cause (kind, bundle, pipe, class, multiplier);
+//   (b) no crisis on a healthy within-capacity topology [AC-E13] — a
+//       multi-route fan with spare capacity passes the surge with ZERO
+//       streaming drops and ZERO crisis events;
+//   (c) dedup [E13] — a persistent flaw never re-fires; exactly one trigger
+//       per activation;
+//   (d) resolve + re-trigger [E13] — the player's capacity fix drains the
+//       queue (Crisis_Resolved); demolishing the fix re-saturates
+//       (re-trigger, cooldown 0); a nonzero cooldown gates re-fire;
+//   (e) the pool-exhaustion backstop — a disconnected map fills the global
+//       pool; the crisis fires with the map-wide cause, resolves once the
+//       fix lets it drain;
+//   (f) no trigger outside the window (the engine fires on schedule ONLY);
+//   (g) replay byte-identity (E10) — identical hash sequences for identical
+//       runs; the terminal barrier (E17) freezes the crisis state.
+//
+// All expectations are GOLDEN-VERIFIED (the 3.4 pattern): the sim is seeded
+// + deterministic, so the crossing ticks are exact. If a threshold or a
+// spawn lands differently, the ticks here must be re-read from the sim and
+// re-pinned — never guessed.
+
+import "core:testing"
+
+// crisis_seed_fixture — a narrow-legal fixture: residential(0) @{8,15},
+// router(1) @{14,15}, content_host(2) @{20,15} (6-tile spans — narrow
+// max_span 10) + the two narrow pipes drawn at tick 1 (res->router,
+// router->host). The host->router bundle is the bottleneck: service 5
+// units/tick (0.167 packets/tick) vs the streaming demand — saturated at
+// base demand, so the surge window opens on an already-saturated flaw.
+crisis_seed_fixture :: proc(s: ^Run_State, cat: ^Catalogs) -> (u32, u32, u32) {
+	res_idx, _ := node_type_index(cat, "residential")
+	rt_idx, _ := node_type_index(cat, "router_basic")
+	host_idx, _ := node_type_index(cat, "content_host")
+	r := topology_spawn_node(&s.topology, res_idx, {8, 15}, cat)
+	g := topology_spawn_node(&s.topology, rt_idx, {14, 15}, cat)
+	h := topology_spawn_node(&s.topology, host_idx, {20, 15}, cat)
+	sla_draw(s, cat, r, g, "narrow", 1)
+	sla_draw(s, cat, g, h, "narrow", 1)
+	return r, g, h
+}
+
+// crisis_record_run — step a run collecting the crisis event stream (the
+// ODN-14 drain convention: record_run clears the buffer per tick, so
+// event-scans must collect as they step) + the per-tick hashes. Only
+// Crisis_Triggered / Crisis_Resolved events are collected.
+crisis_record_run :: proc(s: ^Run_State, ticks: u64, cat: ^Catalogs) -> ([dynamic]u64, [dynamic]Event) {
+	hashes := make([dynamic]u64, 0, ticks)
+	events := make([dynamic]Event, 0, 8)
+	start := s.tick + 1 // resume from the state's next tick (mid-run callers)
+	for tick in start ..< start + ticks {
+		before := len(s.events)
+		batch := make([dynamic]Command, 0, 4, context.temp_allocator)
+		for cmd in s.action_log {
+			if cmd.apply_tick == tick {
+				append(&batch, cmd)
+			}
+		}
+		step(s, tick, batch[:], cat)
+		for e in s.events[before:] {
+			if e.tag == EVENT_TAG_CRISIS_TRIGGERED || e.tag == EVENT_TAG_CRISIS_RESOLVED {
+				append(&events, e)
+			}
+		}
+		append(&hashes, state_hash(s, s.events[before:], cat, context.temp_allocator))
+		clear(&s.events)
+		free_all(context.temp_allocator)
+	}
+	return hashes, events
+}
+
+// crisis_assert_stream — the exact-stream pin: every collected crisis event
+// must equal the expected (tick, tag, archetype, cause, class, target, pipe)
+// in order, and vice versa.
+crisis_assert_stream :: proc(t: ^testing.T, got: []Event, want: []Event) {
+	testing.expectf(t, len(got) == len(want), "crisis stream: got %d events, want %d — %v",
+		len(got), len(want), got)
+	for i in 0..<min(len(got), len(want)) {
+		e := got[i]
+		w := want[i]
+		testing.expectf(t, e.tick == w.tick && e.tag == w.tag && e.archetype == w.archetype &&
+			e.cause == w.cause && e.class == w.class && e.target == w.target && e.pipe == w.pipe,
+			"event %d: got (tick %d tag %d arch %d cause %d class %d bundle %d pipe %d) want (tick %d tag %d arch %d cause %d class %d bundle %d pipe %d)",
+			i, e.tick, e.tag, e.archetype, e.cause, e.class, e.target, e.pipe,
+			w.tick, w.tag, w.archetype, w.cause, w.class, w.target, w.pipe)
+	}
+}
+
+// --- (a) surge on schedule + dedup --------------------------------------------
+
+@(test)
+test_crisis_surge_trigger_on_schedule :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	crisis_seed_fixture(&s, cat)
+
+	// pre-window: the flaw is saturated at base demand but the window is
+	// closed — the engine must not fire (the schedule gates everything).
+	hashes_pre, evs_pre := crisis_record_run(&s, 1199, cat)
+	defer delete(hashes_pre)
+	defer delete(evs_pre)
+	testing.expectf(t, len(evs_pre) == 0, "no crisis may fire before the window, got %v", evs_pre)
+
+	// the window [1200, 3000): at 1200 the 20/tick surge arrives at the
+	// already-bound queue — the first saturated tick. Exactly ONE trigger
+	// while the flaw persists (dedup [E13]) and no resolve (no fix).
+	hashes, evs := crisis_record_run(&s, 1800, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	crisis_assert_stream(t, evs[:], []Event{
+		{tick = 1200, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 1},
+	})
+	testing.expectf(t, len(s.crisis.active) == 1, "one active crisis expected, got %d", len(s.crisis.active))
+	ac := s.crisis.active[0]
+	testing.expect_value(t, ac.archetype, u16(0))
+	testing.expect_value(t, ac.set_piece, u16(0))
+	testing.expect_value(t, ac.kind, Root_Cause_Kind.Saturated_Bundle)
+	testing.expect_value(t, ac.bundle, u32(1)) // the host->router bundle (pipe 1's)
+	testing.expect_value(t, ac.pipe, u32(1))
+	testing.expect_value(t, ac.class, u16(1)) // streaming
+	testing.expect_value(t, ac.multiplier, i32(10))
+	testing.expect_value(t, ac.triggered_tick, u64(1200))
+}
+
+// --- (b) no crisis on a healthy within-capacity topology [AC-E13] -------------
+
+// crisis_seed_capable_path — a within-capacity path for the mult2 catalog
+// (surge = 2/tick): res -> router -> host with TWO parallel wides per side
+// (pooled service 2.67/tick >= arrivals; 4 ports — the basic router's max).
+// The queue hovers at ~2-3 — never near the 6-packet E9 bound, no drops.
+crisis_seed_capable_path :: proc(s: ^Run_State, cat: ^Catalogs) {
+	res_idx, _ := node_type_index(cat, "residential")
+	rt_idx, _ := node_type_index(cat, "router_basic")
+	host_idx, _ := node_type_index(cat, "content_host")
+	r := topology_spawn_node(&s.topology, res_idx, {8, 15}, cat)
+	g := topology_spawn_node(&s.topology, rt_idx, {14, 15}, cat)
+	h := topology_spawn_node(&s.topology, host_idx, {20, 15}, cat)
+	sla_draw(s, cat, r, g, "wide", 1)
+	sla_draw(s, cat, r, g, "wide", 1)
+	sla_draw(s, cat, g, h, "wide", 1)
+	sla_draw(s, cat, g, h, "wide", 1)
+}
+
+@(test)
+test_crisis_healthy_topology_passes_surge :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	crisis_catalog_mult2(cat, 0) // the surge = 2/tick here — the [AC-E13]
+	// contract is magnitude-independent: the engine keys on measurable
+	// saturation (queue-at-bound / drops), never the schedule's numbers.
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 7, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	crisis_seed_capable_path(&s, cat)
+
+	// through the whole window + a settle tail: no crisis, and the surge
+	// class must not drop a single packet (the within-capacity contract).
+	hashes, evs := crisis_record_run(&s, 3020, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	testing.expectf(t, len(evs) == 0, "a healthy within-capacity topology must never fire a crisis, got %v", evs)
+	testing.expectf(t, len(s.crisis.active) == 0, "no active crisis expected, got %d", len(s.crisis.active))
+	// the streaming class's SLA: zero drops — the surge passed clean
+	stream_idx := u16(1)
+	if int(stream_idx) < len(s.flow.sla) {
+		acc := &s.flow.sla[stream_idx]
+		testing.expectf(t, acc.dropped == 0, "streaming dropped %d packets on a within-capacity topology", acc.dropped)
+	}
+}
+
+// --- (d) resolve + re-trigger [E13] -------------------------------------------
+
+// crisis_catalog_mult2 — test_catalog with a gentler surge (era-3 streaming
+// volume 1, multiplier 2 → 2/tick in the window) + the optional cooldown.
+// The narrow bottleneck (0.167/tick service) saturates at base demand; two
+// parallel wides (2.83/tick) drain it — the player's fix.
+crisis_catalog_mult2 :: proc(cat: ^Catalogs, cooldown: u64) {
+	cat.demand.eras[2].entries[1].volume = 1
+	cat.demand.eras[2].set_pieces[0].multiplier = 2
+	cat.crises[0].cooldown_ticks = cooldown
+}
+
+@(test)
+test_crisis_resolve_and_retrigger :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	crisis_catalog_mult2(cat, 0) // cooldown 0 — re-fire allowed immediately
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	crisis_seed_fixture(&s, cat)
+	// the fix: the narrows (pipes 0,1 — the flaw) are demolished @1499, freeing
+	// the router's 4 ports; two parallel wides per side land @1500 (pipes 2..5;
+	// pooled service 2.67/tick >= the 2/tick surge volume). The demolish @1600:
+	// ONE router->host wide (pipe 5) — the path drops back to 1.33/tick
+	// service < arrivals, re-saturating the flaw (re-trigger, cooldown 0).
+	append(&s.action_log, Command{apply_tick = 1499, kind = Cmd_Demolish_Pipe{pipe = 0}})
+	append(&s.action_log, Command{apply_tick = 1499, kind = Cmd_Demolish_Pipe{pipe = 1}})
+	sla_draw(&s, cat, 0, 1, "wide", 1500)
+	sla_draw(&s, cat, 0, 1, "wide", 1500)
+	sla_draw(&s, cat, 1, 2, "wide", 1500)
+	sla_draw(&s, cat, 1, 2, "wide", 1500)
+	append(&s.action_log, Command{apply_tick = 1600, kind = Cmd_Demolish_Pipe{pipe = 5}})
+
+	hashes, evs := crisis_record_run(&s, 3010, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	// The golden-verified lifecycle (read from the run): trigger @1200 (the
+	// window opens on the saturated flaw) → the demolish of the narrows @1499
+	// removes the flaw (resolve) → the severed backlog floods the fresh wides
+	// @1500 (a transient re-trigger — the backlog saturates the new bundle) →
+	// the backlog drains below the resolve margin @1502 (resolve) → the
+	// demolish of one wide @1600 re-saturates the path @1604 (re-trigger,
+	// cooldown 0) → the window ends and base demand clears the backlog @3003
+	// (resolve). Each transition is one tick in the pinned stream — dedup
+	// [E13] holds: a persistent state never re-fires.
+	crisis_assert_stream(t, evs[:], []Event{
+		{tick = 1200, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 1},
+		{tick = 1499, tag = EVENT_TAG_CRISIS_RESOLVED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 1},
+		{tick = 1500, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 4},
+		{tick = 1502, tag = EVENT_TAG_CRISIS_RESOLVED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 4},
+		{tick = 1604, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 4},
+		{tick = 3003, tag = EVENT_TAG_CRISIS_RESOLVED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 4},
+	})
+}
+
+@(test)
+test_crisis_cooldown_gates_retrigger :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	crisis_catalog_mult2(cat, 300) // 300-tick re-fire gate
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	crisis_seed_fixture(&s, cat)
+	// the same fix as the cooldown-0 test (narrows demolished @1499, wides
+	// @1500, one router->host wide demolished @1600)
+	append(&s.action_log, Command{apply_tick = 1499, kind = Cmd_Demolish_Pipe{pipe = 0}})
+	append(&s.action_log, Command{apply_tick = 1499, kind = Cmd_Demolish_Pipe{pipe = 1}})
+	sla_draw(&s, cat, 0, 1, "wide", 1500)
+	sla_draw(&s, cat, 0, 1, "wide", 1500)
+	sla_draw(&s, cat, 1, 2, "wide", 1500)
+	sla_draw(&s, cat, 1, 2, "wide", 1500)
+	append(&s.action_log, Command{apply_tick = 1600, kind = Cmd_Demolish_Pipe{pipe = 5}})
+
+	hashes, evs := crisis_record_run(&s, 3010, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	// the cooldown (300) gates the re-fire: the transient backlog trigger
+	// @1500 is blocked (1500 - 1499 = 1 < 300) and the post-demolish
+	// re-saturation @1604 is blocked (1604 - 1499 = 105 < 300); the same
+	// cause fires exactly at cooldown expiry @1799 (1799 - 1499 = 300 >= 300)
+	// while the flaw is still saturated. The window-end relief resolves it
+	// @3003 like the cooldown-0 run.
+	crisis_assert_stream(t, evs[:], []Event{
+		{tick = 1200, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 1},
+		{tick = 1499, tag = EVENT_TAG_CRISIS_RESOLVED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 1},
+		{tick = 1799, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 4},
+		{tick = 3003, tag = EVENT_TAG_CRISIS_RESOLVED, archetype = 0, cause = u8(Root_Cause_Kind.Saturated_Bundle), class = 1, target = 1, pipe = 4},
+	})
+}
+
+// --- (e) the pool-exhaustion backstop ------------------------------------------
+
+@(test)
+test_crisis_pool_exhaustion :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	cat.balance.pool_max_packets = 16 // a small pool — the backstop engages fast (and drains after the fix: steady-state in-flight ~10 fits under it)
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	// NO pipes: the streaming packets wait at the host (no route — complete
+	// paths only), the pool fills, E22 sheds the surge class. No bundle can
+	// saturate (there are none) — the E9 path cannot fire.
+	res_idx, _ := node_type_index(cat, "residential")
+	rt_idx, _ := node_type_index(cat, "router_basic")
+	host_idx, _ := node_type_index(cat, "content_host")
+	topology_spawn_node(&s.topology, res_idx, {8, 15}, cat)
+	topology_spawn_node(&s.topology, rt_idx, {14, 15}, cat)
+	topology_spawn_node(&s.topology, host_idx, {20, 15}, cat)
+	// the fix at tick 1501: two parallel wides on BOTH edges (service 2.83/tick
+	// >= the post-window base 2/tick — the pool drains, the shedding stops).
+	// During the window the 20/tick surge keeps the pool at cap, so the E22
+	// crisis persists until the window ends.
+	sla_draw(&s, cat, 0, 1, "wide", 1500)
+	sla_draw(&s, cat, 0, 1, "wide", 1500)
+	sla_draw(&s, cat, 1, 2, "wide", 1500)
+	sla_draw(&s, cat, 1, 2, "wide", 1500)
+
+	hashes, evs := crisis_record_run(&s, 3010, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	// @1200: pool at cap + streaming E22 drops → the map-wide cause. @3000:
+	// the window ended, the route delivers, the shedding stops → resolved.
+	// (The exact resolve tick is read from the run — the drain depends on the
+	// seeded delivery timing.)
+	crisis_assert_stream(t, evs[:], []Event{
+		{tick = 1200, tag = EVENT_TAG_CRISIS_TRIGGERED, archetype = 0, cause = u8(Root_Cause_Kind.Pool_Exhaustion), class = 1, target = NO_BUNDLE, pipe = 0},
+		{tick = 3000, tag = EVENT_TAG_CRISIS_RESOLVED, archetype = 0, cause = u8(Root_Cause_Kind.Pool_Exhaustion), class = 1, target = NO_BUNDLE, pipe = 0},
+	})
+}
+
+// --- (f) no trigger outside the window -----------------------------------------
+
+@(test)
+test_crisis_no_trigger_outside_window :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	crisis_seed_fixture(&s, cat)
+	// after the window [1200, 3000): the flaw stays saturated (narrow pipe,
+	// base demand 2/tick) but the set-piece is inactive — no new events; the
+	// (never-resolved) crisis just persists.
+	hashes_pre, evs_pre := crisis_record_run(&s, 1199, cat)
+	defer delete(hashes_pre)
+	defer delete(evs_pre)
+	hashes, evs := crisis_record_run(&s, 1800, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	hashes_post, evs_post := crisis_record_run(&s, 500, cat)
+	defer delete(hashes_post)
+	defer delete(evs_post)
+	testing.expectf(t, len(evs_post) == 0, "no crisis may fire after the window, got %v", evs_post)
+	testing.expectf(t, len(s.crisis.active) == 1, "the never-resolved crisis persists, got %d", len(s.crisis.active))
+}
+
+// --- (g) replay identity + the terminal barrier --------------------------------
+
+@(test)
+test_crisis_replay_identity :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+
+	run := proc(cat: ^Catalogs) -> [dynamic]u64 {
+		s: Run_State
+		defer run_destroy(&s)
+		run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+		s.era = 3
+		crisis_seed_fixture(&s, cat)
+		sla_draw(&s, cat, 1, 2, "wide", 1500) // the mid-run fix
+		hashes, _ := crisis_record_run(&s, 2400, cat)
+		return hashes
+	}
+	// the SAME run twice: byte-identical hash sequences (E10 — the crisis
+	// state + events ride the T1 hash, so a divergent engine would diverge
+	// here).
+	h1 := run(cat)
+	defer delete(h1)
+	h2 := run(cat)
+	defer delete(h2)
+	testing.expectf(t, len(h1) == len(h2), "run lengths differ: %d vs %d", len(h1), len(h2))
+	for i in 0..<min(len(h1), len(h2)) {
+		if h1[i] != h2[i] {
+			testing.expectf(t, false, "hash divergence at tick %d: %016x vs %016x", i+1, h1[i], h2[i])
+			break
+		}
+	}
+}
+
+@(test)
+test_crisis_terminal_freeze :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3
+	crisis_seed_fixture(&s, cat)
+	s.goal = 0
+	s.tick_cap = 100 // lose at tick 100 — BEFORE the window opens
+	hashes, evs := crisis_record_run(&s, 1400, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	// the run froze at tick 100 (Run_Lost, E17): the window opens at 1200 but
+	// crisis_evaluate never runs again — no crisis events, no active rows.
+	testing.expect_value(t, s.outcome, Outcome.Lost)
+	testing.expectf(t, len(evs) == 0, "a frozen run must never fire a crisis, got %v", evs)
+	testing.expectf(t, len(s.crisis.active) == 0, "a frozen run has no crisis state, got %d", len(s.crisis.active))
+}
+
+// --- (h) legacy / era-0 neutrality (the I/O-matrix "Legacy / era 0: no-op" row) ---
+
+@(test)
+test_crisis_era_zero_noop :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 42, cat.hash, TEST_LOGIC_HZ)
+	// era stays 0 (legacy — no director demand, no set-piece schedule): the
+	// engine must be a strict no-op — no events, no active rows, even though
+	// the era-3 schedule exists in the catalog.
+	crisis_seed_fixture(&s, cat)
+	hashes, evs := crisis_record_run(&s, 3020, cat)
+	defer delete(hashes)
+	defer delete(evs)
+	testing.expectf(t, len(evs) == 0, "an era-0 run must never fire a crisis, got %v", evs)
+	testing.expectf(t, len(s.crisis.active) == 0, "an era-0 run has no active crisis, got %d", len(s.crisis.active))
+}
diff --git a/core/determinism_test.odin b/core/determinism_test.odin
index e4bd87d..e7da9fa 100644
--- a/core/determinism_test.odin
+++ b/core/determinism_test.odin
@@ -66,7 +66,8 @@ test_catalog :: proc(cat: ^Catalogs, allocator := context.allocator) -> ^Catalog
 	append(&cat.packet_types, Packet_Type{id = "email", display = "Email", shape = .Circle, icon = "mail", color_rgba = {90, 98, 112, 255}, latency_tol_ms = 500, max_loss_pct = 30, bandwidth_demand = 1, default_lane = 1, demand_weight = 1, era_introduced = 1})
 	append(&cat.packet_types, Packet_Type{id = "streaming", display = "Streaming", shape = .Triangle, icon = "play", color_rgba = {30, 74, 152, 255}, latency_tol_ms = 300, max_loss_pct = 10, bandwidth_demand = 2, default_lane = 1, demand_weight = 1, era_introduced = 3})
 	// 3.1: the per-era demand (mirrors data/demand.json — eras 1/2 email-only,
-	// era 3 email + streaming + the streaming_surge set-piece).
+	// era 3 email + streaming + the streaming_surge set-piece). 4.2: the surge
+	// set-piece names its crisis archetype (crises.json cross-ref).
 	cat.demand.eras = make([dynamic]Demand_Era, 0, 4, allocator)
 	make_era := proc(cat: ^Catalogs, volume: i32, streaming: bool, allocator: mem.Allocator) {
 		e: Demand_Era
@@ -75,13 +76,24 @@ test_catalog :: proc(cat: ^Catalogs, allocator := context.allocator) -> ^Catalog
 		append(&e.entries, Demand_Entry{class = 0, source_role = .Residential, sink_role = .Residential, volume = volume, default_lane = 1, selection = .Weighted_Random, demand_weight = 1})
 		if streaming {
 			append(&e.entries, Demand_Entry{class = 1, source_role = .Content_Host, sink_role = .Residential, volume = 2, default_lane = 1, selection = .Weighted_Random, demand_weight = 1})
-			append(&e.set_pieces, Set_Piece{id = "streaming_surge", class = 1, multiplier = 10, start_tick = 1200, duration_ticks = 1800, forecast_lead_ticks = 600})
+			append(&e.set_pieces, Set_Piece{id = "streaming_surge", class = 1, multiplier = 10, start_tick = 1200, duration_ticks = 1800, forecast_lead_ticks = 600, archetype_idx = 0})
 		}
 		append(&cat.demand.eras, e)
 	}
 	make_era(cat, 2, false, allocator) // era 1
 	make_era(cat, 2, false, allocator) // era 2
 	make_era(cat, 4, true, allocator)  // era 3 — the streaming surge era
+	// 4.2: the crisis archetype table (mirrors data/crises.json) — the surge
+	// archetype at index 0 (the set-piece cross-ref above).
+	cat.crises = make([dynamic]Crisis_Archetype, 0, 2, allocator)
+	append(&cat.crises, Crisis_Archetype{
+		id = "surge",
+		display_name = "Surge",
+		root_cause_pattern = "saturation",
+		failure_effect = "cascade_saturation",
+		preventive_redesign = "Build spare capacity on the forecast spike's path.",
+		cooldown_ticks = 0,
+	})
 	return cat
 }
 
diff --git a/core/flow.odin b/core/flow.odin
index 34dd430..484fad3 100644
--- a/core/flow.odin
+++ b/core/flow.odin
@@ -147,9 +147,9 @@ flow_spawn :: proc(f: ^Flow_State, class: u16, src, dst: u32, tick: u64) {
 // accounting cannot drift from the event stream (the dropped half of the
 // pinned invariant; the 2.3 silent severance cull — which emits NO event —
 // counts explicitly at its cull site).
-event_emit_drop :: proc(state: ^Run_State, tick: u64, class: u16, reason: Drop_Reason) {
+event_emit_drop :: proc(state: ^Run_State, tick: u64, class: u16, reason: Drop_Reason, bundle: u32) {
 	sla_count_drop(&state.flow, class)
-	append(&state.events, Event{tick = tick, tag = EVENT_TAG_PACKET_DROPPED, class = class, reason = u8(reason)})
+	append(&state.events, Event{tick = tick, tag = EVENT_TAG_PACKET_DROPPED, class = class, reason = u8(reason), target = bundle})
 }
 
 // --- 3.4: per-class SLA accounting + breach evaluation ------------------------
@@ -469,7 +469,7 @@ flow_try_spawn :: proc(state: ^Run_State, cat: ^Catalogs, class: u16, src, dst:
 		if shed_idx >= 0 && shed_lane > arrive_lane {
 			// the target is STRICTLY lower priority than the arrival — a
 			// lower-priority resident pays (the ladder's letter: BE drops first)
-			event_emit_drop(state, tick, f.packets[shed_idx].class, .Pool_Exhaustion)
+			event_emit_drop(state, tick, f.packets[shed_idx].class, .Pool_Exhaustion, NO_BUNDLE)
 			flow_remove_at(f, shed_idx)
 		} else {
 			// the arrival is the lowest-priority candidate present (its lane is
@@ -479,7 +479,7 @@ flow_try_spawn :: proc(state: ^Run_State, cat: ^Catalogs, class: u16, src, dst:
 			// WAS a demand attempt (3.4): demand_seen counts it; the drop event
 			// (below) counts dropped. The invariant demand_seen == delivered +
 			// dropped + live holds — the arrival contributes 1 to both sides.
-			event_emit_drop(state, tick, class, .Pool_Exhaustion)
+			event_emit_drop(state, tick, class, .Pool_Exhaustion, NO_BUNDLE)
 			sla_count_demand(&state.flow, class)
 			return false
 		}
@@ -693,12 +693,12 @@ flow_step :: proc(state: ^Run_State, tick: u64, cat: ^Catalogs) {
 						shed_idx = newest_in_bundle_lane(state, cat, b, l, drops[:])
 						if l != lane {
 							// a lower-priority queued packet pays for the arrival
-							event_emit_drop(state, tick, state.flow.packets[shed_idx].class, .Queue_Overflow)
+							event_emit_drop(state, tick, state.flow.packets[shed_idx].class, .Queue_Overflow, b)
 							append(&drops, shed_idx)
 						} else {
 							// the arriving packet is the shed target — it drops,
 							// never joining the queue
-							event_emit_drop(state, tick, p.class, .Queue_Overflow)
+							event_emit_drop(state, tick, p.class, .Queue_Overflow, b)
 							append(&drops, i)
 							admit = false
 						}
diff --git a/core/serialize.odin b/core/serialize.odin
index 6a58ed9..096cf4c 100644
--- a/core/serialize.odin
+++ b/core/serialize.odin
@@ -217,6 +217,28 @@ state_writer :: proc(state: ^Run_State, tick_events: []Event, cat: ^Catalogs,
 		}
 	}
 
+	// 4.2 active-crisis rows — SERIALIZED (the T1 golden contract: the crisis
+	// lifecycle in the hash, E10) but ABSENT-WHEN-EMPTY: while no crisis is
+	// active the section is omitted entirely, so zero-crisis runs hash
+	// byte-identically modulo the catalog_hash fold (the golden-stability
+	// rule). Rows in active-list order (trigger order — deterministic; replay
+	// recomputes them from the serialized flow + schedule + event history).
+	// The cooldown bookkeeping is NOT serialized (derived engine memory — its
+	// only observable effect is the serialized event/state stream).
+	if len(c.active) > 0 {
+		w_u32(&w, u32(len(c.active)))
+		for ac in c.active {
+			w_u16(&w, ac.archetype)
+			w_u16(&w, ac.set_piece)
+			w_u8(&w, u8(ac.kind))
+			w_u32(&w, ac.bundle)
+			w_u32(&w, ac.pipe)
+			w_u16(&w, ac.class)
+			w_i32(&w, ac.multiplier)
+			w_u64(&w, ac.triggered_tick)
+		}
+	}
+
 	// the Topology — the network commands mutate. Serialized slot-by-slot
 	// (alive flags included so tombstones/id-monotonicity ride in the hash,
 	// E11), in insertion order (stable, ODN-10). THIS is what makes the drawn
@@ -343,6 +365,7 @@ state_writer :: proc(state: ^Run_State, tick_events: []Event, cat: ^Catalogs,
 		if e.tag == EVENT_TAG_PACKET_DROPPED {
 			w_u16(&w, e.class)
 			w_u8(&w, e.reason)
+			w_u32(&w, e.target) // 4.2: the shed bundle (E9) / NO_BUNDLE (E22) — the crisis root-cause evidence
 		}
 		if e.tag == EVENT_TAG_SLA_THRESHOLD_CROSSED {
 			w_u16(&w, e.class)
@@ -353,6 +376,13 @@ state_writer :: proc(state: ^Run_State, tick_events: []Event, cat: ^Catalogs,
 			w_u8(&w, e.sign)
 			w_u32(&w, e.target)
 		}
+		if e.tag == EVENT_TAG_CRISIS_TRIGGERED || e.tag == EVENT_TAG_CRISIS_RESOLVED {
+			w_u8(&w, e.archetype)
+			w_u8(&w, e.cause)
+			w_u16(&w, e.class)
+			w_u32(&w, e.target)
+			w_u32(&w, e.pipe)
+		}
 	}
 
 	return w
diff --git a/core/step.odin b/core/step.odin
index e6f01bf..b40f22c 100644
--- a/core/step.odin
+++ b/core/step.odin
@@ -25,6 +25,18 @@ package core
 // harness/app pass the already-loaded Catalogs pointer; core stays pure (no
 // file I/O — ODN-1).
 step :: proc(state: ^Run_State, tick: u64, commands: []Command, cat: ^Catalogs) {
+	// The tick-sequence invariant (4.2 review hardening): step ticks are
+	// strictly monotonic (every caller — harness, app frame loop, tests —
+	// steps forward from state.tick + 1). The crisis engine's drop scans rely
+	// on the events buffer being tick-ordered (the app never drains it), so a
+	// non-monotonic step would silently truncate a scan. A backward tick is a
+	// CRITICAL divergence — latch it like a replayed command failure (§7.1:
+	// never silent), never corrupt forward.
+	if tick < state.tick {
+		state.replay_error = true
+		return
+	}
+
 	// Terminal-event barrier (E17, §6.5): once Run_Won/Run_Lost has latched, the
 	// run is FROZEN — no command apply, no routing rebuild, no flow, no eval. The
 	// tick is NOT advanced (state.tick stays at the terminal tick), so the
@@ -87,6 +99,16 @@ step :: proc(state: ^Run_State, tick: u64, commands: []Command, cat: ^Catalogs)
 	// hash (E10). Firing anything is 4.2; this only ever *names* trouble.
 	warning_evaluate(state, tick, cat)
 
+	// 4.2: the crisis engine (S4, ODN-4) — the consequence half. Downstream
+	// of flow (the saturation it measures is the flow's own E9/E22 state),
+	// read-only topology view: when a set-piece with a crisis archetype is
+	// ACTIVE on schedule, a crisis fires only on measurable saturation
+	// (queue-at-bound / drops) — no crisis on a healthy within-capacity
+	// topology [AC-E13]; one per root cause per activation [E13]. Emits
+	// Crisis_Triggered / Crisis_Resolved (tags 8/9). The Director (ODN-7)
+	// never sees this state — its signature is (cat, era, tick), structural.
+	crisis_evaluate(state, tick, cat)
+
 	// the win/lose gate (1.4 stub, §6.5): score >= goal -> Run_Won; tick cap hit
 	// with score < goal -> Run_Lost. Appends exactly one terminal event + latches
 	// `terminal`/`outcome`; the barrier above freezes subsequent ticks (E17).
diff --git a/core/types.odin b/core/types.odin
index b7dafd5..6692c29 100644
--- a/core/types.odin
+++ b/core/types.odin
@@ -202,6 +202,32 @@ Forecast_Entry :: struct {
 	active:          bool, // tick >= start_tick (inside the active span)
 }
 
+// Root_Cause_Kind — WHAT topology flaw a crisis names (4.2, ODN-4). The
+// structured root cause is the fairness contract's ref half: a crisis fires
+// only with a resolvable flaw + a preventive redesign (the catalog string).
+Root_Cause_Kind :: enum u8 {
+	None,
+	Saturated_Bundle, // the named bundle's lane queue is at the E9 bound (no spare capacity on the surge's path)
+	Pool_Exhaustion,  // the global in-flight pool is at cap + shedding (map-wide capacity shortfall; no element ref)
+}
+
+// Active_Crisis — one live crisis on Run_State (4.2, arch §6.4 S4). The dedup
+// key is (archetype, set_piece) — one active crisis per root cause per
+// ACTIVATION [E13]: while present, the trigger condition is never re-emitted.
+// The refs (bundle/pipe/class/multiplier) are the structured root_cause; the
+// preventive_redesign is the archetype's catalog string (display — the app
+// renders it; determinism rides the refs, never the string).
+Active_Crisis :: struct {
+	archetype:     u16, // crises.json archetype index
+	set_piece:     u16, // era set-piece index (which activation this crisis belongs to)
+	kind:          Root_Cause_Kind,
+	bundle:        u32, // Saturated_Bundle: the bottleneck bundle slot (NO_BUNDLE otherwise)
+	pipe:          u32, // Saturated_Bundle: the first live member pipe id (0 otherwise)
+	class:         u16, // the surge class (packet_types index)
+	multiplier:    i32, // the activation's spawn multiplier (x10 surge)
+	triggered_tick: u64,
+}
+
 // Crisis_State — the 4.1 warning surface (arch §8.2: warnings/forecast rows
 // owned by Run_State). ALL fields are DERIVED per tick inside warning_evaluate
 // (warnings.odin) from serialized state (topology + packets + era + tick +
@@ -209,10 +235,16 @@ Forecast_Entry :: struct {
 // sla_breach: NEVER serialized in full. The serializer emits only the non-None
 // entries + forecast rows (absent-when-empty) so the T1 golden pins the
 // warning state (E10) without binding replay to the derivation order.
+// 4.2: `active` is the crisis registry (dedup [E13]) — evaluated per tick by
+// crisis_evaluate (crisis.odin) from the same serialized state + the event
+// stream (trigger/resolve transitions ARE the lifecycle; the rows are the
+// per-tick pin). Serialized absent-when-empty like the rest of the section.
 Crisis_State :: struct {
 	node_strain: [dynamic]Strain_Level, // parallel to Topology node slots (slot i = node slot i)
 	pipe_strain: [dynamic]Strain_Level, // parallel to Topology pipe slots (a pipe's bundle's pressure)
 	forecast:    [dynamic]Forecast_Entry, // era set-pieces in their forecast windows, set-piece order
+	active:      [dynamic]Active_Crisis, // 4.2 — the active crisis registry (one per activation, E13)
+	cooldowns:   [dynamic]Cooldown_Entry, // 4.2 — recently-resolved root causes (the re-fire gate, arch §6.4); engine memory, never serialized
 }
 
 // Sla_Accumulator — the per-class SLA counters (ODN-3 §5.2; 3.4). Fields of
@@ -239,20 +271,25 @@ Sla_Accumulator :: struct {
 // flow emits Packet_Arrived (1.3); win_lose_eval emits Run_Won/Run_Lost (1.4);
 // 3.3 adds Packet_Dropped (class + reason payload); 3.4 adds
 // Sla_Threshold_Crossed (class + metric + direction payload); 4.1 adds
-// Warning_Raised / Warning_Cleared (sign + target payload). The tag byte is
-// the serialized discriminator. `class`/`reason`/`metric`/`direction`/
-// `sign`/`target` are payload fields used ONLY by the tagged events — the
-// serializer writes them tag-conditionally so pre-3.3/3.4/4.1 event streams
-// stay byte-identical (golden stability).
+// Warning_Raised / Warning_Cleared (sign + target payload); 4.2 adds
+// Crisis_Triggered / Crisis_Resolved (archetype + cause + class + target +
+// pipe payload). The tag byte is the serialized discriminator. `class`/
+// `reason`/`metric`/`direction`/`sign`/`target`/`archetype`/`cause`/`pipe` are
+// payload fields used ONLY by the tagged events — the serializer writes them
+// tag-conditionally so pre-3.3/3.4/4.1/4.2 event streams stay byte-identical
+// (golden stability).
 Event :: struct {
 	tick:      u64,
 	tag:       u8, // 0 = (none); see the EVENT_TAG_* constants below
-	class:     u16, // Packet_Dropped / Sla_Threshold_Crossed payload: the class
+	class:     u16, // Packet_Dropped / Sla_Threshold_Crossed / crisis payload: the class
 	reason:    u8,  // Packet_Dropped payload: Drop_Reason
 	metric:    u8,  // Sla_Threshold_Crossed payload: Sla_Metric
 	direction: u8,  // Sla_Threshold_Crossed payload: Sla_Direction
 	sign:      u8,  // Warning_Raised / Warning_Cleared payload: Warning_Sign
-	target:    u32, // Warning_Raised / Warning_Cleared payload: node id / pipe id
+	target:    u32, // Warning_Raised / Warning_Cleared payload: node id / pipe id; crisis payload: the bundle slot
+	archetype: u8,  // Crisis_Triggered / Crisis_Resolved payload: crises.json archetype index
+	cause:     u8,  // Crisis_Triggered / Crisis_Resolved payload: Root_Cause_Kind
+	pipe:      u32, // Crisis_Triggered / Crisis_Resolved payload: the bottleneck pipe id (0 for Pool_Exhaustion)
 }
 
 // Event tags (stable across the wire; new variants append). The serialized
@@ -265,6 +302,8 @@ EVENT_TAG_PACKET_DROPPED :: u8(4) // 3.3: a packet dropped (class + Drop_Reason
 EVENT_TAG_SLA_THRESHOLD_CROSSED :: u8(5) // 3.4: a class crossed an SLA threshold (class + metric + direction payload)
 EVENT_TAG_WARNING_RAISED :: u8(6)  // 4.1: a node/pipe warning level rose (sign + target payload)
 EVENT_TAG_WARNING_CLEARED :: u8(7) // 4.1: a node/pipe warning level ended (sign + target payload)
+EVENT_TAG_CRISIS_TRIGGERED :: u8(8) // 4.2: a crisis activated (archetype + cause + class + bundle + pipe payload)
+EVENT_TAG_CRISIS_RESOLVED :: u8(9) // 4.2: a crisis ended (same payload shape — the ending crisis's refs)
 
 // Outcome — the latched terminal result (1.4 stub). None while the run is in
 // play; Won/Lost once win_lose_eval appends the terminal event. The terminal-
diff --git a/core/warnings.odin b/core/warnings.odin
index e0f75ec..564fc53 100644
--- a/core/warnings.odin
+++ b/core/warnings.odin
@@ -44,18 +44,23 @@ package core
 // from there (they are not re-stated here).
 
 // crisis_make / crisis_destroy — Run_State.crisis lifetime (mirrors
-// flow_init/flow_destroy; ODN-18 arena discipline lands later).
+// flow_init/flow_destroy; ODN-18 arena discipline lands later). 4.2: the
+// active-crisis registry (the dedup [E13] state) lives here too.
 crisis_make :: proc(c: ^Crisis_State, allocator := context.allocator) {
 	c^ = {}
 	c.node_strain = make([dynamic]Strain_Level, 0, 8, allocator)
 	c.pipe_strain = make([dynamic]Strain_Level, 0, 8, allocator)
 	c.forecast = make([dynamic]Forecast_Entry, 0, 2, allocator)
+	c.active = make([dynamic]Active_Crisis, 0, 1, allocator)
+	c.cooldowns = make([dynamic]Cooldown_Entry, 0, 1, allocator)
 }
 
 crisis_destroy :: proc(c: ^Crisis_State) {
 	delete(c.node_strain)
 	delete(c.pipe_strain)
 	delete(c.forecast)
+	delete(c.active)
+	delete(c.cooldowns)
 }
 
 // event_emit_warning — append a Warning_Raised / Warning_Cleared event with its


--- SPEC / CONTEXT ---
Read ALL of these files (they are your spec; the GitHub issue is "none" — the sprint story stands in for it):
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/spec/job-briefing.md  (the original job briefing)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/spec/story-4-2.md     (the sprint story 4.2 — the canonical acceptance criteria)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/spec/gdd-crisis.md    (GDD M5 — the crisis model + fairness rules)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/spec/architecture-excerpts.md (ODN-4, ODN-7, S6.4, S11.3 fairness, E10/E13)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/spec/lens-guards.md   (the reviewer lens-guards — read BEFORE anything; several are BLOCKER-class)


--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT: your ONLY deliverable is the file /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/edge-c1.json — write the JSON array to that exact absolute path (overwrite if it exists), then STOP. Do not write any other file. Your final message must be exactly: "DONE /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/edge-c1.json <N findings>" where N is the number of findings in the array (0 is fine).