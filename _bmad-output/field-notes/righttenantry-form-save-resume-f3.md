# Field notes — righttenantry-form-save-resume-f3

- gleam `edit`-tool batches are atomic per call — when one oldText in a
  multi-edit call fails, NONE of the edits land; re-apply the survivors
  individually (lost two email_client edits + a decoder edit this way,
  caught only by compile).
- Lustre sorts HTML attributes alphabetically when rendering
  (`name="_form_loaded_at" type=... value=...`) — never write HTML string
  splits that assume source attribute order.
- form.js's `_form_loaded_at` IIFE overwrites the SSR stamp on EVERY load —
  any deliberate server-side backdating (like the resume page's) needs a
  marker guard in form.js, not just the SSR change. And: `.gitignore`
  whitelists every `server/priv/static/*.js` individually — a new static JS
  file is invisible to git until whitelisted (blocker caught in review).
