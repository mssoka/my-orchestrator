# Sheep shard: sheep-journals (Gru + Silas journals, post-marker)

Source: Gru journal 2026-08-09 (post 13:54:22Z) + 2026-08-11 (all), Silas
journal 2026-08-09 (all, ~920 lines) + 2026-08-11 (all). Marker =
2026-08-09T13:54:22Z. Everything below is NEWER than the marker and was
matched against the baseline `store/AGENTS.md` + `store/minion-field-notes.md`
to avoid re-proposing what's already captured.

Convention: sighting count in the title; single-sighting items are included
where Silas/Gru explicitly flagged them as future-note material or the lesson
is high-leverage — Bob filters further.

---

### C1 — Descriptive tab labels convention (NEW user ruling, applied) [3+ sightings]

- Target: AGENTS.md gotchas → Dispatch & handover (or a new "Conventions" subsection)
- Class-hint: NEW
- Lesson: Tabs get DESCRIPTIVE labels, never a bare number — short but
  self-explanatory so the tab-bar shows what's happening at a glance.
  Perkins round tab → `perkins-<job-slug>-r<N>`; mega-minion tab →
  `<job-slug>-<role>`; impl-job tab → `<job-id>`. Panes inside keep
  `mm-<lens>-r<N>`. This is now a standing convention (Gru relayed the
  user ruling; Silas added it to the playbook in 3 spots: Dispatch step-3,
  Perkins step-5, minion standing orders).
- Evidence:
  - Silas journal 2026-08-10T13:05Z: "New convention: DESCRIPTIVE TAB
    LABELS (user ruling); applied + playbook updated … Relabeled the #597
    Perkins tab w1T:t5N: was '8' (generic default) -> 'perkins-apply-form-scrub-fix-r1'."
  - Silas journal 2026-08-10T18:35Z: "tab t5R, BOTH labeled
    'perkins-boundary-gate-state-fix-r1' (the new descriptive-tab
    convention — this time the tab got the convention label at creation,
    not a generic number)."
  - Silas journal 2026-08-10T15:40Z (rta dispatch): "tab label
    'rta-boundary-gate-fix' (descriptive per the new convention + Gru's
    example; pane label = full job-id)."
- Why it makes future sessions smarter: Ops hygiene that prevents the
  "which pane is which?" confusion on a busy board; also pairs with the
  existing "minions never split into identity tabs" gotcha (a labeled
  minion tab is trivially movable out of an identity tab).

---

### C2 — `herdr pane move --label` labels the TAB, not the PANE [1 sighting, explicitly noted recurring]

- Target: AGENTS.md gotchas → Dispatch & handover (or Extensions)
- Class-hint: NEW (adjacent to the existing "`herdr pane move` has no
  `--json` flag" gotcha — same tool, different failure)
- Lesson: `herdr pane move --label <x>` propagates the label to the TAB
  only; the pane's own label stays `None`. Always follow a move with an
  explicit `herdr pane rename <pane> <x>` so the pane is identifiable in
  `herdr agent list` / pane reads. (Distinct from the `--json` gotcha,
  which is about output parsing; this is about label propagation.)
- Evidence:
  - Silas journal 2026-08-09T23:45Z (routing-explorer dispatch): "NOTE:
    the move --label labeled the TAB but NOT the pane (pane label=None)
    -> explicit `herdr pane rename` to fix. (Recurring: pane move doesn't
    propagate the label to the pane, only the tab — always follow with
    pane rename.)"
- Why it makes future sessions smarter: Stops phantom/unlabeled panes
  that force a `herdr agent list` + cwd-forensics detour to identify;
  the rename is one command.

---

### C3 — `herdr tab create` can land in the wrong workspace (verify + move) [2 sightings]

- Target: AGENTS.md gotchas → Dispatch & handover
- Class-hint: NEW
- Lesson: `herdr tab create` (esp. with no explicit `--workspace`) can
  default to whatever workspace is currently focused — not necessarily
  Gru/Silas's home workspace (w1T). The new pane then lives in the wrong
  workspace until moved. Verify the pane's workspace after create
  (`herdr pane get` / `herdr tab list`), and move it into w1T. (Silas
  later built auto-move-into-w1T handling inline, but the verify step
  remains — the default is nondeterministic across sessions.)
- Evidence:
  - Silas journal 2026-08-10T19:40Z (rc3-4 r1 release): "the tab create
    landed in w2N (the create defaulted to a different focused workspace
    this time!) -> MOVED w2N:p2 -> w1T:pR6 / tab t5X … session + queued
    handover survived the move."
  - Silas journal 2026-08-10T20:10Z (#599 r2): "the tab create defaulted
    to w2N AGAIN — the auto-move-into-w1T logic now handles it inline, no
    manual step."
- Why it makes future sessions smarter: A pane stranded in the wrong
  workspace is invisible on Gru's board sweep and easy to lose track of;
  one verify + move fixes it.

---

### C4 — DOUBLE-provider outage + CEO (Gru) himself on the failing provider [1 sighting, high-leverage]

- Target: AGENTS.md gotchas → Provider incidents (AMEND the "3/5 classes" gotcha)
- Class-hint: AMEND — extends the existing "Provider incidents come in 3
  classes (…now 5)" gotcha with a compound/CEO class
- Lesson: When the CEO (Gru) is himself on the failing provider, the
  normal escalation path (Silas → Gru → user) BREAKS — Gru's response
  turn 403s and never relays. Fall back to `herdr notification show`
  (pane-independent system notification) to reach the user directly, and
  PROTECT STATE SILENTLY (ledger notes, no kills — preserve at-risk
  worktree work for commit recovery) while the provider decision is
  pending. A double-provider outage (kimi quota-403 + glm-5.2 429 from a
  concurrent burst) leaves only the mechanical tier (deepseek); the
  user's provider-strategy decision becomes the gate. This is distinct
  from the single-provider classes already captured.
- Evidence:
  - Silas journal 2026-08-09T21:40Z: "🚨 DOUBLE PROVIDER INCIDENT: kimi
    quota-403 + glm-5.2 429; Gru himself dead … ESCALATION PATH BROKEN:
    Gru is kimi-dead — my [SILAS] escalation landed in his pane (visible)
    but his response turn 403'd … Fired a high-visibility `herdr
    notification show` (system notification, pane-independent)."
  - Silas journal 2026-08-09T21:40Z (lesson): "when the CEO (Gru) is
    himself on the failing provider, the escalation path breaks — fall
    back to `herdr notification show` … and protect state silently while
    the provider decision is pending. A double-provider outage (kimi+glm)
    leaves only the mechanical tier (deepseek)."
- Why it makes future sessions smarter: The `notification show` fallback
  is the only channel that reaches the user when Gru is down — without
  this doctrine the incident stalls silently waiting on a dead Gru turn.

---

### C5 — Serialize glm-5.2 concurrent BURSTS (model-capacity, not pane-capacity) [2+ sightings]

- Target: AGENTS.md gotchas → Provider incidents (and/or Watchers/Perkins)
- Class-hint: NEW (distinct from the pane-capacity serialize-hold gotcha)
- Lesson: A Perkins round = ~8 concurrent glm-5.2 panes; run two rounds
  (or a round + a fanned-out mega-minion wave) concurrently and the
  concurrent glm-5.2 calls trip an account rate-limit 429. SERIALIZE the
  bursts (one fan-out at a time), accept light single-pane core
  concurrency. Concretely: defer/stagger a job's mega-minions entirely
  until an in-flight Perkins round closes (trigger = the round's
  close-out). This is a MODEL-CAPACITY serialize, sibling to the
  pane-capacity serialize-hold — same dedup mechanism, different gate.
- Evidence:
  - Silas journal 2026-08-09T23:48Z (Gru ruling): "Gru concurrency
    ruling: serialize bursts; pQ4 fully-defers mega-minions until Perkins
    r2 closes … SERIALIZE the bursts, accept core concurrency … protecting
    Perkins r2's clean glm-5.2 run is the priority — a 429 mid-round is
    the failure mode that killed it once."
  - Silas journal 2026-08-09T21:40Z: "ZAI-CODING-CN/GLM-5.2 429
    rate-limit: 13 UNIDENTIFIED panes … ALL glm-5.2 + rate-limited
    (Chinese 429 '账户已达到速率限制' = account rate limit) — likely a
    burst from 13 concurrent glm-5.2 calls."
- Why it makes future sessions smarter: Prevents the avoidable
  mid-round 429 that kills a Perkins round (the exact failure that
  forced the rc3-3 r2 retry); the serialize-burst trigger is cheap.

---

### C6 — Premature cleanup-KILL on a stale transcript (re-read CURRENT transcript before any destructive action) [1 sighting, high-leverage, self-flagged]

- Target: AGENTS.md gotchas → Provider incidents (and/or Pane forensics)
- Class-hint: NEW
- Lesson: Before any DESTRUCTIVE pane action (killing processes,
  sweeping panes), RE-READ the pane's CURRENT transcript — pane state
  evolves fast between the alert timestamp, the transcript read, and the
  action. A `working->blocked` alert on a transient 429 can be STALE by
  the time you act: pi retried past it, glm-5.2 recovered, lenses
  completed with real findings. Acting on the stale tail orphans the
  lenses the minion was productively polling. Confirm the failure is
  STUCK before sweeping; transient provider blips (429) self-recover.
- Evidence:
  - Silas journal 2026-08-09T23:38Z: "pPT glm-5.2 429 was TRANSIENT
    (minion recovered); my cleanup-kill was premature — heads-up sent …
    I acted on STALE transcript state (the 429 at the transcript tail);
    between my read and my kill, pPT had recovered … My kill orphaned the
    3 incomplete lenses the minion was waiting on."
  - Silas journal 2026-08-09T23:38Z (lesson): "re-read a pane's CURRENT
    transcript immediately before any destructive action (kill
    processes) … Transient provider blips (429) self-recover; confirm
    the failure STUCK before sweeping."
- Why it makes future sessions smarter: Kills are irreversible; this
  re-read-before-kill discipline stops burning completed lens work + a
  ~5min re-run on a self-recovering blip. Pairs with the existing
  "Classify by transcript + pane age BEFORE acting" 5th-class gotcha
  (that one is about NOT continue-spamming; this is about NOT
  kill-sweeping).

---

### C7 — Perkins round created a BRANCH where only a detached worktree should exist (dispatch-mechanics anomaly) [2 sightings, 3 branches, explicitly dream-flagged]

- Target: AGENTS.md gotchas → Watchers, sensors & Perkins rounds
- Class-hint: NEW
- Lesson: Perkins rounds use DETACHED worktrees (`git worktree add
  --detach <sha>` — no branch created; dedup is ledger-ROW-based, not
  branch-based). Yet perkins-* branches have appeared as merged debris
  (3 branches across 2 repos: perkins-odin-prototype-r1/r2 +
  perkins-refcheck-rc3-3-r1) — meaning a dispatch used `herdr worktree
  create --branch <slug>` (the regular-minion path, which creates a
  branch) where the Perkins `git worktree add --detach` path was
  correct, OR a Perkins minion created the branch itself. Harmless when
  caught (merged + recoverable from main; torch with `branch -D`), but
  it's a dispatch-mechanics inconsistency worth auditing. Dream
  pattern-match target: grep dispatch history / Perkins round setups
  for `--branch` where `--detach` was correct.
- Evidence:
  - Silas journal 2026-08-10T00:58Z: "Torch perkins-odin-prototype-r1/r2
    branch debris (Gru); ANOMALY noted … Perkins rounds use DETACHED
    worktrees … Yet perkins-odin-prototype-r1 + r2 existed as BRANCHES
    (merged into main) … Dream pattern-match target: grep dispatch
    history / Perkins round setups for `--branch` where `--detach` was
    correct."
  - Silas journal 2026-08-10T01:02Z: "Perkins-branch ANOMALY = 2nd
    sighting: perkins-refcheck-rc3-3-r1 branch existed as merged debris …
    now 3 branches across 2 repos (odin r1/r2 + rc3-3 r1). A dispatch is
    using `--branch` (herdr worktree create path) where the Perkins
    `git worktree add --detach` path is correct."
- Why it makes future sessions smarter: Flags a latent dispatch bug
  (wrong worktree-create path) before it causes a real problem (e.g. a
  branch-name collision or a dedup confusion); the audit target is named.

---

### C8 — Verify merge/deploy state by commit-containment AFTER pull, never by grepping a single file [2 sightings]

- Target: AGENTS.md gotchas → Ledger (and/or a new "Close-out verification" note)
- Class-hint: NEW
- Lesson: Two failure modes when verifying whether a PR/fix is actually
  in a branch: (a) grepping a single file for the change gives a FALSE
  NEGATIVE if you grep the wrong file (or the change lives elsewhere);
  (b) checking `--merged` / ancestry BEFORE pulling lies — a stale local
  base predates the merge. Use `git merge-base --is-ancestor <commit>
  <branch>` (commit-containment) as the authoritative check, and run it
  AFTER `pull --ff-only` (or `git fetch origin <base>:<base>` when the
  tree is held). Commit-containment is immune to both the wrong-file and
  stale-base traps.
- Evidence:
  - Gru journal 2026-08-11 (RTA #172 family): "RTA #172 family FULLY
    closed in prod … verified via commit-containment, not file-grep —
    grepping the wrong file gave a false negative … LESSON: verify
    deploy/merge state by `git merge-base --is-ancestor` / commit
    containment, not by grepping a single file (wrong-file = false
    negative)."
  - Silas journal 2026-08-10T01:02Z (rc3-3 close-out): "local develop
    (f3c29c3) was STALE (predated the merge), so refcheck-rc3-3 showed
    'NOT in --merged develop' pre-pull; post-pull develop advanced to
    include the #596 merge … Lesson reinforced: check --merged AFTER the
    pull, not before — a stale local base lies about merge status."
- Why it makes future sessions smarter: Stops the false-negative
  re-deploy / re-fix loop (the RTA vetting was safe to re-process but
  file-grep said otherwise); commit-containment is one command and
  unambiguous.

---

### C9 — Briefing boilerplate "After user approval" is the MERGE gate, not a pre-PR approval [1 sighting, Silas explicitly flagged for AGENTS.md]

- Target: AGENTS.md gotchas → Dispatch & handover (and/or minion-field-notes "Conventions that saved time")
- Class-hint: NEW
- Lesson: The standard briefing boilerplate line "After user approval:
  commit, push, open PR" refers to the MERGE gate (the human reviews +
  merges the PR) — NOT a pre-PR approval step. Minions that read it as a
  pre-PR gate stall needlessly with green work unpushed. Silas should
  un-stick via the standard flow (commit→push→open PR now; rc3-3 opened
  #596 with no pre-gate precedent) rather than escalate a non-gate. The
  user still gates the merge + Perkins reviews. (If the user genuinely
  wanted pre-PR approval, they'd say so explicitly / the briefing would
  name a lavish gate.)
- Evidence:
  - Silas journal 2026-08-10T12:50Z: "scrub-fix COMPLETE but halted for
    pre-PR approval; directed standard flow (misread of boilerplate) …
    The wording is standard boilerplate (identical in rc3-3/rc3-4
    briefings); rc3-3 OPENED #596 without a pre-gate … LESSON (for a
    future AGENTS.md note): the briefing boilerplate 'After user
    approval: commit, push, open PR' is the MERGE gate, not a pre-PR
    approval — minions that read it as a pre-PR gate stall needlessly."
- Why it makes future sessions smarter: Un-sticks a HIGH-PRIORITY prod
  fix (the 0/25 form-collapse crisis) without a user round-trip for a
  standard step; also a minion-side reading-convention win.

---

### C10 — `ledger pr` convention is propagating: the briefing template now carries an explicit "set the pr field" instruction [AMEND, 5+ sightings + the fix]

- Target: AGENTS.md gotchas → Ledger (AMEND the "`ledger set in-review` does NOT populate the pr field" gotcha)
- Class-hint: AMEND-2026-08-07 (the existing pr-field gotcha) — adds the durable fix
- Lesson: The existing gotcha (minion self-reports in-review with the URL
  in the note → `pr` NULL → PR watcher silently skips) recurred 5+
  times this window (scrub-fix #597, rta-boundary #173, slot-clear #174,
  sprint-replan #20, …) — BUT two durable fixes are now in flight: (1)
  the briefing template now carries an EXPLICIT `ledger pr <id> <url>`
  instruction, and minions are starting to run it themselves (rc3-4 #599
  "THE MINION RAN `ledger pr` ITSELF this time … only took 4 jobs";
  v2-1.1 #21 "the minion SET the pr field itself — 2nd job in a row");
  (2) Silas still runs `ledger pr` as a belt-and-braces on any in-review
  transition where the field is empty. Amend the gotcha to record that
  the template-level instruction is the durable fix and it's working.
- Evidence:
  - Silas journal 2026-08-10T19:05Z (rc3-4): "THE MINION RAN `ledger pr`
    ITSELF this time (pr field set — the convention propagated after my
    repeated fixes; only took 4 jobs)."
  - Silas journal 2026-08-11T02:35Z (rc3-5 dispatch): "the explicit
    ledger pr instruction — the briefing template now tells minions to
    set the pr field, addressing the recurring gotcha."
  - Silas journal 2026-08-11T04:05Z (#21): "the minion SET the pr field
    itself (the briefing template's explicit ledger-pr instruction
    worked — 2nd job in a row)."
  - Silas journal 2026-08-10T12:55Z / 18:25Z / 00:45Z / 02:05Z: the
    recurring NULL-pr cases Silas fixed with `ledger pr`.
- Why it makes future sessions smarter: Confirms the durable fix
  (template instruction) is taking hold, so Silas can taper the manual
  belt-and-braces run; also flags that the gotcha is NOT yet fully
  solved (still recurred 5x) so the verify step stays.

---

### C11 — bmad tooling resolves repo-root to the CANONICAL checkout, bypassing a worktree minion's writes (4+ sightings, escalating to source files) [AMEND/NEW field-note]

- Target: minion-field-notes.md → Tooling traps (AMEND the 2026-08-07 "relative paths surprise in worktrees" entry; the bmad-tooling root-resolution cause is distinct) AND AGENTS.md gotchas → Ledger/Pane forensics (the close-out stash/pull/pop recovery)
- Class-hint: AMEND-2026-08-07 (relative-paths-in-worktrees field-note) — names the tooling root-resolution root cause + the source-file escalation
- Lesson: The bmad tooling (`create-story` / `dev-story`) resolves the
  repo root to the CANONICAL checkout (`/Users/moses/code/<repo>`)
  instead of the worktree cwd — so a worktree-dispatched minion's edits
  to tracker/spec/source files land in the MAIN checkout, not its
  worktree. The tracker/spec artifacts were the early symptom (rc3-3
  tracker, rc3-4 tracker+spec); rc3-5 escalated it to LIVE STORY SOURCE
  files (sweep.gleam + 5 sweep_*.sql landed entirely in the main
  checkout; the worktree was completely clean). MINION-SIDE: after
  edits, run `git status` in YOUR cwd and confirm the edits landed in
  your worktree; check the tooling's resolved root before trusting its
  writes; commit/push/PR from the worktree only. OPS-SIDE (close-out):
  the main-checkout dirty files block `pull --ff-only` — recover with
  stash→pull→pop (preserve, sync, restore), OR when the merge itself
  brings a committed version of the same file, the MERGE SUPERSEDES —
  revert to HEAD rather than preserve the tooling copy. A misdirected
  live story is recovered by syncing the misplaced files byte-identical
  into the worktree (cmp-verified) and committing from there.
- Evidence:
  - Gru journal 2026-08-11: "bmad tooling-quirk (writes tracker/spec to
    main checkout, not worktree) — 3+ sightings; field-note candidate so
    the dream hardens the 'respect worktree cwd' rule into minion
    standing orders."
  - Silas journal 2026-08-11T04:40Z: "ACTIVE ISSUE: rc3-5 bmad-tooling
    quirk (4th sighting, misdirecting a LIVE story) … the bmad tooling
    (create-story/dev-story) resolves the repo root to the CANONICAL
    checkout (/Users/moses/code/RightTenantry) instead of the worktree
    cwd — a worktree-dispatched minion's edits bypass its worktree
    entirely. The tracker/spec artifacts were the early symptom; source
    files are the escalation."
  - Silas journal 2026-08-10T14:00Z (rc3-3 close-out, the stash/pull/pop
    pattern): "the MAIN checkout had an unstaged tracked-file
    modification … pQ5's rc3-4 create-story tracker update, written to
    the MAIN checkout by the bmad tooling (path quirk) … stash->pull->pop
    is the safe pattern (preserve, sync, restore)."
  - Silas journal 2026-08-11T02:15Z (#599 close-out, merge-supersedes):
    "when a merge brings a committed version of a file the tooling also
    dirtied in the main checkout, the merge supersedes — revert to HEAD
    rather than preserve the tooling copy."
- Why it makes future sessions smarter: This is now the single most
  frequent minion-side trap (4+ sightings, escalating severity) and the
  existing field-note (relative paths) doesn't name the tooling
  root-resolution cause or the source-file escalation; hardening it into
  standing orders ("verify where your edits land") stops a live story
  from being silently misdirected again.

---

### C12 — Client-populated hidden field needs page-specific JS wiring + a BROWSER-PATH test; server-side `simulate.form_body` masks the gap [the inert-W1 saga, AMEND] [1 arc, r1→r2→r3, propagated as a lens-guard to 3+ later rounds]

- Target: minion-field-notes.md → Conventions that saved time (AMEND the "prove a new test/guard actually BITES" + "Node tests are blind to browser-runtime semantics" entries)
- Class-hint: AMEND-2026-08-09 (prove-test-bites) — names the specific simulate.form_body mask + the page-specific-wiring fix
- Lesson: A client-populated hidden field (e.g. `_focus_seconds`) ships
  in the form HTML but is NEVER populated unless page-specific JS wires
  a submit listener that writes it. A server-side integration test that
  POSTs the field via `simulate.form_body` PASSES while production stays
  broken (focus_seconds always 0) — the test masks the gap because it
  bypasses the browser path. Fix: wire a page-specific submit seam +
  pin it with a NODE/real-browser test that drives the actual listener
  (NOT a `simulate.form_body` mask). This exact mask-vs-real-test
  distinction is now a standard Perkins lens-guard ("NOT a
  simulate.form_body mask — the #599 r2 lesson") carried into #21, #174,
  and #22 briefings.
- Evidence:
  - Silas journal 2026-08-10T20:35Z (#599 r2): "NEW BLOCKER B2-r2 … W1's
    fix is INERT — _focus_seconds ships in the review-form HTML but
    reference_form.js NEVER populates it … -> focus_seconds_reported
    STILL always 0 in production (the exact r1 defect). The new flow
    test MASKS it (POSTs 240 directly via simulate.form_body, bypassing
    the browser)."
  - Silas journal 2026-08-10T20:45Z (#599 r3 fix): "added an
    initReviewSubmit seam … Pinned by 4 NODE tests driving the browser
    path (NOT simulate.form_body — the r2 lesson)."
  - Silas journal 2026-08-11T04:05Z / 00:45Z / 09:30Z (#21, #174, #22
    briefings): "real-path regression test no-mask (the #599 r2 lesson)"
    / "NOT a simulate.form_body mask (the #599 r2 lesson)" — propagated
    as a standing lens-guard.
- Why it makes future sessions smarter: The mask-vs-real-test failure
  mode recurred within ONE job's review arc (r1 fixed-but-inert → B2-r2
  → r3 code-trace proof); naming the specific `simulate.form_body` mask
  + the page-specific-wiring fix lets minions avoid it on the first
  round instead of burning two review rounds.

---

### C13 — Temp-worktree for branch merges (develop→staging deploy) when the main checkout is dirty [1 sighting, clean technique]

- Target: AGENTS.md gotchas → Dispatch & handover / Ledger (close-out/deploy technique)
- Class-hint: NEW
- Lesson: To merge one branch into another (e.g. develop→staging for a
  deploy) when the main checkout is dirty (the bmad-tracker quirk, or
  any parked modifications), DON'T do a stash dance on the main
  checkout — use a TEMP WORKTREE: `git worktree add -b <tmp> <wt>
  origin/<target>` → `git merge origin/<source> --no-edit` → `git push
  origin HEAD:<target>` → cleanup (worktree remove + branch -D). The
  main checkout is untouched. If `<target>` ever gains real independent
  changes (not just merge-commits of `<source>`), the next merge may
  conflict — report, don't force.
- Evidence:
  - Silas journal 2026-08-10T14:10Z: "RT develop -> staging merged +
    pushed (deploy prep, user-directed ops) … EXECUTION (via temp
    worktree — avoided touching the main checkout's dirty pQ5 tracker
    entirely): `git worktree add -b staging-merge <wt> origin/staging`
    -> `git merge origin/develop --no-edit` (clean, merge commit
    20056ca) -> `git push origin HEAD:staging` … NOTE: the temp-worktree
    pattern is the clean way to do branch merges when the main checkout
    is dirty (tracker quirk) — no stash dance needed."
- Why it makes future sessions smarter: A clean, no-risk deploy-merge
  technique that sidesteps the dirty-main-checkout trap entirely (vs
  the stash/pull/pop dance used at story close-outs).

---

### C14 — Frozen telemetry vocabulary = a stable contract (don't drive-by rename; add to codespell ignore-words) [1 sighting, clear principle]

- Target: minion-field-notes.md → Conventions that saved time (and/or Recurring review findings)
- Class-hint: NEW
- Lesson: Telemetry/event-name tokens (e.g. `compliance.review_unparseable`)
  are a FROZEN CONTRACT — downstream BQ/Sentry queries + tests depend on
  the exact spelling. A drive-by "fix" (a global codespell sed renaming
  `unparseable`→`unparsable`) silently breaks the contract + the test
  suite count claim. The fix is NOT to restore standard spelling in the
  token; it's to ADD the non-standard word to `[tool.codespell]
  ignore-words` (frozen vocabulary stays frozen; prose keeps standard
  spelling). When touching a telemetry string, grep the contract
  consumers first; treat the token as load-bearing.
- Evidence:
  - Silas journal 2026-08-10T19:15Z (#173 r1 blocker B1): "ACCIDENTAL
    TELEMETRY RENAME — compliance.review_unparseable ->
    review_unparsable (dropped the 'e') … a drive-by in the diff — breaks
    test_unparseable_review_emits_failed_rollup … + the stable BQ/Sentry
    event-name contract #172's evidence queries use."
  - Silas journal 2026-08-10T19:20Z (fix): "B1: restored
    compliance.review_unparseable (the stable event-name contract; the
    drive-by was a global codespell sed) + added 'unparseable' to
    [tool.codespell] ignore-words (frozen vocabulary = a stable telemetry
    contract; prose keeps standard spelling)."
- Why it makes future sessions smarter: Stops the silent
  telemetry-contract break from a well-intentioned spelling "fix"; the
  codespell-ignore-words resolution is non-obvious and durable.

---

### C15 — "No BFS" mandate is PRECISE, not absolute; lavish Decide answers arrive as compact codes [2 minor canon/lavish craft notes]

- Target: minion-field-notes.md → Conventions that saved time (canon-interpretation + lavish craft)
- Class-hint: NEW (two small notes from the sprint-replan-v2 minion field-notes)
- Lesson: (a) Canon bans like "No BFS legacy" are PRECISE, not absolute —
  the PP mandate bans spawn-time BFS + cached route + RR/LB, but
  ODN-10 rule 1 permits a deterministic SPF computing the forwarding
  table internally; read the ban's exact scope before treating a
  mechanism as forbidden. (b) Lavish multi-question Decide answers can
  arrive as compact codes ("1A,2B,3A") and an empty freeform field
  still arrives as a prompt tag with empty text — parse both, don't
  assume a missing freeform means no answer.
- Evidence:
  - Silas journal 2026-08-11T02:05Z (sprint-replan field-notes):
    "'No BFS legacy' is precise not absolute — the mandate bans
    spawn-time BFS+cached route+RR/LB, but ODN-10 rule 1 permits a
    deterministic SPF computing the forwarding table internally."
  - Silas journal 2026-08-11T02:05Z: "lavish multi-question Decide
    answers can arrive as compact codes ('1A,2B,3A') + an empty freeform
    field still arrives as a prompt tag with empty text."
- Why it makes future sessions smarter: Saves a minion from
  over-restricting a design (treating a permitted SPF as banned) and
  from mis-parsing a lavish verdict.

---

### C16 — Canon-amendment disambiguation: two 'E' namespaces + superseded-vs-live architecture docs [1 sighting, PP-specific but generalizable]

- Target: minion-field-notes.md → Conventions that saved time (AMEND the 2026-08-09 canon-amendment craft entry)
- Class-hint: AMEND-2026-08-09 (canon-doc amendment craft — grep the full blast radius)
- Lesson: When grep-bounding a canon amendment, disambiguate colliding
  namespaces + superseded-vs-live docs explicitly: (a) packet-plumber has
  TWO 'E' namespaces — arch edge-case E1-E32 vs GDD epic E1-E11 (a bare
  "E1" citation is ambiguous; qualify it); (b) `architecture-v1.md` is
  the SUPERSEDED GL5.2/Godot arch, `odin-architecture-v1.md` is the LIVE
  canon — only the latter gets amended. A recent date on a doc does NOT
  mean it's the current stack (sprint-plan-v1 was dated post-pivot but
  drafted in Godot/GDScript citing the superseded arch). Grep the
  architecture citation a plan/doc carries before trusting its stack.
- Evidence:
  - Silas journal 2026-08-10T09:38Z (canon-amend blast radius): "disambiguate
    the two 'E' namespaces (arch edge-case E1-E32 vs GDD epic E1-E11) +
    architecture-v1.md (superseded GL5.2/Godot) vs odin-architecture-v1.md
    (live canon) — only the latter amended."
  - Silas journal 2026-08-11T02:05Z (sprint-replan field-notes): "grep
    the ARCHITECTURE CITATION before trusting a plan's stack — v1 was
    dated post-pivot but drafted in Godot/GDScript citing
    architecture-v1.md … a recent date != current stack."
- Why it makes future sessions smarter: Stops amending the wrong
  (superseded) doc and quoting the wrong 'E' namespace — both produce
  silent internal contradictions in canon that a 2-hunter review catches
  late.

---

### C17 — Docs-deliverable lavish gate HOLDS correctly across an absent-user window (REINFORCE the overnight-poll pattern) [1 clear sighting]

- Target: minion-field-notes.md → Conventions that saved time (AMEND the lavish-overnight/state.json entries)
- Class-hint: AMEND-2026-08-09 (the `~/.lavish-axi/state.json` ground-truth path) + AMEND-2026-08-07 (lavish craft)
- Lesson: The docs-deliverable lavish-before-PR gate works AS DESIGNED
  across a multi-hour absent-user window: the minion HOLDS the gate
  (doesn't escalate as blocked, doesn't open the PR prematurely), polls
  on each bash timeout (queued feedback never lost), verifies the
  verdict via `~/.lavish-axi/state.json` (`ended_by:user` + the verdict
  text), THEN opens the PR. A polling minion shows `working` — that is
  WAITING, not stuck. Reinforces that the state.json path is the
  ground-truth verification before acting on any load-bearing verdict.
- Evidence:
  - Silas journal 2026-08-10T09:38Z (canon-amend): "the docs-deliverable
    lavish-before-PR gate working AS DESIGNED across an absent-user
    window: the minion held the gate (didn't escalate as blocked, didn't
    open the PR prematurely), polled on each bash timeout (queued
    feedback never lost), verified the verdict via state.json, THEN
    opened the PR … lavish sign-off captured (user 'good' + Send&End
    after a ~6.5h overnight poll)."
- Why it makes future sessions smarter: Confirms (3rd+ time) the
  overnight-poll + state.json-verify pattern is the correct minion
  behavior, so a dream-promoted note telling minions to "hold + poll +
  verify-via-state.json" lands as established practice, not a one-off.

---

### C18 — CONTINUOUS EXECUTION policy (user ruling): auto-dispatch the next story on merge [standing ruling, playbook-captured — for awareness]

- Target: NOT a gotcha (it's a standing ruling) — surfaced for Bob's awareness; likely stays in the playbook, not AGENTS.md
- Class-hint: NEW ruling (context only)
- Lesson: As of 2026-08-11, the user ruled CONTINUOUS EXECUTION: once a
  story merges, dispatch the NEXT story WITHOUT waiting for a Gru/user
  greenlight (applies to RT refcheck rc3-5→…→RC5 AND PP slice 1→slice N).
  Pause ONLY on a genuine user-pending gate (lavish clarify, decision,
  external gate). Gru authors the next briefing + hands it to Silas on
  each merge-relay. This REPLACES the older "dispatch one story, wait
  for merge + greenlight" sprint pattern (fresh-minion-per-story still
  holds; only the greenlight gate is dropped). Already captured in the
  Gru journal (2026-08-11 standing ruling) + a playbook ops-note. NOT a
  gotcha — surfaced so the dream doesn't re-litigate what's already a
  locked ruling.
- Evidence:
  - Gru journal 2026-08-11: "Standing ruling: CONTINUOUS EXECUTION …
    Once a story merges, dispatch the NEXT story without waiting for a
    user greenlight … Replaces the older 'Gru dispatches one story,
    waits for merge + greenlight' sprint pattern."
  - Silas journal 2026-08-11T02:35Z: "NEW STANDING POLICY (user ruling):
    CONTINUOUS EXECUTION … CAPTURED: journal + a playbook ops-note."
- Why it makes future sessions smarter: Context only — confirms it's
  playbook-captured, so no dream action needed beyond awareness.

---

## Summary for Bob's filter

Strongest (multi-sighting / high-leverage / Silas-or-Gru explicitly
flagged): **C1** (descriptive tab labels — user ruling, playbook-captured),
**C4** (double-provider + CEO-down — `notification show` fallback),
**C5** (serialize glm-5.2 bursts), **C6** (re-read transcript before kill),
**C7** (Perkins-branch anomaly — dream-flagged, 3 branches), **C8**
(commit-containment not file-grep), **C10** (ledger pr — the durable
template fix), **C11** (bmad tooling root-resolution — 4+ sightings,
escalating, field-note candidate named by Gru), **C12** (inert-W1
simulate.form_body mask — propagated lens-guard).

Solid single-sighting: **C2** (pane move --label → tab only, noted
recurring), **C3** (tab create lands in wrong workspace), **C9**
(boilerplate = merge gate — Silas flagged for AGENTS.md), **C13**
(temp-worktree branch merge), **C14** (frozen telemetry vocabulary).

Minor / reinforce: **C15**, **C16**, **C17**. Awareness-only: **C18**.

All AMEND candidates name their target existing entry. No re-proposals of
already-captured material detected (matched against the full baseline
AGENTS.md gotchas + minion-field-notes sections).
