# Briefing: pp3d-stability-sweep-1 — #31 lighthouse crash + #29 environment-blind pin + #23 shutdown leaks

## Context

Three stability/truth chores green-lit together (user, 2026-09-15) while the
transmit-parity lane runs in parallel on its own branch. All three are about
the environment telling the truth: props that stage cleanly, pins that
measure the committed tree, shutdown diagnostics with named owners.

Platform canon: PC + mobile + TV/console equally. Hold regime: glm-5.3 @ max.

## Standing doctrine that governs this work (do not violate)

- NEVER blanket-delete `.import` sidecars — they are load-bearing runtime
  import remaps (the #29 lesson, codified in AGENTS.md): deleting them
  regressed a suite 10 SCRIPT ERRORs + 49 failures historically.
- Environment red ≠ diff red. Pins must measure COMMITTED-tree state, not
  working-tree machine litter.
- Honest attribution over zero-count theater: an engine-side residual leak
  class documented truthfully beats a gamed counter.

## Workstream 1 — #31: lighthouse Nil-transform crash

`props.gd:668` SCRIPT ERROR on every L1 world generation:
`_stage_lighthouse` → `_scene` dereferences `.transform` on Nil because
`pp_lighthouse.glb` references the rider-purged texture
`pp_lighthouse_Water_diffuse.png` as external resource #1 (invalid UID →
text path → absent → Nil).

Fix direction (per issue): restore-or-regenerate the purged lighthouse
texture chain for the glb (or strip the external-resource reference /
embed). AUDIT the other 10 rider-purged orphans for the same .glb
external-reference coupling — fix the class, not the one crash. Receipts in
`pp3d-bounded-run-20260910/` under `_bmad-output/implementation-artifacts/`.

## Workstream 2 — #29: unsatisfiable orphan-texture pin

`tests/test_alive_planet.gd:_orphan_texture_pin` asserts working-tree
`FileAccess.file_exists` on sources OR their `.import` sidecars — but
sidecars are gitignored regenerable churn present in every used checkout.
RED in used environments, GREEN-but-catastrophic if sidecars are deleted.

Fix direction (per issue): measure COMMITTED-tree state (`git ls-files
assets/props` / tracked-manifest check). Pin the SOURCES' absence; tolerate
sidecar presence/absence as environment state. Also file the finding about
ambient worlds depending on sidecar-mediated resolution of purged textures
— if that coupling is real, surface it as a named finding in the PR, do not
paper over it.

## Workstream 3 — #23: shutdown leaks — attribute the owners

73 ObjectDB instances + 61 orphan StringNames at exit, deterministic
population. The read-only investigation casefile is the STARTING EVIDENCE:
`_bmad-output/implementation-artifacts/pp3d-shutdown-investigation-glm-2026-09-09/`
(summary SHA e47db480…, investigation 575532aa…, erratum 700d0c27… — read
the erratum; it corrects overclaims: arithmetic ≠ ownership mapping,
unjoined tracks ≠ independent causes).

Goal: NAME the retaining owners (class/ID → owning code), fix game-side
lifecycles where feasible, and honestly classify any engine-side residual
(RasterizerSceneDummy pages etc.) as documented-not-game-owned. Deliver an
owner-attribution table + before/after diagnostic counts in the PR. No
harmlessness claims beyond what is demonstrated.

## Acceptance

1. One PR vs origin/main (base `main`, pr_review=1). NOTE: the
   transmit-parity lane is in flight on its own branch — keep changes to
   your surfaces (props/assets/tests/shutdown lifecycle), no overlap with
   l1_arpanet.gd transmit/input surfaces; expect a rebase if that lane
   merges first.
2. Suite green with EXPECTED_CHECKS triple; fails-pre-fix discriminators:
   - #29 pin: inject a tracked source file → pin RED; sidecar present OR
     absent in the working tree → pin GREEN (environment-independence is
     the discriminator);
   - #31: lighthouse stages with ZERO SCRIPT ERRORs (capture/boot receipt);
     a regression pin that fails if any .glb references a purged texture;
   - #23: measured diagnostic delta (73/61 baseline → post-fix counts) with
     the owner table; mutation leg = re-introduce one fixed leak → count
     rises (proves the measurement sees what the fix did).
3. Captures/boot entries under the bounded-run grant terms (headless ≤300s
   standard entries; ~900s windowed capture entries with caffeinate -dimsu
   + awake screen; receipt+hash per entry; quiescence; stop-on-surprise;
   extensions = new disclosed grants).
4. No scope creep beyond the three issues. No sidecar deletions. No
   art-direction changes.

## Skills policy

- Workflow: `bmad-quick-dev`.
- Review layers (bmad-build step 04): `bmad-review` (adversarial lens) +
  `bmad-review-edge-case-hunter`.

## Model policy

Hold regime: `zai-coding-cn/glm-5.3` @ max.

## Dispatch parameters

- repo: packet-plumber-3d
- repo_root: /Users/moses/code/packet-plumber-3d
- slug: pp3d-stability-sweep-1
- base: origin/main @ 9b02b46 (post PR #45 merge)
- model: zai-coding-cn/glm-5.3 @ max
- pr_review: 1
- github_issue: 31, 29, 23 (close all three in the PR body)
- PR base branch: main
