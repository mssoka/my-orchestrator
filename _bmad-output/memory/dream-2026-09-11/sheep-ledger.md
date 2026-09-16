# sheep-ledger — dream-2026-09-11

Corpus: 572 pre-dumped events since 2026-09-09T01:21:29Z + live `ledger events 200` cross-check (dump ends 2026-09-11T01:28Z; live tail matches — dream row, constellation r5, lighthouse-staging-fix all in flight at dream dispatch). Deep dives done on all top-8 churn rows.

## Candidate patterns (≥2 distinct jobs)

### 1. Bounded-run grants are now a first-class USER-RULED execution contract (entry budgets + stop-conditions + receipts; exhaustion = STOP and report)
The user gated all Godot/native execution behind explicit grants ("run-word"), and minions self-police them hard — entry counts, receipts per entry, stop-on-surprise/stop-on-drift, and stop-and-report at exhaustion. Extensions are never silent: they are new explicit grants with disclosed bounds.
- `packet-plumber-3d-test-parse-hotfix` (09-10): "LANE-1 EXECUTED + STOPPED PER GRANT… FULL-SUITE ENTRY NOT RUN - grant stop-condition (failure stops sequence, reports)."
- `packet-plumber-3d-main-suite-red-fix` (09-10): "All bounded entries consumed (3 focused + 1 full) - STOPPED and reported per grant discipline"; grant extension had an UNEXPECTED outcome (sidecar deletion regressed the suite) → "STOPPED per discipline, no more entries."
- `packet-plumber-3d-l1-intro-flow` (09-11): "Grant entries CONSUMED - stopped per discipline"; 900s window extension "disclosed + applied to this entry per ruling"; capture entry 2 stopped on the ruling's own condition ("if it breaks the beats or blocks boot, stop").
- `packet-plumber-3d-constellation-view` lane-2 (09-11 00:41): "STOPPED-ON-SURPRISE… PROCESS GAP OWNED: my invocation piped 'tail -30' so the log head… is lost; no rerun per stop-on-surprise" — the minion honored the stop even against its own process mistake and requested authorization for one instrumented rerun.
- `packet-plumber-3d-lighthouse-staging-fix` (09-11 01:20, in flight): grant written into the dispatch note itself ("up to 2 boot-probe entries (<=300s) + ONE capture re-attempt (<=900s)… Silas administers").
- Same shape in the 3D lane: Selva check slots 1-6/8 with fresh-census/safe-slot gating per native invocation (`youtube-channel-selva-electrica-assets-rigs`, 09-09/09-10).
Why it matters: a whole execution-permission regime matured this window (3 days, ≥5 jobs). Store-worthy shape: grants carry entry counts + per-entry bounds + receipts + quiescence + named stop conditions; stop-on-surprise outranks completing the checklist; extensions are new disclosed grants, never a quiet fourth entry.

### 2. bmad-build `ambiguous implementation_artifacts` config HALT recurs across jobs and days; job-local qualified-token binding is the emerging sanctioned recovery
The identical launcher exit-1 ("ambiguous config value implementation_artifacts at modules.bmm… and modules.gds…") blocked ≥4 different jobs on 3 days; the skill "explicitly forbids source fallback," so each minion HALTs and waits.
- `packet-plumber-3d-planet-life-router-legibility` (09-07 17:52 first hit; 09-09 09:38 again after resume; 09-09 17:03 renderer "attempted once but failed before launch" — 3 separate halts in one job).
- `orchestrator-gemini-storyboard-skill` (09-10 09:58): "User live-pilot approval is recorded but does not bypass this gate."
- `packet-plumber-3d-main-suite-red-fix` (09-10 19:02): "Canonical bmad-build skill touched-then-restored during qualified-token binding (contained, git-clean)."
- `packet-plumber-3d-test-parse-hotfix` (09-10 16:15): "bmad-build gate passed via job-local qualified-token binding (ambiguous-short-config halt recurred; reversibility proof PASS, canonical untouched)."
Recovery shape (gemini-storyboard internal unblock, 09-10 10:11): ignored job-local bmad-build copy + exact two-token substitution + reverse byte-equality proof + ONE unchanged renderer invocation; canonical/shared config untouched.
Why it matters: a shared-tooling defect kept re-blocking lanes for 3+ days; the workaround is now field-proven on ≥2 jobs (gemini-storyboard, test-parse-hotfix, main-suite-red-fix) but each minion rediscovered it. Either the config gets fixed at the orchestrator root or the qualified-token recovery becomes standing doctrine.

### 3. Godot fresh-worktree environment: `--headless --import` FIRST; untracked `.import` sidecars are LOAD-BEARING; environment-sensitive pins measure the working tree, not the committed tree
- `packet-plumber-3d-main-suite-red-fix` (09-10): entry-1 red = "fresh worktree had NO .godot/ (never imported) so every class_name global failed to parse" (environment, not the diff); entry-2's 47-tally red = "worktree lacked per-asset *.import sidecars (U4-gitignored; fresh worktrees never have them)… ttf/glb need importers… worlds partially built" — minion DECLINED relayed code fixes as "symptom-patching that would manufacture vacuous greens over degraded worlds." The #29 orphan pin then proved unsatisfiable in any used checkout: "present=pin red; absent=ambient red" (sidecar deletion → 10 SCRIPT ERRORs + 49 failures; restore → byte-identical 11 sidecars back to 1-failure baseline).
- `packet-plumber-3d-constellation-view` lane-2 runbook (09-11): "precondition godot --headless --import --path . FIRST (the #28 lesson)" — the lesson was codified into the next lane's runbook same-window.
- `packet-plumber-3d-intro-main-fix` (09-11): verification ran "import precondition (39s, 2490 sidecars)" before the suite; the #29 pin "PASSES on a pristine tree - the defect only bites used checkouts."
- Related descendant: issue #31 (pp_lighthouse.glb references rider-purged texture → boot deadlock), with the lighthouse fix explicitly briefed "DO NOT blanket-delete sidecars (load-bearing finding on record)."
Why it matters: ≥3 jobs hit environment-vs-diff misattribution traps this window; the discipline that emerged (import precondition first; untracked ≠ harmless; pins must scope to the committed tree; don't code-fix environment reds) is exactly store-gotcha material.

### 4. Merged-UNVERIFIED test debt: pre-registered disclosure + post-merge green-confirm is the designed catch (and it fired)
- `packet-plumber-3d-l1-intro-flow` #27 merged 09-10 23:11 with "suite execution was NEVER verified (run-grant lane 3 held) - the merged intro tests now sit on main unexecuted; the post-#28-merge main full-suite green-confirm may trip on them."
- `packet-plumber-3d-main-suite-red-fix` green-confirm (09-10 23:44): "the disclosed risk materialized" — intro-flow test failing on merged main → `packet-plumber-3d-intro-main-fix` dispatched same night, fixed, r1 APPROVED first-round, merged 09-11 00:50.
- `packet-plumber-3d-constellation-view-perkins-r5` (09-11 01:26): after a 00:51 skip-row (disposable delta), pS8's FIRST lane-2 suite run found REAL parse bugs → new substance delta (af329c0..e4480b2 "execution-found parse fixes") correctly re-armed the loop with r5. NOT an echo — new substance.
Why it matters: the "written, not run" debt class (visible since #27) now has a proven full cycle: disclose at merge → named green-confirm trigger → catch → fix round on main → verify. The skip-row→r5 sequence shows execution-found fixes create legitimate new review deltas.

### 5. Push-hold + rebase-delta re-arm under a fast merge belt; expect DOUBLE rebases
- `packet-plumber-3d-constellation-view` (09-10 23:26→23:56): conflict from #27 merge → "prepare rebase locally, HOLD force-push until in-flight r3 posts" → released → 1383dfc went STALE ("#28 merged in between") → final head 1ca7db8 rebased again, both conflicts keep-both.
- `packet-plumber-3d-main-suite-red-fix` (09-10 23:17→23:20): same conflict, same hold, "REBASE PREPARED LOCALLY, PUSH HELD per relay… READY: on r1 verdict, force-push… fresh head = explicit delta round."
Why it matters: confirms existing push-hold/delta doctrine (×2 jobs, same cause) with a new wrinkle — in a belt merging 3 PRs in ~30 min (#26/#27/#28 order user-ruled), a prepared rebase can go stale before the PR recomputes; verify against the live base right before push and budget for two rebases.

### 6. Perkins verdict posting on mssoka/my-orchestrator: fallback-comment is structural (no app installation + own-PR approve block); manual mint retry is proven
- `orchestrator-gemini-storyboard-skill-perkins-r1` (09-10 11:49): "perkins-token has NO installation for owner mssoka… ambient gh auth IS the PR author (GitHub: cannot approve own PR) — formal APPROVE event structurally impossible on this repo until an app installation or non-author credential exists."
- `orchestrator-skill-collision-worktree-fix-perkins-r1` (09-10 12:33): same, "PR-27 precedent — token mint empty, no retries burned."
- On solarity-services (app exists) the mint itself failed once: `packet-plumber-3d-planet-life-router-legibility-perkins-r4` posted as COMMENT fallback, then "FORMAL-POST RETRY SUCCESSFUL (user-ordered): mint SUCCEEDED on manual retry" → formal 5168444639; tooling row `orchestrator-perkins-token-mint-retry-fix` created (14:34).
Why it matters: two distinct failure surfaces (no-installation repo vs mint flake), both now with proven recoveries (fallback-comment carries full verdict; retry-once manual mint). The owed tooling fix has a row.

### 7. OpenAI plan-cap hold — a NEW provider-incident class (window-based, ~a week, user-held)
- 09-10 10:45Z turn death "on plan cap… window ~2026-09-15 per quota memory" (`orchestrator-gemini-storyboard-skill` 11:05): "continue = waste, parked, NO continue sent; alert is a re-detection of the already-recorded cap death."
- User hold froze 3 rows: `packet-plumber-3d-planet-life-router-legibility` ("F01 fix + ALL PP3D model/asset work DEFERRED until user confirms more OpenAI tokens"), `orchestrator-gemini-storyboard-skill`, `youtube-channel-selva-electrica-assets-rigs` (3D lane paused; image-gen exemption did NOT lift it) — all pointing at memory/openai-quota-hold-glm-interim-2026-09-10.md.
- Same hour: user un-paused code-only work on glm-5.3 (11:21 "code-only exemption… NO OpenAI launches"); later user resumed one pane in-pane (11:16 "user authority supersedes the freeze for this pane - Silas observed only").
Why it matters: a window-capped OpenAI quota behaves like the kimi weekly cap (continue = waste, park with named resume trigger) but rides the PRIMARY GPT chain — hold/park/un-pause discipline plus glm interim routing all exercised in one hour. Distinct from transient 1302 bursts.

### 8. Stale blocked rows with long-merged PRs — caught only at a user-ordered census
- `packet-plumber-3d-l1-arpanet`: PR #11 merged 2026-09-05, row sat blocked until 09-10 ("stale blocked row reconciled to done per user census ruling").
- `packet-plumber-3d-e2-flow-qos`: PR #4 merged 2026-09-04 (with r3 APPROVED), row sat blocked until the same 09-10 census.
- `orchestrator-playbook-consolidation`: empty dispatched row from 08-29 closed 09-10 as DUPLICATE of the done u2 row.
Why it matters: 5-6 day staleness on rows whose merges the watchers missed (blocked rows aren't PR-watched). Cheap fix per existing doctrine: at every merge close-out, commit-containment-check sibling blocked rows (`git merge-base --is-ancestor`), not just the owning row.

## Watch items (single-job anecdotes worth tracking)

- **Locale-mismatch process-identity guard false-positive** (`youtube-channel-selva-electrica-assets-rigs`, 09-10): B v02 stopped on `PROTECTED_PROCESS_DRIFT` for PID41430; read-only diagnosis found "locale-only mismatch… Host LANG=en_GB.UTF-8 vs MCP LANG absent; Pair1 Thu10Sep vs ThuSep10" — guard compared locale-formatted `ps` output. Fix: LC_ALL=C producer+consumer + log rejected raw operands. Paneless hardening follow-up routed as issue #2. Generalizes to every identity-comparison guard.
- **Perkins round spec-path ENOENT** (`planet-life-router-legibility-perkins-r1`, 09-10 09:51): headless validation STOP — required spec unreadable at the orchestrator-root path; the valid copy lived in the DETACHED reviewed tree. Recovered same round with corrected path. Round briefings' spec paths must resolve in the round's tree.
- **Log-head loss from `tail` piping** (`constellation-view` lane-2, 09-11): piped `tail -30` discarded the first-error context; the standard recovery ask that emerged = "ONE instrumented rerun… with full log capture (tee to file) - zero code changes, single execution."
- **Capture-window budgeting** (`l1-intro-flow` lane-3, 09-11): boot+world-gen ate a 300s window (exit 124 mid-boot); 900s extension then boot-DEADLOCKED on #31 ("both logs byte-identical (101 lines)"). Window grants need boot-cost calibration; blocked-on-issue state was routed cleanly (issue #31 filed with boot-log receipt).
- **Gemini pilot economics** (`youtube-channel-selva-full-song-storyboard`, 09-10): $5→$10 ceiling with per-batch guard, reserve math, per-image receipts/hashes, single executor, opaque keys; dogfood of PR #27's own package found it "NOT viable at board scale (immutable RESERVE pin + missing live-sample review.json)" → direct-SDK fallback. Dogfood-before-scale worked.
- **3 concurrent glm Perkins rounds = launch-burst concentration tax** (`main-suite-red-fix-perkins-r2`, 09-10 23:25-23:38): burst death + a continue that "landed mid-burst and died (documented class)" → waited 4min, second continue. Under the glm-only regime, ~3 concurrent round mains reliably tax; the 08-16 full-throttle ruling may want a glm-era serialize advisory for ROUND MAINS specifically.
- **Shell `$` expansion corrupts amounts in notes** (×2 rows, 09-10 10:14): "total US$5" became "US//bin/bash" in relayed notes; corrected via "LITERAL NOTE CORRECTION… historical shell-corrupted wording is preserved as history and superseded by this literal record." Same family as the backtick-eating class — single-quote payloads.
- **Lane-scale pause-and-spec close** (`selva-electrica-assets-rigs` + `selva-full-song-storyboard`, 09-10 17:13): durable handoff doc written to `_bmad-output/implementation-artifacts/` ("never worktree-only"), row → blocked = paused-by-hold, worktree INTACT as resume substrate, "resume = fresh glm minion from this handoff." Existing pause-and-spec doctrine applied at whole-lane scale — clean.
- **Self-caught accounting overclaims corrected against immutable receipts** (Selva 09-10 09:44): "My preceding relay incorrectly said within20min. Immutable closeout truthfully records… 0.065973s over the declared new host cap" — the receipt won over the relay. Healthy pattern, worth encouraging.

## Ledger hygiene findings

- **Review-URL anchor loss in self-close/done events, ×2 this window**: constellation r1 done-event carried `…pullrequestreview-` (no id; formal id filled in the 2-min-later close-out note); l1-intro r3 "the done-event URL lost its id from a wrong-review query" → correction note posted. Known class (08-15/09-02) with a new flavor: wrong-review query. Standing rule holds — fetch the review id at close-out, never trust the self-close event's URL.
- **Phantom-working corrected**: gemini-storyboard row stayed `working` while the pane was plan-cap-dead; "status corrected from phantom-working after idle-pane echo" (11:06). The stuck-pane classification step caught it.
- **`pr` column healthy**: every code job self-set `ledger pr` this window (constellation, main-suite, l1-intro, intro-main-fix, test-parse-hotfix, gemini-storyboard, collision-fix, planet-life, silas-luna-xhigh). Zero NULL-pr sightings — the guard is holding.
- **Round-row hygiene**: r5 row created with parent + sha + prior-findings in the note column (sensor dedup shape per the 08-27 pre-add doctrine); constellation r1 HELD row carried pre-rebase sha marked DEAD verbatim ("bf93d110 DEAD (never reference)") — the conflicting/rebasing hold flavor executed as written.
- **No wrong-row events, no phantom duplicate rows, no false claims surviving** — the two overclaim-shaped notes (accounting, timing) were self-corrected with immutable receipts preserved. Cleanest window I've read.

## Notes for Bob

- Most PP3D v2-window activity CONFIRMS existing store gotchas rather than adding new ones: push-hold + rebase-delta (×2), moot-on-merge/disposable-delta sweeps (main-suite r2, constellation skip-row), mega-diff local-canonical substitution (planet-life r1 526MB/7.87M lines 7-chunk 49-pass; collision r1 345k lines → 188-line substance chunk), 1302 burst one-continue discipline (≥6 sightings), watcher pre-classification notes, self-close sweeps with lens-pane enumeration (main-suite r2's 7 burst-era orphan lenses closed at moot sweep).
- The genuinely NEW store candidates: #1 bounded-run grants, #2 bmad-build ambiguous-config halt + qualified-token recovery, #3 load-bearing sidecars/import-precondition/environment-sensitive pins, #4 merged-unverified debt + green-confirm cycle, #6 fallback-comment verdicts + mint retry, #7 OpenAI plan-cap hold, #8 stale blocked rows at census. I'd rank #1, #3, #4 strongest (multi-job, multi-day, user-ruled, reusable).
- The r5-after-skip-row sequence (00:51 skip → 01:26 r5 on execution-found delta) is CORRECT, not a dedup failure — don't let a future audit misread it.
- Selva's 161-event row is one lane's continuous story (moth repair STOP → storyboard timing → full-film passes 01-05 → gemini board expansion); its generalizable exports are the locale-guard watch item and the lane-handoff close shape, not the bulk.
- In flight at dream dispatch: `packet-plumber-3d-lighthouse-staging-fix` (#31 boot deadlock fix), `packet-plumber-3d-constellation-view-perkins-r5` (execution-found parse fixes delta) — both post-marker, both will land in the next dream's window.
