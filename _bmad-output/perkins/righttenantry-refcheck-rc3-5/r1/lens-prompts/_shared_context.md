# Perkins RC3.5 round-1 review — shared context (non-blind lenses)

You are ONE lens in a parallel code-review team reviewing **PR #600 (RC3.5: the reference-check cadence sweep + Cloud Run Job)** for the RightTenant Gleam/Lustre monorepo. Your output is consolidated with six other lenses; accuracy beats volume. An empty JSON array `[]` is a valid, honest answer.

## Inputs (read these with your tools)
- **Diff (the canonical bytes under review):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/diff.patch` (2818 lines, unified). Review EXACTLY these bytes.
- **Worktree (the reviewed state, for verification reads):** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r1` (detached at sha `cc1b041`). Read actual source here to verify every finding.
- **Spec / context docs:**
  - Round briefing: `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-5-r1.md`
  - Job briefing: `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-5.md`
  - Story spec: `<worktree>/_bmad-output/implementation-artifacts/spec-rc3-5-the-sweep-cadence-engine-cloud-run-job.md`
  - Architecture: `<worktree>/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` — esp. **AD-4** (cadence table, line 238), **AD-14** (guarded updates / sticky terminals / atomic appends, line 508), **AD-15** (security envelope / liveness, line 533), **AD-6** (objection stickiness, line 295), **§4.6** (status↔outcome mapping, line 795), **§8.3** (no-duplicate-terminal notifications, line 1003).
- **Project conventions:** `<worktree>/AGENTS.md` (no JS FFI; no `let assert` in prod; explicit HTTP timeouts; no em-dashes in user-facing copy; Squirrel for SQL; migrations expand-only; brand-voice copy rules).

## The load-bearing invariants for THIS PR (the briefing's lens-guards — do NOT manufacture findings outside these; verify each is actually defended)
1. **EXACTLY-ONCE + idempotent** — re-runs after downtime must NOT double-send (no-duplicate-T0 across a retry is a REQUIRED real test; same for every cadence step).
2. **Guarded atomic update (AD-4/AD-14)** — transition + atomic attempt-append + next-step must be ONE guarded `UPDATE ... WHERE id AND status AND attempt_count=$n` (the rc3-4 objection pattern); a 0-row result = stand down.
3. **Terminal-state respect** — `objected` (sticky), `refused`, `awaiting_correction`, `form_completed`, `unreachable`/`partial`/`failed`/`manual_recorded`/`skipped` must never be re-selected; taken-over rows (`taken_over_at IS NULL` check) skipped entirely.
4. **Cadence math** — T0/T+24/T+48/T+96/T+144 computed from the attempt log (next_attempt_at), offsets correct.
5. **Co-nudge gate (A2)** — fires ONLY when form never opened AND no draft.
6. **Failure path (§4.6, AD-15)** — a row that can't process → `failed` (outcome NULL + terminal_reason), Sentry captures, **NO landlord notification**.
7. **Infra** — Terraform job+scheduler follow the retention/digest house pattern, env-gating matches, manual-fire route is shared-secret protected (not public).
8. **No-op without Twilio keys** — sweep still runs + transitions; SMS just doesn't send (never crashes, never Sentry-captures).
9. **No em-dashes** in user-facing copy (warm-handoff attempt-log render).

## Context note (NOT a finding)
This PR was affected by a known bmad-tooling quirk (work was briefly misdirected to the main checkout, then synced into the worktree; the PR carries the full work). Review the PR's content as-is. Do NOT re-open rc3-4 findings (verified fixed) — carry-forward markers only.

## Output contract — MANDATORY
Write ONLY a JSON array to your output path (given in your lens file). Schema per element:
```json
{
  "source": "<assigned-tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<EXACT lines you READ from the file/diff, pasted verbatim. 'N/A' ONLY when no code reference is possible.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```
- ONLY the JSON array in the file. No prose, no markdown fencing, no preamble. `[]` is valid.
- Do not invent findings to fill a quota. Prefer fewer, well-grounded findings.
- **ACCURACY MANDATE:** every finding will be independently re-verified against the actual source before it reaches the report. Open the file. Read the lines. Quote them verbatim in `evidence`. Hedging ("might"/"could") = you haven't verified it; drop it. A finding without locatable evidence is a hallucination.

When you have written your JSON file and are done, **stop**. Do not attempt fixes; you are read-only.
