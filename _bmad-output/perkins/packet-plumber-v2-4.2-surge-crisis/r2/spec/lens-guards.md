## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology.** The engine is downstream of flow and never writes topology (no topology mutation from crisis code — grep the crisis modules for topology writes). A topology write from the crisis path = a blocker.
- **🚨 ODN-7 / REVIEW M1 — Director never reads crisis state** (structural — grep the director for crisis references). A director→crisis read = a blocker.
- **🚨 E13 DEDUP — one crisis per root cause per activation.** Re-trigger only after `Crisis_Resolved`; a duplicate `Crisis_Triggered` for the same root cause without a resolve = a blocker.
- **🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology**; and **no crisis without a resolvable root cause + `preventive_redesign`** (every crisis carries the ref to the topology flaw + what the player could have built). A crisis firing on a healthy topology, or a missing root-cause ref = a blocker.
- **E10 DETERMINISM — same seed → same crisis timeline.** The surge fires on schedule from the seed; selection lives inside the deterministic RNG stream (no new draw, no map-iter in the hot path). A nondeterministic schedule (wall-clock, sim-rng outside the stream) = a blocker.
- **4.1 WIRING — the telegraph becomes true.** The forecast panel names the surge with a countdown; the engine fires it on cue. Verify the wiring actually exists (panel data → engine trigger); "panel exists but the engine never reads it" = a real defect.
- **GOLDEN DISCIPLINE.** New T1 + event-stream golden (`Crisis_Triggered{Surge}` in the scheduled window) blessed deliberately with proof; **existing goldens must NOT shift** — if one shifted, that is a REAL finding (re-bless-without-proof is the trap), not a routine update.
- **SCOPE GUARD.** Surge archetype + engine + root-cause ONLY. NOT 4.3 (Network Health meter / win-lose-retry), NOT the other four crisis archetypes (post-fun-gate), NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it). Out-of-scope content = a finding; do NOT demand features 4.3 would add.
- **BASE = `v2`** (slices 1–3 + harness + 4.1 in). Do NOT re-open settled prior-story findings (3.x / 4.1 / harness — carry-forward only). `correction`-era RT stories don't apply here.
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical — regression-flag any determinism break, but do not re-litigate the settled routing/ECMP/demolish design.

## Standing orders (from the playbook — verbatim)
