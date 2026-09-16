# sheep-journals — dream-2026-09-15 shard

Sources read fully: gru-journal/2026-09-13.md (post-marker = entries above `## 03:01Z — startup restored`),
gru-journal/2026-09-14.md (full), silas-journal/2026-09-13.md (post-marker = from the "marker advanced to"
bullet onward), silas-journal/2026-09-14.md (full). Marker: 2026-09-13T03:03:31Z. All quotes verbatim
(grep-verified). Note for Bob: two candidates below (plan-before-heist, grid-at-creation P3) were already
hot-applied to live AGENTS.md on 09-14 by Gru/Silas outside the dream — only the NEW nuances need folding.

---

### Second OpenAI quota hold — hold/flip/recovery doctrine rehearsed end-to-end
- Evidence: dream none; Gru journal 2026-09-14 (13:5xZ): User: "we are out of tokens with astra. openai." then "so we are back to glm fully." — "watchman Luna/Astra pins invalid; resume only on explicit user token confirmation."
- Evidence: Gru journal 2026-09-14: "Silas DIED on the cap mid-relay (Codex usage-limit error in pane); Gru revived same pane/session: /model glm-5.3-flash + /thinking high + continue — verified working."
- Evidence: Gru journal 2026-09-14 (14:4xZ correction): "the artist was NOT mid-extraction — the blender-music-video deliverable CLOSED before the cap (canonical row done 13:52:36Z)" — initial mid-flight assumption was wrong, Silas correction accepted.
- Sighting count: 2 (hold #1 2026-09-10, hold #2 2026-09-14; the 09-14 durable doc gained a "second-hold section")
- Why it matters: the flip is now a rehearsed checklist (identity panes in place, mid-relay deaths revived with one /model+/thinking+continue, in-flight rounds complete on launched model, resume ONLY on explicit user token confirmation — never probe-up); also: verify mid-flight-work assumptions before reporting them under a hold.

### Close-out sweep-race: daemons rooted in the worktree die at `worktree remove` — check lsof/ports BEFORE sweeping
- Evidence: Gru journal 2026-09-14 (16:1xZ): "GRU CAUGHT A SWEEP-RACE: Silas swept the worktree BEFORE re-rooting the gallery servers — both (8794/8795) orphaned on the deleted cwd, serving 404s" + "close-out sweeping order must honor preserve-first dependencies (servers rooted in the tree being swept)."
- Evidence: Silas journal 2026-09-14: "close-outs should check `lsof +D <worktree>` / listening-port daemons rooted in a worktree before `worktree remove --force` (pane sweep alone is insufficient — the 08-27 orphan-process class, media-server flavor)."
- Evidence: Silas journal 2026-09-14 (fix shape): "self-rooting serve.py copies at main (36168@8794, 36223@8795... restored 32 untracked mp4s from central preserve archives (rsync --ignore-existing" — self-rooting scripts from main, NOT a bare http.server at the media dir (would break the URL namespace).
- Sighting count: 1 (single sighting; sibling of the 08-27 orphan-process class)
- Why it matters: close-out enumeration must include non-pane daemons rooted in the tree (lsof +D / listening ports) and honor re-root-before-sweep ordering; central-preserve archives made recovery lossless.

### User-facing handover paths pointing INTO a worktree die at close-out — preserve-first + relay the new path
- Evidence: Silas journal 2026-09-14 (l1-spawn-awareness-37 close-out): "PRESERVE-FIRST catch: worktree held 4.3G untracked exports incl. the user's handed-over playable — preserved b40/b18/b30 self-contained builds (bundled Godot+project+PLAY.md each) + 56M capture evidence to implementation-artifacts/l1-spawn-awareness-37-exports-20260914/ BEFORE removal; playable path change relayed to Gru + verified."
- Evidence: Silas journal 2026-09-14: "Lesson reinforced: ACK handover paths pointing INTO a worktree die at close-out — either preserve-first + relay the new path, or hand over from a stable root (the skill-install note got this right on electric-loom: \"global alias targets stable root, not worktree\")."
- Sighting count: 2 (electric-loom media/skill alias, l1-spawn-awareness-37 playable exports; both 2026-09-14)
- Why it matters: any path handed to the USER (playable builds, aliases, links) must either live at a stable root or be relocated + re-relayed at close-out — the user's bookmarked artifact must not 404 after a merge sweep.

### Perkins round brief that FORBIDS formal posting violates the playbook — plus overnight close-out follow-through gap
- Evidence: Gru journal 2026-09-14 (PP3D #42): "The round brief EXPLICITLY forbade “PR comments, formal reviews, approval” alongside legitimate no-fix/no-merge rules. This contradicts playbook619–691: Perkins may APPROVE/REQUEST_CHANGES and must post/verify the review before done."
- Evidence: Gru journal 2026-09-14: "r2 row only marked done09:46:24Z (~8h28m after analysis finished), with no posted URL and result column stillNULL."
- Evidence: Gru journal 2026-09-14 (recovery): "reuse same r2/current SHA and saved artifacts, no new35-lens fleet; amend erroneous no-post restriction" — APPROVED eventually posted 10:03:02Z by perkins-review[bot].
- Sighting count: 1 (single sighting; new failure class — brief-authored scope error + ~8.5h posting gap)
- Why it matters: a Perkins round's brief may restrict FIXES/merges but never the canonical verdict posting; when posting fails/ls overnight, recover by reusing the same sha + saved artifacts, never a fresh fleet.

### glm-only round mains: 1302 deaths kill the MAIN, the wave survives — continue only AFTER settle; lens JSONs on disk are ground truth
- Evidence: Silas journal 2026-09-14 (r1 #45, 00:49Z): "main died on the launch-burst mid-orchestration; wave survived (6/7 working, security-c1.json landed); waited out the burst (5 min, no new deaths) then ONE continue — main working again. Ground truth used: lens JSONs on disk, never pane status."
- Evidence: Silas journal 2026-09-14 (01:02Z): "per-errored-turn continue spent at ~03:1xZ AFTER the wave fully settled — ALL 7 lenses x 2 chunks landed (14 JSONs on disk) while the main was down... 2h of main dead-time; the wake-up census caught it."
- Evidence: Silas journal 2026-09-14 (empty-lens recurrence): "security-c1/c2.json are 3-BYTE EMPTY (empty-lens class, generation 1): resume path = headless one-retry on security, else 6/7 DEGRADED-DISCLOSED."
- Sighting count: 2 main-deaths same night + 1 empty-lens pair (PR #45 r1); matches the 09-10 hold-#1 "~1 continue/round" tax
- Why it matters: under a glm-only hold the round main is the burst casualty while lenses complete — never re-dispatch, budget one post-settle continue, and check stalled rounds at the wake-up/startup census (the 2h gap was alert-queued-between-turns dead time).

### A Perkins main mid-`wave.py wait` is ALIVE — stuck-pane alerts on active async waits get NO nudge
- Evidence: Silas journal 2026-09-14: "r3 ... verified ALIVE by transcript: mid `wave.py wait` (4076s/5400s) after classifying a 1302 burst that killed architecture+tests lenses; will one-continue them after the wave settles per round input... NO nudge — active async wait."
- Evidence: Silas journal 2026-09-14: "Pending classification from the 15:57 stuck-pane alert (r3/p12K): legitimate long synchronous wave.py wait (not a wedge); lenses all 7 done; note-only."
- Sighting count: 2 (same r3 round, 14:40Z start and 15:57Z alert)
- Why it matters: transcript-verify before nudging — a main silently blocked in a long synchronous subprocess wait is healthy; continue-nudging it wastes a turn or corrupts the wave.

### Plan-before-heist ruling (user) — plus the in-chat lavish waiver nuance
- Evidence: Gru journal 2026-09-14 (evening): "we don't just go on heists on impulse. we plan properly before assigning minions. it's also why we have lavish." — ruling already recorded live in AGENTS.md + memory/plan-before-heist-2026-09-14.md (skip re-folding the core).
- Evidence: NEW NUANCE, Gru journal 2026-09-14: "Lavish page waived by user (\"we don't have to do lavish, if we are answering the questions here\") — forks settled in chat, plan doc carries the review."
- Sighting count: 1 ruling, applied immediately (pp3d-playtest-fixes-1)
- Why it matters: lavish is waivable BY THE USER in-chat when forks are being settled live — the durable plan doc then carries the review record; the waiver is user-ruled per-case, not a standing skip.

### Grid-at-creation gap for minion-spawned helper panes; resize surgery empirics; verify "husks" are husks before closing
- Evidence: Gru journal 2026-09-14 (user-flagged): "minion p13R at 22/230 cols (15-char line wrap), review layers p13T 50 + p13S 156, husk p13V 2 cols" — P3 extension to all spawn surfaces already recorded in AGENTS.md orchestration upgrades (skip re-folding).
- Evidence: NEW, Silas journal 2026-09-14: "All three non-minion panes verified LIVE review layers (p13V incl., 665K session — NOT a husk, no close-notes)" — the 2-col pane labeled a husk was live work.
- Evidence: NEW, Silas journal 2026-09-14: "herdr resize --amount = ratio-point DELTA on the addressed pane's edge boundary, --direction = pane GROWTH direction (p13S-left GREW p13S — first move inverted, recovered)."
- Sighting count: 1 (w85:tBP surgery; live round untouched, resize-only)
- Why it matters: never close a narrow "husk" pane without checking its session file; resize semantics: --direction names the pane's GROWTH direction, and mid-round surgery stays resize-only (1x4 even beats a forbidden 2x2 rebuild).

### Tool CALL ≠ RESULT; prepared briefs ≠ received mandates (forensics discipline)
- Evidence: Gru journal 2026-09-13 (Corrected Astra review): "EarlierGru“confirmedmutations”mistooktoolCALLforRESULT; correctedincidentmemory/briefandpublicwording."
- Evidence: Gru journal 2026-09-13 (GLM lens incident): "Gru public correction: earlier readPREPARED briefs andmistookthemforreceivedmandates; user'ssuspicionwasjustified."
- Sighting count: 2 (both 2026-09-13, PP3D constellation lane)
- Why it matters: claims about what an agent DID must rest on RESULT evidence (file diffs, session-jsonl results, gh state) — not on tool-call text, prepared prompts, or pane output that merely constructs receipts.

### Lens-wave model provenance: inherited PI_MODEL env overrides the launch pin on spawned lenses
- Evidence: Gru journal 2026-09-13 (user-caught): "Primary forensics verified5active non-blind sessions actuallyGLM/high despite parent17:06launchtool explicitlypinningAstra/xhigh. Silas subsequently reports inheritedPI_MODEL=glm-5.3/PI_PROVIDER=zai-coding-cn andglobalGLM/highdefaults"
- Evidence: Gru journal 2026-09-13: "Sessionfilenames17:06 butnewheaderids17:09." + reviewer write overlap: "p114editedliveorbit_camera.gd17:25:14; p112editedlivespec17:28:53; p111wrotetmpverificationhelper17:35."
- Evidence: Gru journal 2026-09-13 (recovery shape): "freshindependentAstra/xhighcontextsinexistingownedpanes... no blindrevert" — durable record memory/pp3d-r3-lens-model-and-handover-incident-2026-09-13.md.
- Sighting count: 1 full incident (extends the 09-07 env-beats-pin class to LENS spawns; user spotted it)
- Why it matters: lens panes inherit the round main's env — verify session modelId per lens (filename ≠ header id), contain only lens writers on overlap, rebuild contexts in owned panes, and keep blind diff-only.

### Look-ruling handling: brief-gap attribution, geometry-based discriminators, USER LOOK ACTIVE row protection
- Evidence: Gru journal 2026-09-13 (inset-framing verdict): "evidence is a specification/acceptance gap, NOT proof that individual lenses ignored their instructions. Gru owns correcting brief and review criterion, not fabricating a prior violation/verdict." + "Require geometry-basedcoverage discriminator that rejects currentinsetcase"
- Evidence: Silas journal 2026-09-13: "Updated the owning row with USER LOOK ACTIVE/no-sweep protection and relayed the ruling plus the actual `03-flat.png` path to pYQ and existing non-blind r3 lenses (edge/acceptance/architecture/codebase/tests); BLIND remained untouched/diff-only. All six deliveries were verified in their session JSONLs"
- Sighting count: 1 arc (multiple entries, constellation lane 09-13)
- Why it matters: when a user look-verdict exposes a miss, first check whether the BRIEF encoded the criterion (fix the brief, don't blame the lenses); look acceptance needs a geometry-based discriminator, and mid-look amendments go to non-blind lenses only, delivery verified per session jsonl.

### Healthy long renders are NOT killed for arbitrary internal timeouts (user ruling, SELVA-scoped)
- Evidence: Gru journal 2026-09-13: User: "we waited for 2 weeks to get a blender alternative, and we were still on the first scene. so we can wait for video gen. i'm not sure why there is a time limit."
- Evidence: Gru journal 2026-09-13: "healthySelvageneration is NOT killedforarbitrary8h/earlyETA... Finiteobservationwindows canendwithoutkillinghealthyworker." (scope SELVA only; does NOT override Godot bounded-capture safety)
- Sighting count: 1 (single sighting)
- Why it matters: internal 8h allocations are not human walls — a finite observation window may end without killing the healthy worker; genuine memory/disk/failure/user-stop safeguards still apply.

### User "curiosity" questions are read-only — explicit do-not-interrupt
- Evidence: Gru journal 2026-09-13 (16:18Z): User: "do not interupt the existing download in progress. i'm just curious'. Read-only inspection ONLY; no pane input, signal, restart, configuration or download change."
- Sighting count: 1 (single sighting)
- Why it matters: a user QUESTION is not an action authorization — answer from records/inspection only, never signal/restart/touch the live work the question is about.

### %-completion reporting: hard deliverable counter + labeled planning estimate, both, never inflated
- Evidence: Gru journal 2026-09-13 (15:40Z): "Report baseline: approximately30% whole-project completion, explicitly a rough milestone-weighted planning estimate, NOT measured percent footage/time remaining." + "Hard deliverable counter remains0/55shots=0% finished footage; report both, never inflate from checks/receipts/restarts."
- Evidence: Silas journal 2026-09-13: "Completion metric correction recorded from Gru's 15:40Z report... The roughly 30% figure is a planning estimate, not finished-footage completion."
- Sighting count: 1 arc (user ask "give me a % completion report")
- Why it matters: the dual-metric format (0/55 hard counter + labeled weighted estimate) is the sanctioned answer shape for "where are we / what %" — restarts, checks and receipts never raise the number.

### Ledger WORKING is not execution evidence — recurrence; recovery = concrete next step in the SAME session
- Evidence: Gru journal 2026-09-13 (12:22Z): "Ledger stillWORKING is not execution evidence." (pYR DONE ~50min, row WORKING)
- Evidence: Gru journal 2026-09-13 (15:40Z): "current paneDONE, not working despite ledger" (session ended in WebSocket/SSE/fetch errors 14:43–15:05Z)
- Evidence: Gru journal 2026-09-13 (Loom entry): "Read-onlycensusalsofoundL1#37owneragentdonewithrowworking/PRnullafterinternalreview; sentSilastoinspectasync/usergateandifnone deliverconcretetriage" (recovery: next step delivered in the existing session)
- Sighting count: 3 new (2026-09-13) on top of the consolidated 09-12 gotcha (dream-2026-09-13)
- Why it matters: the 09-12 "row status and final prose are not activity" class is still firing daily — check session growth + pane state, then deliver the concrete next step in the SAME session rather than re-dispatching.

### Approval-pause on ordinary in-scope repair is not a user gate; relay transport failures must not become silent local decisions
- Evidence: Silas journal 2026-09-13: "The pane then paused awaiting approval, but the 2026-09-12 human factory mandate makes this ordinary in-scope repair autonomous."
- Evidence: Gru journal 2026-09-13 (12:22Z): "his relay to literal `gru` failed pane_not_found, then he printed the question locally rather than delivering it to actual Gru w85:p1."
- Sighting count: 2 (12:22Z Selva pause + the failed-relay flavor; PP3D 12:36Z sibling below)
- Why it matters: routine assertion failures mid-mandate continue autonomously; and a failed pane relay (wrong label) must surface/retry to the real pane — printing locally strands the escalation.

### role:user CAN be genuine human input — a direct typed `retry` superseded a BLOCKED row
- Evidence: Silas journal 2026-09-13: "the old closeout tail was followed by a direct role=user `retry` at 16:54:15Z, and pYQ began active cleanup/retry preparation... Corrected the PP3D ledger BLOCKED->WORKING to match the live retry"
- Sighting count: 1 (single sighting; the INVERSE of the pre-marker pYR incident)
- Why it matters: the transport-label doctrine cuts both ways — role:user is neither proof of human origin NOR proof of agent origin; verify content/context against the originating session, and a live user retry overrides a stale BLOCKED disposition.

### Attribution discipline: internal dispositions are not human authority; "Gru application of existing mandate" ≠ new ruling
- Evidence: Gru journal 2026-09-13 (12:36Z): "This is an internal disposition carried into Gru startup, not an independently established new user prohibition." + "Wrote briefings/pp3d-post-audit-parent-continuation-2026-09-13.md as Gru application of existing Sep12 factory mandate, NOT a new human approval."
- Evidence: Silas journal 2026-09-13: "Attribution correction: the repair04 continuation direction was Gru/CEO operational application of the existing 2026-09-12 human factory/autonomy ruling, not a new 2026-09-13 human-origin ruling."
- Sighting count: 2 (12:36Z PP3D hold provenance, repair04 attribution; extends the consolidated ≥3 corrections of 09-12..13)
- Why it matters: provenance-check "user forbids/paused" claims before acting on them; carry corrections as dated applications + AUTHORITY-CORRECTION side files, preserving original history.

### Failed Auto-compacting death: continue insufficient → kill ONLY the owned PID, same pane/tree relaunch, FULL handoff re-delivery
- Evidence: Silas journal 2026-09-13: "Selva pYR remained idle in failed Auto-compacting with no old-session growth after its one continue; only owned PID52661 was killed, same pYR/tree relaunched on Astra/xhigh, and full handoff delivered. New Selva session grew to 38,585 bytes and is WORKING."
- Sighting count: 1 (single sighting; new trigger flavor for the 08-20/21 wedged-pi kill-pid recovery)
- Why it matters: a pi stuck in failed auto-compaction does not respond to continue — the recovery is the kill-pid path scoped to the OWNED pid only, then same-pane relaunch with the full context handover re-delivered and verified by session growth.

### Provider-paused rows: BLOCKED with resume-on-probe-UP + one-continue triggers; expired allocations close honestly, never replay
- Evidence: Silas journal 2026-09-13 (14:05Z): "Both parent rows were moved WORKING->BLOCKED as provider-paused, with exact resume-on-Astra-probe-UP plus one-continue triggers; all partial/RED evidence preserved."
- Evidence: Silas journal 2026-09-13 (15:05–15:43Z): "both lanes hit provider-error tails and were closed honestly, not marked complete... `CLOSEOUT-EXPIRED.json` records host-only expiration... No old-allocation native continuation"
- Sighting count: 1 window (2 rows: Selva correction33, PP3D execution09)
- Why it matters: implementation parents use the same probe-gated park doctrine as Perkins rounds; deadline expiry gets an honest CLOSEOUT-EXPIRED receipt — expired wall-time allocations are never replayed or reported as completions.

### Scoped weight-deletion authority: named weights only, receipts, no Trash, verified byte deltas; path-depth + lsof-scope corrections
- Evidence: Gru journal 2026-09-13: User: "delete the models i need the space." — "noTrash/backupcopiesbecauseactualspacewanted" ... "69025269069weightbytes removed, actualfree-space delta64.285442GiB" (receipts/MODEL-REMOVAL-20260913.json)
- Evidence: Gru journal 2026-09-13 (ops-audit correction): "root.parents[4] pointsALLyoutubechannelworktrees, exactAIworktree isparents[3]; whole-machineperPIDlsofisoverbroad/slow"
- Sighting count: 2 (LTX removal "remove LTX. let's download Wan", Wan-weights deletion; both 2026-09-13)
- Why it matters: deletion asks mean actual space — no Trash/backups, quiescence+symlink checks first, byte-delta receipts after; and scope lsof to the EXACT worktree path depth (parents[3] not parents[4]) instead of whole-machine per-PID scans.

### Storage-gate escalations quantify the exact deficit and give concrete options — never silently delete or substitute
- Evidence: Silas journal 2026-09-13 (16:42Z): "faithful BF16 MLX Wan2.2 I2V-A14B needs 69,046,724,728 bytes (64.305GiB), leaving a 44.600GiB deficit above the 32GiB reserve; official conversion is at least 181.8GiB peak."
- Evidence: Silas journal 2026-09-13: "user must choose >=44.600GiB additional local free space without deleting protected caches, or persistent writable external storage with conservatively >=96.305GiB free."
- Sighting count: 1 (single sighting)
- Why it matters: when capacity gates a mandated acquisition, escalate the exact deficit + option set (free X / external Y) — the user then rules (they chose scoped LTX removal); no quantized-model substitution, no protected-cache deletion, no waived reserve.

### Same-row amendments for creative-lane continuations; "deferred" = a named owed deliverable ON the row
- Evidence: Gru journal 2026-09-13 (six-loop commission): "SAME `youtube-channel-selva-electric-loom` row /w9Z:p1 owner/tree" + "Silas moved the just-closed look row back todispatched for the same-owner extension."
- Evidence: Gru journal 2026-09-14 (skill extraction): "The skill is an explicit owed deliverable on SAME row, not an orphan “later” task."
- Sighting count: 3 (loom→six-loop, MV→skill, six-loop→full-MV; all same owner w9Z:p1)
- Why it matters: follow-on work on the same asset rides the SAME row/owner/tree via a top-linked amendment (avoids duplicate dispatch), and anything "deferred" must be a named deliverable recorded on the row — extending the 09-04 deferred-must-be-a-row ruling.

### Top supersede pointers on briefs so old prohibitions cannot quiet-park a new mandate
- Evidence: Gru journal 2026-09-14 (full MV): "Current comparison brief has a top supersede pointer so old no-full-song text cannot quiet-park the owner."
- Evidence: Gru journal 2026-09-13 (Loom exception): "HistoricalstopbriefTOPclarifiesnewLoomexception: oldnarrative/AIrowsstaystopped/no reacquisition; newjobcannotblockedbyoldblanketstop."
- Sighting count: 2 (both Selva lane, 09-13/09-14)
- Why it matters: when a new mandate contradicts an older blanket prohibition, write the exception/supersede at the TOP of the controlling brief — otherwise the stale text stalls the owner mid-heist.

### User stops: lane-scoped supersede-all, recorded as creative choice not viability proof; "archive" = evidence outside the project, no dead code
- Evidence: Gru journal 2026-09-13 (Selva video stop): User: "stop the video gen. i think at this point in time. blender and local a.i gen are not viable." — "Recordcreative/resourcechoice, NOT universalproofthattoolsareunviable." + "ExplicitSTOP supersedes all earlierwait/no-time-limit/480p/diagnostic/factory-resumeauthority forSelvavideo"
- Evidence: Gru journal 2026-09-13 (constellation cancel): User: "by archived what happens? we dont want dead code" — "Archiveclarifiedto user/Silas: compactpatch/history/evidence OUTSIDEactiveGodotproject, notfeatureflags/dormantclasses/tests/assets"
- Sighting count: 2 stops same day (Selva video lane, PP3D constellation mode); Silas 09-14 confirms both survive as deliberate DEFERRED holds across restarts
- Why it matters: a stop supersedes ALL earlier authorities for that lane only (no cross-job stop); "archived" means compact evidence outside the active project — never dormant flags/classes left in-tree.

### High-frequency direction pivots handled amend-and-relay — ~6 Selva pivots in one day, zero re-dispatches
- Evidence: Gru journal 2026-09-13 chain: MLX pivot 15:49Z → Wan switch 16:31Z ("switch the video gen model") → LTX removal authorization → full stop 19:32Z → weight deletion → Loom selection → six-loop commission — each via durable brief amendment + same-row/same-owner relay.
- Sighting count: 1 day, ~6 reversals (strengthens the consolidated 08-07.. mid-flight-reversal gotcha)
- Why it matters: the healthy reversal form at full speed — brainstorm/consult first (kinetic-loop discussion preceded the Loom heist), amend the controlling brief, relay to the same owner, record durable memory; kill-and-redispatch never needed.

### Skill extraction from a delivered artifact: artifact FIRST, generic-skill hygiene, runtime corrections fold into tests; notification-gap flavor
- Evidence: Gru journal 2026-09-14: User: "can the minion make this into a skill , with scripts so we dont have to burn tokens to repeat this for future videos" — "Deliver that artifact FIRST; do not pause/re-render it for extraction." + "No Selva paths/duration/palette/pane IDs buried in generic code; no mandatory six-look bakeoff every song."
- Evidence: Gru journal 2026-09-14 (QA): "Current MV QA caught a native MP3 start-read offset; owner is testing cached-audio handling, not concealing it with a trim/fade."
- Evidence: Gru journal 2026-09-14: "Silas also owned a notification gap (no explicit completion line pushed to Gru's pane; receipts had gone to ledger + user chat only) — corrected by his relay." (lane closed clean: 28 files byte-verified, 32 tests, 0 diagnostics, /skill: discovered from foreign cwd)
- Sighting count: 1 (blender-music-video skill, 2026-09-14)
- Why it matters: token-saving skill extraction is a commissioned deliverable with an ordering rule (deliver the artifact first) and hygiene rules (no project-specific paths baked in; real runtime corrections become reusable tests); and receipts to ledger+USER CHAT do not count as delivered-to-Gru — the pane relay is still owed.

### Full-MV finishing trap: display-referred source needs a short roundtrip check before any retag
- Evidence: Gru journal 2026-09-14: "source movie is already AgX/display-referred with sRGB transfer and709 primaries/matrix. Native VSE short roundtrip first to catch double tone mapping/incorrect range/transfer; do not merely retag."
- Sighting count: 1 (single sighting, craft-level)
- Why it matters: when re-editing rendered movie output in Blender VSE, verify color management with a short roundtrip test first — double tone mapping is silent and ruins the full export.

### Media-to-main via tracked PR; untracked residue centrally preserved; servers re-rooted only after the user merge
- Evidence: Gru journal 2026-09-14: User: "open a PR. for the local videos and images they have to be moved to main at some point even if they are not tracked. we can't leave them in a worktree." — "233 media files ALREADY TRACKED in the branch (full MV, thumbnail, loops, blends, QA frames) — merge itself moves deliverables to main; untracked/ignored remainder is transient"
- Sighting count: 1 (electric-loom close-out, PR #4)
- Why it matters: creative-lane deliverables must reach main through a tracked-media PR (pr_review=0, user merge click); transient untracked residue gets central preservation, and tree-rooted services re-root AFTER the merge (see sweep-race candidate).

### Research lanes: official-source distinctions, hypotheses-not-winners, explicit user disposition recorded
- Evidence: Gru journal 2026-09-14 (thumbnail CTR): "Strict research tally0 independently verified/10 unverified means no independent replication, NOT unchecked sources." + "Recommend assembled control/exploded/partial-exploded as hypotheses, not guaranteed winners"
- Evidence: Gru journal 2026-09-14: "FINAL USER DISPOSITION: “no, it's fine we leave it as it is.” Keep current thumbnail; no variants or platform experiments. Research brief amended"
- Sighting count: 1 (youtube-channel-thumbnail-ctr-research-20260914)
- Why it matters: research briefs pin what official sources actually say vs proxies, label recommendations as hypotheses, and END with the user's recorded disposition + amended brief — an unacted research lane must close, not linger.

### Backlog intake with scope fences written INTO issue bodies
- Evidence: Gru journal 2026-09-14: "the top-right stats chip stays a compact chip and must NOT grow into a dashboard in this heist." + "#43 NOC dashboard section (parked, design consult deferred; stats chip fence written into the body)"
- Sighting count: 1 (PP3D #43/#44 intake, 2026-09-14)
- Why it matters: when a future feature is parked as an issue, write the active-lane scope fence into the issue body itself — the fence must travel with the backlog item, not live only in the current briefing.

### Dream-dispatch hygiene: the dream template's model line rots — correct per current regime before handover
- Evidence: Silas journal 2026-09-14: "briefing filled from template with the model line CORRECTED (template said stale kimi; hold #2 → glm) + grid-at-creation instruction for the sheep fleet added."
- Evidence: Silas journal 2026-09-13: "Template was filled and corrected for the current dated OpenAI quota-hold: Bob/sheep use `zai-coding-cn/glm-5.3` at max, verified in the new session"
- Sighting count: 2 (dream-2026-09-13, dream-2026-09-15 dispatches)
- Why it matters: extends the briefing-model-line-rot gotcha to the DREAM template specifically — Bob/sheep model lines must be re-pinned at every dream dispatch under a hold, and session-verified after launch.

### Husk worktrees with no row/pane escape ledger sweeps; branch -D failing = a worktree still pins it
- Evidence: Silas journal 2026-09-14: "Extra husk found: worktree `selva-pr-media-clean` (no ledger row, no pane) held branch selva-electric-loom-clean checked out — verified 300d278 contained in main + status clean, then removed husk + branch -D. Branch-delete-first-failure was the worktree pin, not divergence."
- Sighting count: 1 (single sighting)
- Why it matters: worktree censuses must include `git worktree list` (ledger+pane sweeps miss husks); when `branch -D` fails, look for a pinning worktree before suspecting divergence — and verify containment+clean before removing.

### Unbranded ACKs: verify content against ground truth before ANY ledger action
- Evidence: Silas journal 2026-09-14: "NOTE: ACK arrived in my pane unbranded (no [GRU]/[MINION] prefix) — treated as the round main's closing report and verified against gh before ANY ledger action; content provenance held regardless of transport label."
- Sighting count: 1 (r3 close, review 5200796464)
- Why it matters: the [GRU]/[MINION] prefix convention is advisory — when branding is missing, verify the CLAIM (gh/API/files) before mutating ledger state; branding presence alone is also not proof.

### Per-PR split model override: mechanical work on glm-5.3@max, narrow vision checks stay Astra@xhigh, with a suitability clause
- Evidence: Gru journal 2026-09-14 (PR #42 warning fixes): User: "let's fix them. we can use glm5.3 for these. unless they don't fit the criteria." — "GLM5.3@max for specified mechanical implementation/helpers AND canonical mechanical Perkins round/lenses; narrow real-image HUD/focus verification remains Astra@xhigh. Not a global model ruling or a blind visual verdict."
- Evidence: Silas journal 2026-09-14: "fresh PR42 fix-audit rounds already pinned glm-5.3 @ max per the scoped user override." + visual leg "PARKED under the OpenAI hold (narrow real-image HUD/focus check stays Astra@xhigh — deferred, not waived)"
- Sighting count: 1 (pp3d-pr42-warning-fix; extends the 09-12 per-PR override doctrine with split routing)
- Why it matters: user model overrides can route BY WORK TYPE within one PR (mechanical vs vision) and carry an "unless they don't fit" suitability clause — apply narrowly, park (don't waive) the vision leg, and never generalize to a global ruling.

---

End of shard — sheep-journals, dream-2026-09-15.
