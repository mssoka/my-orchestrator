# PP3D — fix the _stage_lighthouse boot deadlock (issue #31)

## Intake (deterministic evidence, 2026-09-11)

Both capture runs (300s and 900s bounds) hung at the EXACT same `props.gd:668 _stage_lighthouse` point — logs byte-identical at 101 lines. Zero beats, zero captures. Root zone: the `pp_lighthouse.glb` → purged-texture staging chain (the texture was rider-purged in an earlier PR; related import machinery also produced the invalid-UID editor warnings on this same asset). All intro-beat captures are BLOCKED on this. Issue #31 carries it.

## Fix scope

Root-cause the staging deadlock and fix it — per evidence, one of: restore/regenerate the lighthouse texture chain properly, strip/redirect the dead external reference, or make prop staging resilient to purged textures (fail loud and continue, not hang). Consider whether the same class lurks in other purged-texture props (the earlier load-bearing-sidecar finding says these chains are real — do not blanket-delete sidecars again). No scope growth beyond the staging deadlock + its direct class.

## Verification grant (Silas administers)

1. Up to 2 headless boot-probe entries (≤300s each): prove `_stage_lighthouse` completes (or fails loud) where it previously hung.
2. ONE capture re-attempt entry (≤900s, the calibrated bound) — the 13-beat intro captures; success = beats captured.
3. Focused suite stays green (1 entry if needed after the fix). All receipted, stop-on-surprise, no retries beyond the listed entries.

## Models / bounds

- glm-5.3 @ max. No OpenAI, no editor, no GUI. pr_review=1, focused PR to main, user merges.
- Lane-2 (constellation captures) remains released/separate — do not consume its entries here.
- Skills: bmad-build (mandatory gate; ambiguous-short-config → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md), gds-quick-dev.

## Dispatch parameters

- job_id: packet-plumber-3d-lighthouse-staging-fix
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: lighthouse-staging-fix · base: main (current head)
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
