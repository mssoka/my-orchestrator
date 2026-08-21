# Night watchman 🌙

An out-of-pi liveness watchdog for the orchestrator's two long-lived staff
panes (`silas`, `Gru`).

## Why

All the orchestrator's sensors (nefario-watch) live **inside** Silas's pi
session. When that pi dies silently — twice now, 17:59Z reboot and a
~00:38Z silent death on 08-20/21 — the whole machine goes deaf until a
human notices. A dead pi leaves a healthy shell prompt, so **pane existence
proves nothing**. The watchman checks **agent liveness**: herdr's agent
detection **and** the session file's existence on disk.

## What it watches

Every 5 minutes (launchd `StartInterval` 300 + `RunAtLoad`), for each
staff pane resolved **by tab label** (survives pane-id churn):

| Target | Tab label | Relaunch env |
|---|---|---|
| Silas (COO) | `silas` | `env -u PI_GRU PI_SILAS=1 pi` |
| Gru (CEO) | `Gru` | `env -u PI_SILAS PI_GRU=1 pi` |

On a detected death it:

1. **Logs the trail** — timestamp, pane id, last-known session file path
   and that file's last-modified (the diagnosis trail for the kill cause).
2. **Relaunches** via the standard dispatch chain: launch command →
   sleep 10 → `herdr agent wait --until idle` → sleep 3 → handover
   ("read your standing orders, run your startup checklist").
3. **Verifies** the new session file exists, the right env extension fired
   (its marker text), and the handover landed (one `send-keys enter`
   recovers a stuck buffer, then re-verifies).
4. **Notifies** via macOS notification — you wake to a report, not a
   corpse. A second notification fires if the relaunch chain fails.

Quiet passes log a single `alive silas gru` line — the heartbeat. **If an
agent is detected, the watchman never types into the pane** (deaths are
double-confirmed with a fresh `herdr pane get` before any keystroke).

## The log

`_bmad-output/watchman.log` (same file for the script's own lines and
launchd's stdout/stderr — the script writes timestamped lines):

```text
2026-08-21T06:14:08Z alive silas gru          ← heartbeat (quiet pass)
2026-08-21T06:20:03Z DEATH silas pane=w1T:p1Y6
2026-08-21T06:20:03Z   last-session=/Users/moses/.pi/agent/sessions/.../xxx.jsonl last-modified=missing
2026-08-21T06:20:03Z   action: relaunch (env -u PI_GRU PI_SILAS=1 pi)
2026-08-21T06:20:55Z   agent-wait: idle (pi booted)
2026-08-21T06:21:10Z   verified: session=... (env marker + handover landed)
```

The `last-modified` line is the kill-cause trail — a session file whose
mtime is hours old (or missing) at death time points at when the pi
actually stopped.

## Install / reinstall

The canonical copies live in the repo (`bin/night-watchman`,
`bin/com.moses.code.night-watchman.plist`). The plist points at
`/Users/moses/code/bin/night-watchman` — the final merged path.

```bash
cp bin/com.moses.code.night-watchman.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.moses.code.night-watchman.plist
launchctl kickstart gui/$(id -u)/com.moses.code.night-watchman   # force one run now
launchctl list | grep night-watchman
```

Manual run (same logic, no launchd):

```bash
bin/night-watchman --once        # one pass
bin/night-watchman --self-test   # deps + env mirror + live resolution
bin/night-watchman --dry-run     # one pass, never types
```

## Disable

```bash
launchctl bootout gui/$(id -u)/com.moses.code.night-watchman
```

The plist file in `~/Library/LaunchAgents/` remains — it re-registers on
the next login, so `bootout` is a session-scoped stop. To disable
permanently, also remove the plist:

```bash
rm ~/Library/LaunchAgents/com.moses.code.night-watchman.plist
```

## Scope & testing status

- The **alive path** is tested (exit 0, one `alive` line, zero keystrokes;
  run twice with no duplicate sessions).
- The **launchd path** is tested with a throwaway agent under launchd's
  minimal PATH (ran, logged, exit 0).
- The **Silas kill test** (the real gate: kill the pi, watch the death
  log + relaunch chain + notification) is **deliberately gated** — it is
  coordinated with Gru/Silas for a safe window and never self-scheduled.
- The **Gru relaunch path** is not kill-tested (Gru is live mid-session);
  correctness by symmetry + `--self-test`'s env-mirror check.
