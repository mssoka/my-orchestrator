# Problem-Solution — 2026-08-23

Skill: bmad-cis-problem-solving · Session: Packet Plumber flow-relationship visibility

## Step 1 — Problem Definition (DRAFT — awaiting user checkpoint)

**problem_title:** Players cannot see traffic relationships — where packets come from and where they're going

**problem_category:** Game UX / information visualization

**initial_problem:**
User misread existing glow tokens (spawn band, router cores) as source/destination
flow. Follow-up: "if we have source/destination it doesn't have to be pairs, could
be a broadcast — how do we make that work?" Mental model held: flows fan out.

**refined_problem_statement:**
The game communicates congestion (amber/red, BREACHED, crisis anchors) but never
communicates flow relationships — which nodes talk to which. Players model "my
network feeds these places" and the board confirms nothing. Existing glow tokens
are silent about meaning — ambiguous enough to be misread as flow. The problem is
not "add a flow glow"; it is "the board lacks a legible layer for flow
relationships, and its current glow vocabulary is ambiguous."

**problem_context:**
- Sim tracks src/dst/edge/class per packet (data is free, read-only derivation)
- Existing tokens: spawn reveal band (green), router tier cores, crisis anchor,
  amber/red utilization, packet trails (#82)
- User constraint: anti-noise (1-in-6 density ruling) — new layers must earn pixels
- NOC dashboard diagnoses drops; it is a panel, not a board language

**reference_precedent (Mini Motorways, user-raised 08-23):**
MM solved flow visibility with three layers: (1) STRUCTURAL COLOR PAINT — house
and workplace share color codes, so the relationship is permanently painted into
fiction: same-color IS the contract (a pure broadcast model — any red car to any
red office, dynamic assignment); (2) THE TRAFFIC IS THE FLOW — colored cars
reveal relationships live as animation, no overlay; (3) ON-DEMAND SELECTION —
click a building for its connections/demand, nothing permanently on screen.
Color works there because assignment is trivial (one dest class per color,
~4-6 colors, one design lever: road topology).
APPLICABILITY VERDICT (grounded in PP catalogs): half-applies. PP already
implemented the class layer at packet level (packet_types.json: shape PRIMARY,
"never colour alone" [UX-DR4]; demand.json selection = weighted_random
source_role → sink_role — PP's sim IS the MM broadcast model). But class is the
WRONG GRANULARITY for PP's pressure question: MM has one dest type per color;
PP has MANY terminals per role (content_host/campus), dst picked weighted-random
per packet → the fan is per-NODE, a subpopulation question INSIDE a class that
color/shape cannot answer (this is why the glow misread happened).
WHAT TRANSFERS: (a) the on-demand reveal pattern (select → fan; zero permanent
pixel tax = success criterion 2 verbatim); (b) broadcast mental model — matches
actual sim selection, so the visualization would be honest, not a construct.
WHAT DOESN'T: permanent color paint as the relationship layer (class layer
already exists; adding color would fight anti-noise and still not answer
"which node").

**refined_problem_statement v2 (post live-play evidence):**
The game communicates congestion but never flow relationships. Its ONE
relationship signal — the R3 route glow — is draw-gated, single-packet, and
6-second transient, so players over-generalize it into "the flow" and
misjudge the real fan (weighted-random broadcast). Even the debug NOC shows
WHAT/HOW-MUCH per pipe, never WHO/WHERE. Consequence: the player can see
THAT an edge is congested but never WHY — and cannot even tell a designed
uniform spread from a selection bug. The problem: no on-demand, fan-level,
src↔dst legibility layer; the draw-gated glow vocabulary over-promises and
under-delivers.

**success_criteria (draft):**
1. "Who does this node feed?" answerable in one glance, no menu
2. Graceful on busy boards (no permanent visual tax)
3. Distinct from congestion + spawn signals (ends glow ambiguity)
4. Supports planning, not just diagnosis

**live_play_evidence (2026-08-23 — screenshot + user report, code-verified):**
User played live and reported (verbatim): "It's clear where there's congestion,
but it's not clear why." Screenshot (Desktop 11:06:54): paused mid-run,
Streaming BREACHED, health 76%, SLA gauges: Streaming del 211 / drop 210 (49%)
/ queue 197 / severed 13 / avg 1649ms vs 1200ms tol; predictive saturation
glyphs (✕×5, ✕×9) on two edges; a thick GREEN BAND tracing a multi-hop path
from a left-side terminal through 3-4 green-tinted routers to a ringed
terminal at bottom-right.

GLOW MECHANISM RESOLVED (code-verified, app/render/assist.odin — Job-B assist
package, canon 2026-08-13): the green band is NOT the spawn reveal. It is the
R3 POST-DRAW ROUTE GLOW: when a pipe draw commits, the game finds the FIRST
live packet whose equal-cost DAG contains the new edge and glows that packet's
FULL winning DAG (ECMP splits both glow) for glow_ticks=120 = 6 s @ 20 Hz.
IT IS LITERALLY A SOURCE→DESTINATION PATH HIGHLIGHT — the user's "misread"
was a CORRECT read of the token's content. The actual failure: it is
draw-gated (only appears when you draw), single-packet (one packet's DAG, not
the fan), and transient (6 s) — yet it is the ONLY flow-relationship signal on
the board, so players over-generalize it into aggregate flow ("all traffic
goes to that home").

FULL SIGNAL INVENTORY (what exists vs what it answers):
1. R2a drag preview (assist) — one packet's would-be DAG, draw-gated
2. R3 post-draw glow (assist) — same DAG, 6 s after commit
3. Packet trails (#82) — where packets pass, not relationships at a glance
4. Congestion signals — amber/red utilization, predictive ✕ glyphs, BREACHED
5. NOC D-panel (PP_DEBUG, app/render/noc_overlay.odin, ruling 08-22) —
   per-class SLA table, per-pipe readout (offered/cap/util/carried/dropped/
   lane queues + drops by class+reason), crisis root causes, drop log.
   CODE-VERIFIED GAP: the per-pipe readout has NO src/dst composition — it
   answers WHAT flows and HOW MUCH, never WHO/WHERE-FROM/WHERE-TO. Even the
   debug dashboard cannot answer "why is this pipe hot — who feeds it?"

THE FORK (demand.json, era 3): streaming source_role=content_host,
sink_role=residential, selection=weighted_random, every home demand_weight=1
— the sim is DESIGNED to spread uniformly across all homes. User's observed
concentration ("almost all traffic seems to go to the first home") is
therefore either (a) VISUAL ILLUSION (glow fixation + queue pile-up reading
as concentration), or (b) a GENUINE dst-selection anomaly (a sim bug).
Decisive: WITH CURRENT BOARD LANGUAGE THE PLAYER CANNOT TELL WHICH — the
visibility gap doesn't just block planning, it blocks distinguishing
"working as designed" from "the game has a bug."

**Open pressure question:** information vs control — does seeing the fan change
what the player DOES, or only what they know?

STATUS: Step 1 near-final (v2) — user PAUSED to gather live evidence with
the NOC interface; field observation list issued (4 questions targeting the
illusion-vs-anomaly fork + information-vs-control). Checkpoint [a]/[c]/[p]/[y]
re-presents on return.
