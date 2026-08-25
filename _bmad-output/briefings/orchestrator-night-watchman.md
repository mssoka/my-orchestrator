# Briefing: orchestrator-night-watchman

## Mission

The orchestrator's sensors all live INSIDE Silas's pi (nefario-watch is an
in-process extension). When that pi dies silently — twice now: 17:59Z
reboot + ~00:38Z silent death on 08-20/21 — the whole machine goes deaf
until a human notices (user woke to a merged PR with no close-out, no
dispatch, 5h dead air). Build a watchman OUTSIDE the pi processes.

KEY LESSON from the incident: the PANE being up proves nothing — a dead pi
leaves a healthy shell prompt. The watchman must check AGENT LIVENESS
(herdr agent detection + session-file activity), never pane existence.

## Deliverables

1. `bin/night-watchman` (bash, `--once` mode + default daemon-friendly):
   - For each long-lived staff pane, resolved BY TAB LABEL (survives pane-id
     churn): `silas` (tab label `silas`), `gru` (tab label `Gru`):
     - `herdr pane get <pane>` → agent detected? (agent_status/agent_session
       present). If NO agent → the pi is dead:
       - Log the death to `_bmad-output/watchman.log`: timestamp, pane,
         last-known session file path, and that file's last-modified
         (the diagnosis trail for learning the kill cause).
       - Relaunch with the CORRECT env per target:
         silas: `herdr pane run <pane> "env -u PI_GRU PI_SILAS=1 pi"`
         gru:   `herdr pane run <pane> "env -u PI_SILAS PI_GRU=1 pi"`
         (then the standard sleep-10 + agent-wait + sleep-3 + handover
         chain, per the dispatch gotchas; handover text = "Read the
         playbook section <Silas (COO) / Gru standing orders> and run your
         startup checklist").
       - Fire a macOS notification: `osascript -e 'display notification
         "<body>" with title "Night watchman"'` — body names target +
         action, so the user wakes/sits to a REPORT, not a corpse.
   - Quiet pass (all alive) → single log line `alive` (keeps the hourly
     heartbeat question answerable from the log).
   - Idempotent + safe: if an agent IS detected, NEVER type into the pane.
2. launchd agent: `~/Library/LaunchAgents/com.moses.code.night-watchman.plist`
   — StartInterval 300 (5 min), RunsAtLoad, logs to
   `_bmad-output/watchman.log` (append). Install: `launchctl bootstrap
   gui/$(id -u)` + `kickstart` to verify.
3. README section in `docs/` (short): what it watches, how to disable
   (`launchctl bootout`), how to read the log.

## Acceptance

- `bin/night-watchman --once` with both pis alive: exit 0, `alive` log line,
  zero pane keystrokes (prove: run twice, no duplicate sessions spawned).
- KILL TEST (the real gate): with Silas's pi deliberately killed (coordinate
  with Gru/Silas for a safe window — NOT during in-flight ops), one
  `--once` pass: death logged with session trail, relaunch chain runs,
  Silas's pi returns with PI_SILAS=1 (verify session file + startup
  checklist handover), macOS notification fires.
- `launchctl list | grep night-watchman` shows it loaded; next tick logs.
- Gru pane relaunch path code-reviewed but NOT kill-tested (Gru is live
  mid-session; correctness by symmetry + the env-mirror test in the script).

## Constraints

- Orchestrator-root repo: worktree job ALWAYS (standing exception), PR to
  main, user merges.
- Do not touch `.pi/extensions/*` (no sensor changes); this is additive.
- `herdr pane run` chain discipline applies (sleep 10 before agent-wait,
  sleep 3 after idle, verify handover landed — the 08-19 0.8.0 gotchas).

## Skills policy

- Workflow: `bmad-build` (ops/infra build, self-contained).

## Model policy

- `deepseek/deepseek-v4-flash` + `--thinking max`.

## Dispatch parameters

- repo: orchestrator root (/Users/moses/code)
- repo_root: /Users/moses/code
- slug: night-watchman
- base: main
- model: deepseek/deepseek-v4-flash + thinking max
- pr_review: 0 (ops-tooling scope)
