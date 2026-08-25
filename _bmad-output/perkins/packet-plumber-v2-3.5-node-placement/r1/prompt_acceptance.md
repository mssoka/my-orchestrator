Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

CRITICAL LENS-GUARDS (from the briefing — treat as canon):
- Terminals are NEVER player-placed (story 5.1): routers are NEVER director-spawned. A path that player-places a terminal, or lets the director spawn a router = blocker.
- Replay determinism [E10] + LOG_VERSION 2→3 re-bless: exactly the version byte changed in old goldens; old v2 logs reject cleanly. A silent re-bless of golden content = blocker.
- ZERO catalog changes claimed (cat.hash fold). Any catalog touch = finding unless deliberate + golden-accounted.
- Validation: span + 7-tile min-separation + no overlap + placement area; rejections use Edit_Error style. A validation hole = blocker.
- Port limits on draws: basic 4 / mid 8 / high 16 from catalog port_capacity; .Router_Ports_Full when exceeded. A draw ignoring port capacity = defect.
- Edit fast-path [ODN-2]: command flows through Command_Bus.validate → apply. A bypass = blocker.
- NO INVENTORY/ECONOMY — do NOT flag "placement is free".
- The prototype is reference-only. Do NOT flag missing prototype commands (draw/upgrade/demolish/lane-weights/pipe-priority/junction-triage) — 3.5 ports ONLY the PLACE command.
- Em-dashes are FINE in Packet-Plumber copy.
- Story 3.5 acceptance: tray renders + arms placement, click drops validated junction, ESC cancels, placed routers accept drag-drawn pipes; Cmd_Place_Router serializes + replays byte-identical; all existing suites green; no code changes outside placement + tests/render; terminals never placable.
