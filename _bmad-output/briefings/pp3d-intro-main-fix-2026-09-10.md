# PP3D — fix merged-intro test failure on main (post-#27 green-confirm)

## Intake (post-#28-merge green-confirm, 2026-09-10)

User merged #27 (intro flow) before #28 per their order; #28 merged pre-verdict on r1-APPROVED substance (safe-merge qualifier recorded). The main full-suite green-confirm FAILED with 3 failures / 0 aborts:

1. Orphan pin (#29) — pre-existing, documented; the confirm gate TOLERATES exactly this one known failure (pin premise disproven; fix rides #29 separately).
2. **Intro test "empty start: pre-installed campus cables hidden" FAILS on merged main** — #27's runtime interaction with the merged world state differs from its branch. THIS is the fix target: root-cause the main-vs-branch difference (world state / merge interaction / load order / scene composition), fix so the intro's empty-start invariant holds on real merged main. No test-weakening: if the test's premise is right, fix the code; if the premise is wrong for merged main, justify and amend the test with evidence.
3. Gate-level tally — expected to clear once #2 is fixed (verify; if the tally independently miscounts, fix per the EXPECTED_CHECKS doctrine).

## Verification grant (small extension, Silas administers)

- ONE focused-suite entry (verify the intro fix) + ONE full-suite confirm re-run. Headless, ≤300s each, receipted on the row, stop-on-surprise.
- Confirm passes when the ONLY failure is the documented #29 orphan pin. Any other failure = red, stop, report.

## Models / bounds

- glm-5.3 @ max. No OpenAI, no editor, no GUI. pr_review=1, focused PR to main, user merges.
- After the confirm passes: lanes 2-3 of the run grant RELEASE (constellation #26 + remaining verification entries).
- Skills: bmad-build (mandatory gate; ambiguous-short-config → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md), gds-quick-dev.

## Dispatch parameters

- job_id: packet-plumber-3d-intro-main-fix
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: intro-main-fix · base: main (post-#28 head)
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
