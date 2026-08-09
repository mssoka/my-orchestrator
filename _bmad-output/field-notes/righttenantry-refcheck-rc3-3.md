# Field notes — righttenantry-refcheck-rc3-3

- `make format` between edit batches REFLOWS long string constants — an `edit` oldText captured pre-format silently mismatches post-format (bit me twice; grep the current shape before re-firing, the dream-2026-08-03 atomicity note's sibling).
- Lustre SSR: `attribute.for` (not `for_`), bare `attribute("k","v")` needs `import lustre/attribute.{attribute}` (module+value namespaces share the name), and local type constructors shadow same-named imports in case patterns (my `TokenState.Completed` shadowed `reference_call.Completed` — qualify in patterns).
- jsonb `||` merge never deletes keys — conditional answers (x only when y) must be explicitly nulled on the non-y branch or stale values survive re-saves; and a remint-then-send flow needs a rollback path when every send fails, or the success page lies while the old link is already dead.
