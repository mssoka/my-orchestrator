## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-refcheck-611-panel-persist · **Reviewed sha:** `0b021b0` · **Reviewers:** 7/7 completed
**Verification:** 11/11 findings confirmed against the code — 0 discarded as false-positive, 2 severity-adjusted down on codebase-idiom evidence

### Round-1 fix audit (this round's mandate)

| r1 finding | Status | Evidence |
|---|---|---|
| **B1** save half unpinned | ✅ **fixed** | The pin now drives Save (`simulate.click` on `refcheck-edit-save-landlord_ref` → `UserSavedRefcheckEdit(call.reference_call_id)` → `save_refcheck_edit`) and asserts `saving == True` **plus all three typed values retained**. It bites: a save-path re-key would leave the `rc-1` entry with `saving: False` and fail. |
| **W1** substitute + refetch unexercised | ✅ **fixed** | `refcheck_substitute_trio_keystroke_survives_refetch_test`: Objected row with `can_substitute_referee=True`, empty substitute prefill, dict write under `reference_call_id` via the real input dispatch, then a **reordered** refetch (`rc-2` first) with the typed edit surviving and re-rendering. |
| **W2** name/phone branches untested | ✅ **fixed** | All three field branches typed and asserted; a mistyped field literal hits the `_ -> edit` swallow and fails the test. |
| N1 string-match asserts | carried (note below) | unchanged by design |
| N2 /bug-hunt re-run | ✅ addressed | Live-repro-supersedes is documented in the PR body; the `reference_checks` scenario dir does not exist at this sha, so a formal re-run isn't possible. |
| N3 fail-loud deviation | carried (accepted) | documented, evidence-backed |
| N4 slot-keyed testids | carried (accepted) | testids unchanged per the guard; deferral documented |

**Local ground truth at `0b021b0`** (CI is billing-blocked): `make test-client` → **573 passed, no failures**. `gleam format --check` clean on both touched files. Em-dash and AR-RC13 lints clean. The r1→r2 delta is **test-only** (+166/−5, `client_test.gleam`) — `reference_panel.gleam` is byte-identical to the r1-verified fix, and the −5 lines are assertions absorbed into strictly stronger ones.

### Blockers (0)

None. The load-bearing guard holds: the edit-trio state is keyed by `reference_call_id` at **every** writer (inputs, form-open buttons, update, save, cancel), no slot-keyed path remains, and the stale-save reproduction is now pinned end-to-end through the real runtime path including the save dispatch.

### Warnings (2)

1. **Per-row edit isolation untested** — both pins are single-row; a view regression wiring row B's inputs to row A's `call_id` would pass every existing test. [tests] — follow-up, not this PR.
2. **Mid-save keystrokes silently discarded (pre-existing)** — trio inputs stay editable while `saving=True`; on success the row's `refcheck_edit` entry is deleted, so edits typed during the in-flight save vanish when the form closes. Not introduced by this diff. [edge] — follow-up (disabling inputs while saving would be out of #611's scope guard).

### Notes (8)

1. Pin tests hand-seed `refcheck_edit`; the form-open writers are unexercised by unit tests (verified keyed correctly in the view; matches existing test idiom). [blind, architecture]
2. Save payload asserted indirectly (model state only) — same idiom as every existing save test; effects don't execute under the simulate harness. [blind, tests]
3. Composed type → reordered refetch → Save not pinned in one test; both halves pin the same dict entry, and the refetch handler provably never touches `refcheck_edit`. [edge, codebase]
4. New tests inline the model scaffolding instead of extending `refcheck_detail_model`. [codebase]
5. Advisory test gate: **PASS** — P0 (the #611 chain) 100% pinned including the save half. [tests]
6. *(carried r1 N1)* re-render assertions string-match serialized HTML. [r1]
7. *(carried r1 N4, documented deferral)* trio data-testids stay slot-keyed. [blind, r1]
8. PR body's Verification section is stale after the r2 commit (+78/572 described; actual +239/573). Worth a one-paragraph refresh; not merge-blocking. [perkins]

### Reviewer agreement
Blind + tests agree on the payload-assertion note; blind + architecture agree on the seeded-dict note; edge + codebase agree on the composed-sequence note. All three agreements verified and held at note level.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
