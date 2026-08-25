# Field notes — packet-plumber-ue-bootstrap (2026-08-20)

- No UE on the machine → the dual-runner spine design (UE-header-free
  headers + standalone `tests/spine_check.cpp`) proved the ODN-9/11 port
  byte-exact against the Odin vectors BEFORE any engine install; engine-
  gated CI gates SKIP-with-reason, never false-green.
- `npx -y ue-mcp <uproject>` boots engine-free (27 tools + the Epic 5.8
  registry snapshot) — repo-root `.mcp.json` (stdio) is the wiring that
  works with pi today; the official Unreal MCP server needs the editor
  running (loopback HTTP :8000).
- UE module API surface (BuildSettingsVersion, EAutomationTestFlags names,
  commandlet run-name == class minus U) is unverifiable without the
  installed engine — flagged in AGENTS.md; re-verify before trusting a
  green engine build.
