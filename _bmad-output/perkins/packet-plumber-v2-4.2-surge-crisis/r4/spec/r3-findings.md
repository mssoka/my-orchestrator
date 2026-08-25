# Perkins r3 findings — the rework this round claims to fix (f9184fa)

The r4 commit message claims to fix B3, W-1..W-3, N-1..N-13. Each item below is the r3 finding VERBATIM. Do NOT re-file these as new findings unless the code proves a claimed fix is absent — then use title prefix 'STILL-PRESENT: ', category 'fix-audit'.

## Blockers
- **B3 [blocker] (acceptance, blind, codebase, edge, perkins-probe): B3: the N4 restructure removed the post-trigger guard — a successful (a)/(b) trigger no longer gates the (c) pool backstop, so ONE (archetype, set_piece) activation can emit two Crisis_Triggered events and hold two active rows on the same tick (E13 dedup breach)**
  - location: core/crisis.odin:430-483 (trigger pass) — regression vs f906725's post-trigger `continue`
  - evidence: r2 (f906725): 'crisis_trigger(state, tick, cat, ai, u16(si), .Saturated_Bundle, b, sp.class, sp.multiplier)\n\t\t\tcontinue' — the continue skipped (c) after a successful (a)/(b) trigger. r3 (121d8a0): (a) fires -> a_hit = true -> (b) skipped via !a_hit -> (c) checks only crisis_cooldown_blocked(.Pool_Exhaustion, 0, 0) (a DIFFERENT kind — never blocks a Saturated_Bundle trigger) -> crisis_trigger appends a SECOND row. crisis_trigger appends unconditionally (no crisis_active_for check); the dedup
  - detail: Two Crisis_Triggered events with no resolve between = the E13 duplicate the lens-guards define as a blocker; the frozen letter says 'Crisis_State.active holds at most one crisis per (archetype, set-piece activation)'. Two rows double the banner cards and the serialized section for one activation. Impossible at f906725 — a regression introduced by the N4 restructure.
  - recommended_fix: After a SUCCESSFUL crisis_trigger in (a) or (b), `continue` to the next set-piece (or re-check crisis_active_for before (c)). N4's intent survives: only a successful trigger gates the pool backstop — a cooldown-BLOCKED (a) still falls through to (c).

## Warnings (W-1=W-warn1, W-2=W-poolcap, W-3=W3-carry)
- **W-1 [warning] (codebase, tests, acceptance, architecture, security, edge, perkins-audit): W-warn1: warn.t1 shifted 300 hashes (ticks 1201-1500) in the rework commit but is OMITTED from the re-bless scope — and the line's 'everything else byte-identical' claim is false**
  - location: goldens/warn.t1:1201-1500 + spec-4-2-surge-crisis.md:175-176 (Re-bless scope line)
  - evidence: git diff f906725..121d8a0: goldens/warn.t1 | 600 +++---- (300 hash rows, ticks 1201-1500). Change-log: 'Re-bless scope this round: qos T1/log/PNGs, warn 65s PNG, surge PNGs + one new capture — all cause-documented; everything else byte-identical.' warn.t1 is not named; 'everything else byte-identical' is contradicted by the delta. The shift IS caused by the same W-qos margin fix (warn.dem's fixture saturates under the surge — its crisis stream changed identically; PNG decode: r2's blessed warn b
  - detail: An unnamed T1 golden shift contradicting an explicit 'byte-identical' claim is the golden-discipline trap the lens-guards define as a real finding — a verifier reading the scope line is misled about what moved and why.
  - recommended_fix: Amend the scope line: name warn.t1 (300-hash shift, same margin-fix cause; the warn 65s PNG changed element 3->1 AND the dash), and drop the unchanged qos log from the re-bless list.
- **W-2 [warning] (edge): W-poolcap: with pool_max_packets = 1 or 2 (legal catalog values) a Pool_Exhaustion crisis triggers but can NEVER resolve — a permanent crisis (fairness rule 4: the player can always recover)**
  - location: core/crisis.odin:412-414 (pool resolve) + core/catalog.odin:620-622 (validation allows any > 0)
  - evidence: resolve: 'cleared = len(state.flow.packets) + int(CRISIS_RESOLVE_MARGIN) < int(cat.balance.pool_max_packets) && !drop_of_reason_this_tick(...)'. CRISIS_RESOLVE_MARGIN = 2. cap 1: len + 2 < 1 impossible; cap 2: len + 2 < 2 impossible. Trigger side fires fine ('drop && len + 2 >= cap' is always true with a drop). The E9 path has the N5 margin clamp ('if bound > 0 && bound <= margin { margin = bound - 1 }') — the pool cap has no equivalent. Shipped balance.json = 512 (unreachable in shipped content
  - detail: A cap-1/2 catalog (legal per the parser's own validation) produces a crisis that never clears even after the player fixes the network — the anti-flap margin eats the entire recovery band.
  - recommended_fix: Clamp the resolve margin for the pool cap (e.g. margin = min(margin, cap-1), the N5 pattern) or validate pool_max_packets >= 3 at load.
- **W-3 [warning] (acceptance, security, edge, architecture, codebase, perkins-audit): W3-STILL-PRESENT: the types.odin Event comment now admits the +4B Packet_Dropped fold AND still ends with the false 'pre-3.3/3.4/4.1/4.2 event streams stay byte-identical' sentence — self-contradictory**
  - location: core/types.odin:290-296
  - evidence: '(Event.target — the 4.2 re-bless's documented event-stream fold; tags 8/9 are genuinely append-only). The tag byte is the serialized discriminator… the serializer writes them tag-conditionally so pre-3.3/3.4/4.1/4.2 event streams stay byte-identical (golden stability).' vs serialize.odin:385-387: 'pre-4.2 drop payloads were class+reason only, so pre-4.2 event streams are NOT byte-identical; the 4.2 re-bless covers the fold'.
  - detail: The r2 fix asked types.odin to adopt serialize.odin's wording. The admission was added but the contradicted sentence remains verbatim in the same comment — a reader is still told the false guarantee three lines below the true one.
  - recommended_fix: Reword the trailing sentence: pre-4.2 drop-bearing streams are NOT byte-identical (the documented +4B fold); only streams without Packet_Dropped events (tags 1-7, 8/9 append-only) stay byte-identical.
  - carry: still present since round 2 (narrowed)

## Notes (N-1..N-13 in order)
- **N-1 [note] (edge): N-hud: the HUD title 'Packet Plumber — v2 story 4.2 (surge + crisis engine)' feeds the byte-truncating draw_text helper — the em-dash renders mojibake in every capture (pre-existing: 4.1's line had it; this PR only renumbered the string)**
  - location: app/main.odin:519 + app/main.odin:741-747 (draw_text truncates runes to bytes)
  - evidence: N/A
  - detail: Same mojibake class the banner fix just removed — the HUD line was touched by this PR and could have been cleaned.
  - recommended_fix: Replace the em-dash with ASCII in the HUD title.
- **N-2 [note] (blind): N-deadparam: crisis_trigger's `cat: ^Catalogs` parameter is unused in the body**
  - location: core/crisis.odin:285
  - evidence: N/A
  - detail: The body reads only state (bundles, first_member_pipe). Dead parameter — callers pass cat for no effect.
  - recommended_fix: Drop the parameter (or use it, e.g. assert archetype bounds).
- **N-3 [note] (architecture): N-stale-comments: the pre-W-qos RELIEVED comment block (still describing 'NO lane at the E9 bound') is stacked above the new margin comment; serialize.odin:367-369 still describes the Packet_Dropped payload as '(class + reason, 3.3)' — omits the 4.2 target byte**
  - location: core/crisis.odin:377-384 (vs 388-400) + core/serialize.odin:367-369
  - evidence: N/A
  - detail: Two stale comments misdescribing the code they annotate — the old lane threshold and the 3-byte drop payload.
  - recommended_fix: Delete/reword the stacked RELIEVED block; append '(+ target, 4.2)' to the serialize comment.
- **N-4 [note] (blind, tests, tests, tests): N-pool-banner: the pool banner title (~69 chars at 15px, ≈500px+) spills the fixed card_w=440 card, and the Pool_Exhaustion banner branch has ZERO blessed pixel coverage anywhere in the golden suite**
  - location: app/render/crisis.odin:30-31 (card_w 440), 63-65 (pool title) — no capture shows the pool banner
  - evidence: N/A
  - detail: The one banner variant never pixel-pinned is also the one that overflows its card — both would surface the first time a pool crisis renders in a capture.
  - recommended_fix: Widen the card or shrink the pool title; bless one pool-crisis T2 capture.
- **N-5 [note] (perkins-audit): N-anyclass: the pool trigger's ANY-class discriminator (a NON-surge class's E22 shed firing the map-wide crisis) remains unpinned — the new routed fixture's shed is the surge class**
  - location: core/crisis_test.odin:305-327
  - evidence: N/A
  - detail: The r2 note's second half (a non-surge-class shed case) was not addressed; the trigger's class-independence rides the frozen letter but no test exercises it.
  - recommended_fix: Add a fixture where the shed class differs from the surge class (e.g. email BE sheds at the pool) and assert the crisis still fires.
- **N-6 [note] (tests): N-b-fallback: no test isolates the (b) drop-fallback's drop-site attribution (the settled-scan test pins (a); the re-trigger pins don't distinguish which element the (b) branch names)**
  - location: core/crisis_test.odin:503-510
  - evidence: N/A
  - detail: The (b) element selection (drop's own site vs slot-order scan) has no fixture where the two disagree and the (b) outcome is asserted.
  - recommended_fix: A fixture where (a) misses (service dips the eval queue below bound) and (b) names the drop's own site — assert the bundle.
- **N-7 [note] (tests, tests): N-laneat-pin: the new bundle_lane_at margin lane-threshold (the W-qos root fix) has no direct unit pin — golden-stream coverage only**
  - location: core/crisis.odin:127-133, 400-405
  - evidence: N/A
  - detail: The fix that closed the churn is pinned indirectly by the blessed qos/warn T1 streams; a unit test asserting the (bound - margin) lane threshold would localize regressions.
  - recommended_fix: A tiny unit test on bundle_lane_at / the relieve condition at the margin boundary.
- **N-8 [note] (tests): N-65535-row: the 65535 set-pieces-per-era fail-fast branch has no catalog test row**
  - location: core/catalog.odin:523-524
  - evidence: N/A
  - detail: The named load error (N3's fix) is untested — a 65536-row JSON is awkward but a direct unit call on the parse path would pin it.
  - recommended_fix: Add a row/unit call exercising the cap.
- **N-9 [note] (tests): N-crises-load: the app + harness load_catalogs crises.json read/parse error paths (the new e6 returns) are untested**
  - location: app/main.odin:811-814 + harness/catalogs.odin:28-29
  - evidence: N/A
  - detail: A missing/corrupt crises.json dies at load in both binaries with no test pinning the message.
  - recommended_fix: One missing-file and one corrupt-file test per loader.
- **N-10 [note] (acceptance, architecture): N-surge-comment: surge.dem's Captures comment block omits the new 119500ms banner-GONE capture**
  - location: demos/surge.dem:19-22 (comment) vs :40 (the new capture line)
  - evidence: N/A
  - detail: The narrative comment lists 30000/65000/170000 but not 119500 — the capture that brackets the resolve/re-fire cycle.
  - recommended_fix: Add a comment line: 119500ms = the banner-GONE frame between resolve @2381 and re-trigger @2401.
- **N-11 [note] (tests): N-refired-T1: the re-fired crisis banner (tick 2401-3000, the wide-bundle crisis) remains T1-pinned only — the new capture brackets the GONE frame, not the re-fired banner**
  - location: demos/surge.dem:38-41
  - evidence: N/A
  - detail: The mandate's bracket is satisfied; the optional second half of the r2 note (a capture of the re-fired banner) was not taken — the new bundle's outline is pixel-pinned nowhere.
  - recommended_fix: Optional: capture at ~121000ms, or note the T1-pin rationale in the demo comment.
- **N-12 [note] (tests): N-ascii-gate: the ASCII-only invariant for draw_text_c-fed render strings is comment-documented but has no automated enforcement — the mojibake class can regress silently**
  - location: app/render/crisis.odin:9-10 (the warning comment) — no lint/test gate
  - evidence: N/A
  - detail: The r2 warning class recurred because nothing checked the invariant; a lint grep or unit assert would have caught the em-dash at authoring time.
  - recommended_fix: Add a lint gate (non-ASCII scan of render-string sources) or a unit test over the title builders.
- **N-13 [note] (blind): N-cooldown-mask: a cooldown-blocked pair A (the slot-order scan's first hit) suppresses the (b) drop-fallback for an unblocked pair B that tick — the per-pair cooldown masks another pair's eligible trigger**
  - location: core/crisis.odin:437-455 (a_hit gates (b) even when (a) was cooldown-blocked)
  - evidence: N/A
  - detail: Pre-existing semantics the N4 restructure kept ((b) is gated on !a_hit, so a blocked-but-hit (a) skips it). Attribution latency, not a dedup breach — flagged for the record.
  - recommended_fix: Optional: run (b) when (a) hit but was cooldown-blocked (its own pair-key cooldown check still applies inside).

## r3 false-positives (21) — NEVER re-raise
The r3 report discarded 21 false-positives during verification. The 24 r2 false-positives + 2 r1 false-positives are also closed. Do not re-raise any.

## r3 fix-audit summary (verified FIXED at 121d8a0 — do not re-open these)
- **B1**: FIXED. test_crisis_slot_renumber_keeps_crisis_attached (core/crisis_test.odin:643): crisis on pair P (router<->host) at slot 2; a FULL demand-free island bundle at slot 0 demolished at 1300 (applies 1301); rebuild renumbers P 2->1. Asserts exactly ONE event (trigger @1200; no spurious resolve/re-tri
- **W-qos**: ROOT-FIXED (probe-verified) + disclosed. Relieve now requires bound > margin && class-queue + margin < bound && NO lane at or above (bound - margin) (new bundle_lane_at helper) + no same-tick Queue_Overflow shed of the class. Probe 1 shows the blessed stream is a single clean trigger (T b0 @1200; th
- **W-pool**: FIXED. Trigger is now drop_of_reason_this_tick(.Pool_Exhaustion) && len + CRISIS_RESOLVE_MARGIN >= cap (drop evidence with eval-time depth as anti-flap); resolve unchanged (len + margin < cap && no drop — hysteresis bands disjoint, no chatter). test_crisis_pool_fires_on_routed_delivering_network (po
- **W3-carry**: PARTIAL (STILL-PRESENT). The frozen Events bullet is marked superseded in the change-log (accepted close-condition), and types.odin now ADMITS the Packet_Dropped +4B fold — but the same comment's trailing sentence still claims 'pre-3.3/3.4/4.1/4.2 event streams stay byte-identical (golden stability)
- **W-render**: FIXED. Both banner title strings are ASCII ('ACTIVE - bundle …', 'ACTIVE - network at capacity (pool exhausted)'); the redesign line (crises.json preventive_redesign + fallback) is ASCII; PNG decode of qos/warn/surge banners shows clean hyphens, no mojibake glyphs. (Residual: the app HUD title em-da
- **B2-3**: FIXED (message now prints the computed 38: 'got %d, want %d').
- **W5**: FIXED (wrong-typed archetype_id:42 row -> 'archetype_id must be a string'; absent-key positive -> archetype_idx -1).
- **pool marginal regime**: FIXED (routed fixture — see W-pool). ANY-class discriminator (a NON-surge class's E22 shed triggering the pool crisis) remains unpinned — note.
- **surge.dem T2 bracket**: FIXED (119500ms capture; banner-GONE frame verified). Residuals: the demo's Captures comment omits the new line; the re-fired banner (2401-3000) stays T1-only — notes.
- **N4**: RESTRUCTURED as claimed (the per-path `continue`s are gone; a cooldown-blocked (a) no longer skips the (c) pool backstop) — BUT the restructure removed the post-SUCCESS-trigger guard too: a successful (a)/(b) trigger no longer gates (c), producing a same-tick double Crisis_Triggered + two active row
- **N2**: CARRIED with recorded reason (the (archetype, set_piece) dedup key is the frozen 4.2 letter; arch §6.4's per-root-cause wording targets the [LATER] era layer — recorded, not acted on).
- **N7**: CARRIED with recorded reason (the multi-bundle same-tick case is exercised by the settled-scan test + the re-trigger pins).
- **frozen-text residues**: CARRIED (both marked superseded in the change-log; the operative trail).