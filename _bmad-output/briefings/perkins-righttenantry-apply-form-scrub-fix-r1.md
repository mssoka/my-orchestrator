# Perkins briefing — round 1: righttenantry-apply-form-scrub-fix

- **PR:** https://github.com/solarity-services/RightTenantry/pull/597 (targets `develop`)
- **Reviewed sha:** `7870f901897e0e8bf463c64f53a3107f1306d61e` (short `7870f90`; commit "fix(apply): guard PostHog sanitize_properties scrub against DOM nodes")
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-apply-form-scrub-fix-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-apply-form-scrub-fix.md` (the pinned diagnosis + the required regression test). No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**HIGH-PRIORITY production fix** (suspected root cause of a 0/25 applicant-completion crisis): the `/apply` form's inline PostHog `sanitize_properties` scrub recursed into ANY `typeof === 'object'` value. `web-vitals.js` attaches **live DOM element refs** to CLS/LCP/INP event properties → the custom `scrub` walked the live DOM node → `o[k]=...` fired **DOM setters** → setting `outerText` on an attached element **replaced the page structure with a text node** → the form collapsed to unstyled HTML the moment an applicant typed (and threw `NoModificationAllowedError` on detached nodes).

**The fix (form_view.gleam ~line 280):** guard the recursion to plain objects + arrays only:
```js
var ts=Object.prototype.toString.call(o);
if(ts!=='[object Object]'&&ts!=='[object Array]')return o;
```
Any host object (DOM nodes, Window, Document, NodeList…) is returned untouched. Token redaction is claimed byte-identical for plain objects/arrays/strings.

**Regression test (required):** `scripts/js-tests/apply_event_scrub.test.js` — extracts the exact shipped snippet bytes from `form_view.gleam` (anchored on stable tokens), evals them, and asserts against a fake DOM element (throw-on-set `outerText`, `[Symbol.toStringTag]='HTMLDivElement'`, enumerable DOM-ish keys): (1) scrub returns without throwing, (2) element unmutated, (3) redaction still works (token keys + URLs, incl. nested in arrays). Plus a negative control (neutered guard → "does not throw" goes red). A structural pin also exists in `form_view_test.gleam`.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

This is a **production fix on the applicant-conversion path** — the review is the last line of defense before a paying-user path ships.

- **The diagnosis is PINNED — do NOT re-derive or re-litigate the bug.** The briefing's root-cause analysis is confirmed (console stack `capture → calculateEventProperties → sanitize_properties → scrub`, triggered by web-vitals). Review the FIX + its tests, not the bug's existence.
- **The guard choice is PRE-APPROVED** — the briefing explicitly offered both variants ("`instanceof Node`… OR… only recurse into plain objects… Pick whichever is most robust AND keeps the resume-token + URL redaction fully working") and the plain-object variant was selected + directed by Silas. Do NOT flag "why not instanceof Node" — instead VERIFY the chosen guard is correct + complete: it must skip ALL host objects (not just Nodes) and keep redaction working. If you find the plain-object guard MISSES a redaction case (e.g. a host object that carries token data — practically impossible, but verify), that's a legitimate finding.
- **THE TOKEN-REDACTION INVARIANT IS LOAD-BEARING.** `resume-token` key redaction + `/resume/<token>` URL redaction in plain-object/string properties MUST still work after the guard (the `attr__data_resume_token` key style + URL strings). This is the thing that must NEVER regress. The test asserts it — verify the assertion is real + complete (plain objects, arrays nested, string URLs).
- **No second ticking copy.** The minion claims exactly ONE production copy of `sanitize_properties`/`scrub` (form_view.gleam); the SPA-shell PostHog init (Makefile/Dockerfile `RT_ANALYTICS` perl) has NO scrub; reference/erasure pages none either. **Verify the grep yourself** (`grep -rn sanitize_properties server/src server/priv/static` + the Makefile/Dockerfile perl) — a second copy without the guard is a blocker (the same bug, live elsewhere).
- **The regression test must be REAL, not tautological.** It extracts the SHIPPED bytes (no drift between test and snippet — good). Verify: the fake DOM element actually exercises the failure mode (throw-on-set `outerText`, enumerable DOM-ish keys, toStringTag), the negative control genuinely flips the test (a neutered guard → red), and the redaction assertions would catch a regression.
- **Do NOT flag "posthog-js no-ops under headless UAs"** — the briefing mandates testing scrub directly (the test extracts + evals the snippet; real PostHog capture isn't used).
- **No em-dashes in user-facing copy** (RT CI ban) — this is internal snippet code, likely N/A, but check any copy touched.
- **Do NOT flag the inline-snippet choice** — keeping the snippet inline preserves the always-on token-redaction invariant (no external-dependency leak path); the minion's rationale is sound + documented.

### Legitimate findings here would be
- **The guard is incomplete/incorrect** — a host-object class still walked (e.g. arrays containing host objects are recursed into → the walk happens at the array level), or the plain-object check has a hole.
- **Redaction regressed** — a token key or URL string no longer redacts after the guard (test misses it, or the shipped bytes differ from what the test asserts).
- **A second ticking copy** exists somewhere the grep misses (Makefile/Dockerfile perl, priv/static, other apps).
- **The regression test is tautological** — it doesn't exercise the failure mode, or the negative control doesn't actually bite.
- **A Gleam compile/test failure** (minion reports test-js 132 / server 1403 / shared 101 / client 471 green — verify they're real).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, this briefing + the job briefing (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/develop`.
- Save the canonical diff first: `gh pr diff 597 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-apply-form-scrub-fix/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-apply-form-scrub-fix/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (cache warnings on stderr corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 597 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment` in your ledger note + final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 597 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-apply-form-scrub-fix / **Reviewed sha:** 7870f90 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-apply-form-scrub-fix-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: zai-coding-cn/glm-5.2** — kimi quota is down this cycle (billing 403); glm-5.2 is the sanctioned review fallback (rc3-3 r2 ran a full 8-pane round to APPROVED on it). If Silas tells you kimi refreshed, `/model` switch mid-session.
