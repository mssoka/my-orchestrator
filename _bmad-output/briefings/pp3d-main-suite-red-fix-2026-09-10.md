# PP3D — fix execution-RED merged main (suite failures found by the bounded run)

## Intake (from the authorized lane-1 run, 2026-09-10)

The user's bounded-run grant executed the post-merge confirm on main @ 77a09a4: **parse repair WORKS** (no parse error), but the focused suite is RED — 3 failures in ~40s (receipts 4db6d8c1 / a558d5d7 on the row):

1. `SCRIPT ERROR: Invalid type in _distribution` — typed-array argument mismatch, `test_router_legibility.gd:181` chain.
2. `test_tooling_contracts.gd` check-count gate ran **11 expected 13** — checks being eaten; an execution-only defect in the Perkins-r2-fixed gate file (the phantom/eaten-check class — investigate abort/early-return/guard paths swallowing checks; EXPECTED_CHECKS pins must prove every check actually RUNS).
3. Third failure per the receipted log — read the full receipts before fixing.

## Scope

Fix ALL execution-RED failures on merged main so focused + full suites pass green by execution. Root-cause each (no symptom-patching); the eaten-checks fix must carry a mutation/abort leg proving the gate fails when checks vanish. No scope growth, no refactors beyond the failures.

## Verification grant (bounded, Silas administers)

- Up to **3 focused-suite native entries** for convergence + **1 closing full-suite** green run. ≤300s each, headless only, receipted on the row, stop-on-surprise (new diagnostic class, identity drift, cap breach → stop + report, no retries).
- If the focused suite stays red after 3 entries: stop and report — do not burn the full-suite entry on a red base.

## Models / bounds

- glm-5.3 @ max (code-only exemption). No OpenAI, no editor, no GUI launch.
- pr_review=1, focused PR to main, user merges. Perkins round on glm-5.3.
- coordinate_with: constellation-view (pS8) + l1-intro-flow (pS9) — they keep BUILDING; their verification entries stay HELD until main is green (Silas holds lanes 2-3 of the run grant).
- Skills: bmad-build (mandatory gate; ambiguous-short-config halt → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md), gds-quick-dev.

## Dispatch parameters

- job_id: packet-plumber-3d-main-suite-red-fix
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: main-suite-red-fix · base: main (head 77a09a4)
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
