# Lens brief: codebase fit (source value: `codebase`)

First read the shared review brief at
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/shared-block.md`
and follow it exactly (inputs, spec, output contract, accuracy mandate).

Your assigned source value is `codebase`. Write your findings JSON array to:
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/codebase.json`

## Your lens (from the code-review skill)

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

**Calibration for this docs-only PR:** verify the diff's repo-facing claims against the
worktree — e.g. paths it references (`_bmad-output/planning-artifacts/...`,
`RightTenantryAgents`, scoring-pipeline files), the frontmatter `inputDocuments` entry
`research/technical-ai-voice-reference-calling-research-2026-03-28.md`, file naming vs
the briefing's conventional path, internal cross-references between the 10 new files
(e.g. links from the main report to heist-535 thread docs), and whether the new files
land in locations the repo's conventions expect. Check `_bmad/bmm/config.yaml`
`planning_artifacts` resolution if the report claims to follow it.
