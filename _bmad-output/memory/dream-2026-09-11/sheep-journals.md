# sheep-journals — dream-2026-09-11

Window: 2026-09-09T01:21Z → 2026-09-11T01:29Z. Sources: gru-journal 09-09
(post-marker sections), 09-10, 09-11; silas-journal 09-09 (post-marker tail),
09-10, 09-11. 09-08 tail-reads: all content pre-marker, nothing undreamed
found. Quotes are verbatim snippets from the journals (journals quote user
rulings verbatim where marked).

## Candidate patterns

### 1. OpenAI-account quota hold → GLM interim regime; identity panes flip, pins go stale (FIFTH cap flavor)
- Examples: [gru-09-10 10:50Z] "User ruling: OpenAI limit hit — finish
  Perkins on glm-5.3, pause ongoing model/asset work, GLM family for all
  other tasks until more OpenAI tokens. Amendment minutes later: image
  generation is NOT paused." Same turn: "Silas died on the cap mid-turn
  (usage limit, failed auto-compaction). Gru revived him IN-PLACE same
  pane/session on zai-coding-cn/glm-5.3 @ max (10:50Z) — /model +
  /thinking max + continue". [gru-09-10 10:57Z] "User: 'silas should be on
  glm5.3 flash.'" + "the USER also flipped GRU to glm-5.3 @ max … watchman
  pins invalid until lift". [gru-09-10 12:2xZ] "User ruled glm-5.3 runs
  max, glm-5.3-flash runs high … incl. relaunch pins and the known
  silas.ts Luna-pin flap during the hold." [gru-09-10 16:5xZ] "Silas now
  on kimi-coding/k3 @ high (user-sanctioned availability)" — interim
  providers churn intra-hold; [gru-09-11 01:00Z] "Silas back on
  glm-5.3-flash @ high."
- Why it matters: extends the cap-incident taxonomy — the cap class is
  PROVIDER-GENERIC (kimi weekly 7-day 09-04 was flavor 4; OpenAI account
  limit 09-10 is flavor 5, killing Astra/Sol/Luna lanes for DAYS). The
  hold has a durable policy file
  (`memory/openai-quota-hold-glm-interim-2026-09-10.md`) with regime,
  exemptions, revive recipe, resume trigger. Code-only exemption
  ([gru-09-10 11:16Z]): "PR #22 changes-requested work is code … →
  glm-5.3 continues it"; image-gen exempt; Astra reserved for 3D craft
  (PP3D #25). Silas model flips during hold = user-sanctioned ad hoc.

### 2. Static-only review ships execution-RED; the bounded-run ("run") grant is the catch net
- Examples: [gru-09-10 18:35Z] "merged main @77a09a4 is execution-RED:
  typed-array mismatch … eaten-checks in the Perkins-r2-fixed
  tooling-contracts gate (11/13 — the phantom-check class,
  execution-only visible) … This is the second proof that static-only
  review ships red — the user's 'run' call vindicated." [gru-09-10 23:45Z]
  post-#28-merge confirm FAILED: "merged-unverified intro test 'empty
  start: pre-installed campus cables hidden' red on main (#27
  runtime-vs-branch world-state difference)" — the disclosed risk
  materialized exactly. [gru-09-11 01:19Z] lighthouse deadlock found only
  on execution: "900s capture run hung at the SAME _stage_lighthouse
  point (logs byte-identical, 101 lines) — deterministic deadlock."
- The grant shape (user "run" word, [gru-09-10 18:31Z]): "three lanes
  only … headless only, ≤300s/entry, JIT entry per job, receipts hashed on
  rows, any failure/drift/diagnostic stops the sequence." Calibration:
  capture bound extended once to 900s ([gru-09-11 01:00Z]) — world-gen +
  13-beat scripts need longer than 300s.
- Why it matters: Perkins APPROVED ≠ execution-green (PR #22 4-round
  loop APPROVED, then bounded run found red; #27 merged with intro tests
  never executed). Every merged-unverified lane owes a main green-confirm
  entry — and that confirm is itself a fix-loop trigger.

### 3. Untracked .import sidecars are LOAD-BEARING; orphan pins measure machine litter (#29)
- Examples: [gru-09-10 22:52Z] "the 11 sidecars were load-bearing import
  remaps for ambient worlds prop/texture resolution (10 script errors +
  49 failures) … Pin unsatisfiable in any used checkout (present = pin
  red; absent = ambient red). Gru's (a) cleanup call was wrong; RESTORE
  ordered". [gru-09-11 23:5xZ → 09-10] "orphan pin PASSES on pristine
  tree — confirmed used-checkout-only defect" (#29 pin bites used
  checkouts only). Lesson propagated forward: #31 fix briefing carries
  "NO blanket sidecar deletion (load-bearing finding)" [silas-09-11].
- Why it matters: gitignored/untracked engine sidecars can be
  runtime-required; deleting "orphans" by name is a regression vector;
  environment-sensitive pins must measure committed-tree state (#29
  amendment). Also: the user's live checkout carries 18 MORE sidecars —
  worktree ≠ user-tree.

### 4. Facts/equality/process-identity guards false-fire on live output drift and locale
- ≥3 concrete flavors this window:
  (a) Policy-facts conflation [gru-09-09]: "wholefacts equality conflates
  ordinary output with policy … CONFIRMS ONLY p2 recent output changed
  during its own polling/reporting" — a 180-line terminal-output blob in
  runtime `facts` made the freshness guard refuse on Silas's own
  progress. Semantic exclusion of ordinary operator progress required.
  (b) Identity-drift monitor abort, cause UNKNOWN [gru-09-09]: "monitor
  abort was owned-test-process identity drift with missing ps-row
  persistence; mismatch cause remains UNKNOWN, not a proven completion
  race" — rejected ps rows MUST be persisted for forensics.
  (c) Locale mismatch [gru-09-10]: "Host LANG=en_GB.UTF-8 versus MCP LANG
  absent … only day-month versus month-day lstart format differed across
  41430/99824/8925. Pair2 child-only LC_ALL=C made all 3 raw stdout
  byte-identical" — fix = per-ps-child LC_ALL=C pinned BOTH producer and
  consumer, expectations regenerated.
- Why it matters: every guard that string-compares whole live process
  state or embeds terminal output will false-fire; comparators need
  pinned locale + normalized fields + persisted rejection evidence.
  Sibling: expired-readiness refusal [gru-09-09] "Silas schedule … was
  785.943548s old vs 180s bound" — corrected sequence is ALL host prep
  first, THEN fresh receipt → immediate launch (no idle-pass reports
  after signing).

### 5. BMad renderer HALT on ambiguous `implementation_artifacts` — recurring, standard recovery exists
- Examples: [gru-09-09] "exited1/HALT: ambiguous `implementation_artifacts`
  at modules.bmm+modules.gds" (pMY bootstrap); [silas-09-10] "Gemini core
  pP9 remains blocked at the mandatory bmad-build gate
  (`implementation_artifacts` ambiguity)"; [silas-09-10] constellation
  review swarm "spawned from the bmad-build halt".
- Standard recovery (proven twice): [gru-09-09] "snapshot installed skill
  into job-local uninstalled `.../workflow-sources/bmad-build` … ONLY
  qualify two shorthand token kinds to full bmm names … ONE corrected
  official renderer bootstrap … no raw fallback". Root cause: BOTH
  implementation_artifacts AND planning_artifacts duplicated bmm/gds with
  identical values; renderer supports FULL `{{config.modules.bmm.*}}`
  names. NEVER edit shared _bmad/skills/symlinks.
- Why it matters: this bit three separate jobs in two days; the recovery
  is now routine and belongs in the store so minions stop halting on it.

### 6. Stage completion must never close a multi-stage creative job (DONE-on-still)
- Examples: [gru-09-09] "Caught operations state error … Silas set overall
  Selva assets row DONE for completed proposal turn despite 55-shot film
  unfinished. Approval relay explicitly corrects to WORKING SAME canonical
  row". Again at CHECK04: "Caught repeated overall-job DONE on a completed
  still … canonical unfinished 55-shot job must be BLOCKED awaiting
  look/next-pass disposition, retain session/worktree/all completed-pass
  evidence, no fake pane pointer or respawn if gone" [gru-09-09 +
  silas-09-09 21:58Z tracking correction].
- Why it matters: recurring Silas-side ledger drift on long creative
  lanes; the correct terminal shape is BLOCKED-for-look with evidence
  preserved, never DONE on a still/proposal.

### 7. Preparation-paperwork vs visible progress — user-facing cadence ruling
- Examples: [gru-09-09] user: "is the music video being worked on. I
  don't see any activities in blender. so wondering." → Gru's answer
  discipline: "yes active asset work, NOT yet shot rendering; short
  background Blender does not animate open window; finished film shots
  0/55". User PROCESS ACK: "well as long as there is real progress being
  made. then it's fine, to do it properly. for less friction down the
  production line." Standing cadence issued: "routine hash/byte/
  finalization receipts stay ledger/evidence/batched, NOT repeated user
  relays … next meaningful updates = usable asset/motion/contact, actual
  shot render, substantive dependency/safety/cost/decision."
- Why it matters: this window's SHA-laden micro-receipt volume drew
  repeated user status questions ("where are we?" ×2, "is the music video
  being worked on", "anything pending on me"). Milestones = "actual
  defects closed, verified usable assets, rendered shots — not escalating
  preparation paperwork."

### 8. Frozen-boundary discipline: versioned rebinding, monotonic deadlines, ticket renewal
- Examples: (a) [gru-09-09] "STOP editing bound master/A-B/scheduling
  briefs for progress after freeze" — BINDING_SHA pins refused
  legitimately-superseded brief hashes; fix = versioned rebinding grant,
  never in-place edits of frozen briefs. (b) [gru-09-10] deadline misread:
  "Silas initially called 00:26:14Z the deadline … monotonic difference
  1800s gives actual deadline 00:56:14Z. Scheduler handoff later ≠ failed
  host preparation … Host deadline bounds PREPARATION, not later
  admission of completed proof." (c) [gru-09-10] ticket deadlock: "every
  entry requires now<=start_before; 180s firstuse anchors ONLY matching
  ticket SHA. NEW tickets are explicitly supported via per-SHA firstuse"
  — the "NO NEW TICKET" operational bound was false; standing renewal
  authority now pre-authorized for unreserved cases.
- Why it matters: the PP3D native-verification machinery (grants,
  tickets, bindings, TTLs) generated a week of stop/disposition cycles;
  these three corrections are the reusable lessons.

### 9. Retained reviewer sessions refuse out-of-original-scope work → clean-session replacement in same pane
- Example: [gru-09-09] "all3 old reviewer sessions refused the broader
  FEATURE/text-to-file assignment under cleanup-only/text-only local
  constraints; 0 layers started" → "ONE clean reviewer-session
  replacement in SAME physical pN0/pP1/pP2, superseding ONLY Gru's prior
  same-session prohibition." Plus launch-envelope catch: "boot_command+
  all3 actual thinking events MAX, not required XHIGH → supported SAME
  session/INPLACE /thinking xhigh correction … no respawn" [gru-09-09;
  silas-09-09 17:13:50Z verified].
- Why it matters: session-local constraints survive their original job;
  assignment changes need either explicit clearance or clean sessions.
  Sibling: thinking-level verification at EVERY launch (Astra/Sol xhigh)
  — booted max twice this window and corrected in-place.

### 10. Perkins loop mechanics under the glm hold: token-mint flake, fallback-comment, dispatched fix row
- Examples: [silas-09-10] "mint succeeded on manual retry → FORMAL
  APPROVED posted as perkins-review[bot] 5168444639 … Mint bug re-flagged
  as owed paneless task row orchestrator-perkins-token-mint-retry-fix
  (signature: worked r1-r3, failed r4 close, succeeded 15min later →
  transient mint bug, no retry; fix = bounded retry + loud logging, keep
  fallback last resort)." [silas-09-10] PR27 r1 posted via
  "sanctioned fallback-comment (perkins-token app absent for mssoka +
  own-PR 422 — the standing tooling gap)". 1302 bursts absorbed twice in
  the PR22 4-round arc. [gru-09-11] WATCH: "Orphaned thread to watch:
  `orchestrator-perkins-to…` row dispatched 14:34Z 09-10, no pane on the
  row — likely the owed perkins-token tooling fix; confirm it is actually
  in flight."
- Why it matters: glm-5.3 proved a full Perkins fallback again (PR22
  4-round arc r1 1B→r2 3B→r3 1B→r4 APPROVED, "all glm-5.3 with 1302
  bursts absorbed"); the mint fix finally has a row — verify it's alive.

### 11. Merge-order gates, user flips order, pre-verdict merges — disclose-then-hold discipline
- Examples: [gru-09-10 23:2xZ] "User merged PR #27 (L1 intro) ahead of
  #28. … Consequence on record: the merged intro tests have never been
  executed … the post-#28 main full-suite green-confirm may trip on them"
  — it did ([gru-09-10 23:45Z]). [silas-09-10] "#28 merged PRE-VERDICT by
  user; r1 informational NEEDS CHANGES — blocker: merge-time restore step
  would restore STALE bytes for 29 drifted canonical files + pull refuses
  → issue #29. STANDING WARNING: never pull the live root past #28
  without an aside copy of .agents/skills (the untrack deleted 1237
  tracked files…)". Held-row shape proven again: [silas-09-10] "Perkins
  r1 row pre-created as HELD with pre-rebase sha bf93d110 marked DEAD
  verbatim + release trigger (rebase lands / PR mergeable → fresh-head
  dispatch)". r4 rebase-delta review discipline: "34/36 files
  byte-identical, twin re-run PASS, count model verified" [gru-09-11].
- Why it matters: belt ordering with gates-on-rows + DEAD-sha holds ran a
  6-PR PP3D wave cleanly; the #28 root-restore hazard is a standing trap
  for every future orchestrator-root pull.

### 12. Multi-day hold = handoff-then-close (mothball) pattern
- Example: [gru-09-10 17:08Z] "User ruling: close the Selva minions, but
  only after each writes a handoff for exact resume; 'Astra won't be back
  for days' … pP5 + pNS each write a durable handoff into
  implementation-artifacts (never worktree-only), Silas verifies
  content/hash BEFORE closing, rows noted paused-by-hold, then panes+tabs
  close. Worktrees stay intact as resume substrate … Resume = fresh glm
  minion from the handoff doc." [silas-09-10] executed: both handoffs
  hash-verified (49f31ada / 3b600ef6), panes+tabs closed, worktrees
  intact.
- Why it matters: clean pattern for provider-cap holds of any lane;
  durable handoff doc is the single resume artifact.

### 13. Numerical false-contact + witness retention (S47 validation chain)
- Examples: [silas-09-09] "Exact failing endpoint native nearest was
  2.6973982585332124 um … while independent binary64 actual evaluated
  triangle-domain distance was 0 m … Classification
  `NATIVE_QUERY_NUMERICAL_FALSE_CONTACT_FAILURE`" — engine native
  closest-point queries produce false contacts at 2um tolerances; the fix
  is an independent binary64 triangle-domain/edge verifier (v2, proven:
  corrected endpoints both 0m). Witness retention: [gru-09-10] "first
  assert discarded non-None `geo.distance(vine,vine,True)` witness;
  historical pair not retained" → rule "retain witness BEFORE refusal";
  recomputed witness then proved a REAL improper vertex-face contact
  (vertex14 strictly inside cap triangle 7179).
- Why it matters: geometry gates at micron tolerances need independent
  double-precision verification AND failure witnesses preserved at the
  refusal site, or failures are undiagnosable.

### 14. Routed-but-unresolved issues stay OPEN; only the routing row is terminal
- Example: [silas-09-10] "created and closed `youtube-channel/issues/2`
  as ISSUE_ROUTED_NOT_FIXED … Routing correction applied: verified GitHub
  issue #2 was CLOSED, reopened it, and reverified OPEN … the paneless
  ledger row remains terminal DONE … its note now explicitly distinguishes
  the open deferred issue from the terminal routing receipt" (Gru's
  wording misread had closed the issue).
- Why it matters: complements the issues-first intake doctrine — the
  ISSUE is the durable work item; the ROW is only the receipt.

### 15. Gemini paid-lane discipline (exact backend, ceilings on rows, disclosed reserves)
- Examples: [gru-09-10] "Latest exact backend ruling: `model=
  'gemini-3.1-flash-image'` … no Pro/preview alias or automatic
  fallback"; "SDK indexed examples use GenerateContentConfig.image_config
  while some current web-guide snippets show response_format;
  implementation must verify actual installed SDK offline, not merge
  incompatible examples." Ceilings: "US$10 total board ceiling … hard
  stop + escalate" [gru-09-10 12:30Z]; final "US$8.90/10" canon locked.
  Skill dogfood verdict: "pNS dogfood-evaluated the packaged helper and
  found it NOT viable for the board expansion (immutable per-attempt
  reserve pin) — expansion rides the proven direct-SDK route" [gru-09-10
  12:4xZ]. Reserve arithmetic: "US$4.063232 reserve … exceeded the 2×v2
  actuals bookkeeping — disclosed, not overspent" [gru-09-10 11:3xZ].
- Why it matters: a repeatable pattern for any paid API lane: exact model
  pin, row-recorded ceilings, hard-stop+escalate, receipts per batch,
  contact-sheet lavish gate; and the skill's per-attempt reserve pin is a
  known design flaw.

## Watch items (single sightings)

- **Selva Blender endpoint switch, cause UNKNOWN**: protected 59538 →
  unprotected 41430 "with unsaved dirty default Scene/frame1/3objects …
  No agent launch/quit/load/import around transition in examined records.
  Cause UNKNOWN" [gru-09-10]. Procedurally resolved by the standing
  Blender ruling, but the silent endpoint swap itself was never explained.
- **Post-approval r5 fix-audit**: "PR26 r5 dispatched earlier (pVF,
  e4480b2 execution-found parse fixes delta-weighted fix-audit)"
  [silas-09-11] — execution-found fixes earned a NEW delta round after
  r4 APPROVED. Watch the shape (approved-then-fixed head re-review).
- **Sensor wrong-repo-root false reads (×2)**: "sensor's 'orphan husk /
  not registered' half was a wrong-repo-root false read
  (/Users/moses/code/my-orchestrator does not exist; worktree WAS
  registered under /Users/moses/code)" [silas-09-10], again on pR6
  ("sensor's husk label again a wrong-repo-root artifact").
- **Shell expansion mangles $-amounts in relays**: "Silas original relay
  'paid /bin/bash' was shell expansion of literal $0" [gru-09-09];
  "Ledger note US / /bin/bash text exposed shell-expansion damage to
  dollar amounts; Silas told to append argv-safe literal correction,
  preserve history" [gru-09-10 10:09Z]; "Relay had a literal //bin/bash
  formatting fragment" [gru-09-10]. Extends the backtick-eating class:
  `$` in herdr payloads needs single-quoting.
- **Heredoc handover failure**: "handover heredoc pattern failed once on
  shell parse (bad substitution) - file-pattern fallback delivered
  cleanly" [silas-09-10] — write briefs/payloads to files.
- **Accidental native run, self-caught + disclosed**: "one accidental
  native run after push (unittest mis-inclusion, ~49s of short-lived
  godot probes, all clean exits … self-caught, PR comment 5618179498 +
  ledger) … Self-caught + disclosed = the healthy pattern; no action"
  [gru-09-10 11:5xZ].
- **Renderer diagnostics at capacity void integrity claims**: "237
  shadow-buffer-full diagnostics, usage2223..2237/capacity2048 … exit0
  was NOT renderer-integrity PASS. No real healthy batch throughput
  measured; errored single-frame extrapolation cannot admit a shot"
  [gru-09-09 CHECK03].
- **Overrun disclosure, never retroactive compliance**: "final sealing at
  1804.853s exceeded the host grant by 4.853s … Preserve this overrun, no
  retroactive within-budget claim" [gru-09-09].
- **Shutdown investigation limits (issue #23)**: "NO holder/root cause
  identified and NO gameplay consequence demonstrated … arithmetic 73 is
  not ownership mapping; grep-paired new/free ≠ lifecycle proof" [gru-09-10
  GLM erratum]. 73 ObjectDB/61 orphan StringNames, owner UNKNOWN.
- **Observer infeasibility finding (Pi platform)**: "Public additive
  extension cannot distinguish initial custom pending from empty or
  intercept sibling pi.sendMessage … hasPendingMessages excludes
  custom/compaction" [gru-09-09] — external pending-control visibility is
  a real gap; Gru's lesson: "our overambitious requirement … has turned
  two editor checks into integration detour. Recommend NOT patching Pi."
  Plain supervised terminal with direct Ctrl-C was the user-approved
  substitute.
- **Constellation seam-curtain technical class**: r1 "B1 seam-curtain
  class (pointwise map_pos, no seam cut — nothing written would catch it;
  numeric-twin verified)"; r2 fixes "stale lo[i] override on exact seam
  verts (96 curtain triangles full map width; fix lo[i]=NaN) + morph
  cache Nil ARRAY_INDEX for SurfaceTool meshes (planet vanishes at
  flatness>0; fix st.index())" [silas-09-10]. Equirect seam vertices +
  SurfaceTool morph caches — candidate for minion field notes (game-dev).
- **oEmbed for reference verification**: "YouTube oEmbed returned
  verified title … Metadata confirmation is not watched-video evidence"
  [gru-09-10] — title/channel verify via oEmbed; claims of viewing must
  be separated from metadata.
- **Compaction/session-change relay survival**: "Fresh-session
  reconciliation showed the queued relay did not survive Gru's session
  change. Re-sent to new w85:p1 … and verified it in the pane" (09-08
  tail, pre-marker but same window's mechanics); "grep-flush artifact
  noted - content beats grep" [silas-09-10]; flush-race re-grep held
  ("0-hit first grep, 1-hit on re-grep - no resend").
- **User browses wrong repo**: "the not-found confusion was them
  browsing the regular packet-plumber (v2/Odin) repo instead of
  solarity-services/Packet-Plumber-3D" [gru-09-10 16:5xZ].
- **Replay determinism**: "two BYTE-IDENTICAL replay passes" [gru-09-09]
  — deterministic replays are cheap regression anchors.
- **PP3D observation instrumentation proof ≠ fix**: "52 mock cases are
  instrumentation proof, not a fix" [gru-09-10]; "Mock equivalence/AST
  identity is NOT ownership repair or operational launch binding."
- **Stray keystrokes**: "one Gru /thinking max landed in the dead-pane
  zsh window (harmless)"; "A user-typed edge-case-hunter launch (Astra,
  --no-extensions…) appeared in the pane trail — presumably cap-failed"
  [gru-09-10 10:57Z].

## User rulings captured (verbatim)

1. **Silas Luna xhigh** (09-09): "let's make silas model luna be on
   xhigh as well. rather than on max." → PR24 (my-orchestrator), merged.
2. **Both-lanes resume + permission-loop rebuke** (09-09): "said we need
   to work on both, why would i need another go, to have both in
   progress?" + answer "both" — internal holds must not become permission
   loops.
3. **Process ack** (09-09): "well as long as there is real progress
   being made. then it's fine, to do it properly. for less friction down
   the production line."
4. **PP3D guard fix go** (09-09): "go with your recommendatipn" (sic) —
   supersedes a standing STOP for the named scope only.
5. **Plain supervised terminal approved** (09-09): user said exactly
   "approved." after "i don't understand" → simplification — control
   contract change (direct terminal stop instead of queued chat STOP).
6. **PP3D comparisons parked** (09-09): user chose "A" (park the
   BEFORE/AFTER editor comparisons; keep whole-tree guarantee).
7. **PP3D feature-only resume** (09-09): "yes. feature completion for
   now".
8. **CHARGE quality floor** (09-09): "would also prefer at least this
   quality https://www.youtube.com/watch?v=UXqq0ZvbOnk&t=99s and
   https://www.youtube.com/watch?v=pNPPVCPuWG8 we don't want some cheap".
9. **Full-film production** (09-09): "this looks good. lets create the
   full music video. the timing is good enough to proceed to full
   production."
10. **U1 policy approved** (09-09): "yes" — durable scope authorization
    vs expiring readiness distinction (dream-2026-09-09 U1; PR25 merged).
11. **Online street assets / pass03** (09-09): "go with your
    recommendation. also the road leading to no where? the minion should
    be able to get assets online. esp for the street if it helps. the mcp
    has tools. for poly and sketchfab" — free lawful assets OK; paid
    still needs explicit approval.
12. **GLM pure-code matrix PROPOSED (never confirmed; superseded for
    hold duration)** (09-09/10): "so going forward. if there are tasks
    that is pure code that doesn't need 3D assets. let's use glm5.3. that
    should be the only change for now. every other model for other roles
    remain the same. create a table and verify before making the
    changes." + "glm should be at the highest thinking level." +
    amendment "even this. 🛠️ Other non-3D, non-code minions/helpers
    should be glm."
13. **GLM shutdown investigation** (09-09): "ok. let's explore that. use
    glm5.3 for that, we don't need to have vision, or create a 3d asset
    to explore that right?"
14. **Gemini initial spend** (09-10): "just generate what we need.
    approved." (US$5, 2-3 images).
15. **OpenAI quota hold** (09-10 10:50Z): OpenAI limit hit → finish
    Perkins on glm-5.3, pause model/asset work, GLM family for other
    tasks; amendment: image generation NOT paused (no 3D modeling
    quality needed).
16. **Silas on flash during hold** (09-10): "silas should be on glm5.3
    flash."
17. **Code-only exemption** (09-10): "glm5.3 is capable of finishing
    this off" (Gemini skill core) + PR22 code work continues on glm.
18. **Standing Blender access** (09-10): "go ahead, blender is for you
    to use. no permission needed. to access blender. I'll rather get
    notified when i need to review an output please" — standing
    authority; durable at `memory/blender-access-policy-2026-09-10.md` +
    canon PR26.
19. **Thinking levels under hold** (09-10): glm-5.3 = max,
    glm-5.3-flash = high (verified already-matching; no registration
    patch).
20. **Concurrency reversal** (09-10): "pleasse dont do that. my system
    can handle both" — PP3D user play + Selva native queue concurrent;
    durable at `memory/pp3d-selva-concurrency-policy-2026-09-10.md`.
21. **PP3D user look → publish** (09-10): "looks good to me. let's
    commit and create a PR for this" (context-verified = PP3D).
22. **Board expansion** (09-10): "widen." (US$10 ceiling) → pass-1
    realism ruling (real lived-in city) → pass-3 dancing/crowd ruling
    (inhabited with dancers, supersedes no-crowds) → canon locked
    "looks good. approved" (54 boards, US$8.90/10).
23. **L1 intro phase B** (09-10): "maybe the first 2 buildings spawn
    with routers and the next 2 for level 1 do not." — sites 1-2
    (UCLA/SRI) pre-equipped; 3-4 bare + inventory drag-to-place.
24. **Bounded godot execution** (09-10 18:31Z): user answered the
    standing question: RUN authorized (three lanes, headless, JIT,
    stop-on-surprise).
25. **Parked-editor disposition** (09-10 15:54Z): "Archive + close."
26. **Constellation transition** (09-10 16:29Z): globe⇄flat = just a
    smooth zoom-out carrying the flatten morph; smooth + interruptible;
    nothing complicated.
27. **CHECK05 look verdict** (09-10, lavish uid3): "Keep the new street
    layout; refine plant form, leaf finish and lighting next."
28. **Selva minions closed for multi-day hold** (09-10 17:08Z): close
    after verified handoffs; "Astra won't be back for days."

## Pruning candidates (store claims contradicted/superseded)

1. **AGENTS.md line ~1617: "Luna … @ max is Silas/COO's route"** —
   superseded twice: user ruling 09-09 (Luna xhigh, PR24 merged:
   "let's make silas model luna be on xhigh as well. rather than on
   max.") and the hold flip (Silas on glm-5.3-flash @ high since 09-10
   10:57Z, with brief k3 interlude). Amend: Luna xhigh is the post-hold
   pin; hold overrides live. Related: line ~704 "Astra/Sol require
   xhigh, Luna max" — the "Luna max" tail is stale.
2. **AGENTS.md "CURRENT MODEL POLICY (2026-09-07 user ruling — GPT
   chain) … kimi/glm/deepseek chains are RETIRED from new dispatches"**
   — temporarily superseded by the OpenAI hold: glm-5.3 IS the dispatch
   chain for code/general work during the hold (user-ruled), image-gen
   exempt, Astra = 3D-craft only (waiting). Do not delete the GPT-chain
   base — add the hold interlude with its policy-file pointer and
   "supersedes the pending GLM matrix proposal for its duration only".
3. **AGENTS.md "Shared Blender: a reservation or handshake is not
   live-state clearance"** (2026-09-09 gotcha) — the permission-ceremony
   half is retired by the standing Blender ruling ("no permission
   needed. to access blender"); keep the live-state-forensics core
   (fresh owner/dirty/frame checks before restart/mutation still
   applied all window — e.g. the locale/endpoint sagas). Qualify, don't
   delete.
4. **AGENTS.md line ~876: "the Perkins tooling still owes the
   badge/token-mint fix task"** — status moved: paneless row
   `orchestrator-perkins-token-mint-retry-fix` dispatched 14:34Z 09-10
   (Gru 09-11 flags it orphaned — no pane on the row). Update the claim
   to "dispatched, verify alive".
5. **Watchman/night-watchman model pins** — store doctrine assumes the
   pinned identity models; during the hold "watchman pins invalid until
   lift (Silas relaunch = glm-5.3-flash, Gru = glm-5.3)" and the
   "silas.ts Luna-pin flap" is a standing trap. Any store text implying
   watchman relaunches land on Luna/GPT needs the hold caveat.
6. **Kimi k3 weekly-cap doctrine (09-04 addendum)** — generalize: cap
   walls are provider-generic; the 09-10 OpenAI account limit is the
   same recovery shape (interim provider + in-place revive + durable
   hold policy + duration-limited supersede of model policy).

## Notes for Bob

- The window is dominated by two LANE sagas (PP3D editor-shutdown +
  native-verification chain; Selva CHARGE quality ladder + Gemini
  boards). Most of it is lane canon already preserved in
  implementation-artifacts + briefings — resist promoting saga detail to
  the store; the ops classes above are the store-worthy residue.
- Three durable policy files were created this window and the store
  should POINT at them, not duplicate: `memory/
  openai-quota-hold-glm-interim-2026-09-10.md`,
  `memory/blender-access-policy-2026-09-10.md`,
  `memory/pp3d-selva-concurrency-policy-2026-09-10.md`.
- Naming collision to avoid in store edits: **my-orchestrator PR26
  (Blender canon) vs PP3D PR #26 (constellation view)** — always
  qualify by repo.
- In-flight at dream dispatch (09-11 01:29Z): lighthouse-staging-fix
  (pVE, #31), PP3D PR #26 r5 (pVF), PR #30 user-merge-pending = last
  main-green gate, lanes 2-3 released pending #30 merge. The hold is
  STILL LIVE — model-policy store edits must read as
  duration-limited.
- The strongest NEW store candidates by evidence count: #2
  (static-review-ships-red, 3+ sightings incl. #31), #4 (guard
  false-fires, 3 flavors), #5 (BMad implementation_artifacts, 3 jobs),
  #1 (hold regime), #3 (load-bearing sidecars, with forward
  propagation into #31 briefing as proof of learning).
- PR22's "exit survivor counts repeat in retained runs" + "no holder
  identified" and issue #23 remain open questions — do NOT let any
  store edit imply the shutdown saga was resolved; it was archived
  (parked), not fixed.
