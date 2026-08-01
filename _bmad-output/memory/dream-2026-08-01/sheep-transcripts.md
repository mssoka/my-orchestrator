# Sheep findings — transcript: righttenantry-form-funnel-w0 (wA:p46)

Source: session `2026-07-31T19-23-29-298Z_…jsonl` (732 events, 2.7 MB,
model kimi-coding/k3) + live pane tail + the 4 mega-minion (hunter)
sessions in the same session dir.

## Crash signature (02:01 arc)

**Not a pi process crash — a model-provider connection failure that ended
the turn and left a LIVE pi sitting idle for 7.5 h.**

- 01:55:54: user msg from Gru: "WORK NEEDED — Perkins r1 on PR #556
  returned CHANGES_REQUESTED…" — review relay delivered; minion began
  rework immediately.
- 01:59:50: last good toolResult: `psql:…/20260731213000_add_inbound_email_sender_state_view.sql:55:
  ERROR: role "anon" does not exist` + Gleam type mismatch
  (`followup_due` — view expression typed `Option(Bool)`). Minion was
  mid-migration on the Perkins blocker, ~5 min into the rework.
- 02:01:14: assistant event with a **complete, correct diagnosis in the
  thinking block** ("Fix: make the REVOKE role-conditional… DO $$ …"),
  then `stopReason: "error"`, `errorMessage: "terminated"` — provider
  stream cut mid-turn, 0 output tokens.
- 02:01:16 / 02:01:20 / 02:01:28: three empty assistant events,
  `errorMessage: "Connection error."` — pi retried 3× in 14 s against
  kimi-coding, gave up, turn died. Pane went idle.
- **02:01:28 → 09:31:53: 7.5 h of silence.** Nobody acted — the failure
  came 5 min after a ~2am relay; Gru was asleep. Detection presumably
  fired (idle transition) with no one awake to classify it.
- 09:31:53: user msg `continue` — Gru's one-word nudge. Same session, no
  relaunch: pi had never died.
- 09:33:00: minion's first post-nudge thinking re-derives the identical
  two-issue diagnosis ("Two issues from the last output: 1. role "anon"
  does not exist… 2. followup_due type mismatch") from the last tool
  result. **Context loss ≈ zero** — one duplicated thinking block (~90 s)
  is the entire re-work cost. Rework completed, sha 7bb5824 pushed
  09:50:30, PR comment posted 09:52.

**Recovery cost:** 7.5 h wall-clock (the real damage — overnight latency,
not lost work); ~0 context; ~0 re-work.

**New trap variant** [STRONG — sibling of the known "idle pane hides a
DEAD pi"]: an **idle pane can also hide a LIVE pi whose turn silently
errored** (provider connection exhausted retries). From the outside both
look like `idle`; the difference matters — this one needs only
`continue`, not a relaunch. Classification step for idle-mid-task panes:
tail the session jsonl for `stopReason:"error"` before assuming done or
dead. Secondary lesson: late-night relays (01:55) need a follow-up
liveness check within ~15 min, or a provider hiccup sleeps until morning.

## Other trap evidence

### `bin/ledger set` same-status no-op — Gru's OWN RELAY TEMPLATE carries the bug [STRONG]
- Gru's review-relay message (01:55:54) instructed: "set the ledger back:
  `/Users/moses/code/bin/ledger set righttenantry-form-funnel-w0
  in-review 'r1 changes addressed <sha>'`" — a guaranteed no-op (job was
  already `in-review`).
- 09:50:45 (thinking): "output says 'already in-review'… the note with
  the sha may or may not have been recorded".
- 09:50:57: `ledger show` confirms the note is missing; 09:51:25 reads
  `--help`; 09:51:40: `bin/ledger note righttenantry-form-funnel-w0 "r1
  changes addressed 7bb5824 …"` → "noted".
- Evidence: minion recovered alone in ~1 min / 4 tool calls — but the
  fix belongs in **Gru's review-relay template**: when status is already
  `in-review`, the relay must say `ledger note`, not `ledger set`
  (matches AGENTS.md gotcha; now proven to bite minions via Gru's
  instructions, not just Gru directly).

### `herdr wait agent-status` 10-min timeouts on mega-minion waves
- 20:43:01: "both-working timed out waiting for agent status change"
  (wave-1 hunters); 21:13:06 and 21:23:23: same, wave 2.
- Handled by re-polling ("working working" → wait again) — friction, not
  failure. Hunters take >10 min; a single 10-min wait is the wrong tool;
  poll loop or longer timeout.

### Edit-tool fumbles (all self-recovered)
- 20:07:47: "Could not find edits[0] in client/src/api/vacancy_…" →
  "Misfiled the first edit — splitting by file." (multi-file edit call).
- 21:31:35 + 09:48:08: stale `oldText` after squirrel regen / earlier
  edits — recovered by re-reading.
- 09:33:24: "Could not find the exact text in supabase/migration…" →
  "Swapped my edit args — redoing."
- 09:38:10: "edits[1].oldText must not be empty".
- ~7 occurrences total; each cost one extra cycle. Anecdote-level noise,
  no pattern worth a rule.

### Good-behavior confirmations (no action needed)
- Handover clean: Gru waited for idle, single handover msg 19:24:13,
  minion read playbook + briefing immediately — no unsent-buffer
  incident this session.
- Mega-minion hygiene: two hunter waves (p4E/p4F 20:32, p4H/p4J 21:02),
  findings triaged, all 4 panes closed (20:50:09, ~21:30); hunter
  session files contain **zero** error events.
- Rituals kept: ledger self-reports at every transition (19:24
  working, 21:41 in-review), field-note shard written 21:42:08
  (793 bytes), `herdr notification` + final summary with PR URL.
- Minor self-recovered friction: heredoc lost cwd (21:37:25 `cd: server:
  No such file or directory`); node test-runner module path
  (20:14:16–20:14:30) — one cycle each.

## Anecdotes
- Whole job ran on kimi-coding **k3**; final statusline: CH 99.8%,
  ~34%/1M ctx, $28.16 — the provider, not the harness, was the single
  point of failure.
- Perkins r1 landed 01:55, ~4.2 h after the PR opened (21:41) — review
  latency pushed the rework into the 2am dead zone where the provider
  hiccup went unnoticed.
- The terminated 02:01:14 thinking block already contained the correct
  fix (role-conditional REVOKE DO-block); the 09:33 resume re-derived it
  independently — terminated-thinking is persisted but not treated as
  done work on resume.
