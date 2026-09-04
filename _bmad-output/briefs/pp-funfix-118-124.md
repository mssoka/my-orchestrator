# Briefing: pp-funfix-118-124 — kill the death clock, give health a way back

**Task:** Fix the two fun-killing systems in **packet-plumber** (`/Users/moses/code/packet-plumber`, worktree + branch + PR — this writes code). The playtest squad's evidence base (fun = 3.5/10, substrate 7+) isolated both to the same death-clock/recovery loop:

- **#118** — era-3 arrival starts an ~17s UNWINNABLE death clock: the surge is unreachable. Era-3's demand spike must be *survivable with correct play* — retune the spike's ramp/magnitude/telegraph so a prepared network can ride it (the squad's .dem evidence shows even strong builds die in ~17s).
- **#124** — the health meter is a one-way drain with NO recovery path: every breach is a countdown. Add a recovery mechanic consistent with the game's economy (e.g., health regen on healthy delivery windows / repair action / Box-economy cost — pick the smallest-Change that creates a real recovery loop, and name the choice in the PR).

**Evidence to read FIRST:** `gh issue view 118` and `gh issue view 124` (solarity-services/packet-plumber), the squad's replayable .dem demos cited in the issues, and `docs/playtests/2026-08-31-{stress,fun}.md`. Corroborating context: neweyes #115 (lose state effectively unreachable) — do NOT overcorrect into impossible-to-lose; the tension must live on BOTH sides.

**Acceptance:** (1) era-3 surge is survivable-by-good-play — a new .dem golden (`era3_surge_survivable.dem` or sibling) shows a prepared build riding the era-3 arrival; (2) a real recovery path exists and is demonstrated in a golden; (3) `odin test core` green; `tools/harness.sh` golden corpus re-blessed where behavior intentionally changed (use the sanctioned rlsw pipeline as prior balance changes did); (4) PR opened with the tuning table (before/after numbers) + the new goldens; the PR body notes which knob moved for #118 and which mechanic landed for #124, and explicitly states the lose-state tension is preserved (how #115 is not regressed).

**Skills policy:** bmad-quick-dev.
**Model policy:** `deepseek/deepseek-v4-flash` (ops/coding tier).
**Dispatch parameters:** worktree + branch `packet-plumber-funfix-118-124`, ledger row same name, pr_review=1 (Perkins rides the PR). Fun-retest round is a HELD row behind this fix (Silas holds it via the trigger graph — release on this PR's merge).
