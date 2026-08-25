# Perkins r2 fix-audit notes (working file — Perkins pane only)

Round: 2 · sha f906725 · PR 36 · job packet-plumber-v2-4.2-surge-crisis

## Verification evidence (all run at f906725 in the round worktree)
- `odin test core` — 117/117 green (tracking allocator; no crisis_test leaks)
- `tools/harness.sh run` — 15/15 demos green (T1 + log + T2 pixel compare)
- `tools/harness.sh drift-check` — 104/104 mutations rejected
- surge.log.bin decodes to the expected 9-command action log (header + 6 draws + 2 demolish... verified growth 71→173 = +4 commands consistent)
- qos.t1 delta = ticks 1200–1500 only (301 ticks) — trigger-element re-bless, cause-documented
- qos.log.bin + qos/65000ms.png UNCHANGED (change-log says "T1/log/T2 re-blessed" — overstates; only T1 moved; T2 pixel-identical)

## Fix audit (verified against code)

### B1 — identity mechanism REAL; biting test MISSING → carried BLOCKER
- Active_Crisis stores (bundle_lo, bundle_hi) canonical pair + E11-stable member pipe; bundle slot re-resolved per tick via bundles_slot_for_pair; !ok (pair gone) → resolve. Cooldown registry keyed on the pair. types.odin comment documents. Pair fields NOT serialized (w_crises_section writes only the resolved slot — T1 bytes unchanged; harness green proves it).
- resolve tests (d)/(l)/cooldown: every topology transition preserves slot order (demolish both narrows → all bundles gone → redraw mints same pairs in same order). The old stale-slot code would produce the same streams. NO test demolishes a preceding bundle while the crisis's pair stays live (the renumber scenario). Mandate close-condition "pinned by a test that bites" UNMET.
- Observed: pipe field = trigger-time member id; banner can name a demolished member while the pair lives (cosmetic; outline is slot-driven and correct).
- surge.dem exercises the !ok branch (@2381 — the whole bottleneck bundle demolished → identity-resolve) — but that's the pair-gone case, not the renumber case.

### B2 — FIXED (three pins verified) with depth notes
1. settled-scan positive: test_crisis_settled_scan_names_slot_order_bundle — (a) branch names bundle 0 at 1200 while drop-free; first streaming shed lands later on bundle 1. BITES.
2. backward-tick latch: test_crisis_backward_tick_latches — backward latches, no events appended, tick unchanged. Equal-tick: allowed + documented (step.odin comment); exercised by pre-existing test_bundle_rebuilds_on_topology_change (step_once twice on one state = tick 1 twice; would latch if rejected; suite green).
3. byte-layout pins: test_crisis_event_payload_byte_layout — drop payload + tags 8/9 + crises section. Crises-section bytes asserted individually; drop-payload + tags 8/9 payloads SIZE-pinned only (no byte-value assertions like the tags 1–7 pin). Test message bug: says "want 30", expression = 38.
→ notes: pin depth (value-blind for drop/tags 8-9), "want 30" message.

### W1 — FIXED. drop_of_reason_this_tick (no class filter) = frozen "ANY Pool_Exhaustion".
### W2 — FIXED. surge.dem: demolish @119000ms (tick 2381) → resolve; wides @120000ms (tick 2401) → re-trigger; window-end resolve @3000. surge.t1/log.bin/170000ms.png re-blessed; harness green at this sha (verified live). Notes: no T2 capture brackets the 2381/2401 cycle (blind-c2/arch-c2 lenses); the resolve ticks are pinned by T1 + comments, not a capture.
### W3 — PARTIAL → carried note. serialize.odin w_event_payload comment AMENDED (admits +4B fold) ✓; change-log admits ✓; types.odin:293 STILL claims "pre-3.3/3.4/4.1/4.2 event streams stay byte-identical"; spec-4-2:30 frozen Events bullet STILL says "pre-4.2 streams byte-identical" (frozen — needs human renegotiation; change-log inside the file admits).
### W4 — FIXED (ordering restored + pinned; residue note). Pass 1 = settled slot-order scan FIRST; pass 2 = drop-fallback. Test (i) pins slot-order-first. qos.t1 re-bless cause-documented. Residue: frozen (b) element text says "first any-lane-at-bound fallback"; the code names the DROP'S OWN site (first shed), any-lane-at-bound only as defensive fallback — documented in the change-log as the faithful implementation; frozen bullet unamended.
### W5 — FIXED (code). json.String type-assert → named load error ("archetype_id must be a string"); absent key → -1 pure demand. Note: the wrong-typed branch has NO test row (only unknown-id row at catalog_test.odin:287-291).
### W6 — FIXED. Flow_State.drop_sites per-tick scratch; cleared at flow_step top; appended in event_emit_drop; NEVER serialized; engine reads only drop_sites. Event buffer untouched.
### W7 — FIXED. test_crisis_replay_identity now deletes evs; no crisis_test leaks in the tracking run.

### N1 — CARRIED, reason VERIFIED (step_once double-step on one state exercises equal ticks; suite green; comment documents).
### N2 — NOT mentioned in change-log → silent omission. Dedup key still (archetype, set_piece); arch §6.4 wording conflict persists. → note.
### N3 — FIXED. 65535 set-piece cap + named load error (catalog.odin).
### N4 — claim INACCURATE. "a blocked cause no longer suppresses a DIFFERENT cause's trigger that tick": the per-path `continue` still skips (b)/(c) for that set-piece on a blocked (a) candidate; what actually changed is the pair-key (slot-collision cross-suppression). r1 N4's literal complaint (fall-through) persists. → note.
### N5 — FIXED. bound-2 clamp test (test_crisis_resolve_margin_clamp_tiny_bound).
### N6 — FIXED (E22 NO_BUNDLE rides the new pin; size-pinned — folded into the B2 pin-depth note).
### N7 — NOT mentioned → silent omission. Multi-bundle same-tick shed attribution order still unpinned. → note.
### N8 — FIXED (comment 1501 → 1500).
### N9 — FIXED (Event.target comment extended).
### N10 — FIXED (crises_256_doc on temp_allocator).
### N11 — CARRIED explicitly ("harness/tooling scope") ✓.
### N12 — CARRIED explicitly ✓.
### N13 — PARTIAL → note. crisis.odin header + change-log document the 3-condition hysteresis ✓; frozen spec Dedup bullet unamended (frozen).

## NEW findings (confirmed, from lenses + my verification)
- NEW-W1 (warning): Pool_Exhaustion trigger's eval-time `len(packets) >= pool_max` under-fires when deliveries drain the pool after the spawn-shed (flow_step phase 5 cull runs before crisis_evaluate). The drop is admission-time evidence (the W4 precedent). Pinned test covers only the no-delivery regime (no pipes). core/crisis.odin:439-442.
- NEW-N (note): B2-3 pin depth + "want 30" message bug (crisis_test.odin:553).
- NEW-N (note): W5 wrong-typed branch untested (catalog_test.odin).
- NEW-N (note): qos change-log "T1/log/T2 re-blessed" overstates — only qos.t1 changed.
- NEW-N (note): surge.dem 2381/2401 cycle not T2-bracketed.
- REJECTED lens findings: draw/flow/win log.bin "byte-identical" (false — catalog fold); doubled wide draws in surge.dem (by design — two parallel wides); security string-length (trusted catalog data, consistent pattern); architecture perf walks (bounded by pool cap 512, negligible at 20Hz).

## Lens status
- c1: 7/7 done, valid JSON.
- c2: 7/7 done, valid JSON.
- c3: running.
- Remaining: c4, c5, c6, c7.

## PROBE VERIFIED (scratch test, deleted after) — qos crisis stream at f906725
- tick 1200: TRIGGER bundle 0 (pipe 0) — the settled scan (slot-order, W4 restore)
- tick 1201: RESOLVE b0 + TRIGGER b1 (pipe 1) — SAME-TICK resolve+re-trigger (no topology edit)
- tick 1300: active = bundle 1 pipe 1 triggered_tick 1201 → matches blessed 65s PNG ("bundle 1 (pipe 1)") → harness green consistent
- Tests-c3 blocker premise ("f906725 engine renders bundle 0 at 65s") REFUTED by probe + PNG decode + harness green.
- CONFIRMED: qos re-bless embeds an undisclosed trigger/resolve/trigger chatter at the window open; change-log cause ("element changed 1->0") covers only tick 1200; "T1/log/T2 re-blessed" false for log/T2 (byte-identical). → NEW WARNING (golden discipline: incomplete cause-doc; blessed chatter cycle undisclosed). Not a dedup breach (resolve precedes re-trigger) — contract-compliant but the golden's ONE-trigger-per-persistent-flaw discipline claim (crisis.odin header) is contradicted by the transient-blip trigger.
