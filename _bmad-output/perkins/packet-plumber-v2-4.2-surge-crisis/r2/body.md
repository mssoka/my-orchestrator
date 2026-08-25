## 🤖 Perkins automated review — round 2 of 3

**Job:** packet-plumber-v2-4.2-surge-crisis · **Reviewed sha:** f906725 · **Reviewers:** 7/7 completed
**Verification:** 32/56 findings confirmed against the code — 24 discarded as false-positive
**Evidence run at this sha:** `odin test core` 117/117 green · `tools/harness.sh run` 15/15 demos green · `drift-check` 104/104 rejected · two scratch probes reproduced the blessed event timelines

### Fix audit (r1 → f906725)

**B2 ✓** — settled-scan positive test bites (names bundle 0 drop-free while the first shed lands on bundle 1); backward-tick latch pinned; equal-tick behavior exercised by the pre-existing `step_once` convention. **W1 ✓** class filter dropped. **W2 ✓** surge.dem now demolishes @2381 → identity-resolve, wides @2401 → re-trigger, relief @3000 (probe-verified against the blessed T1; 170s capture = banner-gone). **W4 ✓** slot-order settled scan restored to pass 1 + pinned; qos.t1 re-bless cause-documented (incompletely — see W-qos). **W5 ✓** `json.String` assert → named load error. **W6 ✓** per-tick `flow.drop_sites` scratch; the ODN-14 buffer is no longer an engine input. **W7 ✓** replay leak fixed (no crisis_test leaks under the tracking allocator). **N1 ✓** carried with a reason that verifies. **N3/N5/N6/N8/N9/N10 ✓** fixed. **N11/N12 ✓** explicitly carried. **W3/N13 partial** (see W3-carry / N-frozen).

### Blockers (1)

**B1 — the renumber-proof identity mechanism is real, but the mandated demolish-and-renumber test still does not exist.** The canonical `(bundle_lo, bundle_hi)` pair + per-tick `bundles_slot_for_pair` re-resolution + `!ok`-resolve are correct by inspection, and the pair-gone branch is exercised (surge.dem @2381). But every resolve fixture preserves slot order at every transition (demolish the crisis's OWN bundle, then redraw pairs in the same first-seen order), so the r1 stale-slot failure mode — spurious `Crisis_Resolved` + same-tick re-trigger + mislabeled banner when a PRECEDING full bundle is demolished mid-crisis — is not pinned. The round-2 mandate closes B1 only on "a test that bites"; the pin is absent. Add a resolve test: crisis active on pair P at slot 1, demolish a full bundle at slot 0, rebuild renumbers P to slot 0, assert the crisis stays active and still names P with no spurious resolve/re-trigger.

### Warnings (4)

**W-qos — qos re-bless cause-documentation is incomplete; "T1/log/T2 re-blessed" is false for log/T2.** Probe-verified: the blessed qos stream is trigger bundle-0 @1200 → same-tick `Crisis_Resolved` b0 + `Crisis_Triggered` b1 @1201 (no topology edit). The documented cause ("element changed bundle 1→0") explains only the @1200 trigger; the @1201 resolve+re-trigger churn — which contradicts the golden-discipline claim "a persistent flaw emits ONE trigger per activation" — is undisclosed. The 65s T2 is pixel-identical because the element converges back to b1 before the capture; only `qos.t1` actually moved (the log and both PNGs are byte-identical to r1). (Lens claims that the T2 "needed" re-blessing are refuted — the harness is green and the PNG decodes to "bundle 1 (pipe 1)".) Amend the change-log with the churn + correct the re-bless scope, or add a trigger confirmation delay (frozen-letter renegotiation).

**W-pool — the Pool_Exhaustion trigger's eval-time pool check under-fires when deliveries drain the pool after the spawn-shed.** The E22 shed is admission-time evidence the pool WAS at cap; the check `len(state.flow.packets) >= pool_max` runs after the flow's phase-5 cull, so in any network that still delivers, the pool sheds every other tick and the map-wide crisis is never named. The pinned test passes only because its fixture has no pipes (zero deliveries). Same evidence class the W4 fix corrected for E9: trigger on the drop evidence, use the eval-time check as the anti-flap guard, and add a routed-network pool fixture.

**W3-carry — types.odin:293 and the frozen Events bullet still assert "pre-4.2 streams byte-identical"** while serialize.odin (amended) and the change-log admit the +4B drop-payload fold. The same PR contradicts itself; the types.odin comment needs the amended wording, and the frozen bullet should be marked superseded (it needs human renegotiation to change).

**W-render — the crisis banner renders a mojibake glyph.** Both title strings use a non-ASCII em-dash, and `draw_text_c` truncates every rune to a byte (`u8(ch)`) — the file's own header warns exactly against this. Every blessed T2 capture (including this round's re-blessed surge 170s) pins the corrupted character in the flagship banner. Replace the em-dash with ASCII in both format strings.

### Notes (7)

- **B2-3 pin depth:** the drop-payload + tags 8/9 payloads are size-pinned only (the crises section asserts individual bytes); the failure message says "want 30" while the expression evaluates to 38.
- **W5 branches untested:** the absent-key (−1) and wrong-typed (named error) `archetype_id` paths have no catalog test rows.
- **Pool marginal regime untested:** the W1 ANY-class discriminator and the routed-network case (see W-pool) are unpinned.
- **surge.dem 2381/2401 cycle is T1-pinned only:** no T2 capture brackets the resolve/re-fire (captures sit at 30s/65s/170s).
- **N4 carry claim inaccurate:** "a blocked cause no longer suppresses a DIFFERENT cause's trigger" is true only via the pair-key; the per-path `continue` still skips the alternative causes on a cooldown block.
- **N2/N7 silently omitted** from the carry list — no explicit reason for either (arch §6.4 dedup-key wording; multi-bundle same-tick shed attribution).
- **Frozen-text residues:** the Dedup bullet omits the 3-condition hysteresis; the trigger bullet's (b) element says "first any-lane-at-bound fallback" while the code names the drop's own site — both documented in code headers + change-log only.

### Reviewer agreement

- B1 test-gap: 3 independent lens waves + the fix-audit (4 sources).
- qos re-bless incompleteness: edge + acceptance + architecture + codebase + security (5 sources), probe-verified.
- Pool under-fire: edge lens + mechanism verification (phase order + pinned-fixture analysis).
- W3 residue: acceptance + blind + fix-audit.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
