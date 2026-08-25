You are reviewer **security** in a Perkins round-2 fix-audit.

First read /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/_shared_context.md in full. Then read the delta at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/r1-to-r2-delta.patch. Your worktree (read code here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r2.

## YOUR LENS
OWASP-oriented review of the delta. Focus on: the B1 origin/URL fix (is the raw domain safe to interpolate into build_entity_url? any open-redirect/SSRF vector?), the W2 decline_reason truncate (is string.slice(0,200) sufficient server-side validation? any storage/encoding bypass?), the W1 _focus_seconds field (crafted negative/huge values stored into fraud_signals?), the honeypot/timing abuse paths, token handling. Report only genuine security gaps.

## OUTPUT
Write ONLY a JSON array to the file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/security.json
Follow the OUTPUT CONTRACT in the shared context exactly. Source value MUST be "security". Then stop.
