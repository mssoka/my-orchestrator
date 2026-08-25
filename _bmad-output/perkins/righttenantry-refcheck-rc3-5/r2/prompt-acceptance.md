# Lens: ACCEPTANCE AUDITOR (source: `acceptance`) — Perkins r2 FIX-AUDIT

Audit the fix delta against the spec. Identify:
- Violations of specific acceptance criteria (ACs) or architecture decisions (AD-*)
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC/AD/constraint in `detail` (quote the exact phrase from the spec when possible).

**This is a FIX-AUDIT round.** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/lens-common.md` FIRST — fix-audit scope (B1+W1-W5 verify FIXED), lens-guards (do NOT re-litigate, do NOT re-open rc3-4), legitimate round-2 findings.

Your fix-audit job: confirm each of B1+W1-W5 is actually fixed against the spec (AC7 = DB failure → `failed` + Sentry; AD-15 = fail loudly; AD-4/AD-14 = guarded atomic update; OWNS #7 = manual route pins `sentry_client.Disabled`; §8.3 = warm-handoff is the `reference_unreachable` notification, T+144 silent). Verify the fixes don't violate a spec invariant (exactly-once, terminal-respect, no landlord notification on `failed`). Carry forward still-open Notes N1-N9 (do NOT escalate them).

**Spec files:** `lens-common.md`, the job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-5.md`, the epics `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (story RC3.5), the architecture `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (AD-4/AD-6/AD-14/AD-15, A2, A7, §4.6, §8.3, §9), issue `r2/issue-548.json`. Delta: `r2/delta-r1-r2.patch`. Prior: `r1/consolidated.json`. Verify against worktree `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (read-only).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/acceptance.json` — then stop.
Schema per element:
```
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ from the file, verbatim>",
  "detail": "<≤40 words, quote the AC/AD phrase>",
  "recommended_fix": "<≤40 words>",
  "round2_audit": "<FIXED | STILL OPEN | NEW | CARRIED-N<n> | N/A>"
}
```
ONLY the JSON array in the file. `[]` is valid. Open the file, read the cited lines. A finding without locatable evidence is a hallucination — drop it.
