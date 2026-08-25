# Perkins r1 — Packet-Plumber PR #98 (resting-home wiring pin)

## Round
- Job id: `packet-plumber-v2-pr97-b1-wiring-pin`
- Round: r1
- PR: https://github.com/solarity-services/Packet-Plumber/pull/98
- Repo: `solarity-services/Packet-Plumber`
- Base: `v2` · Head: `packet-plumber-v2-pr97-b1-wiring-pin` @ `1bec4e3`
- Canonical diff: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr97-b1-wiring-pin/r1/diff.patch`
- Worktree: `/Users/moses/code/packet-plumber` (currently on the head branch)
- Spec/context: original B1 job brief `brief-pr97-b1-wiring-pin-2026-08-25.md`; the A/R/C and verify commands are in that brief.

## Standing orders (Perkins)
You are Perkins. You review; you never fix, push, or merge. Review the canonical
diff bytes in `diff.patch` (and the worktree as needed). Verdict mapping: 0
blockers → APPROVE; 1–3 blockers → CHANGES_REQUESTED; 4+ → CHANGES_REQUESTED with
MAJOR REWORK lead. Report findings with severity (blocker/minor/info). The change
is intentionally small and test-only (adds three wiring-pinning tests); judge it
on those merits — do not invent nitpicks.

## Note for the record
This run executes the perkins-lite lens fan-out (blind adversarial, acceptance,
edge) with a consolidator, in this DSH session. The verdict is posted as the
`perkins-review` app via `/Users/moses/code/bin/perkins-token`.
