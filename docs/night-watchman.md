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
   `--self-test` asserts this statically. Kill tests are human-run.
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
bin/night-watchman --self-test   # deps + env mirror + safety assertions +
                                 #   model-gate unit tests + live resolution
bin/night-watchman --dry-run     # one pass, never types (probe gate skipped)
```

## Simulating the incident classes (sandbox recipe)

The watchman is deliberately testable against a scratch tab — the real
`silas`/`Gru` tabs are never touched. Target records are pipe-form,
6 fields: `label|key|launch-env|handover|env-marker|tier`.

```bash
# scratch tab + a sacrificial pane
herdr tab create --label watchman-sandbox --workspace w1T
T='watchman-sandbox|test|cd <worktree> &&|Read the playbook section test standing orders and run your startup checklist|Read the playbook section|ops'

# (a) boot-race: start a pass while a pi boot lands mid-grace →
#     "classified BOOTING after grace — boot-race guard: no keystrokes"
NIGHT_WATCHMAN_TARGETS="$T" bin/night-watchman --once &   # pass in bg
herdr pane run <pane> "cd <worktree> && pi"               # boot lands mid-grace

# (b) real death: kill the sacrificial pi, then one pass →
#     DEATH trail → relaunch into the SAME pane (no split) → ready → verified
NIGHT_WATCHMAN_TARGETS="$T" bin/night-watchman --once

# (c) live-agent no-op: pane has a live pi → single "alive test" line,
#     identical pid + session (zero keystrokes)
NIGHT_WATCHMAN_TARGETS="$T" bin/night-watchman --once

# (d) identity tab missing → warn + notify + no pane created
NIGHT_WATCHMAN_TARGETS='no-such-tab|ghost|env -u PI_GRU PI_SILAS=1|h|m|ops' \
  bin/night-watchman --once

# (d2) stray split: herdr pane split <pane> → pass warns "holds 2 panes",
#      notifies, and types nothing
```

For the model gate: `NIGHT_WATCHMAN_PROBE=<stub>` overrides the probe tool
(`--self-test` uses an internal stub; a live run against the real
`bin/quota-probe` shows today's pin decision, e.g. k3 403 → glm-5.3).

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
