# orchestrator-night-watchman-hardening

## Task

Fix the night-watchman's misfire classes observed on its first live day
(2026-08-21), preserving its working core. The service stays LIVE during
the fix (it is ticking clean as of 10:08Z — do not bootout).

## Context (incident 2026-08-21; watchman.log authoritative, all UTC)

- 09:16:20 FALSE silas death — liveness check raced a boot (session file
  09:16:21 not yet visible at check time); watchman typed
  `env -u PI_GRU PI_SILAS=1 pi` into a live/booting pane; keystrokes sat
  queued and were delivered as a stray user message ~40 min later. Its
  agent-wait ALSO failed rc=1 at 09:18:01 ("pi did not come up within
  90s") although pi was up — wait-class false failure.
- 09:50–09:54 pane drift + tab splits — relaunch attempts created NEW
  panes (splits of the Gru tab), the watchman then tracked its own split
  (w1T:p2J7) as "gru", and booted bare `pi` (deepseek-v4-flash via
  defaultProvider — wrong tier for Gru).
- 09:52:20 DEATH gru pane=w1T:p2J7 — declared Gru dead based on its own
  split pane's dead pi; the eventual relaunch landed correctly in the
  Gru tab (p1, session 09-54-09Z — the current Gru) but only via
  multiple attempts with collateral panes.
- 09:53:57 FAILED verify (false alarm): "pi up but startup handover
  unconfirmed" — fresh Gru was mid-startup-checklist.
- The REAL Gru death (session 09-13-23, glm-5.3, last write ~09:52Z)
  cause UNKNOWN — crash. NO kill action exists anywhere in watchman.log
  (grep clean) — the kill suspicion is retired; the audit item below
  stands to keep it retired.
- Full narrative: `_bmad-output/silas-journal/2026-08-21.md` (~10:55
  local entry).
- NEW (23:39Z, live exposure): the Gru model-pin probe gate is
  PATH-broken under launchd — `bin/quota-probe` invokes bare `pi`
  (line ~61), launchd's minimal PATH can't resolve it, the probe dies
  with `env: pi: No such file or directory` BEFORE reaching the
  provider, and the gate misreads that as ALL reasoning providers
  DOWN. With k3 billing-capped (403) and glm-5.3 the only live
  reasoning provider, a real Gru death right now = notify-only, NO
  auto-relaunch until this ships.

## Fix scope (all required)

1. **Boot-race guard:** on death detection, re-check after a 30–60s
   grace before declaring death; mid-boot / session-file-pending =
   alive. Also fix the agent-wait false-failure class (rc=1 while pi is
   demonstrably up).
2. **Pane identity:** re-resolve gru/silas panes BY TAB LABEL every
   tick; never cache pane ids across ticks; NEVER create or split panes
   on relaunch — type into the existing identity-tab pane only. Identity
   tab missing entirely → notify + STOP (no split, no new pane).
3. **Live-agent no-op guard:** if the target pane already has a live pi,
   do nothing — zero keystrokes (same hazard class as the 08-06 herdr
   pane-run race).
4. **Model pin on Gru relaunch:** reasoning tier with probe gate —
   `kimi-coding/k3` primary, `zai-coding-cn/glm-5.3` fallback; NEVER
   `deepseek-v4-pro`, NEVER flash. Silas relaunch: `PI_SILAS=1` as today
   (silas.ts auto-sets flash — keep).
5. **Verify hardening:** the startup-handover verify must retry across
   ticks before flagging (mid-checklist ≠ failure).
6. **Kill-path audit:** document and assert there is no kill path (the
   log confirms none today); if any kill code exists, remove it or gate
   it behind explicit user arming. Required before any future kill-test.
7. **Preserve:** `--once`/`--dry-run`/`--self-test` modes, tab-label
   resolution, env-mirror relaunch chains, death-trail log, macOS
   notifications, the clean-tick single-line log format.
8. **launchd PATH fix (the live exposure above):** absolute binary
   resolution for EVERY external invocation — `pi` inside quota-probe,
   any `pi`/`herdr` the watchman itself execs. Resolution chain:
   plist `EnvironmentVariables` (e.g. `PI_BIN`) → well-known fnm path
   → `command -v` fallback. Self-test must FAIL LOUDLY when a
   required binary is unresolvable, and startup must log the resolved
   paths. Verify under a REAL launchd-spawned context (launchctl
   kickstart): the probe's output must be a provider verdict
   ("OK/DOWN <model>"), never a PATH error. Keep interactive use of
   quota-probe working (Silas runs it from a full shell).

## Acceptance

- Self-test + dry-run green.
- PR body shows simulated scenarios: (a) boot-race (session file
  delayed) → classified alive, no relaunch; (b) real death of a
  sacrificial pi → relaunch into the CORRECT existing pane with the
  CORRECT model, no tab split; (c) pane already has a live agent →
  no-op, zero keystrokes; (d) identity tab missing → notify + stop;
  (e) probe executed under a launchd-equivalent minimal PATH →
  provider verdict, not a PATH error (hard fail if any invocation
  degrades to `No such file or directory`).
- No behavior change to the clean-tick path (`alive silas gru` = one
  log line).

## Skills policy

bmad-quick-dev. NOTE: bmad-build render is broken upstream (6.11.0
config token bug — waived on the night-watchman #6 job, 2026-08-21);
this briefing is self-contained, proceed without it if it fails the
same way, and note the waiver in the PR body.

## Model policy

deepseek-v4-flash, thinking max (ops tier). Mega-minions (if any): same.

## Dispatch parameters

- repo: orchestrator root
- repo_root: /Users/moses/code
- slug: orchestrator-night-watchman-hardening
- base: main
- model: deepseek-v4-flash
- worktree: MANDATORY (orchestrator-root exception — always a worktree)
- ledger: row already EXISTS (`orchestrator-night-watchman-hardening`,
  blocked, created 09:58:12Z) — flip it, do not re-add
- pr_review: 0 (ops-tooling scope guard; local verification is the
  merge ground truth per the 2026-08-16 ruling)
