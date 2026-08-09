Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Round-2 specific: the fold-in is deliberately small (one allowlist line, three tests). Do not re-litigate the r1 architecture warnings (W2 copy-paste, N1 refetch-dup) — those are tracked deferred follow-ups. Assess only whether the fold-in itself fits.
