# Perkins r3 fix-audit working notes (authoritative, Perkins-owned)

Sha: 121d8a0 (reviewed). All verifications performed against the round worktree
(/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r3).

## Fix audit vs r2 findings (mandate a-e)

### (a) B1 — FIXED (test exists and bites)
- `test_crisis_slot_renumber_keeps_crisis_attached` (core/crisis_test.odin:643): crisis on pair P
  (router<->host, slot 2); demand-free island bundle at slot 0 demolished at 1300 (applies 1301);
  rebuild renumbers P 2->1. Asserts: exactly ONE event (trigger @1200, no spurious resolve/re-trigger),
  active stays 1, bundle_lo/hi (1,2) unchanged, pipe 2, bundle re-resolved to 1,
  triggered_tick 1200, bundles_slot_for_pair(1,2)==1, re-resolved slot still saturated.
- Bites both ways: neutralizing the pair identity (slot-keyed) resolves spuriously (slot 2 out of range
  after renumber -> !ok -> resolve -> event count fails); removing the demolish leaves the slot at 2 ->
  expect(ac.bundle==1) fails. NOT vacuous (island carries no terminals; streaming flow untouched).
- surge.dem: capture at 119500ms (tick 2390) added — PNG decode confirms NO banner (the banner-GONE
  frame between resolve @2381 and re-trigger @2401). T2 bracket present. surge.t1 byte-identical
  (not in the delta) — consistent.

### (b) W-qos — ROOT-FIXED (probe-verified) + disclosure, but scope line still inaccurate
- Code: relieve now `bound > margin && bundle_class_queue+margin < bound && !bundle_lane_at(b, bound-margin)`
  + `cleared = relieved && !drop_of_class_this_tick(...)` (crisis.odin:400-405). New helper bundle_lane_at.
- PROBE (tools/probe-r3, qos.dem scenario seed 3003, 1250 ticks): tick=1200 TRIGGERED cause=1 class=1
  target=0 pipe=0; NO other crisis events; active at end = 1 row (bundle 0 lo=0 hi=1 pipe=0 triggered=1200).
  The @1201 same-tick resolve+re-trigger churn is GONE. qos/65000ms.png re-blessed shows
  "ACTIVE - bundle 0 (pipe 0)" (r2's blessed PNG named bundle 1 — the churn's residue).
- Change-log discloses the churn + the fix accurately, corrects the r1-fix scope claim.
- BUT the NEW scope line is itself inaccurate (see NEW finding N-warn1 below): warns "everything else
  byte-identical" while warn.t1 shifted 300 hashes (1201-1500), and lists "qos T1/log/PNGs" while
  qos.log.bin is unchanged in the delta.

### (c) W-pool — FIXED (code + fixture) 
- Trigger now `drop_of_reason_this_tick(.Pool_Exhaustion) && len + CRISIS_RESOLVE_MARGIN >= cap`
  (drop evidence + anti-flap) — matches the mandate. Resolve unchanged (len+margin < cap && !drop —
  hysteresis bands disjoint: trigger needs drop, resolve needs !drop; no chatter).
- `test_crisis_pool_fires_on_routed_delivering_network`: pool cap 10, email delivers over two wides per
  side (eval pool below cap while shedding), streaming waits at an unroutable host; asserts trigger @1200
  (Pool_Exhaustion, NO_BUNDLE) — the routed under-fire regime pinned. 119/119 odin test green.

### (d) W3-carry — PARTIAL (still-present) + W-render — FIXED
- types.odin:290-296 now ADMITS the Packet_Dropped +4B fold BUT the trailing sentence still claims
  "pre-3.3/3.4/4.1/4.2 event streams stay byte-identical (golden stability)" — self-contradictory
  comment (serialize.odin:385-387 says the opposite). STILL-PRESENT (5 lenses + my read agree).
- Frozen Events bullet marked superseded in the change-log (the operative trail) — accepted.
- W-render: both banner title strings now ASCII ("ACTIVE - bundle ...", "ACTIVE - network at capacity
  (pool exhausted)"). PNG decode of qos/warn/surge 65s banners: clean "-" glyphs, no mojibake.
  redesign string (crises.json preventive_redesign + fallback) is ASCII. Non-ASCII runes in
  crisis.odin/view.odin are comment-only. FIXED.

### (e) Notes
- B2-3 message: FIXED ("got %d, want %d" with the computed 38).
- W5 branches: FIXED (wrong-typed archetype_id:42 row -> "archetype_id must be a string"; absent-key
  positive -> archetype_idx -1).
- Pool marginal regime: routed fixture added (see (c)). ANY-class discriminator (a NON-surge class's
  E22 shed triggering the pool crisis) remains unpinned — in the new fixture the shed is the surge class.
- surge.dem T2 bracket: FIXED (119500ms capture; banner-GONE frame verified by PNG decode).
- N4: the per-path `continue`s are GONE (a_hit flag; (b) gated on !a_hit; (c) reached regardless) —
  BUT the restructure introduced the (a)/(b)+(c) same-tick double-trigger (see BLOCKER below).
- N2: recorded reason in change-log (frozen 4.2 letter; arch §6.4 wording targets [LATER] era layer).
- N7: recorded reason (the settled-scan test + re-trigger pins exercise the attribution).
- Frozen-text residues: both marked superseded in the change-log.

## NEW findings (my own verification)

### BLOCKER B3: N4 restructure removed the post-trigger guard — (a)/(b) trigger + (c) pool backstop
fire the SAME tick for ONE (archetype, set_piece) activation (E13 dedup breach)
- r2 had `crisis_trigger(...); continue` after (a) and (b). The restructure (fixing N4's cooldown-skip)
  removed the post-SUCCESS-trigger continue: (a) fires -> a_hit=true -> (b) skipped -> (c) checks only
  the PER-CAUSE cooldown (Pool_Exhaustion vs Saturated_Bundle — never blocks) -> second trigger.
- crisis_trigger appends unconditionally; the `crisis_active_for(ai, si)` dedup check runs once at the
  top of the set-piece loop, BEFORE any trigger — not re-checked.
- PROBE-VERIFIED reachable (tools/probe-r3/main2.odin): pool cap 14, email BE on all pipes, streaming
  standard, narrow host->rt leg. At tick 1200: TWO Crisis_Triggered events + two active rows
  (kind=1 Saturated_Bundle bundle=2 AND kind=2 Pool_Exhaustion NO_BUNDLE), both set_piece=0 archetype=0.
  At r2 (f906725) the same tick could not double-fire (post-trigger continue). REGRESSION.
- Frozen dedup letter: "Crisis_State.active holds at most one crisis per (archetype, set-piece
  activation)". Lens-guard E13: duplicate Crisis_Triggered without a resolve = a blocker. -> BLOCKER.
- Fix: after a successful crisis_trigger in (a)/(b), `continue` to the next set-piece (or gate (c) on
  "no trigger appended this tick" / re-check crisis_active_for). N4's intent (cooldown-blocked cause
  must not skip the pool backstop) survives: only a SUCCESSFUL trigger gates the rest.

### WARNING W-warn1: warn.t1 shifted 300 hashes (ticks 1201-1500) — not in the re-bless scope line
- Delta f906725..121d8a0: goldens/warn.t1 changed 600 lines (300 hash rows) at ticks 1201-1500.
- Change-log scope: "qos T1/log/PNGs, warn 65s PNG, surge PNGs + one new capture — all cause-documented;
  everything else byte-identical." warn.t1 is NOT named; "everything else byte-identical" is FALSE.
- The shift IS caused by the same W-qos margin fix (warn.dem's fixture saturates under the surge — its
  crisis stream changed identically), so the cause exists — but the golden-discipline trail doesn't
  name it, and the explicit claim is contradicted by the delta.
- Also: "qos T1/log/PNGs" lists log, but qos.log.bin is UNCHANGED in the delta (over-claim).
- Fix: amend the scope line to name warn.t1 (300-hash shift, same margin-fix cause) and drop the
  unchanged qos log from the re-bless list.

### WARNING W-poolcap: Pool_Exhaustion crisis can never resolve when pool_max_packets is 1 or 2
- Resolve: `len + CRISIS_RESOLVE_MARGIN(2) < cap` — cap 1: len< -1 impossible; cap 2: len<0 impossible.
  Trigger side fires (drop + len+2 >= cap is always true with a drop). Legal catalog values (parser
  requires only > 0). A cap-1/2 catalog = a PERMANENT, never-resolving crisis (fairness rule 4:
  "the player can always recover"). The E9 path has the N5 margin-clamp (`if bound <= margin { margin =
  bound-1 }`); the pool cap has no equivalent clamp. Shipped balance.json = 512 (unreachable in shipped
  content) — catalog-authoring-only, so warning not blocker.
- Fix: clamp margin for the pool cap (e.g. margin = min(margin, cap-1) or the bound-1 pattern), or
  validate pool_max_packets >= 3 at load.

### NOTES (new)
- N-hud: app/main.odin:519 HUD title "Packet Plumber — v2 story 4.2 (surge + crisis engine)" feeds the
  byte-truncating draw_text (same u8(c) truncation as draw_text_c) — em-dash renders mojibake in EVERY
  capture. The em-dash predates the PR (4.1's line had it; the PR only renumbered the string) — a
  pre-existing defect in a touched line, not introduced by this PR.
- N-deadparam: crisis_trigger's `cat: ^Catalogs` parameter is unused in the body.
- N-stale-comments: (1) the pre-W-qos RELIEVED comment block (crisis.odin:377-384, "NO lane at the E9
  bound") is stacked above the new margin comment and misdescribes the code (now bound-margin);
  (2) serialize.odin:367-369 event-loop comment describes the Packet_Dropped payload as "(class +
  reason, 3.3)" — omits the 4.2 target byte.
- N-pool-banner-overflow: the pool title (~69 chars at 15px ≈ 500px+) exceeds card_w=440 — spills the
  card border (and the pool banner branch has zero blessed pixel coverage).
- N-anyclass: the pool trigger's ANY-class discriminator (a non-surge class's E22 shed firing the
  map-wide crisis) remains unpinned (in the new fixture the shed is the surge class).
- N-b-fallback-pin: no test distinguishes the (b) drop-fallback's drop-site attribution (the settled
  scan test pins (a); the re-trigger pins don't isolate (b)'s element selection).
- N-laneat-pin: bundle_lane_at / the margin lane threshold has no direct unit pin (pinned indirectly by
  the blessed qos/warn T1 streams).
- N-65535-row: the 65535 set-pieces-per-era fail-fast branch (catalog.odin:523-524) has no test row.
- N-crises-load-errs: app + harness load_catalogs crises.json read/parse error paths untested.

## Rejected / not re-raised (c1 lens noise)
- blind "Frozen 'pre-4.2 streams byte-identical' guarantee is false (spec Events bullet)" — the frozen
  bullet is marked superseded in the change-log (the mandate's accepted close-condition). Not new.
- blind "Trigger pass 2 implements drop-site attribution while the frozen text and the file header
  claim the first any-lane-at-bound fallback" — the documented frozen-text residue, marked superseded.
  The file-header mention is part of the same accepted deviation. Not new (folded into N-stale-comments).
- blind "root_cause_pattern and failure_effect parsed but never consumed" — frozen data-schema fields
  for the [LATER] archetypes; the catalog is the data table (hash-folded for stability). Not a defect.
- blind "cooldown-blocked first saturated bundle suppresses triggers for other saturated bundles" —
  per-pair cooldown + slot-order scan: a blocked pair A masks an unblocked pair B's (b) fallback that
  tick. Attribution latency, not a contract breach; pre-existing semantics the N4 fix didn't target.
  Keep as note (attribution-order subtlety) or reject — leaning keep-as-note.
- tests "Tag-4/8/9 payload pins remain size-only" — re-raise of the settled B2-3 either/or
  (byte-level OR fixed message; the message was fixed). Reject.
- tests "Advisory test gate: PASS" — gate artifact, not a finding.

## Verification evidence (mine)
- odin test core: 119/119 green at 121d8a0 (tracking allocator; crisis tests leak-free).
- tools/harness.sh run: 15/15 demos green at 121d8a0.
- tools/harness.sh drift-check: 104/104 mutations rejected.
- Probe 1 (qos scenario, seed 3003, 1250 ticks): single clean trigger @1200 target=0; no churn;
  active row at end = bundle 0 (lo=0 hi=1 pipe=0, triggered 1200).
- Probe 2 (double-fire regime, pool cap 14, email-BE/streaming-std, narrow host->rt): tick 1200 ->
  2 Crisis_Triggered + 2 active rows (Saturated_Bundle bundle 2 + Pool_Exhaustion NO_BUNDLE),
  same (archetype=0, set_piece=0). E13 breach demonstrated.
- PNG decode (qos/warn/surge 65s + surge 119500ms): ASCII "-" banners, no mojibake; qos names bundle 0
  (pipe 0); warn/surge name bundle 1 (pipe 1); 119500ms = no banner (banner-GONE frame).
- PR head 121d8a0 unchanged during review.
