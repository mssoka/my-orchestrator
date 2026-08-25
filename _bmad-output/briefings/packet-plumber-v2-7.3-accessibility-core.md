# Briefing — packet-plumber-v2-7.3-accessibility-core (slice 7: the a11y floor)

- **Job id:** `packet-plumber-v2-7.3-accessibility-core`
- **Repo:** packet-plumber · **Base:** `v2` @ post-wire-aesthetics merge head
  (HELD — Silas resolves the exact sha at release) · **Slug:**
  `v2-7.3-accessibility-core`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-wire-aesthetics` merge close-out (both are view-lane; the
  wire canon must land first so a11y modes style the FINAL wire rendering,
  not a moving target). Record the hold on the row (`blocked_by`).
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `gds-quick-dev` (view+settings work);
  `project-context.md` for code conduct. `lavish` NOT required — a11y modes
  are conformance work against the stories-v2 contracts (palettes are
  simulator-grade, not aesthetic choices); cite golden evidence in the PR.
- **Perkins:** `pr_review: 1` (every-frame view surface + palette canon). **Loop
  ruling (user, 2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-7.3-accessibility-core <url>` yourself.
- **CANON CONTEXT:** stories-v2 §Story 7.3; GDD E9.1–E9.3; ODN-1
  (view-reads-snapshot, never-color-alone); the 7.1 light-canvas canon +
  palette table (data/palette.json, the palcheck oracle); the landed
  background-maps water/coast/park tokens + wire-aesthetics ribbon canon
  (a11y palettes must restyle ALL of it); 5.4 input parity (full parity holds
  under every a11y mode); 7.2 audio juice (the caption targets).
- **CI:** `tools/ci-local.sh` (10 gates incl. palcheck) is the merge ground
  truth.

## Mission — implement accessibility core (colorblind, reduced-motion, scaling + captions)

**Goal (stories-v2 7.3, verbatim intent):** colorblind-safe
(Deuteranopia/Protanopia/Tritanopia palettes; icon+shape for packets,
icon+outline for node states), reduced-motion (disable flash/shake; crises
stay readable), scaling + captions. Every state/machine readable WITHOUT
color; reduced-motion disables flagged effects AND crises stay readable;
UI/gauge scaling works; all audio alerts captioned; full input parity holds.

**Deliverables:**

1. Three colorblind palettes as first-class palette-table entries (the
   palcheck oracle covers them — extend it); every state/machine carries a
   non-color channel: icon+shape for packet types, icon+outline for node
   states (never-color-alone [ODN-1] becomes testable, not aspirational).
2. Reduced-motion mode: flagged effects (flash/shake/spray) disable; crisis
   telegraphy survives via static alternatives (crisis readability contract).
   View-only — sim untouched [ODN-1].
3. UI/gauge scaling (the settings knob; chrome stays legible at each step) +
  captions for every 7.2 audio alert (the caption strip + timing).
4. Settings persistence + the a11y settings surface (mode switches land in
   the existing settings panel canon).
5. Golden: T2 under each a11y mode (colorblind ×3, reduced-motion, scaled) —
   deliberate re-bless with cause-documented chains (the background-maps
   pattern); T1/replay byte-identical (a11y is pure View [ODN-1] — prove it).
6. **Canon fold:** mark §Story 7.3 `Status: implemented` in stories-v2.md
   (same-PR edit) + note the slice-7 exit = FUN-TEST GATE now unblocked
   pending 6.x.

**Acceptance:**

1. GWT from stories-v2 7.3 demonstrably green; never-color-alone + crisis
   readability + captions tested per mode; input parity holds under every
   mode.
2. `tools/ci-local.sh` 10/10 (palcheck extended over the new palettes); T1 +
   replay byte-identical; T2 re-blesses cause-documented.
3. PR body: palette tables, the non-color channel inventory (state →
   icon/shape/outline), caption coverage list, citations (ODN-1, stories-v2
   7.3, GDD E9).

**Scope guard:** the a11y FLOOR only. No new difficulty options, no remapping
UI, no localization — name them as follow-ups. Sim is untouched: if a change
wants to touch a snapshot field or LOG_VERSION, STOP — that's a red flag
(a11y is View-only), flag it in the PR.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-7.3-accessibility-core
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
