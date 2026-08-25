# sheep-shards — candidate patterns (dream-2026-08-21)

Sources: orchestrator-night-watchman(+hardening), packet-plumber ue-bootstrap/ue-slice-1/v2-6.2/v2-6.3, righttenantry demo-polish-2/mobile-form-hunt/mobile-layout-1, wire-aesthetics (tail backfill). All quotes verbatim from those shards.

## Orchestrator / herdr class

S1 — **bmad-build render HALT is an upstream 6.11.0 bug with a sanctioned waiver, not a repo problem.**
- `ambiguous config value implementation_artifacts` (bmm + gds both define it; the fresh skill uses the `{{.implementation_artifacts}}` short-token) halts every bmad-build render; no in-repo fix exists (config.toml installer-managed; overrides still leave 2 matches). The working pattern: self-contained briefing + waiver note in the PR body, avoid bmad-build until upstream fixes the template.
- Evidence: orchestrator-night-watchman + -hardening (2026-08-21): "Waived by Silas ruling — briefings should avoid bmad-build until upstream fixes" / "the briefing's waiver pattern (self-contained briefing + waiver note in PR body) works".
- Why: a minion hitting the halt will burn hours on in-repo fixes that cannot work; the waiver is the sanctioned path.

S2 — **Agent liveness forensics hardened: check PROCESS, not agent+file; never gate chains on `agent wait`.**
- herdr can report `agent_session.value` up to ~1s BEFORE the file exists (the 09:16 false-death race, reproduced) and reports stale idle agents after death (agent clears ~2s late; the session file persists forever). Mid-boot, the only reliable signal is `process-info` argv0 == `pi`. And `herdr agent wait --until idle` times out rc=1 on an up-but-WORKING agent — poll `pane get` agent_status and treat "session exists + busy" as up-with-deferred-handover, not failure.
- Evidence: orchestrator-night-watchman-hardening (2026-08-21): "the pane's foreground `process-info` argv0 == `pi` is the only mid-boot signal — liveness must check process, not just agent+file".
- Why: this refines the 08-19 dispatch-chain doctrine (sleep + wait) — a `wait` rc=1 or a missing-yet session file mid-boot is NOT death; relaunching on it creates phantom panes.

S3 — **After any large write, verify the file contains exactly ONE copy of each function — the write tool ingests drafts.**
- The night-watchman write produced a file with planning text + a duplicated full script mid-file. Post-write hygiene: `grep -c '^main()'` (== 1) and grep for planning-arrow (→) fragments before running the artifact.
- Evidence: orchestrator-night-watchman-hardening (2026-08-21): "The night-watchman write tool ingested DRAFT notes mid-file (planning text + a duplicated full script)".
- Why: a duplicated main/plan fragment in a script that then runs is a silent production hazard, not just noise.

## Verification class

S4 — **Verify screenshots with pixel scans, never a single vision read — the vision model hallucinated a rendered frame.**
- A "mid-traversal" frame the vision model described had ZERO dot pixels; the dot was also genuinely broken. After the fix, pixel-scan (4 positions × 12 frames) + vision agreed. Rule: never re-bless evidence on a vision claim alone.
- Evidence: packet-plumber-ue-slice-1: "the vision model hallucinated it — I trusted a single vision read".
- Why: extends the 08-18 vision doctrine (explicit + local routing) — even a routed vision read is a claim, not evidence; mechanical scans are the ground truth for rendered output.

S5 — **For "why does prod differ" mysteries, grep the DEPLOYED BUNDLE — that is the runtime truth; component parity is blind to stale deploys.**
- The toast mismatch was production staleness (prod 36 commits behind staging, pre-#615 classes in the shipped client.js) — demo/staging/develop all render identically through the shared component, so polish-1's component-level parity checks passed while prod was stale. Matching prod would have regressed the #615 guarantee.
- Evidence: righttenantry-demo-polish-2: "Grep the deployed client.js for the position class — that IS the runtime truth; component-level parity checks (polish-1's) can't see a stale deploy".
- Why: parity-testing the code tree answers the wrong question when the bug lives in the deploy pipeline.

S6 — **When a UI gate never fires, verify the DATA feeding the gate, not the gate's existence.**
- Compare-top-3 hid because demo_store set `score_based_rank` = overall score (86, 78…) instead of competition rank 1..8 — `top_three_ids` needs rank ∈ {1,2,3}, so a correct gate rendered nothing. Same shape for the "shallow" demo PDFs: the typst template already rendered Analyst's Brief etc.; they were absent because pdf_prebake extras lacked the data fields. Port the server's ordering/fields (`score-DESC-NULLS-LAST`, detailed_insight/category_notes/…) into the demo store.
- Evidence: righttenantry-demo-polish-2: "verify the DATA feeding a render gate, not the gate's existence"; "Real demo PDF depth came from data, not the template".
- Why: two independent failures in one job with the same root class — semantic mismatch of gate inputs, invisible to code-presence checks.

S7 — **Briefing premises about current state are claims, not facts: grep the disk; when a premise says "no producer exists", grep BROADER.**
- r1: "vacancy_detail already handles the compare-bar bottom padding" was FALSE — grep showed NEITHER page had it. r2: briefing claimed no real `entity_type=="application"` producer; `ai_notifications.gleam` under `/server/src/ai/` (outside `notification/`) DOES emit one.
- Evidence: righttenantry-mobile-layout-1 (PR #631): "Always grep disk, not the briefing's current-state claim" / "Grep `/server/src/ai/` (not just `notification/`) when the briefing claims 'no real producer'".
- Why: briefings are written from stale context; both slips would have shipped wrong fixes (missing padding; a schema change to dodge a real producer).

S8 — **Bless/golden coverage: `harness save` does NOT cover every verb; wrong-blessed goldens merged silently under billing-blocked CI.**
- `harness input-parity save` is a separate verb from `harness save <demo>` — a catalog_hash fold re-bless that skips it fails gate 10 on "catalog drift". And with GH CI billing-blocked since the 7.3 rounds, v2 merged T2 goldens blessed with the WRONG palette state (remap not applied) + a stale QoS-era parity expectation, never CI-verified; the local container leg (`tools/ci-local.sh`) is the only working CI ground truth.
- Evidence: packet-plumber-v2-6.2-advance-trigger: "a catalog_hash fold re-bless must include it or gate 10 fails" / "The local container leg (`tools/ci-local.sh`) is the only working CI ground truth right now".
- Why: bless verbs and CI legs are each partial — a "green" re-bless or merge can still carry wrong goldens; enumerate the verbs and run the local leg.

S9 — **Temp-allocator lifetime clobbers produce VACUOUS test verdicts — re-log at the site, treat "rejected (OK)" as suspect.**
- A temp-allocated `lpath` held across `replay_hashes`' per-tick `free_all(context.temp_allocator)` read garbage → `accepted=false` → a vacuous "rejected (OK)". Any future flip/divergence class must re-call `log_path(name)` at its site.
- Evidence: packet-plumber-v2-6.2-advance-trigger: "reads garbage → `accepted=false` → a VACUOUS 'rejected (OK)'".
- Why: the test PASSES while testing nothing — the most dangerous class of green; allocator-lifetime discipline (re-log after frees) is the guard.

## UE (engine + tooling) class

S10 — **ue-mcp bridge operational mechanics: pty-only init, stale port.json, kill by pid, keep one old dylib.**
- `ue-mcp init` is pty-only — deploy via the package's `dist/deploy-cli.js` then REBUILD (stale editor shows "Incompatible or missing module"). The bridge port.json goes STALE on editor restarts — rewrite from `Saved/UE_MCP_Bridge/instances/<pid>.json`. pkill misses old editors (kill by pid). Stale `Binaries/Mac/*.dylib` pile up (43) and the editor loads the HIGHEST — a full wipe+relink produces an INCOMPATIBLE stamp; keep at least one old dylib.
- Evidence: packet-plumber-ue-slice-1: "The bridge port.json goes STALE on editor restarts — rewrite it from `Saved/UE_MCP_Bridge/instances/<pid>.json`".
- Why: every one of these presents as "bridge broken / module missing" mystery downtime; the recipe avoids a debugging spiral per editor restart.

S11 — **UE widget lifecycle traps cluster: build in `RebuildWidget()`, widget geometry (not viewport) is layout truth, pre-create pools, explicit ImageSize, controller-constructor input actions.**
- C++-only UUserWidget must build its tree in `RebuildWidget()` (NativeConstruct runs after Slate exists; RootWidget there silently renders nothing). UMG canvas is DPI-SCALED — the widget geometry (1896x1081) is the layout truth, not the game viewport (1280x730). Runtime AddChildToCanvas in NativeTick never paints — pre-create the pool in a layout pass, only reposition in tick; every ClearWorld pairs with a pool rebuild; `FSlateRoundedBoxBrush` ImageSize defaults to ZERO (explicit or invisible). Enhanced Input runtime actions must be created in the CONTROLLER CONSTRUCTOR (SetupInputComponent runs before BeginPlay — else dead mouse). Test-module headers must live in `Public/` with the API macro; qualify `PP::FIntPoint` in engine-side files.
- Evidence: packet-plumber-ue-slice-1: "NativeConstruct runs after the Slate widget exists and setting RootWidget there silently renders nothing" / "the widget geometry (e.g. 1896x1081) is the layout truth, NOT the game viewport".
- Why: each trap fails SILENTLY (nothing renders / dead input), so they cost hours each; this is the pre-flight checklist for any UE UI work.

S12 — **Engine-free verification spine: prove the port byte-exact BEFORE the engine exists; CI gates SKIP-with-reason, never false-green.**
- With no UE installed, UE-header-free headers + standalone `tests/spine_check.cpp` proved the ODN-9/11 port byte-exact against the Odin vectors; engine-gated CI gates skip with a reason. The unverifiable remainder (BuildSettingsVersion, EAutomationTestFlags names, commandlet run-name == class minus U) is flagged in AGENTS.md — re-verify before trusting a green engine build.
- Evidence: packet-plumber-ue-bootstrap (2026-08-20): "engine-gated CI gates SKIP-with-reason, never false-green".
- Why: the pattern generalizes — missing heavyweight dependency ≠ blocked verification; isolate the logic, verify what's verifiable, and name what isn't instead of papering over it.

## Packet-plumber sim class

S13 — **Mirror-fixture rule: a new struct field MUST land in EVERY fixture builder that constructs the struct — a miss silently zeroes behavior.**
- `test_catalog`'s `make_era_row` (determinism_test) built era rows WITHOUT the decay factor → defaults to 0 → `pipe_effective_capacity` silently zeroed EVERY era-1+ pipe's capacity and the whole suite collapsed. Any new Era_Row field must mirror in BOTH the catalog_test fixtures AND determinism_test's make_era_row.
- Evidence: packet-plumber-v2-6.3-upgrade-lifecycle: "Any new Era_Row field MUST mirror in BOTH the catalog_test fixtures AND determinism_test's make_era_row (the load contract's mirror)".
- Why: duplicated fixture builders with defaulted fields fail as silently-wrong data, not errors — grep for every constructor site when adding a field.

S14 — **A global mechanics change (era-3 decay) silently shifts TUNED fixtures into marginal regimes — re-stage on the tier that preserves staging.**
- Crisis/health fixtures were tuned on narrow@10 u/s pre-6.3; decayed narrows (5) + standards (7) pushed them into the marginal regime (attribution chatter — resolve-margin dips cross). Re-stage ENGINE-mechanic tests on the tier that keeps their staging; at era 3 STANDARD is legacy too ("modern" means wide only). Grep `s.era = 3` + standard/narrow draws when touching era-3 scenarios.
- Evidence: packet-plumber-v2-6.3-upgrade-lifecycle: "the crisis/health fixtures were tuned on narrow@10 u/s pre-6.3; decayed narrows (5) + standards (7) push them into the marginal regime".
- Why: post-change test failures that look like bugs are often STAGING drift — retune fixtures before debugging the mechanic.

## Client / async-state class (righttenantry mobile-layout-1 arc)

S15 — **Every response message that fills cached route data must carry the id it was dispatched for + a match-guard — late responses re-fabricate state.**
- A late `ApiReturnedLeaderboard` from the prior vacancy after A→B navigation re-fabricated a wrong vid; the fix mirrored the existing refresh-handler request-id guard (response carries the dispatched id, applies on match). Related: cached `model.leaderboard` survives navigation into most routes (only VacancyDetail/Handoff reset it), so `get_vacancy_id(route)` could fabricate a wrong vid from a stale Success.
- Evidence: righttenantry-mobile-layout-1 r3/r2: "a late `ApiReturnedLeaderboard` from prior vacancy after A→B nav re-fabricates; `LeaderboardResponse` messages needed the vacancy id + guard, mirroring the existing refresh-handler request-id guard".
- Why: reviewers caught this a round AFTER the initial fix — async-response guards are a standing requirement for any cached-route-data store, and stale-cache survival across navigation is the enabling condition.

S16 — **A guard is only as complete as its SET-SITES: every fetch dispatch site (including cold-boot/boot effects) must set the guard tag, and the Error arm needs guarding too.**
- r4's guard dropped the legitimate first response because the cold-boot paths (session-restore + enter_demo, where `modem.init` doesn't dispatch BrowserChangedUrl so handle_browser_change is unreachable) never set the model tag — the UI stranded at NotAsked forever: a live-product regression INTRODUCED by the guard. When a reviewer says "the guard misses the cold-boot paths", enumerate EVERY fetch dispatch site and pair each with its tag; guard Error, not just Ok.
- Evidence: righttenantry-mobile-layout-1 r4: "failing to set that tag in the COLD-BOOT fetch paths … DROPS the legitimate first response and strands the UI at NotAsked forever — a live-product regression introduced by the guard itself".
- Why: guards fix races by creating new ones — the fix's blast radius (all writers of the guarded field, incl. boot paths) must be enumerated, not assumed.

S17 — **Shared helper needed by two arms (real + demo): a circular import is a routing problem, not an excuse — move it to a NEUTRAL module and call it from BOTH arms.**
- The routing helper lived in client (client↔demo_update circular import), so the demo arm re-implemented only the application branch and silently no-oped vacancy-typed clicks. Extract to `helpers/` both import; call from both arms.
- Evidence: righttenantry-mobile-layout-1 r3: "a circular import (client↔demo_update) is not an excuse to leave one arm inline — move the helper to a NEUTRAL `helpers/` module both import, and call it from BOTH arms".
- Why: duplicated partial re-implementations of shared logic diverge silently; the module boundary (not the import graph) decides where shared code lives.

## Env / tooling class

S18 — **Fresh worktrees bootstrap only the root `.env`; per-server env symlinks must be recreated, and `dot_env.load_default()` OVERRIDES process env.**
- Only root `.env` is bootstrapped — a fresh worktree panics "DATABASE_URL not set" until `server/.env` is recreated (rm stale symlink + cp + patch for a local Docker DB); and `load_default()` overrides process env, so env vars alone can't redirect the server.
- Evidence: righttenantry-mobile-form-hunt: "a fresh `server/.env` symlink must be created in new worktrees (only root `.env` is bootstrapped) or the server panics 'DATABASE_URL not set'".
- Why: worktree-create + run produces a misleading panic that looks like a broken server, not a missing env file.

S19 — **agent-browser: `eval` returns array-wrapped DOUBLE-encoded JSON; the default session is shared machine-wide.**
- `eval` returns `["<json-string>"]` — parse with a loop, not a single json.loads. Always `--session <job-id>` (default session is shared machine-wide); `set viewport W H 3` gives DPR3.
- Evidence: righttenantry-mobile-form-hunt: "agent-browser `eval` returns `["<json-string>"]` (array-wrapped double-encoded) — parse with a loop, not a single json.loads".
- Why: cross-job session bleed and double-decode parse failures both present as inexplicable wrong values.

S20 — **Debug flex/CSS geometry by walking the ancestor chain in the DOM, not by reading classes; `shrink-0` is the root-cause fix for rail truncation.**
- The stepper-escape bug needed BOTH `min-w-0` on the rail AND `w-full` on its wrapper — the wrapper is a flex item of a `flex-col items-center` column where align-items:center sizes items by CONTENT, so flex-shrink/min-width never apply. And mid-word truncation in an `overflow-x-auto` rail: `shrink-0` on pills/stops, not `text-overflow: ellipsis` (which permanently clips).
- Evidence: righttenantry-mobile-form-hunt: "verify flex geometry by walking the ancestor chain in the DOM, not by reading classes"; mobile-layout-1: "`shrink-0` on filter pills/stepper stops is the root-cause fix".
- Why: class-reading misses cross-axis sizing rules; two durable CSS recipes that each look like a different bug.

S21 — **Odin gotchas cluster (from wire-aesthetics badge-out, backfill):**
- Multi-return `X, t, ok := f()` with `X` unused compiles clean — don't chase it as an error. Constants (`CIRCLE16`/`PULSE16`) need a LOCAL copy to index at runtime ("Cannot index a constant"). `delete()` on a string LITERAL aborts — clone first. Also: `#partial switch` for unhandled enum cases, `inc[:]` to pass a dynamic as slice, `pc: i32` vs `pc := 4` (int) mismatch.
- Evidence: wire-aesthetics (2026-08-19 badge-out): "Odin multi-return `X, t, ok := seg_cross(...)` with `X` unused compiles clean (tuple destructuring allows unused) — don't chase it as an error".
- Why: each of these presents as a compile/runtime mystery that costs a detour; the cluster is the PP/Odin pre-flight list.

S22 — **A late aesthetic gate verdict (lavish) can REVERSE a just-completed re-bless — structure variants as legacy-inline + path-walk from the start; byte-identical flags-off render is the proof.**
- The wire-aesthetics first pass was a big T2 golden churn; the lavish verdict ("ship pure straight, routing OFF, anchors OFF") turned the re-bless requirement into its opposite — the shipped flags-off render must be BYTE-IDENTICAL to pre-7.5. A shared path-walk that "should be equivalent" drifted 1 pixel in estate_surge — found only because the flags-off harness run must be fully green.
- Evidence: wire-aesthetics (2026-08-19): "the shipped flags-off render must be BYTE-IDENTICAL to pre-7.5, and the harness run on committed goldens is the proof".
- Why: sibling to the 08-07 mid-flight-reversal doctrine — when an aesthetic gate is pending, keep a legacy branch byte-identical so either verdict ships cheap; "should be equivalent" refactors drift.

## No-pattern observations (one-offs worth a watch item)

- **launchd StartInterval self-heal across a merge** (orchestrator-night-watchman): a plist whose ProgramArguments path doesn't exist yet just logs exit-78 per tick and starts succeeding once the merge materializes the file — no re-bootstrap; and the git-overwrite refusal makes copying the script into the live tree a trap.
- **UE editor rewrites `DefaultEngine.ini` on every boot** (AndroidFileServer section) — disabling the plugin is the fix (packet-plumber-ue-slice-1).
- **`npx -y ue-mcp <uproject>` boots engine-free** (27 tools + Epic 5.8 registry snapshot); repo-root `.mcp.json` (stdio) is the pi wiring that works (packet-plumber-ue-bootstrap, 2026-08-20).
- **Gleam/Lustre trivia**: `list.find_map` returns `Result`, not `Option` (hand-roll recursion); gleam_json 3.x `Json` is opaque — `decode.field` chains, and evidence items' `structured` is a BOOL, not a string-dict (righttenantry mobile-layout-1 / demo-polish-2).
- **Reviewers pinged two real blockers on r2** ("verify before trusting the reviewer's 'all green' but they were both genuine here") — reviewer findings on this arc were consistently genuine across r1-r4; supports taking Perkins blockers at face value.
