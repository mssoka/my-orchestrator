# Briefing: pp-playtest-neweyes — the blind-first-session clarity audit

**Task:** You are a first-time player of **packet-plumber** (`/Users/moses/code/packet-plumber`). Work IN-REPO (no code changes). Your charter: **play your first session BLIND** — do NOT read the README or docs first — and log every moment of confusion, then file clarity/UX improvement issues.

**Protocol (USER RULING — golden-harness demos, NO GUI):**
1. **Blind session:** WITHOUT reading README/docs/demos, author your first .dem scripts from pure intuition — what would you TYPE to make this game go? Run them (`tools/harness.sh run`), read the captures/logs with your vision. Log every confusion: commands you guessed that failed, outcomes you couldn't explain, systems you never discovered existed, vocabulary you couldn't find.
2. **Doc pass:** NOW read README/docs + skim demos/*.dem for the real vocabulary. Note every "oh, THAT's how it works" — each is a doc-vs-discovery gap.
3. **Second session:** author informed demos (real strategies); note what STILL feels undiscoverable even knowing.

**Issue protocol (as you go):** `gh issue create` — title prefix `[PLAYTEST-UX] `, label `enhancement` + `playtest` (create the label if missing). Body: the confusion moment, what you assumed, what the game actually does, a concrete clarity fix (hint, affordance, label, default, first-run cue), build sha.

**Acceptance:** blind session log (timestamped confusion moments), doc-gap list, informed-session notes, ≥4 clarity issues filed, final report at `docs/playtests/2026-08-31-neweyes.md`.

**Skills policy:** none required.
**Model policy:** `zai-coding-cn/glm-5.3-flash` (multimodal).
**Dispatch parameters:** in-repo main checkout; Silas provides the pane; self-report via `herdr notification show "pp-playtest-neweyes" --body "..."` (verify `shown:true`).
