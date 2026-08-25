### Slice 7 — Juice + accessibility (MVP done)

**Goal.** *Just-enough juice* to prove the **concept** (not just the loop), core
accessibility, and input parity. **The MVP (E1–E9) is complete; the fun-test can run in
full.**

**Stories:** 7.1 visual juice (light-canvas polish, packet feel) · 7.2 audio juice (1–2 Suno
stings, cosmetic rng) · 7.3 accessibility core (colorblind-safe, reduced-motion, captions).

**Playable increment:** *the MVP is complete — a juiced graybox that feels and sounds like
saving the internet, accessible, playable on mouse/touch/controller.*

**Exit criteria:** View reads only snapshots `[ODN-1]`; packet type/node state never
color-alone (icon + shape + outline) `[GDD § Accessibility]`; reduced-motion disables
flagged effects + crises stay readable; all audio alerts captioned; SFX variant pick draws
from the app-owned cosmetic rng only `[ODN-15]`. **→ On S7 exit, run the playtest (both
audiences). Pass → greenlight slice 8+ + content; fail → iterate via the data catalogs
`[ODN-5]`.**

### Slice 8+ — The six GDD mechanics (post-fun-gate)

**Goal.** The six mechanics the user ratified (decision-log 2026-08-10), each integrated at
its **natural home** in GDD voice/format, bundle-consistent, no tenet contradiction.
Sketched at slice-level here; full story cards land post-fun-gate (the playtest may reorder
them).

- **Congestion-heatmap persistence** → Player Assistance (primary) + UI filter/focus (toggleable
  demand-vs-capacity heatmap overlay over persistent breach-marks).
- **Bespoke per-era crisis thresholds** → M5 (a "demand director") + difficulty rhythm
  invariant.
- **Error-404 specific-counter post-mortem** → Win/Loss (loss screen) + Player Assistance
  cross-ref.
- **Emergent clutch from constraints** → Core loop (reward/cascade) + crisis juice (clutch
  resolution swell) — a tuned sim property, not a scripted event.
- **Costly always-available fallback** → Win/Loss "no soft-locks" — the escape is an
  emergency **load-shed**, cost = **drops** (shed traffic → SLA breach → uptime/score
  drain), NOT cable-wear. Invariant: "always available, never free."
- **Interconnected upgrades** → M4 (compound modernization ladder) + Player Progression.

All six are written in the **locked** per-hop/ECMP/bundles vocabulary `[RR]`. `[FULL]`
scope per the decision-log (5 of 6 carry an explicit `[FULL]` note; the post-mortem's
specific-counter layer is `[FULL]` over the MVP's plain retry).

### Slice N — Full-game content (E10) + production polish (E11)

**Goal.** The campaign beyond the fun gate. `[epics.md E10/E11]`

- **E10 (content + impl swaps):** remaining packet types (gaming/banking/voice/multicast/
  IoT/AI — catalog data); eras 4–6 (real-time triage; cloud scale + CDN reservoirs; Era-6
  overlay mechanics — VPN/SDN/AI as data + small procs, **no new core system** `[arch
  §13.2]`); economy (score core + Could-tier SLA contracts/currency; no-pay-to-win); V2 AI
  stress-test (`AiAuditorDirector` behind the existing seam `[ODN-7]`); replayability
  (daily/weekly seeded runs + leaderboards — the **portable-core re-sim validation** story
  `[ODN-6]`).
- **E11 (production polish):** the forge's "prototype is reference, not codebase" doctrine
  `[FORGE #7]` is **partially absorbed by v2** — v2 *is* the from-scratch build (prototype →
  reference-only). So E11 becomes "production-quality polish + content scale on the v2
  spine" rather than "discard prototype + rebuild fresh." **Test contract:** the production
  build reproduces the proven fun before content scaling. (Honest scope change vs the
  GDD/epics — surfaced, not silently dropped.)

---

## 4. Traceability — story → architecture system → edge-case contract
## 7. Decisions & rationale (load-bearing calls — for the PR)
