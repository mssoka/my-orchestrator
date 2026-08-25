# Dream report — 2026-08-19

Material: 13 shards, 6 journal entries (gru ×3, silas ×3), 41 ledger jobs (334 events), since 2026-08-17T17:47:09Z.

Store copies edited (diff-ready): `store/AGENTS.md` (13 hunks, all additive), `store/minion-field-notes.md` (4 hunks, all additive). Live files untouched.

## Proposals

### P1 — Reasoning-tier chain: v4-pro BANNED; k3 → glm-5.3 → HOLD
- Target: store/AGENTS.md (Provider incidents) · Class: auto
- Change: appended the 08-19-morning supersede — v4-pro banned from reasoning (cost); chain k3 → glm-5.3 → HOLD (park, no reasoning dispatches while both down; mid-work rounds park until a probe-flip; never a v4-pro continue). Retires the 08-12/08-16/08-17/08-18 fallback chains. Folds in the user-ruled both-down HOLD regime: merges held too, fallback-model verdicts informational-only (5.11 r4 precedent).
- Evidence: gru-journal 08-19 "v4-pro BANNED from reasoning tier (cost). Chain: k3 -> glm-5.3 -> HOLD"; ledger righttenantry-demo-mode 08-19 03:27Z + dream-2026-08-19 row note; playbook already carries it (7e889ec).
- Reasoning: the AGENTS.md supersede chain ended at 08-16 and still named v4-pro as sanctioned fallback/recovery — stale doctrine on the most load-bearing policy.

### P2 — NEW incident class: deepseek 402 Insufficient Balance (account wall)
- Target: store/AGENTS.md (Provider incidents) · Class: auto
- Change: appended — 402 ≠ 403/429 (billing, not quota/rate; a user top-up fixes it, waiting does not); it killed the always-live ops spare midday 08-19; user flipped all ops to glm-5.3 (af06ff3), reverted to flash same evening (b2f51d9; in-flight panes stay on their launched model). Recovery per pane: `/model <ops fallback>` + continue, once.
- Evidence: righttenantry-demo-mode p268 turn 402-errored 08-19 09:26Z; v2-7.3-accessibility-core "model flash->glm-5.3 (402)" 17:17Z; ruling close 16:50Z "ops back to flash (glm interlude retired)".
- Reasoning: the "always-live spare" died — the fleet had no doctrine for the spare failing; now it does.

### P3 — Probe doctrine hardened (×4)
- Target: store/AGENTS.md (Provider incidents) · Class: auto
- Change: appended — probe at EVERY reasoning dispatch (k3 flickered 22:35→01:41→02:41→03:40 one night); a freed rolling window is NOT headroom (glm 03:47Z early-reset re-capped in ~4h under one round's lens load); the cap message's reset time lies (claimed 17:54Z vs actual 12:48Z); a single probe-DOWN row with empty error can be transient — re-probe once before acting.
- Evidence: gru-journal 08-18/19 flicker log; silas-journal 08-18 cap-message discrepancy; silas-journal 08-19 false-DOWN "sanctioned re-probe OK"; demo-mode-perkins-r3 "early-reset window burned by the round's lens load" 08-19 07:55Z.
- Reasoning: four independent probe-trust failures in two days; the P1 quota-probe tooling is only as good as its usage doctrine.

### P4 — 1302 concentration: capped primary → episodic fleet-wide glm bursts
- Target: store/AGENTS.md (Provider incidents) · Class: auto
- Change: appended — with k3 cycle-capped all reasoning rides glm and the account 1302-bursts episodically (17:53Z wave: QoS-r1 + demo-mode-r4 + 7.3-r1 + dream panes); one continue per errored pane, hold NEW glm dispatches until the wave settles, escalate only if continues stop clearing.
- Evidence: silas-journal 08-19 17:53Z wave description + recovery loop.
- Reasoning: extends the 08-14 glm-1302 ceiling lesson with the concentration mechanism — one capped primary changes the burst profile of the survivor.

### P5 — herdr 0.8.0 dispatch-chain rewrite
- Target: store/AGENTS.md (Dispatch & handover) · Class: auto
- Change: appended to the boot-chain gotcha — `herdr wait agent-status --status idle` is GONE ("unknown command: wait"); 0.8.0 form is `herdr agent wait <pane> --until idle --timeout 90000`; it races pi registration (`agent_not_found`) → sleep ~10 BEFORE the wait (post-idle sleep 3 stands); NO PIPES on the wait (`2>&1 | tail -1` masks the failure exit code → the `&&` chain continues into a not-ready pane).
- Evidence: silas-journal 08-19 (pipe-masking quote verbatim; corrected chain "sleep 12 + un-piped agent wait — FULL-CHAIN-OK first try"); dream-2026-08-17 shard ("herdr wait agent-status is GONE"); this dream's own boots hit both failure modes live (`unknown command: wait` on sheep-shards; `agent_not_found` race on sheep-journals).
- Reasoning: every fresh dispatch hits the stale recipe; verified from both the journals and first-hand this session.

### P6 — Pin `--model` at every Perkins round-MAIN launch; defaultProvider is now flash
- Target: store/AGENTS.md (Model dispatch & correction ops) · Class: auto
- Change: appended supersede — defaultProvider is now deepseek/deepseek-v4-flash (the "kimi-coding" line is stale); bare-`pi` round launch ran wire-aesthetics r1 entirely on flash (APPROVED 0B — user SANCTIONED as a one-off, not precedent); pin `--model` on round MAINS too (08-13 lesson covered lens briefings) + verify session modelId after every launch.
- Evidence: silas-journal 08-19 wire-aesthetics r1 account; ledger packet-plumber-wire-aesthetics 08-19 12:47Z "PROVENANCE FIX (user)"; v2-6.2-perkins-r1 09:25Z "round launched bare-pi -> defaultProvider deepseek-v4-flash".
- Reasoning: user ruling on record; closes the last unset-model hole (the round pane itself).

### P7 — Pane valve advisory under full throttle + RT-first business priority
- Target: store/AGENTS.md (Serialize concurrent Perkins BURSTS bullet) · Class: auto
- Change: appended — the ~20-pane valve is advisory ("dont hold... let them all run"; 21 panes flew clean; record pressure as a row note and dispatch); real contention resolves by the 08-19 BUSINESS PRIORITY ruling: RT first over PP; PP belt merge-gated/self-pacing, batch PP merge relays, no urgency framing (playbook 0d70ff5).
- Evidence: ledger packet-plumber-wire-aesthetics 08-19 08:40Z (hold-lift ruling + the overridden 13+8=21 valve note); ledger righttenantry-demo-mode 08-19 01:12Z (RT-first ruling).
- Reasoning: two user rulings on record that qualify the serialize-hold-for-pane-capacity gotcha's default.

### P8 — Audit-intake doctrine: issues-first, fix-now vs batch, scope-guarded
- Target: store/AGENTS.md (Moot-on-merge bullet, FYI-routing area) · Class: auto
- Change: appended — audit findings route to GitHub issues BEFORE any fix dispatch (one fix-now issue + one batch issue: RT #625/#626), fix-now briefing scope-guarded against the batch; M-1 shipped r1 APPROVED + merged #627 same day.
- Evidence: gru-journal 08-18 ("user 'create github issues for them first'"); ledger 08-18 16:29–17:05Z (#627 APPROVED/merged, fold-forward to #626).
- Reasoning: durable intake shape for future audit/heist outputs; one full clean fire cycle on record.

### P9 — herdr 0.8.0: `tab create --cwd` does NOT pin the workspace
- Target: store/AGENTS.md (Extensions, pane-ids bullet) · Class: auto
- Change: appended — r4 tab landed in stray workspace w6H (the 08-18 "lands directly in w1T" observation does not hold on 0.8.0); pass `--workspace` explicitly; 0.8.0 tab-create JSON returns the pane under `root_pane`.
- Evidence: silas-journal 08-19 (demo-mode-r4 tG5 in w6H; 7.3-r1 p299 created directly in w1T with the explicit flag).
- Reasoning: supersedes a stale 08-18 observation with 2 sightings and the fix.

### P10 — Orchestration upgrades: first-fire + production verification
- Target: store/AGENTS.md (Orchestration upgrades section) · Class: auto
- Change: (a) Lens-spawn rooting entry gains the 08-18 first fire (8-pane mis-rooted wave at the root; all closed, relaunch-with-`--cwd` relayed, one idle root pi swept). (b) Trigger graph entry gains the production-verification note: `blocked_by` release fired (5.12 ← 5.11-types), deferred registry auto-surfaced the parked security-audit at the probe-flip (RESUME-TRIGGER row note rode the park), `coordinate_with` exercised in the #67 rebase handshake; ops notes: graph keys via sqlite3 UPDATE post-add; DEFERRED READY SET lines can echo stale.
- Evidence: ledger 5.12 08-18 23:26Z; security-audit 08-18 12:48Z; 5.11-terminal-types-perkins-r1 08-18 06:19Z (user-flagged mis-rooted wave).
- Reasoning: the upgrades are no longer design — recording the clean firings prevents re-litigation and misreads of the new tooling.

### P11 — No-PR completion signal: third gap flavor (`shown:false`)
- Target: store/AGENTS.md (no-PR jobs gotcha) · Class: auto
- Change: appended — `herdr notification show` itself returns `shown:false` when the relay is busy; verify `shown:true`, never assume.
- Evidence: ledger wire-aesthetics 08-19 08:35Z ("Notification relay busy (shown:false) — ledger + watcher caught it").
- Reasoning: third flavor of the notification-gap class (compliance-gap 08-07, sensor-gap 08-15, relay-busy 08-19) — the class now has ≥3 sightings; the verify-the-result rule covers all three.

### P12 — Ledger self-create class still live (round row at `working`, fields empty)
- Target: store/AGENTS.md (Ledger, self-create gotcha) · Class: auto
- Change: appended sighting — v2-6.2-perkins-r1 row self-created at `working` with pane/tab/worktree/model/pr empty (Silas filled post-hoc); verify-and-fill stays the guard.
- Evidence: ledger v2-6.2-advance-trigger-perkins-r1 08-19 09:21–09:25Z.
- Reasoning: recurrence of the 08-14 class; keeps the guard from going stale.

### P13 — Deliverable-relay gap: sighting #3
- Target: store/AGENTS.md (Silas deliverable-relay gotcha) · Class: auto
- Change: appended — v2-6.1 close-out executed but the escalation never reached Gru's input (re-escalated 08:13Z); the relay step is still the failure point.
- Evidence: silas-journal 08-19 (6.1 close-out "never escalated... Re-escalated to Gru 08:13:58Z").
- Reasoning: 3rd sighting of the 08-01 gotcha; keeps the count honest.

### P14 — Perkins round ops: empty-lens standing trigger, push-hold discipline, vision caveat
- Target: store/AGENTS.md (Watchers/sensors/Perkins section, new bullet) · Class: auto
- Change: new bullet — (a) USER RULING: 3-byte-empty acceptance/architecture lenses a THIRD straight generation → sweep + regenerate; g-wave compensation verdicts count as valid (5.11 r3: 7/7 valid on 51/71 findings, no sweep). (b) Minion folds LOCALLY and holds the push until the in-flight verdict posts; the pushed head re-arms as an explicit delta review (5.11 r1-fold 790325a; 7.1 fold d9db462; 5.11 r2 = rebase-delta). (c) Non-k3 round briefings carry the VISION CAVEAT verbatim (mechanical pixel proofs only; aesthetics deferred, never faked — ×6 briefings).
- Evidence: ledger 5.11-terminal-types-perkins-r3 08-18 19:13Z (trigger) + 20:00Z (not triggered, compensation valid); ledger 5.11 08-18 14:56Z + 7.1 20:58Z (push-holds); briefings perkins-*-r1 (7.1, 5.10, 5.11, background-maps, terminal-assets) grep-verified.
- Reasoning: two rulings + one verbatim-recurring briefing discipline, each with ≥2 sightings.

### P15 — Vision doctrine: explicit + local, no silent delegation
- Target: store/AGENTS.md (Extensions section, new bullet) · Class: auto
- Change: new bullet — vision.json's silent lmstudio fallback ran 15+ invisible delegations under a lying log identity (deleted); vision routes explicitly to `lmstudio/qwen3.8-27b-mlx@4bit` via `bin/vision-read` (user test-ruled); pi gates image attachment on declared `input` types — models.json entries need `input: ["text","image"]`.
- Evidence: silas-journal 08-18 (vision.json deletion + audit-log proof + accuracy test); bin/vision-read exists (verified on disk).
- Reasoning: user-driven doctrine with shipped tooling; the silent-fallback failure mode is exactly the class memory exists to prevent.

### P16 — Odin lifetime traps (temp arena / defer scope / literal delete)
- Target: store/docs/minion-field-notes.md (Tooling traps, new bullet) · Class: auto
- Change: new bullet — temp arena frees wholesale (never per-slice delete); `defer` inside an `if` runs at the if-block's end (silent use-after-free that PASSES tests); `delete()` on a string literal aborts (clone first).
- Evidence: packet-plumber-background-maps (08-18), v2-5.12-aggregation-groups (08-19, defer trap + vacuous pass), wire-aesthetics (08-19, literal delete).
- Reasoning: 3 jobs in 2 days hit the same family.

### P17 — Serialized state is a contract surface
- Target: store/docs/minion-field-notes.md (Tooling traps, new bullet) · Class: auto
- Change: new bullet — append catalog entries at the END (array order is T1-visible); load new cross-ref catalogs LAST; log headers carry the RUN-SETUP (start) era or replay validates against the wrong era and latches replay_error.
- Evidence: v2-5.11-terminal-types + v2-6.1-era-definition (2 jobs, 3 facets).
- Reasoning: extends the 08-13 golden-poison canon with the layout/order facets.

### P18 — Changing a default is never one-line
- Target: store/docs/minion-field-notes.md (Tooling traps, new bullet) · Class: auto
- Change: new bullet — a default/catalog change re-times dependent tests (scratch-instrument, print, re-pin — never guess); grep for setups relying on the old default (stale lane-only tests sat green at E7-floor rates).
- Evidence: v2-5.10-narrow-access + v2-qos-default-standard (×2).
- Reasoning: green-but-wrong-premise suites are the expensive kind of green.

### P19 — Rebuild harness/binaries before bless + new mechanical proofs
- Target: store/docs/minion-field-notes.md (rlsw harness bullet, addendum) · Class: auto
- Change: addendum — REBUILD `bin/harness` BEFORE bless and AFTER any rebase (7.1: CI caught the stale bless; 5.11: pre-rebase harness had no map.odin → background-less frames; rebuilt + amended force-with-lease); `cmp -l` every `.log.bin` vs HEAD expecting only version-field bytes (5.10: exactly 8 @ 18..25); `harness fold-check` proves a fold-only shift (qos).
- Evidence: v2-7.1-visual-juice + v2-5.11-terminal-types (stale-build ×2); v2-5.10-narrow-access + v2-qos-default-standard (proofs ×2).
- Reasoning: two independent stale-build bites; the proof tools are the concrete artifacts worth reusing.

### P20 — Vacuous-pin flavors ×3
- Target: store/docs/minion-field-notes.md (08-17 vacuous-assertion bullet, addendum) · Class: auto
- Change: addendum — concentration pins need CREDIT-RICH fixtures (starved gate = vacuous); never hand-append engine-managed states (`Active_Crisis` auto-resolves); window-scoped counts inside the SURGE WINDOW only.
- Evidence: 5.12-aggregation, 6.1-era, 5.11-terminal-types (×3 jobs).
- Reasoning: the vacuity family keeps growing flavors; each flavor named once is a pin saved later.

### P21 — Model attribution: briefing/ledger model lines can be provider-DEAD at dispatch
- Target: store/docs/minion-field-notes.md (bare-label/generalization paragraph, addendum) · Class: auto
- Change: addendum — the briefing's `deepseek/deepseek-v4-flash` line was 402-dead at dispatch (Silas launched glm-5.3 despite the ledger's flash field); check `PI_MODEL` + session jsonl modelId before trusting ANY model attribution.
- Evidence: v2-7.3-accessibility-core shard (08-19); corroborates the standing PI_MODEL gotcha with the 402 flavor.
- Reasoning: extends existing canon with a new dead-line mechanism (balance, not routing).

## Watch items (anecdotes — tracked, not proposed)

- W1 — A mid-flight `/model` on a WORKING pane ENDS the current turn (6.2-perkins-r1 p28Y stranded mid-verification; `continue` revived). Pair every mid-flight switch with a continue. 1 sighting.
- W2 — A quota wall landing mid-session can wedge the turn loop BEHIND a tool error (7.1 08-17: STOP:error on the Blender MCP connect failure; continue + send-keys inert; root cause kimi cycle-403; `/model` + continue revived). When continue is inert, suspect the provider wall and switch first. 1 sighting.
- W3 — Post-lens-wave stall: a round main clean-stops (STOP:stop) after the lens wave with all JSONs on disk but no consolidation/post (terminal-assets r1; idle 4.5h; one continue-nudge recovered). Signature: round main done→idle + lens panes done + no review. 1 sighting.
- W4 — Lens-fleet rotation on a mid-round provider flip: sweep/re-`/model` the capped provider's leftover lens panes (demo-mode r3; glm-labeled survivors confused provenance). 1 sighting.
- W5 — Provider churn can silently degrade lens re-runs to a local 2B non-reasoner (5.11 r1: gemma-4-e2b JSONs had to be re-run on glm-5.3); verdicts must state the real lens model. 1 sighting.
- W6 — Mega-minion handover failure modes (7.1): a quota-403 consumes the handover as an EMPTY assistant turn (pane looks done — check the jsonl for assistant CONTENT, not existence); `pane run "pi --model x"` can type into a nested shell; a pasted image can arrive as bare `[Image-#N]` text. 1 job.
- W7 — Pane reclamation race: external pane closure ate two lens dispatches mid-hunt (security-audit); for small residual scope, finishing in-pane beat a third spawn+reclaim cycle. 1 job.
- W8 — Provider-cap pause protocol: preserve artifacts + write resume-notes BEFORE parking; the resume rode the probe-flip losslessly (security-audit). 1 job.
- W9 — Lavish triage at scale: per-finding native radio forms + one Queue button each + ONE batch question for the Low block — 47 findings triaged in one session (security-audit). 1 job.
- W10 — Structure variants for reversal from the start: legacy-inline branch + variant branch, flags-off path byte-identical and harness-proven (wire-aesthetics; the lavish verdict reversed the re-bless requirement). 1 job.
- W11 — Deterministic render ≠ deterministic encoding: after adding sprites, `git checkout` the unchanged PNGs so regen diffs stay additive (terminal-assets-5.11). 1 job.
- W12 — Odin compile idioms: constant-index needs a local copy ("Cannot index a constant" — CIRCLE16; the claimed PULSE16 prior is NOT independently documented in any shard), unused tuple destructure compiles clean, `#partial switch`, `inc[:]` (wire-aesthetics). 1 documented job.
- W13 — Round-row dedup notes need the FULL sha — a short-sha note let a stale sensor echo re-fire (demo-mode 08-19 07:05Z). 1 sighting.
- W14 — User-driven in-pane model experiments (abort ×2 + `/model qwen3.8-27b`, p281/p296/p268 08-19): classify USER-DRIVEN (note-only, never reverse), flag the context-window ceiling (65k vs >250% ctx), and ASK whether the experiment is still live before any restore. 1 day-cluster.
- W15 — `bin/ledger` has no flag parsing: `ledger add --help` created a phantom job row named `--help` (08-19 08:35Z). See U3.
- W16 — P2c ledger guard vs no-PR jobs: `ledger set <id> in-review` now refuses without "http" in the note or a set `pr` — correct for the NULL-pr class, but it also blocks DREAM rows (no-PR, repo=-): dream-2026-08-19 hit it at badge-out (first dream since the guard shipped 08-18). Resolution this time: explanatory note + notification (shown:true verified) + row left at working for close-out. Suggest exempting `repo=-` rows (folds into U3).
- Anecdotes (from sheep-shards): structurally-impossible golden → unit-pin + disclose in the PR body (6.2); a palette-less view segfaults (7.3); run a brace-depth check after multi-hunk edits (7.3); init/ensure must run BEFORE the early-return guard (6.2). From sheep-journals: a minion canonized its own drift in a code comment that survived to user report (qos-default-standard); quota-probe wrote a bogus `--help` probe row (arg-guard hygiene).

## User-ack items (outside the dream store targets)

- U1 — Dream procedure: tail-read plausibly-BACKFILLED source files. The marker/mtime filter silently drops late-written material (the 08-03-08-07 gru-journal backfill file; the 08-17 dream recovered the 5.2 20h arc only by tail-reading a backfilled journal). Suggest adding to the dream template's Inputs step: "for files dated at/before the marker, tail-read the end rather than skipping." Target: `_template-dream.md` + playbook Dreaming section (playbook edit → user-ack).
- U2 — Playbook consolidation (P3) rides the NEXT dream as planned; the new material it must absorb: the v4-pro-ban chain (already committed 7e889ec), the 402 class + ops flip/revert (af06ff3/b2f51d9), probe hardening, 1302 concentration, valve-advisory + RT-first (0d70ff5). Model-policy + Perkins sections are the stale parts; supersede history → changelog appendix.
- U3 — Tooling suggestions: (a) `bin/ledger` arg-guard — reject job ids starting with `-` in `add` (kills the `--help` phantom-row class); (b) exempt `repo=-` rows from the P2c in-review PR-URL guard (W16 — dreams and other no-PR jobs can never satisfy it); (c) the quota-probe arg-guard noted 08-19.

## Pruned / rejected candidates (with why)

- sheep-shards C4 (golden byte-proof) — mostly DUPLICATE of the 08-13/08-15 golden-discipline canon; only the new mechanical-proof tools survived (folded into P19).
- sheep-shards C1 — merged into P5 (same fix, three sources).
- sheep-ledger C5 — merged into P6 (same ruling).
- sheep-ledger C10 — merged into P1 (the HOLD regime is the chain's terminal state; merges-held + informational-verdict facets folded in).
- sheep-journals C15 — merged into P10(b) (the deferred-registry fire is the production-verification evidence).
- sheep-journals/ledger duplicates (J-C1≈L-C1, J-C2≈L-C2, J-C3≈L-C11, J-C4≈L-C5, J-C6≈L-C8, J-C7≈L-C12, J-C11≈L-C16, J-C13≈L-C3, J-C14≈L-C4) — same incidents from two sources; counted once.
- sheep-journals "Reinforcements" (escalation gap, P7 lens-sweep scoping, empty self-close verdict note, degraded-guard compensation, template model-line rot, full-path provenance) — existing gotchas HELD; only the escalation-gap recurrence earned a sighting tick (P13). NULL-pr self-report gap: ZERO occurrences this window (the P2 ledger guard + briefing line are holding) — healthy, no action.
- W12's PULSE16 prior sighting — not independently documented in any shard; only the wire-aesthetics self-report exists, so the constant-indexing idiom stays a watch item rather than a ×2 pattern.

## Notes

- Model compliance: Bob + all 3 sheep ran `zai-coding-cn/glm-5.3` (full-path label at every launch), per the 08-19 Silas amendment; no v4-pro anywhere.
- Sheep: 3/3 completed clean (shards 13.7KB, journals 20.8KB, ledger 17.3KB), all panes verified working after handover, all closed at badge-out.
- The herdr 0.8.0 wait-rename (P5) was verified FIRST-HAND this session — both failure modes (`unknown command: wait`, `agent_not_found` race) hit the sheep boots.
