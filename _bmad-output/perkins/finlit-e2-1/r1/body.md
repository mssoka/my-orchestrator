## 🤖 Perkins automated review — round 1 of 3
**Job:** finlit-e2-1 · **Reviewed sha:** `5a9e87c` · **Reviewers:** 7/7 completed
**Verification:** 12/12 findings confirmed against the code — 0 rejected as false-positive, 0 kept as [unverified]

### Blockers (0)

None.

### Warnings (4)

1. **`record()` write-error accounting path never exercised** — `game/scripts/playtest_session.gd:123-127`. The `get_error()` → `_events -= 1` branch (disk full / ejected media) has no test. Inject a failing FileAccess after `begin()` and assert the count excludes the dropped line.
2. **`tutor_open` mode branching (scripted/llm/compare) has no test** — `game/scripts/street.gd:819-824`. The internal review already found and fixed a bug in this exact code; the three branches remain unverified. Open the tutor panel with key unset/set/debug-compare and assert `tutor_open.mode`.
3. **Seven scorecard-row hooks lack any verified coverage** — `buy`/`upgrade`/`repair`/`event`/`league_open`/`new_game`/`street_name_reroll` in `street.gd`. These feed the scorecard's observation rows; no test drives the popups that fire them.
4. **Advisory test gate: CONCERNS** — P0 (AC8 paths) 100%, but P1 sits below the 90% PASS bar for the reasons above. Raising it is the same work as #1–#3.

### Notes (7)

- **Reviewer agreement:** `age_picked` and `street_name` hooks are never exercised — the scene test emits `_age_picked`/`_street_name_picked` signals directly (`test_playtest_session.gd:182,184`), skipping the record handlers in `_on_age_picked` and the accept lambda. Both events are absent from the test log, not merely unasserted. (blind + tests)
- Collision guard compounds suffixes: a 3rd same-second session becomes `X-2-3.jsonl` instead of `X-3.jsonl` (`playtest_session.gd:91-96` — loop rebases off the mutating `target`).
- Scorecard "First wage <60s" row (`docs/playtest-scorecard.md:50`) divides session-wide `elapsed_ms` by 1000; after a 🔄 NEW GAME that yields total session time, not the segment's first-wage time. Row 2 (FIND WORK) already subtracts the segment `boot` — Row 1 should say so too.
- Story Task 2.3 checkbox left `[ ]` though the RerollTapProbe is implemented and verified.
- Story source-tree table says `PlaytestChip` sits under `Root/HUD`; the committed scene puts it at `parent="."` (top-left, outside the HUD row) — stale row from the review round.
- `--playtest-log` override is accepted unsanitized (no `user://` confinement / `..` filter). Safe today — source is the trusted launcher's `OS.get_cmdline_user_args()`. State that assumption in the docstring.
- `_do_repair` re-fetches the asset via `find_asset` (`street.gd:479`) though `repair_asset` already returns `result["asset"]` — diverges from `_do_upgrade` ten lines above.

### Reviewer agreement

- `age_picked`/`street_name` bypass (blind + tests) — see Note 1.

### Verdict

**READY TO MERGE**

Observer-only tooling; zero gameplay change with the flag absent. Both bare-runner invocations green in the round worktree (41 + 56 checks), existing suite unaffected (241), import gate clean, capture-rig seed fix verified against the L1 rental price ($2000). All findings are coverage gaps or doc/tracking nits — none block, all are worth a follow-up sweep before round 2.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
