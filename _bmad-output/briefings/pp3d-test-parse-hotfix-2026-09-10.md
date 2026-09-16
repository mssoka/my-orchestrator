# PP3D hotfix — parse error in tests/test_ambient_water.gd on merged main

## Intake

User's Godot editor (4.7.2, post-PR-#22 merge) reports:

```
ERROR: res://tests/test_ambient_water.gd:138 - Parse Error: There is already a for loop iterator named "j" declared in this scope.
```

Verified by Gru on merged main (79a7ba6): line 91 `for j in 12:` and line 138 `for j in 12:` collide in the same function scope (file introduced by c5a4760 during the PR #22 F01 fix; suites were never executed on the post-fix heads — static-verified only, user merged knowingly). The file IS in the suite list (run_tests.gd:40), so the error also breaks any suite run that loads it.

## Fix

Rename the line-138 loop iterator (and its uses in the `var k := side * 26 + j * 2` lines, ~138-141) to a distinct name. Check the rest of the c5a4760-era test files for the same duplicate-iterator pattern statically (editor enumerated only this one, but prove it). No behavior change — this is a parse repair of an already-merged test.

## Bounds

- Code-only, glm-5.3 @ max (quota-hold exemption). No native godot run without separate user authorization (the bounded-run question is still pending with the user — do NOT run godot).
- Static proof: file-scope iterator-uniqueness scan of all touched test files + git diff review. If the user authorizes the bounded headless run mid-flight, the suite pass becomes the verification.
- The pp_*.glb UID warnings the user also saw are OUT of scope (import-cache noise, textures fall back to text paths, cosmetic — noted for a later editor-reimport pass, no action now).

## Dispatch parameters

- job_id: packet-plumber-3d-test-parse-hotfix
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: test-parse-hotfix · base: main
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
- Skills: bmad-build (mandatory gate; ambiguous-short-config halt → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md)
- Focused PR to main; no merge (user merges).
