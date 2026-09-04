# sheep-journals — dream-2026-08-27

Sources: gru-journal 2026-08-24 (tail), 2026-08-25, 2026-08-25-pi-restoration-
handover; silas-journal 2026-08-24 (tail), 2026-08-25, 2026-08-26, 2026-08-27.
Window: DSH interlude tail → pi/herdr restoration → PP viscomm trilogy (#99/#100/
#102) → spine ratification (#103) → egress migration (#104) → Sally look sessions.

## C1 — The fold pattern leaves redundant originals: expect a base-sync collision at the NEXT merge after any fold
- Evidence: silas-journal 2026-08-26 ~19:10Z — "#102 MERGED close-out (+ collision forensics)": ff blocked by (a) modified deferred-work.md, (b) 9 untracked originals colliding with the fold's now-tracked paths; resolution stash + aside + ff + verify; all 9 byte-identical redundant; the stash-pop conflicted and the stashed copy proved STALE (missing the fix-minion's 6 lines) → took tracked HEAD.
- Evidence: silas-journal 2026-08-26 ~20:05Z — #103 merge: "08-26 arch dir collision = aside-verify-drop again, byte-identical, clean".
- Note: NEW close-out law. Folding untracked artifacts into a PR leaves duplicate originals in the main checkout → the next `pull --ff-only` collides. Verify aside copies byte-identical before dropping; never assume stash-newer-is-superset (wrong once same day); diff-check --theirs resolutions.

## C2 — Minion cleanup contract must EXCLUDE its own pane (pane-vanish mid-badge-out)
- Evidence: silas-journal 2026-08-26 ~20:50Z — "migration pane vanished mid-badge-out": w85:p1S gone (tab too); session forensics showed agent at badge-out ("close the mega-minion panes") then died — "almost certainly SELF-SWEPT its own pane in the cleanup sweep". Work intact: all 6 commits on branch, worktree clean. Recovery = fresh pane in the SAME worktree, completion-only handover (push/PR-per-brief/ledger/notes/notification + explicit never-close-your-own-pane).
- Note: NEW briefing clause. Any minion whose swarm-sweep instruction says "close the mega-minion panes" needs the own-pane exclusion stated. Recovery shape: branch survives; completion-only handover to a fresh pane; cost = one dispatch.

## C3 — gh pr diff 20k-line API cap → local canonical diff + MEGA-DIFF PROTOCOL
- Evidence: silas-journal 2026-08-24 ~16:25Z — "BIG DIFF 84,831L (gh pr diff API 20k-capped -> git diff origin/v2...refs/pr-96 saved; chunking mandatory in the briefing)".
- Evidence: silas-journal 2026-08-26 ~20:55Z — "gh pr diff 406'd (>20000-line API cap — FIRST occurrence as a 406) → canonical diff generated locally (git diff merge-base 7ad48f9..1e9c783 = 54356 lines, substitution disclosed)"; protocol: full lens waves on CODE chunks + mechanical bulk-verification on goldens/docs (T1 re-bless inventory + D6 replay); r2 then runs fix-delta-weighted (r1 verified the 51k bulk → spot-check only).
- Evidence: silas-journal 2026-08-26 ~21:20Z — "The mega-diff protocol held: 14 lens runs 0 failed, 51k bulk lines mechanically verified, canonical-diff substitution disclosed".
- Note: Perkins ops convention for >20k-line PRs: generate the diff locally off merge-base, disclose the substitution, split verification into lens-waves (code) vs mechanical bulk (goldens/docs), and let the fix round spot-check the already-verified bulk.

## C4 — User-authored PRs are Perkins-sensor-blind: register a row (pr_review=1) and dispatch
- Evidence: gru-journal 2026-08-25 ~01:0xZ — "#98 gap caught: user PR with no Perkins coverage... user-authored branches carry no job row → no pr_review=1 → sensor blind. Handed Silas full package: register row (pr_review=1) + dispatch Perkins r1".
- Evidence: silas-journal 2026-08-24 ~20:40Z — user PR #97 quirk: no minion row, no session dir, user self-reviewed COMMENTED at 20:32Z; classified USER-INITIATED PR; round spec = PR body, "user's informal review = NOT the verdict".
- Note: NEW trigger for the 08-12 pr_review-blindness class. On catching a user-authored PR: Silas registers the row with pr_review=1 and dispatches Perkins; spec = PR body; the user's own COMMENTED review is never the verdict.

## C5 — Merged-over-CHANGES_REQUESTED lifecycle: live-on-base blockers → user fix-forward → pin PR closes the loop
- Evidence: gru-journal 2026-08-24 ~23:5xZ — user merged own PR #97 over r1 CHANGES_REQUESTED (posted 21:03Z, 2B/5W/4N) — "sole-merger call, their PR"; B1/B2 live-on-base blockers awaiting user call.
- Evidence: gru-journal 2026-08-25 ~01:0xZ → 08:58Z — "#97 B1 closed end-to-end: merged-over-CHANGES_REQUESTED → live-on-base blocker → user fix-forward (own branch packet-plumber-v2-pr97-b1-wiring-pin → PR #98) → mutation-proven pin → merged" (r1 APPROVED 0B/2W/3N, core gate mutation-PROVEN: all 3 routing calls isolated-fail, no 4th site).
- Note: NEW lifecycle pattern. When the user merges their own PR over a CR verdict, blockers become fix-forward follow-ups; the user's fix branch becomes a NEW user PR (→ C4 applies: register + review). One-day full arc.

## C6 — DSH interlude verdict: mid-turn interruptibility + never-blocked user lane is the load-bearing orchestrator property
- Evidence: pi-restoration-handover journal — "DSH's Silas lane cannot accept new tasks mid-turn, and its workflow fan-out blocks Gru's turn — the user cannot converse while ops run. Reverted to pi/herdr... one background ops agent cannot be interrupted with new work mid-turn; foreground fan-out starves the user lane. pi/herdr's persistent interleavable sessions remain the fit."
- Note: Architecture-level lesson for the store: the fit criterion for any orchestrator substrate is (a) accept new tasks mid-turn, (b) user lane never starved during ops fan-out. The DSH-day lens doctrine amendments (7-lens full set, skill-file-first, blind = diff-ONLY) are real and carried over.

## C7 — Restoration/move checklist: empty-shell DB, canonical symlink set, symlinked homes split state
- Evidence: pi-restoration-handover — "Ledger: the real 490-row DB moved back... the one at that path was an empty shell, no jobs table — backed up as orchestrator.db.empty-shell.bak".
- Evidence: pi-restoration-handover (Gru ~17:0xZ) — "docs symlink was MISSING from the restoration set (bin/.agents/.pi were symlinked, docs wasn't) — PLAYBOOK constant in gru.ts/silas.ts AND AGENTS.md references dangling".
- Evidence: pi-restoration-handover — "Silas's journal re-homed (it had been landing in the clone via symlink resolution — state was splitting)"; fixed by the layout inversion: ~/code IS the checkout, .git moved to root, nested clone deleted (sync 5b5de85); watchman penalty-box (program path vanished) kickstarted back.
- Note: NEW ops checklist for any orchestrator restore/move: verify the ledger DB by schema (jobs table present), not path existence; canonical symlink set = bin/.agents/.pi/docs (one canonical copy each); symlinked homes split live state across clones — prefer one real checkout.

## C8 — herdr status/wait reads are unreliable around transitions — pane forensics is ground truth (both directions now seen)
- Evidence: pi-restoration-handover — "herdr agent-wait false-negatived BOTH boots (registration race) — pane-forensics verification (process + session file) is the reliable check, not the wait".
- Evidence: silas-journal 2026-08-25 ~01:30Z — "herdr reported agent_status=done on w85:p1 while the pi process was alive+idle... Classified per the 08-17 liveness doctrine (process + session = up; NO relaunch); the due APPROVED escalation doubled as the functional probe".
- Note: Extends the 08-19 agent-wait registration race: false-not-idle at boot AND false-done while alive-idle are both live. Check process + session file before any relaunch/continue; a pending escalation delivery doubles as the functional probe.

## C9 — Tab-label resolution must be case-insensitive with ambiguity guard (night-watchman false alarm)
- Evidence: pi-restoration-handover ~17:1xZ — "'Gru tab MISSING' notification every 30 min since 16:10Z. Root cause: config expects tab label `Gru` (capital), live tab is `gru` (lowercase, from the user relaunch) — resolve_tab is case-sensitive jq exact match → permanent miss. Fix (e5838c1): exact match first, unique case-insensitive match second, ambiguity (2+ variant tabs) still warns (never guesses)."
- Note: NEW tooling trap. Case-sensitive label matching turns a relabel/relaunch case flip into a permanent miss. Any tab/pane-label resolution: exact → unique-case-insensitive → ambiguity-warn; verify with the tool's --self-test.

## C10 — Stray out-of-band typed input opens interactive UIs and kills long polls (external-input class)
- Evidence: silas-journal 2026-08-26 ~13:00Z — "a stray '/dedi' (out-of-band typed input, likely a misfired keystroke) opened pi's interactive skill navigator in w85:p1B mid-lavish-poll, aborting the 3500s poll... 'q'/escape insufficient (navigator ate a 'continue' too) — C-c cleared it; then one continue resumed the turn. Noted on row: external-input class, not provider."
- Note: NEW pane-incident class. Classification key: session shows an interactive navigator/skill UI opened by typed input (not a provider error). Recovery: C-c (not q/escape), then one continue; re-arm any aborted polls.

## C11 — Pre-add the Perkins round row with parent=/sha= dedup keywords BEFORE handover
- Evidence: silas-journal 2026-08-25 ~17:05Z — "Perkins-sensor dedup miss fixed: the 'round 2 pending' alert was stale — the r1 round row note lacked parent=/sha= keywords. Keywords added via ledger note."
- Evidence: silas-journal 2026-08-25 ~21:35Z — "Round row PRE-ADDED by me this time (dispatched + parent=/sha= in note) so sensor dedup holds even before the agent's working self-report"; same on 08-26 (~00:35Z, ~21:40Z "Round row pre-added with dedup keys").
- Note: Refinement of the durable-dedup doctrine: the round row with parent=/sha= keywords must exist at DISPATCH time (Silas pre-adds), not at the agent's self-report — kills the stale round-pending echo class.

## C12 — `ledger add` chokes on sha= keys; round agents self-create the healthy row
- Evidence: silas-journal 2026-08-25 ~17:30Z — "ledger add chokes on sha= (not a column; k=v parser scans the note too) — the round agent SELF-CREATED the row correctly at working with parent=/sha= in its own note (the healthy self-create flavor); I filled pane/tab/briefing via sqlite."
- Note: NEW ledger gotcha. sha= is not an add-key; write parent=/sha= via `ledger note` after add, or let the round agent self-create then fill fields via sqlite (verify-and-fill as ever).

## C13 — pr_review column silently 0 despite briefing=1 — fix the SIBLING rows too, not just the firing one
- Evidence: silas-journal 2026-08-25 ~21:30Z — "CATCH: pr_review COLUMN was 0 though the briefing + Gru's dispatch said 1 (the 08-12 sensor-blindness class) — SQL-fixed on gauge-telegraph AND crisis-duck (same latent gap) within minutes; shape-vocab stays 0 legitimately (era-gated, re-set at release)."
- Note: 08-12 gotcha recurrence with a new wrinkle: paneless sibling rows wired in the same batch share the latent gap — sweep the batch when one fires. Era-gated design rows legitimately hold 0 until release.

## C14 — Backtick-eaten relay via double-quoted herdr payload — 3rd known sighting
- Evidence: silas-journal 2026-08-25 ~16:15Z — "Backtick-eaten relay slip hit AGAIN (double-quoted herdr payload) — correction resent single-quoted."
- Note: Reinforcement of the 08-13 class (1 direct + 1 sibling then). The documented fix (single-quote the whole payload / drop backticks) still gets missed in live relays — candidates for a stronger habit or a herdr wrapper that refuses double-quoted payloads containing backticks.

## C15 — Trigger graph ran a whole multi-job belt hands-off — conventions that made it work
- Evidence: gru-journal pi-restoration ~23:40Z — "Crisis-duck AUTO-RELEASED at close-out exactly as wired... The first fully hands-off release through the graph since the pi restoration — brief staged, ruling relayed, graph did the rest."
- Evidence: silas-journal 2026-08-27 ~09:40Z — "#104 merged → Trigger fired: look-zoom-language released... The full chain delivered: user pivot -> spine (1 day) -> migration (1 day) -> look heist (now)."
- Evidence: silas-journal 2026-08-26 ~19:15Z — "The release authorization crossed my close-out escalation mid-flight — verified single dispatch (one row/pane/worktree)"; also "briefing column backfilled after the re-check caught it empty" on the paneless look row.
- Note: At-scale proof of the 08-18/23 doctrine (belt = paneless blocked_by rows + named release triggers + fresh-head resolution). Working conventions: Gru stages the briefing BEFORE release; release = close-out + probe + fresh head; when a release crosses an in-flight escalation mid-flight, verify single dispatch (one row/pane/worktree); paneless held rows need the briefing column backfill check too.

## C16 — Recorded revisit triggers pay off verbatim days later
- Evidence: gru-journal pi-restoration ~02:xx — "Link vocabulary pivot... this re-opens the 08-23 egress-qos steelman WITHDRAWAL — recorded trigger was 're-open re-framed at make QoS changes feelable (no queue migration)'. Today = exactly that re-frame: RENDER-side, sim untouched."
- Evidence: silas-journal 2026-08-26 ~07:30Z — "08-23 revisit trigger firing; SIM UNTOUCHED boundary" wired into the dispatch.
- Note: When withdrawing/deferring a design direction, record the exact re-open condition on the row/issue — when the trigger fires days later, archaeology is instant and scope boundaries (sim untouched) carry forward.

## C17 — Architecture briefings on load-bearing calls must name Coaching-vs-Fast explicitly
- Evidence: gru-journal pi-restoration ~12:3xZ — "Process note: the minion ran the Fast path (draft-then-ratify) rather than coaching the user through the forks live — the deviation lived in Gru's briefing; the interactive gap was closed by ruling the four rows directly in chat. Future architecture briefings on load-bearing calls: name the Coaching-vs-Fast choice explicitly per the skill doctrine."
- Note: NEW briefing convention: the interactive-vs-draft mode is a briefing decision, not minion initiative; name it per call.

## C18 — Loaded-but-unwired config findings become NAMED decisions/stories, never silent drift
- Evidence: silas-journal 2026-08-26 ~12:45Z — "Best catch: reality-check lens found bandwidth_demand loaded-but-unwired → D-2 named BALANCE decision (streaming 8 vs 16 ticks), not silent."
- Evidence: gru-journal pi-restoration ~12:4xZ — "D-2... loaded-but-unwired: NAMED STORY on the migration heist per ratified D3 (streaming 8->16 ticks disclosure; T1 re-bless) — never silent drift"; shipped as S3 in #104 with disclosure.
- Note: Pattern for dead-config findings (review or architecture): name it a decision, route it as a story on the owning row — it eventually ships as real wiring with disclosure, not a silent fix or a silent drop.

## C19 — glm-only regime (k3 403 + flash 402): 1308 frees early, connection waves kill round mains mid-lens-wait, lens JSONs are the durable progress signal
- Evidence: silas-journal 2026-08-25 ~17:05Z — "flash 402 account-wall (top-up pending), k3 still 403 — glm-5.3 carries reasoning AND ops; episodic 1302s = one continue per pane, hold nothing unless probe fails."
- Evidence: silas-journal 2026-08-26 ~07:40Z — "Cluster stop 07:35 (2 panes dead on 1308 five-hour cap, stated reset 19:22:01)... The rolling window freed within ~1 min — double probe OK → one continue each revived both... stated reset times lie, probe-only decides; no continue-spam."
- Evidence: silas-journal 2026-08-26 ~16:00Z — "connection-error wave killed the [r2] main after a 3600s lens wait (c1 6/7 durable, edge-c1 missing; c2 panes vanished unread). Probe chatty-OK false-read both times (provider demonstrably up — it answered); one continue → main working, re-driving c2."
- Note: Provider-regime addenda: (a) a 1308 rolling window can free ~1 min after the cap — never wait on the stated reset; (b) a connection wave can kill a Perkins MAIN mid-lens-wait — one continue revives it and it re-drives the vanished chunk panes; chunk JSONs on disk are the durable progress signal; (c) chatty-OK false-reads persist — "it answered" beats the strict match.

## C20 — The cheap transient classes now self-recover: classify BEFORE spending a continue
- Evidence: silas-journal 2026-08-26 ~14:15Z — "triple alert, all transients: cache-miss-after-idle (74m, 164k re-billed — no-action class), connection/timeout wave (self-recovered via auto-retry), settle echo. All note-only, zero continues spent (both panes revived themselves — the cheap classes)."
- Note: Extends the 08-09 5th class: pi's auto-retry now covers minion connection waves too — a continue spent on a self-recovering pane is waste. Classify by transcript first.

## C21 — PR-readiness gates must use per-reviewer LATEST verdict (check-pr-ready fix, PR #15)
- Evidence: silas-journal 2026-08-25 ~20:35Z — "check-pr-ready BUG: gate read ANY CHANGES_REQUESTED as outstanding → superseded r1 CR blocked the r2-APPROVED PR #99 (and every future loop-closed PR); mirror bug: stale APPROVED could mask a newer CR. Fixed per-reviewer latest-verdict semantics (submittedAt sort; COMMENTED/PENDING carry no stance). Live-verified NOT READY → READY rc=0 + negative leg."
- Note: NEW ops-tooling law: any gate over review state evaluates per-reviewer latest verdict, not any-verdict — loop-closed PRs (CR → fixes → APPROVED) are the common trigger. Built in a root worktree (never move the live tree's HEAD).

## C22 — Lens findings read during the round's OWN mutation window are timing artifacts
- Evidence: silas-journal 2026-08-26 ~21:20Z — "One lens finding rejected as a timing artifact (read during the round's OWN mutation window — disclosed)."
- Note: NEW Perkins verification nuance: when the round main runs mutation legs while lenses read, a lens may see mutated code; such findings are timing artifacts — reject with disclosure, not verified findings.

## C23 — Billing-block CI signature recurred 4× in one day — note-only discipline held
- Evidence: silas-journal 2026-08-26 ~12:50Z (#103, "failed in 3 SECONDS, zero logs"), ~14:35Z ("3rd occurrence today"), ~20:55Z (#104, "5s failure, zero logs — billing signature again, note-only").
- Note: Reinforcement of the standing 08-16/08-19 rulings at high volume: 3-6s run + zero logs = billing signature; note-only on the row, no rerun, no relay, local suite = ground truth. Local-suite ground truth carried every merge this window (#102/#103/#104 all merged billing-blocked).

## C24 — palcheck in headless panes requires the harness.sh shadow path
- Evidence: silas-journal 2026-08-27 ~09:35Z — "invocation note documented (palcheck requires the harness.sh shadow path in headless panes)".
- Note: Small PP-specific ops fact for Perkins/headless briefings: palcheck fails without the harness.sh shadow path — carry the invocation note in briefings.

## C25 — Design minions: interactive halt ≠ stall; pause-and-spec captures session value durably
- Evidence: silas-journal 2026-08-26 ~13:05Z — "INTERACTIVE HALT, not a settle: post-amendment Sally presented fork 1/5... Awaiting user IN-PANE (direct-to-pane legit per doctrine). Escalated the waiting-on-user FYI to Gru (both gates wait on the user)."
- Evidence: gru-journal pi-restoration (evening 08-26) — "Design session concluded (pause-and-spec): LOOK-SPEC.md = 6 design locks...; open forks parked for a future Sally session"; LOOK-SPEC then rode the released look heist as spec input ("Sally's LOOK-SPEC as law").
- Note: Sally/interactive minions halt awaiting user answers in-pane — classify waiting-on-user, escalate the FYI, never continue-nudge. The pause-and-spec output (design-locks doc + parked forks) turns a user-gated session into durable spec for the next heist.

## C26 — A SECOND user complaint on the same visual axis = recurring look-imbalance class; read-only evidence job first
- Evidence: gru-journal pi-restoration ~01:12 — "User: 'barely see the nodes even when zoomed in'... SECOND complaint on this axis (08-23 buildings → grew; now nodes/pucks)... prime suspect the 9bf9797 puck shrink + pipe saturation dominance."
- Evidence: silas-journal 2026-08-26 ~00:20Z — "Dispatched IN-REPO on the clean main checkout (no branch/worktree — the parallel-safe shape vs in-flight crisis-duck)... Row pr_review=0 (no code) + durable notes: fix-job routing (lavish gate → fix heist blocked_by crisis-duck)".
- Note: Repeat play-feedback on one axis is systemic, not a one-off: dispatch a READ-ONLY evidence job (captures at zoom tiers + KYLE pixel measurements + git archaeology + lavish proposals) before any fix heist; read-only = parallel-safe in-repo on the clean main checkout, no branch/worktree; route the follow-up heist on the row.

## C27 — Env-gated resources hide limit violations from staging CI — audit all literals × both envs + CI guard
- Evidence: gru-journal 2026-08-24 — "RT prod deploy blocked — terraform SA id lengths... account_id regex 30 cap. Broken: prod-only resources (count=prod?1:0), staging never saw them. Latent: staging 31."
- Evidence: silas-journal 2026-08-24 ~17:20Z — "Full audit of every account_id literal × both envs (24 evaluated ids)... renames ZERO-churn; guard: check_service_account_ids.py (evaluates production+staging, asserts <=30) wired into CI terraform-validate + make tf-guard".
- Note: prod-only (count-gated) resources escape staging validation entirely; latent staging values sit at the legal bound. Fix = audit ALL literals across envs at real per-env lengths + a CI guard that evaluates both environments.

## C28 — protocol_mismatch on herdr calls = transient upgrade-pending noise; a server restart renumbers the WORKSPACE prefix but pane ids survive
- Evidence: silas-journal 2026-08-24 ~20:40Z — "herdr `pane read` threw a protocol_mismatch (client 20 vs server 19) once on Gru's pane then worked — transient, flagged for the next server restart".
- Evidence: silas-journal 2026-08-25 ~00:59Z — "Server restart detected: workspace moved w1T→w85 (the flagged protocol_mismatch transient from 08-24; pane/session ids survived)".
- Note: A one-shot protocol_mismatch is client/server version skew noise (retry works), and it predicts a server restart that will renumber the workspace prefix — pane ids stay valid; don't chase phantom panes, but expect the ledger's pane ids to keep working under the new prefix.

## Cleanup candidates NOTICED (for Bob's dedupe pass — not verified against live store)

- **Round-row id typo lineage**: the tie-deconflect lineage has inconsistent round-row ids — r1 round row correct-spelled (deconflect... actually `deconflict`), r2 round row carries the briefing's typo (`deconflect`, self-created); r2 artifacts dir initially created under the typo dir then moved to canonical. Journal itself flags "dream-pass cleanup candidate".
- **r1 note understated its lens set**: "r1 artifacts live under CORRECT-spelling dir (7 lens JSONs — full set, not the 'lite' the r1 note implied)" — a note-vs-artifact mismatch to remember when reading old round rows.
- **Stale dsh paths in archived briefs**: briefs from the DSH window still carry dsh-orchestrator-setup paths (archived at briefs-archive/ — harmless, do not resurrect).
- **Local+remote redundant branch**: packet-plumber-v2-pr97-b1-wiring-pin branch deletion "awaits USER word" (row carries the branch watch).
- Possible duplication to check: C8 here vs the 08-19 agent-wait race + 08-17 liveness doctrine in AGENTS.md (mine is a new-sightings addendum); C13 vs the 08-12 pr_review key gotcha; C14 vs the 08-13 backtick class; C19/C20 vs the provider-incident classes; C23 vs the 08-16/08-19 billing rulings; C15 vs the 08-23 trigger-graph addendum.
