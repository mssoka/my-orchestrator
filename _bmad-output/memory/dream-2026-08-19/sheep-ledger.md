# sheep-ledger — ledger mining, dream-2026-08-19

Window: marker 2026-08-17T17:47:09Z → 2026-08-19T17:57:02Z (334 events, 42 job rows).
Sources: `bin/ledger events 300`, `ledger all`, `ledger show`, read-only sqlite on
`_bmad-output/orchestrator.db`. Carried standing item from dream-2026-08-17 (06:44:45Z):
**P3 playbook consolidation rides THIS dream** (rewrite Model policy + Perkins sections;
supersede history → changelog appendix) — C1/C2/C5 below are the fresh rulings that
section must absorb.

---

### C1 - Reasoning-tier chain churn ended in "v4-pro banned" — supersedes the 08-16 k3-back ruling
/ target: AGENTS.md-gotchas (Provider incidents)
/ class: user-ack
/ evidence: righttenantry-demo-mode 2026-08-19T03:27:49Z — "STANDING CHAIN for r2+ (Gru 03:35Z): probe order k3 -> glm-5.3 (post-06:48Z reset) -> v4-pro LAST RESORT; until the user rules on hold-vs-v4-pro, v4-pro carries MECHANICAL FIX-AUDITS ONLY... never a judgment round as the record." Then dream-2026-08-19 row (17:52Z) — "glm-5.3 (k3 cycle-capped; v4-pro banned per 08-19 ruling)". Chain context: 08-17 20:23Z "reasoning tier = glm-5.3 while kimi quota-down" → 08-18 23:23Z "HOLD LIFTED (user 22:4xZ): kimi k3 back" → 08-19 k3 flicker (01:41 down / 01:42 up / ~02:41 403 / 03:40 up) + cycle-cap 403 again by 17:51Z.
/ why: The model-policy lineage (08-16 k3 → 08-17 glm → 08-18 k3 → 08-19 chain+v4-pro-ban) must be consolidated in one place; k3 flicker is a 4th live sighting of the "kimi back is unreliable" guard, and v4-pro is now banned, not merely last-resort.

### C2 - NEW provider class: deepseek 402 INSUFFICIENT BALANCE (ops tier) + glm interlude retired
/ target: AGENTS.md-gotchas (Provider incidents)
/ class: user-ack
/ evidence: righttenantry-demo-mode 2026-08-19T13:07:14Z — "minion's turn 402-errored (deepseek INSUFFICIENT BALANCE); swept per the 08-19 ops-flip ruling: /model zai-coding-cn/glm-5.3 + continue". packet-plumber-v2-7.3-accessibility-core 17:17:22Z — "model flash->glm-5.3 (402)". Ruling close: 16:50:36Z — "USER RULING 08-19 evening: ops back to flash (glm interlude retired). In-flight glm panes STAY."
/ why: 402 balance is a distinct failure from 403 quota/429 rate (the always-live spare died); recovery was an ops-tier flip to glm-5.3, retired same day when balance returned.

### C3 - NEW user ruling: RT-first business priority for all capacity conflicts
/ target: AGENTS.md-gotchas (serialize-hold / capacity section)
/ class: user-ack
/ evidence: righttenantry-demo-mode 2026-08-19T01:12:33Z — "BUSINESS PRIORITY (user ruling 08-19): RT first over PP — capacity conflicts (pane slots, provider quota, Perkins scheduling, dispatch windows) resolve to RT. PP belt autonomous to the fun-test gate (merge keystrokes only). RT = revenue engine (research verdict)."
/ why: A standing scheduling tiebreaker that outranks Silas' discretionary capacity calls; every hold/release decision now names the winner by business priority.

### C4 - NEW user ruling: pane-valve serialize-hold OVERRIDDEN — "let them all run"
/ target: AGENTS.md-gotchas (serialize-hold / capacity section)
/ class: user-ack
/ evidence: packet-plumber-wire-aesthetics 2026-08-19T08:40:46Z — "USER RULING 08-19 (hold-lift): do NOT serialize-hold r1 behind demo-mode r3 — 'let them all run'; full-throttle 08-16 governs; valve-pressure overridden." (The hold had been written per the old valve: "13 live + 8 = 21 > ~20 valve; RT first per the 08-19 BUSINESS PRIORITY ruling — PP yields", r1 row note.)
/ why: Extends the 08-16 full-throttle ruling past provider quota to the ~20-pane valve; combined with C3, valve pressure alone no longer gates a round — priority (C3) resolves real contention.

### C5 - NEW user ruling (provenance): pin --model at EVERY Perkins launch; flash verdict sanctioned; defaultProvider is now deepseek-flash (stale gotcha line)
/ target: AGENTS.md-gotchas (Model dispatch & correction ops)
/ class: user-ack
/ evidence: packet-plumber-wire-aesthetics 2026-08-19T12:47:52Z — "USER RULING 08-19: the flash-model r1 APPROVED on #70 is SANCTIONED (accepted — verdict stood on in-tree code verification; no k3 re-review needed). PROVENANCE FIX (user): pin --model explicitly at every Perkins round launch going forward (bare pi resolves defaultProvider)." Root incident: packet-plumber-v2-6.2-advance-trigger-perkins-r1 09:25:31Z — "round launched bare-pi -> defaultProvider deepseek-v4-flash; /model kimi-coding/k3 applied mid-flight 09:23Z."
/ why: SUPERSEDES the stale "pi's defaultProvider is now kimi-coding" line (unset now resolves to deepseek flash) and hardens the load-bearing-model-line lesson to round MAINS, not just mega-minion briefings.

### C6 - NEW incident class: provider churn drove a Perkins round to re-run lenses on a local 2B model (not a reviewer)
/ target: AGENTS.md-gotchas (Perkins rounds / model dispatch)
/ class: auto
/ evidence: packet-plumber-v2-5.11-terminal-types-perkins-r1 2026-08-18T13:26:13Z — "round was re-running g5/g6 lenses on lmstudio/gemma-4-e2b (2B local vision model — not a reviewer) after the provider churn; instructed to re-run gemma-produced lens JSONs on zai-coding-cn/glm-5.3 (fallback v4-pro) before consolidation and state the real lens model in the verdict."
/ why: Lens-model provenance can silently degrade to any reachable model during churn; guard = sanctioned-chain-only for lens re-runs + verdicts must state the real lens model.

### C7 - Mis-rooted lens wave (8 panes at the orchestrator root) — promote from upgrades note to full gotcha
/ target: AGENTS.md-gotchas (Perkins rounds)
/ class: auto
/ evidence: packet-plumber-v2-5.11-terminal-types-perkins-r1 2026-08-18T06:19:45Z — "USER-FLAGGED: the round's lens wave was mis-rooted — the lens tab was created WITHOUT --cwd (panes at /Users/moses/code, the orchestrator root; Gru-contamination class, one idle pi at the root). All 8 mis-rooted panes CLOSED; relaunch-with-cwd instruction relayed."
/ why: The 08-18 upgrades section records the fix (skill template pins --cwd forever); the incident itself + recovery recipe (close all, relay relaunch-with-cwd) now has ledger evidence and belongs in the gotchas proper.

### C8 - NEW stall class: post-lens-wave orchestration pause (STOP:stop, no error, continue-nudge recovers)
/ target: AGENTS.md-gotchas (Pane forensics)
/ class: auto
/ evidence: packet-plumber-terminal-assets-5.11-perkins-r1 2026-08-18T04:54:29Z — "the round's turn ended at 00:18Z after the blind lens (STOP:stop) and never resumed — all 7 lens JSONs on disk but no consolidation/posted verdict... Root-cause class: orchestration pause after the lens wave (the wedge-flavored stall; pi alive + idle). RECOVERED via continue-nudge 04:55Z."
/ why: A clean turn-end mid-orchestration is a stall distinct from stopReason:error; the pane-watcher done→idle alert is the only signal — classify by "all lenses done + no consolidation" then nudge once.

### C9 - NEW mechanic: empty-lens THIRD-generation standing trigger; compensation verdicts count as valid
/ target: AGENTS.md-gotchas (Perkins rounds)
/ class: user-ack
/ evidence: packet-plumber-v2-5.11-terminal-types-perkins-r3 2026-08-18T19:13:23Z — "STANDING TRIGGER (user via Gru 19:0xZ): if acceptance/architecture lenses return 3-byte-empty a THIRD straight generation (r1 acceptance mis-rooted; r2+r3 g1 waves both 3-byte) -> INTERVENE per empty-lens doctrine: sweep those lens panes + regenerate." Outcome 20:00:36Z — "User empty-lens trigger: NOT triggered — g-wave compensation delivered a valid 7/7 verdict (51/71 findings); no sweep needed."
/ why: Converts chronic 3-byte empties from per-round annoyance into a counted escalation (3 generations → sweep) and blesses compensation-wave verdicts as satisfying acceptance.

### C10 - NEW regime: user-ruled HOLD (merges + reasoning work) while BOTH reasoning providers are down; fallback verdicts = informational only
/ target: AGENTS.md-gotchas (Provider incidents)
/ class: user-ack
/ evidence: packet-plumber-v2-5.11-terminal-types 2026-08-18T20:34:51Z — "HOLD REGIME: user holds merges + reasoning-tier work until glm-5.3 OR kimi k3 probe-flips back; belt rows stay held; ops/flash-tier continue." Same ts on r4 row — "r4 verdict on v4-pro = informational record ONLY; NO r5 on v4-pro. If r4 needs changes: minion fix rides flash, NEXT round waits for glm/kimi probe-flip. Auto-release per deferred-registry at the flip." Lifted 23:23:04Z (k3 probe OK 22:35:06Z).
/ why: Distinct from the 08-13 Silas-doctrine HOLD: user-issued, covers MERGES too, and degrades any verdict completed on a fallback model during the hold to informational record.

### C11 - NEW nuance: glm 1308 early-reset window gets burned by the round's own lens load
/ target: AGENTS.md-gotchas (Provider incidents)
/ class: auto
/ evidence: righttenantry-demo-mode-perkins-r3 2026-08-19T07:55:04Z — "07:53Z: glm-5.3 1308 cap re-hit mid-verification (early-reset window burned by the round's lens load; reset 15:57:37Z) — recovered /model kimi-coding/k3 + continue."
/ why: A posted reset time is not full capacity — one round's lens wave can consume the early window; plan wave load against the reset, not just the clock.

### C12 - NEW incident class: tool-error mask — MCP connect failure wedges the turn while the real cause is a quota wall; continue alone is INERT
/ target: AGENTS.md-gotchas (Provider incidents)
/ class: auto
/ evidence: packet-plumber-v2-7.1-visual-juice 2026-08-17T18:43:31Z — "turn loop wedged on stopReason:error after the Blender MCP connect failure (continue + send-keys inert) — root cause: kimi cycle quota exhausted (2nd 403 today). Revived via /model deepseek/deepseek-v4-pro + continue."
/ why: A tool failure can end a turn whose recovery path (one continue) then fails because the provider is quota-dead; when continue is inert, suspect the provider wall and switch model FIRST, then continue.

### C13 - NEW failure mode: herdr notification returns shown:false (relay busy) — notification alone is never the completion signal
/ target: AGENTS.md-gotchas (no-PR jobs / completion signals)
/ class: auto
/ evidence: packet-plumber-wire-aesthetics 2026-08-19T08:35:32Z — "Notification relay busy (shown:false) — ledger + watcher caught it (this alert)."
/ why: Second confirmed flavor of the notification gap (08-15 was sensor-side); the settle-note + watcher sweep is the working backup — verify `shown:true`, never assume.

### C14 - Dedup nuance: round-row notes must carry the FULL sha — a short sha let a sensor echo re-fire
/ target: AGENTS.md-gotchas (Ledger / echo classes)
/ class: auto
/ evidence: righttenantry-demo-mode 2026-08-19T07:05:15Z — "Sensor echo 07:05Z: round-3 dispatch alert on 1c2a6a9 = STALE... NO r3 on this sha; r3 fires on the minion's fix push. Dedup key fixed: r2 row note updated to the FULL sha."
/ why: Extends the durable-dedup doctrine from held rows to round rows: the sensor's sha match needs the full hash; short-sha notes are a dedup hole.

### C15 - Push-hold discipline: folds stay LOCAL until the in-flight round's verdict posts; push → fresh sha → next round re-arms as delta review
/ target: AGENTS.md-gotchas (Perkins rounds / review-target stability)
/ class: auto
/ evidence: packet-plumber-v2-5.11-terminal-types 2026-08-18T14:56:28Z — "r1 fold COMPLETE (locally committed 790325a, PUSH HELD per instruction — r2 is mid-review on 11c6cf6)". packet-plumber-v2-7.1-visual-juice 20:58:53Z — "Folded the non-blocking set LOCALLY (d9db462)... HOLDING the push until r3 posts per Silas." Complement: 5.11 12:50:29Z — rebase push mid-round, "r2 mid-review on the pre-rebase head — its verdict lands on the old sha; the fresh sha re-arms" (r2 = rebase-delta review).
/ why: Stabilizes the review target without idling the minion: fold locally, push at verdict-post, and treat the moved head as an explicit delta-review round rather than contamination.

### C16 - NEW incident class: user-driven in-pane model experiments mid-flight (local qwen; aborts) — deliberate, never reverse
/ target: AGENTS.md-gotchas (Pane forensics)
/ class: auto
/ evidence: packet-plumber-v2-7.3-accessibility-core 2026-08-19T16:45:07Z — "USER-DRIVEN — abort x2 + /model lmstudio/qwen3.8-27b at 16:40:56Z (second sighting of the user testing qwen across panes after p281 16:40:25Z; deliberate, not to be reversed)... Pane idle/auto-compacting on qwen (65k window vs 251% ctx)." 6.2 16:42:42Z — "flagged the qwen 65k-window risk to Gru (context 1028%), no reversal (user is in the pane)."
/ why: Watcher alerts from user-touched panes classify as USER-DRIVEN (note-only, no revive/reversal); the standing risk to flag is local-model context ceilings on over-full sessions.

### C17 - NEW incident class (CLI): `ledger add --help` creates a phantom job row — no flag parsing in bin/ledger
/ target: AGENTS.md-gotchas (Ledger)
/ class: auto
/ evidence: job row `--help` added 2026-08-19T08:35:21Z (all fields empty, status dispatched) — `bin/ledger`'s add branch (`elif cmd == "add" and len(args) >= 2: job_id = args[1]`) treats any second token as the id, so `ledger add --help` inserts a job named `--help`. Created seconds before wire-aesthetics-perkins-r1's add (08:35:26Z) — usage-check mid-dispatch.
/ why: Sibling to the 08-14 phantom-row class, new mechanism (CLI misuse, not minion self-create); guard proposal: reject ids starting with `-` (ledger-guard P2 pattern).

### C18 - Orchestration-upgrade features verified in production: blocked_by release, deferred auto-surface, coordinate_with handshake
/ target: docs/minion-field-notes.md
/ class: auto
/ evidence: (a) trigger graph — packet-plumber-v2-5.12-aggregation-groups 2026-08-18T23:26:11Z "RELEASED per trigger-graph (blocked_by 5.11-types done)"; (b) deferred registry — righttenantry-security-audit 12:48:42Z "RESUMED on zai-coding-cn/glm-5.3 (probe-confirmed back at 12:48Z — the deferred:glm tag lifted; row auto-surfaced per Improvement #6)"; (c) soft edge — background-maps ↔ 5.11-terminal-types "coordinate_with ... (T2 re-bless handshake — soft edge, never blocks)" 06:44:58Z, exercised in the #67 rebase (12:50:29Z).
/ why: The 08-18 upgrades are no longer design — each has a clean production firing; field note should record the working patterns (incl. durable RESUME TRIGGER written as a row note at park, 07:39:34Z).

### C19 - RECURRENCE (existing class, no new lesson): Perkins round row self-created at `working` with missing fields
/ target: AGENTS.md-gotchas (Ledger, 08-14 class — append sighting)
/ class: auto
/ evidence: packet-plumber-v2-6.2-advance-trigger-perkins-r1 2026-08-19T09:21:10Z "— -> working added"; 09:25:31Z "Row fields (pane/tab/worktree/model/pr) filled post-self-create."
/ why: Confirms the 08-14 self-create class is still live; Silas verify-and-fill remains the guard.

### C20 - Vision caveat is a standing Perkins briefing line on non-k3 rounds
/ target: docs/minion-field-notes.md
/ class: auto
/ evidence: packet-plumber-v2-7.1-visual-juice-perkins-r1 2026-08-17T19:24:36Z — "MODEL FALLBACK: glm-5.3 (kimi k3 cycle quota exhausted — VISION CAVEAT: pixel verification MECHANICAL only (byte/hash/capture-diff); aesthetic verdicts deferred for the k3 re-check, never faked)." Recurs verbatim in 5.10-r1, terminal-assets-r1, background-maps-r1 briefings ("glm-5.3 + vision caveat").
/ why: Repeatable briefing discipline whenever the reviewer lacks vision: mechanical pixel proofs now, deferred aesthetic re-check named as follow-up.

---

## ANECDOTES (one-offs, not promoted)

- Duplicate Perkins review posted, deletion attempt 422, harmless — righttenantry-demo-mode-perkins-r1 2026-08-19T03:25:18Z.
- Direct user question landed in a minion pane ("what's the link to lavish?"); watcher classified transient, assist relayed — packet-plumber-v2-5.10-narrow-access 2026-08-17T18:31:54Z.
- glm-labeled lens survivor /model'd to the round's current provider so a re-wave can't catch a capped-provider pane — righttenantry-demo-mode-perkins-r3 2026-08-19T07:59:09Z.
- 7.3-perkins-r1 row note "corrected launch chain — explicit ws w1T" (explicit-worktree launch correction, one sighting).
- Mis-rooted lens incident spawned "one idle pi at the root" — zero-harm this time; the Gru-contamination guard held (see C7).

## Doctrine compliance notes (no candidates needed)

- **No NULL-pr self-report gaps this window** — every in-review row carries `pr`; "self-set ledger pr ✓" noted on 5.10, 7.1, 5.11, background-maps, 6.1, 6.2, 5.12, demo-mode, 7.3, qos. The verify-and-set guard + briefing line are holding.
- **Watcher-echo doctrine executed cleanly throughout** — every echo answered with a same-status classification note (sensor races 20:19:30Z, stale review echoes 07:05Z/16:30:54Z, settle echoes, billing-block CI echoes all note-only, zero double actions).
- **Moot-on-merge doctrine** — terminal-assets-5.11-perkins-r1 swept MOOT on the normal terminal merge (04:58:49Z), artifacts kept, chained job released per doctrine.
- **No-PR close-out doctrine** — security-audit: artifacts preserved to implementation-artifacts/, notification verified `shown:true`, lavish triage artifact (15:36:25Z).
