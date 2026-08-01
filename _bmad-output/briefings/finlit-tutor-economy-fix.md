# Briefing: finlit-tutor-economy-fix

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: `git@github.com:solarity-services/finlit.git`)
- **Worktree:** this pane's cwd (`tutor-economy-fix` worktree, branch `tutor-economy-fix`, base `origin/main`)
- **Skills policy:** workflow = **gds-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **gds-code-review** or **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start (DeepSeek thinking/max_tokens lesson is DIRECTLY relevant); badge-out shard per standing orders.

## Mission

Two fixes for the playtest build, both playtest-blocking:

### Fix 1 — LLM tutor answers truncate mid-sentence

Evidence: `/Users/moses/Desktop/Screenshot 2026-08-01 at 01.24.05.png` — Mrs. K's live answer ends "…smart because it gets your…" mid-word. The parent-reviewable log (`FinLitLlmTutor.LOG_PATH`) should confirm `finish_reason == "length"` — CHECK IT.
Root cause hypothesis (verify): the ~80-word output cap / `max_tokens` is hit mid-sentence even with thinking disabled. Fix properly, not by raising the cap blindly:
1. **Never ship a dangling sentence**: if `finish_reason == "length"`, trim to the last complete sentence boundary before display (log the full raw response in the jsonl log regardless).
2. **Brevity by construction**: tighten the system prompt to a hard shape (e.g. "max 3 short sentences, kid words") sized well under the token cap.
3. Optional: a one-shot "shorter please" retry on `finish_reason == "length"` before falling back to sentence-trim.
Regression test: synthetic `finish_reason=length` response → display ends on a sentence boundary; log keeps the raw.

### Fix 2 — Economy balance: houses fall out of the sky (day-13 mansion, zero debt)

Evidence: same screenshot — day 13, $8,856 cash, $10,043 assets, house bought easily with NO debt. Moses: *"a char just bought a house easily without debt — that's not real life"* — and unrealism kills the teaching goal.
Doctrine (from the locked design — two doors):
- **Wages door** teaches work: income covers living/repairs/events + SLOW saving. Working a shift should feel meaningful but never mansion-buying.
- **OPM door teaches leverage**: big assets (duplex, house, tower) must be ASPIRATIONAL — reachable via weeks of saving OR the trust-gated loan path. A house by day 13 with no debt must be IMPOSSIBLE.
Rebalance per the spec's economy tables + the memlog's two-door doctrine: asset prices up hard (house-class assets an order of magnitude over early wages), wage/shift income tuned so the FIRST cheap asset (Snack Cart class) is a short-session win, but property needs the second door. Check rent/income ratios stay fun (60s tick shouldn't feel punitive). Update the spec's economy tables + any balance notes to match, with rationale.
Regression tests: property unaffordable from wages alone before day N (pick + justify N); Snack Cart affordable early; loan path makes property reachable.

## Acceptance

- Both fixes with root causes named + regression tests; 202+ suite green; headless gate clean; capture evidence (no dangling "…" in the tutor panel; shop prices visibly aspirational) in your final message.
- Commit on `tutor-economy-fix`, push, `gh pr create --base main` titled "fix: LLM truncation guard + economy rebalance (two-door doctrine)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` present; `.env` symlinked — LLM path testable live).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-tutor-economy-fix working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-tutor-economy-fix in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-tutor-economy-fix <url>`
- On blocked/finished: `herdr notification show "finlit-tutor-economy-fix" --body "<one-line>"`
- Final message: summary, root causes, files changed, PR URL, test evidence, open questions.
