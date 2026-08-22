# Night watchman 🌙

An out-of-pi liveness watchdog for the orchestrator's two long-lived staff
panes (`silas`, `Gru`).

## Why

All the orchestrator's sensors (nefario-watch) live **inside** Silas's pi
session. When that pi dies silently — twice now, 17:59Z reboot and a
~00:38Z silent death on 08-20/21 — the whole machine goes deaf until a
human notices. A dead pi leaves a healthy shell prompt, so **pane existence
proves nothing**. The watchman checks **agent liveness**: herdr's agent
detection **and** the session file's existence on disk **and** the pane's
foreground process (the mid-boot signal).

## What it watches

Every 5 minutes (launchd `StartInterval` 300 + `RunAtLoad`), for each
staff pane resolved **by tab label** (fresh every tick — pane ids churn
across restarts and workspace moves):

| Target | Tab label | Relaunch command |
|---|---|---|
| Silas (COO) | `silas` | `env -u PI_GRU PI_SILAS=1 pi` |
| Gru (CEO) | `Gru` | `env -u PI_SILAS PI_GRU=1 pi --model <k3\|glm-5.3> --thinking max` |

Gru's model is pinned at relaunch time through the **quota probe gate**
(`bin/quota-probe`): `kimi-coding/k3` primary, `zai-coding-cn/glm-5.3`
fallback. **Never** `deepseek-v4-pro` (cost-ban) and **never** flash
(reasoning tier) — if both probe DOWN the watchman notifies and does NOT
relaunch rather than boot a wrong-tier Gru.

## Safety invariants (hardened 2026-08-21 after the first live day)

1. **No kill path.** The watchman never signals agent processes — the
   only `kill` in the script is `kill -0` (the lockfile liveness probe).
   `--self-test` asserts this statically (any `kill` that is not
   `kill -0`, and any `pane close`/`pane kill`, fails the assertion).
   Kill tests are human-run.
2. **Never creates or splits panes.** It types only into the pane already
   inside the identity tab. Identity tab missing, or holding ≠1 pane
   (a stray split) → macOS notification + STOP. It never guesses which
   pane is "the" pane.
3. **Never types into a possibly-live pi.** Liveness is classified
   ALIVE / BOOTING / DEAD: BOOTING (pi process visible, session file not
   yet on disk — the mid-boot window) is life, zero keystrokes. A
   suspected death is confirmed across a **60s grace window** (4 fresh
   re-polls) before any action, and the pane is re-polled immediately
   before the first keystroke (live-agent no-op guard).
4. **Handover verification retries across ticks** (state file in
   `_bmad-output/.night-watchman.state/`) — a pi mid-startup-checklist is
   *pending*, not failed. Escalation only after 3 ticks/15 min (handover
   sent) or 6 ticks/30 min (marker-only, deferred because the pi was busy).
   A herdr flake during the ready-wait reads UNKNOWN and is treated as
   *up* (handover deferred) — never as a failed relaunch (the 09:18
   agent-wait false-failure class).
5. **Absolute binary resolution (launchd PATH fix).** Every external
   invocation runs through resolved absolute paths — `herdr`/`jq`/
   `osascript` in the watchman, `pi` inside `bin/quota-probe`. Resolution
   chain: plist `EnvironmentVariables` (`PI_BIN`/`HERDR_BIN`/`JQ_BIN`) →
   fnm well-known paths (`~/.local/share/fnm/aliases/default/bin`, then
   `node-versions/*/installation/bin` newest-first) → `command -v`.
   `herdr`+`jq` unresolvable = startup FATAL + self-test FAIL (loud).
   A broken probe tool is logged + notified as **TOOL-BROKEN**, never
   misread as providers DOWN (the 23:38Z class: bare `pi` died under
   launchd PATH, the gate saw "ALL reasoning models DOWN", a real Gru
   death went unrelaunched). Startup logs the resolved paths once per
   configuration change.

## On a confirmed death

1. **Logs the trail** — timestamp, pane id, last-known session file path
   and that file's last-modified (the diagnosis trail for the kill cause).
2. **Re-resolves the identity tab** fresh (missing / multi-pane → notify +
   STOP), re-polls the pane (live agent → no-op), then computes the launch
   command (probe gate for Gru).
3. **Relaunches** via the dispatch chain: launch command → sleep 10 →
   ready poll (up to 90s; a busy pi is *up*, the handover is deferred
   rather than typed into a working pane) → sleep 3 → startup-checklist
   handover.
4. **Verifies** the new session file exists, the right env extension fired
   (its marker text), and the handover landed (one `send-keys enter`
   recovers a stuck buffer; unconfirmed → cross-tick retry).
5. **Notifies** via macOS notification — you wake to a report, not a
   corpse. A second notification fires if the relaunch chain fails or a
   persistent anomaly (missing tab, stray split, both providers down)
   requires manual intervention (deduped to once per 30 min per anomaly).

Quiet passes log a single `alive silas gru` line — the heartbeat.

## The log

`_bmad-output/watchman.log` (same file for the script's own lines and
launchd's stdout/stderr — the script writes timestamped lines):

```text
2026-08-21T06:14:08Z alive silas gru          ← heartbeat (quiet pass)
2026-08-21T06:20:03Z DEATH silas pane=w1T:p1Y6
2026-08-21T06:20:03Z   last-session=/Users/moses/.pi/agent/sessions/.../xxx.jsonl last-modified=missing
2026-08-21T06:20:03Z   action: relaunch (env -u PI_GRU PI_SILAS=1 pi)
2026-08-21T06:20:55Z   ready: idle (pi booted)
2026-08-21T06:21:10Z   verified: session=... (env marker + handover landed)
2026-08-21T10:25:36Z   classified BOOTING after grace — boot-race guard: no keystrokes   ← mid-boot, no action
2026-08-21T10:30:35Z warn identity-tab label=Gru holds 2 panes — skipping (never guess)  ← anomaly, notify+stop
2026-08-21T23:59:00Z paths: herdr=... jq=/usr/bin/jq osascript=/usr/bin/osascript probe=... pi=...  ← once per config change
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

The plist carries `PI_BIN` (absolute pi path — the launchd PATH fix).
When updating the script WITHOUT reinstalling the plist, the fnm-path
fallback inside the script resolves `pi` anyway — a script-only deploy
is safe (the loaded plist's env simply stays PI_BIN-less).

Manual run (same logic, no launchd):

```bash
bin/night-watchman --once        # one pass
bin/night-watchman --self-test   # deps + env mirror + safety assertions +
                                 #   model-gate unit tests + live resolution
bin/night-watchman --dry-run     # one pass, never types (probe gate skipped)
```

**Binary resolution & the launchd PATH fix (2026-08-21 23:38Z exposure).**
The watchman and `bin/quota-probe` resolve every external binary through
absolute paths so launchd's minimal PATH can never break them:
`PI_BIN`/`HERDR_BIN`/`JQ_BIN` (plist `EnvironmentVariables`) → fnm
well-known paths → `command -v`. The plist ships `PI_BIN` pointing at
`~/.local/share/fnm/aliases/default/bin/pi`; the fnm fallback covers an
installed plist that predates it, so a script-only update is safe.
`bin/quota-probe --paths` prints the probe's resolution (used by
`--self-test` and the startup log); an unresolvable `pi` exits 2 and
writes NO regime entry — a PATH error is never a provider verdict.
The launchd verification recipe (prove the fix under a REAL launchd
context, without touching the live service):

```bash
# throwaway LaunchAgent running the probe under launchd's env
cat >/tmp/nw-probe-test.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.moses.test.nwprobe</string>
  <key>ProgramArguments</key>
  <array>
    <string>BIN/quota-probe</string>
    <string>kimi-coding/k3</string>
  </array>
  <key>StandardOutPath</key><string>/tmp/nw-probe-launchd.out</string>
  <key>StandardErrorPath</key><string>/tmp/nw-probe-launchd.err</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
  <key>ProcessType</key><string>Background</string>
</dict></plist>
EOF
launchctl bootstrap gui/$(id -u) /tmp/nw-probe-test.plist
launchctl kickstart gui/$(id -u)/com.moses.test.nwprobe
sleep 70   # probe timeout is 60s
cat /tmp/nw-probe-launchd.out   # must be a provider verdict ("OK/DOWN <model>"),
                                # NEVER "env: pi: No such file or directory"
launchctl bootout gui/$(id -u)/com.moses.test.nwprobe
```

The same trick runs `bin/night-watchman --self-test` under launchd
(set `NIGHT_WATCHMAN_LOG`/`NIGHT_WATCHMAN_STATE_DIR` to /tmp paths in the
job's env) — the whole dependency + safety + resolution surface proven
in a launchd-spawned context.

## Simulating the incident classes (sandbox recipe)

The watchman is deliberately testable against a scratch tab — the real
`silas`/`Gru` tabs are never touched. Target records are pipe-form,
6 fields: `label|key|launch-env|handover|env-marker|tier`.

```bash
# scratch tab + a sacrificial pane
herdr tab create --label watchman-sandbox --workspace w1T
T='watchman-sandbox|test|cd /tmp/nw-sandbox &&|Read the playbook section test standing orders and run your startup checklist|run your startup checklist|ops'

# isolated log/state/lock keep sandbox runs out of the live service's
# files (and the lock); NIGHT_WATCHMAN_NOTIFY=0 silences notifications.
S='NIGHT_WATCHMAN_LOG=/tmp/nw-test.log NIGHT_WATCHMAN_STATE_DIR=/tmp/nw-test.state NIGHT_WATCHMAN_LOCK_DIR=/tmp/nw-test.lock NIGHT_WATCHMAN_NOTIFY=0'

# (a) boot-race: start a pass while a pi boot lands mid-grace →
#     "classified BOOTING after grace — boot-race guard: no keystrokes"
NIGHT_WATCHMAN_TARGETS="$T" env $S bin/night-watchman --once &   # pass in bg
herdr pane run <pane> "cd /tmp/nw-sandbox && pi"               # boot lands mid-grace

# (b) real death: kill the sacrificial pi, then one pass →
#     DEATH trail → relaunch into the SAME pane (no split) → ready → verified
NIGHT_WATCHMAN_TARGETS="$T" env $S bin/night-watchman --once

# (c) live-agent no-op: pane has a live pi → single "alive test" line,
#     identical pid + session (zero keystrokes)
NIGHT_WATCHMAN_TARGETS="$T" env $S bin/night-watchman --once

# (d) identity tab missing → warn + notify + no pane created
NIGHT_WATCHMAN_TARGETS='no-such-tab|ghost|env -u PI_GRU PI_SILAS=1|h|m|ops' \
  env $S bin/night-watchman --once

# (d2) stray split: herdr pane split <pane> → pass warns "holds 2 panes",
#      notifies, and types nothing
```

For the model gate: `NIGHT_WATCHMAN_PROBE=<stub>` overrides the probe tool
(`--self-test` uses an internal stub; a live run against the real
`bin/quota-probe` shows today's pin decision, e.g. k3 403 → glm-5.3). A
reasoning-tier test target (`...|reasoning`) + stub pin verifies the
relaunch command carries `--model <k3|glm-5.3> --thinking max`.

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
- The **incident classes are simulated** (sandbox recipe above, 2026-08-21
  hardening job): boot-race grace, real-death relaunch into the correct
  pane (no tab split), live-agent no-op, missing tab + stray split STOPs.
- The **model gate** is unit-tested (k3 → glm-5.3 → abort; never
  v4-pro/flash) and exercised live (k3 403 → glm-5.3 pinned, 10:32Z
  08-21).
- **Kill tests remain human-run** — the watchman has no kill path by
  design (asserted in `--self-test`).
- **Launchd PATH fix verified under a real launchd context** (throwaway
  LaunchAgent + kickstart, 08-22): the probe prints a provider verdict
  under launchd's minimal PATH with and without `PI_BIN`; the self-test
  passes in a launchd-spawned env; the live service was never
  interrupted (isolated log/state/lock for all sandbox runs).
