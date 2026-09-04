# Briefing: pp-playtest-stress — break the game, file the bugs

**Task:** You are a QA stress-tester for the game **packet-plumber** (repo: `/Users/moses/code/packet-plumber`, Odin, Mini-Motorways-like: draw pipes between buildings and routers, route colored packets). Work IN-REPO on the main checkout (you write NO code changes — demo scripts, captures, and issues only). Your charter: **play to BREAK it**, and file a GitHub issue for every bug you find, with reproducible evidence.

**How to run & drive (USER RULING — the golden-harness demo system, NO GUI):** you cannot access a GUI window — you play by **authoring .dem scripts** (timed input plans) and running them through the deterministic software-rendered harness.
- Vocabulary (see demos/*.dem for 52 examples): `seed <n>`, `run <ms>`, `era <n>`, `map dublin`, `box on`, `fixture qos|off`, `spawn_node <type> [x y]` (residential/router_basic/content_host), `at <ms> draw <a> <b> <tier>`, `at <ms> place router_basic <x> <y>`, `capture at <ms>`, `expect hash`.
- Execute: `tools/harness.sh run <your-demo>` (builds the SW shadow itself); read the captures with your vision + the run log (events, delivery ratios, fail states).
- `odin test core` — determinism/fairness contract tests; run once as baseline.
- Recently fixed, regression-hunt it: third-spawn SIGABRT (PR #108, Box arrays ownership). (Your squadmate demo stress_spawn_marathon.dem already soaks it — extend, don't duplicate.)
- A bug with a replayable .dem repro is gold: attach the script path to every issue.

**Hunt list (start here, then go feral):** repeated spawn cycles; router/pipe spam and deletion under load; pause/resize/minimize hammering; save+reload mid-crisis; map flip mid-session; long-idle (30+ min) drift; NOC panel (D) toggling under stress; window edge cases.

**Issue protocol (as you go, never batched):** `gh issue create` in `solarity-services/packet-plumber` — title prefix `[PLAYTEST] `, label `bug` (create label `playtest` via `gh label create playtest` once). Body: repro steps (exact), expected vs actual, severity guess, evidence (screenshot/demo paths), build sha (`git rev-parse HEAD`).

**Acceptance:** ≥3 full play sessions (≥20 min each or to fail state); baseline `odin test core` result recorded; every anomaly either filed as an issue or explicitly noted as non-repro in your final report. Final report at `docs/playtests/2026-08-31-stress.md` (sessions, issues filed with URLs, non-repro notes, your top-3 severity calls).

**Skills policy:** none required (no bmad skill applies — pure adversarial QA craft).
**Model policy:** `zai-coding-cn/glm-5.3-flash` (multimodal — read your own screenshots).
**Dispatch parameters:** in-repo main checkout; Silas provides the pane; you self-report via `herdr notification show "pp-playtest-stress" --body "..."` on completion (verify `shown:true`); ledger row owned by Silas.
