# packet-plumber-v2-viscomm-gauge-telegraph (2026-08-25)

- bmad-build WITHOUT render_skill.py: the pre-rendered snapshot at `_bmad/render/bmad-build/packet-plumber-*/` (hash dir) is complete + project-resolved — follow its step files directly (worktree needs `cp -R <repo_root>/_bmad .` first, per the annex bootstrap); carried the waiver canon note in the PR body per the standing Silas ruling.
- Odin proc literals do NOT capture enclosing locals — bitten twice in one job (palcheck render/count closures): write file-level helper procs with explicit params, never inline `proc` values over loop/config locals.
- The health meter's bar FILL + pct draw the darkened `state_*_text` variants (not the raw state colors — the 08-15 contrast audit's ripple); pixel-scan pins must match the text variant or they read 0 px and look like a geometry bug.
