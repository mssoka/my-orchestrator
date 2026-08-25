# Briefing: righttenantry-apply-form-scrub-fix — HIGH PRIORITY

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, base `develop`). **CRITICAL production bug on the applicant-conversion path.**
- **Urgency:** HIGH — jumps the queue. This bug **destroys the application form the instant an applicant interacts with it**; it is the suspected root cause of a 0/25 application-completion crisis.

## Mission

Fix a self-destruct bug in the applicant apply form's PostHog `sanitize_properties`
scrubber. **Do not re-derive the diagnosis — it's pinned below.** Implement the fix,
add a regression test, PR.

## Root cause (confirmed — exact)

`server/src/application/form_view.gleam` (~lines 278-286) renders an inline PostHog
init with a custom `sanitize_properties` whose `scrub` recurses into ANY
`typeof === 'object'` value:

```js
var scrub=function(o){if(!o||typeof o!=='object')return o;
  for(var k in o){var v=o[k];
    if(/resume-token/i.test(k)){o[k]='<redacted>';}
    else if(typeof v==='string'){o[k]=v.replace(re,'$1<redacted>');}
    else if(v&&typeof v==='object'){scrub(v);}}
  return o;};
return scrub(p);
```

`web-vitals.js` fires CLS/LCP/INP events (a few seconds in / on layout shift when
the applicant types) whose event properties carry **live DOM element refs**
(the shifted/largest-painted/interaction target). The custom `scrub` recurses into
those elements (`typeof element === 'object'` → true), then `for(var k in element)`
walks the live DOM node and `o[k]=...` **fires DOM setters**: setting `outerText` on
an attached element **replaces it with a text node**, deleting the page's structure
(and the classes the CSS targets) → the form collapses to raw unstyled HTML the
moment the applicant fills it. On a detached element the same assignment throws
`NoModificationAllowedError: Failed to set 'outerText' … element has no parent`
(the console error). This is mobile AND desktop (web-vitals is universal).

**Evidence:** console stack `capture → calculateEventProperties → sanitize_properties
→ scrub (× recursion)`, triggered from `web-vitals.js`. Symptom: form renders fine,
loses ALL styling once filling begins.

## The fix

Guard `scrub` so it never walks DOM nodes. Minimal targeted fix:

```js
var scrub=function(o){
  if(!o||typeof o!=='object')return o;
  if(typeof Node!=='undefined'&&o instanceof Node)return o;   // never walk the DOM
  for(var k in o){ ... unchanged ... }
```

This only *skips* nodes scrub should never have touched — it cannot regress the
token redaction (DOM nodes carry no `resume-token` keys, and token URLs are strings
in plain object properties, not in DOM nodes).

A more defensive alternative the minion may prefer: only recurse into **plain
objects** (`Object.prototype.toString.call(o)==='[object Object]'`), which also
skips Arrays/Window/any host object. Pick whichever is most robust AND keeps the
resume-token + URL redaction fully working (verify with the test below). Keep the
existing redaction behaviour for plain object nests and strings intact.

## Scope — fix ALL instances

This `sanitize_properties`/`scrub` pattern may be duplicated in other PostHog
snippets (e.g. the referee `/reference` form, resume/erasure pages). **grep for
`sanitize_properties` and `scrub` across `server/src` and `server/priv/static`**
and apply the same guard wherever the recursive scrub lacks a DOM/Node guard.
Don't leave a second ticking copy.

## Regression test (REQUIRED — this must never recur)

Add a test that exercises the `scrub`/`sanitize_properties` logic in isolation
(extract it to a testable unit if it's currently an inline string — e.g. a small
`server/priv/static/*-test.js` or a Gleam test that asserts the emitted snippet's
scrub behaviour). Assert, given an event-properties object that contains a **DOM-like
element** (a real detached `HTMLElement` in a jsdom/headless context, or a faithful
fake with a throw-on-set `outerText` setter and enumerable DOM-ish keys):

1. `scrub` returns **without throwing** (no `NoModificationAllowedError`).
2. The element is **not mutated** (its `outerText`/`innerText`/`textContent`/class
   untouched — scrub never wrote to it).
3. The existing redaction STILL works on plain object nests: a property
   `{attr__data_resume_token:"x"}` → `<redacted>`, and a string URL containing
   `/resume/<token>` → `/resume/<redacted>`.

Note: posthog-js no-ops capture under HeadlessChrome UAs (`_is_bot()`), so don't
rely on real PostHog capture in the test — exercise the scrub function directly.

## Verify

- The scrub unit test (above) green; existing redaction tests still pass.
- `make test-server` + `make test-shared` green.
- Manual/SSR spot-check (if feasible): loading `/apply/<short_code>` and simulating
  a web-vitals-style capture with an element ref does NOT unstyle the page and does
  NOT throw in the console.
- No em-dashes in any user-facing copy (RT CI ban) — this is internal snippet code,
  so likely N/A, but keep any copy clean.

## Acceptance

- `scrub` guards against DOM nodes (and, if using the plain-object variant, all host
  objects); the form no longer collapses on interaction; the console error is gone.
- Regression test added + green.
- Same pattern fixed in every copy of the snippet across the codebase.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `bin/ledger set righttenantry-apply-form-scrub-fix working` at start
- `bin/ledger set righttenantry-apply-form-scrub-fix in-review "PR <url>"` when PR opens
- `herdr notification show "apply-form-scrub-fix" --body "<one-line>"` on finish
- Final message: the fix summary, the test added, every snippet location patched, PR URL.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: apply-form-scrub-fix · base: develop
- model: zai-coding-cn/glm-5.2   (kimi down; this is a small, precisely-diagnosed fix — glm-5.2 is adequate; the diagnosis is in this briefing)
- pr_review: 1   (production code on the conversion path; Perkins on the glm-5.2 fallback)
- github_issue: (none)
- PRIORITY: HIGH (jumps the queue — every applicant currently hits this)
