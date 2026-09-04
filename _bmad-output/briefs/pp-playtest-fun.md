# Briefing: pp-playtest-fun — is it FUN? prove it, then improve it

**Task:** You are a game-feel evaluator for **packet-plumber** (`/Users/moses/code/packet-plumber`). Work IN-REPO (no code changes). Your charter: **play to WIN, repeatedly, with distinct strategies**, score the fun, and file concrete fun-improvement proposals as enhancement issues.

**How to run & drive (USER RULING — golden-harness demos, NO GUI):** you play by **authoring .dem scripts** (timed strategy plans) and running them via `tools/harness.sh run <demo>` (deterministic, software-rendered, captures + event logs). Vocabulary/examples: demos/*.dem — `seed`, `run <ms>` (use LONG windows for full games), `era`, `map dublin`, `box on`, `spawn_node`, `at <ms> draw/place`, `capture at <ms>`, `expect hash`. Read captures with your vision; mine run logs for delivery ratios, crises, fail states. `odin test core` baseline optional.

**The play plan:** ≥4 full runs, each with a named strategy you declare up front: (1) RUSH — expand as fast as possible, (2) GREEDY — hoard/upgrade late, (3) BALANCED — steady growth, (4) your own invention after learning from 1–3. Per run record: survival time, peak network size, first-crisis moment, what killed you (or the win), and a 1–10 fun score for: pacing, tension curve, fairness feel, clarity of cause-and-effect, "one more run" pull.

**Improvement hunting:** the best proposals come from specific moments ("at minute 12 the tension flatlined because…"). For each proposal: the moment, why it deflates or would delight, a concrete change (tunable, not a rewrite), and the expected effect. Prefer 5 sharp proposals over 15 vague ones.

**Issue protocol (as you go):** `gh issue create` — title prefix `[PLAYTEST-FUN] `, label `enhancement` + `playtest` (create the label if missing). Body: the moment/evidence, the proposal, expected effect, your strategy-run context, build sha.

**Acceptance:** ≥4 declared-strategy runs documented; ≥5 fun-improvement enhancement issues filed (or fewer with explicit justification for why the game needs fewer); final report at `docs/playtests/2026-08-31-fun.md` (run table, fun scores, proposal digest with issue URLs).

**Skills policy:** none required.
**Model policy:** `zai-coding-cn/glm-5.3-flash` (multimodal).
**Dispatch parameters:** in-repo main checkout; Silas provides the pane; self-report via `herdr notification show "pp-playtest-fun" --body "..."` (verify `shown:true`).
