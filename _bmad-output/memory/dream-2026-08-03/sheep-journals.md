# Sheep findings — Gru + Silas journals

Material: 6 journal files (gru 2026-07-30, 2026-08-01, 2026-08-02; silas
2026-08-01, 2026-08-02, 2026-08-03 — the silas journal was born this
window), ~65 timestamped entries since 2026-08-01T10:44:57Z.
gru/2026-07-30.md predates the marker entirely (context only);
gru/2026-08-01.md is post-marker from the Silas hiring (~11:49Z) onward;
all silas entries are post-marker. Prior dream (2026-08-01) had NO
journal sheep — this is the first journal scan ever, so "already in
store" is checked against the live AGENTS.md gotchas + curated
field-notes + dream-2026-08-01 proposals.

## Candidate patterns

### 1. Provider incidents are now daily; the `continue`-revival doctrine scales to fleet-wide waves
- Sightings: form-stepper-f1 2026-08-01 17:40Z — "kimi-coding timed out
  4x and the turn errored... Sent 'continue' — pane back to working in
  <30s. The dead-provider gotcha paying rent again"; refcheck-rc1-2
  2026-08-01 19:35Z — "Same dead-provider pattern... model REFUSAL
  instead of timeout... Second revival of the day"; fleet wave
  2026-08-02 12:25Z — "a connection-error wave (~11:49Z–12:21Z) blocked
  the fleet — Silas included... continue x9... ALL back to working...
  Doctrine held: one 'continue' per pane, no loops"; finlit 2026-08-02
  22:50Z — "Third provider incident of the day... The errored-turn
  doctrine has carried the fleet through a quota 403 and two connection
  waves today with zero escalations needed"; Gru 2026-08-02 12:4xZ —
  "Second provider incident of the day (05:14Z quota 403, 12:0x
  connection)".
- Already in store? partial — the AGENTS.md gotcha "idle pane can hide a
  LIVE pi whose turn died on the provider → `continue`" exists
  (dream-2026-08-01 P8). NEW since: the doctrine validated at fleet
  scale (9 panes, one wave, zero escalations), the explicit
  "one continue per pane, no loops" rule, and Gru's own flag that
  recurrence warrants a provider-stability note ("worth a
  provider-stability note if it recurs" — it has, 3× in one day).
- Candidate memory target: AGENTS.md gotchas (extend the existing
  errored-turn gotcha with fleet-wave + no-loop doctrine)

### 2. Quota-wall mid-round kills a Perkins round — retry protocol with regenerate-everything amendment
- Sightings: form-save-resume-f3 / PR #563 2026-08-02 10:15Z —
  "kimi-coding account hit its usage cap ~05:14Z: Perkins r2 on #563
  died mid-round (lenses c1/c2 only, no review)... swept 8 dead panes,
  re-added the worktree at the same sha, relaunched (w1T:p3H), SAME
  round row re-pointed via sqlite, briefing carrys a
  regenerate-everything amendment"; LESSON quote — "long-lived minions
  on the same provider share one quota; a mid-round 403 leaves partial
  artifacts — always name the retry in the briefing so stale JSONs don't
  contaminate the verdict"; retry concluded clean 2026-08-02 13:30Z —
  "The retry run went clean (21/21 fresh lens verdicts)".
- Already in store? no — last dream's P8 covered the errored-turn
  `continue`; a mid-round 403 needing sweep + same-sha worktree +
  row re-point + regenerate amendment is a distinct, documented
  protocol.
- Candidate memory target: AGENTS.md gotchas (Silas/Perkins ops)

### 3. Perkins sha discipline: verify head before every dispatch; skip-rows burn noise heads without spending rounds
- Sightings: form-stepper-f1 2026-08-01 19:30Z — "Perkins sensor fired
  r2 on head 61fd8959 — the predicted docs-only delta... the skip-row
  pattern for docs-only/noise heads" (first use); 2026-08-01 21:25Z —
  "burning the FINAL r3 on a known-broken sha guarantees a stale
  verdict; r3 reviews the fix push as the merge candidate. LESSON (cost
  me a sqlite fix): skip-row notes need sha=<full 40-char> — fetch
  headRefOid first, never write sha=<short>"; 2026-08-01 21:35Z — "All
  three real rounds spent on true merge candidates — the skip-row
  policy's full payoff"; form-save-resume-f3 2026-08-02 13:45Z — "the
  minion never pushes without my sha check before dispatching the round
  (learned from the docs-only skew earlier: verify head first, always)";
  2026-08-02 12:25Z — "Verified #563's head still = r2's reviewed sha
  (11fcaa3)... the round reviews the right bytes".
- Already in store? no — the pattern was invented 2026-08-01 evening,
  after the last dream's marker.
- Candidate memory target: AGENTS.md gotchas (Perkins ops; the playbook
  Perkins section is the natural long-term home)

### 4. Ledger round-rows have their own lifecycle: Perkins can self-close its row; sqlite fills CLI gaps
- Sightings: PR #563 r2 2026-08-02 13:30Z — "this Perkins self-closed
  its round row (working->done at 13:23) — my close-out 'set done' hit
  the same-status no-op; when that happens the verdict detail MUST be
  re-recorded via 'note' (did)"; form-stepper-f1 2026-08-01 15:55Z —
  "ledger tab_id updated via sqlite (CLI has no tab-update) + note for
  the audit trail"; 2026-08-01 20:00Z — "pre-created the r2 row
  status=dispatched with the sha note — sensor deduped durably";
  2026-08-02 10:15Z — "SAME round row re-pointed via sqlite".
- Already in store? partial — the generic "ledger set refuses
  same-status transitions → ledger note" gotcha exists. NEW: round rows
  specifically can be closed by the Perkins pane itself (the close-out
  must detect the no-op and re-note the verdict), and direct sqlite is
  the accepted tool for fields the CLI can't write (tab_id, round-row
  re-point) — always paired with an audit-trail note.
- Candidate memory target: AGENTS.md gotchas

### 5. Sensor/write races: alerts are point-in-time and cross same-minute ops writes; dedup is durable-row-based
- Sightings: form-stepper-f1 2026-08-01 21:30Z — "The Perkins sensor
  fired r3-on-b13c974 in the same minute I wrote its skip-row... Pattern
  confirmed twice now: sensor alerts are point-in-time; same-minute ops
  writes can cross them. Note-only, no dispatch, no re-relay";
  2026-08-01 19:30Z — "Sensor tick carried two alerts, both
  already-mapped... durable dedup silences per-tick re-alerts";
  PR #563 2026-08-02 13:30Z — "Sensor-vs-watcher ordering: the review
  sensor fired ~2min BEFORE the pane watcher this time — relay on
  whichever arrives first, dedup the other"; Gru 2026-08-01 addendum 3 —
  dual-gated pane: "Watcher alerts WILL duplicate into Gru — treat them
  as echoes; Silas owns them".
- Already in store? partial — the "settle transitions are noise" gotcha
  covers one noise class. NEW: the generalized race/ordering doctrine
  (write durable dedup rows, expect one stale echo, relay on first
  arrival across sensors, note-only the twin).
- Candidate memory target: AGENTS.md gotchas

### 6. Fresh-session catch-up: review-sensor baselines are in-memory — startup `gh pr view` sweep + re-escalation of unacked items
- Sightings: Silas journal 2026-08-01 'Lessons' — "Review-sensor
  baselines are in-memory — a fresh Silas session has no catch-up for
  reviews posted while no Silas ran. The startup reconcile's direct
  `gh pr view` on every in-review PR covers the gap; keep that step
  non-negotiable"; same entry — "Idle ≠ broken for in-review jobs.
  Minion panes go idle the moment the PR opens"; first escalation
  2026-08-01 ~11:55Z — "Re-escalated even though the overnight notes
  existed — a fresh session cannot verify the earlier escalation reached
  the user... the escalation matrix prices that at one line"; relaunch
  2026-08-01 14:06Z — "Herdr restarted; old wA pane ids dead. Fresh
  session ran startup checklist".
- Already in store? no — Silas (and his startup checklist) post-date the
  last dream; these are first-generation COO lessons.
- Candidate memory target: neither (report-only — route to playbook
  Silas-startup section; the practice is already followed, the gap it
  covers is not written down anywhere)

### 7. Gated dispatch queues ride ledger notes on the GATE job's record; flips use the same mechanism
- Sightings: form-save-resume-f3 2026-08-01 14:20Z — "HOLD until
  righttenantry-form-stepper-f1's PR merges; dispatch C as part of that
  close-out... Also noted on B's ledger record so the close-out path
  sees it"; SEQUENCE FLIP 2026-08-01 19:05Z — "rc1-2 un-queued,
  dispatched immediately on plain develop @ f04aff3... All recorded as a
  ledger note on form-stepper-f1"; Gru 2026-08-02 00:0xZ — "The flip:
  rc1-2 fix first → stepper rebase → Perkins r3 clean → merge. Played
  out exactly"; Silas 2026-08-02 00:05Z — "The whole day's sequencing
  (parallel plan -> flip -> gates) executed without a lost round or a
  stale dispatch"; merge-friction protocol 2026-08-01 19:30Z — "first PR
  to land → relay rebase-develop heads-up to the other's pane".
- Already in store? no.
- Candidate memory target: neither (report-only — strong playbook
  dispatch/close-out candidate: "the queue lives on the gate job's
  ledger record")

### 8. Briefing lens-guards + seam-carrying handovers preempt whole classes of churn
- Sightings: refcheck-rc1-2 Perkins r1 2026-08-01 19:55Z — "Added
  lens-guard context to the briefing: missing step-aware gating is BY
  DESIGN (ships before the stepper) — preempts a whole class of false
  blockers"; PR #563 r1 2026-08-02 02:00Z — "Lens-guard context added:
  values-only drafts are spec requirement 4 (not a gap), local-only
  migration is policy, the stepper seam is sanctioned"; f3 dispatch
  2026-08-02 00:05Z — "Handover carried the stepper's documented seam
  (rt:form-step-changed event, F3-SEAM intact, firstErrorIndex as
  restore template) so no archaeology needed"; f3 finish 2026-08-02
  01:55Z — "The seam handoff paid off exactly as designed"; r2 briefing
  reuse 2026-08-02 03:50Z — "sed-template the r1 briefing + python patch
  for prior_findings/round-N — faster than re-authoring, no drift in the
  verbatim standing orders".
- Already in store? no.
- Candidate memory target: neither (report-only — playbook briefing
  conventions; demonstrably worked across 2 jobs and 5+ rounds)

### 9. Forensics ground-truth: bash-tool env ≠ pi process env; session jsonl entry types are the real probe
- Sightings: Gru 2026-08-01 addendum 2 — "`ps eww` env scraping doesn't
  work for pi processes here; the reliable probe is `env | grep ^PI_`
  from inside the bash tool" (later corrected); Gru addendum 3 — "the
  bash tool's env is NOT a reliable proxy for the pi process env —
  PI_GRU/PI_SILAS are invisible to it while harness vars (PI_MODEL etc.)
  show. Ground truth for 'which extensions are armed' = the session
  jsonl's entry types (`custom_message` = extension-injected; `message`
  role=user = typed)"; Silas 2026-08-01 19:35Z — "a worktree's session
  dir collects the minion's AND its mega-minions' sessions (shared cwd)
  — identify the live pane's file via herdr pane get agent_session, not
  by newest mtime"; Silas 2026-08-03 10:55Z — Bob's session dir is
  "--Users-moses-code-_bmad-output-bob-- (note the underscore — grep
  'bob' in the sessions dir catches it)".
- Already in store? no (addendum 2's wrong diagnosis and addendum 3's
  correction both post-date the marker; the correction invalidates the
  earlier "lesson" — consolidation must take addendum 3's version).
- Candidate memory target: AGENTS.md gotchas

### 10. Perkins 3-round arc validated: each round catches a NEW defect class lower layers cannot see
- Sightings: PR #563 2026-08-02 15:05Z — "Third round, third defect
  class caught: r1 transport security (X-Forwarded-Host), r2 browser
  runtime semantics (Illegal invocation), r3 analytics data-leak...
  strongest evidence yet for the 3-round design"; r1 2026-08-02 03:20Z —
  "continue-link tokenized URLs built on X-Forwarded-Host — victim's own
  email exfils their live PII token... Minion's own 2-hunter review
  missed it"; r2 2026-08-02 13:30Z — "detached window.setTimeout — the
  debounced save never fires in any real browser (Illegal invocation)...
  Node tests blind to it (no brand-check)"; r3 briefing 2026-08-02
  13:45Z — "instructs real-browser timer-seam verification
  (specifically — the class Node can't see)"; user cap override
  2026-08-02 22:50Z — "r4 live on d3f7700... override verbatim on the
  round row + no-precedent flag in the briefing" (Gru: "cap stays 3
  going forward").
- Already in store? no (last dream pruned a similar "Perkins works"
  signal as working-as-designed — the NEW content here is the
  per-round-novel-defect-class evidence + the browser-empirical blind
  spot + the cap-override protocol).
- Candidate memory target: minion-field-notes.md (the tooling trap:
  detached `window.setTimeout` / DOM seams are invisible to Node tests —
  verify timer/browser seams empirically in a real browser; RightTenantry
  crew). The "3-round design validated" line itself is report-only.

### 11. Non-blocking clarify: escalate rulings without flipping to clarifying; the pane resumes on the relay
- Sightings: finlit-gdd-v1 2026-08-01 18:50Z — "8 numbered design-ruling
  questions... explicitly NOT a halt ('keep building while you
  ponder')... New pattern worth noting: non-blocking clarify — escalate
  the same, but don't flip to clarifying and don't expect the pane to
  stay done; it resumes on the relay"; resolution 2026-08-01 20:5xZ
  (Gru) — "User answered all 9 in the browser + Send&End... Silas
  drained the queue + relayed to the GDD minion".
- Already in store? no.
- Candidate memory target: neither (report-only — playbook clarify-relay
  section; one episode but a named, reusable status-handling rule)

## One-off anecdotes (single sighting — watch items)

- **db.sh banner goes to STDERR** (backlog-extract ops, 2026-08-02
  10:20Z): "don't tail-strip stdout (lost the CSV header on the first
  pass, re-extracted)". Companion convention that worked: used the app's
  OWN cohort query — "Count matched the report's 66 exactly".
- **`edit` tool aborts ALL edits atomically on one oldText mismatch**
  (Gru 2026-08-01 addendum): "two playbook attempts rolled back
  wholesale. Verify multi-line oldText line-break positions with grep
  before submitting batches". Durable tooling fact; gotcha-worthy
  despite the single sighting.
- **Parse-test extensions before commit** (Gru 2026-08-01 addendum):
  "Both extensions parse-tested with `node --experimental-strip-types`
  before commit (backtick gotcha discipline)". Extends the in-store
  backtick gotcha with its preventive practice.
- **User philosophy for briefings** (Gru 2026-08-02 00:3xZ): "user
  accepts expectation-setting copy ahead of machinery when the human
  would do it anyway" (landlord_helper ruling). A user-preference
  memory for future briefing authors.
- **Dual-gate echo open loop** (Gru 2026-08-01 addendum 3): this Gru
  process has BOTH PI_GRU=1 and PI_SILAS=1; fix = relaunch as
  `env -u PI_SILAS PI_GRU=1 pi`. No later entry confirms the relaunch —
  next dream should check whether the loop closed.
- **Gru journal 2026-07-31 backfill STILL missing** — carried watch
  item from dream-2026-08-01 ("the biggest day... has no journal
  entry"); no 2026-07-31.md exists as of this scan. Second dream
  flagging it → promote.
- **Long-lived minion cost watch** (Silas 2026-08-02 10:15Z /
  2026-08-03 10:55Z): finlit-gdd-v1 "12h build, one cache-miss rebill",
  later "at 5.2M tokens and counting"; shares the kimi-coding quota
  with the whole fleet (ties into pattern 2).
- **Test-DB container debris on :54323** (Silas 2026-08-01 13:10Z, via
  Gru addendum 2): "left for review rounds; user's call to stop" — no
  later entry records the stop.
- **Store paying rent (no action, confirmation only)**: the in-store
  gotchas were visibly load-bearing all window — deliverable-not-
  reported REPRIMAND (2026-08-01 15:55Z), identity-tab hygiene (same
  entry), handover verification (every dispatch), settle-vs-finish
  classification (2026-08-01 18:40Z "done = clean finish (not
  settle)"). Do not re-propose any of these.
