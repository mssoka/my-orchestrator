# Briefing — packet-plumber-v2-5.3-pause-anywhere (pause-and-plan)

- **Job id:** `packet-plumber-v2-5.3-pause-anywhere`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-5.3-pause-anywhere`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (canon-surface gameplay code — stepping semantics).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` — sibling jobs (5.5/5.6) may merge while you work; rebase onto origin/v2
  when they do (you share `app/main.odin`).
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will be
  red/not-started until the user fixes it. NOT a code failure. Run the FULL local suite
  green (`odin test`, `harness run`) before opening the PR; Perkins verifies locally.

## Mission — story 5.3 Pause-anywhere (the plan card exists in
`_bmad-output/planning-artifacts/sprints/stories-v2.md` — this story was PLANNED, now
dispatched early by the user's order: he wants pause-and-plan for placing routers and
upgrading links)

**The plan card:** pause freezes the sim deterministically; crises tick only unpaused
(fairness + accessibility — pause-and-plan works, even mid-crisis); the edit fast-path
still applies edits while paused `[ODN-2]`; resume continues from the exact tick.

**Key binding (user ruling):** **`P` OR `SPACE`** toggles pause (regular keys — no
F-keys; the user is a solo dev on a laptop keyboard). Neither must collide with anything
(R restart, T assist, E/S/B lanes, 1/2 class, U preview, X/DEL demolish, ESC cancel are
taken).

**The work (read the architecture's RunController + ODN-2 sections first):**
1. Core: pause freezes STEPPING deterministically — the tick counter does not advance;
   no sim state mutates while paused. Crises tick only unpaused. Resume continues from
   the exact tick (no drift — replay equality must hold through pause/resume cycles).
2. Edits while paused: the validate→apply fast-path `[ODN-2]` still applies edits while
   paused (draw, place, demolish, QoS) — the player plans the network frozen in time.
   This is the heart of pause-and-plan; if the fast-path's apply_tick semantics need a
   small pause-aware adjustment, read ODN-2 and do exactly that, no more.
3. App: `P` toggles pause in Run mode; a clear paused indicator (HUD) — dim/overlay +
   "PAUSED" text; placement/draw/demolish/QoS interactions stay fully usable while
   paused.
4. Goldens: NEW T1 (paused state stable) per the card; existing goldens MUST NOT shift
   (pause is additive — no pause in any existing log). Any old-golden drift = STOP and
   flag.
5. PR body carries the story 5.3 card update (status/moved-up note) in
   `_bmad-output/planning-artifacts/sprints/stories-v2.md` — canon rides the PR.
   **UPDATE: the GDD Controls table amend is ALREADY DONE (commit `5f51236` —
   Pause = P / Space).** Read the canon at start and align — do not re-amend.

**Acceptance:**

1. `P` pauses mid-run: packets freeze, meter frozen, nothing mutates; `P` resumes from
   the exact tick.
2. While paused: draw pipes, place routers, demolish, adjust QoS — all edits land and
   apply (fast-path), visible immediately.
3. Mid-crisis pause: crises tick only unpaused — pausing during a crisis is fair
   (telegraphs stay, no hidden progress).
4. Replay equality: a run with pause/resume + edits replays byte-identical `[E10]`.
5. Full local suite green; goldens per discipline above.
6. Launchable increment in the PR body: pause mid-surge, plan a redesign, resume — the
   plan applies and the surge continues from the exact tick.

**Scope guard:** pause mechanics + indicator only. No speed controls, no save/load, no
other bindings, no telemetry (separate job).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.3-pause-anywhere
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
