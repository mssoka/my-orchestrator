# orchestrator-night-watchman-hardening (2026-08-22)

- launchd PATH class: quota-probe + night-watchman resolve pi/herdr/jq absolutely (PI_BIN env → ~/.local/share/fnm/aliases/default/bin → node-versions newest-first → command -v); a PATH error is NEVER a provider verdict — probe exits 2 with NO regime write, watchman startup FATALs on unresolvable herdr/jq, and a broken probe is logged+notified as TOOL-BROKEN (the 23:38Z misread class).
- Sandbox isolation hooks (NIGHT_WATCHMAN_LOG/STATE_DIR/LOCK_DIR/NOTIFY=0) keep test runs out of the live service's files — the live watchman never skipped a tick during the whole verification (isolated lock matters: --once shares the lock dir).
- Self-test assertions that grep $0 must not contain the literal word they assert (the no-create regex's `kill` flagged itself) — break the literal with a bracket class (kil[l]).
