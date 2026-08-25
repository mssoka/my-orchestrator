# packet-plumber-v2-noc-player-toggle (2026-08-23)

- bmad-build is UNUSABLE on packet-plumber: `_bmad/scripts/` has NO render_skill.py (only memlog.py/resolve_*.py) — skill waived per Silas ruling 08-21; the briefing was self-contained; carry the waiver as a canon note in the PR body.
- Edit-tool batches: an em-dash in oldText can silently fail the WHOLE batch (atomic reject, "edits[N] not found" while the block is verifiably present) — use minimal ASCII-only anchors, or a python replace for em-dash-heavy regions.
- The harness `overlay-check` verb's ms arg needs the `ms` suffix (`parse_ms` requires it): `harness-debug overlay-check surge 3000ms`, not `3000` — a bare number falls to usage().

- Rebase fold (post-r2): when a sibling PR (camera) adds a settings row at the SAME index you did, the merge keeps BOTH — your row moves up (PULLBACK=4, NOC=5, SETTINGS_ROW_COUNT 6) and the W2 nav pin must be re-pointed to the new depth. Also: a sibling's PP_DEBUG compile gate around a runtime feature (effect_overlay / wheel scroll) is OBSOLETE once you ungate the feature — ungate their gate too (a PP_DEBUG-only scroll body dead-zones the wheel in every normal build) and update THEIR test that pinned the old two-build behavior (the B2 release-leg premise "release can't have the overlay" dies with the runtime gate).
