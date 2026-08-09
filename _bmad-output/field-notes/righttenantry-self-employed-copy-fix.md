# Field notes — righttenantry-self-employed-copy-fix (2026-08-04)

- The apply-form stepper's Continue is `type=button` + JS validation; `agent-browser click` advanced silently and my re-snapshot read stale state — drive it via `eval` + read `Step N of 8` from `document.body.innerText`, and dump `[required]` controls per visible `.form-section` to find blockers (date inputs need value+input/change events).
- Dev server against a private Docker DB needs NO symlink surgery: tracked `.env.test` (placeholder secrets only) + `ENV=test gleam run`; temporarily repoint its DATABASE_URL port and `git checkout .env.test` after — but it is NOT gitignored, so never let real secrets land in it.
- Copy fix that touches a user-visible phrase: grep `_bmad-output/creative-campaign/*copy-sheet*` too — production copy sheets carry verbatim sentences and silently reintroduce the old copy downstream (edge-case hunter caught it; both hunters otherwise verified clean on a 12-file label-only diff).
