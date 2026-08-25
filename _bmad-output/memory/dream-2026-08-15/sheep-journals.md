# Sheep findings — journals (dream 2026-08-15)

Sources: gru-journal/2026-08-14.md (fully undreamed); silas-journal/2026-08-13.md (undreamed = entries after 2026-08-13T16:26:29Z — everything from ~17:15Z onward, incl. Aug-14-dated entries misfiled in that file); silas-journal/2026-08-14.md; silas-journal/2026-08-15.md (both fully undreamed). AGENTS.md skimmed for dedup.

## Candidate patterns

### C1 — GLM-5.3 is the reasoning tier (user ruling 08-14) — AGENTS.md model-policy lines are now STALE
- Suggested target: AGENTS.md gotchas (model policy / provider incidents block)
- Evidence: gru-journal/2026-08-14.md (MODEL POLICY RULING, evening): "GLM 5.3 released today — 'back on top'. ALL thinking/deep-reasoning work returns to GLM: `zai-coding-cn/glm-5.3` replaces deepseek/deepseek-v4-pro for the reasoning tier (Gru, Perkins, Bob). Execution tier (flash: Silas, minions, mega-minions) unchanged."
- Evidence: silas-journal/2026-08-13.md (~13:55Z, Aug 14): "glm-5.3 = live reasoning tier; v4-pro = fallback" + silas-journal/2026-08-15.md (~16:35Z): Bob's dream itself ran on glm-5.3.
- Why it matters: SUPERSEDES the 2026-08-12-late block in AGENTS.md ("the reasoning tier is `deepseek/deepseek-v4-pro`") — routing v4-pro by default is now wrong; playbook Model policy already updated by Silas (committed), AGENTS.md is not.
- Supersedes: AGENTS.md "2026-08-12-late supersede (user ruling, playbook a96d36b): kimi k3 RETIRED entirely — the reasoning tier is deepseek/deepseek-v4-pro".

### C2 — Model-flip verification traps: hallucinated self-ID + wrong-endpoint curls; session jsonl = ground truth
- Suggested target: AGENTS.md gotchas (Model dispatch & correction ops)
- Evidence: gru-journal/2026-08-14.md (MODEL VERIFICATION CLOSED): "the 'glm-4.7' self-report was model hallucination; bare glm labels still misroute — full path mandatory... Gru's session jsonl confirms modelId glm-5.3 (the /model change took)... Silas' earlier 'balance 0' note was a wrong-endpoint curl, corrected."
- Evidence: silas-journal/2026-08-13.md (~13:55Z, Aug 14): "My 13:35Z 'ZAI balance = 0' conclusion was WRONG — the direct curls hit the wrong endpoint/path (api.z.ai + open.bigmodel.cn raw); pi's actual route succeeds."
- Why it matters: verify new models THROUGH pi (env-cleared probe + session jsonl provider/modelId), never trust the probe reply's self-named id or raw API curls — a false "provider down" ruling almost parked the new tier.

### C3 — No mid-round model flips
- Suggested target: AGENTS.md gotchas (Model dispatch & correction ops — one line)
- Evidence: gru-journal/2026-08-14.md: "Interim: in-flight 5.3-r1 Perkins stays v4-pro, sanctioned; no bare-glm strays." + silas-journal/2026-08-13.md (~13:55Z, Aug 14): "In-flight 5.3-r1 stays v4-pro (no mid-round flips)."
- Why it matters: model-policy flips apply to NEW dispatches only; a running round completes on its launched model (round consistency beats policy freshness).

### C4 — Round serialization is per-PROVIDER: deepseek parallel OK (user override 08-12), ZAI/glm serialize
- Suggested target: AGENTS.md gotchas (amend "Serialize concurrent Perkins BURSTS")
- Evidence: gru-journal/2026-08-14.md: "Two parallel Perkins rounds ran without contention on deepseek (user's parallel-rounds override from 08-12 holds)."
- Evidence: silas-journal/2026-08-14.md (~19:50Z): "Coexists with the in-flight 5.7-r1 glm-5.3 round (different providers — no burst conflict)." + (~14:45Z): "Perkins queue (serialize — one glm-5.3 fan-out at a time)."
- Evidence: silas-journal/2026-08-14.md (~20:45Z): "1302 = BURST class (not the 1308 5h wall) — ONE `continue` revived the pane... 5th glm-5.3 round today on ZAI... cumulative usage; expect possible recurrences, one continue each, no spam." (glm-5.3 extension of the codified 429 taxonomy)
- Why it matters: the serialize gate is per-provider quota, not absolute — deepseek carries the user's parallel-rounds override, ZAI does not; the existing gotcha reads as unconditional.

### C5 — Backticks in herdr pane-run payloads are eaten by bash command substitution
- Suggested target: AGENTS.md gotchas (dispatch/handover mechanics — new bullet)
- Evidence: silas-journal/2026-08-13.md (~17:15Z): "RELAY SLIP + RECOVERY: my relay's backticked code spans were eaten by bash command substitution (blank spans in the delivered message)... LESSON: NEVER put backticks inside a double-quoted herdr pane run argument — single-quote the whole payload or drop the backticks."
- Why it matters: relays carrying code spans silently arrive with blanks — the minion gets a corrupted fix recipe.

### C6 — Worktree bootstrap: `cp -r` cycles on the self-referencing `_bmad` symlink — `rsync --exclude='_bmad'` is the standard
- Suggested target: AGENTS.md gotchas (dispatch mechanics) or playbook dispatch section
- Evidence: silas-journal/2026-08-13.md (~18:40Z): "_bmad copied via rsync (cp -r CYCLES on the main checkout's self-referencing _bmad symlink — rsync --exclude='_bmad' fixed; note for future dispatches)"
- Evidence: silas-journal/2026-08-13.md (~19:20Z): "_bmad rsynced (the self-ref _bmad symlink cycle again — rsync --exclude is now the standard copy)" — ×2 sightings.
- Why it matters: recurring dispatch-bootstrap mechanics; cp -r fails/hangs every time on RT checkouts.

### C7 — GitHub Actions CI billing block = new incident class (account-level, ≠ red CI, ≠ infra-flake)
- Suggested target: AGENTS.md gotchas (Provider incidents — sibling class) + playbook CI doctrine
- Evidence: silas-journal/2026-08-13.md (~23:52Z): "CI failed on #40 (all 4 verify checks). Log: 'The job was not started because recent account payments have failed or your spending limit needs to be increased' — GITHUB ACTIONS BILLING block, runner never started... NOT infra-flake (rerun useless) + NOT a code failure. Escalated to Gru for the user."
- Evidence: silas-journal/2026-08-13.md (~00:15Z, Aug 14): "r2 dispatched WITHOUT the CI-green poll; briefing tells Perkins his local verification at the sha is the ground truth (the billing block ≠ code instability; the stable-target hold doctrine is about red code-CI, not account blocks)."
- Evidence (resolution): silas-journal/2026-08-14.md (~14:50Z): "CI billing FIXED... The 'CI billing-blocked' note is stale for future briefings" + gru-journal/2026-08-14.md: "CI-billing note retired from future briefings (confirmed fixed via #618 green checks)."
- Why it matters: new incident taxonomy — account blocks don't gate dispatch (local verification = ground truth), need user billing action, and their briefing caveat lines must be explicitly retired once fixed.

### C8 — Phantom ledger ROWS: minions can self-create WRONG-ID rows
- Suggested target: AGENTS.md gotchas (Ledger)
- Evidence: silas-journal/2026-08-13.md (~13:40Z, Aug 14): "PHANTOM ROW: `refcheck-followup-607` (NO righttenantry- prefix) — the minion SELF-CREATED its own ledger row... with the WRONG id (dropped the prefix), tracking the job in parallel with my canonical row; it kept the PR watcher alive post-merge... NEW SELF-REPORT VARIANT for the field notes: minions can create WRONG-ID rows — always check for a phantom when the watcher re-fires on a merged PR."
- Why it matters: extends the self-report-gap family (beyond pr-NULL): wrong-id rows keep watchers firing on dead work and break dedup lookups.

### C9 — Preserve no-PR deliverables orchestrator-side BEFORE the sweep (reports + test suites are durable assets)
- Suggested target: AGENTS.md gotchas (no-PR jobs) + playbook
- Evidence: silas-journal/2026-08-14.md (~21:15Z): "deliverables PRESERVED to orchestrator _bmad-output/implementation-artifacts/ (report + runlog + evidence) BEFORE the sweep (the worktree copies would have died; the local-test precedent lost its untracked artifacts to the sweep — not repeating that)."
- Evidence: silas-journal/2026-08-14.md (~23:40Z): "preserve the suite to _bmad-output/implementation-artifacts/bug-hunt-suites/reference_checks/ (fixes the twice-swept waste)" + silas-journal/2026-08-15.md (~09:05Z): "suite preserved... round 3 starts from a preserved suite, the twice-swept waste is fixed" — ×4 sightings incl. Gru's briefing line.
- Why it matters: closes a twice-paid cost — untracked no-PR artifacts (esp. regression suites) must land in the orchestrator store before worktree sweep.

### C10 — Base-sync no-op head move on an in-review PR → SKIP-ROW (don't burn round budget)
- Suggested target: docs/orchestration-playbook.md (round mechanics) — "round-budget skip policy"
- Evidence: silas-journal/2026-08-13.md (~09:10Z, Aug 14): "the push = 'Merge branch v2' — a base-sync... Verified the PR's own diff vs v2 is UNCHANGED... Pure no-op head -> the round-budget skip policy applies: skip-row written (full sha dedup, reason documented), r1 APPROVED stands."
- Why it matters: head moves via base-merge with an unchanged PR diff get a documented skip-row, not a fresh round — pairs with C11 (the non-no-op case).

### C11 — Same-file base-merge moves an APPROVED head → MERGE-HUNK AUDIT round flavor
- Suggested target: docs/orchestration-playbook.md (Perkins rounds) or AGENTS.md (Perkins section)
- Evidence: gru-journal/2026-08-14.md: "the 5.7 base-merge moved #49's head to bfdd7c5 (BOTH touched app/main.odin) → Silas dispatched r2 as a MERGE-HUNK AUDIT on glm-5.3 — right call: re-verifying the exact hunks after a same-file base-merge, not rubber-stamping."
- Evidence: silas-journal/2026-08-14.md (~23:25Z): "the delta is a BASE MERGE (v2 absorbed the 5.7 telemetry merge... both jobs touched app/main.odin). Briefing = merge-hunk audit (no dropped/overwritten hunk from either side; edge chip intact; determinism + 25/25 goldens hold)."
- Why it matters: a third head-move path (vs skip-row C10 and full re-review): same-file base-merges on APPROVED PRs get a scoped hunk audit, then moot-sweep on merge (clean instance of the codified moot doctrine).

### C12 — Respawn triggers + routing decisions recorded as LEDGER NOTES (survive session/context turnover)
- Suggested target: docs/orchestration-playbook.md (workflow convention)
- Evidence: gru-journal/2026-08-14.md: "RESPAWN TRIGGER recorded: #618 merged → fresh verification re-run over reference_checks scenarios." + silas-journal/2026-08-14.md (~17:00Z): "RESPAWN TRIGGER armed: #618 merge = the local-test verification re-run dispatch... Fire the fresh dispatch at #618's merge close-out."
- Evidence: gru-journal/2026-08-14.md: "#621 ROUTED (user 'do that' = Gru's rec): batched — rides the next RT batch (#617/#568 analytics pair, when ordered). No solo dispatch. Silas ledger-noting the routing so it survives context turnover." + silas-journal/2026-08-15.md (~09:05Z): "Routing survives turnover via the ledger note."
- Why it matters: durable triggers/routing live on ledger rows, not in agent context — sessions die (Silas restarted twice this window), the plan doesn't.

### C13 — User-ruled trade-offs carried in round briefings as do-not-re-litigate guards
- Suggested target: briefings template + playbook Perkins section
- Evidence: silas-journal/2026-08-14.md (~16:20Z): briefing guards list "degenerate-corner trade-off documented/user-flagged = do-not-re-litigate"; gru-journal/2026-08-14.md (618-r1): "10/12 verified (2 discards = out-of-scope re-litigation of the user-ruled 320x480 trade-off)."
- Why it matters: Perkins only discards re-litigation of user decisions when the briefing carries the ruling — surfaced user decisions must ride every round briefing for that PR.

### C14 — Serialize-holds need FALLBACK TIMERS (prevent queue deadlock)
- Suggested target: AGENTS.md gotchas (serialize-hold addendum)
- Evidence: silas-journal/2026-08-14.md (~21:15Z): "5.3-pause-ux-r1 hold EXTENDED: 5.7-r3 (imminent one-liner push) takes the next glm slot; 5.3-pause-ux-r1 releases at r3 close-out (fallback: no 5.7 push within 45 min of 21:05Z -> release it, hold r3 behind)."
- Why it matters: a hold keyed on an expected-soon event with no deadline can deadlock the whole queue when the event slips.

### C15 — FULL THROTTLE chain doctrine in heavy use (pending U2 user-ack; not yet codified)
- Suggested target: docs/orchestration-playbook.md (escalated as U2 at dream-08-13 close-out)
- Evidence: silas-journal/2026-08-13.md (~23:15Z, Aug 14): "THREE-WAY FAN-OUT (disjointness pre-verified: pin = core TEST files only... C = new core SRC module... B = app/render... -> all three parallel, no hold)"; (~01:45Z, Aug 14): "DISJOINTNESS CHECK per doctrine: inspected 4.3's live worktree — its edits are... app/main.odin NOT yet touched... -> DISPATCHED with ready-first merge ordering + coordination note"; (~08:25Z, Aug 14): "Gru chain ruling: all same-files sequential (app/main.odin + tray + render), each releases on the prior PR's merge... Chain: #44 merge -> 5.6 -> 5.3 -> 5.7 -> 5.8."
- Evidence: silas-journal/2026-08-15.md (~00:55Z): "QUEUE ARMED (Gru queue note): 5.1 merge -> release 5.2... -> 5.2 merge -> release 5.4... 5.2/5.4 briefings NOT yet authored — request at release." (briefing-at-release convention)
- Crash-resilience bonus: silas-journal/2026-08-14.md (~14:05Z): "5.3-r1 serialize-held (dispatch never completed pre-restart; no pane/briefing/session; worktree @ 9ae8612 staged)" — pre-created held rows survive Silas session death and complete at release.
- Why it matters: the standing execution pattern for multi-job lines (disjointness gate, same-files sequencing, release-on-merge chains, briefing-at-release) — used ~10× this window, still uncodified pending user ack.

### C16 — pr_review=0 quick-fix scope (pending U3 user-ack): user-supplied verbatim strings → human reviewer, no Perkins round
- Suggested target: docs/orchestration-playbook.md (escalated as U3)
- Evidence: gru-journal/2026-08-14.md: "pr_review=0 (user-supplied verbatim strings, no logic — the CI/ops class of lightweight review; user filed the spec themselves)" + silas-journal/2026-08-14.md (~20:55Z): "pr_review=0 -> human review; no Perkins round."
- Why it matters: doctrine in active use (ctr-619, bughunt2, surge-explainer all pr_review=0/no-PR) — needs codification so the lightweight class doesn't get re-derived per job.

### C17 — Cap-override rounds + VERIFY-DON'T-REOPEN mandate (pending U1 user-ack) — used twice more
- Suggested target: docs/orchestration-playbook.md (escalated as U1)
- Evidence: silas-journal/2026-08-13.md (~17:35Z): "#36 r4 DISPATCHED (USER-APPROVED CAP OVERRIDE, verify-don't-reopen @ f9184fa)" + (~19:35Z): "#36 saga: r1 CR, r2 CR, r3 CR, r4 APPROVED (2 cap overrides, user-driven)."
- Why it matters: beyond-cap rounds via explicit user override + verify-don't-reopen briefing guards are now a repeated, user-sanctioned pattern (rc4-3 r4/r5, #36 r4) — still pending codification.

### C18 — Vision models misjudge pixel coordinates → programmatic pixel-scan verification
- Suggested target: docs/minion-field-notes.md
- Evidence: silas-journal/2026-08-14.md (~20:45Z): "edge chip (120x38 tray-styled) in the top HUD band @ win_w/2+240 (collision-verified via rlsw-shadow replica + PIL pixel-scan — vision models misjudge coordinates)."
- Why it matters: layout/collision claims need pixel scans, not vision-model eyeballing — generalizes beyond this PR.

### C19 — No-PR completion fell through the watchers AGAIN (recurrence ×2 of a codified gotcha — verify the failure mode)
- Suggested target: recurrence note on existing AGENTS.md gotcha (no-PR jobs, 2026-08-07)
- Evidence: silas-journal/2026-08-15.md (~09:05Z): "bughunt2 DONE (self-set done 00:22Z; its no-PR completion fell through the watchers — pane went idle AFTER the row flipped done, so no alert; caught now via the Gru ruling relay)" — 8.5h gap.
- Why it matters: already codified, BUT the journal does not record the mandated compliance check (session jsonl `cli:notification:show` results) — Bob should flag: which failure mode was it this time (notification not fired vs. not seen)? Recovery came via user/Gru relay, not the intended signal.

### C20 — Interactive-job pane hygiene: mega-minion tabs get de-congested on user ask; pane ids STABLE on plain tab moves
- Suggested target: docs/orchestration-playbook.md (minor, pane hygiene)
- Evidence: silas-journal/2026-08-13.md (~09:30Z, Aug 14): "the local-test tab tAX held 12 panes... — unreadable. Moved the 10 mega-minions 5+5 [into two helper tabs]... Pane ids STABLE on move (no ledger correction needed)."
- Why it matters: interactive jobs spawn helper fleets; split them into labeled helper tabs before readability dies — and note plain tab-moves (unlike workspace moves) keep pane ids.

## Already codified (recurrences only — no re-proposal)

- **pr-field NULL gap** (AGENTS.md, persistent): recurred on 4.3 (gru 08-14: "pr-field NULL gap recurred on 4.3's self-report — Silas caught + fixed") and #610 (silas 08-13 ~19:05Z: "SELF-REPORT GAP again"). POSITIVE trend: silas 08-14 ~14:45Z: "Self-set pr + in-review (the briefing's ledger-pr instruction worked — crew compliance improving)" — 613-615/5.5/5.6/C all self-set correctly. Verify-and-set guard still required.
- **Perkins self-close norm + verdict-recovery note**: silas 08-14 ~22:05Z "(6th today — the self-close pattern is now fully the norm; verdict-recovery notes each time)"; silas 08-15 ~00:45Z "(7th)", ~02:05Z "(8th)". Working as codified.
- **Office-firewall class**: silas 08-13 ~18:00Z + ~22:40Z waves ("i was back on the office network"), one continue per pane each time — codified 08-13, clean recurrences.
- **429 taxonomy (1302 burst)**: silas 08-14 ~20:45Z glm-5.3 burst — codified class, new provider instance (see C4).
- **Pane/tab-id hand-typing slips**: silas 08-15 ~00:55Z "(tC5->tC4... the hand-typed-id slip class)" + ~14:40Z "(p1P0→p1P8 — hand-typed in the chained add... FIX: capture pane/tab to vars and use them in the add, never re-type)" — ×8 lifetime; habit still losing to the chained-command reflex.
- **pane-run buffer + send-keys recovery**: silas 08-13 ~01:55Z (Aug 14): "first pane-run queued unsent (buffer), submitted via send-keys enter, verified in session (the gotcha's recovery, again)".
- **Template/briefing caveat lines rot**: silas 08-15 ~16:35Z "Template model line refreshed (v4-pro -> glm-5.3... template lines rot otherwise)"; CI-billing caveat retired (C7) — codified 08-13, two more instances.
- **Sweep lens tabs at close-out**: silas 08-14 ~14:05Z field observation — 612 close-out left 9 panes ("the round's 'pane closed' event covered only the round pane"); codified sweep list, one more recurrence.
- **Moot-on-merge (pre-verdict merge of APPROVED PR)**: silas 08-14 ~23:30Z r2 moot-swept on #49 — clean codified instance.
- **Mid-flight reversal → amend+relay (not kill)**: gru 08-14 "Explainer REFRAMED (user mid-flight)... Correction relayed via Silas → minion p1NW" — the codified 08-13 healthy path, worked without a kill.
- **Duplicate relay echo, note-only**: gru 08-14 "Duplicate [SILAS] relay echo arrived in Gru's pane (same 4.3-shipped message twice) — note-only, no action" — known echo class.
