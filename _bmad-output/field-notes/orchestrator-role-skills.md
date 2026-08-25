# orchestrator-role-skills (2026-08-22)

- pi extensions load via jiti (`jiti/static` → `createJiti`): the strongest load
  test is importing the real extension files through it; a `pi -e <ext> -p
  --no-session -nt "Reply OK"` boot from a NEUTRAL cwd exercises the full pi load
  path with zero side effects (the extensions' hardcoded-cwd guards short-circuit;
  verify via the session jsonl: only "Reply OK" present).
- The extension discovery glob is `.pi/extensions/*.ts` + `*/index.ts` (no deeper
  recursion, loader.js) — generated helper modules importable from extensions
  belong in a subdir WITHOUT index.ts (e.g. generated/role-blocks.ts).
- jiti/static is ESM-only (its package.json exports map has no "require" arm) —
  from CJS use dynamic import of the absolute lib path, never createRequire.
- Generator emission trick: JSON.stringify/json.dumps double-quoted strings
  (ensure_ascii=False) — backticks/${}/quotes/backslashes become inert; no
  template literal, so the 2026-08-01 ParseError class is impossible. Worst-case
  fixture round-trip test pins it.
