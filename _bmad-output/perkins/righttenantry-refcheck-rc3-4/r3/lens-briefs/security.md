# LENS: security (source tag: `security`) — Perkins r3 refcheck

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing verification, output contract).

OWASP-oriented security review of the delta (the `initReviewSubmit` seam + tests). The seam runs client-side on the PUBLIC referee form (`/reference/:token`) — an unauthenticated, attacker-reachable surface.

Check:
- Does the seam write any attacker-controllable value to the DOM in a way that could XSS? (`focusField.value = clampFocusSeconds(...)` — `clampFocusSeconds` returns `String(Math.floor(...))`, digits only. Confirm no `innerHTML`/`insertAdjacentHTML`/template injection.)
- Does it read `env.Date.now()` / `location` / DOM attributes in a way that leaks across tokens or reflects untrusted input? (It reads only `[data-focus-seconds]` + `[data-testid='reference-review-form']`.)
- Does the seam weaken the no-JS degradation (AD-3) in a way that introduces an authz/CSRF gap? (The review POST is still a native form POST through the existing token-gated handler — confirm the seam doesn't forge/redirect/suppress it.)
- Does `_focus_seconds` now carry a value the server trusts for a fraud signal (rc3-4 form_session)? If the server treats it as honest, a crafted POST can set any value — but that's pre-existing (the field was always client-reportable, AD-10 "honestly weak"); confirm the seam doesn't make a NEW trust claim. (This is a note at most — server-side `parse_focus_seconds` already treats it as weak; deferred N7.)
- Any secret/token leak into the field value or a log? (None expected — it's a number.)

**OUTPUT:** write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/security.json`. `source` must be `"security"`. `[]` is valid.
