# Dream report — 2026-08-23

Material: 17 field-note shards read in full (+2 pre-marker tail-reads: ue-slice-1, night-watchman — both clean pre-marker), 6 journal files (gru 08-21 post-marker / 08-22 / 08-23; silas 08-21 post-marker / 08-22 / 08-23), ledger 700-event stream end-to-end (~52 jobs with post-marker activity), since 2026-08-21T18:49:59Z. Sheep: shards / journals / ledger (all kimi-coding/k3, thinking max, provenance verified via session modelId; 28 + 20 + 21 candidates). The window is one story: the PP v2 design wave — 16 PRs merged in ~30h (#76–#92 arc) under a billing block, 2 both-providers-down HOLDs, ~30 Perkins rounds — plus an orchestrator tooling burst (PRs #8–#14 incl. the round-debris sensor).

Store copies edited (diff-ready): `store/AGENTS.md` (+138 lines, 13 edits: 9 appends to existing gotchas + 4 new entries — all additive), `store/minion-field-notes.md` (+85 lines, 7 edits: 2 addenda + 5 new entries — all additive). Live files untouched. All proposals class **auto** (gotcha appends / new gotcha entries within existing sections / shard promotions / facet addenda per the 08-19/08-21 dream precedent); no user-ack proposals this pass.

## Proposals (all applied to store copies)

### P1 — HOLD/park resume doctrine: head-staleness key + vision-wait ruling + 1302 taxonomy
- Target: store/AGENTS.md (Provider incidents) · Class: auto
- Change: appended — (a) the RESUME decision keys on head staleness: a parked round whose target sha moved is SWEPT + fresh-dispatched on the current head; an unchanged head resumes with ONE continue; a round never re-targets. (b) USER RULING 08-23: a parked round with visual evidence WAITS for the vision-capable provider (k3) — a glm resume buys a mechanical-only verdict. (c) 1302 burst taxonomy: launch-bursts (harmless, one continue) / mid-burst continue-landings (wait, one more — never spam) / post-1308-reset cycling (expected) / probe-verified concurrency bursts (no hold) — the probe distinguishes burst from wall.
- Evidence: motion-r2 3635de0 + estate-r3 be7c0fa stale at the 08-22 19:2xZ lift; spawn-feel/camera/dublin/font swept-and-refreshed ×4; camera-r4 + font-r5 continued same-head at the 12:15Z k3 flip; the 10:58Z vision-wait ruling written identically on 2 rows; ≥15 1302 events 08-22/23 (dublin r1/r3 2.9KB launch-bursts; silhouettes-r2 mid-burst; scale-depth post-reset ×3; camera/font 12:22Z concurrency).
- Reasoning: the park/probe/flip/continue loop absorbed 2 HOLDs with zero work lost this window — but the resume decision (sweep vs continue) and the vision-wait preference were only encoded in row notes; both are now doctrine, and the 1302 taxonomy replaces "one continue per pane" with per-flavor handling.

### P2 — Round debris is SYSTEMATIC: sweep at every close-out + census; detection-only sensor shipped
- Target: store/AGENTS.md (Watchers/sensors, Close-out drift entry) · Class: auto
- Change: appended — self-close ≠ SWEPT: lens panes + worktrees + ORPHAN HUSKS (registration pruned; lens agents wrote .unblock-marker/.cwd-keep placeholders after mid-session sweeps) accumulate between merge close-outs. Sweep perkins-cwd panes/worktrees at EVERY merge close-out AND startup/census; NULL pane/tab/worktree fields on done round rows at sweep. The 7th nefario-watch sensor (round-debris, PR #14) is DETECTION-ONLY (done-rows only, cwd-EXACT, never closes/removes) — detection-only is the sanctioned shape for ANY cleanup sensor (08-17 burns).
- Evidence: user-flagged census 06:26Z closed 42 panes (45→3); 11:20Z startup sweep: 14 lens panes + 9 worktrees + husks; post-#87 sweep: 7 orphaned r6 lens panes (processes survive worktree removal); v2-look-polish debris 08-21; sensor PR #14 merged 10:37Z with planted-husk validation.
- Reasoning: debris was a recurring miss the whole window (3 sweeps + a census + a sensor job) — the systematic gap (sweeps only fired at close-outs/startup) and the husk class were unnamed in canon; the sensor's never-act invariants deserve the standing rule.

### P3 — Perkins quality bar: mutation-proven pins, degraded-lens guard, in-flight sweep-stale
- Target: store/AGENTS.md (Perkins round ops entry) · Class: auto
- Change: appended (d)(e)(f) — VACUOUS pins are the dominant blocker class (a gate that can't be made to fail by mutation is a BLOCKER finding); the accepted fix standard = the MUTATION LEG, and Perkins now mutation-verifies fixes independently. 429-degraded lenses: 6/7 valid when findings exist or coverage is re-proven by direct guard verification — disclosed, never faked, never re-dispatched. A head move mid-round = SWEEP the stale round + dispatch FRESH at the new head (a round never re-targets; cost = one worktree add).
- Evidence: font r4 gate-10 ("passes with overlay never drawn, 775>=500"), camera r3 W4, spawn-feel B2, motion B1 (vacuous); noc-toggle r2 (delete-dismissal fails / default-flip fails 3 tests / ROW_COUNT->4 wraps+fails) + font r5 (dual-render 0px-vs-54k) as fix standard; sound r1 + silhouettes r2 + font r5 6/7-with-findings; spawn-feel/camera/dublin/font swept-stale ×4.
- Reasoning: the PP wave raised the review bar — "mutation-proven" is now the acceptance evidence for fixes, vacuous gates are blockers in their own right, and the degraded-lens guard keyed on findings presence was exercised 3× without a wasted re-dispatch.

### P4 — Moot doctrine at scale: disposable confirmation rounds + early-wave SUPERSEDED sweep
- Target: store/AGENTS.md ("Moot on merge" entry) · Class: auto
- Change: appended — confirmation/delta rounds around an APPROVED substance are DISPOSABLE (sweep, no re-dispatch, record the safe-merge qualifier); sibling class: an EARLY-WAVE round (diff-only, no lens outputs) when the head moved and the merge is armed gets swept with NO rN+1 unless the user asks for a pre-merge verdict.
- Evidence: noc-toggle r3 (merged ON the reviewed head mid-review), silhouettes r3 (parked under HOLD), sculpt r2 + scale-depth r2 (merged before confirmation posted), estate r3; font r6 swept SUPERSEDED @4688d3d 14:45Z.
- Reasoning: moot-on-merge fired 5× this window plus a new sibling (deliberate supersede of an early-wave round vs imminent merge) — the qualifier-recording habit is what keeps sweeps safe and auditable.

### P5 — Merge-wave orchestration: merge-LAST golden colliders, domino rebases, zero-churn verification
- Target: store/AGENTS.md (Watchers/Perkins, NEW entry) · Class: auto
- Change: new gotcha — the end-to-end wave playbook: paneless holds → trigger-merge release → per-merge DOMINO conflict relays (rebase + force-with-lease + re-verify + rebase-delta round) → one declared MERGE-LAST job for the golden collider rebasing ONCE onto the settled head; order by FEWEST REBASES not importance; zero-churn verification beats re-blessing ("re-bless ONLY if a diff proves otherwise, cause-documented") and still catches real bugs (gallery_inject, gate 2); arm the final move explicitly so the dominoes stop deliberately.
- Evidence: the 16-PR wave #76–#92 (Gru's "font first" guidance was wrong; Silas's fewest-rebases order held — corrected to the user); font #87 merged LAST 15:43Z after 3 rebases with 48/48 byte-identical NO re-bless; ~20 domino-relay events 08-22/23.
- Reasoning: the whole wave ran on improvised-but-consistent merge choreography that was never written down; it is now the largest proven orchestration pattern in the store and the first to run golden colliders through a merge order.

### P6 — Pre-merge APPROVAL AUDIT: merge-readiness = APPROVED on the CURRENT head
- Target: store/AGENTS.md (Watchers/Perkins, NEW entry) · Class: auto
- Change: new gotcha — after a HOLD/park or churn window, before anything merges: audit each PR's actual GitHub review list (`gh api .../pulls/<n>/reviews`), never minion claims or ledger notes.
- Evidence: user-caught #82 motion-readability 08-22 19:20Z reached the merge-ready list with a single CHANGES_REQUESTED on a stale sha (fix fold + rebase NEVER reviewed; struck until r4 APPROVED landed on the current head); the same audit passed estate-spawning clean the same minute; motion's minion then internalized "fresh round = the approval gate" on its own.
- Reasoning: the one skipped audit nearly merged a never-approved PR and the USER caught it — the cheapest gate in the whole loop (one API call per PR) was missing from canon.

### P7 — Mid-flight relay discipline: verify delivery; amendments are the healthy path
- Target: store/AGENTS.md (Dispatch & handover, deliverable-reporting entry) · Class: auto
- Change: appended — delivery verification extends to MID-FLIGHT relays to WORKING panes: a relay can VANISH (capture-drop → resend + send-keys enter) or QUEUE until turn end (a retry duplicates the queue — harmless); verify by pane read / session grep. Mid-flight AMENDMENTS are the healthy change path (relay + verify, never kill-and-redispatch); a briefing guardrail yields to a USER RULING via relayed amendment, never to minion initiative.
- Evidence: design-audit AMENDMENT #3 capture-drop (resend + send-keys enter, 08-22); camera-r4 escalation queued in Gru's steering buffer (08-23 12:45Z); ×3 healthy amendments (look-polish vision-MM scope, design-audit blur-test columns, MM press-kit no-fetch supersede).
- Reasoning: the handover-delivery gotcha covered dispatch-time; mid-flight relays have TWO new failure shapes (vanish/queue) and one strong healthy pattern — all three were exercised this window.

### P8 — Lens-tab layout doctrine: MAX 6/tab as 3×2, built at creation
- Target: store/AGENTS.md (Dispatch & handover, NEW entry) · Class: auto
- Change: new gotcha recording the user ruling — lens tabs are a 3-rows × 2-cols grid built AT CREATION, never a split ladder; post-hoc even-out via small iterative resizes + layout reads (empirical semantics: up = top edge up = grow; down = bottom edge down = grow; edges clamp); surgery on a LIVE round is safe if no pane is closed/moved. Playbook + lens-skill-template amendments noted as pending.
- Evidence: Gru's fumbled ladder (6 panes at 1/1/2/3/58/7 rows, user-flagged 08-23); Silas's pane surgery evened all 6 to 12 rows with zero closures.
- Reasoning: user-ruled standing doctrine; the gotcha append preserves it for every future lens wave while the playbook/skill amendments ride the docs pass.

### P9 — _local-refs/ is the intake lane for external reference assets
- Target: store/AGENTS.md (Dispatch & handover, NEW entry) · Class: auto
- Change: new gotcha — IP-sensitive/user-generated references live in `/Users/moses/code/_local-refs/` (UNTRACKED, outside all repos, provenance README per drop); minions cite but never copy into a tree; briefing no-fetch clauses yield only to user rulings; lavish serves them via a loopback http.server pane (static root 403s symlinks).
- Evidence: ×3 drops (MM press kit 9 JPGs, design-video DIRECTION.md, Suno ambience WAV) + the design-audit symlink-403 → http.server:4388 recipe; the MM drop superseded design-audit rule-3 by user ruling.
- Reasoning: the reference-asset workflow stabilized this window around _local-refs; the IP guardrail + serving mechanics were only in job shards.

### P10 — KYLE addendum: local vision fallback + the pixel-verification law + spawn craft
- Target: store/AGENTS.md (Vision/KYLE entry) · Class: auto
- Change: appended — routing grew a LOCAL fallback (remote glm-4.6v → `bin/vision-read --local` lmstudio glm-4.6v-flash → gemma coarse `--fast`); vision capability follows the CURRENT pane model and flips intra-day. Craft laws: (a) a vision verdict is a SCREENING layer, never evidence — pixel-verify before it drives a decision; (b) spawn craft — prompts to FILES, absolute OUT paths, verify session modelId, read findings from DISK, nudge overdue turns with "write NOW compactly".
- Evidence: local fallback wired + verified through pi 08-22 22:2xZ; Gru flipped glm-5.3 (blind) mid-morning 08-23; design-audit pass-1 "3D shading" wrong (sprites 90-93% flat) + "shapes identical" wrong (aspects 1.01 vs 1.45-1.48); silhouettes KYLE caught nothing at contact-sheet scale (bbox table + zoomed check caught the stacked port-ring dots); 500/timeout handling per design-audit.
- Reasoning: four jobs converged on "measure pixels before believing a vision verdict" — the KYLE doctrine entry had the routing but not the evidence bar or the operational spawn recipe.

### P11 — launchd MINIMAL-PATH class: a PATH error is NEVER a provider verdict
- Target: store/AGENTS.md (Pane forensics, watchman entry) · Class: auto
- Change: appended — the watchman's probe failed `env: pi: No such file or directory` under launchd, wrote a bogus both-down regime, and REFUSED to relaunch a genuinely dead Gru (glm was UP). Fixed in PR #11: pi/herdr/jq resolved ABSOLUTELY at install (PI_BIN → fnm aliases → node-versions → command -v); broken probe exits 2 with NO regime write, logged+notified TOOL-BROKEN. Generalizes to any out-of-shell automation.
- Evidence: the 23:38Z 08-21 false-DOWN incident (Silas relaunched Gru manually); PR #11 deployed 08-22 00:17Z with paths resolved in the log.
- Reasoning: the most severe watchman failure mode (refusing a valid relaunch on a tool error) is now structurally prevented; the TOOL-BROKEN ≠ provider-verdict distinction is the durable part.

### P12 — Generators sidestep the backtick ParseError class structurally
- Target: store/AGENTS.md (Extensions, backtick gotcha facet) · Class: auto
- Change: appended one facet — emit generated strings via JSON.stringify / json.dumps double-quoted (ensure_ascii=False): backticks/${}/quotes/backslashes become inert, no template literal at all.
- Evidence: role-skills gen-role-blocks.ts + drift-check (byte-identical regen, dogfooded same day it landed).
- Reasoning: the 08-01 class had only an avoidance rule ("escape every span"); the generator pattern makes the hazard structurally impossible — a facet addendum to the existing gotcha.

### P13 — Trigger graph carried a whole 16-PR wave; sequential same-repo worktree creates
- Target: store/AGENTS.md (Orchestration upgrades / P2 trigger graph) · Class: auto
- Change: appended — a whole multi-job WAVE encodes as paneless blocked_by rows + named release triggers, including merge gates keyed on USER actions (Blender launch); create same-repo worktrees STRICTLY SEQUENTIALLY during a mass release (a parallel pair hit an index.lock race once — retried clean).
- Evidence: 7 wave rows held behind #76, released on cue at its merge close-out (all working within ~7 min); the 08-21 00:57Z index.lock race; the wave completed 08-23 15:43Z with zero misfires.
- Reasoning: the P2 entry said "verified at scale 08-19/20" for 4 rows; this window proved the mechanism at 16-PR scale with a new ops wrinkle (the lock race).

### P14 — rlsw dual-render facets: LINE alpha opaque, CCW winding, SW-build traps, GPU lies twice
- Target: store/minion-field-notes.md (Tooling traps, rlsw entry addendum) · Class: auto
- Change: appended a 2026-08-23 addendum with the NEW facets only (existing 08-11/13/15/21 content untouched): LINE primitives render alpha OPAQUE in rlsw (×2); hand-built fans must wind CCW (renders NOTHING in both renderers otherwise); SW-app traps (GetTime()==0 busy-wait — skip the FPS limiter; no raudio — gate via PP_SW_AUDIO); the GPU path lies twice (compositor front-buffer freeze + RenderTexture alpha pollution) — SW framebuffer is the only reliable capture; harness verbs need the `ms` suffix + app-matching view flags (×2).
- Evidence: look-polish, spawn-feel, font-overhaul, noc-readability-2 shards (firsthand).
- Reasoning: the PP v2 visual wave kept rediscovering these at cost (wasted re-bless cycles, invisible geometry); the addendum keeps one entry as the canonical dual-renderer trap list.

### P15 — bmad-build waiver: SECOND root cause + transient in-place fix proof
- Target: store/minion-field-notes.md (Tooling traps, bmad-build entry) · Class: auto
- Change: appended — second root cause in the PP repo (`_bmad/scripts/` has NO render_skill.py); same waiver path ×4 jobs this window; estate-spawning proved it transiently FIXABLE in place (temp-disambiguated dup keys, config restored byte-equal) — but the waiver stays the standing path until a real fix job.
- Evidence: pace-tuning 23:57Z, motion-readability 15:04Z, camera-zoom 08:08Z, noc-player-toggle shard; estate 15:08Z in-place fix.
- Reasoning: the 08-21 entry recorded one root cause and "no in-repo fix exists" — both halves are now stale; the recurrence count (4 jobs/window) also justifies a real tooling job eventually.

### P16 — Piped/scripted runs silently no-op: capture rc, prove freshness, byte-check artifacts
- Target: store/minion-field-notes.md (Tooling traps, NEW entry) · Class: auto
- Change: new entry — `blender -b -P … | grep` masked the exit code AND traceback (two "determinism-proof" runs had crashed while cmp compared STALE files); scripted rewrites corrupt invisibly (heredoc/tr corruption; triple-quote self-termination). Verification = rc captured un-piped AND output proven fresh AND the generated artifact byte-checked. Sibling of the AGENTS.md herdr no-pipes rule — the class is ANY wrapper.
- Evidence: blender-sculpt (08-23); playbook-diet ×2 (08-21).
- Reasoning: three independent silent-failure surfaces in two days; the herdr rule was the first sighting of a general class.

### P17 — Edit-batch anchors: em-dashes and wrapped copies atomically reject the whole batch
- Target: store/minion-field-notes.md (Tooling traps, NEW entry) · Class: auto
- Change: new entry — edit batches are ATOMIC; special chars are the silent killers (an em-dash in oldText failed a whole batch while the block was verifiably present; store-copy anchors wrap differently than in-context rendering). Grep the exact anchor bytes in the TARGET file first (watch phantom leading spaces on wrapped lines), use minimal ASCII-only anchors, script replaces for punctuation-heavy regions.
- Evidence: noc-player-toggle (08-23) + dream-2026-08-21 Bob's own wrap lesson + RE-CONFIRMED by this dream (3 of 7 field-notes edit batches bounced on exactly this class — phantom leading spaces).
- Reasoning: this dream's own edit pass hit the trap 3×; it is now a 3-sighting pattern across two independent writers.

### P18 — Review crafts: mutation legs unprompted, fold-regression lineage, PR-body audit
- Target: store/minion-field-notes.md (Recurring review findings, NEW entry) · Class: auto
- Change: new entry — (a) ship every pin with its MUTATION LEG unprompted; (b) fix-folds REGRESS THEMSELVES on shared chrome/input surfaces — budget multiple rounds, carry the class LINEAGE in fold briefings so the minion greps the whole surface; (c) the PR body + fold claims are AUDITABLE artifacts — a claim the code doesn't back is a BLOCKER, a stale body is a note; re-audit the body against the final head before each round.
- Evidence: noc surface arc r1→r3 (stuck-panel → play_w desync → header collision → tray-chip dead zone — each fold genuinely good, each exposing the adjacent bug); font r3 fictitious N11 + font r1 B2 wrong body; noc-readability-2 N6' stale body fixed via one `gh pr edit`.
- Reasoning: minion-side counterpart to P3 — what Perkins now demands, minions should ship unprompted; the lineage-carry practice is what turned the 4-round arc into convergence instead of ping-pong.

### P19 — Determinism evidence: decoded pixels, PNG metadata stripping, re-bless triple-verify
- Target: store/minion-field-notes.md (Conventions, NEW entry) · Class: auto
- Change: new entry — compare DECODED PIXELS never file bytes (md5 diffs were encoder metadata; strip tEXt/iTXt/zTXt — the Date tEXt is the only mover); a no-op re-render is golden-safe (render + pixel-compare, no re-bless); the per-commit re-bless loop pays when every commit carries the triple-verify (cmp -l every .log.bin/.t1; diff-bbox scans matching PREDICTED blend colors ±0; palcheck re-pins with measured floors).
- Evidence: blender-silhouettes (pixel-deterministic re-render), blender-sculpt (PNG chunk strip), look-polish (5 deliberate re-blesses, CI 10/10 at every commit).
- Reasoning: three render-pipeline jobs converged on the same evidence standard; byte-compare false alarms cost real debugging time this window.

### P20 — Clarify rulings EVOLVE: amend on evidence contact; final shrinks scope + adds acceptance proof
- Target: store/minion-field-notes.md (Conventions, NEW entry) · Class: auto
- Change: new entry — a clarify ruling is the START of the decision: expect AMENDMENT on first contact with evidence; the FINAL ruling often shrinks scope while ADDING an acceptance proof ("a render function never called is not a feature" — the E2E key-toggle capture). A minion's reasoned keep-as-dispatched recommendation can itself be the ruling.
- Evidence: noc-overlay D-key saga (clarify halt → Q1-Q4 rulings → root-cause amendment → FINAL "one key, one panel, zero dead code", 08-22 20:09→20:30Z); playbook-diet clarify halt (08-21).
- Reasoning: two independent arcs show rulings-as-process; the quotable acceptance standard ("a render function never called is not a feature") deserves canon status for any UI-wiring job.

## Watch items (anecdotes — tracked, not proposed)

1. **Directive-vs-question recall** (flow-focus 08-23): a user musing routed through Gru was dispatched over-eagerly; recall = park row + sweep + HARVEST the groundwork + spawn a skill-armed DISCUSSION minion the user talks to directly (checkpoints land in an artifact). High-value single sighting — if it recurs, promote.
2. **pi can silently omit an image attachment** (Gru, Dublin screenshot 08:58Z 08-23): the "visual read" was inference — check the session jsonl for the attachment before believing a blind-model read; flag inference in the same breath.
3. **escape = interrupt, ctrl+c = clear-editor** (Silas ops error 08-21, recovered): buffer hygiene on a WORKING pane is ctrl+c only.
4. **`gh pr diff` >20k-line API cap** (pace-tuning r1): reconstruct byte-exact via git + stats cross-check.
5. **Event-stream additions move T1 manifests with zero pixel delta** (sound-immediacy): budget the re-bless, prove purity via git status + divergence-tick alignment; live/replay must emit identical events at identical apply_tick.
6. **Shadow-clone prediction recipe** (spawn-feel): deep-copy ALL Run_State arrays + replay pending commands; pin with a hash round-trip.
7. **Odin `#load` embeds data at COMPILE time** (node-clarity): rebuild the harness after any palette/data-token edit or silently render old data.
8. **Calibrate a new gate on the OLD golden first** (node-clarity): reproduce known baseline numbers before trusting it; offline sims under-predict — screen with sim, settle with real renders.
9. **Tick-clamp rate derivation** (pace-tuning): effective rate = 1/ceil(1000/accrue), not accrue/1000; a global pace re-tune ripples into EVERY exact-tick pin (17 files/46 pins).
10. **pi extension authoring facts** (role-skills): jiti/static is ESM-only; extension load-test = neutral-cwd one-shot boot; discovery glob has no deep recursion (helpers in index.ts-less subdirs).
11. **Vision provenance facts** (vision-tooling): the auto models-store catalog may already declare image input (no override needed); `--no-session` writes NO jsonl — pin sessions by prompt text; (the missing vision-read symlink was fixed as direct ops 08-22).
12. **Diet craft** (playbook-diet): segmented line surgery beats full-file rewrites (they re-inflate ~950+); report the honest doctrine floor (713) flagged in the PR.
13. **Lavish verdict retrieval** (playbook-diet): check `~/.lavish-axi/state.json` sessions.<id>.chat when the poll returns dom_snapshot/0 prompts.
14. **Top-down look doctrine** (blender-sculpt): at ~60° elevation, two-tone ROOFS + proportional cast shadows carry depth; sub-roof massing = muddy stripes; coplanar plates z-fight (butt-joint).
15. **Blender-MCP exec chunking** (blender-sculpt): fresh globals per call — park helpers in driver_namespace, chunks <100 lines, partial-exec = clear-and-rebuild.
16. **Font pipeline traps** (font-overhaul): verify TTF magic bytes (a 404 HTML silently loads as fallback); loaders must FAIL LOUDLY; LoadFontData compacts glyph arrays (lookup by value, never index; never mix allocators).
17. **PP_CAM_E2E pattern** (camera-zoom): env-gated E2E harness for view-layer features — real Device_Events injected, screenshot after EndDrawing, pixel-scan before/after; architect view state as pure targets outside the sim loop → goldens byte-identical by construction.
18. **Odin const float arithmetic truncates** (noc-readability-2): `i32(360 * 1.4)` = 503, not 504 — int math for UI geometry.
19. **Impossible design ruling arithmetic** (noc-readability-2): show the math, implement the sanctioned alternative, document the deviation in the PR.
20. **Ledger-row race at dream dispatch** (dream-2026-08-21): a dispatch can arrive before its row — verify with `ledger show` before assuming.
21. **Self-report compliance is now the norm** (~6+ jobs): pr field set by minions, notifications shown:true, settle notes pre-emptive — Silas's verify step stays, but the failure mode has shifted from missing fields to over-trusting claims (see P6).

## Pruned / rejected candidates (with why)

- **Standing doctrine re-confirmations** (billing-block note-only signature ×~20; settle/echo classification ×15; sensor dedup ×8; recovered verdicts ×4; provenance pins; vision-caveat carriage; fickle-k3 ×2) — canon already covers each; this window only re-proved them at volume. The one NEW facet (minions pre-classify billing in their own PR bodies) shows the 08-19 briefing-signature fix worked — noted in sheep-ledger, no canon change needed.
- **KYLE spawn recipes as a standalone proposal** — folded into P10 (one KYLE addendum keeps the vision doctrine single-voiced).
- **heredoc/tr corruption + script-wrapper facets** — folded into P16 (one wrapper-failure entry).
- **LINE-alpha/SOLID-BLACK/swizzle facets already in canon** (08-11/13/15 entries) — P14 carries only NEW facets; duplicates dropped.
- **"Arc-level: play sessions are the requirements engine"** (sheep-journals #20) — true and quotable but already encoded as the fun-test gate + look-parity canon (08-20/21 rulings); no edit.
- **Singleton craft notes** (watch items 5-19) — below the ≥2-sighting bar; tracked as watch items per the evidence rule, not proposed.
- **Pane-id hand-typed slip #7** (noc-readability-2 row add 16:00Z) — the canon rule (variable-capture) already exists and was violated again; the fix pattern (sqlite UPDATE to the parsed move result) was applied same-minute. No new canon — documentation demonstrably doesn't stop this one; only the habit does.
