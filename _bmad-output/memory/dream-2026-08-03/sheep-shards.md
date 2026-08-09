# Sheep findings — field-note shards

Material: 17 shards read, 4 new since marker (2026-08-01T10:44:57Z)

New shards: refcheck-privacy-draft (2026-08-02),
righttenantry-form-save-resume-f3 (2026-08-02),
righttenantry-form-stepper-f1 (2026-08-01),
righttenantry-refcheck-rc1-2 (2026-08-01).
(Note: dream-2026-08-01.md at 10:36:52Z is 8 min OLDER than the marker —
counted as old.)

## Candidate patterns

### Multi-edit `edit` calls are atomic — one bad oldText sinks the whole batch; re-read after formatters
- Sightings:
  - righttenantry-form-save-resume-f3, 2026-08-02 (new): "gleam `edit`-tool
    batches are atomic per call — when one oldText in a multi-edit call
    fails, NONE of the edits land; re-apply the survivors individually
    (lost two email_client edits + a decoder edit this way, caught only by
    compile)"
  - refcheck-privacy-draft, 2026-08-02 (new): "`functions.edit` batches are
    ATOMIC — one bad `oldText` rejects every edit in the call, and
    `gleam format` reflows split strings between runs; re-read the
    formatted file before re-issuing a failed batch"
  - finlit-bugfix-event-messages, 2026-07-31 (corroboration, pre-marker):
    "a failed edit in a multi-edit `edit` call fails the WHOLE call
    atomically — re-check the file"
- 3 sightings across 2 repos (Godot + Gleam) — tool-level, not
  repo-specific. The formatter-reflow addendum (privacy-draft) is the new
  twist: re-read the file before re-issuing a failed batch.
- Candidate memory target: minion-field-notes.md (Tooling traps). Not in
  the curated doc yet.

### Lustre SSR: assert the serialized render, never view-source assumptions (attribute order, entity escaping)
- Sightings:
  - righttenantry-refcheck-rc1-2, 2026-08-01 (new): "Lustre SSR renders
    attributes SORTED BY NAME with empty-valued ones bare (`checked`,
    `required`) — never assert attribute order from the view source"
  - righttenantry-form-save-resume-f3, 2026-08-02 (new): "Lustre sorts HTML
    attributes alphabetically when rendering (`name="_form_loaded_at"
    type=... value=...`) — never write HTML string splits that assume
    source attribute order"
  - refcheck-privacy-draft, 2026-08-02 (new): "apostrophes come back as
    `&#39;` (houdini escape) — 'landlord's' in an h2 pin fails against raw
    text" (assert the RENDERED form)
  - righttenantry-refcheck-rc1-2, 2026-08-01 (new): "verbatim copy
    colliding with assertion substrings (the §5.3 footer's 'references are
    checked' ate my `checked` no-default assertion; assert `checked
    data-testid="..."` instead)"
- Attribute-sorting kernel seen independently in 2 jobs; escaping +
  substring-collision extend the same meta-lesson. 4 sightings, 3 jobs,
  all new since marker.
- Candidate memory target: minion-field-notes.md (Tooling traps). Not in
  the curated doc yet.

### `server/priv/static/*` is git-ignored with a per-file whitelist — new static assets deploy as dead script tags unless whitelisted
- Sightings:
  - righttenantry-form-stepper-f1, 2026-08-01 (new): "every new static
    asset needs its `!` line in `.gitignore` or it deploys as a dead
    script tag while SSR pins (which only assert the tag) stay green
    (review swarm caught it)"
  - righttenantry-form-save-resume-f3, 2026-08-02 (new): ".gitignore
    whitelists every `server/priv/static/*.js` individually — a new static
    JS file is invisible to git until whitelisted (blocker caught in
    review)"
  - righttenantry-form-funnel-w0, 2026-07-31 (corroboration, pre-marker):
    "`server/priv/static/*` is gitignored with a per-file exception list —
    any new static asset MUST get a `!path` exception in `.gitignore` or
    it silently never deploys (caught only by the review swarm)"
- 3 sightings, and ALL THREE were caught only by review — the lesson was
  shard-recorded on 2026-07-31, missed promotion in the 2026-08-01 dream,
  and has bitten twice since. Strong promote signal.
- Candidate memory target: minion-field-notes.md (Tooling traps or
  Recurring review findings). Not in the curated doc yet.

### Verify reviewer mechanism-claims against ground truth before crediting them
- Sightings:
  - righttenantry-refcheck-rc1-2, 2026-08-01 (new): "the SSR apply form
    carries `novalidate` on BOTH the GET and error re-render — native
    browser validation NEVER fires there... Reviewers (both hunters,
    independently) hallucinated native-blocking findings from the
    `required` attributes; verify mechanism claims against the form
    element before crediting them"
  - finlit-game-brief, 2026-07-31 (corroboration, pre-marker):
    "Mega-minions re-reviewing a file the parent just edited can report
    STALE findings from session context (2 this run) — verify every
    finding against disk before applying"
- Extends the already-curated "ground-truth-first" convention with a new
  failure mode: not just stale findings, hallucinated browser-mechanism
  claims from two independent reviewers.
- Candidate memory target: minion-field-notes.md (extend the existing
  2026-07-31 "ground-truth-first" entry under Conventions).

### RightTenantry local tooling vs staging/env: env files clobber overrides; staging lags unmerged migrations
- Sightings:
  - righttenantry-form-stepper-f1, 2026-08-01 (new):
    "`dot_env.load_default()` overrides the process env — to repoint a
    local dev server, replace the `server/.env` symlink with an edited
    copy (gitignored); staging DB lags develop migrations (submissions 500
    on `submitted_ip_text`), so E2E against a local Docker DB + seeded
    vacancy"
  - righttenantry-form-funnel-w0, 2026-07-31 (corroboration):
    "`run_squirrel.sh` sources `.env` and clobbers your override"
  - righttenantry-refcheck-rc1-1, 2026-07-31 (corroboration):
    "`run_squirrel.sh` points at staging, which doesn't have unmerged
    migrations"
  - righttenantry-refcheck-rc2-1, 2026-07-31 (corroboration): "point
    `DATABASE_URL` there for squirrel (never staging)"
- The anti-staging half is partially curated (Squirrel triple-trap entry);
  the NEW generalization is `dot_env.load_default()` clobbering process
  env at runtime + staging lag breaking E2E (not just squirrel regen).
- Candidate memory target: minion-field-notes.md (extend the Squirrel /
  RightTenantry tooling entries).

## Stale / superseded notes

- dream-2026-08-01 shard (and the curated 2026-08-01 entry derived from
  it) frames the remedy for gru.ts checklist-injection as "Until the
  extension is gated (report P9), brief every mega-minion launched there:
  'you are NOT Gru'". In practice the remedy that stuck is **cwd exile**:
  the 2026-08-01 AGENTS.md gotcha ("never hand a non-Gru agent a pane
  rooted at the orchestrator root") plus Bob's home dir — sheep briefs
  still carry the NOT-Gru line as belt-and-braces (this very brief does),
  but no extension gating has happened and the cwd guard is now the
  documented control. The injection fact remains true; "until the
  extension is gated" is superseded as the operative fix.
- No notes in the 4 NEW shards were contradicted by later events. (f1's
  deferred `showInlineError` display bug is still deferred, not stale;
  f1/f3 re-recording the gitignore trap is a repeat sighting, not
  staleness.)

## One-off anecdotes (single sighting — watch items)

- refcheck-privacy-draft, 2026-08-02: "`element.unsafe_raw_html` CANNOT
  emit a standalone HTML comment (lustre 5.6 wraps inner_html in
  `<tag>…</tag>`; a `!--` tag renders `<!-->TEXT</!-->` and LEAKS visible
  text)" — post-render `string.replace` on the serialized open tag +
  uniqueness pin instead.
- righttenantry-refcheck-rc1-2, 2026-08-01: making a form field mandatory
  server-side breaks every bug-hunt scenario that submits the form —
  update all 5 scenario files (landing/apply-form,
  landing/apply-form-label-invariants, workflows/apply-form-soak,
  workflows/seed-archetype-applicants, workflows/seed-applicants) in the
  same PR.
- righttenantry-form-save-resume-f3, 2026-08-02: form.js's
  `_form_loaded_at` IIFE overwrites the SSR stamp on EVERY load — any
  deliberate server-side backdating needs a marker guard in form.js, not
  just the SSR change.
- righttenantry-form-stepper-f1, 2026-08-01: upload-slot `.field-error`
  spans need inline `display:flex` (they never get `.has-error`); same
  display bug exists in form.js's preflight `showInlineError` (deferred).
- righttenantry-form-stepper-f1, 2026-08-01: timing trap rejects <2s fills
  as spam — sleep before scripted submits.
