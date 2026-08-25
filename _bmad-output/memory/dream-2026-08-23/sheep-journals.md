# sheep-journals — dream-2026-08-23

Sources: gru-journal + silas-journal 2026-08-21 (post-marker 18:49:59Z only),
2026-08-22, 2026-08-23 (08-23 read live mid-writing). Routine status noise,
settles, and already-classified echoes skipped. Candidates flagged
[2+ sightings] or [singleton]; arcs with multiple data points noted inline.

## 1. Perkins round debris is SYSTEMATIC — self-close leaves lens panes, worktrees, orphan husks behind [2+ sightings]

Sightings:
- v2-look-polish r1, 2026-08-21 (~23:47Z, Silas): "leftover Perkins debris swept (v2-look-polish): round r1 row done-but-empty-result (self-close gotcha) … Plus unregistered debris dirs (v2-4.3-network-health + v2-5.5-demolish-input = bare `_bmad` symlink dirs …) removed."
- camera-zoom-r1 / font-r2 / dublin-r3 + 6 more, 2026-08-23 (~11:20Z, Silas, user-flagged): "PERKINS ROUND-DEBRIS SWEEP (the recurring miss): lens panes + worktrees from DONE/superseded rounds were left behind (2nd+ occurrence; systematic — rounds self-close, sweep only fires at merge close-outs/startup)" — 14 lens panes closed, 9 worktrees removed, plus "ORPHAN HUSKS (worktree registration already pruned; lens agents had written `.unblock-marker`/`.cwd-keep` placeholder files after a mid-session sweep)".
- font-overhaul r6 lenses, 2026-08-23 (~15:45Z, Silas): "7 orphaned r6 lens panes closed (spawned pre-supersede-sweep, processes survived the worktree removal — the 08-17 class) + r3 husk dir removed".

Generalizes: round self-close ≠ swept — debris accumulates between merge
close-outs; sweep perkins-cwd panes + worktrees at every merge close-out AND
every startup/census, and expect husk placeholder files from mid-session sweeps.

## 2. Detection-ONLY sensor doctrine — sensors flag debris, never auto-clean [singleton event, built on 2 prior burns]

Sightings:
- silas-round-debris-sensor, 2026-08-23 (~11:20Z, user question): "do we need a sensor for clean up? how would that work? without cleaning pre-maturely" → answer: "a DETECTION-ONLY 7th nefario-watch sensor (round-debris) keyed on done round rows + cwd-matching panes + git worktree list; never auto-closes (premature-clean risk burned us 08-17 ×2 — id-proximity/label matching). Execution stays with Silas."
- Same job, built + merged PR #14, 2026-08-23: "Safety invariants (08-17 ×2 burns): done-rows only (in-flight exempt), cwd-EXACT matching, one alert until resolved, never closes/removes."

Generalizes: any new cleanup sensor ships detection-only with explicit
never-act invariants; execution stays with an operator who verifies
row-done + review-posted + cwd-exact before closing anything.

## 3. Mutation-proven gates: a gate that can't fail is a BLOCKER, not a pass [2+ sightings]

Sightings:
- font-overhaul r4, 2026-08-23 (Silas): "B1 gate-10 VACUOUS (mutation-proven: passes with overlay never drawn, 775>=500 from background; verb skips flip+swizzle overlay.odin:106-107)" → minion rebuilt it as "dual-render diff, mutation-proven 0px-vs-54k".
- noc-player-toggle r2, 2026-08-23 (Silas): "B1 dismissal + W1 boot defaults + W2 nav leg ALL mutation-verified by Perkins independently (delete-dismissal fails; default-flip fails 3 tests; ROW_COUNT->4 wraps+fails)".

Generalizes: pin/gate suites must carry a mutation leg (break the feature,
prove the gate bites); Perkins now mutation-verifies fixes independently —
a vacuous pass is itself a blocker finding.

## 4. Merge-LAST endgame for golden-storm colliders: domino rebases with ZERO re-bless by construction [2+ sightings]

Sightings:
- font-overhaul #87, 2026-08-23 (Gru ~11:4xZ): "Cause = merge-last × golden storm × 3 rebases. USER RULING: let it keep going (no protective merge-hold)."
- font-overhaul #87, 2026-08-23 (Gru ~14:3xZ): "My earlier 'font first' guidance was wrong — Silas' order right (fewest rebases); corrected to the user."
- font-overhaul #87 final move, 2026-08-23 (Silas ~14:50Z): "goldens HELD — no re-bless exactly as the ruling predicted (camera pinned-default + noc zero-pixels → 0 churn, 48/48 byte-identical, T1/replay untouched)" — one genuine catch found by the suite: "gallery_inject was misplaced ungated inside cam_e2e, gate 2 caught it".

Generalizes: order a colliding PR merge-LAST, fire each rebase off the
sibling's merge close-out, and verify zero golden churn on the combined
code instead of re-blessing; fewest-rebases-first beats
most-important-first when goldens collide.

## 5. Moot/supersede doctrine extended: EARLY-WAVE rounds on a stale head get swept, no rN+1 [2+ sightings]

Sightings:
- noc-player-toggle r3, 2026-08-23 (Silas ~14:40Z): "user merged the REBASED head (29addf4) while r3 was mid-review → r3 MOOT ON MERGE (08-07 doctrine: terminal merge moots the in-flight round, no re-dispatch)".
- estate-spawning r3, 2026-08-22 (Gru ~21:4xZ): "estate r3 moot (#80 merged on standing approvals)".
- font-overhaul r6, 2026-08-23 (Silas ~14:50Z): "r6 swept as SUPERSEDED (early-wave on the pre-rebase 4688d3d — diff-only, no lens outputs; head moved; merge imminent per plan — no r7 unless the user asks for a pre-merge verdict)".

Generalizes: the 08-07 moot-on-merge doctrine now also covers early-wave
rounds (diff-only, no lens outputs) when the head moved and the merge is
armed — sweep and skip the next round unless the user asks.

## 6. UI-surface Perkins rounds converge B1 → B1' → B1'': each fix unmasks the ADJACENT interaction bug [1 arc, 4 rounds of data]

Sightings (all packet-plumber NOC surface, 2026-08-23, Silas):
- noc-player-toggle r1: "disabling NOC via the settings row while the panel is open leaves it STUCK ON (5-lens convergence)".
- noc-readability-2 r1: "B1: settings-row NOC dismissal desyncs play_w … (the rail-era sibling of the noc-player-toggle stuck-panel class)".
- noc-readability-2 r2: "all r1 findings FIXED … NEW B1': header row collides in the PR's own captures … loss[1134,1170] vs SLA@1150 = 'loS&A'".
- noc-readability-2 r3: "r2 fold GENUINELY GOOD … NEW B1'': the W5' plate press-swallow deadens the two rightmost tray chips that paint over the plate … swallow (main.odin:1201) runs BEFORE the tray hit-test".

Generalizes: budget multiple rounds for shared chrome/input/rail surfaces —
each CHANGES_REQUESTED fold is genuinely good yet exposes the next
interaction-adjacent bug; carry the class lineage ("sibling of the
stuck-panel class") in each fold briefing so the minion greps the whole
surface, not just the named lines.

## 7. Reasoning HOLD cycle absorbed cleanly: park with named resume trigger → probe → flip → continue, zero work lost [2+ sightings]

Sightings:
- camera-zoom r4 + font r5, 2026-08-23 (Silas ~10:47Z): "BOTH round mains errored on 1308 (5h hard cap, reset claimed 19:40Z) — account-wide wall, continue = waste … Both rounds PARKED mid-wave with named resume triggers on the rows"; lifted ~12:15Z — "k3 probe OK 12:15:02Z (cycle refreshed). Camera r4 (p2ZZ) + font r5 (p2Z0) each ONE continue → working".
- Gru, 2026-08-23 (~12:15Z): "Second hold of the arc absorbed: parked -> probed -> flipped -> continued, zero work lost. User-side: #90 Dublin merge-ready, hold-immune throughout." Also notes "user call right" on the ~1h hold estimate.
- font r4, 2026-08-22 (Gru ~02:1xZ): "glm 1308-capped again mid-round (reset est 09:31:51Z) — r4 finished on k3 via the sanctioned mid-round flip; new dispatches k3-primary regardless."

Generalizes: (largely canon already — fresh confirmations) the park/probe/
flip/continue loop loses zero work; user-side merges are hold-immune and
should proceed; the provider's stated reset time is never trusted.

## 8. Probe strict-match: chatty replies read false-DOWN — re-probe once before acting [singleton this window; recurrence of the 08-20 class]

Sightings:
- noc-readability-2 r1 dispatch, 2026-08-23 (Silas ~16:45Z): "probe k3 = 403, glm FIRST READ false-DOWN (chatty 'OK — how can I help' reply vs strict ^OK$ — the 08-20 class), RE-PROBE = OK → glm-5.3 round".

Generalizes: the probe verdict must strict-match the reply body; any
surprising DOWN read earns exactly one re-probe before a HOLD or reroute.

## 9. _local-refs/ is the intake lane for external reference assets — provenance README, never committed [2+ sightings]

Sightings:
- MM press kit, 2026-08-21 (~01:3xZ, Gru): "Fetched the OFFICIAL Dinosaur Polo Club press-kit images zip (9 JPGs, 3840x2160) into _local-refs/mm/Mini-Motorways-images/ + provenance README … refs still never enter repos/committed artifacts." Also: a user ruling can supersede a briefing guardrail — "supersedes briefing rule-3 no-fetch clause".
- design-videos DIRECTION.md, 2026-08-22 (~02:3xZ, Gru): "Synthesized _local-refs/design-videos/DIRECTION.md: 5 steps mapped to PP" — extracted from a full transcript + KYLE thumbnail reads; some sources walled ("storyboards 403'd (session-signed), Hokkori transcript unavailable (innertube walled)").
- Suno ambience asset, 2026-08-22 (~20:4xZ, Gru): "Vaulted to _local-refs/audio/ + README (provenance, mood plan…)".

Generalizes: IP-sensitive or user-generated reference material lives in
_local-refs/ OUTSIDE all repos, each with a provenance README; briefings
point at the drop path and minions cite but never copy into the tree.

## 10. Vision routing in practice: remote 4.6v → LOCAL lmstudio 4.6v-flash fallback → gemma coarse; capability follows the ACTIVE model intra-day [2+ sightings]

Sightings:
- local fallback wiring, 2026-08-22 (~22:2xZ, Gru): "Wired bin/vision-read --local slot to it (gemma demoted to coarse --fast last resort); verified through pi on the user's screenshot … Vision routing now: remote glm-4.6v primary -> local glm-4.6v-flash fallback -> gemma coarse."
- Gru mid-morning flip, 2026-08-23 (~11:2xZ): "my model flipped glm-5.3 (blind) mid-morning — KYLE reads for me again; the earlier k3 'native vision' window closed".
- KYLE pipeline first production run, 2026-08-21 (~01:3xZ, Gru): "first production run of the merged KYLE quick-read (bin/vision-read @ glm-4.6v) — correctly identified the gameplay shot. Pipeline proven live."

Generalizes: vision capability is a property of the CURRENT pane model and
flips intra-day with HOLDs/fallbacks — keep the remote+local fallback chain
wired so reads never block, and verify every new slot THROUGH pi with a
real image (never trust a self-named id).

## 11. Honesty flag: pi can silently OMIT an image attachment — a 'visual read' that was inference must be called out [singleton]

Sightings:
- Gru Dublin screenshot read, 2026-08-23 (~11:2xZ): "the 08:58 Dublin screenshot read was CONTEXTUAL not visual — pi omitted the image; my Dublin description was inference, flagged for honesty".

Generalizes: when a blind-model session appears to have read an image,
check the session jsonl for the actual attachment before believing it —
and if the read was inference, say so in the same breath as the answer.

## 12. Directive-vs-question misfire: the recall path = parked pane + artifact-backed DISCUSSION minion [singleton]

Sightings:
- flow-focus, 2026-08-23 (Gru ~11:4xZ): "flow-focus: RECALLED by user ('it was a question') — pane parked, design discussion instead. CIS problem-solver session opened; user then asked for a SPAWNED DISCUSSION MINION with the skill -> pane w1T:p2ZX … armed with SKILL.md + the draft artifact _bmad-output/problem-solution-2026-08-23.md; user talks to it directly; checkpoints land in the artifact."

Generalizes: before dispatching build work off a user's musing, confirm
directive-vs-question; on a recall, park the pane (cheap) and, if the user
wants to think, spawn a skill-armed discussion minion they talk to
directly — the artifact, not the chat, accumulates the decisions.

## 13. Pane layout doctrine: MAX 6/tab as 3×2, built AT CREATION — post-hoc resize semantics are empirical [singleton ruling + 1 surgery]

Sightings:
- user ruling, 2026-08-23 (Gru ~11:4xZ): "Pane layout doctrine (user ruling): MAX 6/tab, 3 rows x 2 cols — relayed to Silas (redistribute the 7-8-pane lens tabs + standing split rule)".
- pp-font-r5-lenses (tP1) surgery, 2026-08-23 (Silas ~12:40Z): "Gru fumbled the lens-ladder layout (6 panes at 1/1/2/3/58/7 rows, user-flagged) … learned the resize semantics empirically (up = top edge up = grow; down = bottom edge down = grow; top/bottom panes clamp → shrink/no-op), iterated ~10 small resizes with layout reads → all 6 lenses EVEN at 12 rows each. Zero panes closed/moved — live round intact."

Generalizes: lens tabs are created as a 3×2 grid (never a split ladder);
if a ladder happens, even it out with small iterative resizes + layout
reads — surgery on a live round is safe if no pane is closed or moved.

## 14. Mid-flight relays to WORKING panes can vanish — verify delivery, resend + send-keys enter [2 flavors]

Sightings:
- design-audit AMENDMENT #3, 2026-08-22 (Gru ~03:xxZ session-lessons): "user-relay to a working pane can vanish (AMENDMENT #3 needed resend + send-keys enter — pane capture-dropped the first)".
- camera-zoom r4 escalation, 2026-08-23 (Silas ~12:45Z): "Escalation queued in Gru's steering buffer (pi-owned — delivers at turn end; retry duplicated the queue, harmless)" — the flip side: a queued relay to a busy pi only lands at turn end.

Generalizes: the handover-delivery gotcha extends to mid-flight relays —
every relay to a working pane ends with a delivery check (pane read /
session grep), and a retry into a busy pane may queue rather than deliver.

## 15. Mid-flight AMENDMENTS to working minions are the healthy path (relay + verify, never kill-and-redispatch) [2+ sightings]

Sightings:
- v2-look-polish p2KM, 2026-08-21 (~20:3xZ, Gru): "Relayed to p2KM (vision spawn recipe + code-context mode + IP guardrail + scope relaxation)" — the vision-driven MM comparison folded in mid-flight; FULL refresh/repolish approved without redispatch.
- design-audit p2KZ, 2026-08-22 (~02:3xZ, Gru): "MID-FLIGHT AMENDMENT #2 relayed to design-audit (p2KZ): blur-test scoring, harmony+depth columns in the verdict table, sound in recommendations."
- design-audit p2KZ, 2026-08-21 (~01:3xZ, Gru): MM press-kit refs relayed mid-flight — "supersedes briefing rule-3 no-fetch clause; side-by-side + per-verdict citations".

Generalizes: scope/inputs changes ride a relayed amendment into the
working pane (with delivery verification per #14); the briefing is a
starting contract, not a cage — including superseding its guardrails when
the user rules so.

## 16. launchd/cron minimal PATH breaks embedded CLI probes — resolve tools by ABSOLUTE path at install time [singleton, fixed same night]

Sightings:
- night-watchman false-DOWN, 2026-08-21 (~23:37-23:47Z, Silas): "the watchman's quota-probe runs under launchd MINIMAL PATH and fails `env: pi: No such file or directory` (wrote the artifact into quota-regime.json 23:38:43Z)" — watchman REFUSED to relaunch a genuinely dead Gru because its probe gate read both providers down; manual probes showed "glm-5.3 = UP" and Silas relaunched Gru himself.
- Fix deployed, 2026-08-22 (~01:20-01:30Z, Silas): "plist copied + bootout/bootstrap/kickstart → launchd job active with PI_BIN=/Users/moses/.local/share/fnm/aliases/default/bin/pi; watchman log 00:17:57Z shows `paths: herdr=... pi=<absolute>` resolved — the scope-8 PATH fix LIVE in production".

Generalizes: any out-of-shell automation (launchd, cron, watchdogs) that
shells out to pi/herdr/git must bake absolute binary paths into its
environment at install time, and its probe results must be treated as
suspect until the PATH fix is verified in the tool's own log.

## 17. Trigger-graph wave release at scale: paneless held rows + named triggers + SEQUENTIAL same-repo worktree creates [2+ sightings]

Sightings:
- WAVE POSTURE encoded, 2026-08-21 (~01:5xZ, Silas): "all 7 wave rows … now PANELESS with blocked_by graph + named release triggers … Auto-release at each merge close-out per trigger-graph doctrine."
- Wave released, 2026-08-22 (~15:00-15:06Z, Silas): "WAVE RELEASED (the #76 merge cascade): READY SET = estate-spawning + tier-1 x4 … 5 worktrees @origin/v2 4ccc8c7 (sequential creates — no lock races) … ALL WORKING."
- index.lock race self-corrected, 2026-08-21 (~00:57Z, Silas): "First parallel worktree-create hit an index.lock race (second create failed once, retried clean) — sequential creates for same-repo pairs next time."
- Full arc verified, 2026-08-23 (Silas ~15:45Z): "The wave: #76 pace-tuning → #77/#78/#80/#81/#82/#83/#84/#85 (wave tier-1 + held) → #86 ambience → #88 blender-sculpt → #89 camera-zoom · #90 dublin-map-spike · #91 noc-player-toggle · #87 font (LAST) — all four APPROVED by Perkins" — blocked_by chains (spawn-feel ← estate, scale-depth ← sound, blender ← scale-depth + user merge gate) all fired clean.

Generalizes: the paneless-held-row + named-release-trigger mechanism now
carries whole multi-job waves, including merge-gates keyed on USER actions
(Blender launch); create same-repo worktrees strictly sequentially during a
mass release.

## 18. Known ledger/pane gotchas STILL recur — verify-and-fix remains the only guard [2+ sightings]

Sightings:
- noc-readability-2 row add, 2026-08-23 (Silas ~16:00Z): "pane-id gotcha hit + corrected (guessed ids in the add, fixed via sqlite to the parsed move result)" — the hand-typed-id class again, despite the variable-capture canon.
- camera-zoom r4 self-report, 2026-08-23 (Silas ~10:30Z): "Same-status self-report dropped its note → ledger note written" — `ledger set` same-status no-op swallowed the minion's completion note.
- debris sweep hygiene, 2026-08-23 (Silas ~11:20Z): "stale pane_ids NULLed on 10 done round rows + flow-focus (row fields already swept at badge-out)" — row fields drift out of sync with the swept reality.

Generalizes: documentation does not stop the pane-id/same-status/stale-field
classes — keep the sqlite verify-and-fix step in every dispatch/close-out,
and NULL pane/tab/worktree fields on rows at sweep time.

## 19. Degraded-lens rounds still count: 6/7 lenses + surviving findings = valid verdict [singleton; sibling of the 08-19 g-wave COMPENSATION canon]

Sightings:
- font-overhaul r5, 2026-08-23 (Silas ~12:45Z): "APPROVED … 6/7 lenses — codebase 429×2 degraded, findings exist so guard passes; 17/17 confirmed".

Generalizes: a lens degraded by provider 429s does not invalidate the round
when the lens still produced findings — the guard keys on findings presence,
not lens count; note the degradation on the round row.

## 20. Arc-level observation: the user play session is the requirements engine — one sentence → a 16-PR wave [2+ arcs]

Sightings:
- PP v2 design wave, 2026-08-22 (Gru ~06:21Z): "The 2026-08-22 play-session arc: one sentence ('look better like mini motorway') -> 10 merged PRs + NOC dashboard + font pick pending + Blender stage-2 + Suno verdict."
- Wave completion, 2026-08-23 (Gru ~15:43Z): "Arc origin: one user sentence at a play session ('look better like mini motorways') -> design audit (KYLE) -> 7-job wave + pace/estates -> fonts, dublin, camera, sculpt, ambience, noc-for-players" — 16 PRs #76-#91 merged across 08-22/23.
- real-city-maps arc, 2026-08-23 (Gru ~08:0xZ): "User (playing the rebuilt city): wants REAL city maps — a Dublin cross-section board" — next wave opens from the next play session.

Generalizes: keep a playable build on main and the fun-test gate user-held —
the user's play sessions, not planning docs, generated the highest-velocity
requirements stream in this window; design-audit (KYLE) first, then a
trigger-graphed wave, is the proven conversion shape.

DONE (sheep-journals, 20 candidates)
