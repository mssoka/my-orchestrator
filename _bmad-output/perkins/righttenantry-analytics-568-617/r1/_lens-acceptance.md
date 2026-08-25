# Lens: Acceptance Auditor (source: `acceptance`)

Read your shared context first: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/_shared.md — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `acceptance`. Your output path is: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/acceptance.json

--- YOUR LENS ---
Audit the diff against the spec and context docs (the job briefing + GitHub issues #568 and #617 listed in the shared context). Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Pay special attention to the spec's acceptance list (briefing section "Acceptance"): #617 first-touch populated from the landing URL (or provider=google fallback), cookie short-lived + cleaned up; #568 Meta CAPI fires on OAuth signup insert consent-gated, auto-create paths decided + logged, fire-once contract verified; tests added; scope guard (analytics/attribution ONLY — no OAuth-flow changes beyond the cookie round-trip, no UI changes, no consent-banner changes, no schema changes).
