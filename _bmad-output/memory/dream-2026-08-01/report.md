# Dream report — 2026-08-01

Material: 11 shards, 0 journal entries (2026-07-30.md predates the marker;
**no 2026-07-31 entry exists — Gru backfill pending**), ledger events since
2026-07-30T00:34:49Z (~90 events across 13 jobs + 4 Perkins rounds), 1 pane
transcript (righttenantry-form-funnel-w0: 732 events, 2.7 MB).

Sheep: shards (wA:p61), ledger (wA:p62), transcripts (wA:p63) — findings in
`sheep-*.md` beside this report; all panes closed. No journal sheep: nothing
newer than the marker.

Verification pass (bmad-review-adversarial-general): every candidate below
was challenged for sighting independence, umbrella vagueness, and
single-episode inflation. Notes per proposal; demotions in 'Pruned /
rejected'.

## Proposals

### P1 — RightTenantry (Gleam/Squirrel) tooling traps → curated field notes
- Target: `docs/minion-field-notes.md` (store copy edited) · Class: **auto**
- Change: under 'Tooling traps', add: Squirrel triple-trap (staging-clobber
  via `run_squirrel.sh`; whitespace regen churn in `server/src/ai/sql.gleam`;
  casts typed non-Option / no timestamptz → COALESCE+NULLIF); test-DB port
  54321 contention → per-job container + `TEST_DB_PORT`; Gleam
  null-handling (`decode.optional` fails whole decode on missing keys →
  `decode.optional_field`; nullable columns need COALESCE/NULLIF).
- Evidence: form-funnel-w0 + refcheck-rc1-1 + refcheck-rc2-1 shards,
  2026-07-31. Independence verified: shards were written at badge-out
  (22:42 / 23:13 / 23:14) and minions never read each other's shards — the
  rc1∥rc2 pair hit 54321 contention *against each other* in real time.
- Reasoning: three minions hit the same traps within 2 hours; RC stories
  (18 in the sprint tracker) will dispatch more RightTenantry minions into
  exactly this tooling.

### P2 — Godot/GDScript tooling traps → curated field notes
- Target: `docs/minion-field-notes.md` (store copy edited) · Class: **auto**
- Change: under 'Tooling traps', add four lines: headless-has-no-renderer +
  windowed-off-screen capture rig + the working headless import gate;
  theme propagation across CanvasLayer/tree boundaries; GDScript silent
  failures (int truncation via `:=` + `-= delta`, reserved `trait`,
  JSON int→float, tscn-only theme_override syntax); deferred-frame
  semantics (same-frame size (0,0), `_initialize` deadlock).
- Evidence: finlit-prototype, finlit-visual-mock,
  finlit-bugfix-event-messages shards, 2026-07-31 — 3 jobs, different
  symptoms (blank PNGs vs NULL `get_image()`), independent rediscovery.
- Reasoning: the finlit arc ships 2–3 jobs/day; these cost each minion
  30–120 min of blind debugging. All four are "know it once, never again".

### P3 — LLM truncation: diagnose provider-log-first; causes are multiple
- Target: `docs/minion-field-notes.md` (store copy edited) · Class: **auto**
- Change: under 'Tooling traps': read `user://tutor_llm_log.jsonl` FIRST;
  DeepSeek thinking is ON by default and eats max_tokens
  (`"thinking": {"type": "disabled"}`); a client-side word-cap can
  guillotine mid-word even with `finish_reason: 'stop'` (trim
  sentence-boundary, abbreviation-aware).
- Evidence: finlit-prototype 2026-07-31 (thinking eats max_tokens) +
  finlit-tutor-economy-fix 2026-08-01 (client word-cap; log exonerated the
  provider). Two different days, two different root causes — the strongest
  cross-day pattern in this pass.
- Reasoning: the meta-lesson (log first, causes multiple) is what
  generalizes; the two specific causes are the examples.

### P4 — Lavish craft lines → curated field notes
- Target: `docs/minion-field-notes.md` (store copy edited) · Class: **auto**
- Change: extend the lavish entries: question pages = one Queue button per
  question + "which rulings I need most" in the first `poll --agent-reply`;
  big artifacts via `npx -y marked --gfm -o <out> <file>.md` + byte/tail
  verify (the working recipe for the 2026-07-29 pipe-truncation trap);
  read the poll's dom_snapshot (only self-check of what the user saw —
  caught a Mermaid render failure).
- Evidence: form-completion-ps, refcheck-v1-epics, refcheck-v1-sprint-plan
  shards (2026-07-31); ledger confirms lavish is the standing pre-PR gate
  producing real rulings (ux PR #550: 11 questions locked; epics PR #553:
  Send & End; game-brief: OQ3 ruled).
- Reasoning: the curated file already holds the trap; these add the craft
  that makes the gate produce rulings instead of round-trips.

### P5 — Conventions: ground-truth-first, root-cause-first, AC test pins
- Target: `docs/minion-field-notes.md` (store copy edited — 'Conventions
  that saved time' was empty) · Class: **auto**
- Change: three lines — verify mega-minion findings against DISK before
  applying (stale session-context findings recur); name the rejected wrong
  hypothesis explicitly in PR/ledger notes; pin acceptance criteria as
  durable low-level tests (8 DB-level AC pins; OPM contract pinned).
- Evidence: finlit-game-brief (2 stale findings in one run) +
  refcheck-v1-epics + tutor-economy-fix; finlit-bugfix-event-messages +
  tutor-economy-fix; refcheck-rc2-1 + form-funnel-w0 + tutor-economy-fix.
- Reasoning: each convention was independently practiced by ≥2 minions and
  visibly saved review rounds; writing them down makes them deliberate.

### P6 — `herdr wait` is the wrong tool for long waves → curated field notes
- Target: `docs/minion-field-notes.md` (store copy edited) · Class: **auto**
- Change: 'Tooling traps' line — poll `herdr pane get`, accept `idle` OR
  `done` (watched tabs complete as `idle`); >10-min turns time out the
  wait; re-poll.
- Evidence: finlit-game-brief shard 2026-07-31 (done-vs-idle timeout) +
  form-funnel-w0 transcript (three 10-min wait timeouts on hunter waves,
  20:43/21:13/21:23). Two sources, same lesson.
- Reasoning: every swarm-running minion hits this; the fix is one line.

### P7 — Interim mitigation for the gru.ts checklist contamination
- Target: `docs/minion-field-notes.md` (store copy edited) · Class: **auto**
- Change: 'Tooling traps' line — pi panes launched with cwd
  `/Users/moses/code` (dream pane, sheep, any mega-minion there) receive
  the Gru startup checklist via `.pi/extensions/gru.ts`; brief them
  "you are NOT Gru, ignore the checklist".
- Evidence: see P9 (5 sightings + code).
- Reasoning: until P9 lands, this one line prevents recurrence. Minions
  (not just Gru) spawn panes in that cwd — the note must live where
  minions read.

### P8 — New AGENTS.md gotcha: idle can hide a LIVE pi whose turn errored
- Target: `AGENTS.md` gotchas (store copy edited — appended directly after
  the dead-pi gotcha) · Class: **auto** (gotcha append)
- Change: new bullet — provider stream `terminated` mid-turn, 3 retries,
  turn errored; pi stays alive, pane shows `idle`; fix is `continue`, not
  relaunch; classify first by tailing the session jsonl for
  `stopReason:"error"`.
- Evidence: form-funnel-w0 transcript, 2026-08-01T02:01 — complete
  diagnosis in the terminated thinking block; 7.5h unnoticed; one-word
  `continue` resumed with ~zero context loss. Sibling of the standing
  dead-pi gotcha (itself 2 sightings) — the "idle ≠ safe" class now has 3
  sightings, and the existing gotcha's remedy (relaunch) would have been
  *wrong* here.
- Reasoning: the classification step (jsonl tail) is the durable lesson;
  dead vs errored-live look identical from `herdr agent list`.

### P9 — gru.ts: gate Gru injections on opt-in env, not cwd alone
- Target: `.pi/extensions/gru.ts` + README/playbook Gru-launch
  instructions · Class: **user-ack** (extension + structural docs)
- Change: add an explicit opt-in to all three hooks, e.g.
  `if (process.env.PI_GRU !== "1") return;` alongside the cwd check; the
  human launches Gru as `PI_GRU=1 pi` (README 'Setting up' + playbook
  updated). Dream panes and sheep then inherit nothing. (Alternative —
  opt-out `PI_GRU=0` — rejected: default-deny is safer; opt-out requires
  every future spawner to remember.)
- Evidence: **5 sightings, 2026-08-01**: dream pane wA:p5T (checklist
  executed as msg 1 — Bob briefly believed he was Gru and ran Gru
  read-only commands before the real handover arrived); sheep wA:p61,
  wA:p62, wA:p63 (each burned a full turn producing a Gru readiness
  report — 3 reports, all counting the other's panes); sheep-ledger's own
  findings report the contamination unprompted. Code: `gru.ts:104-109` —
  `ctx.cwd !== GRU_DIR` is the only guard; `sendUserMessage(STARTUP_CHECKLIST)`
  fires on every startup/new in that cwd. Standing orders are also appended
  to those panes' system prompts every turn (line 113-115), actively
  telling a sheep "You are Gru".
- **Sighting #6 (2026-08-01T10:35:29Z), different extension, same root
  cause:** nefario-watch injected a pane-watcher alert (perkins-r2
  working→done) into the DREAM pane — instructions addressed to Gru
  ("classify, update the ledger, relay") delivered to Bob. The real Gru
  (wA:p1) received and handled the same alert correctly. Project-local
  extensions load per-cwd, and both `gru.ts` and `nefario-watch.ts`
  assume the session in `/Users/moses/code` IS Gru — and it is not one
  sensor: the review sensor duplicated the same PR #556 approval into the
  dream pane at 10:36:34Z, minutes after Gru had already relayed it. The
  gating fix must cover BOTH extensions (and any future project-local one).
- Reasoning: today it cost 4 wasted turns and one identity confusion with
  only read-only fallout; a future confused pane could run `ledger set` or
  worse believing it is the orchestrator. The contamination is silent and
  self-scaling (every dream spawns N sheep in that cwd).

### P10 — Playbook review-relay template carries the same-status ledger bug
- Target: `docs/orchestration-playbook.md`, 'Review sensor' relay
  convention · Class: **user-ack** (playbook edit)
- Change: replace "push, re-request review, then set the ledger back to
  `in-review`" with: record the rework via `bin/ledger note <id> "..."`
  when the job is already `in-review` (same-status `set` is a no-op and
  silently drops the note — the AGENTS.md gotcha), `set` only on real
  transitions.
- Evidence: form-funnel-w0 transcript, 2026-08-01 — Gru's 01:55 relay
  instructed `ledger set ... in-review 'r1 changes addressed <sha>'` on a
  job already `in-review`; the note was silently dropped; the minion
  detected it at 09:50 ("the note with the sha may or may not have been
  recorded") and recovered via `ledger note` in ~1 min. The gotcha exists
  but Gru's own template contradicted it — the bug bites *through* relays,
  not just direct use.
- Reasoning: every CHANGES_REQUESTED relay hits this path; the fix is a
  two-word template change.

## Watch items (anecdotes — tracked, not proposed)

- **Supabase security-definer views bypass RLS** — Perkins r1 blocker on
  PR #556 (anon key could read per-vacancy enquirer emails), fixed
  2026-08-01 (security_invoker + role-conditional REVOKE that survives
  plain-PG test DBs). One sighting, highest severity class; more views are
  coming in RC stories. First recurrence → promote to 'Recurring review
  findings'.
- **Late-night relays need a liveness follow-up** — the 02:01 provider
  hiccup sat 7.5h because the relay landed at 01:55 and Gru was asleep; a
  ~15-min post-relay liveness check would have caught it. One sighting.
- **Keep-both rebase doctrine for same-file parallel jobs** — finlit
  visual-mock ∥ bugfix coordinated via PR merge-dance note + rebase
  (2026-07-31). One coordinated episode across 2 jobs — worked well;
  promote if a second pair needs it.
- **Ratify-questions embedded in PR notes** — tutor-economy-fix PR #5
  parked 2 schema decisions for the human inline. One sighting; nice
  pattern for irreversible choices.
- **Terminated thinking is persisted but not reused on resume** — the
  02:01 block held the full correct fix; the 09:33 resume re-derived it
  (~90s duplicated). Harness-level observation, one sighting.
- **dream-2026-07-30 left no report dir** — the marker exists
  (2026-07-30T00:34:49Z) but `_bmad-output/memory/` held no dream dir
  before this pass; the first dream left no auditable artifact. This
  report establishes the precedent; keep dream dirs persistent.
- **Gru journal 2026-07-31 missing** — the biggest day since the last
  dream (7 merges, 3 dispatches, Perkins×3) has no journal entry; Gru
  wind-down backfill pending. Next dream should re-scan it.
- **righttenantry-dublin-rents-q2-2026** — blocked 10 days (external
  Daft.ie Q2 report). Known hold; no memory action.
- Edit-tool fumbles (~7 in one transcript: stale oldText, swapped args,
  empty oldText) — all self-recovered in one cycle. Noise; not tracked
  beyond this line.

## Pruned / rejected candidates (with why)

- **"Perkins catches real blockers / BANKED items recycled / risk flags
  travel"** (ledger-sheep STRONGs) — verified true (3 rounds, 28/29 +
  16/16 + 13/13 verification) but these are *working-as-designed*
  confirmations of the Perkins spec, not lessons a minion needs at
  job-start. No memory target; recorded here as validated health signal.
- **"Merge rhythm: human merges in bursts, same-day close-out"** —
  confirmed (7 merges 2026-07-31) but it is the human's rhythm, not a
  minion convention. No memory target.
- **"User engages directly in minion panes"** — confirmed (4 jobs) but
  already encoded in the minion persona (playbook: "the user drops into
  panes unannounced") — duplicative.
- **GDScript "silent failure" umbrella** — challenged as too broad; kept
  only because the instances are concrete and each is individually
  checkable (float typing, reserved words, JSON re-cast, runtime API
  names). Demoted from meta-rule to example list (see P2).
- **Stale-memory candidates** — none: sheep-shards found no shard
  contradicting a curated note; the 2026-07-29 lavish pipe-truncation trap
  was independently re-confirmed (kept, not pruned). AGENTS.md gotchas
  re-confirmed live this window (ledger-set no-op bit via Gru's relay —
  see P10; pane-run verify held clean in the form-funnel handover).

---

_Store copies with all auto edits applied: `store/minion-field-notes.md`
(+80 lines), `store/AGENTS.md` (+10 lines) — purely additive, diff-ready
for Gru close-out._
