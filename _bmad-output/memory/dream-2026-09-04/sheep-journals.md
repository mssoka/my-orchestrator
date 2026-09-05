# sheep-journals

Window 2026-09-02T22:38Z → 2026-09-04T23:58Z. Sources: gru-journal/2026-09-04 (full), silas-journal/2026-09-03 (full), silas-journal/2026-09-02 (post-22:38Z entries), gru-journal/2026-09-01 (backfill check: mtime 2026-09-02T18:36Z UTC, all content pre-marker — clean, nothing undreamed).

## Candidates

### 1. k3 WEEKLY 7-day cap = third kimi cap flavor; "we are out of kimi" regime
- **Evidence**: e1-tiny-planet r2, 09-04 05:0xZ: "r2 attempt 1 died mid-verification on 403 'weekly (7-day) usage limit' — a THIRD kimi cap flavor (not 1302 burst, not 1308 5h wall)". User ruling 09-04 05:1xZ: "NO plan upgrade; k3 out until the 7-day window self-resets (probe decides, never the stated time)." Written durably to `_bmad-output/memory/quota-regime-policy.md`.
- **Why it recurs / rule**: kimi cap flavors keep multiplying (1302 burst / 1308 5h / weekly 7-day). The regime: reasoning rides glm-5.3 probe-gated (HOLD if glm dies too), probe-before-dispatch mandatory on EVERY reasoning dispatch, recovery for a mid-work weekly-cap death = preserve attempt-1 artifacts + sweep + SAME-row retry on glm-5.3 with amended briefing (retry context + vision caveat). Only window reset or plan upgrade heals; continue = waste.

### 2. glm-5.3 proven as a FULL Perkins reasoning fallback (with vision caveat)
- **Evidence**: packet-plumber-3d PR #2, 09-04: "PR #2 APPROVED at R2 ON glm-5.3 (fallback proved: 7/7 lenses regenerated, mutation-proven RED-then-GREEN)". Enforced discipline, e2 r1 09-04 13:2xZ: "the minion's 'visually verified inline' claim explicitly NOT accepted this round".
- **Why it recurs / rule**: with k3 out, every round ran glm-5.3 and closed clean (e1 r2, rta r1, e2 r1-r3, art r1). The standing package: full 7-lens coverage achievable, mutation legs unchanged, BUT aesthetic verdicts are mechanical-only — KYLE/flash = screening layer, the USER-PLAY gate IS the look verdict ("no k3 aesthetic re-check owed for slice 1", user precedent).

### 3. Chatty-OK probe false-DOWN reads still gate dispatches — read CONTENT, not the matcher
- **Evidence**: e2-flow-qos r1 dispatch, 09-04 13:2xZ: "quota-probe returned DOWN x3 on glm-5.3 — but every 'error' was a chatty alive reply ('OK — I'm ready to help...')"; dispatched on re-probe content evidence, false-read documented on the round row. Again 23:5xZ: "glm-5.3 chatty-OK (UP — content-proven)".
- **Why it recurs / rule**: third+ window in a row for this class (08-20, 08-27, now 09-04 ×2, "chatty-OK reads intermittent — matcher flakiness, provider fine"). The strict `^OK$` matcher false-DOWNs on coherent instant replies; a DOWN verdict on a chatty reply = re-probe and read the content before acting, and document the false-read so the record is honest.

### 4. 1302 bursts mid-round are ROUTINE — census first, the wave survives, ONE continue
- **Evidence**: e2 r3, 09-04 15:2xZ: "Census first: all 5 c1 lens panes SURVIVED (only the main's turn died)... then ONE continue -> main resumed working"; art r1, 23:3xZ: "main died post-spawn, all 7 lens panes survived and completed (~8min)".
- **Why it recurs / rule**: two same-day sightings on glm with 6-7 concurrent lens panes (the concentration class). Fixed shape: main dies right after spawning a wave → census the lens panes (they live), wait the wave out in-turn, one continue, zero re-dispatch, zero continue-spam. Empty lens JSON from a burst → the headless one-retry rule (art r1 security.json recovered).

### 5. Same-sha APPROVED stale sensor echoes — note-only, loop terminal on the approve
- **Evidence**: e2-flow-qos, 09-04 15:4xZ: "'dispatch r4' echo = stale... this is the second same-sha stale echo today... the sensor's dedup keeps missing same-sha APPROVED closures when the tick lands in the post-verdict window — the note-only answer is the standing correct response."
- **Why it recurs / rule**: the Perkins sensor's dedup window vs post-verdict ticks is a persistent structural race. Answer every same-sha-after-APPROVED echo with a note; never dispatch rN+1 on an approved sha.

### 6. User pre-verdict merges are routine — moot-on-merge FYI rounds catch live reds; ordered-click recovery
- **Evidence**: rta prod-scale-to-zero, 09-04 12:5x-13:1xZ: "#176 (prod scale-to-zero) user-merged at 11:52Z before r1's verdict (deliberate click; r1 = FYI round per moot-on-merge)... B1 REAL — test_concurrency.py:38 pins min_instances==1, unit suite RED at merged develop (1/2051; CI blind via path filter) — and it's showing RED on promote #177's checks RIGHT NOW... The moot-on-merge FYI doctrine earned its keep." Recovery: fix relayed to the OPEN minion pane → #178 → ordered user clicks (merge #178 FIRST → #177 re-runs green → promote) with #177 merge HELD by Gru until all-green.
- **Why it recurs / rule**: the user merges fast and sometimes deliberately pre-verdict (PR #1 ~5min; #176 pre-verdict). Rounds continue to verdict as FYI; REAL findings become fixes on the open minion with dependent-PR merge holds and explicit click ordering. Post-merge verdicts are the safety net CI path-filters can't provide.

### 7. User-play gates: rows go BLOCKED, gate metric written up-front, gates are re-targetable
- **Evidence**: e1-tiny-planet, 09-04 09:5xZ: "row -> BLOCKED not done: the A6 gate holds (user plays godot --path and rules; done rides the ruling). First fun-test-gate close-out shape executed end-to-end." Deferred gate, 22:0xZ: "The user plays ARPANET L1 (post-pivot) instead of the raw E2 sandbox; the L1 play session doubles as the E2 engine ruling."
- **Why it recurs / rule**: every PP-3d slice now ends in a user-play gate (merge ≠ done). Mechanics of the shape: gate metric on the row at dispatch (09-02 lesson), mechanics-only close-out (worktree/pane swept, row BLOCKED), notification carries the run command, done rides the ruling. A gate can be DEFERRED to a later artifact (L1) without re-dispatch — just re-note the trigger.

### 8. PASSED-WITH-NOTES gate verdicts route to named lanes, not sticky notes
- **Evidence**: E1 gate, gru 09-04: "PASSED-WITH-NOTES (editor view friction, art wants upgrade). Notes routed: editor-preview -> E2 fold; bigger world -> E3 (core first, user's own call); cool routers/houses/DCs/schools/pipes -> asset lane."
- **Why it recurs / rule**: every gate note becomes either a fold into a named upcoming epic or a dispatched lane (asset-scout was born from one). Unrouted gate notes evaporate — routing at verdict time is the standing shape.

### 9. "Deferred" must mean a DISPATCHED row — the art-integration miss
- **Evidence**: gru 09-04 (owned miss): "art integration was deferred as 'next art pass' and never dispatched... Lesson: a folded QoL that ships as a BUTTON needs its click step in the relay, and 'deferred' must mean a DISPATCHED follow-up row, not vibes." Cost: user opened the editor post-#4 and saw placeholder primitives + no world.
- **Why it recurs / rule**: folds and QoL deferrals accumulate silently; the user's next contact surfaces them. Two rules: deferred work gets a ledger row at defer-time, and any fix that manifests as a UI button/action must carry its exact click steps in the relay to the user.

### 10. Direction pivots stay cheap: amend canon + lavish gate + mid-flight relay, zero re-dispatches
- **Evidence**: levels-as-planets pivot, 09-04 21:3xZ: "User-pivot docs amendment (era->levels->planets campaign; L1 = ARPANET 1969 w/ the LO-crash scripted beat...)... lavish gate HALTS for in-page user rulings before the PR." Cables amendment, 10:4xZ: "DROP wifi-router direction entirely... links = CABLES... Noted on row + relayed to p8H (verified in-pane)."
- **Why it recurs / rule**: both same-day user direction changes flowed as amend-and-relay: docs-only canon amendment behind a lavish gate for big pivots (GDD → L1 brief → build sequencing), row-note + verified pane relay for in-flight scope cuts. Scope guarded to the named repo ("3D repo ONLY: don't mess up other projects" — user explicit).

### 11. Dispatch-mechanics hygiene cluster: full-sha verbatim + add-then-update ledger order + row-id pinning
- **Evidence**: e1 r1, 09-04 03:1xZ: "my launch note typo'd the sha token (9fad9320 vs 9fad932b...) — the parent=/sha= dedup keys are only as good as the bytes; copy full shas verbatim, never from memory." rta r1, 12:4xZ: "the sqlite field-fill UPDATE ran before `ledger add` created the row (batching order bug)... when add+update ride one command, add FIRST." Both re-applied correctly later same day ("FULL sha verbatim (r1's note-typo lesson applied)"; "add-then-update order held this time").
- **Why it recurs / rule**: these are one-liner slips that break dedup/sensors; the countermeasures are habit-level (copy shas from command output; add before update; pin row id in handover) and post-verify after every dispatch. The slips recur under batching; the post-verify keeps catching them.

### 12. clear-pane does NOT close the pane — leftover panes accumulate at every close-out
- **Evidence**: 09-03 midday cull: "p6C stress + p6E neweyes (rows done 08-31, panes survived the close-outs — clear-pane doesn't close panes)... LESSON reinforced: clear-pane NULLs the ledger pointer but does NOT close the pane — minion close-outs need the explicit herdr pane close (the 08-28 cull caught 2, today 3 more)."
- **Why it recurs / rule**: structural herdr behavior; every done sweep must enumerate row + worktree + branch + pane with the explicit close, and startup reconciles catch the survivors.

### 13. herdr agent_session pointer goes stale — pane read / newest-mtime session file is ground truth
- **Evidence**: 09-04 00:2xZ: "herdr agent_session pointer for p1 went STALE (08-29 file, mtime unchanged) while the pi was alive... Pane read is the functional probe; never conclude non-delivery from a stale agent_session path." Refined 12:3xZ: "the functional ground truth = the newest-mtime file in the session dir containing the relay text, NOT the registry pointer... grep must disambiguate files, newest-first, and never trust a single-file hit" (own session contains relay texts too).
- **Why it recurs / rule**: the registry pointer rots while panes live long; every delivery verification and liveness check must use pane reads or newest-mtime session-file greps, excluding one's own session.

### 14. NULL-pr self-report gap persists UNDER the ledger guard
- **Evidence**: art-integration, 09-04 23:1xZ: "NULL-pr self-report gap AGAIN (3rd+ sighting) — verify-and-set executed; the guard passed on URL-in-note, so the column gap persists under the guard."
- **Why it recurs / rule**: the in-review guard accepts a URL in the note, so minions who self-report that way still leave the `pr` COLUMN null and the PR watcher stays blind. Silas verify-and-set (`ledger show`, then `ledger pr`) on every in-review transition remains the only reliable guard — do not relax on the guard's existence.

### 15. Chunked mega-diff rounds are standard and pay for themselves via cross-wave corroboration
- **Evidence**: e2-flow-qos r1, 09-04 13:3xZ: "14/14 lens runs across 2 waves, 52/53 confirmed, single blocker (pipe-select grammar zero coverage — flagged by tests lens in BOTH waves = the chunking paying for itself, same finding surfaced from two angles)." Diffs 3636L → 4014L → 4240L all 2-wave chunked with verdict disclosure.
- **Why it recurs / rule**: >3000L → chunk; the two-wave shape gives independent double coverage of shared surface and its disclosure in the verdict is standing. No wave-spawn bash-array regressions this window.

### 16. Perkins counting discipline: phantom checks, vacuous gates, self-catching EXPECTED_CHECKS gates
- **Evidence**: e2 r2, 09-04 15:0xZ: "the new isolation test aborted with 3 PHANTOM checks (23 check() calls vs 20 printed — the counting discipline caught it)" and "the run_tests exit-0 fold is VACUOUS (aborted coroutines still yield ints on 4.7.1, so PASS printed over a crashed test)". e2 r3, 15:1xZ: "the semantic EXPECTED_CHECKS gate (12/12 files pinned, shortfall = 'ran N, expected M' FAIL) caught 4 files its own flag-patch missed pre-push (atomic-edit casualty incl. a half-killed test_world.run_all)".
- **Why it recurs / rule**: vacuous-gate/phantom-coverage hunting is now the dominant blocker class on Godot harness lanes (extends the 08-23 doctrine). The counter-pattern that keeps winning: count printed checks vs check() calls, pin per-file expected counts semantically, and make aborts FAIL the suite. Fix-audit briefings carry mutation legs as standard ("B1 runtime-check not claim; B2 real-path verification").

### 17. Unstable-target hold/release executed textbook — pre-create row, release on settled head with fresh sha
- **Evidence**: e1-tiny-planet r1, 09-04 02:3xZ: "held per the unstable-target doctrine, PRE-CREATED the round row (parent= + sha= in note) to dedup the sensor... Released on the settled head: fresh sha 9fad932" — the minion was mid internal 3-reviewer self-review with fixes imminent.
- **Why it recurs / rule**: minions increasingly run internal review swarms before pushing; sensor fires mid-swarm must be held (head moving), row pre-created for dedup, released at settle on the fresh sha. Also seen: stability gate = minion done + suite green + head settled before rN+1.

### 18. Dream passes COMMIT but never PUSH — push at dream close-out
- **Evidence**: PR #16 close-out repair, 09-02 23:0xZ (post-marker, undreamed until now): "the routine ff-pull ABORTED: root main had diverged — my 4 dream commits... were never pushed... LESSON: dream passes COMMIT but never PUSH — the unpushed-dream-commits pile grew to 4 deep behind a docs PR; dream close-outs should PUSH the doc commit immediately (the pass is already the commit boundary)."
- **Why it recurs / rule**: every dream adds a commit to the orchestrator root; without a push, the next docs-PR merge close-out hits a diverged main and needs stash-rebase-pop. The dream close-out is the natural push boundary. (Repair was clean: 4/4 replayed — canon files were edited in disjoint regions.)

### 19. Briefing model lines keep going stale — verify at dispatch, every time
- **Evidence**: rt-643 dispatch, 09-03 ~01:15Z: "(brief deepseek line stale again — corrected in relay)". Third known instance of the class (dream-2026-09-02 funfix brief named retired deepseek ops four days after retirement).
- **Why it recurs / rule**: hand-authored and template briefings rot against model-policy supersedes faster than they're rewritten. The dispatch-time correction layer (Silas overrides + notes the correction) is load-bearing; modelId verification in the session jsonl after every launch remains the proof.

### 20. Grep-after-generate on machine-derived briefings
- **Evidence**: art r1, 09-04 23:2xZ: "the briefing-derive pipeline broke this time (sed unterminated pattern produced a 2-line fragment base) — caught by the post-write grep gate (stale-ref count + marker count) and rebuilt python-only; the grep-after-generate habit saved the round from shipping a garbage briefing to the lens wave."
- **Why it recurs / rule**: any sed/templating pipeline can silently emit fragments; generated briefings need a mechanical content gate (marker count + stale-ref count) between generate and dispatch. Rebuild in python when sed fights quoting.

## Watch items

- **Godot .import side-file collisions at ff-pull** (e2 close-out, 09-04 21:4xZ): "ff-pull COLLIDED on untracked Godot side-files (captures/*.png.import + test_gesture.gd.uid — generated locally by the user's play sessions, then tracked by the merge)... the aside-move is the practiced fix (note for the next collision), longer-term maybe .gitignore policy ruling." Residual: 4 tracked .import files sit modified after every user play session — WILL collide again.
- **Remote staging branch had been DELETED** (rta promote, 12:5xZ): "restored at its true last position (b657417 = the #166 merge) so the PR targets a live base" — deleted remote bases surface only at promote time; check base liveness before opening cross-branch PRs.
- **Stray-keystroke / auto-Enter retirement** (10:4xZ + gru evening): Silas' delivery-verify auto-Enter "may have submitted the user's half-typed line ('we don't need a')"; pattern RETIRED — "delivery checks are read-only from now on; a stuck buffer gets an explicit judgment call, not a reflex Enter". Gru doctrine: "fragments = void, wait for full sentences."
- **Trivial-prompt probe ≠ capability verdict** (gru, glm-5.3-flash thinking saga): "one trivial-prompt probe is not a verdict — check long-lived session jsonls before declaring a capability dead." ZAI emits reasoning_content by default; models.json patched `reasoning: true` on glm-5.3-flash. First sighting of the class — watch that the registration flag holds.
- **Godot MCP is user-global** (gru 09-04): "34 tools, connected live (godot_editor-version -> 4.7.1.stable). Every pi pane in any cwd gets it — the implementation belt's editor-driving surface." New standing tooling fact for all PP-3d lanes.
- **New-repo in-repo dispatch pattern** (09-03 23:4xZ): brand-new repo = mkdir + git init -b main + IN-REPO first dispatch (no worktree until a merge exists); `_bmad` symlink carried per the PP gotcha; `gh repo create --private` with fallback flags. Worktrees + sequential creation (index.lock) from lane 2 onward.
- **RT lane standing specifics** (09-03): RT default branch = develop ("the sensor template main-fallback does not apply"), PR `--base develop` pinned, bootstrap = server/.env → ../.env symlink + root .env copied pre-handover.
- **Checklist-gate self-notify trend holding** (09-04 00:2xZ): "pasted shown:true (3/3->4/4 trend)" — but verify-and-fire stays until past PR #16's merge (per 09-02 addendum).
- **No-Perkins judgment call on test-only fix PRs** (13:1xZ): "NO Perkins round on #178 (test-only, executes Perkins' own fix, suite-verified)" — a sanctioned skip shape when the fix IS the reviewer's prescription.
- **CI path-filter blindness on infra repos** (rta 12:4xZ): "deploy-to-prod.yml = push-to-main-only + path-filter EXCLUDES deployment/terraform/**... merge is NOT a prod change; the cut lands only via manual terraform apply" — merge semantics ≠ deploy semantics; Perkins + local suite are the real gate, and unit pins (min_instances==1) can go red invisibly.
- **Shared-Blender guardrails** (10:3xZ): user's video-lane Blender session is LIVE while asset lanes probe it — "read-only unless exporting user picks, zero saves, no open_mainfile".
- **Fast user merges** (PR #1 ~5min after open, "user was watching"; #2 ~5h; #4 ~40min post-approval): assume merges can land any time; keep rows/gates ready before escalation goes out.
- **h3-local-production-queue still holding-by-design** (p69, documented stand-down) and lang-safety tab residue swept 09-03 — long lanes flip idle legitimately; classify against row notes, not alerts.
- **Mid-session model flip flash→k3 on the GDD minion** (09-03 23:5xZ): upgrades mid-docs-pass happen; noted on row, no harm — provenance check stays per-pane at verdict time.
