# Sheep findings — journals (dream 2026-08-13)

## Candidate patterns

### C1 — 429 classes need triage: 1302 burst vs 1308 5-hour hard cap (different recoveries)
- Suggested target: AGENTS.md gotchas (Provider incidents)
- Evidence: silas-journal/2026-08-12 ~00:27Z: "NEW 429 class: **code 1308** ... NOT the short-window 1302 burst (one continue revives that); this is a HARD ACCOUNT-WIDE WALL — continue re-429s (waste)."
- Evidence: silas-journal/2026-08-12 ~00:3xZ: "pVT (pp-3.1) is WORKING again — auto-resumed after the 1308 cap (the fleet's other glm panes going idle backed off the rolling 5h-window usage"
- Evidence (the 1302 class it contrasts with): silas-journal/2026-08-11 ~21:13Z: "PATTERN NOW PROVEN 3x ... : ~9+ concurrent glm panes (8-pane Perkins round + 1-2 working minions) = guaranteed short-window account 429; one continue per pane recovers every time."
- Why it matters: continue-spamming a 1308 wall is pure waste; classify the code before recovering, and the 1308 window self-heals as panes idle.

### C2 — Staggering lens spawns wave-1(4)/wave-2(3) = zero 429s; lens panes need a send-keys-enter fallback
- Suggested target: docs/minion-field-notes.md (amend the G1 serialize-bursts entry)
- Evidence: silas-journal/2026-08-11 ~22:47Z: "The burst-mitigation VALIDATED: staggering wave-1(4)->wave-2(3) kept peak glm concurrency at 6 -> ZERO 429s (vs 3 bursts today at 9+)."
- Evidence: silas-journal/2026-08-11 ~22:47Z: "every lens pane needed a send-keys-enter fallback (pi's startup banner trapped the handover) — add to the headless-mode checklist."
- Why it matters: the burst-warning-in-every-Perkins-briefing practice works, and lens launches have a known handover trap needing the existing send-keys-enter fix.

### C3 — Dual-provider outage toolkit: always-live spares, hold regime, pi one-liner probe
- Suggested target: AGENTS.md gotchas (Provider incidents)
- Evidence: gru-journal/2026-08-12 (outage arc): "Verified deepseek + openrouter are authed + LIVE ... deepseek + openrouter are always-live spares — the fleet can ride out a glm/kimi outage on them."
- Evidence: silas-journal/2026-08-12 ~00:27Z: "BOTH providers down until then: kimi (billing-cycle 403) + glm (5h cap). Any NEW glm dispatch would block instantly -> HOLD dispatches."
- Evidence: silas-journal/2026-08-12 ~00:30Z: "Standing instructions for the hold: Watcher alerts -> minimum effort ... merges = standard light close-out (ledger/git, no model-heavy work) so the board stays clean."
- Evidence: gru-journal/2026-08-12 (learning): "pi auth.json providers use `{"type":"api_key","key":"sk-..."}` (field is `key`, not apiKey/api_key)" + the env-cleared `pi --model <p>/<m> -p --no-session -nt "Reply OK"` one-liner probe.
- Why it matters: a two-provider simultaneous outage is survivable if the spare-provider list and a hold regime are known in advance; the probe one-liner and auth.json field gotcha are concrete tools.

### C4 — Recurring connection-error waves on ALL tiers = check the user's network (firewall) before provider blame
- Suggested target: AGENTS.md gotchas (Provider incidents — new class)
- Evidence: silas-journal/2026-08-13 ~13:05Z: "PATTERN: deepseek API connection errors recur every ~30-40 min on BOTH v4-pro and v4-flash — a provider episode, not a model-tier issue; one continue per pane still clears each wave."
- Evidence: silas-journal/2026-08-13 ~13:20Z: "the connection-error waves were the OFFICE FIREWALL blocking deepseek API calls, not a provider episode ... LESSON (field-note worth): recurring 'Connection error / Retry failed after 3 attempts' on deepseek = CHECK NETWORK with the user before looping continues or blaming the provider — the office firewall class."
- Evidence: silas-journal/2026-08-13 ~12:30Z: "Both panes hit the provider connection-error class ('Error: Connection error. Retry failed after 3 attempts' ...) — mid-work, no artifacts lost ... ONE continue per pane (no loops)" (×2 waves)
- Why it matters: provider incidents have a 5th class — the user's local network; asking the user is faster than any pane-side action, and one-continue still clears each wave meanwhile.

### C5 — Manual dispatch masks sensor outages; the fallback sweep rule works and should fire proactively
- Suggested target: AGENTS.md gotchas (amend the existing pr_review entry)
- Evidence: silas-journal/2026-08-12 ~23:5xZ: "the Perkins sensor's gate is `job.pr_review === 1` on the ledger COLUMN ... columns defaulted 0 -> the sensor silently skipped every job (5 rows confirmed 0 ...). The last auto-fired round was #31 (12:19Z) ... Everything since was manual/held dispatch, which masked the outage."
- Evidence: silas-journal/2026-08-12 ~23:59Z: "at every minion completion/settle, sweep in-review pr_review=1 jobs; no round row at the current head sha + head stable -> dispatch manually, never wait on the sensor."
- Evidence: silas-journal/2026-08-13 ~13:50Z: "PROACTIVE r1 dispatch (sweep rule — head 1a3839c stable, no round row)" — the ratified fallback executed without a sensor tick.
- Why it matters: the incident is already gotcha'd, but the masking lesson ("manual dispatch hides a dead sensor") and the now-proven proactive-sweep execution are the durable add-ons.

### C6 — Never guess review URL anchor ids; fetch via gh api
- Suggested target: AGENTS.md gotchas (Ledger or review ops)
- Evidence: silas-journal/2026-08-11 ~19:43Z: "SLIP: my first done-note guessed the review URL anchor id (4908829057) — corrected via gh api ... LESSON: never construct a review URL by guessing the id — `gh api .../pulls/<n>/reviews --jq '.[-1].id'` first (the review-sensor alert gives it for rc3-5, but pane-done alerts don't)."
- Evidence: silas-journal/2026-08-11 ~21:20Z: "review id 4910842259 — fetched via gh api, the 1.4 lesson held: never guess the id" (×2 sightings)
- Why it matters: guessed ids write wrong URLs into the permanent ledger; the gh api one-liner is the fix.

### C7 — A fix whose regression test is vacuous/absent is still a blocker even when the mechanism is real
- Suggested target: docs/minion-field-notes.md (Perkins review section)
- Evidence: silas-journal/2026-08-13 ~08:48Z: "wrong_person_awaiting_sql_has_taken_over_backstop_test calls the dead SQL directly, never the POST route — VACUOUS"
- Evidence: silas-journal/2026-08-13 ~15:00Z: "B1 = the renumber-proof identity mechanism is REAL by inspection but the mandated demolish-and-renumber test is ABSENT (every resolve fixture preserves slot order; the r1 stale-slot failure mode unpinned)."
- Evidence: silas-journal/2026-08-13 ~09:10Z (what fixed it): "direct-SQL test replaced by wrong_person_taken_over_race_stands_down_test driving the POST route + pinning the SQL mechanism"
- Why it matters: fix-audits must verify the TEST pins the original failure mode and drives the real route — mechanism-inspection alone passes a broken fix.

### C8 — Round caps are doctrine, not law: user overrides work; cap bookkeeping is orchestrator-side
- Suggested target: playbook (Perkins round section)
- Evidence: gru-journal/2026-08-12 (r4 entry): "The cap is doctrine, not law — the user can always order another round."
- Evidence: silas-journal/2026-08-13 ~08:48Z: "CAP FLAG: next #606 sha = r5 — beyond the user-approved r4 override → escalate to Gru at push time (r5 vs human review)."
- Evidence: silas-journal/2026-08-13 ~09:10Z: "Minion believed cap-hit (no r5) — the override is Silas/Gru-side, as designed."
- Why it matters: override rounds (r4/r5) each used fix-audit + prior_findings + verify-don't-reopen and worked; minions don't know about overrides — Silas tracks the budget and escalates at exhaustion.

### C9 — Held-round hygiene: fresh sha at release, rebase dirty bases, re-verify at release
- Suggested target: AGENTS.md gotchas (serialize-hold entry, amend)
- Evidence: silas-journal/2026-08-12 ~09:2xZ: "#28 flagged DIRTY (base moved with #29) -> pi relaunched in pVT (parked-dead) + rebase relayed ... r2 held-row sha refreshed a980194->abe578b (release on #604 r1 close-out, re-verify at release)."
- Evidence: silas-journal/2026-08-12 ~11:4xZ: "NOTE in row: #30 APPROVED but UNMERGED — rebase onto post-#30 v2 if the merge lands mid-work"
- Evidence: silas-journal/2026-08-13 ~10:52Z: "release trigger = #36 merge/close-out + fresh sha" and ~13:35Z: "fresh fetch + rebase onto post-#36 origin/v2 ... at release" (×N sightings)
- Why it matters: hold-time shas go stale when bases merge mid-hold; every release needs a fresh fetch/verify, and parked minions need a relaunch + rebase relay when their base moved.

### C10 — Parallel/held gate = file-level overlap (goldens, shared modules); serialize doctrine is provider-scoped
- Suggested target: AGENTS.md gotchas (serialize-hold entry, amend)
- Evidence: silas-journal/2026-08-13 ~10:52Z: "packet-plumber-routing-bandwidth-cost — SERIALIZE-HELD (HOLD GATE = OVERLAP): **goldens/ OVERLAP** — 4.2 changed 19 golden files ... the new job's acceptance asserts 'existing goldens MUST NOT shift' which needs the post-4.2 baseline. **core/routing.odin = clean** (0 files in 4.2's diff)."
- Evidence: silas-journal/2026-08-13 ~13:35Z: "DISJOINTNESS VERIFIED -> PARALLEL: app/render partitioned by file ... both post-A v2"
- Evidence: silas-journal/2026-08-12 ~15:50Z: "the serialize doctrine SUSPENDED for Perkins rounds while on deepseek API (user override; glm-429/1308 cap history does not apply)."
- Evidence: gru-journal/2026-08-12 (pipeline entry): "SERIALIZE-HELD behind 3.5-node-placement (same repo, serialize/command overlap risk; release at 3.5 close-out)."
- Why it matters: hold-vs-parallel is now decided by file-level disjointness (goldens/shared modules), and the pane-capacity serialize rule only binds on capped providers — deepseek API allows full throttle.

### C11 — CI pending ≠ CI red: fresh r1 dispatch is OK on pending
- Suggested target: AGENTS.md gotchas (unstable-review-target entry, amend)
- Evidence: silas-journal/2026-08-12 ~09:2xZ: "CI pending (UNSTABLE=pending not red)."
- Evidence: silas-journal/2026-08-13 ~08:48Z: "PR #36 OPEN, head b94d54f stable, CI 4/5 pass + 1 pending (UNSTABLE-pending, not red — fresh-r1 dispatch OK)." (×2 sightings)
- Why it matters: the unstable-target hold gates on RED CI; treating pending as red needlessly blocks fresh rounds.

### C12 — `herdr worktree create` with no args makes a junk worktree in the CWD — never invoke bare
- Suggested target: AGENTS.md gotchas (dispatch & handover)
- Evidence: silas-journal/2026-08-13 ~10:52Z: "SLIP RECOVERED: my no-args `herdr worktree create` made a JUNK worktree in the ORCHESTRATOR ROOT (w52/worktree-quiet-harbor-aa25, branch worktree/quiet-harbor-aa25) — removed via git worktree remove + prune + branch -D ... LESSON: `herdr worktree create` takes --cwd/--branch/--base/--label; a no-args call defaults to the CWD repo (the code root!) — never invoke without args."
- Why it matters: a bare invocation writes a junk worktree into the live orchestrator root — the one tree that must never get stray branches.

### C13 — `herdr pane move` re-scopes pane ids; the ledger pane_id must be corrected post-move
- Suggested target: AGENTS.md gotchas (pane-id entry, amend)
- Evidence: silas-journal/2026-08-12 ~10:25Z: "pane w1T:pXM (tab t7P; id re-scoped w4T:p1->w1T:pXM on move — ledger corrected)"
- Evidence: silas-journal/2026-08-12 ~13:55Z: "id re-scoped w4W:p1 -> w1T:pZ8, ledger corrected" and ~14:45Z: "id re-scoped w4X:p1 -> w1T:pZD, ledger corrected" and ~18:50Z: "id re-scoped w4Y:p1 -> w1T:p0V, ledger corrected" (×4 sightings, one day)
- Why it matters: the pre-move id becomes a phantom the pane watcher would chase; re-read the id after every move and correct the ledger row.

### C14 — herdr JSON parse keys: `result.pane` (not split_result) and `move_result.created_tab`
- Suggested target: AGENTS.md gotchas (pane ops / herdr)
- Evidence: silas-journal/2026-08-12 ~08:2xZ: "NOTE: pane-split parse key is result.pane (not split_result) and move's tab key is move_result.created_tab — first split attempt left orphan pWH (closed)."
- Why it matters: wrong parse keys leave orphan panes behind; the correct key names are now known.

### C15 — Minions over-halt at internal "approval" checkpoints; standing orders pre-approve them — nudge, never relaunch
- Suggested target: AGENTS.md gotchas (watchers or minion behavior)
- Evidence: silas-journal/2026-08-12 ~06:58Z: "pVT (pp-3.1) done = story implementation COMPLETE but parked 'Not committed/pushed — awaiting approval' (an over-halt at an internal checkpoint — the standing orders pre-approve internal checkpoints ...). Relayed: checkpoint is PRE-APPROVED — commit, push, open the PR targeting v2, self-report in-review + set pr. pVT resumed working."
- Why it matters: a parked-done minion waiting on a pre-approved gate is silent dead time; the fix is one relayed nudge.

### C16 — Briefing/template model lines are load-bearing for mega-minion spawns; bare `pi` inherits defaultProvider
- Suggested target: playbook (briefing rules) + AGENTS.md gotchas
- Evidence: gru-journal/2026-08-12 (model-policy audit): "LATENT LEAK found + fixed: today's briefings carry pre-ruling model labels ... minions run deepseek correctly, but standing orders launch megas PER THE BRIEFING TEXT, so a mega spawned from those briefings would get glm-5.2 (or kimi if unset) ... GRU BRIEFING RULE from here: Model policy names deepseek/deepseek-v4-flash for minion AND mega-minions, explicitly, every time."
- Evidence: silas-journal/2026-08-12 ~08:36Z: "explicit mm-launch guidance (launch every lens pane with `pi --model deepseek/deepseek-v4-flash` — bare pi defaults to kimi via defaultProvider ...). The code-review skill pins NO model on mm launches — the guidance was load-bearing."
- Evidence: silas-journal/2026-08-13 ~16:12Z: "MODEL OVERRIDE (template's 'unset' is stale — pi default = retired kimi/k3): Bob + every sheep on deepseek/deepseek-v4-pro (explicit --model)."
- Why it matters: unset/`pi` launches resolve to defaultProvider, not the orchestrator's model — on provider failover every mm spawn must be forced, and every briefing must name the model twice (minion + megas).

### C17 — Dream template carries two known-stale lines (marker writer, model unset) — fix the template
- Suggested target: template fix task (playbook)
- Evidence: silas-journal/2026-08-11 ~16:07Z: "Marker written: 2026-08-11T16:06:54Z (Silas writes it per playbook step 5 + 08-07 practice — NOT Gru, despite the template's stale briefing-body line; watch item for a template fix)."
- Evidence: silas-journal/2026-08-13 ~16:12Z: "write marker (SILAS writes it per playbook step 5 — template briefing-body says Gru, known stale line)" (×2 sightings)
- Why it matters: the stale template line forces a judgment call at every dream close-out; plus the model line (C16) — both are one-line template edits.

### C18 — pr_review 0 "quick-fix" shortcut: CI/ops-tooling only, never canon-surface code
- Suggested target: playbook (briefing rules)
- Evidence: gru-journal/2026-08-12 (lesson entry): "LESSON (user prompt: 'no perkins review on them?'): #30 (3.5 node-placement) was briefed pr_review 0 as a 'quick-fix' — user rightfully expected the v2 line's standing bar ... Gru rule: the quick-fix shortcut applies to CI/ops-tooling fixes, NOT gameplay/canon-surface code (new command kinds, serialization, LOG_VERSION, payload contracts) — those keep pr_review 1."
- Why it matters: skipping Perkins on canon-surface code violates the standing bar and the user notices; scope the shortcut tightly.

### C19 — Follow-up intake: batch advisory findings into one issue per repo; sweep deferred-work docs at dispatch windows
- Suggested target: playbook (ops routines)
- Evidence: gru-journal/2026-08-12 (intake entry): "Follow-up intake filed (user ruling: one issue per repo): Packet-Plumber #34 (6 items ...) · RightTenantry #607 (5 items ...)."
- Evidence: gru-journal/2026-08-12 (sweep entry): "Deferred-work sweep (user directive — parse bmad deferred-work docs, run unblocked items in parallel; RT filter: refcheck only) ... (2) RC2.1 notification codec ... GATED on RC4.4, folded INTO the RC4.4 briefing ... Routine: sweep deferred docs at dispatch windows."
- Why it matters: advisory note floods become one reviewable issue per repo, and deferred work either runs parallel-safe or folds into a future briefing — both are now standard.

### C20 — Mid-flight canon rulings: amend the docs + relay to the in-flight minion so the PR carries the canon; prototype main branch is ground truth
- Suggested target: playbook (canon section) / docs/minion-field-notes.md
- Evidence: gru-journal/2026-08-12 (spatial lanes): "CANON: QoS lanes are SPATIAL (user ruling ...). Amended all three docs ... Committed 2e3acab on v2, relayed to the in-flight 3.3 minion (pZ8) so the lane visual ships in 3.3's PR."
- Evidence: gru-journal/2026-08-12 (addendum): "CANON addendum (user): no auto-assigned QoS + lane speed ... Committed 8ece056 on v2, relayed to in-flight 3.3 (pZ8)."
- Evidence: gru-journal/2026-08-12 (router miss): "the PROTOTYPE had Cmd_Place_Router + hardware tray (main branch = prototype-era code, placement intact); the v2 replan dropped it (only 3 commands left) and 5.1's passive 'routers co-spawn' contradicted the GDD loop."
- Why it matters: the healthy path for mid-flight reversals is amend-canon + relay (the PR ships the ruling), and when GDD/architecture/stories diverge the prototype's main branch is the ground truth to diff against.

### C21 — RTA-crew self-report gap recurs: pr field still NULL on in-review (#609)
- Suggested target: AGENTS.md gotchas (existing 2026-08-11 addendum — recurrence count)
- Evidence: silas-journal/2026-08-13 ~13:50Z: "SELF-REPORT GAP again: pr field NULL on in-review (the RTA-crew pattern) -> ledger pr set + verified (pr_review=1 column intact)."
- Why it matters: the crew-level fix hasn't propagated to the RTA minions yet; Silas's verify-and-set on every in-review transition remains the only reliable guard.

### C22 — A round pane stalled ~5h with no artifacts + session file gone = relaunch, not continue
- Suggested target: AGENTS.md gotchas (pane forensics, amend)
- Evidence: silas-journal/2026-08-13 ~08:15Z: "rc4-3-perkins-r4 ... 02:35Z launch stalled (~5h dead window — no artifacts; original session file gone); 07:55:48 relaunch re-did diff (07:56Z) → lenses c1 7/7 JSONs landed 08:09-08:12Z → second lens wave active ... Healthy."
- Why it matters: an overnight round pane can die silently and sit ~5h before anyone notices; the no-artifacts + missing-session-file signature says relaunch, and relaunching re-does the setup cleanly.

### C23 — bmad canonical-checkout quirk (F1) confirmed live: cmp-verified recovery executed cold from the documented procedure
- Suggested target: docs/minion-field-notes.md (reaffirm F1)
- Evidence: silas-journal/2026-08-11 ~18:25Z: "the bmad-quirk (dream F1 finding, live): the minion's edits mis-resolved to the main checkout, leaving 7 UNTRACKED files ... RECOVERY (dream F1 'cmp-verified' pattern, non-destructive): backed the 7 files to /tmp, pulled (succeeded ...), cmp'd backup vs merged. 5 IDENTICAL (strays matched); 2 DIFFER ... Merge correctly brought the fixed versions; backup discarded ... LESSON confirmed live: the dream F1 bmad-canonical-checkout quirk + its cmp-verified pull-blocker recovery are real + repeatable — handled it cold from the documented procedure. Worth a field-note reaffirmation."
- Why it matters: the merge-pull-blocker class (untracked strays vs committed versions) recurs across RT merges and the documented recovery works without supervision.
