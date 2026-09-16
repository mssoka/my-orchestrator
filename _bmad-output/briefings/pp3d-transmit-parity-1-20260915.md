# Briefing: pp3d-transmit-parity-1 — #39 input parity for LOGIN/transmit + IMP→ROUTER label unification

## Context

User green-lit issue #39 after consult (2026-09-15): the last mouse-only
surface in L1 is the TRANSMIT/RETRANSMIT button. Text entry is ALREADY gone
("no typing" flow since earlier work) — do not re-add any typing. The user
likes the button's current location and affordance; the verb behind it
becomes a proper game action. Same consult also ruled the label
unification folded into this heist (same surfaces).

Platform canon: PC + mobile + TV/console EQUALLY (user ruling 2026-09-14).

## Workstream 1 — Transmit as a semantic game action (issue #39)

- **Keep the TRANSMIT/RETRANSMIT button** where it is — it remains the
  touch and mouse affordance.
- **Add ONE semantic confirm/transmit action** behind it:
  - keyboard: a conventional single key (Enter/Space class — pick via
    input-design judgment, show the real binding in prompts);
  - controller: the platform's native confirm/interact via the active
    InputMap mapping conventions — NEVER a hard-coded literal "A"/button
    index; use the mapping/glyph conventions of the active device;
  - touch: the button itself (tap-sized, no soft keyboard, no typed LOGIN).
- **Single-intentional-action protection**: focus changes, held buttons,
  key-repeat, or device switching must NEVER cause accidental/double
  transmission.
- **Controller reachability**: every UI surface in the L1 begin/transmit/
  retry flow is focusable/activatable without a mouse; focus never traps
  the player away from the game.
- **Prompts agree with the active device**: keyboard glyph vs controller
  glyph vs tap wording, updating on device switch; unavailable/disabled
  actions explained.
- **History beats preserved exactly**: the LO-drop, RETRANSMIT beat,
  progression gates — input abstraction must not bypass or alter them.

## Workstream 2 — IMP→ROUTER label unification (user ruling "b. unify")

User quote: "let's use the known terms for the game."

- **Planet-side node labels** become "<SITE> ROUTER" (e.g. "SRI ROUTER",
  "UTAH ROUTER") — scripts/levels/level_manifest.gd builds labels as
  "<SITE> IMP" today (name/label fields around L160-184).
- **Mechanical vocabulary everywhere says "router"**: the dock already
  says ROUTERS; reject hints ("buildings link through their IMP") and any
  prompt/hint that teaches MECHANICS uses router wording.
- **IMP survives ONLY as history flavor**: the guide narration, IMP log
  panel titles ("IMP LOG — UCLA TO SRI"), the LO-drop story text — the
  period narrative keeps its period noun. One story beat may still
  reference the term as history; do NOT delete the history.
- The type ladder (ui_text.gd) is test-frozen — string changes only, no
  size edits; any ladder change is a deliberate re-pin with the test.

## Acceptance (from issue #39, plus house standard)

1. PR vs origin/main (base `main`, pr_review=1). Playable b42 export
   preserved centrally (self-contained Start.command pattern).
2. Complete the L1 begin/LOGIN/transmit/retry flow with KEYBOARD ONLY and
   with CONTROLLER ONLY — no typed strings, no mouse-only control.
3. Runtime-probe-first discriminators (the PR #45 B1 machinery — synthetic
   input probes), each with fails-pre-fix receipts:
   - transmit via the semantic action works; probe fails pre-fix;
   - held/repeat/focus-change produces exactly ONE transmission;
   - controller can focus/activate every flow UI;
   - labels read "<SITE> ROUTER" on planet; IMP absent from mechanical
     prompts, present in history text (grep-pinned both ways).
4. EXPECTED_CHECKS triple; mutation legs RED-then-GREEN; device/touch
   checks DISCLOSED as performed or unverified — never inferred from
   keyboard tests alone.
5. Captures (bounded-run grant terms: headless ≤300s entries, capture
   entries ~900s windowed + caffeinate -dimsu + awake screen, receipt+hash
   per entry, quiescence, stop-on-surprise): transmit flow via keyboard
   and synthetic gamepad; label unification before/after; prompts showing
   per-device glyphs.
6. No changes outside these two workstreams. No port/cert claims.

## Skills policy

- Workflow: `bmad-quick-dev`.
- Review layers (bmad-build step 04): `bmad-review` (adversarial lens) +
  `bmad-review-edge-case-hunter`.

## Model policy

Hold regime: `zai-coding-cn/glm-5.3` @ max. glm-5.3 native vision is fine
for mechanical capture reads; feel/look verdict = user play on b42.

## Dispatch parameters

- repo: packet-plumber-3d
- repo_root: /Users/moses/code/packet-plumber-3d
- slug: pp3d-transmit-parity-1
- base: origin/main @ 9b02b46 (post PR #45 merge)
- model: zai-coding-cn/glm-5.3 @ max
- pr_review: 1
- github_issue: 39
- PR base branch: main
