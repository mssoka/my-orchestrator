# Briefing: finlit-bugfix-event-messages

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: `git@github.com:solarity-services/finlit.git`)
- **Worktree:** this pane's cwd (`bugfix-event-messages` worktree, branch `bugfix-event-messages`, base `origin/main`)
- **Skills policy:** workflow = **gds-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **gds-code-review** or **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start (the Godot/headless lessons are directly relevant); badge-out shard per standing orders.

## Mission

Fix the bugs Moses found playing the merged prototype (PR #2), reproducing and VERIFYING each fix via the headless capture loop (see Method).

### Bug 1 (reported): event/tutor messages fire non-stop

User: "the messages just keep going - on stop." Screenshot evidence (day 41, Rate Hike card displayed): `/Users/moses/Desktop/Screenshot 2026-07-31 at 20.12.55.png`
Pointers: `game/scripts/street.gd` `_run_market_tick()` (~line 134) fires every `FinLitEconomy.TICK_SECONDS`; `_show_tutor_beat` displays the message; `game/scripts/economy.gd` `_draw_event` + the event-chance constant (~lines 10–12). Suspects: event chance effectively 100%, repeated re-show of the same card, message panel stacking/appending instead of replace/auto-dismiss, or tutor beats re-triggering per tick. Diagnose first, then fix the ROOT cause (spec intent: event cards are an occasional chance per 60s tick — check the spec's matrix in `_bmad-output/implementation-artifacts/spec-quick-prototype-finlit-street.md`).

### Bug 2 (Gru's spot, verify): top-bar text washed out

In the same screenshot: "$60 🐕 +$3", the day counter, and "ERA: EARNING · Puddle Place" render white-on-cream, barely readable. Likely missing/wrong font-color override on the top-bar labels. Verify visually via your capture loop and fix.

### Method (the "seeing" loop)

- Build a headless capture rig: run the game with a capture script that boots `scenes/street.tscn`, simulates input/advances ticks (you can drive `_run_market_tick` directly), and saves PNG screenshots (`get_viewport().get_texture().get_image().save_png(...)`) to `game/tests/captures/`. READ those PNGs yourself to confirm the bug, then re-capture to prove the fix.
- Reproduce Bug 1 by simulating multiple consecutive ticks and capturing the message panel each time.
- Known-good gate (from the field notes): `godot --headless --path game --import` then `--quit-after 600`; tests via `--script res://tests/x.gd` with `extends SceneTree` + `_initialize()`. The existing offline suite (163 tests) must stay green — add regression tests for both bugs.
- Captures are test artifacts — gitignore `game/tests/captures/` (do not commit PNGs).

## Acceptance

- Root causes named; both bugs fixed with regression tests; offline suite green + headless run clean; before/after captures in your final message as evidence.
- Commit on `bugfix-event-messages`, push, `gh pr create --base main` titled "fix: event message pacing + top-bar contrast" with **Decisions & rationale**. **Never merge.**
- Moses may relay MORE bugs into this job while you work — if Gru relays additional items, triage them in (or defer with a note if scope balloons).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-bugfix-event-messages working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-bugfix-event-messages in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-bugfix-event-messages <url>`
- On blocked/finished: `herdr notification show "finlit-bugfix-event-messages" --body "<one-line>"`
- Final message: summary, root causes, files changed, PR URL, test evidence, open questions.
