# Lens brief: architecture (source value: `architecture`)

First read the shared review brief at
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/shared-block.md`
and follow it exactly (inputs, spec, output contract, accuracy mandate).

Your assigned source value is `architecture`. Write your findings JSON array to:
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/architecture.json`

## Your lens (from the code-review skill)

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

**Calibration for this docs-only PR:** the deliverable proposes an architecture (voice
orchestration in `RightTenantryAgents`/ADK, status + transcript display in this repo,
a transcript→structured-reference handoff schema feeding the scoring pipeline). Review
that proposal against the actual conventions and boundaries visible in the worktree
(repo layout, AGENTS.md/CLAUDE.md, existing scoring-pipeline patterns). Also review the
research deliverable's own structure (main report + heist-535 thread docs) against the
bmad-domain-research conventions the briefing mandates.
