# 2026-08-25 — pi/herdr restoration handover (from the DSH interlude)

Context: orchestration ran in DSH for ~1 day (2026-08-25) after the pi pivot.
User verdict: DSH's Silas lane cannot accept new tasks mid-turn, and its
workflow fan-out blocks Gru's turn — the user cannot converse while ops run.
Reverted to pi/herdr. Everything below is the live state at handover (~16:55Z).

## What was restored

- `my-orchestrator` re-cloned from origin (main @ ac9e0b4).
- `~/code/AGENTS.md` = the pi-era doc (from `dsh-orchestrator-setup/AGENTS.md.pre-dsh`).
- `~/code/bin` → `my-orchestrator/bin`; `~/code/.agents` → `my-orchestrator/.agents`;
  `~/code/.pi` → `my-orchestrator/.pi` (gru.ts / silas.ts / nefario-watch.ts intact).
- Ledger: the real 490-row DB moved back to `~/code/_bmad-output/orchestrator.db`
  (the one at that path was an empty shell, no jobs table — backed up as
  `orchestrator.db.empty-shell.bak`). Perkins rounds, field-notes, memory,
  quota-regime copied back; DSH-era briefs archived at
  `_bmad-output/briefs-archive/`.
- `dsh-orchestrator-setup/_bmad-output/` is ARCHIVED (see its ARCHIVED.md) — do not write there.
- herdr server never died (PID 83927). Night-watchman was in the launchd penalty
  box (program path vanished during the pivot); kickstarted back to exit-0 health.

## Runtime state at handover

- **Silas (pi) is ALIVE and mid-flight** on `silas-perkins-r1-completion`
  (Perkins r1 for PR #99, packet-plumber tie-deconflect): validating the 6 lens
  JSONs on disk, re-dispatching the missing codebase lens, then verify →
  consolidate → post verdict via perkins-token → ledger. Brief:
  `_bmad-output/briefs-archive/silas-perkins-r1-completion.md`.
  DO NOT double-dispatch that row.
- **Gru (pi) relaunched** on zai-coding-cn/glm-5.3 --thinking max in w85:p1.
- Provider regime: kimi-coding/k3 is 403 (billing-cycle quota wall, same as the
  DSH era); glm-5.3 probed OK via the env-cleared pi probe. Reasoning chain per
  playbook: k3 → glm-5.3 → HOLD. Everything rides glm-5.3 until k3's cycle flips.
- Orphan sweep done: stale lldb debug process (font-overhaul era) killed.

## Open board (ledger rows)

| Row | Status | Note |
|---|---|---|
| packet-plumber-v2-viscomm-tie-deconflect | in-review | PR #99 open vs v2; CI green; awaiting Perkins r1 verdict |
| packet-plumber-v2-viscomm-tie-deconflect-perkins-r1 | working | Silas completing (see above) |
| dsh-client-plugin-orchestrator-dashboard | in-review | PR #1 open (dashboard plugin) |
| dsh-dashboard-perkins-cap | dispatched | needs re-dispatch on pi lane (PerkinsRows slice(0,10) → cap 2 done rows); brief in briefs-archive |
| packet-plumber-v2-viscomm-gauge-telegraph | blocked | blocked_by tie-deconflict |
| packet-plumber-v2-viscomm-crisis-duck | clarifying | needs USER design ruling |
| packet-plumber-v2-viscomm-shape-vocab | blocked | era-gated |

- Human merges PR #99 and dashboard PR #1 — never us.
- Fixes from the r1 verdict relay to the tie minion, then r2 at the new sha.

## DSH interlude lessons worth keeping

- The DSH experiment's failure mode (for the record): one background ops agent
  cannot be interrupted with new work mid-turn; foreground fan-out starves the
  user lane. pi/herdr's persistent interleavable sessions remain the fit.
- The Perkins 7-lens / skill-file-first doctrine amendments made during the DSH
  day are real and carry over: load `~/.agents/skills/code-review/SKILL.md`
  (now correctly symlinked), run ALL lenses with verbatim briefs, blind =
  diff-ONLY. The AGENTS.md.pre-dsh already carries the 08-23-era lens doctrine;
  the 7-lens emphasis from 08-25 stands.

— the DSH orchestrator session (handing over and standing down)

## Post-handover fix (Gru, ~17:0xZ)

- `docs` symlink was MISSING from the restoration set (bin/.agents/.pi were
  symlinked, docs wasn't) — `/Users/moses/code/docs/` didn't exist, so the
  PLAYBOOK constant in gru.ts + silas.ts AND the AGENTS.md references were
  all dangling. Created `~/code/docs -> my-orchestrator/docs`. One canonical
  copy, zero duplicates.

## Layout inversion executed (user ruling: "the real origin should be in ~/code")

- ~/code IS the my-orchestrator checkout now: killed Silas (state on disk),
  parked watchman, removed the 4 root symlinks, rsync'd real content in
  (live wins), moved .git to root, deleted the nested clone. Sync commit
  5b5de85 pushed. Watchman plist path unchanged (resolves to real file now).
- Restoration gaps closed by the move: docs/ (this file's earlier symlink fix
  superseded), managed-repos.txt (intake allow-list), README.md, test/, and
  Silas's journal re-homed (it had been landing in the clone via symlink
  resolution — state was splitting).
- Silas rebooted on real paths (session 16-46-14Z), handover verified in
  session jsonl. herdr agent-wait false-negatived BOTH boots (registration
  race) — pane-forensics verification (process + session file) is the
  reliable check, not the wait.

## DSH dashboard plugin abandoned (user ruling, ~18:0xZ)

- User closed PR #1 (dsh client dashboard plugin) unmerged at 16:22Z; ruling:
  abandon the plugin work. Silas marks rows done-unmerged, archives briefs,
  sweeps debris. The DSH interlude is now fully closed — client, plugin, all.

## Night-watchman false alarm fixed (~17:1xZ)

- Symptom: "Gru tab MISSING" notification every 30 min since ~16:10Z. Root
  cause: config expects tab label `Gru` (capital, the 08-21 setup), live tab
  is `gru` (lowercase, from the 16:00Z user relaunch) — resolve_tab is
  case-sensitive jq exact match → permanent miss. silas immune (key==label).
- Fix (e5838c1): case-insensitive fallback in resolve_tab — exact match
  first, unique case-insensitive match second, ambiguity (2+ variant tabs)
  still warns (never guesses). Verified: --self-test PASS incl. live
  resolution (gru w85:t1 ALIVE), --dry-run pass logs `alive silas gru`.
  Stale notify state cleared; launchd picks up the fixed script next tick.

## Crisis-duck ruling + viscomm belt state (~20:5xZ)

- USER RULING: crisis-duck approved — desaturate non-involved network during
  crisis. Briefing staged (crisis-duck.md); serialized behind gauge-telegraph
  (same render surface precedent), release = its merge close-out. Key
  contracts: byte-identical-when-inert, mutation-leg on draw path, CVD
  tables diffed, reduced-motion pins the transition. Involvement predicate
  seeded from Active_Crisis (bundle_lo, bundle_hi) pair (core/crisis.odin).
- Earlier: PR #99 merged 0b893ee (finding A shipped, r2 APPROVED);
  gauge-telegraph dispatched (w85:pJ) on finding B.

## Gauge PR #100: Perkins r1 APPROVED first-round (review 5024547297)

- 7/7 lenses glm-5.3, 22/22 verified, 0 blockers; mutation leg independently
  re-run by Perkins (bypass → palcheck ×2 FAIL); 49 goldens byte-identical.
  CI 4/4, MERGEABLE — user holds merge. On merge: crisis-duck auto-releases
  (fresh head, issue #101 fold rides it).

## PR #100 merged (23:30:50Z, 0b2aeb9) — trigger-graph release executed

- Finding B shipped. Crisis-duck AUTO-RELEASED at close-out exactly as wired:
  pane w85:pY (tab tD), glm-5.3 +thinking max, worktree @0b2aeb9 fresh head,
  issue #101 fold carried. Viscomm wave: A+B shipped, C in flight, D
  era-gated. The first fully hands-off release through the graph since the
  pi restoration — brief staged, ruling relayed, graph did the rest.

## Node legibility intake (user, 01:12 local — first play on merged v2)

- Report: "barely see the nodes even when zoomed in". Play was main checkout
  v2 @0b2aeb9 (rebuilt 00:44 right after Gru's v2 switch; 28-min session).
  Diff archaeology: viscomm merges did NOT touch node drawing — standing
  look imbalance; prime suspect the 9bf9797 puck shrink (1.05 base) + pipe
  saturation dominance. SECOND complaint on this axis (08-23 buildings →
  grew; now nodes/pucks).
- Dispatched READ-ONLY evidence job look-node-legibility-diag (captures at
  all 3 zoom tiers + KYLE pixel measurements + 2-3 proposals via lavish).
  Fix heist follows, serialized behind crisis-duck + user ruling at the
  lavish gate. [dublin] log-spam dedup noted for the fix row.

## Link vocabulary pivot (user, ~02:xx — the 08-23 revisit trigger fired)

- Direction: links SINGLE solid color, no lanes; queue state as ingress/
  egress READ at routers. Archaeology: this re-opens the 08-23 egress-qos
  steelman WITHDRAWAL — recorded trigger was "re-open re-framed at make QoS
  changes feelable (no queue migration)". Today = exactly that re-frame:
  RENDER-side, sim untouched (ODN-3 per-(bundle,lane) queues stand).
- Dispatched link-vocab-redesign (read-only exploration, lavish bake-off;
  folds era-gated finding D shape-vocab into the same gate). Hypothesis on
  the row: lane stripes are ALSO the node-legibility culprit — three
  lavish pages (node-legibility, link-vocab, crisis-duck verdict) converge
  at ONE user gate. Implementation serializes behind crisis-duck.

## Latency/egress architecture intake (user, ~02:xx — the escalation path fired)

- User: architect the packet-latency model (bmad skills) BEFORE deploying
  the link redesign. Sim truth verified: latency is SLA accounting only;
  delay = link-queue residency + travel ticks; no propagation model.
- Dispatched arch-latency-egress-queue-model (full bmad-architecture; fills
  a dated 08-26 spine — the 08-23 one was an empty template; memlog is the
  source of record). Heart: latency decomposition (egress queue residency
  + serialization at rate + propagation + hop) and the FEELABLE steelman
  (the 08-23 withdrawal bar). LAVISH gate before any PR.
- Sequencing wired: link-vocab implementation blocked_by architecture
  ratification; design exploration continues (may share the gate session);
  crisis-duck + node-legibility orthogonal.

## Latency/egress architecture RATIFIED (user, ~12:3xZ — "looks good", all leans)

- R1 FULL DUPLEX direction split (each direction gets bundle_cap; fixes the
  shared-bidirectional-queue divergence the investigation found). R2 config
  stays PER-PIPE (FORGE #4 letter amendment). R3 NO propagation term. R4 E9
  bound-6 re-keyed per-(port,lane), semantics unchanged.
- Process note: the minion ran the Fast path (draft-then-ratify) rather than
  coaching the user through the forks live — the deviation lived in Gru's
  briefing; the interactive gap was closed by ruling the four rows directly
  in chat. Future architecture briefings on load-bearing calls: name the
  Coaching-vs-Fast choice explicitly per the skill doctrine.
- Relay verified in the arch minion session; spine finalization + lavish
  ratification page in flight; link-vocab implementation releases at the
  arch row's completion per the wiring.

## Post-ratification wiring (Gru calls, ~12:4xZ)

- Spine docs PR: GO with explicit lavish exemption (content ratified
  in-session; re-review = bureaucracy). pr_review=0 docs job.
- D-2 bandwidth_demand loaded-but-unwired: NAMED STORY on the migration
  heist per ratified D3 (streaming 8->16 ticks disclosure; T1 re-bless) —
  never silent drift.
- New row arch-egress-migration (paneless, blocked_by crisis-duck merge
  close-out, pr_review=1): implements D1-D8 + R1 + D-2. Belt after crisis-
  duck: migration heist + link-vocab implementation (both serialize on the
  shared surface).

## Look-language consolidation + crisis r1 cycle (Silas, ~16:xxZ)

- ONE Sally rules the full look language (user ruling): link-vocab session
  consolidated into node-legibility w85:p11 (HANDOFF.md preserved; fork
  ladders merged; :4387 lavish server survived the pane close).
- crisis-duck Perkins r1 returned findings; B1 fix landed @0c86e83; r2
  fix-audit dispatched (w85:p1H, B1 mutation re-verify mandated). Remote CI
  billing-blocked (3rd time today) — standing ruling: local suite = ground
  truth, noted in brief + rows.
