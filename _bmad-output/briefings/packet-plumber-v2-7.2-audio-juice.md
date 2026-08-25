# Briefing — packet-plumber-v2-7.2-audio-juice (story 7.2 — audio juice, minimal)

- **Job id:** `packet-plumber-v2-7.2-audio-juice`
- **Repo:** packet-plumber · **Base:** `v2` @ e07265b (post-#57 head; Silas resolves
  the exact sha at dispatch) · **Slug:** `v2-7.2-audio-juice`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (ODN-15 determinism surface + new app module).
  **Loop ruling (user, 2026-08-17, "keep going"):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-7.2-audio-juice <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 7.2
  (relative to `/Users/moses/code/packet-plumber`). Read it + `sprint-plan-v2.md` §7
  row BEFORE designing.
- **Parallel-lane context (don't trip siblings):** 5.5 demolish-input is in flight on
  another worktree (touches `app/input` + the demolish popover draw — NOT audio);
  slice 5B core-flow work follows. Your lane is disjoint: a NEW app audio module +
  two event hooks + captions. If you find yourself editing `app/input/*`, the
  demolish popover, or core flow — STOP, that's the sibling lane.
- **CI:** GitHub Actions is org-billing-blocked — note-only; the LOCAL suite is
  ground truth. `tools/ci-local.sh` (9 gates) must pass; keep it green.

## Mission — implement story 7.2 (audio juice, 1–2 stings)

**The goal:** just-enough audio to prove the concept — a crisis-alert sting and an
arrival click, played through raylib's raudio layer, with variant selection from the
**app-owned cosmetic rng** (determinism-neutral) `[ODN-15]`, and every audio alert
captioned on-screen.

**Hard requirements (all pinned by the card):**

1. **Audio module, app-side.** A new `app/audio` (or the ODN-15-specified home)
   module: init/load/play/teardown through raudio. The core NEVER sees audio; the
   View/app reads snapshot/events and fires audio events. No wall-clock, no
   randomness in the sim path.
2. **Two stings + variant rng.** Crisis alert (hook the 4.2 surge/crisis event) +
   arrival click (packet arrival/absorb event, rate-limited so a busy tick doesn't
   become a buzz — pick a sane, documented throttle). The SFX variant pick draws
   from the **app-owned cosmetic rng ONLY** — never the sim rng `[ODN-15]`. Prove
   determinism-neutrality: the T1 golden asserts audio events don't perturb the sim
   hash (same log → byte-identical replay, audio on or off).
3. **Captions.** Every audio alert is captioned on-screen (the a11y contract — 7.3
   builds the full caption system; you caption YOUR two alerts through whatever the
   current alert/notification surface is).
4. **Asset contract (user-external, do NOT block on assets).** Real audio is
   user-supplied and dropped in later — **SFX (the stings): ElevenLabs;
   music/ambience: SUNO (decided 2026-08-17 — ElevenLabs Music set aside:
   its Studio Games exclusion makes commercial multi-platform game music an
   Enterprise-sales conversation), only IF NEEDED — music/ambience timing is a
   backlog call, not this job (2 stings only)**. Ship the module with **procedurally
   generated placeholder tones** (synthesized waves are fine; raylib can load from
   samples) behind a clean asset-drop contract: documented path + naming + format
   (e.g. `assets/audio/crisis_01.ogg`), loaded from disk when present, placeholder
   fallback when not. raylib loads `.wav` / `.ogg` / `.mp3` directly — NO
   transcoding/ffmpeg step is required in the contract. The PR body documents the
   drop-in procedure + the named sources.
   **ElevenLabs mechanics (researched 2026-08-17):** an API key is available as
   `ELEVENLABS_API_KEY` in the shell env (sourced from ~/.zshrc — present in NEW
   panes; your running pane predates it, and you don't need it: NO fetching in
   this job). If you touch the key at all: read from env ONLY, never write it to
   the repo, logs, PR, or any file. Terms notes for the PR body: (a) paid-plan
   outputs are assigned to the user with perpetual commercial rights, surviving
   subscription end; (b) SFX outputs are SUBLICENSED to other ElevenLabs users
   BY DEFAULT — the "Disable" toggle on the Sound Effects product page opts out
   (flag this to the user when real SFX are generated); (c) MUSIC = SUNO
   (terms verified 2026-08-17): songs made on a Pro/Premier paid plan are
   OWNED by the user with perpetual commercial rights (survive cancellation),
   and commercial use EXPLICITLY includes video games — no games carve-out,
   any-platform. NEVER generate on the free/Basic tier (Suno owns those).
   Suno Studio editing adds the human-authorship layer (the AI-copyright
   mitigation). ElevenLabs Music researched + set aside: all its self-serve
   plans exclude "Studio Games" (commercialized + multi-platform games →
   Enterprise-only).
5. **Existing suite unshifted.** All tests + goldens pass unchanged. New T1
   audio-determinism golden added. Default audio ON for the runnable game, OFF (or
   mock-silent) in the harness — goldens never capture audio state.

**Acceptance:**

1. Card's Given/When/Then verified: crisis fires → sting; arrival → click; variant
   from cosmetic rng only; captions shown.
2. New T1 determinism golden; existing suite unshifted; `tools/ci-local.sh` 9/9.
3. PR body carries: the module shape (home, lifecycle, event wiring), the
   cosmetic-rng proof + citation `[ODN-15]`, the throttle policy, the asset-drop
   contract, the caption surface used.
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** audio juice ONLY — 2 stings, no soundtrack, no ambience, no mixer
UI, no settings page (a compile-time or one-flag volume/mute is enough; full audio
settings are full-game). No core changes, no sim-rng touches, no GDD/canon changes
unless a one-line decision-log note is forced. Do NOT generate or fetch real audio
assets (Suno is user-external).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-7.2-audio-juice
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
