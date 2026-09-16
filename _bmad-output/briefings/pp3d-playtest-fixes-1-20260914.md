# Briefing: pp3d-playtest-fixes-1 — b40 playtest response (camera, spawn feel, HUD, connect)

## Context

User playtested the merged PR #42 build (b40, merge 4102a82) and ruled four
workstreams after a design consult with Gru (2026-09-14 evening). This is a
PLAN-FIRST dispatch: every fork below is user-ruled. Implement as specified;
do not re-open settled design forks. Where a spec says "user tests it", the
verdict lands at the user play session on the b41 export — build it exactly
as ruled, no improvisation on feel.

Platform context (user-ruled, AMENDED 2026-09-14: record in docs/ as part of
the PR): the game caters to THREE platforms EQUALLY — **PC (mouse/keyboard,
close screen), mobile (touch, small screen), and TV/console (controller,
large screen)**. No platform is first-class; design for parity. Concretely:
mouse hover states exist for PC; touch hit-targets are mobile-sized
(48dp-class, generous); every verb is controller-navigable; HUD insets are
device-adaptive (TV action-safe inset on large-screen presentations,
tighter on PC/mobile); text scales per device class, one ladder.

## Evidence (read-only grounding; do not copy into the tree)

- `/Users/moses/code/_local-refs/pp3d-playtest-b40-2026-09-14/` — the user's
  screen recording, 10 extracted frames, 4 annotated screenshots, README with
  the user's verbatim feedback. The 20.50.39 screenshot is the SRI/UTAH case:
  at max zoom-out SRI is clipped top-right, UTAH clipped bottom-left — both
  never fully visible at once.
- `/Users/moses/code/_local-refs/mm/` — Mini Motorways press kit + screenshots
  (the look family for spawn feel). IP GUARDRAIL: cite/diff locally ONLY,
  never copy assets into any repo tree.

## Workstreams (all specs user-ruled 2026-09-14)

### WS1 — Camera auto-pan to new spawns (Google-Earth feel)

Current: spawn awareness never moves the camera; the player must click
"New buildings" (scripts/ui/spawn_awareness.gd `reveal`/`_visit_next`).
Flight machinery exists: `focus_point` / `offset_focus` / `cancel_focus` in
scripts/input/orbit_camera.gd with exponential damping (EASE_RATE=10).

Ruled spec:
- **Auto-fly to newly spawned buildings** with ALL gates stacked:
  - **idle-gated**: fly only when the player has made no input/gesture for
    ~2–3s (never steal the camera mid-task, never during a connect gesture);
  - **visibility-gated**: fly only if the spawn is offscreen or near the
    planet limb (already clearly in view = no flight);
  - **batched**: at most one flight per spawn batch (grouped arrivals =
    one swoop to the group).
- **First L1 spawn flies unconditionally** — the teaching beat.
- **Google-Earth easing**: fast at the start of the travel, smoothly
  decelerating into the location — a duration-based strong ease-out
  (quintic-class) on the travel path, distance-adaptive duration. NOT the
  current constant-rate exponential damper profile; introduce a proper
  fly-to tween (slerp/azimuth path) with that velocity profile.
- **Any player input cancels instantly** — ride the existing cancel-on-gesture
  path (`cancel_focus`/`focus_cancelled`); a cancelled flight must leave the
  camera exactly where the gesture began (existing semantics).
- The dwell/inspectable acknowledgement system (PR #42) stays intact — a
  flight that completes still owes the honest-inspection dwell gates.

### WS2 — Spawn feel: sonar ring OUT, pop/bounce + placement cue IN

Current: expanding double-line sonar ripple (scripts/ui/spawn_awareness.gd
`_draw` + `ripple_segments`, RIPPLE_SECONDS 2.2, radius 0.055→0.13 fading).

Ruled spec:
- **Remove the sonar ripple entirely.**
- **Building pops in with a scale-bounce** (overshoot-and-settle tween;
  node_site.gd already has pulse-tween machinery to build on).
- **Subtle ground shadow / dust puff at placement** — a placement feel, not a
  radar feel. MM family: quick, soft, gone. Reference the press-kit frames
  locally for the energy level; do not copy assets.

### WS3 — Text/HUD declutter (TV-first)

Ruled zone map (LOCKED — do not move zones; the corner layout is
platform-neutral, works identically for mouse/touch/controller):
- **Top-left**: "New buildings" visit button — KEEP as is.
- **Top-center**: history guide narration (the internet-history explainer) —
  KEEP; user likes it.
- **Top-right**: **scores/stats cluster** — NEW home: compact persistent chip
  (packets delivered · links up · network health). Arcade convention per user.
- **Bottom-center**: **dock** (Routers | Links) — MOVED down from top; remove
  the persistent objective text below it ("install the new IMPs, then link
  every IMP — one net" disappears as persistent UI).
- **Bottom-right**: **toast notifications** — NEW system, macOS-style cards,
  auto-dismiss (short TTL), stack capped (~3), device-adaptive inset (TV
  action-safe on large screens, tighter on PC/mobile), clear gap from the
  dock. ALL transient info rides toasts: arrivals, objective beats
  (the removed dock text becomes a toast at level start), SLA breach alerts
  (shout once, dismiss). No persistent breach chip.
- **Bottom-left**: RESERVED (future pause/menu) — leave empty.
- **Arrow/directional marker panels are REMOVED** ("← Utah / behind planet")
  — user called them noise. Discovery pointing is the camera flight (WS1)
  + the "New buildings" button, nothing else.
- The planet-side building labels (Label3D, node_site.gd) keep the game-wide
  type ladder; NOTE ui_text.gd's ladder is FROZEN by test_ui_theme — any size
  change is a deliberate re-pin in lockstep with the test, never a silent edit.

### WS4 — Connect: sticky tap-tap + label de-occlusion

Current: drag-to-connect only (scripts/input/connect_controller.gd:
draw_begin/draw_move/draw_end; generous 14°-arc snap). The SRI↔UTAH playtest
case proves both endpoints must be simultaneously visible — unconnectable at
max zoom-out.

Ruled spec (user: "we can test that"):
- **Sticky tap-tap connect**: tap source building → it stays "picked up"
  (clear highlight/glow state) → camera free to rotate/zoom → tap target
  → connect commits. Reuse the existing snap generosity and the
  pair-declined law UX (warm-amber preview + gentle steer hint) — the law's
  teaching moments must work identically in tap-tap mode.
- **Drag stays as an alias** for mouse players (current flow unchanged).
- **Offscreen picked-source indicator**: while a pick is active and the
  picked building is offscreen/behind the limb, a subtle edge indicator
  points to it (this is NOT the removed arrow-marker system — it exists only
  during an active pick).
- **Labels de-occlude** (user: "let's see it in action"): planet labels DIM
  during any connect gesture/pick (drag or tap-tap), and shrink or hide at
  extreme grazing/limb angles where they smear across the planet edge.
- Tap-tap must be controller-native at the input layer: the verb is
  select-then-select, no held drag required.

## Acceptance

1. PR vs origin/main (base `main`, pr_review=1 — gameplay-surface code).
2. PP3D suite green with the harness discipline: EXPECTED_CHECKS triple
   (per-file expected run-count pins + completion flag + final-line guard),
   and every new gate carries a fails-pre-fix discriminator (mutation leg):
   - auto-pan gate FAILS when a flight triggers during an active gesture
     (idle gate must be provable);
   - visibility gate FAILS when a flight targets an already-centered spawn;
   - toast gate FAILS when a toast persists past TTL or exceeds stack cap;
   - picked-source indicator gate FAILS when source offscreen and no
     indicator rendered;
   - sonar-ripple gate FAILS if any ripple geometry draws (regression pin).
3. Captures (windowed entries, ~900s, caffeinate -dimsu wrapper, the
   don't-close-pop-up note; receipt+hash per entry, quiescence check,
   stop-on-surprise): camera flight showing the ease-out profile; spawn
   pop/puff; HUD zone map (all six zones as ruled); tap-tap connect of the
   playtest SRI↔UTAH pair (both endpoints NOT simultaneously visible);
   label dim during pick; limb-angle label shrink/hide.
4. Playable export b41 (same Start.command self-contained pattern as b40),
   preserved centrally under _bmad-output/implementation-artifacts/ with the
   PR. The user play session on b41 is the final verdict for WS1 feel,
   WS2 look, WS4 tap-tap and label behavior.
5. No merge. Preserve user look resources. No changes outside these four
   workstreams (no art-direction drift, no balance changes).

## Skills policy

- Workflow: `bmad-quick-dev`.
- Review layers (bmad-build step 04): `bmad-review` (adversarial lens) +
  `bmad-review-edge-case-hunter`.

## Model policy

Hold regime (2026-09-14 second OpenAI hold): minion runs
`zai-coding-cn/glm-5.3` @ max. glm-5.3 is natively multimodal — the minion
may attach the playtest screenshots/frames for grounding. Aesthetic
ratification = the user play session on b41 (E1 precedent: a user-play gate
IS the look verdict). Narrow real-image HUD/focus verification stays
Astra@xhigh when tokens return — parked, note-only.

## Bounded-run grant (user-ruled standing terms)

Godot/native execution ONLY under these terms: headless-only for tests;
entry-count budget named in your run plan (standard entries ≤300s; capture
entries ~900s windowed, caffeinate -dimsu, screen awake); receipt+hash per
entry; quiescence check; NAMED stop conditions — any failure/drift/diagnostic
STOPS the sequence and reports; stop-on-surprise outranks completing the
checklist; extensions are NEW disclosed grants, never a quiet extra entry;
exhaustion = STOP and report.

## Dispatch parameters

- repo: packet-plumber-3d
- repo_root: /Users/moses/code/packet-plumber-3d
- slug: pp3d-playtest-fixes-1
- base: origin/main @ 4102a82 (post PR #42 merge)
- model: zai-coding-cn/glm-5.3 @ max
- pr_review: 1
- PR base branch: main
