# Field notes — packet-plumber-v2-7.3-accessibility-core (2026-08-19)

- The briefing's `deepseek/deepseek-v4-flash` model line was 402-DEAD at dispatch (playbook 08-19 ruling): the job + the epic-context mega-minion ran on `zai-coding-cn/glm-5.3`; check `PI_MODEL` before trusting a briefing's model (Silas launched me on glm despite the ledger's flash field).
- The `hud()` scaled-int helper is the byte-identity hinge: at ×1.00 `i32(f32(k)*1.0+0.5) == k`, so scaling the capture-visible HUD (health/forecast/banner) through it kept every pre-existing T2 byte-identical — proven by the full suite, never assumed.
- Parity/zero-View traps: `settings_chip_rect` reads `v.palette.mode` — a view without a palette (the parity harness's) SEGFAULTS on the chip rect; every view construction needs a loaded palette. Also: a misplaced `{}` brace + a comment-merged `{` in palcheck took two full debug passes to find — run the brace-depth checker on any file after multi-hunk edits.
