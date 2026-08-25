# Dream report — 2026-08-21

Material: 9 field-note shards (+1 backfill tail: wire-aesthetics), 6 journal files (gru ×3, silas ×3 — 08-19 files read post-marker only), 44 ledger jobs (294+ events), since 2026-08-19T18:27:41Z. Sheep: shards / journals / ledger (all glm-5.3, provenance verified; 22 + 16 + 12 candidates).

Store copies edited (diff-ready): `store/AGENTS.md` (8 hunks, +126 lines, all additive), `store/minion-field-notes.md` (8 hunks, +117 lines, all additive). Live files untouched. All proposals class **auto** (gotcha appends / shard promotions / facet addenda per the 08-19 dream precedent); no user-ack proposals this pass.

## Proposals (all applied to store copies)

### P1 — Reasoning chain supersede: glm-5.3 = STANDING primary; fickle-k3; probe false-reads both ways
- Target: store/AGENTS.md (Provider incidents) · Class: auto
- Change: appended the 08-19-night ruling (playbook 39c9574 + quota-regime `_policy`, quoted verbatim): glm-first, re-probe k3 only if glm errors, NO proactive k3 flips (the 18:03 reflip re-capped ~1h). Probe-at-dispatch is a dispatch-time gate not a round-long guarantee — fickle-k3 re-capped ~5 min after an OK probe (≥5 sightings) → briefings PRE-AUTHORIZE the mid-round flip (`/model glm-5.3` + one continue, proven ≥5×). Probe false-reads both directions (k3 false-negative; glm false-DOWN on chatty reply vs `^OK$`). 1308 window freed ~11h early — only the probe gates a resume.
- Evidence: quota-regime `_policy` (verified in git 39c9574); 6.2-r2, demo-polish-2-r1/r2, 7.3-r2, mobile-layout-1-r1; silas-journal 08-20 16:13Z false-DOWN.
- Reasoning: the live gotchas' chain ends at "k3 → glm-5.3 → HOLD" (08-19 morning) — two supersede levels stale on the most load-bearing policy; every dispatch reads it.

### P2 — Pin the ENTIRE launch envelope: `--thinking max` + model on every spawn surface; `/model` on a working pane pairs with continue
- Target: store/AGENTS.md (Model dispatch & correction ops) · Class: auto
- Change: appended the 08-20 user ruling (bd2e550): `--thinking max` on EVERY launch (defaultThinkingLevel was UNSET → pi defaults off). Lens fleets launched on capped k3 via bare-pi default while mains rode glm (user-spotted ×2 in one hour; code-review skill lens template now pins model MANDATORY — verify at next wave). Relauncher surfaces inherit all dispatch rules (watchman relaunched Gru on flash pre-hardening). `/model` to a WORKING pane ends the turn cleanly — always pair with continue (6.2-r1 stalled 09:25Z→12:49Z).
- Evidence: playbook bd2e550 (verified in git); 6.2-r3 tHM + demo-polish-2-r3 tHP lens fleets; night-watchman-hardening row; silas-journal 08-19 Lessons arc.
- Reasoning: the provenance ruling covered round-mains and lens briefings; the incident surface is wider (skill templates, revive paths, relaunchers) and the thinking pin was nowhere in the gotchas.

### P3 — Silent pi deaths + census/watchman layer; boot-race liveness traps
- Target: store/AGENTS.md (Pane forensics, new entry) · Class: auto
- Change: appended — pi dies SILENTLY with pane up (6.2 frozen 13.4h + orphan core.bin 99.9%; Gru died ×2 08-21); census sweep is the detection layer; wedged pi (continue/send-keys inert) recovers via kill-pid + FULL handover; crash recovery RE-DELIVERS undelivered escalations. The night-watchman (launchd, 5-min, PRs #6/#7) is the standing out-of-pi liveness layer (kill test PASSED, tab-label resolution, ~3m18s vs the 5h silent night that spawned it). Standing traps: session-file BOOT RACE (absent ≠ dead mid-boot; argv0==pi is the mid-boot signal); `agent wait` rc=1 on an up-but-working agent; keys typed into a booting TUI deliver as stray input ~90 min later; relaunchers never split identity tabs; check the tool's log before blaming the tool (kill suspicion retired by log forensics).
- Evidence: sheep-shards S2; journals J3/J4/J5; ledger L7; hardening PR #7 merged 11:01Z 08-21.
- Reasoning: consolidates the 08-20/21 liveness incident arc (5h silent night → watchman → first-day misfires → hardening) into the forensics doctrine; every element bit within 48h.

### P4 — Perkins close-out drift (badge-out systematically broken) + W3 spawn-turn stall + reboot recovery
- Target: store/AGENTS.md (Watchers/sensors & Perkins rounds, new entry) · Class: auto
- Change: appended — badge-out fails systematically (mains hang post-post ×2/day; self-close-empty recovered-at-close-out ~2/3 of rounds — 5 recovered-verdict events + 2 badge-hangs in the visible stream); expect verdict reconstruction from artifacts (pre-emptive note + durable lens JSONs); Perkins tooling still owes the badge/token-mint fix. W3 stall class, 3 sightings (demo-mode-r5, 7.3-r3, ue-bootstrap-r1): main idle + lenses working → ONE continue-nudge when the wave finishes. Machine-wide reboot ≠ lost work: relaunch SAME row SAME sha, regenerate only missing lenses (5/7 JSONs survived).
- Evidence: ledger events verified firsthand (3 W3 notes; 5 recovered-verdict; 2 badge-hangs); journals J9/J11; ledger L1/L6/L12.
- Reasoning: close-out recovery is now the NORM not the exception (the 08-02/07 self-close gotcha understates it); the W3 stall had no name in the store; the reboot recipe is proven.

### P5 — Ledger row hygiene: wrong-ROW events + model column
- Target: store/AGENTS.md (Ledger) · Class: auto
- Change: appended two new flavors: (a) the r5 round's self-report landed on the r4 ROW (sibling done row flipped; round ids drift by one — read the id back before the set); (b) model column empty while notes say "provenance verified" — fill it at dispatch. Guard extends to verify-and-fill ROW STATE + pr + model.
- Evidence: 7.3-perkins-r4 row 08-19 21:39/23:12Z (restored); form-hunt/bootstrap-r2/slice-1-r2/r3 empty model columns.
- Reasoning: the self-report gap mutates faster than the guard; these two flavors are new since the 08-19 addendum.

### P6 — Trigger graph proven at scale; park rows carry RESUME TRIGGERs; fun-test gate
- Target: store/AGENTS.md (Orchestration upgrades / P2) · Class: auto
- Change: appended — 4/4 held rows released at merge close-outs with fresh heads (the whole PP v2 belt completed through it, zero misfires); parked rows MUST carry the named resume trigger + probe cadence (3/3 resumed clean; the probe never the provider's stated time); NEW milestone type: the fun-test gate (user-held; merge ≠ done).
- Evidence: ledger L3/L10; 6.1→6.2→6.3→ue-architecture-slice-map releases; PP belt complete 08-20 17:42Z.
- Reasoning: the P2 upgrade note said "verified in production 08-18/19" for 2 mechanisms — the window proved the rest at scale plus the new gate type.

### P7 — The HEALTHY reversal form: user-played pixel-first bake-off gates; byte-identical legacy path
- Target: store/AGENTS.md (Dispatch & handover / reversals) · Class: auto
- Change: appended — the LOOKS-primary ruling (side-by-side vs the actual reference, ref frame local-IP, MCP proof doubles as delivery vehicle); one slice bought the engine verdict ("just focus on odin for now" → UE slice-2 parked, Odin look-polish dispatched). Sibling (wire-aesthetics): pending aesthetic verdict → keep the legacy path BYTE-IDENTICAL (legacy-inline + path-walk; flags-off render byte-identical is the proof either verdict ships cheap).
- Evidence: ledger 08-20 23:38/23:39Z rulings + slice-map folds; wire-aesthetics shard (backfill tail); journals J14.
- Reasoning: reframes the reversals gotcha from "reversals kill work" to "design the gate so the reversal is cheap" — two independent jobs converged on it.

### P8 — Billing-block echo: highest-volume noise + minions still propose reruns
- Target: store/AGENTS.md (Provider incidents / billing) · Class: auto
- Change: appended — ~15 note-only echo events/48h; demo-polish-1 proposed a useless rerun; carry the signature (5s run / zero logs / "payments failed") in briefings; sensor auto-mute is a Silas config task.
- Evidence: ledger L8; mobile-layout-1 08-19 23:56Z; demo-polish-1 21:43Z.
- Reasoning: the standing ruling covers ops; the gap is minion-side (briefings) — one signature line stops the useless-rerun proposals.

### P9 — bmad-build 6.11.0 broken on this install: sanctioned waiver path
- Target: store/minion-field-notes.md (Tooling traps) · Class: auto
- Change: new entry — `ambiguous config token implementation_artifacts` (bmm + gds both define it; step files consume the short token — verified in the skill files); no in-repo fix; Silas WAIVED the skill (self-contained briefing + canon note in PR body); avoid naming bmad-build in briefings until upstream dedupes.
- Evidence: night-watchman + -hardening (2 jobs); skill files verified firsthand.
- Reasoning: every bmad-build-named briefing halts at step-01 with a trap that looks like a repo problem; the waiver is the sanctioned route.

### P10 — UE cluster: bridge ops, widget lifecycle, engine-free spine
- Target: store/minion-field-notes.md (Tooling traps, 3 new entries) · Class: auto
- Change: (a) ue-mcp bridge ops (pty-only init, stale port.json recipe, kill-by-pid, dylib pile/keep-one-old, DefaultEngine.ini rewrites, engine-free npx boot, repo-root .mcp.json wiring); (b) UE widget lifecycle traps (RebuildWidget not NativeConstruct; DPI-scaled widget geometry = layout truth; pre-created pools; ImageSize zero default; controller-constructor input actions = the r1 dead-mouse blocker); (c) engine-free verification spine (byte-exact port proof before the engine exists; SKIP-with-reason gates with a NAMED LIFT-CONDITION — lifted when UE 5.8.1 turned out installed).
- Evidence: packet-plumber-ue-bootstrap + -slice-1 (2 jobs); sheep-shards S10/S11/S12.
- Reasoning: a new engine domain bootstrapped this window; each trap fails silently and cost hours — this is the UE pre-flight list (the Godot/Odin cluster pattern, third installment).

### P11 — Vision reads are claims: evidence-grade screenshots need pixel gates + negative controls
- Target: store/minion-field-notes.md (facet addendum to the 08-15 pixel-scan entry) · Class: auto
- Change: appended — a vision read described a frame with ZERO dot pixels (the r1 "fabricated evidence" blocker, owned by the minion); rule: pixel-scan rendered evidence + a COMMITTED geometry gate with a NEGATIVE CONTROL (the old frame fails by 37px, new pass). Never re-bless evidence on a vision claim alone.
- Evidence: packet-plumber-ue-slice-1 Perkins r1/r2; ledger slice-1 events 09:18Z/11:46Z.
- Reasoning: extends the 08-18 explicit-local vision doctrine — routing fixed WHO reads the image, not WHETHER to trust it; mechanical gates are the truth layer for rendered evidence.

### P12 — Name the SURFACE: deployed bundle = runtime truth; grep BROADER on "no producer" claims
- Target: store/minion-field-notes.md (facet addendum to ground-truth-first) · Class: auto
- Change: appended — production 36 commits stale made two successive parity verdicts wrong (component parity blind to stale deploys; matching stale prod would have regressed #615); grep the deployed bundle. And when a premise claims "no producer exists", grep broader paths (`ai_notifications.gleam` lived outside the named module).
- Evidence: demo-polish-1/-2 (wrong ×2, diagnosed on the 3rd); mobile-layout-1 r1/r2.
- Reasoning: the ground-truth convention covered disk-vs-briefing; this adds the deploy-pipeline dimension and the negative-existence claim type.

### P13 — Vacuous-pin genus consolidated: wiring-level bites, asserting collects, kill-the-dependency races
- Target: store/minion-field-notes.md (facet addendum to the negative-control convention) · Class: auto
- Change: appended the consolidation — pins bite at the WIRING level not the helper level (7.3-r5 deleted-flip passed 16/16); every fix ships a revert-failing pin (briefings carry the bar verbatim); collects-that-never-assert are vacuous; shared-path races close by KILLING the dependency (macOS identical nanoseconds; 7.3's race survived r3→r6); fix-chains migrate surfaces (grep ALL surfaces).
- Evidence: ≥7 sightings — 7.3 r2→r7, 6.2-r2, demo-polish-2-r2, mobile-layout-1; journals J6; ledger L4.
- Reasoning: the #1 Perkins blocker genus across ALL repos this window; the store had the pieces scattered — the consolidated form is what briefings quote.

### P14 — PP fixture traps: mirror-fixture rule, era-decay staging drift, save-verb enumeration
- Target: store/minion-field-notes.md (new entry) · Class: auto
- Change: (a) a new struct field must land in EVERY fixture builder (make_era_row missed the decay factor → silently zeroed era-1+ capacities, suite collapsed); (b) global mechanics changes shift TUNED fixtures into marginal regimes — re-stage on the tier that preserves staging; (c) `harness input-parity save` is a separate verb — a fold re-bless that skips it fails gate 10.
- Evidence: 6.3-upgrade-lifecycle + 6.2-advance-trigger (2 jobs); sheep-shards S13/S14/S8.
- Reasoning: three silent-data traps in the PP sim test layer; (a) collapsed the whole suite, (c) bites exactly when the golden discipline says re-bless.

### P15 — Odin facets (backfill + temp-alloc vacuity)
- Target: store/minion-field-notes.md (facet addendum to the Odin lifetime entry) · Class: auto
- Change: appended — unused multi-return compiles clean; constants need a local copy to index; `#partial switch`; `inc[:]` slice cast; and a temp-allocated path held across `replay_hashes`'s per-tick `free_all` produced a VACUOUS "rejected (OK)" — re-log at the site; treat "rejected (OK)" as suspect.
- Evidence: wire-aesthetics badge-out (backfill tail — recovered per the U1 caveat); 6.2-advance-trigger; sheep-shards S21/S9.
- Reasoning: the backfill caveat paid for itself again — the wire-aesthetics tail carried undreamed material; the vacuous-rejected is a new green-that-lies flavor.

### P16 — RT front-end/env: ancestor-chain flex debugging, shrink-0, agent-browser eval decoding, server/.env bootstrap
- Target: store/minion-field-notes.md (new entry) · Class: auto
- Change: (a) walk the ANCESTOR chain in the DOM for flex geometry (min-w-0 alone did nothing — the wrapper was content-sized); shrink-0 fixes rail truncation (ellipsis permanently clips); (b) agent-browser eval returns array-wrapped double-encoded JSON — parse in a loop; `set viewport W H 3` = DPR3; (c) fresh RT worktrees bootstrap only the ROOT .env — server/.env must be recreated (DATABASE_URL panic).
- Evidence: mobile-form-hunt + mobile-layout-1 (2 jobs); sheep-shards S20/S19/S18.
- Reasoning: extends the 08-07 agent-browser entry and the worktree-bootstrap entry with the facets that actually bit this window.

## Watch items (anecdotes — tracked, not proposed)

1. **Write-tool draft ingestion** (S3): a large write produced planning text + a duplicated full script mid-file — verify ONE copy of each function after big writes (1 job: night-watchman-hardening).
2. **RT async-state cluster** (S15/S16/S17): response-id match-guards; guard set-sites incl. cold-boot (a guard fix DROPPED the legitimate first response — live-product regression introduced by the guard); shared helpers to a NEUTRAL module. All one job (mobile-layout-1's 4-round arc) — promote on the next sighting.
3. **Gate-data not gate-existence** (S6): UI gates that never fire — verify the DATA feeding the gate (2 sub-cases, 1 job: demo-polish-2).
4. **Wrong-blessed goldens merged under billing-blocked CI** (S8b): v2 T2 goldens blessed with the WRONG palette state + a stale QoS-era expectation, never CI-verified; local container leg is the only ground truth — a latent-artifact risk on PP v2 main worth a sweep job.
5. **Interactive/parked no-PR minions** (J12): completion classified from session tail; shared :4000 dev servers silently swap code under a parked verify minion (port-clobber sibling).
6. **Lavish hunts are user gates** (J13): findings → in-session user approval → fix PR; Perkins opt-in is a separate user decision (form-hunt shape).
7. **Night-shift standing orders** (J16): the Gru-watch jolt template (one /model+continue per failure, no loops) — k3-primary-specific, mostly moot under glm-primary; keep as a template not doctrine.
8. **Sensor signature teaching** (L8b): auto-note/mute the billing echo in nefario-watch — Silas config task (sensor-doctrine-sync grep required).
9. **herdr agents-pane repo label = hosting WORKSPACE root, not pane cwd** (cosmetic; no action mid-round).
10. **Journal timestamp skew**: 08-21 silas headings ~1h skew (IST-labeled-as-Z) — matters in forensics correlation.
11. **Release triggers: read the ledger column, never memory** (1 sighting).
12. **demo-dev-verify local .env → PRODUCTION Supabase** — dev servers with prod credentials; watch class.
13. **Lens waves growing** (14 panes on slice-1-r3, 21/21 lenses) — 1302 exposure grows with wave size.
14. **Degraded-round acceptance**: 4/7-lens rounds delivering valid verdicts (compensation-verdict ruling held).

## Pruned / rejected candidates (with why)

1. **S6 as a proposal** — single job; the observable-effect half is already covered by P13. → watch item.
2. **S15/S16/S17 as proposals** — all three from ONE job (mobile-layout-1); the ≥2-sighting rule bars promotion. → watch item (promotion-ready on first recurrence).
3. **J16 Gru-watch as doctrine** — adversarial challenge: it encodes k3-as-primary context the glm-standing ruling retired; promoting it would bake stale policy. → watch item (template).
4. **"Teach the sensor the billing signature" as a store edit** — not a memory-store change (sensor config); rejected as a proposal, routed as an ops note (watch item 8).
5. **L5 lens-wrong-model as standalone** — root cause already fixed in the code-review skill (model pin mandatory); the residual is one verification line, folded into P2.
6. **J14 and S22 as separate proposals** — same class (cheap-reversal design), 2 jobs combined into P7 to avoid duplicate entries.
7. **S21 standalone Odin entry** — 4 sub-facets, 1 job; folded as a facet addendum (P15) matching the store's facet-addendum precedent.
8. **S2 "never gate chains on agent wait" standalone** — the wait-rc=1 trap is one facet of the liveness cluster; folded into P3.
9. **Playbook status notes** (PP belt complete, dublin-rents blocked, UE debris, stale extension alert text) — status, not lessons; live in the ledger/journals.

## Flag for Silas/Gru — U2/P3 playbook consolidation is NOT carried by this dream's briefing

The AGENTS.md upgrades note records: "Playbook consolidation (P3): rides the NEXT dream (Model policy + Perkins sections rewrite; supersede history → changelog appendix). Recorded scope (user-approved 2026-08-19, U2)". This dream's briefing does not carry that mandate (Bob never touches repos — a playbook rewrite is repo work). **First-hand finding for the U2 task:** the playbook currently SELF-CONTRADICTS — the Model policy block edited by 39c9574 (~line 247, glm-first) vs the older passage at ~lines 285-296 still saying "Perkins rounds MUST pass `pi --model kimi-coding/k3 --thinking max`" and "Gru / Perkins / Bob launches name `kimi-coding/k3` (fallback glm-5.3; HOLD if both down)". Consolidated current state for the rewrite: **reasoning = zai-coding-cn/glm-5.3 standing primary (no proactive k3 flips; k3 only if glm errors); interim fallbacks k3 → HOLD (v4-pro BANNED); ops = deepseek/deepseek-v4-flash; thinking = max everywhere; vision = lmstudio qwen via bin/vision-read.** Recommend dispatching U2 as its own job (or amending a future dream's mandate explicitly).
