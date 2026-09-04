# Briefing: packet-plumber-v2-viscomm-shape-vocab

DESIGN-CONVERSATION job (the quinn pattern): read-only on the repo, no
PR, no code changes. You produce evidence, present forks, and IDLE-AWAIT
user rulings in-pane. Direct-to-pane user answers are legitimate; record
every [ADOPTED ruling] verbatim. A watcher alert on this row = an
interactive halt or its settle echo — never continue-nudge.

## Context

- Viscomm design-audit finding D: **7 of 9 packet classes lack a shape
  vocabulary** — packets read as color/motion only; shape does not yet
  carry meaning.
- The affordance theory basis is the Indie Game Clinic video (the lane's
  canon): https://www.youtube.com/watch?v=SV1BBtD3hY4 — esp. the
  crystals example ("what kinda crystals?"): a thing's SHAPE implies its
  function before any tooltip does.
- Timing (why this lane released now): the-box PR #107 lands era
  progression — packet classes become LIVE in play. Shapes must be
  decided before/with classes landing, so the affordance read exists
  when players meet the classes (release trigger: class-landing wave,
  now in review).
- Canon to respect: LOOK-SPEC (scale covenant, zoom-language rungs,
  calm-at-green), the viscomm lane rulings (distinct telegraphs per
  meaning — shapes must not collide with existing signal colors/pulses),
  and the mechanics-quinn record (typed pieces; shape vocab is for
  PACKET classes, a parallel axis).

## Phase 1 — Evidence (read-only)

1. Inventory the 9 packet classes: current visual treatment (shape,
   color, motion) from code + captures; which 7 lack shape vocabulary
   (audit finding D names the gap — re-verify against current v2 HEAD).
2. For each class: its FUNCTION in play (what the player must infer at
   a glance) → the affordance-relevant shape language candidates
   (silhouette class, angle vocabulary, size grammar — geometry FROM the
   renderer, PIL-measured; KYLE-class vision may corroborate, never
   decide).
3. Constraint-check every candidate against the canon above (covenant
   widths, zoom-rung legibility at ACCESS scale, color-collision audit
   vs telegraph hues).

## Phase 2 — The ruling menu (lavish)

Render a per-class proposal menu: each class gets 2-3 shape-vocab
candidates with affordance rationale + look-fit + contact-sheet crops at
all three zoom rungs. User rules per class (adopt / amend / reject).
Serve via lavish (loopback pane if assets 403). Then idle-await.

## Phase 3 — The record

Durable record at
`_bmad-output/implementation-artifacts/packet-plumber-v2-shape-vocab-<date>.md`:
rulings verbatim, rationale, shape-spec per adopted class (geometry
anchors, measurements), open calibration questions, and parked fork
options explicitly fenced out. This becomes the spec input for the
shape-vocab implementation heist (a FOLLOW-UP job — not yours).

## Ops

- No-PR job: on each phase gate (menu served / record closed) run
  `herdr notification show "packet-plumber-v2-viscomm-shape-vocab"
  --body "<one-liner>"` (verify shown:true). Ledger transitions are
  Silas'.
- READ-ONLY on packet-plumber: no commits/edits in the repo; artifacts
  to _bmad-output/. Worktree choice is Silas' (read-only evidence =
  main-checkout-parallel-safe per doctrine).
- bash 3.2 — no arrays. Vision prompts to files; findings from disk.
- The pane STAYS OPEN after the record closes (amendment-ready, the
  quinn precedent).

## Skills policy

- Primary: `bmad-agent-ux-designer` (Sally persona — this is her lane).
- Menu render: `lavish`.

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max (vision INLINE).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-viscomm-shape-vocab
- base: v2 (read-only; resolve fresh head at dispatch)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: none — design conversation, no PR
- release note: trigger fired 2026-08-27 (class-landing wave #107 in
  review); released by Gru per the row's named trigger
