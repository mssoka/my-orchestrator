## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-4.2-surge-crisis · **Reviewed sha:** b94d54f · **Reviewers:** 7/7 completed
**Verification:** 22/56 findings confirmed against the code — 9 discarded as false-positive, 25 merged into the survivors

### Blockers (2)

**1. `Active_Crisis.bundle` is a compaction-prone slot index — mid-crisis topology edits renumber bundle slots, breaking the `[E13]` dedup contract and the root-cause ref** *(edge)*
`core/crisis.odin:283-285` + `core/bundles.odin:105-113` + `core/types.odin:224`

Bundles are a derived view rebuilt from scratch on every topology change (`clear(&b.bundle_lo) … b.n = 0`, then slots assigned in pipe-slot order on first-seen canonical pair). `Active_Crisis.bundle` stores the SLOT index. Demolish a full bundle whose slot precedes the crisis's named bundle mid-crisis → later slots shift down → the registry's ref now names a different pair (or nothing). The resolve pass then sees queue 0 / no bound lane → **spurious `Crisis_Resolved` while the real flaw is still saturated**, followed by same-tick re-trigger (E13 chatter) or a silently vanishing crisis; the banner + bottleneck outline mislabel the wrong pair. The resolve test passes only because its fixture's canonical pairs preserve slot order across the demolish/redraw. This is the story's own core scenario (player edits during a crisis).
**Fix:** key `Active_Crisis` on stable refs — the canonical `(bundle_lo, bundle_hi)` node pair or the E11-stable member pipe id — resolving the bundle slot at eval time (`bundles_slot_for_pair` / `bundle_of_pipe`).

**2. Advisory test gate: FAIL — the settled-scan trigger branch never executes, the 4.2 tick-latch has zero coverage, and the 4.2 serialization surface has no byte-layout pins** *(tests)*
`core/crisis.odin:325-342` · `core/step.odin:35-38` · `core/serialize.odin:229-243,379-386`

Every fixture's saturated tick also sheds same-tick, so `crisis_find_saturated_bundle`'s `ok=true` branch — half of the pinned trigger contract — never executes. No test steps a backward tick (`replay_error` unreachable). `test_event_payload_byte_layout` pins tags 1–7 only: the drop-payload target byte, tags 8/9, and the crises section could be deterministically wrong and pass replay + blessed T1s silently. P0 is 100%; P1 ~77% → FAIL.
**Fix:** (1) settled-scan positive test (queue at bound, no same-tick drop); (2) backward-tick latch test; (3) byte-layout pins for the drop target + tags 8/9 + crises section.

### Warnings (7)

1. **Pool_Exhaustion backstop is class-filtered — frozen contract says ANY `Pool_Exhaustion` drop** *(edge, acceptance)* — `core/crisis.odin:359-361`. With QoS reprioritization, a resident class pays the E22 shed while the surge rides a higher lane: pool at cap, shedding, no crisis ever fires. Under-fires (fail-safe) but breaches the pinned "any" definition. Drop the class filter or amend the frozen text.
2. **`surge.dem` omits the frozen spec's mid-run capacity fix — no `Crisis_Resolved` pin in the launchable golden** *(acceptance, edge, tests, blind)* — `demos/surge.dem`. The frozen Golden bullet pins "trigger @window start, a mid-run capacity fix, resolve after the window ends"; the shipped demo never draws the fix and its 170s capture pins banner-present. Unit tests cover resolve; E2E does not — the "you can fix it" half of the fairness loop is undemonstrated.
3. **Frozen "pre-4.2 streams byte-identical" promise is false as written** *(blind, acceptance, codebase, architecture)* — the drop payload grew 4 bytes (`w_u32 target` unconditional); only the change-log admits it. `spec-4-2:30`, `core/types.odin:279`, `core/serialize.odin:358` still claim byte-identity. Amend all three texts (mechanism itself verified: `state.catalog_hash` rides every per-tick hash; drop-payload byte folds drop-bearing streams).
4. **Trigger root-cause attribution reverses the pinned slot-order definition** *(blind, acceptance)* — `core/crisis.odin:325-342` names the drop's bundle first; the frozen contract pins "first saturated bundle in slot order (a → first hit)". Change-log #1 documents the reversal (admission-time evidence is sharper) but the frozen block is unamended. Amend the frozen trigger block or restore slot-order selection.
5. **Wrong-typed `archetype_id` silently loads as a pure demand event** *(security)* — `core/catalog.odin:550-551,821-824`. `jstr` returns "" for numeric/bool/null → indistinguishable from absent → the set-piece never fires a crisis, no load error, while an unknown string id fails fast. ODN-5 bar: type-assert `json.String`; key present but non-string → named load error.
6. **Crisis engine reads the ODN-14 event buffer as sim input — the app's never-drain becomes a correctness contract** *(architecture)* — `core/crisis.odin:143-175` + `app/main.odin:120-126`. The buffer grows unboundedly on the app path; any future drain/filter silently breaks attribution; the guard is a human-only tripwire comment. Prefer a per-tick drop-site field on `Flow_State`.
7. **`test_crisis_replay_identity` leaks the events array (2×256B) under the tracking allocator** *(codebase, edge, acceptance)* — `core/crisis_test.odin:53,366-371` (`hashes, _ := …`). Contradicts the change-log's "leak hygiene" claim; leaks are CI failures per project-context.

### Notes (13)

1. Step tick-latch rejects only backward ticks; `tick == state.tick` re-runs the tick despite the "strictly monotonic" claim *(blind, security, architecture)*.
2. E13 dedup key (archetype, set_piece) is coarser than arch §6.4's per-root-cause key — spec-compliant per the frozen 4.2 text, but §6.4 now conflicts *(architecture)*.
3. Set-piece index truncates to u16 with no roster cap (the crises roster got a 255 cap for the same class) *(edge, security)*.
4. Cooldown-blocked drop branch skips the settled-scan + pool backstop for that set-piece *(blind)* — cooldown > 0 only.
5. Resolve-margin clamp branch (bound ≤ margin) never executes in any test *(tests)*.
6. E22 drops' `target=NO_BUNDLE` has no unit assertion *(tests)*.
7. Earliest-drop attribution across multiple bundles in one tick is untested *(tests)*.
8. Pool test comment says the fix lands @1501; the code draws it @1500 *(blind)*.
9. `Event.target` comment omits the new Packet_Dropped shed-bundle usage *(blind)*.
10. `crises_256_doc` leaks its builder string under the tracking allocator *(codebase)*.
11. Harness `load_catalogs` crises.json read-error path has no negative test *(tests)*.
12. qos golden span ends mid-window (tick 1500 < 3000) *(tests)*.
13. Frozen resolution sentence omits the implemented hysteresis (below bound−margin, no lane at bound, no same-tick drop) *(blind)*.

### Reviewer agreement
- **surge.dem fix/resolve omission** — acceptance + edge + tests + blind
- **byte-identity promise drift** — blind + acceptance + codebase + architecture
- **pool backstop class filter** — edge + acceptance
- **trigger attribution order** — blind + acceptance
- **replay-test leak** — codebase + edge + acceptance
- **latch non-strict** — blind + security + architecture

### Golden discipline (verified clean)
Every existing `.t1`/`.log.bin` shift traces to the documented causes: the catalog_hash fold (`crises.json` + `demand.json` `archetype_id` — rides every per-tick hash via `state.catalog_hash`, and the `.log.bin` header) + the drop-payload byte. The only shifted T2s are `warn`/`qos` @65s (era-3 surge-active banner + outline — documented); zero-traffic demos' T2s are untouched (the negative proof). `surge.t1` is new, 4000 ticks, captures at 30s/65s/170s consistent with the narrative. No re-bless-without-proof found.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
