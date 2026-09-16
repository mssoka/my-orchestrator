# sheep-ledger shard — dream-2026-09-15

Source: `_bmad-output/memory/dream-2026-09-15/ledger-dump.txt` (12 jobs with activity
since 2026-09-13T03:03:31Z). All quotes verbatim from ledger notes (grep-verified
against the dump). Rows covered: constellation-view-v2 (+perkins-r2),
selva-electrica-assets-rigs, selva-mlx-ai-production, l1-spawn-awareness-37
(+perkins-r1/r2/r3), selva-electric-loom, thumbnail-ctr-research,
pp3d-playtest-fixes-1 (+perkins-r1).

## A. Authority & provenance

### Attribution corrections: Gru applications of prior rulings get re-labeled as non-human
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-13T00:50:57Z — "ATTRIBUTION CORRECTION 2026-09-13: the prior event labeled HUMAN RULING 2026-09-13 was Gru/CEO operational application of the existing 2026-09-12 human factory/autonomy ruling, not a new human-origin instruction."
- Sighting count: 3 (selva-electrica-assets-rigs 2026-09-12T20:47:02Z, 2026-09-13T00:50:57Z; constellation r2 audit flags "R2-W3 unsupported human-origin attribution in ledger event6017")
- Why it matters: future sessions must reserve "HUMAN RULING" for verified human-origin text and label Gru applications as dated applications — mislabeled authority propagates into review findings.

### Assistant toolcall relay misread as user stop → wrongful pane kill (the pYR incident, ledger side)
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-13T00:12:06Z — "CORRECTION: prior 2026-09-13 Selva STOP was not user-authorized. pYQ session 01a0954e-8ed9-7700-9619-3c3c1ba7b261 event9157beb9 at00:03:26.359Z was an ASSISTANT bash toolcall herdr pane run w85:p2 carrying PP3D closeout text; Herdr TUI injection made it appear role:user."
- Sighting count: 1 full kill+restore cycle (stop 00:05:12Z, correction 00:10-00:12Z, sibling PROVENANCE RULE note on constellation @ 00:18:00Z)
- Why it matters: never stop/kill a sibling lane from pane role=user text; provenance is proven from the ORIGINATING session jsonl (assistant toolcall id), and false records stay preserved but superseded via AUTHORITY-CORRECTION side files.

### Direct user input to a minion pane IS legit authority when session forensics confirm it
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-13T16:56:01Z — "session forensics then showed a new direct role=user input `retry` at 16:54:15Z. The pYQ agent is now actively preparing a native retry/cleanup turn; no Silas continue or kill was sent and no native child was visible at last process probe."
- Sighting count: 1 (constellation retry); contrast class with the pYR misread above
- Why it matters: the distinguishing test is origin-session forensics (timestamps + routing), not the receiving pane's role label — both directions verified this window.

## B. Model / provider routing

### MODEL PROVENANCE INCIDENT: inherited PI_MODEL env silently mis-routes lens waves despite explicit --model pin
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-13T17:51:49Z — "MODEL PROVENANCE INCIDENT 2026-09-13: actual r3 lenses p112/p00/p111/p114/p115 recorded zai-coding-cn/glm-5.3 at high despite pYQ launch command explicitly pinning openai-codex/gpt-6-astra xhigh."
- Sighting count: 1 wave (5 lens panes); root cause confirmed: "Live p0Z shell probe proved inherited PI_MODEL=glm-5.3 and PI_PROVIDER=zai-coding-cn; ~/.pi/agent/settings.json independently defaults to glm-5.3/zai/high."
- Why it matters: a launch-command model pin is NOT sufficient — lens spawn surfaces must clear PI_MODEL/PI_PROVIDER or the whole review is invalid for its intended tier ("GLM outputs are invalid for Astra approval"); corrected relaunch on same panes with frozen diff-only guard preserved the round.

### In-place /model correction BEFORE any lens output, no re-dispatch
- Evidence: packet-plumber-3d-constellation-view-v2-perkins-r2 @ 2026-09-13T02:33:23Z — "MODEL CORRECTION 2026-09-13 per Gru/CEO operational policy: initial p0Q GLM-5.3/max launch was caught before any lens pane/output; it performed preparatory reads only."
- Sighting count: 1 (plus the r3 lens-wave flavor above as the caught-too-late variant)
- Why it matters: wrong-model launches are recoverable in place when caught pre-output — verify modelId+thinkingLevel in session JSONL, correct round-input + jobs.model, credit nothing from the wrong-model prep.

### Quota-hold BLOCK + probe-gated single continue (Astra DOWN window 09-13 14:06Z)
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-13T14:08:28Z — "QUOTA-HOLD 2026-09-13T14:06Z: execution09 entry01 is not a clean completion." … and recovery @ 14:18:16Z — "CONTINUE RECOVERED 2026-09-13: Astra probe returned OK and the single permitted continue resumed the same pYQ session."
- Sighting count: 2 rows same window (constellation execution09 + selva correction30/33); selva flavor @ 14:17:33Z: "The single permitted continue was sent after the provider flip, but pYR remained idle in Auto-compacting with no session growth; this is a genuine wedged-pi recovery"
- Why it matters: provider-down blocks park with a named resume trigger (probe-UP → exactly one continue); if the continue fails on a wedged/Auto-compacting pane, escalate to kill-owned-pid + same-pane relaunch, never loop continues.

### 1302 launch-burst kills glm round mains ~1-2x/round; one continue per death after settle
- Evidence: packet-plumber-3d-pp3d-playtest-fixes-1-perkins-r1 @ 2026-09-15T00:57:21Z — "died on a 1302 launch-burst (stopReason error, retry-failed x3) mid-wave-1 orchestration — the expected ~1x/round glm class."
- Sighting count: 2 deaths in one round (00:49Z + 01:02:51Z; second continue "spent at 03:1xZ after the wave FULLY settled")
- Why it matters: budget ~1-2 continues per glm Perkins round; never re-dispatch, never model-flip mid-round; a continue landing mid-burst doesn't clear — wait for settle.

### OpenAI hold #2: in-place pane flips Astra→glm-5.3@max, visual legs deferred with named resume
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T14:38:25Z — "OPENAI QUOTA HOLD #2 (user ruling 2026-09-14, GPT chain suspended not retired): artist pane w9Z:p1 flipped in place Astra->zai-coding-cn/glm-5.3 @ max; session events verified model_change 14:36:45Z + thinking max 14:36:48Z."
- Sighting count: 2 surfaces (loom artist flip; l1-spawn r3 "Astra visual leg DEFERRED under OpenAI hold (resume = explicit user token confirmation)" + fix-go on glm)
- Why it matters: hold-era pattern is now repeatable — flip in place with event-verified model_change/thinkingLevel, park visual/aesthetic verification with an explicit resume trigger (user token confirmation), keep code/testing moving on glm.

## C. Perkins / review loops

### Full loop-until-APPROVED cycle: r1 blockers → remediation → r2 APPROVE → user fix-go on warnings → r3 → user merge
- Evidence: packet-plumber-3d-l1-spawn-awareness-37 @ 2026-09-14T17:43:57Z — "PR #42 MERGED 17:41:21Z (merge 4102a82) after Perkins r3 APPROVE (review 5200796464, loop satisfied)."
- Sighting count: 1 complete cycle (~19h dispatch→merge; r1 23:03Z 09-13 → merge 17:41Z 09-14)
- Why it matters: the healthy shape end-to-end: exact-SHA rounds, prior_findings carried, "HOLD r2 until owner freezes and pushes a new SHA" (00:04:14Z), APPROVE ≠ merge ("Merge decision = USER (human-only merger)" @ 17:28:30Z), warnings routed to user-directed follow-ups not silent merges.

### Sensor-gap fallback: manual round completion when the watcher never fires
- Evidence: packet-plumber-3d-l1-spawn-awareness-37 @ 2026-09-14T09:46:25Z — "R2 completed manually because the watcher did not produce a fresh activation relay during this cycle: 5/5 waves, 35/35 Astra xhigh lenses, 0 failed layers;"
- Sighting count: 1 (r2; overnight gap 00:26Z dispatch → 09:46Z manual completion)
- Why it matters: never wait on the sensor — the completion sweep fallback (dispatch at stable head when no round row exists) is load-bearing; formal review then posted from complete artifacts with no rerun.

### Empty-lens 3-byte JSONs recur under glm; one retry then 6/7 DEGRADED-DISCLOSED
- Evidence: packet-plumber-3d-pp3d-playtest-fixes-1-perkins-r1 @ 2026-09-15T03:09:11Z — "security-c1.json + security-c2.json are 3-BYTE EMPTY (empty-lens class, generation 1 — headless mode's one-retry on resume, else 6/7 DEGRADED-DISCLOSED per doctrine; an empty-lens verdict never ships)."
- Sighting count: 1 round this window (2 lens JSONs, one generation)
- Why it matters: wave-state ground truth is lens JSONs ON DISK (byte size), never pane status; the empty-lens standing trigger (3rd straight generation → intervene) still applies.

### Stale sensor/pane echoes answered with same-status notes, never second actions
- Evidence: packet-plumber-3d-pp3d-playtest-fixes-1-perkins-r1 @ 2026-09-15T00:45:05Z — "00:42:13Z Perkins-sensor fire = STALE ECHO racing the manual dispatch (row pre-added 00:43 with parent + sha=662f408eae070741bbef4221c158111112c18d8c in the note COLUMN — dedup query satisfied; round live on w85:p13W). No second dispatch."
- Sighting count: 2+ (also l1-spawn r3 @ 17:31:15Z "STALE ECHO racing the 17:26-27Z close-out"; plus ~30 watcher-classification notes across all rows)
- Why it matters: pre-adding the round row with parent + full sha in the note COLUMN silences the dedup query even when added seconds AFTER the fire; every echo gets a note, never a second dispatch.

### WATCHER CLASSIFICATION as routine same-status discipline (density record)
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-09T13:29:04Z — "WATCHER CLASSIFICATION 2026-09-09 09:25Z/09:35Z/10:18Z/10:43Z: pNE pane working->done is a completed bounded S47 diagnostic/source-asset turn, not full-film job completion, clarify halt, or provider error."
- Sighting count: 30+ events across 8 rows this window (settle-noise, finished-bounded-turn, stale-echo, restart/boot flavors)
- Why it matters: classification-by-pane-read before action is now the default ops rhythm; batched multi-timestamp notes (one note covering 4 alerts) keep the ledger readable.

### Synchronous wave-wait flat session is NOT a wedge
- Evidence: packet-plumber-3d-l1-spawn-awareness-37-perkins-r3 @ 2026-09-14T16:12:39Z — "STUCK-PANE alert 15:57Z classified NOT-A-WEDGE: main (w85:p12K) inside deliberate synchronous wave.py wait (5400s timeout, ~4076s elapsed at 15:55Z read) after a 1302 burst killed 2 lenses;"
- Sighting count: 1
- Why it matters: a round main inside a long bash toolcall shows zero jsonl growth by design — check what the main is waiting on before sending continues or killing.

### Same-session audit independence limitation disclosed honestly
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-13T00:55:11Z — "Independence limitation: this is a fresh evidence reassessment in the retained authoring session as explicitly requested, NOT a separate reviewer identity or external sign-off."
- Sighting count: 1
- Why it matters: same-session "independent" audits must disclose they aren't a separate reviewer identity; truncated handoff SHAs get reconciled through sealed bindings ("Supplied63hex SHA corrected explicitly to sealed64hex endingf2." @ 00:22:23Z) rather than silently accepted.

## D. Stop-on-surprise / native gates (PP3D)

### Import stop-on-surprise: rc0 with unexpected diagnostics still STOPs
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-12T09:11:21Z — "Native sequence STOP: counted import 1/1 returned rc0 in 85.121s but unexpected diagnostics outside #29: custom Nunito font no loader/error loading (lines3/5), translation locale warnings lines2651-2679, CanvasItem/ObjectDB/TextServer RID leaks lines4088-4093."
- Sighting count: 3 import entries (import-01 STOP, import-recovery-02 FAILED, verbose diagnostic-03 NON-GREEN), each escalating evidence without waiver
- Why it matters: exit-0 ≠ green under the bounded-run grant; each retry was a NEW disclosed grant with deeper instrumentation (verbose run named the retaining resource: "Resource still in use res://assets/fonts/nunito-variable.ttf; leaked FontFile refcount6").

### Local _bmad facade repair for locale-warning ingest (repeat confirmation)
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-12T11:14:30Z — "real local _bmad contains OWN .gdignore and 12 top-level forwards. Shared target non-following manifest242 entries byte/metadata unchanged;"
- Sighting count: 1 repair (symlink inode preserved verbatim; also pre-bootstrapped on playtest-fixes dispatch: "_bmad facade silences locale ingest, godot import clean")
- Why it matters: the facade pattern is now standard pre-flight on fresh PP3D worktrees — prevents the CSV-as-translations diagnostics class before it fires.

### Frozen allocation contracts: mode0444 allocation.json, STOP on drift, honest WALL RED
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-12T22:50:56Z — "gate is RED solely for allocation.json protected-source drift during the run. Dynamic census removed from allocation authority; allocation.json now frozen mode0444 SHA a38eb264515417e4e4dd4caee518ac5bd633a958f570b596094c55ef5b900a9b."
- Sighting count: 3 flavors (drift-RED + freeze fix; execution07 "ALLOCATION WALL RED, late seal explicit" @ 00:05:36Z 09-13; two EXPIRED-CLOSEOUTs below)
- Why it matters: allocation authority must be immutable during the run it governs; wall-deadline misses are reported RED honestly, never back-dated or quietly sealed.

### EXPIRED-CLOSEOUT: honest close after absolute deadline expiry
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-13T15:44:35Z — "EXPIRED-CLOSEOUT 2026-09-13T15:43Z: correction33 host stage closed honestly after its absolute deadline 15:23:53.095398Z." (twin: constellation "execution09 closed honestly after its absolute deadline 15:42:48.537980Z" same minute)
- Sighting count: 2 (both rows, same Astra-down afternoon)
- Why it matters: when provider-down eats the window, close with CLOSEOUT-EXPIRED.json + fresh-allocation-required note instead of pretending completion; counters/RED history stay immutable.

### Honest overrun accounting, never rewrite history
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-10T09:44:21Z — "[pP5 ACCOUNTING CORRECTION] My preceding relay incorrectly said within20min. Immutable closeout91fca8cc truthfully records1200.065973s against the conservative09:24:00 start/deadline09:44:00:0.065973s over the declared new host cap; time_caps_compliant=false."
- Sighting count: 2 (this + "old 34343B breach remains" carried in later Selva accounting notes)
- Why it matters: relays that overstate compliance get corrected by appending truth against the immutable receipt, preserving the conservative deadline choice — overruns stay red flags in cumulative accounting, not noise.

### User cancellation flow: archive → containment check → worktree retire → row stays blocked
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-13T18:35:07Z — "Merged-main read-only check before removal: origin/main=39d82d0632ca2b0b1b4bd190a089e0f5444e20aa contains normal L1 files and historical constellation docs, but no runtime constellation_view/world_morph/request_flat/flatness implementation. No narrow removal delta required;"
- Sighting count: 1 (constellation cancelled:user; mlx row uses the same deferred=cancelled:user shape)
- Why it matters: cancellation preserves evidence to no-pr-evidence/, checks main containment before any removal, retires worktree/branch, and leaves the row blocked with successor linkage (tiny-planet issue #37) — never `done`.

### no-pr-evidence archives with parent-seal child dirs under concurrent writers
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-12T11:22:02Z — "Parent seal child avoids overwriting Silas concurrent preservation."
- Sighting count: 4+ archives in one row (import-01, import-recovery-02 + parent-seal-01, diagnostic-03, execution-08, cancelled-constellation)
- Why it matters: the hash-verified central archive pattern is now the default parking spot for every halt/stop/cancel; child dirs prevent two writers clobbering one archive path.

## E. Selva lane process shapes

### Locale drift breaks process-identity guards (LANG/LC_ALL + trailing whitespace)
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-10T01:44:17Z — "locale-only mismatch PRESENT across assigned PID41430/99824/8925. Host LANG=en_GB.UTF-8 vs MCP LANG absent; Pair1 Thu10Sep vs ThuSep10; other visible identity fields match."
- Sighting count: 2 guard-failure flavors (locale drift; @ 09:44:00Z "recorded census rejected new parser on trailing whitespace in16 unrelated ssh/pi process titles")
- Why it matters: ps-based identity comparators must pin LC_ALL=C on producer AND consumer and log rejected raw operands; a guard refusal is an expectation failure, not proven host drift — fix the comparator, don't assume drift.

### Reviewer reuse across lanes with artifact-completion release trigger
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-09T12:25:37Z — "DURABLE S47 REVIEW RELEASE TRIGGER (user ruling 2026-09-09): pN2 remains on its current PP3D safety-review deliverable. When that deliverable is genuinely complete, verified by final artifact/session (not pane idle/settle echo), reuse the same retained pN2 for the ready/stable Selva narrow review."
- Sighting count: 1 cycle (trigger written 12:25Z, released 12:46Z after pane-output + session-jsonl verification)
- Why it matters: scarce reviewers are reused across lanes keyed on the prior deliverable's actual artifact (not pane idle); no new fleet spawned while waiting.

### Mothball handoff + hold-lift resume with fresh parent
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-12T08:52:53Z — "OpenAI hold lifted by user at 2026-09-12; releasing existing retained native row with fresh Astra/xhigh parent; old stops/handoff preserved; no duplicate writer or native reset"
- Sighting count: 1 full cycle (handoff written 09-10T17:13Z "durable path, never worktree-only"; resume 09-12; read handoff SHA first)
- Why it matters: the paused-by-hold pattern works end-to-end — row blocked, worktree INTACT as resume substrate, pane closed, durable handoff doc hash-verified, resume = fresh parent reading the handoff.

### Same-session amend-and-relay instead of re-dispatch (mid-flight user amendments)
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T10:49:34Z — "USER AMENDMENT ACCEPTED IN-PANE (w9Z:p1): current full-MV delivery/QA remains first; owner explicitly ACKed extraction afterward in same row."
- Sighting count: 5+ (loom skill-extraction ack; selva "MID-FLIGHT USER AMENDMENT: stop inherited pass04/full-film preparation churn" @ 09-12T19:44:55Z; playtest "CANON AMENDMENT relayed mid-flight (user ruling via Gru, 2026-09-14 ~20:1xZ; verified queued in minion session): platform canon = PC + mobile + TV/console EQUALLY (not TV-first)")
- Why it matters: amendments land in the existing session with delivery verified (queued-in-steering-buffer counts as delivered-not-lost); zero re-dispatches across the whole window.

### Row re-opening: done→working for a new pass under delegated approval
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-09T20:01:27Z — "GRU DELEGATED APPROVAL 2026-09-09: proposal turn was not full-film completion; restore canonical row to working for NEW charge-look-pass02."
- Sighting count: 2 (selva pass02; loom "done -> dispatched SAME-OWNER AMENDMENT ACCEPTED" @ 09-13T22:26:05Z)
- Why it matters: a finished-turn done classification on a long-lived heist row is provisional — new user/delegated authority reopens the SAME row (never a duplicate), with the spec SHA-bound: "DELEGATED APPROVAL: Gru approved the complete current Selva spec under explicit user delegation; actor=Gru, not fictitious user A/E. SHA256=3a75326b..." @ 11:21:00Z.

### USER LOOK ACTIVE freeze on owning resources
- Evidence: packet-plumber-3d-constellation-view-v2 @ 2026-09-13T17:07:03Z — "USER LOOK ACTIVE 2026-09-13: user wants to see current PP3D visuals now. Do not sweep/close/move the owning worktree, branch, pYQ pane, capture artifacts or any in-flight mechanical-review panes until the user reports look review done."
- Sighting count: 5 events 09-13 (17:07/17:16/17:18/17:20/17:29) + retained previews on l1-spawn (b18/b30/b40)
- Why it matters: user look sessions freeze sweeps/closes/relaunches while mechanical review continues in parallel; mid-look amendments ("default flat in-game composition must fill the playable viewport" @ 17:16:19Z) become NEW candidates under fresh accounting, never mutate the viewed artifact.

### User verdicts captured verbatim from Lavish polls
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-10T08:37:56Z — "USERVERDICT VERIFIED via Lavish Send&End uid3: keep new street layout; refine plant form, leaf finish, lighting."
- Sighting count: 3+ (selva check05 ruling; loom comparison "User favorite=nocturnal-iris; disposition=keep for all six" @ 09-14T00:39:16Z; final "direction A+B Tropical Club Orbit + Prism Ribbons" @ 00:54:27Z)
- Why it matters: poll-result.txt / USER-REVIEW-DISPOSITION.json carry the verbatim verdict + context (comparison baseline named); ended sessions are never reopened — the durable record is the amendment surface.

### Honest completion metrics vs planning estimates
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-13T15:44:35Z — "COMPLETION REPORT 2026-09-13: full-film target55 shots/277.320979s; hard finished-footage metric0/55=0% usable shots and0 admitted deliverable seconds."
- Sighting count: 1 ("The roughly30% figure is explicitly a planning estimate only, not the finished-shot percentage")
- Why it matters: progress reporting uses prepared assets / validated motion / usable shots / rendered seconds — never percentage vibes; a 0% usable-shots row with real intermediate assets is an honest state, not a failure to hide.

## F. Close-out & hygiene

### Preserve-first playable exports; worktree-relative paths die at sweep
- Evidence: packet-plumber-3d-l1-spawn-awareness-37 @ 2026-09-14T17:45:30Z — "PRESERVE-FIRST: user playable b40 + b18/b30 builds (2.0G, self-contained with bundled Godot + PLAY.md) + 56M capture RED-history evidence preserved to /Users/moses/code/_bmad-output/implementation-artifacts/l1-spawn-awareness-37-exports-20260914/ — the worktree-relative playable path in the ACK is DEAD; new canonical playable = <preserve>/PacketPlumber-L1-SpawnAwareness-b40/Start.command"
- Sighting count: 1 (l1-spawn close-out)
- Why it matters: every user-facing receipt after a sweep must re-anchor playable paths to the preserve dir — the pre-sweep ACK path is dead the moment the worktree is removed.

### Link-restoration: sweep raced the re-root, central archives recover untracked-by-design media
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T16:12:02Z — "LINK-RESTORATION (Gru-ordered fix after close-out sweep raced the re-root): worktree sweep deleted untracked media copies (untracked-by-design). Recovered from central preserve archives selva-kinetic-comparison-20260914 + selva-full-mv-iris-20260914: rsync --ignore-existing restored 32 mp4s into main working tree (gitignored, status clean, tracked bytes untouched)."
- Sighting count: 1 (32 mp4s, servers re-rooted to merged serve.py copies, 5 canonical links re-verified 200)
- Why it matters: post-merge end-states that depend on untracked media need the copy-into-main step ORDERED BEFORE the worktree sweep (or a re-root-aware sweep); central archives are the recovery substrate; self-rooting serve.py survives merges.

### youtube-channel drops worktrees (new standing ruling)
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T14:50:11Z — "STANDING RULING (user, 2026-09-14): youtube-channel drops worktrees — future dispatches default to main checkout /Users/moses/code/youtube-channel unless two lanes genuinely collide."
- Sighting count: 1 (recorded in PR #4 open note; PR body from file per backtick-safe doctrine same event)
- Why it matters: repo-specific dispatch default changed — future youtube-channel minions go to the main checkout, worktrees only on genuine collision; worth canonizing next to the RT-main-checkout rules.

### pr column now self-set by minions at in-review (guard healthy)
- Evidence: packet-plumber-3d-l1-spawn-awareness-37 @ 2026-09-13T23:00:04Z — "pr: https://github.com/solarity-services/Packet-Plumber-3D/pull/42" (also pp3d-playtest-fixes-1 "pr: https://github.com/solarity-services/Packet-Plumber-3D/pull/45" @ 09-15T00:39:20Z; loom "pr: https://github.com/mssoka/youtube-channel/pull/4" @ 09-14T14:50:11Z)
- Sighting count: 3/3 self-set this window (loom's landed done→in-review post-completion at user-request PR creation — delivery-first, PR-later is a valid local-lane shape)
- Why it matters: the historical NULL-pr self-report gap did not recur; verify-and-set can relax only if the trend holds — the delayed-flavor (pr set after done) still needs the done→in-review transition to arm the watcher.

### Same-status notes instead of same-status sets
- Evidence: youtube-channel-selva-mlx-ai-production @ 2026-09-13T16:34:06Z — "Ledger remains BLOCKED; no same-status set used because it would drop the note."
- Sighting count: 1 explicit (pattern used throughout)
- Why it matters: confirms the known `ledger set` refusal behavior is now deliberately worked around via notes — documentation value only.

### Shell-expansion artifacts in relays ($0 → /bin/bash) corrected via file-safe resend
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-09T14:33:16Z — "RELAY CORRECTION 2026-09-09: substantive check02 relay resent to Gru from file-safe payload; accounting explicitly recorded as paid=0 (prior relay text had shell-expanded paid/bin/bash display artifact only, no ledger or production-state change)."
- Sighting count: 1 event pair (corrupted "paid/bin/bash" visible @ 14:32:35Z + correction + ACCOUNTING NORMALIZATION @ 14:33:44Z)
- Why it matters: third sighting of the $-expansion class on a new surface (native accounting fields); single-quote/file-safe payloads remain the fix, and corrupted amounts get an argv-safe literal correction note preserving history.

### Premature RUNNING claims corrected from source logs
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T09:59:37Z — "CORRECTION to immediately prior roundtrip status: native VSE edit was created, but pack-edit background UI normalization failed before launching the90-frame worker (inactive SpaceView3D lacks view_type after area switch). Previous shell continued to relay despite Python assertion; no worker had actually started."
- Sighting count: 1 (two corrections 09:59:37Z/09:59:43Z, then VERIFIED RESUME @ 10:00:16Z with terminal.json evidence)
- Why it matters: a shell continuing past a Python assertion produces false RUNNING relays — claim worker starts only from durable terminal/START receipts, and correct the record within minutes.

### Durable receipts supersede stale session claims after recovery
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-13T09:41:55Z — "IMPORTANT durable evidence supersedes stale prelaunch note:23 actually launched08:50:10Z, completed exit0 with31/31 actual fit GREEN, exact49083/49084 reaped08:51:31Z."
- Sighting count: 1 (post-wedge-recovery reconciliation)
- Why it matters: after kill+relaunch, reconcile from on-disk receipts (REPORT.md/RECONCILIATION.json), not the dead session's last words — prevents replaying completed work.

## G. Backlog & user-ruling intake

### Backlog-only intake with explicit fences (issues #34-#44)
- Evidence: packet-plumber-3d-pp3d-playtest-fixes-1 @ 2026-09-14T20:07:57Z — "BACKLOG INTAKE (user-filed future work, Gru relay 2026-09-14): PP3D #43 NOC dashboard (parked design consult) + PP3D #44 bespoke PP building asset family. FENCES: backlog-only — no dispatch, no fold into the active lane, no resume of other stops, no per-issue acknowledgement; nothing moves without a dispatch."
- Sighting count: 2 windows (constellation row records #34-#41 across 8 quiet events 09-12; playtest row #43+#44)
- Why it matters: intake ≠ work — GitHub issues recorded quietly on active rows with fences; the constellation events also show quiet amendment intake (#40 typography scope widened, still backlog-only).

### Standing rulings recorded verbatim with durable memory paths
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-10T00:56:42Z — "USER STANDING BLENDER RULING 2026-09-10, verbatim: \"go ahead, blender is for you to use. no permission needed. to access blender. I'll rather get notified when i need to review an output please\"."
- Sighting count: 3 standing rulings this window (Blender access; PP3D/Selva concurrency "PP3D user play and authorized Selva queue may run concurrently; supersedes the play-done dependency" @ 09:06:16Z 09-10; youtube-channel drops worktrees)
- Why it matters: each got a durable memory/briefing file + verbatim quote in the ledger — the concurrency reversal shows the earlier play-done hold (08:47:16Z) being superseded in place, not argued with.

## H. MLX/Wan lane (single-window lessons)

### Storage gates measured exactly before transfer; scoped cleanup by user ruling
- Evidence: youtube-channel-selva-mlx-ai-production @ 2026-09-13T16:41:09Z — "WAN STORAGE GATE RED: exact unquantized BF16 MLX I2V-A14B route needs 69,046,724,728 bytes (64.305GiB) with 0 reusable bytes; only 21,157,580,800 bytes remain above the 32GiB reserve, a 47,889,143,928-byte (44.600GiB) deficit."
- Sighting count: 1 gate cycle (RED → user ruling "scoped LTX removal and exact Wan2.2 I2V-A14B acquisition are authorized" @ 16:47:34Z → "Cleanup reclaimed 171,940,831,232 bytes; current free ~211.833GiB; capacity gate PASS" @ 16:58:39Z)
- Why it matters: big-model intake gets an exact-bytes gate BEFORE any transfer, and deletions of prior runtimes are user-ruled + provenance-preserving, never minion initiative.

### Arbitrary ETA kills vs healthy long renders (Wan pilot)
- Evidence: youtube-channel-selva-mlx-ai-production @ 2026-09-13T19:20:52Z — "healthy renders may wait beyond the old internal 8h/ETA cutoff. Same owner must audit/remove arbitrary healthy-render kills from wrapper/subprocess watchdogs while retaining genuine memory/disk/32GiB/failure/user-stop safeguards, then finish bounded diagnosis + one new-marker five-second clip."
- Sighting count: 1 (pilot killed at "first step 1737.93s; tqdm ETA 18:49:39 remaining" @ 19:04:05Z; SIGTERM classified "ordinary owner recovery after measured throughput projection, not PP3D cleanup, engine crash, or an eight-hour human wall")
- Why it matters: watchdog ETA projections must not kill healthy local-ML renders — separate throughput-projection stops (report + ruling) from hard failure/user-stop safeguards.

### HUMAN-STOP park with model_availability=REMOVED
- Evidence: youtube-channel-selva-mlx-ai-production @ 2026-09-13T19:43:06Z — "HUMAN-STOP 2026-09-13: Selva video/local-AI parked by verified user instruction; owner retired, workers quiescent, model_availability=REMOVED; not provider/capacity failure; no generation/diagnostic/retry/resume."
- Sighting count: 1 ("Wan weights removed under verified delete authority"; recoverable handoff preserved; deferred=cancelled:user)
- Why it matters: user parks record WHAT was removed (69GB weights) and what's recoverable — reacquisition is not automatic on resume; distinct from provider holds because the model itself is gone.

## I. Blender craft (loom/full-MV lane)

### sRGB vs BT709 transfer-tag trap in native VSE exports
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T10:17:14Z — "native writer wrongly tags sRGB asBT709. Native Rec1886 output-transform trial02 is mathematically valid under common-view normalization yet visibly lifts browser shadows (~14.5/255 difference), so not adopting that look."
- Sighting count: 1 (resolved via "Corrected sRGB signalling changes exactly2 generated-file metadata bytes, no payload/file-length change" @ 10:28:33Z — in-process avcC/colr transfer 1→13 patch)
- Why it matters: Blender 5.2 VSE H264 writes wrong transfer tags; the sanctioned fix is metadata-only in-process correction with constant-length assertion + browser-verified MAD, NOT a re-grade or Rec1886 switch — reusable for any native MV export.

### Uncached MP3 start-read defect (~23ms skip)
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T10:52:30Z — "full-file QA found real uncached MP3 start-read defect (~1105 samples / ~23ms); all 8320 picture phases passed."
- Sighting count: 1 (fix: "Native Sound.use_memory_cache=True fixes sample 0 in cached 0–3s tests at 0/1/2s with correlations >.9999")
- Why it matters: first-frame audio alignment in native VSE needs Sound.use_memory_cache=True; caught only by full-file PCM correlation QA, not by spot checks.

### Comparison-gallery playability is a first-class user-facing defect
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-13T23:29:35Z — "COMPARISON USER LOOK FEEDBACK: full poll-result.txt consumed from kinetic-comparison-v01/gallery; user verbatim: this doesnt look complete. i cant play anything. Comparison gallery playback is a real usability defect; fix in place in the existing owner/session, inspect actual media paths/player wiring and verify playable A/B media before next user look."
- Sighting count: 1 (CORS catalog-fetch defect; "versioned local classic script" fix; verified embedded A/B playback before next poll)
- Why it matters: deliverable galleries must be PLAY-verified (embedded playback, swap, scrub) before a user look — a broken player wastes a verdict round and reads as unfinished work.

### Skill extraction from a successful lane → central preserve → stable install
- Evidence: youtube-channel-selva-electric-loom @ 2026-09-14T13:45:51Z — "FULL MUSIC-VIDEO SKILL INSTALLED: inspected central HANDOFF and discovery conventions; no existing blender-music-video collision. Byte-copied verified 28-file/1,862,481-byte package to real stable directory /Users/moses/code/.agents/skills/blender-music-video"
- Sighting count: 1 full flow (extract staged in worktree skills/ → 33 generic CLI events + negative tests → HANDOFF.json → Silas byte-verified install + alias + discovery-validated with 0 diagnostics)
- Why it matters: the reusable-skill pipeline (owner stages/tests → central preserve → Silas installs with collision check + discovery proof) is the template for harvesting skills from production lanes — no root pull, no worktree symlink.

## J. Misc single sightings

### User-facing delivery via QuickTime open with receipt (no watch claim)
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-08T18:08:42Z — "USER-FACING DELIVERY: exact verified WIP MP4 opened with macOS QuickTime Player at 2026-09-08T18:08:23Z; open exit=0, QuickTime process observed PID9433, no claim user watched."
- Sighting count: 1 (player-open-receipt.json with SHA)
- Why it matters: delivery ≠ verdict — the receipt proves the open, explicitly not the watching; the verdict lands later as a separate user-look event.

### Research-lane no-PR completion with dual-pane delivery proof
- Evidence: youtube-channel-thumbnail-ctr-research-20260914 @ 2026-09-14T12:19:19Z — "Read-only research complete ... OS notification shown:true. BOTH w85:p2 and w85:p1 delivery verified via exact tagged message plus Working state; proof .../delivery.json."
- Sighting count: 1 (10-min headless research job, clean self-notify + dual relay + pane closed)
- Why it matters: the no-PR completion contract (notification shown:true + verified relays + delivery proof file) executed perfectly — the checklist-gate hardening is holding.

### Dirty-scene preservation phases (43 orphans, save-copy, viewport-abort)
- Evidence: youtube-channel-selva-electrica-assets-rigs @ 2026-09-08T13:16:36Z — "PHASE 1 VERIFIED / PHASE 2 STILL UNAUTHORIZED: receipt.json SHA256 9f1f5286...; artifact SHA256 7a981889...; 43/43 explicit IDs captured (42 MESH + 1 ARMATURE), artifact 3,532,115 bytes; gpu_used=false;"
- Sighting count: 1 saga (unknown dirty frame129 → preserve-then-restore two-phase user ruling → SOLID-viewport pre-abort @ 13:22:36Z → verified restore @ 13:28:30Z → "DIRTY-STATE SAGA CLOSED")
- Why it matters: unknown-provenance dirty state gets preserve-first (including zero-user datablocks a save-copy omits) before any restore; GPU-preview risk aborts loads (viewport MATERIAL→SOLID needs explicit mechanics release) — the shared-Blender forensics doctrine in its fullest exercise.
