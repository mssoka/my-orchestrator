# Sheep shard: sheep-ledger (source = ledger event stream, post-marker)

Sheep for Bob's dream-2026-08-11. Source = `/Users/moses/code/bin/ledger`
event stream + `show` detail. Marker = `2026-08-09T13:54:22Z`
(dream-2026-08-09 row). Everything below is dated AFTER the marker.
Read-only — no ledger writes, no live-store edits. Bob filters (≥2
independent sightings to promote; I surface generously with evidence).

Window shape: 2026-08-09 evening → 2026-08-11 ~14:21Z. Dominant threads =
the **kimi-quota-403 saga** (rc3-3/rc3-5 Perkins, odin-prototype r2) +
the **glm-5.2 fallback model** becoming the sanctioned Perkins review
model + a dense **Perkins multi-round rework chain** on RightTenantry
(rc3-4 r1→r2→r3) and RightTenantryAgents (#173 r1→r2 → #174 r1).

---

## NEW candidates

### C1 — A Perkins round can be HELD on an UNSTABLE review target (not just pane capacity)
- Target: AGENTS.md gotchas → "Watchers, sensors & Perkins rounds" (new sibling to the serialize-hold entry)
- Class-hint: NEW (distinct from serialize-hold, which gates on PANE capacity; this gates on REVIEW-TARGET stability)
- Lesson: A Perkins fix-audit round is deferred when the PR head is still MOVING (minion iterating CI fixes / active A/B reshaping) AND/OR CI is RED — the harness verification can't run on a red/unstable CI. Hold for the STABLE sha (CI green + r1 blockers addressed + minion done iterating). Expect the review sensor to RE-FIRE on every new commit while the head moves — those are echoes, not new work. Answer each with a same-status note, never a double dispatch.
- Evidence:
  - packet-plumber-odin-prototype (2026-08-09T18:43:36Z): "Perkins r2 on #17 HELD — head fc3ca42 is unstable: CI RED (ubuntu segfault + macOS catalog drift), minion still pushing gdb/segfault fixes... r1 blockers (B1 app.bin, B2 demolish) unaddressed. The r2 harness verification can't run on a red CI. Dispatch r2 on the STABLE sha... Sensor will re-fire on each new sha until then — echoes."
  - packet-plumber-odin-prototype (2026-08-09T19:13:22Z): "Perkins r2 STILL HELD (head now 0b92fa4)... the head is still MOVING — 0b92fa4 is a FEATURE commit (Mini-Motorways hardware inventory replaces the budget, a user ruling from the A/B)... r2 fix-audit runs on the STABLE sha (A/B verdict + CI fully green + minion done iterating)."
- Why it makes future sessions smarter: Stops Silas dispatching a fix-audit onto a target that's still churning (wastes a round + a worktree); codifies the "sensor re-fires per-commit while head moves = echoes" echo class so they aren't mistaken for new review events.

### C2 — A Perkins round can be USER-PAUSED mid-review (user chats the Perkins pane directly)
- Target: AGENTS.md gotchas → "Pane forensics" (new) OR "Watchers, sensors & Perkins rounds"
- Class-hint: NEW
- Lesson: The user can pause a Perkins round by interrogating its pane directly (asking scope/stage questions). The Perkins agent answers well (flags premature steps, defers dispatch to Gru), then idles awaiting the user's keep-going/pause call. The round STAYS `working` (in-flight, user-paused) — the pane watcher must NOT read that idle as done/blocked/settle. Provenance: it's the user in the pane (direct chat), not a verdict — treat any "next stage" answer as FYI, route dispatch decisions back through Gru.
- Evidence:
  - packet-plumber-odin-prototype-perkins-r2 (2026-08-09T22:48:51Z): "USER-PAUSED: the user is directly interrogating this pane about the Odin pivot stage/scope ('we've not re-written the architecture right? not sure what stage we are'); Perkins clarified it's the prototype-build implementing arch-v1 #15... Awaiting the user's keep-going/pause decision... Status stays working (in-flight, user-paused)."
  - packet-plumber-odin-prototype-perkins-r2 (2026-08-09T22:51:54Z): "user-pause CONTINUES — the user now asked Perkins 'what's the next stage' + typed /gds-sprint-planning... Perkins (glm-5.2) answered well... correctly flagged sprint-planning PREMATURE before the fun-gate + that it's Gru's dispatch (review-only)... Round still mid-review... Status stays working."
- Why it makes future sessions smarter: Prevents a watcher/Silas from "recovering" or closing a healthy user-paused Perkins round, and stops acting on a Perkins pane's stage-advice as if it were an ops verdict.

### C3 — Silas model-QUOTA gating: DEFER ALL mega-minions behind a Perkins round on the shared fallback model
- Target: AGENTS.md gotchas → "Dispatch & handover" (new) or "Provider incidents"
- Class-hint: NEW (distinct from serialize-hold = pane capacity; this is MODEL-QUOTA capacity on the shared fallback model)
- Lesson: When the primary model (kimi) is quota-down and everything falls back to glm-5.2, the glm-5.2 quota is SHARED and contended. Silas gates mega-minion spawning behind the in-flight Perkins round: ruling = "DEFER ALL mega-minions until Silas signals (the Perkins round must complete clean)." The minion builds single-threaded and ACKs. The ruling is delivered as a direct `pane run` from Silas with explicit provenance ("ops ruling, not a verdict"). Lift = the Perkins round closes clean → glm-5.2 freed.
- Evidence:
  - packet-plumber-routing-explorer (2026-08-09T23:45:49Z): "building v1 single-pane (no swarm — glm-5.2 quota shared w/ Perkins rc3-3)"
  - packet-plumber-routing-explorer (2026-08-09T23:47:25Z): "Silas concurrency ruling (direct pane): DEFER ALL mega-minions entirely until Silas signals (Perkins rc3-3 r2 on glm-5.2 must complete clean). Building single-threaded. Provenance: direct pane-run from silas, ops ruling (not a verdict) — acked."
  - packet-plumber-routing-explorer (2026-08-10T00:48:35Z): "Silas ruling (direct pane): mega-minion DEFERMENT LIFTED — Perkins rc3-3 r2 CLOSED (APPROVED), glm-5.2 freed."
- Why it makes future sessions smarter: Stops a minion fanning out a review/lavish swarm that 429-starves the in-flight Perkins round under quota pressure; codifies the direct-pane-run ruling + provenance shape so the minion doesn't mistake it for a verdict.

### C4 — Three model ROLES, independently reassignable by user ruling (minion vs Perkins-review vs lens-workers)
- Target: AGENTS.md gotchas → "Provider incidents" / "Model dispatch & correction ops" (extend the /model-mid-session entry)
- Class-hint: NEW nuance on the existing model-switching gotcha
- Lesson: Model policy is per-ROLE, not per-job. At least three roles: the minion/worker model, the Perkins REVIEW model, and the lens-worker model. A user ruling (relayed by Gru) can reassign them INDEPENDENTLY and MID-FLIGHT — e.g. Perkins review flips deepseek→kimi while the minion stays its own model; later workers flip to glm-5.2 while the minion stays kimi. The ruling lands as a "MODEL POLICY UPDATE" note on the round row; the minion ACKs and keeps its own model. Don't assume one model per dispatch.
- Evidence:
  - packet-plumber-odin-prototype-perkins-r2 (2026-08-09T20:04:50Z): "MODEL POLICY UPDATE (user ruling 2026-08-09, Gru relayed): Perkins review model is now kimi-coding/k3 (was deepseek-v4-flash)... The rc3-3 r1 finishes on deepseek (in-flight, no kill). All future Perkins rounds = kimi-coding/k3."
  - packet-plumber-odin-prototype (2026-08-09T20:51:21Z): "model policy ack: workers -> zai-coding-cn/glm-5.2 per GRU ruling; minion stays kimi-coding/k3"
- Why it makes future sessions smarter: Stops Silas forcing a single model onto every role, and stops killing/re-dispatching when a role-level `/model` flip is all the ruling asked for.

### C5 — LATENT pre-existing bug → P0 when a SEPARATE change raises the trigger rate (check blast radius)
- Target: minion-field-notes.md → "Conventions that saved time" or "Recurring review findings" (new)
- Class-hint: NEW
- Lesson: A bug can be latent (rare trigger, no prod symptom) and become P0 when an UNRELATED later change raises the trigger frequency — e.g. a gate state-marshalling bug that rarely fired until a model-quality change raised the clean-verdict rate. When fixing, grep prod for the blast radius (confirmed instances in a window) and grade P0 by the new rate, not the old. Note the latent-vs-active distinction in the PR so review doesn't under-weight it.
- Evidence:
  - righttenantryagents-boundary-gate-state-fix (2026-08-10T18:23:10Z): "#169 finding: LATENT (reads predate #169; model-flash raised the clean-verdict rate -> P0). Blast radius: 1 confirmed instance/30d (re-process run_id=e-9aeb254d-)."
- Why it makes future sessions smarter: Tells future minions to look for the trigger-rate amplifier when a latent bug surfaces, and to size severity by the post-amplifier rate.

### C6 — Drive-by rename in a fix PR breaks a name that's a CONTRACT (telemetry event / test id)
- Target: minion-field-notes.md → "Recurring review findings" (new)
- Class-hint: NEW
- Lesson: A "harmless" spelling correction (review_unparseable→review_unparsable) committed as a drive-by in a fix PR is dangerous when the token is a CONTRACT — a telemetry event name (BQ/Sentry), a test name, or an API surface. It breaks the pinned test AND the downstream analytics contract; Perkins flags it as a blocker. Leave contract tokens alone in a fix PR, or rename them end-to-end (token + every consumer + test) in the same change.
- Evidence:
  - righttenantryagents-boundary-gate-state-fix-perkins-r1 (2026-08-10T19:03:02Z): "B1: accidental telemetry rename review_unparseable->review_unparsable (compliance_enforcement.py:239, drive-by in the diff) — breaks test_unparseable_review_emits_failed_rollup + the BQ/Sentry event-name contract; fix = restore the e."
- Why it makes future sessions smarter: Stops a recurring Perkins-blocker class caused by drive-by "tidy" renames; tells authors to treat telemetry/event/test tokens as load-bearing.

### C7 — The "registry-omission" blocker class: every new POST route must be registered in ALL registries
- Target: minion-field-notes.md → "Recurring review findings" (new, RightTenantry-specific but the pattern generalizes)
- Class-hint: NEW (recurred ≥3 times; now baked into briefings as a named lesson)
- Lesson: Adding a POST route means registering it in EVERY access-control/observability registry the codebase maintains (is_public_path, CSRF allowlist, redact_token_route, etc.). Missing one is a recurring Perkins blocker (csrf arm absent → route 403s or redaction gaps). The fix is now propagated INTO briefings as a named carry-forward ("the rc3-3 csrf-registry lesson" / "the rc3-2 redact gap") — when adding ANY new route, enumerate every registry and arm each.
- Evidence:
  - righttenantry-refcheck-rc3-3-perkins-r1 (2026-08-09T21:02:41Z): "B1 (csrf.should_skip missing ["reference",..] arm — same registry-omission class as the rc3-2 redact gap; 3-lens agreement)"
  - righttenantry-refcheck-rc3-4 (briefing note): "MUST register every new POST route in ALL 3 registries (is_public_path, CSRF allowlist, redact_token_route) — the rc3-3 csrf-registry lesson."
- Why it makes future sessions smarter: Pre-empts a whole blocker class at authoring time; the cross-round naming shows the lesson is sticking only because briefings repeat it.

### C8 — pr_review=0 "ops-helper" job class: PR opened, Perkins OFF, USER reviews the diff directly
- Target: AGENTS.md gotchas → "Watchers, sensors & Perkins rounds" (extend the no-PR-job entry, or new)
- Class-hint: NEW nuance between full-Perkins and no-PR
- Lesson: A job can carry `pr_review=0` — a PR IS opened (so the PR watcher catches the merge) but Perkins is OFF and the USER reviews the diff directly. Close-out does NOT wait on a Perkins round; it waits on a human merge. The "is there a Perkins round pending?" check is the wrong gate for this class — verify `pr_review` on the job, not just `pr` presence.
- Evidence:
  - righttenantry-find-stuck-terminal (2026-08-11T11:10:59Z): "PR #601 OPEN (-> develop; pr_review=0 — ops helper, awaiting USER review of the diff)."
  - righttenantry-find-stuck-terminal (briefing note): "pr_review=0 (ops helper; user reviews the diff)."
- Why it makes future sessions smarter: Stops Silas holding close-out for a Perkins round that will never fire, and stops arming Perkins on a job the user wants to review themselves.

### C9 — lavish SVG: insertBefore on a non-child throws NotFoundError, aborts draw() mid-loop but looks "working"
- Target: minion-field-notes.md → "Tooling traps" (lavish craft)
- Class-hint: NEW (single sharp sighting; generous surface)
- Lesson: In a hand-built SVG lavish artifact, `el.appendChild` + `insertBefore(nextSibling)` blows up when nextSibling isn't a child of the parent (throws NotFoundError on the first visited node). The throw aborts draw() mid-loop, but because the trace/state was updated BEFORE draw, the page looks "working" (partial render) — a silent render failure. Fix: maintain an explicit z-order with ALL elements as direct children of the svg root (pipes→rings→nodes), no insertBefore gymnastics. Verify the full expected node count rendered, not just "something drew."
- Evidence:
  - packet-plumber-routing-explorer (2026-08-10T00:04:51Z): "Lavish round 1 (user): BFS map broken — only R1 renders, no highlights. Root cause: draw() visited-ring code does el(circle, svg.firstChild)+insertBefore(nextSibling) → insertBefore into a path whose nextSibling isn't its child throws NotFoundError on first visited node, aborting draw() mid-loop (trace updated before draw so looked 'working'). Fixing ring z-order (pipes→rings→nodes, all direct svg children)."
- Why it makes future sessions smarter: A reusable lavish/SVG craft trap — the "looks working but aborted mid-loop" failure mode is easy to miss without a node-count assertion.

---

## AMEND / REINFORCE candidates

### C10 — Perkins catches an INERT fix + its masking test; the lesson now propagates INTO briefings by name (AMEND)
- Target: minion-field-notes.md → extend "Node tests are blind to browser-runtime semantics" (2026-08-03) + "prove a new test/guard actually BITES" (2026-08-09)
- Class-hint: AMEND (elevates a minion-tooling lesson into a Perkins-enforced + briefing-named convention)
- Lesson: Perkins now reliably catches the class where a fix is INERT (the value ships in HTML but the JS never populates it) AND the accompanying test MASKS it (drives `simulate.form_body` which bypasses the real browser path). The remediation convention has crystallized: wire the real submit listener + drive the BROWSER path in the node test (not the simulator), and prove the test bites (neutralize the fix → test fails). This is now referenced BY NAME in downstream briefings ("the #599 r2 lesson") as a mandatory guard.
- Evidence:
  - righttenantry-refcheck-rc3-4-perkins-r2 (2026-08-10T20:31:00Z): "NEW BLOCKER B2-r2 (6-lens): W1's fix is INERT — _focus_seconds ships in the review-form HTML but reference_form.js never populates it... -> focus_seconds_reported still always 0 in prod; the new flow test MASKS it (simulate.form_body bypasses the browser). Fix: wire a submit listener on reference-review-form + a node test."
  - righttenantryagents-boundary-gate-slot-clear (briefing note): "REQUIRED regression test driving the REAL path (NOT a simulate.form_body mask — the #599 r2 lesson)."
  - righttenantryagents-boundary-gate-slot-clear-perkins-r1 (2026-08-11T01:17:52Z): "W1: the regression tests model an unreachable window — the clean stamp derives from the SAME slot whose write the test claims lost; the fix is still correct per-attempt" (same masking-test class caught again).
- Why it makes future sessions smarter: Confirms the simulator-masks-the-fix failure mode is now a Perkins specialty AND a briefing-propagated convention; future authors pre-empt it by defaulting to browser-path tests.

### C11 — kimi-quota-403 "back up" premise breaks WITHIN a billing cycle; `/model + continue` = zero-loss recovery for a FIRST-TURN 403 (AMEND)
- Target: AGENTS.md gotchas → "Provider incidents" (extend the glm-5.2 / quota-403 entries)
- Class-hint: AMEND (2026-08-02/07/09 provider-incidents gotcha)
- Lesson: The "kimi is back up" signal (another job's activity / a Gru nod) is UNRELIABLE mid-billing-cycle — quota-403 can recur within ~12 minutes of an apparent recovery. The durable, zero-loss recovery for a FIRST-TURN 403 (no lenses/artifacts yet) is a mid-pane `/model <fallback> + continue` — pane recovers to working, no re-dispatch, no regenerate. glm-5.2 is now the sanctioned Perkins fallback (proven by the odin r2 run). For a MID-WORK 403 (partial lens JSONs), the full sweep+regenerate doctrine still applies.
- Evidence:
  - righttenantry-refcheck-rc3-3-perkins-r2 (2026-08-09T23:16:52Z): "KIMI QUOTA 403 AGAIN mid-review (billing-cycle limit, NOT a rate-limit)... The 'kimi is back up' premise (Gru 23:05) broke."
  - righttenantry-refcheck-rc3-5-perkins-r2 (2026-08-11T13:55:50Z): "Model redirect: kimi-coding/k3 403'd at launch (quota exhausted this billing cycle) -> switched to zai-coding-cn/glm-5.2 (r1's sanctioned fallback) via /model + continue; pane recovered to working. No work lost (first-turn 403, no lenses/artifacts)."
- Why it makes future sessions smarter: Adds the "back-up premise is unreliable" + "first-turn 403 = /model+continue, not sweep" recovery shape to the provider playbook.

### C12 — Retry-DOCTRINE: a 403-killed round retries on the SAME row (not rN+1); sweep ALL dead panes + fresh worktree + regenerate lenses (AMEND)
- Target: AGENTS.md gotchas → "Provider incidents" / "Watchers, sensors & Perkins rounds" (Perkins self-close)
- Class-hint: AMEND (2026-08-02 quota-403 sweep+regenerate doctrine)
- Lesson: A Perkins round killed by quota-403 mid-review is a RETRY on the SAME round row — NOT a new round (don't increment rN). Recovery: sweep every dead pane in the fan-out (8 kimi-dead panes in one sighting), re-add a FRESH worktree at the same sha, regenerate ALL lens JSONs (discard partial artifacts — 3-byte empties contaminate the verdict). Carry the prior round's confirmed findings forward in the briefing so the retry confirms rather than re-discovers.
- Evidence:
  - righttenantry-refcheck-rc3-3-perkins-r2 (2026-08-09T23:23:08Z): "RETRY #1 on glm-5.2 (kimi quota-403 killed the first attempt mid-review). Swept all 8 kimi-dead panes (pPA+7 chunk-1 lenses); fresh worktree @ 84f5b94... B1 carry-forward noted in briefing (confirm, don't re-discover)... NOT r3 — same r2 row, retry-doctrine."
  - packet-plumber-odin-prototype-perkins-r2 (2026-08-09T21:42:23Z): "KIMI QUOTA 403 mid-review — consolidation never completed (consolidated.json ABSENT; partial lens JSONs litter r2 dir, e.g. acceptance-b/e = 3-byte empties)... On re-dispatch: REGENERATE all lens JSONs (discard partial r2 artifacts — they contaminate the verdict)."
- Why it makes future sessions smarter: Locks the round-naming + sweep-scope + regenerate rule so a retry doesn't masquerade as a new round or inherit poisoned partial artifacts.

### C13 — Stale echo on a model-REDIRECT recovery: pane-watcher catches the transient post-403 'done' before /model+continue (AMEND)
- Target: AGENTS.md gotchas → "Watchers, sensors & Perkins rounds" (settle/boot echo entries)
- Class-hint: AMEND (a new echo sibling to settle + boot `gone -> idle`)
- Lesson: When a 403 kills a turn and `/model + continue` revives it seconds later, the pane-watcher can catch the transient `gone -> done`/`done` flicker in between and echo it as an alert. Classify via the round row + pane read: if the pane is now working on the fallback model, the 'done' was the pre-recovery transient — note-only, no action. Distinct from a real close (which leaves the row done AND the round consolidated).
- Evidence:
  - righttenantry-refcheck-rc3-5-perkins-r2 (2026-08-11T14:00:40Z): "Pane-watcher echo (13:48:15Z gone->done): stale — captured the transient post-kimi-403 'done' before the /model+continue recovery. Pane verified working on glm-5.2... No double-action."
- Why it makes future sessions smarter: Adds the model-recovery flicker to the echo-classification checklist so Silas doesn't close/re-dispatch a round that's already healed.

### C14 — `pr` field still occasionally NULL on minion self-report; the convention propagated to RT+PP crews but is NOT universal (AMEND)
- Target: AGENTS.md gotchas → "Ledger" (`set in-review` does NOT populate `pr`)
- Class-hint: AMEND (2026-08-07 gotcha; reinforcement + asymmetry note)
- Lesson: The "minion runs `ledger pr` itself at in-review" convention has propagated into the RightTenantry and packet-plumber crews (multiple "pr field set by the minion (convention holding)" notes this window), BUT it is NOT universal — the RightTenantryAgents crew still produced a NULL `pr` on self-report (PR watcher would've skipped it). Silas must still VERIFY `pr` on every in-review transition (the table view lies; use `ledger show`); don't trust propagation alone.
- Evidence:
  - righttenantryagents-boundary-gate-state-fix (2026-08-10T18:23:10Z): "pr field was NULL (minion set in-review w/o ledger pr) — set. Perkins sensor will fire on #173's sha (pr_review=1)."
  - righttenantry-apply-form-scrub-fix (2026-08-10T12:54:18Z): "pr field now set (was NULL — the minion set in-review without ledger pr; PR watcher would've skipped it)."
  - vs. righttenantry-refcheck-rc3-4 (2026-08-10T19:01:19Z): "pr field set BY THE MINION (ledger pr — the convention propagated)."
  - righttenantry-find-stuck-terminal (2026-08-11T11:10:59Z): "pr field set by the minion (the convention is holding)."
- Why it makes future sessions smarter: Stops Silas relaxing the `pr` verification just because most crews now self-set it; the RTA miss proves propagation is leaky.

### C15 — Serialize-hold is now heavily used CROSS-REPO; the release trigger is the in-flight round's close-out (AMEND)
- Target: AGENTS.md gotchas → "Watchers, sensors & Perkins rounds" (serialize-hold entry)
- Class-hint: AMEND (2026-08-07 serialize-hold; ≥4 fresh cross-repo sightings)
- Lesson: The pre-create-the-round-row serialize-hold is now standard ops across repos (RightTenantry ↔ packet-plumber), not just same-repo pane capacity. The held round's briefing names the in-flight round it's behind ("SERIALIZE-HELD behind perkins-v2-1.2-window-draw-pipe-r1 (pRS in flight; board at valve edge ~20)") and the RELEASE trigger (the in-flight round's close-out). The held round's pane stays dispatched (sensor dedup'd) until release.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10T19:01:19Z): "Perkins round HELD (serialize behind #173's round)."
  - righttenantryagents-boundary-gate-state-fix (2026-08-10T19:12:38Z): "Awaiting Perkins r2 (auto-fires on the new sha) — HELD for serialization behind rc3-4's round."
  - righttenantry-refcheck-rc3-5 (2026-08-11T09:48:08Z): "Perkins r1 HELD (serialize behind #22's in-flight round)."
  - righttenantry-refcheck-rc3-5-perkins-r1 (briefing note): "SERIALIZE-HELD behind perkins-v2-1.2-window-draw-pipe-r1 (pRS in flight; board at valve edge ~20 with both). RELEASE when pRS's round closes."
- Why it makes future sessions smarter: Confirms serialize-hold is the default valve mechanic now; the named-behind + named-release-trigger briefing shape is the durable practice.

### C16 — "settle (working->done after clean completion)" is now a STANDARD pre-emptive close-out note (AMEND)
- Target: AGENTS.md gotchas → "Watchers, sensors & Perkins rounds" (settle-transition entry)
- Class-hint: AMEND (2026-07-29 settle-transition gotcha; practice crystallized)
- Lesson: Silas now pre-emptively writes a "settle (working->done after clean completion): <summary>" note at close-out to classify the inevitable watcher settle-transition echo before it fires. This is the durable dedup for settle noise: the note IS the classification, so the echo that follows is note-only. The note also doubles as the human-readable completion summary (PR + suite counts + what was proven).
- Evidence (5 sightings, one window):
  - righttenantry-refcheck-rc3-4 (2026-08-10T20:03:08Z): "settle (working->done after clean fix-push): Perkins r1 on #599 FULLY addressed..."
  - righttenantryagents-boundary-gate-state-fix (2026-08-10T18:23:10Z / 19:12:38Z): "settle (working->done after clean completion): PR #173 OPEN..."
  - righttenantry-apply-form-scrub-fix (2026-08-10T12:54:18Z): "settle (working->done after clean completion): PR #597 OPEN..."
  - righttenantry-find-stuck-terminal (2026-08-11T11:10:59Z): "settle (working->done after clean completion): PR #601 OPEN..."
  - packet-plumber-sprint-replan-v2 (2026-08-11T02:02:29Z): "settle (working->done after clean completion): PR #20 OPEN..."
- Why it makes future sessions smarter: Codifies the pre-emptive settle-note as the standard close-out step (not optional) — it's both the dedup and the summary.

### C17 — Mid-job sibling-PR merge → rebase; for an append-only decision-log, resolve as DUAL-APPEND (keep both) (AMEND)
- Target: minion-field-notes.md → extend the canon-doc AMENDMENT craft entry (2026-08-09) and/or the in-repo follow-up gotcha
- Class-hint: AMEND (2026-08-09 canon-doc amendment craft; 2026-08-07 in-repo follow-up)
- Lesson: When a sibling canon-doc PR merges MID-JOB (your branch is off the same base), rebase onto it. For a decision-log / append-only file, the merge conflict resolves as DUAL-APPEND (keep both entries) — don't pick a side. Verify the rebased PR is MERGEABLE/CLEAN and update the body. (Generalizes the in-repo follow-up tree-conflict handling to the sibling-merge case.)
- Evidence:
  - packet-plumber-gdd-mechanics-amend (2026-08-10T14:27:47Z): "PR #18 merged mid-job → rebased onto it; gdd.md auto-merged clean, decision-log dual-append resolved (both kept); PR #19 now MERGEABLE/CLEAN, body updated."
- Why it makes future sessions smarter: Gives the resolution rule for the recurring sibling-merge-on-append-only-file case so a minion doesn't drop a decision-log entry or stall on the conflict.

---

### Lighter / single-sighting surface (for Bob's watch list)

- **Perkins lens-guards now named explicitly in briefings** — e.g. packet-plumber-v2-1.2-window-draw-pipe-perkins-r1 briefing: "Lens-guards: replay-equality over draw (action-log path), ODN-1 core engine-free, T2 golden real, W1 CI negative test ACTUALLY in CI (the #599-r2 gap)". The "the #599-r2 gap" cross-reference shows Perkins lens-guard conventions propagating across repos via briefing naming. (Reinforces C10; maybe fold.)
- **"W1 CI negative test ACTUALLY in CI"** — a Perkins finding recurred (v2-1.1 W1 "no CI negative test on the drift-rejection path — the #599-r2 gap, non-blocking" → v2-1.2 briefing bakes "W1 CI negative test ACTUALLY in CI" as a guard). Reinforces the "prove a guard bites + wire it into CI, not just locally" lesson. (Fold into C10 / the 2026-08-09 "prove a test BITES" entry.)
- **CONTINUOUS EXECUTION policy** — righttenantry-refcheck-rc3-5 briefing: "dispatched on the #599 merge without greenlight." A job can be auto-continuous-chained off a merge without an explicit Gru greenlight. Minor ops note (single sighting).
- **bmad-quirk recovery verified** — rc3-5: "committed from the worktree post-sync; the bmad-quirk recovery verified. Main-checkout safety copy intact (uncommitted, untouched)." Suggests a known bmad worktree/sync quirk with a named recovery + a main-checkout safety-copy practice. Single sighting — worth a glance by Bob to see if it's documented elsewhere.
- **Perkins lenses running IN-PROCESS (no herdr fan-out)** — packet-plumber-v2-1.1-walking-skeleton-perkins-r1 (2026-08-11T04:15:00Z): "Lenses ran in-process (no herdr fan-out — contract honored)." A Perkins execution mode. Single sighting; minor but worth noting the mode exists.
