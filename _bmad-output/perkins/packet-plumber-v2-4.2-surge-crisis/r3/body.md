## 🤖 Perkins automated review — round 3 of 3
**Job:** packet-plumber-v2-4.2-surge-crisis · **Reviewed sha:** 121d8a0 · **Reviewers:** 7/7 completed
**Verification:** 54/75 lens findings confirmed against the code — 21 discarded as false-positive/chunking-artifact; merged into 17 findings (1 blocker, 3 warnings, 13 notes)

### Fix audit (r2 → r3) — the rework claims, checked

- **B1 — FIXED.** `test_crisis_slot_renumber_keeps_crisis_attached` exists and bites: crisis on pair P at slot 2, a full demand-free island bundle at slot 0 demolished mid-crisis, rebuild renumbers P 2→1 — asserts the crisis stays active, still names P, no spurious resolve/re-trigger, slot re-resolved, still saturated. The slot-keyed pre-B1 code fails it; removing the demolish fails it. surge.dem gains the 119500ms banner-GONE capture (verified no-banner).
- **W-qos — ROOT-FIXED, probe-verified.** The relieve lane threshold now carries the resolve margin (`bound > margin && queue+margin < bound && no lane ≥ bound-margin` + no same-tick shed). Probe of the qos scenario: a single clean trigger @1200 (bundle 0); the r2 @1201 resolve+re-trigger churn is gone; the re-blessed 65s banner names bundle 0. The change-log discloses the churn + fix accurately — but the new re-bless scope line is itself inaccurate (W-1 below).
- **W-pool — FIXED.** Trigger now keys on the E22 drop evidence with the eval-time depth as anti-flap; `test_crisis_pool_fires_on_routed_delivering_network` pins the routed under-fire regime. Hysteresis bands disjoint (no chatter).
- **W3-carry — PARTIAL** (W-3 below). **W-render — FIXED** (both banner titles ASCII; PNG decode shows clean hyphens in qos/warn/surge captures).
- **Notes:** B2-3 message fixed (prints the computed 38) · W5 branches pinned (wrong-typed row + absent-key positive) · pool routed fixture in · surge.dem bracket in (comment + re-fired-banner residuals noted) · N4 restructured as claimed — **but the restructure removed the post-trigger guard too: see B3** · N2/N7 recorded with reasons · frozen-text residues marked superseded.

### Blockers (1)

**B3 — same-tick double-trigger: one (archetype, set-piece) activation can emit two Crisis_Triggered events and hold two active rows (E13 dedup breach).** `core/crisis.odin:430-483`. The N4 restructure replaced the post-trigger `continue` with an `a_hit` flag: a successful (a)/(b) trigger no longer gates the (c) pool backstop, and `crisis_trigger` appends unconditionally (the `crisis_active_for` dedup check runs once, before any trigger). Probe-verified at pool cap 14 (email BE + streaming standard, narrow bottleneck, seed 3003): tick 1200 emits TWO Crisis_Triggered — Saturated_Bundle bundle 2 AND Pool_Exhaustion — with two active rows for set_piece 0 archetype 0, no resolve between. Reproduces at caps 11–14 (legal catalog values). Impossible at f906725 (post-trigger `continue`) — a regression. Fix: after a successful `crisis_trigger` in (a)/(b), `continue` to the next set-piece (a cooldown-*blocked* (a) still falls through to (c) — N4's intent survives).

### Warnings (3)

**W-1 — warn.t1 shifted 300 hashes (ticks 1201–1500) and is omitted from the re-bless scope; "everything else byte-identical" is false.** The shift is the same W-qos margin fix acting on warn.dem's crisis stream (its 65s banner moved bundle 3→1 in addition to the documented mojibake fix), but the scope line doesn't name warn.t1 and explicitly claims byte-identity elsewhere; it also lists "qos T1/log/PNGs" while qos.log.bin is unchanged in the delta. Amend the scope line to name warn.t1 with the margin-fix cause and drop the unchanged log.

**W-2 — pool cap 1 or 2 (legal catalog values) = a Pool_Exhaustion crisis that can never resolve** (resolve needs `len+2 < cap`; impossible at caps 1–2; the trigger still fires). The E9 path has the N5 margin clamp; the pool cap has none. Shipped balance.json is 512 (unreachable in shipped content) — catalog-authoring-only, so warning not blocker. Clamp the margin for the pool cap, or validate `pool_max_packets >= 3`.

**W-3 — STILL-PRESENT (narrowed): the types.odin Event comment now admits the +4B Packet_Dropped fold AND still ends with "pre-3.3/3.4/4.1/4.2 event streams stay byte-identical"** — self-contradictory three lines apart (serialize.odin says the opposite). Reword the trailing sentence.

### Notes (13)

N-1: HUD title em-dash through the byte-truncating draw_text (pre-existing; the PR touched the line) — `app/main.odin:519`. N-2: `crisis_trigger`'s `cat` parameter unused. N-3: two stale comments (stacked pre-W-qos RELIEVED block; serialize.odin's drop payload still "(class + reason, 3.3)"). N-4: pool banner title (~500px) spills the 440px card AND the pool banner branch has zero blessed pixel coverage. N-5: the pool trigger's ANY-class discriminator (non-surge-class shed) remains unpinned. N-6: no test isolates the (b) drop-fallback's drop-site attribution. N-7: `bundle_lane_at` / the margin lane-threshold has no direct unit pin (golden-only). N-8: the 65535 set-pieces fail-fast branch has no test row. N-9: app + harness crises.json load-error paths untested. N-10: surge.dem's Captures comment omits the new 119500ms line. N-11: the re-fired banner (2401–3000) stays T1-only. N-12: the ASCII render-string invariant has no automated enforcement (the mojibake class can regress silently). N-13: a cooldown-blocked pair A masks an unblocked pair B's fallback that tick (attribution latency, not a breach — for the record).

### Reviewer agreement

- **B3** — independently filed by acceptance, blind, codebase, and edge lenses (4/7 reviewers) and probe-verified by Perkins: highest-confidence finding of the round.
- **W-1** — filed by 6/7 lenses across chunks c1–c7 (17 raw findings merged) and confirmed against the delta by Perkins.
- **W-3** — filed by 5/7 lenses; confirmed verbatim against the file.
- The advisory gate: **CONCERNS** — the B1/W-qos/W-pool/W-render fixes hold, but the E13 dedup has a demonstrated same-tick breach that no test exercises.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
