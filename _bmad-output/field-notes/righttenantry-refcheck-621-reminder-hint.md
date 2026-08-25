# righttenantry-refcheck-621-reminder-hint

- The reference_checks bug-hunt scenario suite lives on `origin/rt-refcheck-bughunt2`, NOT develop — copy it in from there for verification runs (untracked, don't commit; matches #616/#618 precedent). The verification-rerun sandbox is still alive: server `rt-refcheck-verification-rerun` on :4100, fixture DB container `rt-refcheck-verification-rerun-dev-db` on 54335 — but :4101 is a stale bug-hunt2 sandbox server (old code); run your own build on a free port.
- The fixture DB has TWO seed generations (a dead one stuck at `submitted` with zero reference_calls) — the dead generation sorts FIRST in the leaderboard (all scores NULL → `created_at ASC`) and silently breaks every scenario; delete it before running.
- agent-browser evals share one global scope: `const row` in a second eval throws "already declared" — wrap every eval in an IIFE `(() => { ... })()`, and `return` at the top level is a SyntaxError (use an expression or IIFE).
