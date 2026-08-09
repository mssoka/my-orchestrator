# Dream report — 2026-08-03

Material: 17 field-note shards (4 new since marker), 6 journal files
(~65 entries), 200 ledger events across 23 jobs — since
2026-08-01T10:44:57Z. Sheep: sheep-shards, sheep-journals, sheep-ledger
(findings in sibling files; all sheep badged out and closed).

Store copies with all **auto** edits applied diff-ready:
`_bmad-output/memory/dream-2026-08-03/store/` (diff vs live: field-notes
70 diff-lines, AGENTS.md 38 diff-lines — all appends + two entry
amendments).

## Proposals

### P1 — Multi-edit `edit` calls are atomic; formatters invalidate stale batches
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry — one bad oldText rejects the WHOLE batch silently;
  re-apply survivors individually; re-read the file after any formatter
  run before re-issuing; grep-verify multi-line oldText break positions.
- Evidence: form-save-resume-f3 2026-08-02 ("lost two email_client edits
  + a decoder edit this way, caught only by compile");
  refcheck-privacy-draft 2026-08-02 ("`gleam format` reflows split strings
  between runs"); finlit-bugfix-event-messages 2026-07-31; Gru journal
  2026-08-01 ("two playbook attempts rolled back wholesale").
- Reasoning: 4 sightings across 2 repos (Gleam + Godot) and 2 agent
  roles — a tool-level trap that costs silent work-loss every time it
  bites. Not previously curated.

### P2 — Lustre SSR: assert the serialized render, never view-source assumptions
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry — attributes render sorted by name (empty-valued ones
  bare); apostrophes escape to `&#39;`; page copy can contain your
  assertion substring — pin `checked data-testid="..."`.
- Evidence: refcheck-rc1-2 2026-08-01 (attribute sort + substring
  collision, two pins); form-save-resume-f3 2026-08-02 (attribute sort,
  independent rediscovery); refcheck-privacy-draft 2026-08-02 (houdini
  `&#39;` escape).
- Reasoning: independently hit in 3 jobs in 2 days; each cost a failing
  pin or a false one. Deterministic framework behavior — durable.

### P3 — `server/priv/static/*` gitignore whitelist: new static assets deploy dead
- Target: `docs/minion-field-notes.md` (Recurring review findings) · Class: **auto** (applied)
- Change: new entry — new static asset without a `!` line deploys as a
  dead script tag while SSR pins stay green; whitelist in the same PR.
  (Also seeds the previously-empty Recurring review findings section;
  the Supabase security-definer watch note is preserved.)
- Evidence: form-funnel-w0 2026-07-31 (shard-recorded, missed promotion
  in dream-2026-08-01); form-stepper-f1 2026-08-01; form-save-resume-f3
  2026-08-02 — **all three caught only by review swarms.**
- Reasoning: the strongest promote signal of this pass — shard-recorded
  a week ago, unpromoted, bitten twice since. SSR-tag pins are structurally
  blind to it; only the .gitignore line prevents it.

### P4 — Ground-truth-first extends to reviewer MECHANISM claims
- Target: `docs/minion-field-notes.md` (extend existing Conventions
  entry) · Class: **auto** (applied)
- Change: amend the ground-truth-first entry — two independent hunters
  hallucinated native-browser-validation blockers on a form carrying
  `novalidate` on both GET and error re-render; verify the mechanism
  exists against the actual element/runtime.
- Evidence: refcheck-rc1-2 2026-08-01 (novalidate case, both hunters
  independently); finlit-game-brief 2026-07-31 (stale-context findings
  corroborate the meta-pattern).
- Reasoning: new failure mode of a curated convention — not stale
  findings but invented browser mechanics. Cheap to check, expensive to
  "fix".

### P5 — RightTenantry env traps generalize: dot_env clobbers process env; staging lags migrations
- Target: `docs/minion-field-notes.md` (Tooling traps, beside the
  Squirrel entry) · Class: **auto** (applied)
- Change: new entry — `dot_env.load_default()` overrides the PROCESS env
  at runtime (repoint via an edited gitignored `server/.env` copy, not
  env vars); staging lags unmerged migrations (submissions 500) — E2E on
  a local Docker DB + seeded vacancy, never staging.
- Evidence: form-stepper-f1 2026-08-01 (both halves);
  form-funnel-w0 + refcheck-rc1-1 + refcheck-rc2-1 2026-07-31
  (corroboration).
- Reasoning: the anti-staging half was curated only for Squirrel regen;
  the trap is wider (any E2E) and the dot_env clobber defeats the obvious
  workaround (env override) — that combination is what cost time.

### P6 — Token/PII leaks recur across seams; rework introduces the next round's blocker
- Target: `docs/minion-field-notes.md` (Recurring review findings) · Class: **auto** (applied)
- Change: new entry — a scrub-in-one-place token finding means audit the
  WHOLE token path (URL generation, DOM/analytics, headers, logs) in the
  same fix; each Perkins round's rework can create the next round's
  blocker — full-suite re-run + regression pin per fix.
- Evidence: form-save-resume-f3 PR #563 arc (r1 X-Forwarded-Host token
  exfil → r3 PostHog autocapture scraping the raw token from `<body>` —
  different seam each round); form-stepper-f1 PR #561 arc (r2's 2
  blockers were both in r1's reworked E2E suite).
- Reasoning: two independent Perkins arcs show the same shape. The fix
  behavior is what needs to change, not the review.

### P7 — Node tests are blind to browser-runtime semantics (detached window.setTimeout)
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry — a detached `window.setTimeout` debounce passes all
  Node tests (no brand-check), throws `Illegal invocation` in any real
  browser; timer/DOM seams need empirical real-browser verification.
- Evidence: form-save-resume-f3 Perkins r2 2026-08-02 (empirical catch —
  the blocker suite-green Node could not see); r3 briefing 2026-08-02
  (real-browser timer-seam verification explicitly instructed — the
  practice already adopted).
- Reasoning: names the blind spot of the default test layer; the
  empirical re-drive is what caught the round's only blocker.

### P8 — Provider incidents: 3 classes, 3 recoveries (quota wall ≠ errored turn)
- Target: `AGENTS.md` gotchas (append) · Class: **auto** (applied)
- Change: new gotcha — stalls/refusals/connection-waves = LIVE pi with
  `stopReason:"error"` → one `continue` per pane, no loops, then verify
  any reviewed sha; account-wide quota 403 = DEAD panes → sweep, re-add
  worktree at same sha, re-dispatch the SAME round row with a
  regenerate-everything amendment, another job's activity as recovery
  evidence; second failure → blocked + escalate.
- Evidence: form-stepper-f1 2026-08-01 (stall→continue); refcheck-rc1-2
  2026-08-01 (refusal→continue); form-save-resume-f3-perkins-r2
  2026-08-02 (quota 403 → retry sweep, clean 21/21; connection wave →
  continue x9, sha verified); finlit-gdd-v1 2026-08-03 (3 incidents in
  one day).
- Reasoning: the existing errored-turn gotcha covers class 1; the quota
  wall nearly cost a Perkins round and its recovery protocol (esp.
  regenerate-everything, so stale lens JSONs don't contaminate the
  verdict) existed only in Silas' journal.

### P9 — Sensor-vs-write races: expect one stale echo per action; note-only, never re-act
- Target: `AGENTS.md` gotchas (append) · Class: **auto** (applied)
- Change: new gotcha — review/Perkins/cap sensors re-fire seconds-to-
  minutes after Silas already acted; answer with a same-status note, never
  a second action; durable dedup = round row + full-sha note written the
  same minute; racing sensors → relay on first arrival, note the twin.
- Evidence: 6+ sightings 2026-08-01/02 (PR #563 ×3 incl. "Third
  sensor-vs-write race today — pattern documented"; rc1-2 APPROVED echo;
  stepper-f1 double echo).
- Reasoning: distinct class from the curated settle-transition noise;
  the handling doctrine (durable same-minute dedup + note-only echoes) is
  what kept 6 races from becoming double dispatches/relays/escalations.

### P10 — Perkins can self-close its round row → pre-emptive verdict note
- Target: `AGENTS.md` gotchas (append) · Class: **auto** (applied)
- Change: new gotcha — closing the Perkins pane writes `working -> done`
  itself; the close-out `set done` then no-ops and eats the verdict;
  write the verdict note pre-emptively at close-out.
- Evidence: form-save-resume-f3-perkins-r2 2026-08-02 (verdict
  re-recorded after the collision); -perkins-r3 2026-08-02 (pre-emptive
  note written — practice already adopted).
- Reasoning: the existing same-status gotcha names the tool behavior but
  not this cause; the insurance costs one line and removes a silent
  verdict-loss mode.

### P11 — Pane forensics: session jsonl is ground truth, not env scraping
- Target: `AGENTS.md` gotchas (append) · Class: **auto** (applied)
- Change: new gotcha — bash-tool env ≠ pane pi-process env (PI_GRU/
  PI_SILAS invisible); armed extensions = jsonl entry types
  (`custom_message` vs `message`); worktree session dirs mix minion +
  mega-minion sessions — identify via `herdr pane get` agent_session,
  never newest mtime.
- Evidence: Gru journal 2026-08-01 addenda 2–3 (wrong diagnosis
  self-corrected — consolidation takes the corrected version); Silas
  journal 2026-08-01 (session-dir mixing) + 2026-08-03 (Bob's own
  underscore session dir).
- Reasoning: two independent investigators burned time on the wrong
  probe in one window; the correct probes are now named twice each.

### P12 — Stale-remedy prune: cwd exile, not extension gating, is the gru.ts control
- Target: `docs/minion-field-notes.md` (amend the 2026-08-01
  dream-2026-08-01 entry) · Class: **auto** (applied)
- Change: the entry's "until the extensions are gated, brief every pane"
  remedy clause replaced — operative control is cwd exile (per the
  AGENTS.md gotcha); the NOT-Gru brief line remains belt-and-braces.
- Evidence: dream-2026-08-01 + 3 sheep ran as pseudo-Grus 2026-08-01;
  since cwd exile (Bob home dir), zero recurrences including this pass's
  3 sheep; no extension gating ever landed.
- Reasoning: keeps the curated remedy pointing at the control that
  actually works; the old framing implied a pending fix that never came.

### P13 — Playbook: codify the Perkins ops practices invented this window
- Target: `docs/orchestration-playbook.md` (Perkins section + Silas
  startup ritual) · Class: **user-ack** (NOT applied — playbook edit)
- Change: three additions, all with ≥2 sightings:
  (a) **Skip-row policy** — a docs-only/noise head or a known-broken sha
  gets a `-perkins-skip-<sha>` row (note carries `sha=<full-40>`; fetch
  headRefOid first, never a short sha) instead of burning a round:
  preserves the 3-round cap and dedups per-tick sensor alerts. Payoff
  sighted: stepper-f1 r3 APPROVED 0B because two skips kept r3 for the
  merge candidate.
  (b) **Proactive next-round dispatch precondition** — dispatch the next
  round on the fix push with prior_findings handed over, and write the
  round row + full-sha note in the SAME minute (this same-minute write
  is what makes later sensor ticks dedup silently — see P9).
  (c) **Startup catch-up made explicit** — the Silas startup ritual's
  "catch-up" step should name the gap it covers: review-sensor baselines
  are in-memory (documented in the playbook's failure modes), so a fresh
  Silas runs a direct `gh pr view` sweep on every in-review PR and
  re-escalates anything unacked (a fresh session cannot verify an earlier
  escalation reached the user; the matrix prices a re-escalation at one
  line).
- Evidence: skip rows ×2 + payoff (2026-08-01); proactive dispatch ×3
  (2026-08-01/02); catch-up gap + first re-escalation (Silas journal
  2026-08-01, ×2 entries).
- Reasoning: all three are practiced and proven but live only in
  journals; the playbook is what a fresh Silas re-reads.

## Watch items (anecdotes — tracked, not proposed)

- **Hold-release for pane capacity** (one episode, 2026-08-01): pre-create
  the round row `dispatched` to dedup the sensor, attach pane/worktree at
  execution (~20-pane valve). Worked once; propose on second use.
- **Non-blocking clarify** (one episode, finlit-gdd-v1 2026-08-01):
  escalate rulings WITHOUT flipping to clarifying; the pane resumes on
  the relay. Named, reusable — propose on second use.
- **Watcher 'pane vanished' can be self-inflicted** by your own cleanup
  sweep (f3-perkins-r2 2026-08-02): check whether you closed the pane
  yourself before treating a vanish as an incident.
- **Ledger event text strips `$` amounts** (finlit-tutor-economy-fix
  2026-08-01): prices mangled ("Duplex ,000") — keep $ figures in PR
  bodies, not ledger notes.
- **Parse-test extensions before commit** (Gru 2026-08-01):
  `node --experimental-strip-types` — the preventive practice for the
  in-store backtick gotcha; amend that gotcha on second sighting.
- **`gleam format` must cover all packages** (refcheck-rc2-1 2026-07-31):
  CI red from formatting `server` but not `shared/`.
- **Provider instability is daily and clustered** (finlit-gdd-v1
  2026-08-03: 3 incidents in one day; long-lived minion at 5.2M tokens
  sharing the fleet quota). Watch whether waves cluster; cost note for
  marathon builds.
- **Gru journal 2026-07-31 backfill STILL missing** — second consecutive
  dream flagging. Gru owns journals; flagged for Gru's wind-down.
- **Dual-gate echo open loop** (Gru 2026-08-01): this Gru process had
  BOTH PI_GRU=1 and PI_SILAS=1; fix = relaunch `env -u PI_SILAS PI_GRU=1
  pi` — no journal entry confirms the relaunch; next dream should check.
- **Test-DB container debris on :54323** (2026-08-01, left for review
  rounds; no stop recorded).
- Lustre `element.unsafe_raw_html` cannot emit a standalone HTML comment
  (refcheck-privacy-draft 2026-08-02 — post-render string.replace +
  uniqueness pin instead).
- Making a form field mandatory server-side breaks 5 bug-hunt scenario
  files — update all in the same PR (refcheck-rc1-2 2026-08-01).
- form.js's `_form_loaded_at` IIFE overwrites the SSR stamp on every
  load — deliberate backdating needs a marker guard (form-save-resume-f3
  2026-08-02).
- Upload-slot `.field-error` spans need inline `display:flex`; same bug
  in form.js preflight `showInlineError`, still deferred
  (form-stepper-f1 2026-08-01).
- User preference for briefing authors: expectation-setting copy ahead of
  machinery is acceptable when the human would do it anyway
  (landlord_helper ruling, 2026-08-02).
- db.sh banner goes to STDERR — don't tail-strip stdout
  (backlog-extract, 2026-08-02).

## Pruned / rejected candidates (with why)

- **Cap mechanics worked; override by explicit user ruling** (PR #563
  cap-3 + r4 override with no-precedent flag) — working-as-designed
  confirmation; the protocol is already policy. Report-only.
- **Banked seams/handoffs get consumed by successors** (4 sightings —
  validate_choice owner, rt:form-step-changed, RC2.3 fold-ins) — already
  the standing handover practice; confirmation, no change.
- **Lavish rulings loop for DOCS deliverables** (3 sightings) — already
  encoded in the root project instructions; working as designed.
- **Round close-out formula** (verify posted / 0 lens leftovers / pane /
  worktree) — already verbatim in playbook Perkins step 7. Report-only.
- **"Perkins 3-round design validated"** (each round caught a novel
  defect class — transport security, browser runtime, analytics leak) —
  strong evidence, but it's a design confirmation, not a memory item;
  the actionable kernel (browser-empirical blind spot) is P7.
- **Queue-next notes ride the gate job's ledger record** (f3 queued on
  stepper-f1; the user sequence-flip executed cleanly) — worked, but one
  continuous arc (single job chain); carried in journals. Revisit if a
  second arc uses it.
- **Briefing lens-guards preempt false blockers** (rc1-2, f3) — two
  sightings and it worked, but it is a briefing-craft refinement for
  Silas' judgement, not a rule; over-codifying risks boilerplate.
  Journal-carried.
