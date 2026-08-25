# Briefing — packet-plumber-v2-5.5-demolish-input (story 5.5 — demolish input surface)

- **Job id:** `packet-plumber-v2-5.5-demolish-input`
- **Repo:** packet-plumber · **Base:** `v2` @ post-#57 merge head (Silas resolves the
  exact sha at dispatch; merge recorded @ e07265b) · **Slug:** `v2-5.5-demolish-input`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (gameplay + canon surface — ODN-12 input contract).
  **Loop ruling (user, 2026-08-17, "keep going"):** rounds run UNTIL APPROVED — the
  cap-3 human-takeover is lifted for this job exactly as it was for 5.4 (each round:
  fix-audit on the fresh stable sha, prior_findings carried).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.5-demolish-input <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 5.5
  (relative to `/Users/moses/code/packet-plumber`). Read it + `sprint-plan-v2.md` §5.5
  row BEFORE designing.
- **CI:** GitHub Actions is org-billing-blocked (runner never starts) — note-only per
  the 2026-08-16 ruling; the LOCAL suite is ground truth. `tools/ci-local.sh` (9
  gates) must pass; keep it green.

## Mission — implement story 5.5 (demolish input surface, restore from prototype)

**The goal:** the demolish MECHANIC (2.3 — `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node`,
core-built + tested, merged #27) finally REACHABLE from the input surface:
click-select a pipe or junction on every left release, see a demolish popover + the
X/DEL key, and watch the topology respond (bundle shrink, atomic junction batch). The
missing third step of 3.5's launchable ("place routers, connect them, demolish and
redesign").

**Current state (investigate first, don't reinvent):**

- 5.4 (#57, just merged) shipped the **intent layer** (`app/input`) — raw device
  events → Intent → validated Command, with the release-based click-select surface
  (node → pipe → clear, on EVERY left release) preserved through it. The demolish
  surface MUST ride the intent layer: a demolish intent reachable from mouse (click
  + popover button / X/DEL), touch (tap-select → popover), and controller
  (select → confirm) — parity by construction `[FORGE #6]`, no per-device command
  production.
- The shared `input.popover_demolish_hit` helper already exists (5.4 factored it;
  `app/input/exec.odin` + the parity harness delegate to it) — 5.5 makes its positive
  path real and pinned (see fold W1-r4 below).
- The prototype is the interaction reference (select → demolish popover + X/DEL);
  its "refund banked" copy does NOT apply (no economy yet).

**Hard requirements (all pinned by the card):**

1. **Select → demolish affordance.** On every left release the click-select surface
   resolves node → pipe → clear; a selected pipe/junction shows the demolish popover
   and X/DEL is live. Demolish is DISABLED while placing (no collision with the 1/2
   lane keys, the right-click dial, or placement mode).
2. **Existing commands only.** Popover button / X/DEL submits the EXISTING
   `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` through the validated edit fast-path +
   action log. **No new command kinds, no `LOG_VERSION` bump**; replay byte-identical
   `[E10]` (prove it in the PR body).
3. **Topology response.** Pipe demolish shrinks its bundle gracefully — traffic
   continues, only full-bundle-loss drops the route `[E1]`. Junction demolish runs
   the atomic batch: incident pipes in edge-id order, then the vertex `[E27]`.
   Terminals NEVER show a demolish affordance (`.Terminal_Demolish` mirrored in the
   UI) `[E2]`. Rejects surface the existing error strings `[E29]`.
4. **Goldens.** New T1 + T2 of pipe-demolish under a bundle (capacity shrink) and
   T1 + T2 of the junction-demolish batch (the E27 batch ORDER is pinned by the
   core's 2.3 tests — the golden pins the batch end state). Existing goldens MUST NOT
   shift — this is an app-layer-only change.
5. **No economy.** No refund, no inventory, no refund copy anywhere (refunds land
   with the economy story).

**Fold-ins from 5.4's Perkins trail (in scope, named by r4):**

- **W1-r4 (positive demolish pins — 4-lens agreement):** the shared
  `popover_demolish_hit`'s positive demolish path never executes in any scripted
  scenario today (`harness/parity.odin:813-816` + `app/input/exec.odin:437-475`).
  5.5 builds that path — pin it: positive-pin scenarios for junction demolish-button
  press → `Cmd_Demolish_Node`, and the pipe twin → `Cmd_Demolish_Pipe`.
- **r3-N7:** the input-parity CLI arg-validation leg is untested — add the pin while
  you're in the harness.
- **Carried 10W/11N (+2 accepted-standing) from 5.4 r1–r4:** stay tracked (Perkins
  carries them forward); fold opportunistically ONLY where they touch the demolish
  surface — never as new scope.

**Acceptance:**

1. Card's Given/When/Then verified; edge contracts `[E1]` `[E2]` `[E10]` `[E27]`
   `[E29]` held.
2. New T1+T2 goldens (pipe-demolish bundle shrink; junction atomic batch); existing
   suite unshifted; full local suite green (`tools/ci-local.sh` 9/9).
3. PR body carries: the demolish intent shape (device → Intent → Command for all
   three devices), the no-new-command-kinds / no-LOG_VERSION proof, the replay
   byte-identical proof, citations `[ODN-12]` / `[FORGE #6]` / the E-contracts.
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** demolish input surface ONLY. No new mechanics, no economy/refunds,
no balance changes, no rendering overhaul beyond the popover/affordance, no core
changes (the 2.3 core is already built + tested — you are wiring, not rebuilding).
No GDD/canon changes unless a surface decision forces a one-line decision-log note.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.5-demolish-input
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
