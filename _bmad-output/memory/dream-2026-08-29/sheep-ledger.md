# Sheep shard — ledger events (dream-2026-08-29)

Read: `ledger events 200` — full window 2026-08-27T10:29:07Z (dream-2026-08-27
close) → 2026-08-29T21:30:44Z (dream-2026-08-29 working); 200 events reached
back to 08-26T18:16Z, so the post-marker window is complete (no deeper paging
needed). `ledger show` run on: packet-plumber-v2-mechanics-the-box,
box-crash-third-spawn, lang-safety-research, viscomm-shape-vocab,
mechanics-quinn, viscomm-regression-audit, congestion-read-a1,
arch-egress-migration (verified pre-marker, excluded), orchestrator-checkpr-
review-recency, dream-2026-08-29.

## Candidates

### C1 — Blind lens = the truncation canary on flash-tier Perkins rounds (retry once on a fresh pane, else 6/7 degraded-disclosed)
- Example: packet-plumber-v2-look-zoom-language-perkins-r1, 2026-08-27T17:23:09Z —
  "blind lens failed both attempts (glm-5.3-flash long-context truncation) —
  the diff was read by all 6 remaining lenses" (degraded-disclosed, APPROVED).
- Sightings: 7 rounds / 4 jobs / 2 days — look-zoom r1 (2x truncated pre-write);
  congestion-read-a1 r1 08-28T01:09:33Z (blind ×2 mid-thinking stream stalls →
  retried once on a fresh pane → recovered 7/7); mechanics-the-box r1 08-28T08:53:43Z
  (blind output-cap 2x → 6/7), r3 08-28T13:11:45Z (blind failed 3x incl 1302s → 6/7),
  r4 08-28T18:02:56Z (security+blind one retry each → 7/7 landed), r5 08-28T19:23:06Z
  (blind re-dispatched once after truncation → 7/7); box-crash r1 08-28T22:18:19Z
  (blind failed 2x on output-length → 6/7). The blind lens reads the whole diff
  (most context) so it caps FIRST on big diffs; on flash-tier rounds this is the
  norm, not an anomaly. Retry-once-fresh-pane recovers ~half; the rest close
  6/7 degraded-disclosed with zero verdict loss.
- Novel? Novel — distinct from the empty-lens doctrine (3-byte empties) and the
  429-degraded doctrine (this is output-length/truncation, not 429, not empty).
- Target: AGENTS.md (Perkins round ops; the code-review skill could also carry it).

### C2 — Connection-class round-main deaths are a DAILY episodic wave on the flash tier; pre-wave death salvages from the saved canonical diff
- Example: packet-plumber-v2-mechanics-the-box-perkins-r5, 2026-08-28T18:58:14Z —
  "main died 4x errored turns (connection class - 5th today) before any lens JSON
  landed (only diff patches saved); ONE continue revived it — the wave
  starts/restarts from the saved canonical diffs."
- Sightings: 6 events / 2 jobs / <24h (08-28) — congestion r1 00:36:57Z (6/7 JSONs
  landed), mechanics r1 08:21:19Z (~03:59Z death, 6/7 + drafted pr-body.md), r3
  12:33:17Z ("3rd today"), r4 17:32:40Z ("4th today"), r5 ("5th today"), congestion
  r2 09:34:21Z (died pre-verdict → swept moot on the user merge). Every live case:
  ONE continue, zero rounds lost, durable artifacts carried. New facets vs the
  08-27 addendum: (i) episodic PER-DAY concentration on the flash tier (counted
  "Nth today" in-row); (ii) a death BEFORE the wave still salvages — diff.patch /
  diff-code.patch on disk restart the wave.
- Novel? Extends AGENTS.md "CONNECTION-class waves" (2026-08-27 addendum (d)) —
  propose as an addendum there.
- Target: AGENTS.md.

### C3 — A carried blocker closes in BYTES, not claims: blob forensics vs merged-tree warm bytes + blessing-machine convention census + carried-blocker escalation flag
- Example: packet-plumber-v2-mechanics-the-box-perkins-r4, 2026-08-28T18:02:56Z —
  "B2 CARRIED (11 named goldens still stale pre-#106 bytes; census: 116/117 swapped
  convention, ZERO warm bytes absorbed; the claimed one-machine settle unsupportable
  against committed bytes)"; parent row 18:04:24Z — relay "bytes-not-claims, find the
  re-bless pipeline defect" + "FYI to Gru with the carried-blocker pattern flag".
  Closed at r5 19:21:39Z: "B2 ANSWERED — 86/117 byte-identical to #106 warm bytes,
  0 stale, 0.00% swap-signature, full-corpus 50/50 reproduction on the review machine".
- Sightings: 3 rounds (r3 13:11:45Z "Root cause census: TWO blessing machines with
  R/B-swapped conventions blessed the two lanes" → r4 carried → r5 closed), spanning
  PRs #106/#107; 1 day. Craft laws: (i) corpus convention census (swap-signature %)
  is a re-bless verification leg; (ii) ONE blessing machine per corpus — provenance
  matters, verify against the MERGED tree's warm bytes, never the run log; (iii) a
  blocker carried ≥2 rounds earns an explicit carried-blocker pattern-flag escalation.
- Novel? Novel facets on top of the existing re-bless doctrine (field-notes golden
  discipline covers byte-verify/fold-check/cause-document, but NOT convention-swap
  census, blessing-machine provenance, or the carried-blocker escalation).
- Target: minion-field-notes.md (craft) AND AGENTS.md (escalation shape).

### C4 — MEGA-DIFF fix rounds are mega too: the two-class protocol applies to fix-deltas, with blob forensics as the mechanical leg on re-bless bulk
- Example: packet-plumber-v2-mechanics-the-box-perkins-r4 dispatch, 2026-08-28T13:54:48Z —
  "FIX-DELTA 88825L (0431813..6e3a3c8) = mostly the ONE-MACHINE golden corpus
  re-settle; MEGA-DIFF chunking: full lens on code chunk, mechanical blob
  verification on PNG bulk (convention census + black-frame scan + pulse-presence
  on the 11 named beats)"; verdict 18:01:07Z: "651L code chunk full lens wave; 88k
  T1 re-bless mechanical (fold-check PASS = catalog_hash fold alone)".
- Sightings: 2 — r4 delta 88825L (13:54:48Z) and r5 delta 88689L (18:38:54Z,
  "CRITICAL QUESTION: do the 11 named goldens NOW byte-match the merged tree
  (blob-forensics FIRST)"). On a mega-diff PR the rework push is dominated by the
  re-blessed corpus, so a "fix-delta" is still 88k lines; the mechanical leg for
  byte-claim blockers is blob forensics (census + byte-diff), not spot-check.
- Novel? Extends the AGENTS.md MEGA-DIFF protocol (2026-08-27) which says "r2 then
  runs fix-delta-weighted (spot-check)" — the re-bless-heavy fix round needs MORE
  than spot-check on the bulk.
- Target: AGENTS.md (MEGA-DIFF addendum).

### C5 — Flag-ON coverage: ruling wiring + debug-override legs + feature-flagged demos ship with ZERO coverage unless the flag-on surface is explicitly gated
- Example: packet-plumber-v2-box-crash-third-spawn-perkins-r1, 2026-08-28T22:18:19Z —
  "class CI-invisible because zero golden demos run box-on (playtest was the only
  box-on × telegraph-lead surface)" — the 3rd-spawn SIGABRT reached the user's
  playtest with no gate ever exercising the Box.
- Sightings: 3 / 2 jobs / 1 day — mechanics r3 08-28T13:11:45Z blocker 4 "ruling-1
  wiring (era-1 start + 6.2 gate) ZERO coverage"; mechanics r4 08-28T18:02:56Z B5
  "era-wiring row ships PP_DEBUG RED — gate the ==1 assertion on !PP_DEBUG"
  (debug-override leg); box-crash (above). A user ruling that changes shipped
  defaults needs its wiring covered in EVERY configuration the gates build
  (default AND debug override), and a flag-gated feature needs ≥1 flag-ON demo/gate.
- Novel? Novel — sibling of the existing COVERAGE-GAP note (per-component assertion
  mirroring, field-notes ~L885); this is the flag-on/configuration dimension.
- Target: minion-field-notes.md.

### C6 — Falsify-the-premise as a first-class briefing shape: a disconfirmed lead hypothesis with the real chain is the deliverable; cross-job evidence relay feeds it
- Example: packet-plumber-v2-box-crash-third-spawn, 2026-08-29T00:18:12Z — "loop
  closed at r1 with the briefed hypothesis disconfirmed on evidence" (briefing's
  2→4-grow hypothesis disconfirmed: "box_grow is once-at-enable, idempotent"; real
  chain = shadow_clone value-copy aliasing the LIVE heap allocator → double free at
  topology.gen re-predict; both .ips explained; mutation gate re-run machine-proven
  RED→GREEN; class sweep "55 deletes = 53 clone lines + 2 zeroed").
- Sightings: 2 jobs / 1 day — box-crash (above) + packet-plumber-lang-safety-research
  08-28T20:25:30Z dispatch ("lead question = falsify-the-premise") answered
  23:45:31Z "on the REAL crash root cause (shadow_clone aliasing; folded in via
  steering relay)" — the sibling job's Perkins verdict was relayed INTO the live
  research lane as primary evidence mid-flight (22:18:47Z).
- Novel? Novel as a named briefing/craft doctrine (the mid-flight-amendment and
  cross-job-flag doctrines exist; the hypothesis-plus-mandated-falsification shape
  and the verdict→research evidence relay do not).
- Target: either (briefing craft → AGENTS.md; minion craft → field-notes).

### C7 — User-ordered pane cull closes conversation lanes: the durable record is the amendment surface (future amendments = NEW session from the record)
- Example: packet-plumber-v2-mechanics-quinn, 2026-08-29T01:48:42Z — "LANE CLOSED by
  user-ordered pane cull: The Box SHIPPED (#107 merged), design record durable at
  mechanics-quinn-2026-08-27.md; pane closed; future amendments = new session
  launched from the record" (supersedes the same row's 08-28T00:35:10Z "PANE STAYS
  OPEN by design (ruling amendments) — never sweep w85:p3P").
- Sightings: 2 lanes, 1 order — mechanics-quinn + viscomm-shape-vocab both culled
  2026-08-29T01:48:42Z; stale-tick echoes classified note-only 01:50:15Z ×2 with
  pane/tab NULLed post-cull. Shape-vocab had ruled + de-scoped 20:01:01Z with the
  pane kept "OPEN amendment-ready (quinn precedent)" — the cull retired that
  precedent ~6h later.
- Novel? Novel facet on the interactive-design-session doctrine (AGENTS.md, 2026-08-27):
  the close shape was missing — this adds it (user cull; record = amendment surface).
- Target: AGENTS.md (interactive-session addendum).

### C8 — Skills dedup sweep (user-ordered): repo .agents/skills snapshots drift from canonical; census → note → rm; LIVE main checkout = SWAP-NOW symlink + REMOVE-LATER at last-lane close (deferred cross-row trigger)
- Example: packet-plumber-v2-viscomm-shape-vocab, 2026-08-28T23:47:25Z —
  "packet-plumber/.agents/skills (stale Aug-5 snapshot) MOVED to
  .agents/skills.stale-aug5 + replaced with a symlink to /Users/moses/code/.agents/skills
  — live sessions (Sally) resolve through the link to canonical, zero breakage…
  NOTE: the symlink must ALSO be removed (not just the dir) at lane close — it
  points at the orchestrator root's working tree." Final step UNBLOCKED at the
  2026-08-29T01:48:42Z cull.
- Sightings: 3 repos + 2 row-notes + 1 execution / 1 day — kids-finlit-game-brainstorm
  08-28T20:28:55Z (stale Jul-28 snapshot, 71 only-in-repo entries); packet-plumber-
  ue-architecture-slice-map 20:28:55Z (byte-clean subset, 6 real dirs where canonical
  has symlinks); packet-plumber main checkout (SWAP-NOW above). The DEFERRED SWEEP
  TRIGGER was written on BOTH live rows (lang-safety + shape-vocab 20:29:07Z) with
  LAST-close semantics ("sweep at whichever close-out lands LAST; before rm, capture
  'Only in repo' list to a ledger note") and fired correctly at the last close.
- Novel? Novel — skills-drift, the census-before-rm procedure, the symlink swap for
  a live checkout, and the last-lane-close deferred trigger are all unrecorded.
- Target: AGENTS.md.

### C9 — PR-body / commit-message over-claims are a serial Perkins warning class (claims inflation compounds rounds)
- Example: packet-plumber-v2-mechanics-the-box-perkins-r4, 2026-08-28T18:01:07Z —
  "W4 serial (4 new over-claims: B2/B3/one-machine-50-50/econ-CI)" alongside
  "W3 STILL OPEN (econ-check in no CI, body claim false)".
- Sightings: 3 rounds, 1 job, 1 day (concentrated) — r3 13:11:45Z warnings
  "PR-body over-claims x3 + stale econ table" (relay included "PR-body honesty
  corrections"); r4 (above); r5 19:21:39Z "disclosure degree inflated (W4b pattern)".
  Once an over-claim is found, Perkins re-verifies EVERY prose claim in the next
  round — the PR body becomes a verify-target, not a narrative.
- Novel? Novel as a named class (the bytes-not-claims relay in C3 is the ops side;
  this is the minion-facing prose-honesty side).
- Target: minion-field-notes.md.

## Anecdotes (single-sighting — watch items)

- **PR-body DESIGN FLAGS as the async user-ruling intake** — mechanics-the-box
  08-28T03:51:43Z: "THREE DESIGN FLAGS for the user (in PR body, not unilateral)"
  (era start / golden source of truth / saves disposable) — all 3 ruled 08:50–08:55Z
  and folded into the rework push. Sibling of the lavish decision-menu and in-pane
  fork shapes; the PR-body variant needs no session. Watch for a 2nd sighting.
- **Committed evidence crops IN THE PR = the user-eyeball delivery vehicle** —
  congestion-read-a1 08-28T09:14:49Z: "peak-vs-trough corridor crops COMMITTED at
  z1.0/1.4/2.0 for the user eyeball gate"; user merged #106 on that gate 09:34:34Z,
  pre-empting Perkins r2 (moot sweep — already doctrine; the eyeball-gate flavor
  and the committed-crops vehicle are new).
- **Minion self-model-switch mid-job → status flicker burst + cache re-bill** —
  look-zoom-language 08-27T14:12:10Z: "idle/done/idle in 1min = the minion's own
  model switch to glm-5.3-flash applying (config auto-set at its turn boundary,
  246k cache re-bill on switch)" — classify, no action. Watch: does the flicker
  recur on every self-switch?
- **Interactive-lane dead-pi relaunch mid-conversation** — mechanics-quinn
  08-27T19:24:46Z: pi died ~18:36Z in the herdr server outage (18:41–19:11Z),
  "nobody watches minion panes", dead ~47min; relaunched same pane, opening
  re-presented from a recovered-opening brief file. Watch item: minion/conversation
  panes have no night-watchman coverage during a herdr outage.
- **Named trigger released early by user ruling** — viscomm-shape-vocab
  08-28T12:36:00Z: "RELEASE NOW - merge-waiting defeats its own trigger". A held
  row's named trigger yields to a user ruling when the wait defeats the trigger's
  purpose. Single sighting.
- **Read-only audit while the main checkout is HELD** — viscomm-regression-audit
  08-27T19:43:37Z: detached worktree at the AFTER sha + "BEFORE sha via minion-owned
  scratch worktree at 088cf00" because mechanics-quinn held the main checkout.
  Inverse of the 08-27 read-only-main-checkout routing; single sighting.
- **URGENT lane economics: fun-test gate fired as a bug-surface** —
  box-crash-third-spawn: user playtest crash → URGENT dispatch 08-28T20:17:05Z →
  PR 21:17Z → Perkins r1 APPROVED 22:18Z → merged 08-29T00:18:12Z (~4h). The
  user-held fun-test gate surfaced the CI-invisible class exactly as designed.
- **User-ordered MODEL EXCEPTION for a research lane** — lang-safety-research
  08-28T20:25:30Z: "glm-5.3 PRO (+thinking max) for the minion AND every spawn,
  explicitly NOT flash". Research-grade lanes can be ruled onto the reasoning tier
  by exception; the spawn-pin discipline still applies.

## Already-covered confirmations (no proposal)

- **shadow_clone aliasing class RECURRED** on the #107 Box arrays — the 2026-08-26
  field-note ("every new step()-touched dynamic array must be added to
  spawn_fx.odin's shadow_clone clone list") predicted it; box-crash proved it.
  New facets for that note if touched: double-free via topology.gen re-predict;
  both .ips explained; the clone-list census sweep ("55 deletes = 53 clone lines").
- **Notification compliance gap, 3rd sighting** — lang-safety-research 08-28T23:45:31Z
  ("minion skipped herdr notification show, 0 results in session — Silas fired it").
  Fully covered by the 08-07 gotcha + 08-15 addendum.
- **Moot-on-merge / sweep-stale-on-rebase / sensor-echo twins / round-debris
  detection-only** — congestion r2 moot sweep 09:34:21Z; mechanics r2 swept stale
  09:34:52Z ("a round never re-targets"); echo-twin notes ×6; r5 debris flag
  19:21:57Z (leftover mm-lenses-r2 tab, detection-only) + 7 orphaned #106-r2 lens
  panes cleared at the r5 close-out (cross-round debris outlives its sweep).
- **arch-egress-migration**: all activity pre-marker (merged 08-27T09:37:35Z) —
  excluded, already dreamt.
