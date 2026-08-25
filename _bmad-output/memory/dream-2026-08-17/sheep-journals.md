# sheep-journals — candidate patterns for dream-2026-08-17

**Sources read (post-marker 2026-08-15T17:01:46Z only):**
- gru-journal/2026-08-16.md (full), 2026-08-17.md (full), 2026-08-14.md (post-marker entries only — file was backfilled 16 Aug; used entries from the dream-2026-08-15 close-out onward, ~17:05Z+)
- silas-journal/2026-08-16.md (full), 2026-08-17.md (full), 2026-08-15.md (entries from ~17:05Z onward only)

---

## USER RULINGS (high-value flags)

| # | Ruling (date) | Quote | Status |
|---|---|---|---|
| R1 | **kimi k3 back as reasoning tier** (08-16) | "kimi3 is back — use it for Bob, Gru, Perkins." Supersedes 08-14 glm-5.3; fallbacks glm-5.3 → v4-pro → flash; probe-before-first-round guard kept. | ✅ ALREADY PROMOTED (Silas, commit d270ce4; AGENTS.md supersede present) |
| R2 | **Billing de-gated** (08-16) | "ignore github billing for now — if we have integration tests." Local/integration tests = merge ground truth; billing caveat retired. | ✅ ALREADY PROMOTED (AGENTS.md 08-16 supersede) |
| R3 | **FULL THROTTLE Perkins** (08-16) | "run full throttle — don't worry about caps." Serialize-on-quota lifted, all providers; 429 wave = one continue per pane. | ✅ ALREADY PROMOTED (playbook + AGENTS.md amended) |
| R4 | **Perkins cap lifted per-job → loop-until-APPROVED** (08-17 ~01:5xZ) | "go more rounds. until we have an approval." — 3/3 cap lifted for #57; r4 dispatched, APPROVED. Later extended to ALL new jobs via R5 ("loop-until-APPROVED" now standard in Gru briefings). | ⚠️ NOT in playbook as standing doctrine — only a job-row note. PROMOTE. |
| R5 | **STANDING AUTHORIZATION — autonomous dispatch** (08-17 ~08:2xZ) | "dont wait foe me.. keep going." Gru briefs + dispatches the queue without per-step user acks; Perkins loop-until-APPROVED extended to new jobs; **MERGE ritual unchanged (user merges)**; countermand-able any time. | ⚠️ HIGH-VALUE, lives only in Gru journal. PROMOTE to playbook (Gru standing orders). |
| R6 | **Vision-capable model routing for visual jobs** (08-17 ~08:30Z) | 7.1-visual-juice on kimi-coding/k3 — "we need a model with native vision" (look-book canon, T2 pixel goldens, before/after re-bless). | ⚠️ Model policy has no capability-routing line. PROMOTE (one line in playbook Model policy). |
| R7 | **Lane ruling: intent layer = only legal home for a runtime key** (08-17 ~08:55Z) | ACCEPT the 7.2 M-mute input-touch; "the lane guard was over-broad — post-5.4 the intent layer is the ONLY legal home for a runtime key." | Project canon (PP). Belongs in PP GDD/decision-log or PP field-notes section. |
| R8 | **Full-game doctrine** (08-17 ~09:4xZ) | "we are building fully — prototype was already done." v2 IS the full-game build; E11 production-rebuild superseded; fun-test gate = content greenlight, not rebuild trigger. | Project canon; cascaded via #61 (merged). Note-only. |
| R9 | **Asset sources + licensing** (08-17) | SFX = ElevenLabs (paid = assigned/perpetual; SFX sublicense opt-out toggle at generate time); music = Suno Premier (owned incl. games; free tier = Suno owns, never generate there). ELEVENLABS_API_KEY in ~/.zshrc — **env-only rule: never in repo/logs/PR; new panes inherit, RUNNING panes predate the key**. | Project canon + the env-only-key ops rule is generalizable. |
| R10 | **Canon renders demoted + lavish-gated 2-phase visual direction** (08-17) | 8 canon renders "ugly" → composition/shape reference only; target = Mini Motorways flat-2D. 7.1 restructured: Phase A = style probe (2–3 treatments rendered as REAL game frames via the game's own draw code) via lavish HARD GATE → Phase B = implement. lavish added to skills policy. | Generalizable pattern for subjective visual work. PROMOTE (field notes + playbook lavish doctrine). |
| R11 | **Dream U1 APPLY / U2 SHELVE** (08-15 ~17:15Z) | U1: playbook model policy merged into one glm-5.3 block (later superseded by R1). U2: settle-echo suppression shelved low-pri. | ✅ Executed same evening. |

---

## CANDIDATE PATTERNS

### 1. Lavish verdict recovery: session ended + 0 rulings = poll raced the submit — RE-POLL before doubting the user
- **Example:** terminology-audit, 08-15 ~23:35Z (silas-08-15): "The user's Q1-Q4 answers WERE queued (lavish state.json: session ended_by user, 4 pending prompts) — the minion's poll died on a harness timeout before collecting; my earlier 'prompts: 0' note was stale." Gru: "the lavish submit ended session 36b4f1ff33e248bd but the minion's poll died to harness timeout before collecting; re-poll fetched the queued feedback (the never-lost-queue property held)."
- **Ops rule already written in Gru journal:** "session 'ended' + 0 rulings recorded = poll raced the submit — re-poll before doubting the user."
- **Caveat:** lavish 0.1.52 (08-17) changed the poll mechanics (see candidate 12) — promote reconciled with the new workflow.
- **Target:** field notes (lavish traps).

### 2. herdr server restart is SURVIVABLE; watcher vanish-alerts during the transition = noise
- **Example:** herdr 0.8.0 upgrade 08-16 ~09:12Z (silas-08-16 ~10:45Z): "all 7 pi processes survived… pane ids UNCHANGED"; nefario-watch fired "pane no longer has a detected agent" for all 5 tracked panes — false alarm, ledger-noted, no action. Gru: "Field-note worth filing: herdr restart = survivable, alerts are noise; verify then sweep orphans."
- **Verify procedure:** pane ids unchanged if session restored + pi processes mapped via lsof cwd — before acting.
- **Bonus lesson (same entry):** worktree removal does NOT kill spawned processes — 3 stuck core.bin (removed 5.2 worktree) spinning ~3.5 cores since 1am + 2 orphaned beam.smp dev servers from closed-out jobs killed. Sweep orphan processes at close-out/census.
- **Tooling delta:** 0.8.0 syntax — `herdr agent wait <pane> --until idle`; `tab create` JSON gives `root_pane.pane_id`.
- **Target:** AGENTS.md watchers gotcha + field notes tooling traps.

### 3. Perkins lens close-sweeps must scope to OWN pane ids — lens tabs share the generic label
- **Example (near-miss):** 08-17 ~09:15Z, 5.5-r1 (silas-08-17): "lens close-loop found 7 more mm-*-r1 panes (tab tDT, 'perkins-r1-lenses') with the SAME labels and nearly killed the sibling 7.2-r1's in-flight lenses (4 working). Relayed STOP… 5.5-r1 closed only its own 7."
- **Same-day recurrence (lesson held):** doctrine-r1 close-out ~10:25Z "correctly LEFT the sibling 7.2-r2 lenses alone (label-collision lesson held)".
- **Corollary (08-16 ~00:20Z sweep):** lens fleets live in SEPARATE workspaces (w2N traffic-model lenses verified LIVE, untouched) — verify cwd/session before killing strays.
- **Full-throttle makes this bite harder** (R3): concurrent rounds are now the norm → colliding `perkins-r1-lenses` labels are guaranteed.
- **Target:** AGENTS.md Perkins gotcha. STRONG.

### 4. Redispatching a done job id = ledger row RESET — NULL the `pr` field FIRST
- **Example:** 08-17 ~08:15Z, 5.5 dispatch (silas-08-17): "REUSED the canonical id (UNIQUE conflict on add) — 08-14 stub (done, #44 merged pre-intent-layer) reset: done→dispatched→working, pr NULLed (stale #44 would have tripped the PR watcher at in-review)."
- **Same-day ×2:** 5.5-r1 round row (~08:45Z): "OLD 08-14 r1 row (reviewed superseded #44) RESET — pr→#59, worktree/pane/tab updated, model→kimi k3, result cleared, redispatch note."
- **Target:** AGENTS.md Ledger gotcha (sibling to the phantom-row lesson — this is the legitimate-reuse flavor).

### 5. A doc-only head push does NOT re-trigger a round (sensor echo, classify not dispatch)
- **Example:** 08-17 ~09:30Z, 7.2 (silas-08-17): "Doc-only head adfcb19 gets NO r2 (sensor echo classified — r2 fires on the fix sha)."
- **Target:** Perkins stability-gate gotcha — new flavor: head moved but the delta is docs-only → echo.

### 6. Merge-train hygiene: send the rebase relay BEFORE the rework push
- **Example:** 08-17 ~09:35Z (silas-08-17): "7.2 merge-order pre-empt: #59 first → #60 rebases (types/exec/poll overlap) — rebase relay sent before the B1 fix push lands so r2 reviews one clean head." Result: r2 APPROVED on one clean head 1b96bea.
- **Target:** field notes conventions / playbook merge ops.

### 7. Held jobs recorded as PANELESS rows with the release trigger on the row — fires at the named close-out
- **Example:** 08-17, 7.1-visual-juice (silas-08-17 ~08:25Z): "row added with the hold note — release trigger = packet-plumber-v2-5.5-demolish-input MERGE CLOSE-OUT… No pane/worktree until release." Fired on cue ~09:35Z ("RELEASE TRIGGER FIRED… dispatched").
- Extends the already-promoted durable-routing ruling with mechanics: held row carries trigger + model + pr_review; release = resolve fresh head then dispatch.
- **Cross-window recurrence:** same mechanics as serialize-held Perkins rounds (5.2-r1 held behind traffic-model r2/r3, 08-16 ~00:50Z, sha refreshed ef7c0f0→088fdcd during the hold per held-row hygiene).
- **Target:** extend the serialize-hold gotcha.

### 8. Close-out base-sync hazard: preserve-to-_bmad-output collides when a later PR commits the same path
- **Example:** 08-16 ~08:50Z, traffic-model-design close-out (silas-08-16): "git pull --ff-only aborted — the main checkout held UNTRACKED copies of the surge-explainer artifact that PR #53 committed (r1 W3 fix). Verified the committed tree carries the artifact, moved the untracked copy aside, pulled @ e7fa548, diffed (byte-identical) → removed the /tmp copy."
- Cause chain: the 08-15 preserve-before-sweep rule copies deliverables to the main checkout → a later PR commits that same path into git → next pull hits the untracked collision.
- **Target:** field notes tooling traps (close-out checklist: pull-fail → check untracked artifact collisions first).

### 9. A long-running minion (18–20h) is not a stall — verify via session-file growth before classifying
- **Example:** 5.2-node-health ~20h (gru-08-14 post-marker): "5.2 (p1NV) verified ALIVE (session growing, toolUse) — 18h+ is deep work, not a stall." Silas at badge-out (08-16 ~00:50Z): "the ~20h was REAL DESIGN WORK (probed the sim… chose the stuck-pile measure SHARED with 4.1 — coherence over invention)."
- **Cross-day recurrence:** verified twice independently (user-asked census 08-15, badge-out 08-16) — the check preceded any `continue`/revive reflex both times.
- **Target:** pane-forensics gotcha (inverse of the dead-pi-idle trap: long ≠ stuck; session mtime/toolUse growth = alive).

### 10. Merge-base check before blessing goldens — PR-event CI builds the MERGED tree
- **Example:** 08-16 ~01:00Z, PR #54 CI failure (silas-08-15 late entries): "PR-event CI builds the branch MERGED into origin/v2 (Open Sans render) vs the old-font T2 blessing; push-event run + local passed (hence the green same-sha twin)." Fix (~01:05Z): clean v2 merge + deliberate 3-PNG T2 re-bless. A same-sha green twin run is the signature of this class.
- **Status:** Silas wrote "Lesson badged to field notes (merge-base check before blessing)" — verify it actually landed in the 5.2 shard/field notes before re-promoting.
- **Target:** field notes (PP golden discipline).

### 11. GitHub platform outage = its own incident class: retry beats alert, no holds; local merge+push recipe unblocks merges
- **Example:** 08-17 ~15:1xZ, GH major outage since 13:40Z (gru-08-17): "API/PRs/Issues/Actions, webhooks partial, ~20% error rate; git operations GREEN." Silas doctrine: "API flakes / sensor gaps / webhook lag = incident noise (retry beats alert); Perkins local verification unaffected; no holds."
- **Merge unblocked locally:** user merged #61 + #60 via local-merge+push CLI recipe (web merge down), 8s apart; webhooks lagged the watcher alerts ~4 min.
- Sibling of the billing-block class (which recurred twice more this window, note-only per R2 — 08-16 ~10:00Z, 08-17 ~00:48Z).
- **Target:** provider-incidents gotcha (new class).

### 12. Tool updates silently change agent-facing contracts — sync the on-disk skill + relay deltas mid-flight (lavish 0.1.52)
- **Example:** 08-17 ~17:00Z (silas-08-17): layout issues now file PASSIVELY (user-queued only — agents NEVER auto-repair unqueued; only fatal artifact_failures interrupts the poll); NEW self_paint_warning mechanic. "Our on-disk skill was stale (old auto-repair workflow)" → synced from npx cache → committed 0f1b916 → deltas relayed to in-flight 7.1 minion (p1Z3).
- **Target:** field notes tooling traps (skill-staleness watch) — and reconcile with candidate 1.

### 13. Perkins self-close + orchestrator death = orphaned `working` round row — fresh-session catch-up must reconcile ROWS, not just panes
- **Example:** 08-17 ~00:50Z (silas-08-17): r3 posted its verdict 00:04:31Z and "cleaned its own lens panes and exited expecting Silas' close-out — old Silas died before doing it, row sat working overnight ~1h." Catch-up closed it (verdict recovered as note, pane/worktree swept); minion p1Q9 found dead-at-shell and relaunched via the standard path.
- **Target:** Perkins self-close gotcha — add: after any orchestrator respawn, sweep non-done round rows against posted reviews.

### 14. Full throttle on kimi k3 held — first 3-round parallel burst, zero 429s
- **Example:** 08-16 ~18:40Z (silas-08-16): "Full-throttle burst (3 concurrent kimi rounds, first since 08-12)… No 429 waves on the parallel burst." Also 08-17: two concurrent k3 rounds (5.5-r1 + 7.2-r1) clean.
- Confirmation data for R3 (already promoted) — worth one line so future sessions don't re-litigate the serialize reflex on kimi.
- Bonus capability note (08-16, #56 verdict): Perkins "re-verified determinism firsthand: harness 29/29 T1/T2 byte-identical, capture_frame never calls draw_hud" — rounds run the harness themselves, not just read claims.
- **Target:** one-line addendum to the serialize gotcha.

### 15. Orchestrator respawn: the extension startup checklist beats the handover
- **Example:** 08-17 ~00:47Z (gru-08-17): Silas respawned — "His extension beat the handover to it: checklist injected at session_start, he ran it unprompted."
- Minor: respawn doctrine — the extension carries the checklist; the handover only needs state deltas.
- **Target:** field notes (minor).

---

## Borderline (08-15 16:35–17:01:46Z — inside the marker window, possibly already dreamed)

- **Explainer close-out + correction on record** (~16:45Z): "CORRECTION ON RECORD: my in-chat diagnosis of the 99-vs-95 drop gap (class priority) was WRONG — email + streaming both default to the Standard lane; the gap is run arithmetic (artifact, evidence-grade)." Lesson: in-chat mechanical hypotheses are provisional until evidence-verified; record corrections explicitly. (Minor Gru-hygiene note if undreamed.)
- **Ruling: explainer Section B design notes are TASKS** (~16:45Z) → traffic-model-design dispatched. Already executed; note-only.

## Recurrence summary (cross-day signals this window)
- Perkins self-close is fully the norm (r3/r4/5.5-r1/7.2-r1/r2/doctrine-r1 all self-closed clean); the NEW risk is orchestrator-side (candidate 13), not Perkins-side.
- Billing-block recurrence classified note-only ×2 with zero wasted reruns — R2 doctrine holding.
- Minions self-setting `ledger pr` now routine on the PP crew (5.5, 7.2: "self-set ledger pr ✓" ×2 on 08-17) — the RTA-crew NULL-pr gap did NOT recur this window; verify-and-set guard still the backstop.
- Label/id-scoping discipline recurred 3× in one day (candidate 3 near-miss → doctrine-r1 held → w2N sweep verified) — fastest propagation of a lesson seen.
