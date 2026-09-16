# PP3D dock close-out correction — local main never advanced

## User defect and verified cause

User: "i just tried playing in main. i dont see the latest dock changes in main".

Gru's read-only checks establish:
- Actual `/Users/moses/code/packet-plumber-3d` branch main/HEAD = `19aae6a135281a45ce5260cc6865a3c4a34d05d7` (through PR32).
- Local origin/main AND GitHub PR33 mergeCommit = `39d82d0632ca2b0b1b4bd190a089e0f5444e20aa`.
- `git status` reports main behind12. PR33 head = `2f4d2324c5ca3c48a08db826d83ecdecf7166cc6`.
- Local dirt: modified `_bmad-output/implementation-artifacts/deferred-work.md`; untracked `spec-gh-31-lighthouse-staging-fix.md` and `captures/l1-*.png` (exact status must be freshly read before mutation).

The merged change is absent from the user's local main. This is a close-out/base-sync failure, not established editor-cache or implementation failure. Earlier 'closed out' relay omitted this fact. Correct that record. Do not create a speculative code-fix job or repeat an already-completed PR close-out.

## Silas-owned recovery, authorized now

Continue the SAME `packet-plumber-3d-inventory-dock` close-out record. This is local version-control/preservation recovery, not a new minion or code implementation task.

1. Freshly check exact checkout/HEAD/dirt and user game/editor/process state. Do not interrupt a live user process, change another worktree, recreate/delete the already-swept dock tree or alter the constellation-v2 checkout. A genuine live-file safety conflict is the only reason to hold; report it precisely.
2. Preserve all locally modified/untracked potentially colliding files OUTSIDE the repo in a named recovery directory with original relative paths, hashes and manifest BEFORE moving/restoring any of them. Preserve the full original deferred-work document and capture bytes; never blanket-clean/reset/delete or drop a stash. Compare against incoming tracked paths so harmless unrelated files need not move.
3. Safely fast-forward the actual checked-out **main working tree**, not just fetch origin or update a ref. Preserve-first aside handling of the identified doc/capture collisions is authorized. Leave differing originals safely archived with their paths; never assume old deferred-work notes or captures equal/supersede the merged versions. Restore nonconflicting local content where safe. Do not silently overwrite incoming source or union conflicting docs; retain originals and disclose any semantic reconciliation still owed.
4. Prove actual working-tree HEAD includes PR33's real mergeCommit and head by commit containment AFTER sync. Confirm tracked dock implementation files in the user's checkout agree with the shipped version and report any remaining relevant dirty source. This is a source-sync verification, NOT a game-play or native-test PASS.
5. Relay promptly: actual local HEAD, contains33=true, preserved-local-work path, and whether a fresh user launch is ready. If sync cannot safely complete, report exact blocker and leave all content preserved. A remote merge is not completion of this recovery.

No Godot import/run/test/capture, editor-cache removal, native grant, code change, PR/merge, branch force-update, or unrelated root policy work authorized here. After successful sync the user can launch main again; merged-head play-check remains theirs. Other already-authorized jobs proceed independently.

## Dispatch parameters / skills

- owner: existing Silas COO, operations-only recovery; no minion/worktree bootstrap
- job_id: packet-plumber-3d-inventory-dock (existing canonical close-out; append correction, not phantom row)
- repo: packet-plumber-3d
- repo_root: /Users/moses/code/packet-plumber-3d
- base: main
- model: existing Silas `openai-codex/gpt-5.6-luna` / xhigh
- pr_review: unchanged; PR33 already merged, no new review/PR
- Skills: `herdr` for exact live-user coordination if necessary; no bmad-build for this version-control-only recording/sync recovery. If source divergence becomes a real code defect, stop and route a separately scoped `gds-investigate` / `bmad-build` task rather than changing code here.

Keep routine preservation receipts in the existing row. User milestone is their actual updated checkout, not another cleanup receipt.
