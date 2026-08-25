# Spec context — packet-plumber-v2-5.3-pause-anywhere (Perkins r1)

## §1 The job (original briefing, abridged to review-relevant content)

Repo: packet-plumber (Odin). Base branch `v2`. PR #46. Story 5.3 Pause-anywhere:
pause freezes the sim deterministically; crises tick only unpaused (fairness +
accessibility — pause-and-plan works, even mid-crisis); the edit fast-path still
applies edits while paused `[ODN-2]`; resume continues from the exact tick.

Key binding (user ruling, LOCKED): `P` OR `SPACE` toggles pause (regular keys —
no F-keys). Must not collide with R restart, T assist, E/S/B lanes, 1/2 class,
U preview, X/DEL demolish, ESC cancel.

Work items:
1. Core: pause freezes STEPPING deterministically — tick counter does not
   advance; no sim state mutates while paused. Crises tick only unpaused.
   Resume continues from the exact tick (replay equality must hold through
   pause/resume cycles).
2. Edits while paused: the validate→apply fast-path `[ODN-2]` still applies
   edits while paused (draw, place, demolish, QoS) — the player plans the
   network frozen in time. If apply_tick semantics need a small pause-aware
   adjustment, read ODN-2 and do exactly that, no more.
3. App: `P` toggles pause in Run mode; a clear paused indicator (HUD) —
   dim/overlay + "PAUSED" text; placement/draw/demolish/QoS interactions stay
   fully usable while paused.
4. Goldens: NEW T1 (paused state stable); existing goldens MUST NOT shift
   (pause is additive — no pause in any existing log). Any old-golden drift =
   STOP and flag.
5. PR body carries the story 5.3 card status note; the GDD Controls amend was
   ALREADY done in commit 5f51236 — do not re-amend.

Acceptance:
1. `P` pauses mid-run: packets freeze, meter frozen, nothing mutates; `P`
   resumes from the exact tick.
2. While paused: draw pipes, place routers, demolish, adjust QoS — all edits
   land and apply (fast-path), visible immediately.
3. Mid-crisis pause: crises tick only unpaused — pausing during a crisis is
   fair (telegraphs stay, no hidden progress).
4. Replay equality: a run with pause/resume + edits replays byte-identical
   `[E10]`.
5. Full local suite green; goldens per discipline above. (GitHub CI is
   account-billing-blocked — local suite is ground truth; NOT a defect.)
6. Launchable increment: pause mid-surge, plan a redesign, resume — the plan
   applies and the surge continues from the exact tick.

Scope guard (LOCKED): pause mechanics + indicator ONLY — no speed controls, no
save/load, no other bindings, no telemetry.

## §2 Story 5.3 card (stories-v2.md, canonical)

- Goal. Pause freezes the sim deterministically; crises tick only unpaused
  (fairness + accessibility — pause-and-plan works, even mid-crisis).
- Given the pause control + the run controller; When the player pauses (even
  mid-crisis); Then stepping freezes deterministically (no drift on resume);
  the edit fast-path still applies edits while paused `[ODN-2]`; resume
  continues from the exact tick.
- Edge-case contracts: pause freezes stepping deterministically. Golden: T1
  (paused state stable). Launchable: pause-and-plan works, even mid-crisis.

## §3 Architecture pins in force

- [ODN-1] The core never knows about pause: pause is a DRIVER decision (app /
  harness). The sim only ever steps.
- [ODN-2] Edit fast-path: player edits validate + apply instantly (render
  immediately), and are logged so replay converges at step boundaries.
- [ODN-13] App-layer FSM: Boot/Run/Paused/Game_Over; Paused = same run context,
  stepping stopped.
- [ODN-11] Replay gate: replay must reproduce the recorded hashes exactly;
  replay_error latches loud.
- [ODN-14] Per-tick event stream drains into the hash of the tick that caused it.
- [E10] Replay equality: a run + its log replay byte-identical.

## §4 Lens-guards (LOCKED — do NOT file findings on these)

- KNOWN-LEGIT: the FIRST paused wall-tick hash legitimately differs from the
  last stepped tick's hash (the T1 hash advances one more wall tick into the
  pause window; the stability contract is window-internal — the harness code
  comments state this).
- KNOWN-LEGIT: pause is DRIVER-level (harness/app), never core. A core-side
  pause concept would be a defect; its absence is correct.
- KNOWN-LEGIT: fast-path mid-pause edits render instantly in the app while the
  harness defers application to the first resumed step — two models converging
  at step boundaries is the DOCUMENTED design (the T1 pin freezes the sim; the
  log pins the edits). Do not file this as an inconsistency.
- KNOWN-LEGIT: the app's paused bundle-view rebuild (`bundles_rebuild` on the
  gen guard while Paused) mutates DERIVED state only — documented in the PR
  body ("review r1" item), T1 untouched. Do not file as sim-state mutation.
- LOCKED SCOPE: P/Space binding, no speed controls, no save/load, no
  telemetry, no GDD re-amend. Base = v2 with 5.5/5.6 merged (bcf2f45) —
  carry-forward only, do NOT re-open settled findings from prior stories.
- CI billing-blocked: red/not-started GitHub CI is NOT a finding; the local
  suite is ground truth.

## §5 THE HARD BLOCKER CLASS (what a blocker looks like here)

The determinism spine: the paused window must be ONE repeated T1 hash
(stability-checked in live + replay), resume must continue from the EXACT tick,
and a run with pause/resume + mid-pause edits must replay byte-identical [E10].
Any path where the paused window drifts, resume lands on the wrong tick, or
replay diverges = a blocker. Mid-pause edits must log at paused tick + 1 and
land on the first resumed step — an edit that applies at the wrong tick (or
drops) = a blocker. Existing goldens must NOT shift (additive change) — any
old-golden drift = a blocker.

## §6 Implementer claims (claims to verify, NOT truth)

- 158 core tests green; all 25 harness demos green (24 pre-existing goldens
  unshifted); W1 drift-check 174 mutations all rejected; preview-check 7
  scenarios; lint gates green; odin build app clean.
- pause.dem: pause at 60500ms (tick 1210, mid-crisis after the 1200 surge),
  window 1211–1400 one repeated hash, edit logged at apply_tick 1211, resume
  70000ms → hash moves exactly at 1401.
- Harness hardening (review r1, folded in): parse-time pause/resume validation
  (strict arity + alternation); O(len(pauses)) apply-tick lowering; replay
  stability-violation string uses default allocator.
