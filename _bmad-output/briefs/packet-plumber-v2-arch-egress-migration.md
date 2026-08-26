# Briefing — packet-plumber-v2-arch-egress-migration (THE model migration)

Skill to execute: **bmad-quick-dev** (implementation; step-04 review layers
MANDATORY). The spine is LAW — read it FIRST and cite ADs in every story:

- `_bmad-output/planning-artifacts/architecture/architecture-egress-qos-2026-08-26/ARCHITECTURE-SPINE.md`
  (final, ratified 2026-08-26, 4/4 user rulings)
- Its `.memlog.md` (decision record D1–D8, rulings R1–R4, investigation
  findings — the direction-duplex divergence + existing-mechanics audit)

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Base: **v2 @ `79e8939`** (post-#102 fresh head). Silas creates the
  worktree on branch `packet-plumber-v2-arch-egress-migration`; work ONLY
  there. Main checkout is clean on v2 — never touch it.
- Read `/Users/moses/code/packet-plumber/project-context.md` first.
- Field notes: `_bmad-output/field-notes/packet-plumber-v2-4.2-surge-crisis.md`
  (crisis engine truth: admission-time shed bundles + resolve hysteresis
  MUST survive the re-key).

## The law you implement (AD summary — the spine binds, this is a map)

- **AD-1/D1** store-and-forward egress QoS: routers buffer+schedule per
  (egress-port, lane); links transmit only; endpoints pace. No unit may
  derive a "link queue" concept for ANY purpose.
- **D2** queue placement logical at the port; PHYSICAL ENCODING STAYS
  DERIVED (on_edge/edge/heading membership resolves port+lane; no new
  Packet fields, no queue structs serialized).
- **D3/R3** per-hop delay = 1-tick processing (join convention formalized)
  + egress queue residency + serialization ceil(demand × 800 / line_rate).
  NO propagation term. Integer-only, tick-quantized (ODN-2).
- **D4** WFQ/WRR + E7/E6/E5/E8 migrate VERBATIM re-keyed to port queues;
  weights stay per-pipe; port lane caps = summed member caps (exactly
  bundle_lane_caps today). E9 ladder → per-(port,lane) bound 6, drops at
  admission-to-port (the bound IS the arrival>rate drop). Crisis triggers
  read port queues, SAME measures + hysteresis; root_cause names
  (router, port).
- **D5/R1** FULL DUPLEX: each direction gets bundle_cap (fixes the
  shared-bidirectional-queue divergence). Same-direction estate contention
  survives.
- **D6** ALL queue state derived; LOG_VERSION STAYS 6 (prove: save
  round-trip + replay byte-identity on unchanged runs).
- **D7** reads contract: link paints UTILIZATION, router paints BUFFERING,
  NOC rail re-keys to (router, port). RENDER heists own the visuals —
  this job ships the READS (derived state + events), not the look.
- **D8** era/growth/ECMP: reads-only touchpoints, no behavior change.
- **D-2 NAMED STORY** (user-routed, never silent): bandwidth_demand is
  loaded-but-unwired — wire it into the D3 serialization formula.
  DISCLOSURE: streaming transit 8→16 ticks at standard rate; SLA math
  shifts; T1 re-bless where it contends.

## Story ladder (one commit per story, suite green between stories)

1. **S1 — port re-key (D2/D4, semantics-preserving):** logical queues at
   (router, egress-port, lane), derived encoding. T1 proof: unchanged runs
   replay identically (the re-key is invisible until S2).
2. **S2 — full duplex (D5/R1):** direction-split budgets. Balance
   disclosure in the commit + PR body (bidirectional-shared pairs gain 2×
   effective capacity). T1 re-bless ONLY where runs contend.
3. **S3 — D-2 demand wiring (the named story):** serialization formula
   honors bandwidth_demand. Streaming 8→16 ticks disclosure. T1 re-bless
   where SLA math shifts.
4. **S4 — drop/crisis re-key (D4/R4):** E9 per-(port,lane) bound-6,
   drop events target = port (ODN-14 shape unchanged), crisis triggers +
   root_cause naming. The 4.2 hysteresis survives VERBATIM (prove with the
   oscillation fixture from the field note).
5. **S5 — latency ledger + reads (D3/D7):** processing 1-tick
   formalization, per-hop attribution (queue-wait vs transit), the
   derived reads surface (port depths, utilization rings per
   (bundle,direction)) + NOC rail section re-key. Minimal mechanical
   render edits for compile/read correctness ONLY — pixel goldens change
   ONLY where S2/S3 shifted runs; zero [LOOK] redesign (that is the
   link-vocab heists' surface).

## Testing standard (non-negotiable, the house bar)

- **Mutation leg per story**: deleting/bypassing each story's mechanism
  MUST fail a test (S1: port derivation bypass; S2: direction split
  collapse; S3: demand unwired → streaming tick assertion; S4: bound
  re-scope; S5: attribution terms). RED-then-GREEN runs in the report.
- T1 golden discipline: re-bless ONLY deliberately, per-story, with the
  balance-shift disclosure; unchanged runs MUST replay byte-identical
  (D6 proof).
- Full suite green per story gate + at head: `odin test core` (incl.
  crisis + qos), `odin test app` , `odin test app/render`, palcheck.
- Remote CI may be billing-blocked (standing ruling: local suite is
  ground truth; disclose once).

## PR / ledger

- ONE PR to v2, title `arch(egress): store-and-forward queue migration
  (ratified spine 2026-08-26)`. Body: the story ladder, ALL balance
  disclosures, T1 re-bless inventory, the D6 save/replay proof.
- `ledger set packet-plumber-v2-arch-egress-migration in-review "<url>"`
  THEN `ledger pr ... <url>` (both steps).
- Perkins r1 arms via sensor at the stable local-green head.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider), `--thinking max`.
- Mega-minions: pin `zai-coding-cn/glm-5.3` explicitly (bare pi misroutes).

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: arch-egress-migration
- base: v2 (head 79e8939)
- branch: packet-plumber-v2-arch-egress-migration
- model: zai-coding-cn/glm-5.3
- pr_review: 1 (canon-surface sim migration — the full Perkins treatment)
