# Problem-Solution — 2026-08-23 · Egress QoS

Skill: bmad-cis-problem-solving · Session: Packet Plumber queue-model migration
(per-(bundle,lane) link queues → router-egress-port scheduling)

## Step 1 — Problem Definition (DRAFT — awaiting user checkpoint)

**problem_title:** Congestion semantics live in the wrong place — buffers on
links instead of router egress ports

**problem_category:** Game architecture / sim-model correctness (design-integrity
migration under hard determinism contracts)

**initial_problem:**
User ruling (network engineer, via Gru): buffers/queues belong on ROUTERS, not
on links; links become dumb bit-pipes. Target model: each router holds output
queues per egress port (per link), per-class WFQ/WRR scheduling on the port,
drops at egress when arrival > link rate. Discuss and plan first — nothing
dispatched for code until the user says so.

**user answers (Step 1 gathering, 2026-08-23):**
- Q1 trigger: the congestion-cause blindness from this morning's flow-vis
  session; PLUS realism as a design value — "a game about running the
  internet should work close to how the internet actually works"
- Q3 success-feel: "making the QoS changes actually has impact" — the player
  must FEEL QoS configuration change outcomes
- Q4 scope: FIX PROPERLY, not patch — "modify whatever needs to be modded";
  balance/pace re-bless is licensed, byte-identical light-load is NOT a gate
- Q6 NOC: "NOC dash each" — read: the dashboard shows EACH router-port's
  queue depth (per-port relabel confirmed in spirit; exact phrasing to pin
  in solution steps)

**refined_problem_statement (draft v1):**
The sim's congestion model is physically inverted vs real networks. Today
(code-verified): queues are per-(bundle, lane) and DERIVED (membership =
on_edge + edge; lane = qos_lane_of(edge, class)); a full lane queue (E9 bound
6) sheds by drop precedence BE→Standard→Express at the LINK; QoS bandwidth is
allocated per PIPE (integer WFQ weights, untouched pipe = 100% Standard); the
E22 global pool (512) drops at admission. Real routers queue at EGRESS PORTS
and drop when arrival exceeds link rate. Consequences of the inversion:
(a) the game teaches the wrong mental model — differentiator #1 (QoS
trade-offs, FORGE #4) is anchored to pipes, not to the devices that actually
schedule; (b) congestion CAUSES are structurally hard to surface (the parked
flow-visibility session hit exactly this: "clear where there's congestion,
not clear why"); (c) the QoS panel, NOC readouts, and crisis anchors
(bundle_lane_at_bound at E9) all describe a model being retired. The problem
is a SEMANTIC migration under hard contracts: 20 Hz fixed tick, byte-identical
replay, LOG_VERSION=6, golden stability (queues are currently derived state),
and the MM pace feel (a lone packet gets full capacity — light-load transits
must not drift).

**problem_context:**
- code ground truth: core/flow.odin (queues, serve windows, E9/E22 drop
  ladders), core/qos.odin (WFQ allocator, E5/E6/E7/E8 rules), data/balance.json
  (lane_queue_packets=6, pool_max_packets=512, lane_presets,
  lane_auto_reserve_ladder [100]/[70,30]/[50,30,20]), app/qos_panel.odin
  (per-pipe panel, AUTO=derived), core/serialize.odin (LOG_VERSION 6)
- constraints to bound (per Gru directive): determinism/replay + LOG_VERSION;
  MM pace feel; QoS panel UX (per-pipe → per-port?); E22 pool fate; era
  tables; NOC relabels
- inherited spine: odin-architecture-v1 (ODN-3 QoS paradigm survives; its
  queue placement is the amendment surface); FORGE #4 intent (player-
  engineered QoS, never auto) binds
- sibling session (parked): flow-relationship visibility — the egress model
  may make congestion causes MORE legible (piles form at routers, not
  invisibly on links); interaction to verify, not assume
- open questions carried in: Q1 queue-state ownership (router × port × lane —
  derived or serialized), Q2 drop semantics at egress (tail-drop vs
  precedence), Q3 QoS UX surface, Q4 E22 fate, Q5 LOG_VERSION/determinism,
  Q6 NOC relabels, Q7 era interaction

**success_criteria (v2 — after user answers):**
1. Links carry rate + delay only; ALL buffering lives at router egress ports
   (per port × class), verifiable in code shape
2. Drop semantics at egress explicit, deliberate, and player-legible
3. QoS configuration changes have FEELABLE impact in a run (the headline
   player-facing outcome — user answer 3); FORGE #4 intent (trade-offs,
   player-engineered, never auto) preserved; config surface coherent with
   the new model (per-port or deliberate hybrid)
4. Determinism contract held: integer-only, replay byte-identical; any
   LOG_VERSION bump is deliberate and minimal
5. FIX PROPERLY license (user answer 4): pace/balance may be re-tuned and
   goldens re-blessed deliberately — but every re-bless is a reviewed event,
   and the MM pace feel is re-PROVEN after the migration, not assumed
6. No stale language: NOC shows each router-port's queues; QoS panel and
   crisis anchors describe the egress model when it ships

**advanced elicitation (2026-08-23 — methods 3 First Principles, 4 Steelmanning,
2 Map-Is-Not-The-Territory, run in sequence on Step 1 v2):**

KEY FINDINGS:
- (M3) ISOMORPHISM: today's on-edge queue is functionally the source router's
  egress queue — a queue on edge e fed by router u IS u's output buffer for
  port e, named after the link. The migration decomposes into 3 primitives:
  queue-ownership relocation (near-mechanical), port scheduler relocation
  (near-mechanical), and WIRE TRANSIT (genuinely new — the current queue IS
  the link's delay mechanism; remove it without a transit model and packets
  teleport). Q1 splits into Q1a queue ownership / Q1b wire-transit model.
- (M4) STEELMAN: per-pipe config is a deliberate UX choice (FORGE #4 wording),
  not an engineering accident — realism binds the SIM, not necessarily the UX;
  E9 push-out precedence is MORE expressive than tail-drop; derived queues are
  why goldens are stable. Steelman fails to refute realism-as-design-value and
  cannot fix congestion-cause blindness — but it REFRAMES the migration's
  value proposition.
- (M4) ANTICLIMAX RISK: because of the isomorphism, the felt player experience
  of the full migration could be ~zero — criterion 3 (feelable QoS impact)
  would have to be carried by the drop-semantics + visibility changes, not
  the queue move.
- (M2) DIVERGENCE BOUNDARY: match reality on buffer LOCATION / drop SITE /
  per-class scheduling; deliberately diverge on tick-quantized time, flat
  per-tier transit (not geometric), tiny buffers (difficulty knob), E22
  (engineering bound, decoupled from realism).

USER PIVOT RULING (2026-08-23, post-steelman): "we need this to be fun and
playable... we should LEAVE IT PER LINK." The egress migration as ruled at
session open is WITHDRAWN. Recorded consequences:
- FORGE #4 stands unamended; ODN-3 stands unamended — NO canon cascade needed
- the parked architecture workspace (architecture-egress-qos-2026-08-23/)
  becomes the record of a deliberated-and-rejected change — its memlog +
  this artifact's divergence boundary are the anti-re-litigation lock
- RESIDUAL PAINS NOT CURED by staying per-link: (i) congestion-cause
  blindness (the session's trigger — owned by the PARKED flow-vis session),
  (ii) QoS changes lacking feelable impact (success criterion 3)

## SESSION OUTCOME — CLOSED (Path A), 2026-08-23

User ruling: the in-flight BANDWIDTH CHANGE may alleviate the QoS-feelable-
impact gap — "I'll wait for that." Session closes as:
- NO MIGRATION: queues stay per-(bundle,lane) on links; the egress-port model
  is a deliberated-and-REJECTED change (the steelman + divergence boundary
  above are the record; do not re-litigate without new evidence)
- DELIBERATE DIVERGENCE adopted: the map-is-not-territory table is the canon
  answer to "why doesn't the game queue like real routers" — buffers on links
  are a fun/playability CHOICE, not an oversight
- RESIDUAL ROUTING: (i) congestion-cause legibility → the parked flow-vis
  session (problem-solution-2026-08-23.md) owns it fully; (ii) QoS-feel →
  DEFERRED, parked against the revisit trigger below
- REVISIT TRIGGER: after the bandwidth change lands and the user has played
  it — if QoS weight changes still don't FEEL impactful, re-open this
  problem re-framed at criterion 3 ("make QoS changes feelable", no queue
  migration); the Reframe sketch from this session is the starting point

STATUS: CLOSED at Step 1 by user ruling (discuss-first mandate satisfied —
nothing dispatched for code). All findings preserved for the trigger.
