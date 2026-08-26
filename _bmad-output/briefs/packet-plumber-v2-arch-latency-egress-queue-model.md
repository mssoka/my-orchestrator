# Briefing — packet-plumber-v2-arch-latency-egress-queue-model (bmad-architecture)

Skill to execute: **bmad-architecture** (create intent — the Architecture
Spine). NO production code in this job. Companion read: the gds- game
architect's lens is optional for the gameplay-feel steelman; the spine is
the deliverable.

## USER DIRECTION (2026-08-26, firing the recorded escalation path)

"and the latency issue for packets? we should [use] bmad skills to
architect this before deploying"

The link-vocab redesign (in flight, render-side) assumed SIM UNTOUCHED.
The user now escalates the sim question explicitly: architect the latency
+ queue model BEFORE the link redesign deploys.

## The question (in the user's own recorded words)

08-23 user ruling (network-engineer authority, from the memlog):
"buffers/queues belong on ROUTERS, not links; links become dumb bit-pipes;
per-egress-port output queues, per-class WFQ/WRR scheduling, drops at
egress when arrival > link rate" — AND the open question: **how packets
experience latency if links are dumb**.

## Current truth (verified 2026-08-26, v2 @0b2aeb9)

- Latency is SLA ACCOUNTING ONLY: `latency_tol_ms` (catalog.odin:103) vs
  measured avg delivery ms (flow.odin:230+); breach events on cross.
- The delay mechanism = per-(bundle,lane) LINK queues (queue_packet,
  on_edge/edge membership; qos.odin:111 lane derivation) + travel ticks.
- No link propagation, no serialization-at-rate, no router egress state.
- ODN-3 (3 DiffServ lanes, integer WFQ weights, WRR floor) — inherited,
  its queue PLACEMENT is what this architecture amends or re-affirms.

## History you MUST build on (do not re-litigate from zero)

- READ FIRST: `_bmad-output/planning-artifacts/architecture/
  architecture-egress-qos-2026-08-23/.memlog.md` — the full decision
  record: the spine was scaffolded (the .md template is UNFILLED), the
  migration WITHDRAWN post-steelman on fun/playability, divergence
  recorded DELIBERATE, revisit trigger: "re-open re-framed at 'make QoS
  changes feelable' (no queue migration)". The steelman doc itself was
  swept — the memlog carries its essence.
- The 08-26 render pivot (single-color links + router queue reads) is the
  LOOK half, in flight separately; this architecture owns the MODEL half.
  The two must converge: the router queue-read surface is designed against
  whatever state model this spine ratifies.

## Task: author the Architecture Spine (the real one this time)

1. **Fill the spine** at
  `_bmad-output/planning-artifacts/architecture/architecture-egress-qos-2026-08-26/ARCHITECTURE-SPINE.md`
   (new dated dir; the 08-23 dir stays as history). Follow the bmad
   architecture skill's kernel method — decisions, not rationale
   (rationale → the new memlog).
2. **The decision set to author** (each an AD with Binds/Prevents/Rule):
   - Queue placement: router-egress-port vs per-(bundle,lane) links vs
     hybrid (e.g. links keep transit ticks only).
   - The LATENCY MODEL — the user's headline question: decompose packet
     delay into (a) egress queue residency at the router, (b) serialization
     at link rate (packet-size/rate in integer ticks), (c) optional
     propagation ticks (link length/distance feel), (d) processing hop.
     Integer-only, tick-quantized, deterministic — ODN-2 constraint.
   - Scheduling: per-class WFQ/WRR at the port (ODN-3 weights migrate or
     stay), drops-at-egress semantics (arrival > rate), interaction with
     the E9 admission ladder + E22 crisis triggers (the 4.2 field-note
     hysteresis must survive).
   - Serialization boundary: queue state derived vs serialized
     (LOG_VERSION bump if any — currently derived membership), save compat.
   - NOC/rail + HUD reads (memlog Q6), era interaction (Q7), spawn/growth
     (7.x) touchpoints.
   - The FEELABLE constraint: the 08-23 withdrawal was fun/playability —
     the spine must steelman how the new model makes QoS changes FEELABLE
     (weight nudges visible in queue depth + latency readouts) WITHOUT
     breaking calm-at-green. This is the ratification bar, not a footnote.
3. **Conflict + inheritance discipline:** ODN-3 amendment = surface + tag
   [ADOPTED] only after the user ratifies; inherited invariants read-only.
4. **Deliverable gate: LAVISH** (docs review BEFORE anything merges): one
   page — the latency decomposition diagram (where delay lives now vs
   proposed), the decision table with the open ruling rows marked, the
   feelability steelman, migration cost estimate (LOG_VERSION, goldens,
   T1/T2 churn). The user rules in the browser; the spine finalizes after.
5. Preserve all drafts under the dated dir. No PR until the lavish verdict.

## Sequencing (durable on rows — Silas wires)

- link-vocab IMPLEMENTATION heists: blocked_by THIS architecture's
  ratification (the router queue-read builds on the ratified model).
- link-vocab DESIGN exploration (in flight): continues — its lavish gate
  and this spine's gate can merge into ONE user session if both are ready.
- crisis-duck + node-legibility: unaffected (orthogonal surfaces).

## Ledger / reporting

- Row: `packet-plumber-v2-arch-latency-egress-queue-model`. No PR pre-gate.
  Completion: `ledger note` + `herdr notification show
  "packet-plumber-v2-arch-latency-egress-queue-model" --body "<lavish url>"`
  (verify shown:true).

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider), `--thinking max`
  — this is reasoning-tier work on the ops model pin (k3 403, flash 402;
  interim per the 08-19 precedent).
- Mega-minions: pin explicitly, same probe discipline.

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: arch-latency-egress-queue-model
- base: v2 (head 0b2aeb9 — docs + read-only analysis; no branch)
- branch: NONE (architecture docs commit via a docs PR AFTER the lavish
  verdict, per the DOCS review loop)
- model: zai-coding-cn/glm-5.3
- pr_review: 0 (docs; the post-ratification spine PR is a fast-follow)
