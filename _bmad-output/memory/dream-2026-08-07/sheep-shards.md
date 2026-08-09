# Sheep findings — field-note shards

Material: 22 new shards read in full (mtime > 2026-08-03T11:12:13Z marker);
older shards corroborated via the curated `docs/minion-field-notes.md` (which
cites them by job+date).

New shards (22):
1. righttenantry-form-e2e-pass (3 Aug 14:18)
2. righttenantry-form-resume-progress-fix (3 Aug 18:54)
3. finlit-architecture-v1 (3 Aug 18:58)
4. righttenantry-form-nojs-submit-fix (3 Aug 19:12)
5. righttenantry-draft-grace-period (3 Aug 19:38)
6. righttenantry-self-employed-copy-fix (4 Aug 02:30)
7. righttenantry-self-employed-sweep (4 Aug 03:24)
8. righttenantry-csp-enforce-allowlist (5 Aug 00:33)
9. finlit-e2-1 (5 Aug 01:13)
10. finlit-e2-7 (5 Aug 01:27)
11. orchestrator-nefario-conflict-sensor (5 Aug 10:34)
12. righttenantry-form-copy-revision (5 Aug 10:43)
13. righttenantry-guarantor-autofill-fix (5 Aug 13:34)
14. finlit-gdd-amendments (5 Aug 14:34)
15. righttenantry-oauth-posthog-fix (5 Aug 19:24)
16. packet-plumber-setup-brief (6 Aug 01:49)
17. righttenantry-csp-posthog-allowlist (6 Aug 03:40)
18. righttenantry-gcp-cost-analysis (6 Aug 13:39)
19. righttenantry-agent-model-flash (6 Aug 14:38)
20. packet-plumber-gdd-v1 (7 Aug 01:10)
21. righttenantryagents-model-flash (7 Aug 01:45)
22. packet-plumber-architecture-v1 (7 Aug 09:52)

---

## Candidate patterns (NEW — not in store)

### 1. Briefings themselves can be stale/wrong — ground-truth BRIEFING claims against disk before trusting them
- Sightings:
  - righttenantryagents-model-flash (7 Aug): "Briefing forensics can be STALE relative to merged work — this job's briefing said `config.py` default was still `gemini-3.5-flash`, but PR #164 had already moved `config.py` + the default-tier Terraform vars to `gemini-3.6-flash`. The real delta was only the 5 Pro-tier vars. Always `grep` disk for the current model strings before trusting a briefing's 'current state'."
  - righttenantry-agent-model-flash (6 Aug): "Gru's briefing said 'AI agent code lives in `server/src/ai/`' — that is the *orchestration* layer. RT is a **pure ADK client** … All model selection is in `RightTenantryAgents/tenant_scorer/config.py`."
  - packet-plumber-setup-brief (6 Aug): "the briefing listed source-material paths under the orchestrator-root `_bmad-output/planning-artifacts/`, but the concept + forge files actually lived in the REPO's own `_bmad-output/planning-artifacts/` (same relative path, different root)."
  - righttenantry-csp-posthog-allowlist (6 Aug): "Security-control briefings can ship a WRONG mechanism — ground-truth the stated reason against disk + vendor docs before crediting. Here both the briefing's reasons ('array_loader fetches from eu.posthog.com' + 'ingestion goes there') were FALSE."
- Candidate memory target: **minion-field-notes.md** — extends the existing
  "ground-truth-first" convention (which currently covers mega-minion REVIEW
  findings + reviewer MECHANISM claims) to explicitly include BRIEFING-level
  claims (paths, "current state", stated mechanisms/rationales). 4 independent
  sightings in one window; the briefing is a minion's ground truth of last
  resort and it drifted on paths, code location, model state, AND a security
  rationale.

### 2. agent-browser `click` silently no-ops on JS-driven steppers — drive via `eval`-dispatched clicks (+ scrollIntoView first)
- Sightings (5 independent, one explicitly notes "4/5 mega-minions hit the same three traps"):
  - righttenantry-form-e2e-pass (3 Aug): "agent-browser on this form: `click` silently no-ops on below-fold elements (emulated viewport + smooth scroll) — eval `scrollIntoView({behavior:'instant'})` first; `fill` can't set `input[type=date]` (set value + dispatch input/change); click the `label[for=field-X]` not the visually-hidden radio. 4/5 mega-minions hit the same three traps independently."
  - righttenantry-form-resume-progress-fix (3 Aug): "agent-browser `click` silently no-ops on the stepper's Back/Continue buttons under an emulated mobile viewport (sticky progress bar overlap) — drive stepper nav via `eval` clicks on `[data-testid=step-continue-<id>]`; `fill` can't set input[type=date] either."
  - righttenantry-self-employed-sweep (4 Aug): "agent-browser `click` doesn't drive this app's stepper buttons (agent-native click reported Done, nothing advanced) — `eval`-dispatched `el.click()` works. Radios/labels also need explicit `checked=true` + dispatched `change`/`input` events; date inputs take `value='YYYY-MM-DD'` + events."
  - righttenantry-self-employed-copy-fix (4 Aug): "The apply-form stepper's Continue is `type=button` + JS validation; `agent-browser click` advanced silently and my re-snapshot read stale state — drive it via `eval`."
  - righttenantry-form-nojs-submit-fix (4 Aug): "its clicks race `scroll-behavior: smooth` — `eval scrollIntoView` → sleep ~1.2s → `find first '<css>' click` is the reliable pattern."
- Candidate memory target: **minion-field-notes.md** (tooling traps) — NEW
  cluster, nothing about agent-browser exists in the store. The reliable recipe
  across all 5: `eval scrollIntoView` → `eval el.click()` (or click the
  `label[for=]`), and for `input[type=date]` set `.value` + dispatch
  input/change (agent-browser `fill` can't).

### 3. Fresh worktrees ship NO node_modules → `make build` fails on `tailwindcss: command not found`
- Sightings (4 independent, 3 different fixes offered):
  - righttenantry-csp-posthog-allowlist (6 Aug): "`make build` fails in fresh RT worktrees on `tailwindcss: command not found` (dev-dep CLI not bootstrapped) — Use `make build-server` + `make test-server` for server-only verification."
  - righttenantry-csp-enforce-allowlist (5 Aug): "worktree bootstrap does NOT copy node_modules — `ln -s /Users/moses/code/RightTenantry/node_modules` before `make build` (tailwindcss)."
  - righttenantry-form-resume-progress-fix (3 Aug): "`make build` in a fresh worktree fails at tailwind until `npm ci` (worktrees ship no node_modules; `make test` never notices because js-tests use bare node)."
  - righttenantry-draft-grace-period (3 Aug): "Worktree bootstrap gap: `make build` fails on `tailwindcss: command not found` — `ln -s /Users/moses/code/RightTenantry/node_modules node_modules` fixes it (gitignored, never committed)."
- Candidate memory target: **minion-field-notes.md** (tooling traps) — NEW.
  Three known fixes (symlink node_modules from main checkout / `npm ci` / skip
  with `make build-server`); pick by scope. Note `make test` does NOT surface
  it (js-tests run on bare node), so the failure bites at build time only.

### 4. Mega-minion review swarms EARN their panes on big docs — and budget an R2 pass (R1 fixes introduce their own bugs)
- Sightings:
  - packet-plumber-architecture-v1 (7 Aug): "A **2-hunter review swarm** (adversarial-general + edge-case-hunter mega-minions) caught real contradictions the author was blind to on a high-stakes doc every downstream agent reads … Worth the ~2-pane cost; verify every finding against disk (ground-truth-first) before applying — all 40 findings here were legit."
  - finlit-architecture-v1 (3 Aug): "Mega-minion review swarms EARN their panes on big docs: the R1 swarm caught a schema that silently violated a locked pillar (KID-persists) and a sync-over-HTTP seam that wasn't buildable; R2 caught a defective rounding formula I'd written to fix R1 (the GDD's own $24→$2 tax example was the disproof) — budget an R2 pass, R1 fixes introduce their own bugs."
  - finlit-gdd-amendments (5 Aug): "silent edits get caught by the review swarm every time (both lenses flagged provenance/citation issues; the adversarial lens web-verified the Disney Research citation)."
- Candidate memory target: **minion-field-notes.md** (conventions / practices
  that worked) — NEW as a standalone note. The R2-budget corollary (R1 fixes
  introduce bugs) is the novel, durable part.

### 5. Relative-path resolution surprises in worktrees — edit/write tools resolve to the MAIN checkout; ESM imports resolve to the SCRIPT's dir, not cwd
- Sightings:
  - finlit-e2-7 (5 Aug): "Relative-path edit/write tools resolved to the MAIN checkout, not the worktree — one `git commit` ran with `cd /Users/moses/code/kids-finlit-game` and landed on local main (recovered via stash + branch move; ALWAYS use absolute worktree paths for file tools and git)."
  - orchestrator-nefario-conflict-sensor (5 Aug): "ESM relative imports resolve against the SCRIPT's directory, not `cwd` — a /tmp scratch importing a worktree `.ts` needs the absolute path; keep scratch files inside the worktree instead."
- Candidate memory target: **minion-field-notes.md** (tooling traps) — 2
  sightings, same root cause (relative path ≠ worktree). Rule: absolute paths
  for file tools + git in worktrees; keep scratch importers inside the worktree.

### 6. `node --experimental-strip-types` REJECTS constructor parameter properties + `const enum` (parse-test your .ts extension before commit)
- Sightings:
  - orchestrator-nefario-conflict-sensor (5 Aug): "Node 22 `--experimental-strip-types` REJECTS constructor parameter properties (`private x: T` in a constructor signature) — 'TypeScript parameter property is not supported in strip-only mode'. Declare the field explicitly and assign in the body. (Same flag also can't run a file with non-erasable runtime enums/`const enum` — stick to plain const Sets like the extension already does.)"
- Candidate memory target: **minion-field-notes.md** (tooling traps) — this is
  the 2nd sighting of the "parse-test TS extensions before commit" watch item
  (see Watch items recurring); the new content is WHAT the flag rejects
  (parameter properties, `const enum`). Promote with the rejection list.

---

## Watch items recurring (2nd sighting this window)

- **parse-test TS extensions before commit (`node --experimental-strip-types`)** — 2ND SIGHTING this window (orchestrator-nefario-conflict-sensor, 5 Aug), with new technical detail: the flag rejects TS **constructor parameter properties** (`private x: T` in a ctor signature) and non-erasable runtime enums / `const enum` — use plain `const` Sets and explicit field declarations + body assignment. Promote-worthy → captured as candidate #6 above. (1st sighting was the dream-2026-08-03 era watch item establishing "run strip-types to test your .ts extension before committing".)

Other previously-watched items checked for a 2nd sighting this window — **NO new sightings**:
- hold-release for pane capacity — none.
- non-blocking clarify (escalate without flipping to clarifying) — none.
- watcher "pane vanished" self-inflicted by your own sweep — none.
- ledger event text strips `$` amounts — none.
- `gleam format` must cover all packages — none (squirrel regen appears, but not the gleam-format-all-packages point).
- dual-gate echo (PI_GRU+PI_SILAS) / was the relaunch journaled — none.
- form.js `_form_loaded_at` IIFE overwrites SSR stamp — none.
- upload-slot `.field-error` needs `display:flex` — none.

---

## Stale / superseded notes

- **righttenantry-agent-model-flash (6 Aug) "Current prod map" is PARTIALLY STALE.** It lists the Flash tier (`default_model`) as `gemini-3.5-flash` ("verified by reading `variables.tf` directly"), and resolves the cost job as "target = `gemini-3.6-flash` for **ALL** agents (both tiers) … So `default_model` 3.5→3.6-flash AND all 5 Pro vars." The next day's shard (righttenantryagents-model-flash, 7 Aug) shows **PR #164 had already moved `config.py` + the default-tier Terraform vars to `gemini-3.6-flash`** — i.e. the Flash-tier change landed between the two shards; only the 5 Pro-tier vars remained as the real delta. If promoting any "current prod model map" to memory, use the 7 Aug state (Flash tier already on 3.6-flash), not the 6 Aug map. (The 7 Aug shard itself flags this as the canonical "briefing-stale" example — see candidate #1.)

---

## One-off anecdotes (single sighting — watch items)

Grouped by theme for scanning. Each is job-id + date + the durable kernel.

### agent-browser (beyond the click cluster in candidate #2)
- **Shared default session is machine-wide** (righttenantry-form-nojs-submit-fix, 4 Aug): "agent-browser's DEFAULT session is shared machine-wide — a sibling minion's drive hijacked my browser mid-scenario (I landed on THEIR page on THEIR port). Always `--session <job-id>`."
- **Playwright `javaScriptEnabled:false` kills in-page rAF** (righttenantry-form-nojs-submit-fix, 4 Aug): actionability-gated click/check time out as "not stable"/"detached", but fill/select/boundingBox + CDP evaluate still work; drive clicks via `page.mouse.click` at boundingBox center. Probe with CDP evaluate to PROVE page scripts are off.

### Godot / finlit (extends existing Godot cluster in store)
- **Disabled Buttons swallow clicks + emit no `gui_input`; headless never routes GUI** (finlit-e2-1, 5 Aug): tap capture needs a transparent `MOUSE_FILTER_STOP` overlay child (anchors FULL_RECT), verified windowed; headless tests pin wiring via direct `gui_input.emit`.
- **`FileAccess` WRITE buffers empty until `flush()`** (finlit-e2-1, 5 Aug): `get_file_as_string` right after `store_line` is empty until flushed (same trap as pipe truncation); also `Time.get_datetime_string_from_system(false,true)` puts a SPACE in filenames (use UTC + replace ":").
- **Root window is 64×64 while content space is 1280×1280 (stretch)** (finlit-e2-7, 5 Aug): resize the window to content size or routed taps never land; `push_input` delivery is deferred one frame (assert a frame later).
- **Measure popup targets only after a bounded settle loop** (finlit-e2-7, 5 Aug): the leaderboard card's first layout pass is ~8x tall from unwrapped labels — never `await resized` alone (rect stable across frames).
- **`aspect=expand` + both orientations needs a SQUARE base (720×720)** (packet-plumber-setup-brief, 6 Aug): a rectangular base yields a different scale factor per orientation (per the multiple-resolutions doc). User then ruled landscape-only → 1280×720 + `orientation=0`.
- **GDScript 4.7: no `Array.find_last` (use `rfind`); `:=` on a String/Array ternary trips INFERENCE_ON_VARIANT warnings-as-errors (annotate `: Array`)** (finlit-e2-1, 5 Aug).

### lavish (extends existing lavish cluster)
- **Mid-review file rewrite → browser serves CACHED old version** (righttenantry-gcp-cost-analysis, 6 Aug): after overwriting the dashboard HTML mid-review, the user said "nice" to the STALE content; the poll's `dom_snapshot` was the only ground truth. Fix: `lavish-axi <file> --reopen` OR tell the reviewer to reload AND verify via the NEXT poll's dom_snapshot that the new content rendered before trusting any "looks good."
- **One `poll` can return a BATCH of feedback items** (packet-plumber-architecture-v1, 7 Aug): handle them together, re-render, reply once; batch the doc edits in one `edit` call (disjoint oldTexts) — faster than per-item round-trips.
- **Lavish design-doc review can drive 15+ substantive user-driven changes** (packet-plumber-gdd-v1, 7 Aug): keep `decision-log.md` current PER change (provenance + pillar-fit + "why it earned its place") so the PR's rationale stays traceable.

### RT / ADK / GCP infra
- **Prod models are Terraform-managed, not code-managed** (righttenantry-agent-model-flash, 6 Aug): a code-only PR bumping `config.py` `_DEFAULT_HARDCODED` changes only the FALLBACK — prod runs on env-overridden Terraform values; moving prod = change `variables.tf`/`vars/*.tfvars` too. Two surfaces, both must change.
- **`rg` through the harness MASKS `gemini-*` tokens as `n.*`; `cat`/`read` shows real strings** (righttenantry-agent-model-flash, 6 Aug) — tooling trap when grepping for model strings.
- **RT is a pure ADK client** (righttenantry-agent-model-flash, 6 Aug): model selection lives in `RightTenantryAgents/tenant_scorer/config.py` (`get_agent_model`: `{AGENT}_MODEL` env → `DEFAULT_MODEL` env → hardcoded default), never in RT's `server/src/ai/` (orchestration layer only).
- **Judge sanity-checks confounded by `web_search` tool without `BRAVE_API_KEY`** (righttenantryagents-model-flash, 7 Aug): `consistency_checker` on Flash retried the failing tool in a slow loop while Pro tried once — a dev-env artifact, not a model-quality signal (prod has Brave). For judge checks, confirm Brave is present or pick a tool-free path.
- **Don't attempt inline full-pipeline eval head-to-heads** (righttenantryagents-model-flash, 7 Aug): each evalset case ran >10 min (anonymizer slow-mode + multi-agent); the repo routes full evals to staging deploy. Also `StreamingMode.SSE` hits an `httpx readline(max_line_length=...)` version mismatch in this venv — use default non-streaming `run_config`.
- **GCP billing export is CONSOLE-ONLY** (righttenantry-gcp-cost-analysis, 6 Aug): `gcloud` has no billing-export command and the Cloud Billing v1 API doesn't expose the BigQuery export config — from a minion shell you can `bq mk` the dataset + write attribution queries, but flipping the export is the user's 4 console clicks (role: billing admin).
- **A single GCP project can blend MULTIPLE use-cases** (righttenantry-gcp-cost-analysis, 6 Aug): `iginsider` blended RT Facebook-ad creative + RT agents + personal YouTube — never assume one project = one use-case; require app-side resource/call LABELS to attribute (project boundary is the only clean line billing gives).

### Sentry / CSP
- **Classic `sentry-cli` token (event:read) works; the NEW `sentry` CLI's own token 403s** (righttenantry-csp-enforce-allowlist, 5 Aug): read event payloads via `curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" https://sentry.io/api/0/organizations/right-tenantry/events/?query=issue.id:N...` (org-scoped events path, NOT `/api/0/issues/`); `/api/0/issues/{id}/events/` 404s.
- **CSP report endpoint forwards junk** (righttenantry-csp-enforce-allowlist, 5 Aug): `blocked-uri` values like bare `properties` or same-origin script under `'self'` are physically impossible from real browsers — the public unauthenticated `/api/v1/csp-report` forwards any parseable body. Verify impossible payloads before allowlisting; Sentry short-ID groups can mix multiple blocked_uris under one title.

### Chrome autofill (deep technique — guarantor-autofill-fix, 5 Aug)
- **Chromium `kTypeValueFormFillingLimit = 9`** (per type, per fill, counted across the whole form in DOM order): the apply form's 10 NAME_FULL / 11 PHONE / 11 EMAIL fields suppress the 10th/11th instances (primary guarantor block) on every fill — reproduces "other sections fill; guarantor suggests but doesn't populate." Lever: `tel` vs `tel-national` are separate Chrome type buckets (keeps co-applicant phones fillable); NAME/EMAIL have no alternative standard tokens.
- **Real-browser autofill verification via raw CDP** (Node 22 built-in WebSocket): `Autofill.enable` + `Autofill.setAddresses` then `Autofill.trigger` with `fieldId` = `DOM.describeNode` backendNodeId; `chrome://autofill-internals` logs fill decisions (only ground truth for why fields skip). DOM-mutation tests invalidate Chrome's cached form structure — use fresh page loads per experiment.

### Testing practices (generalizable)
- **An invariant TEST only proves value if it BITES — run a negative control** (righttenantry-csp-posthog-allowlist, 6 Aug): for a "X must stay absent" lock, inject X into the source, confirm the test goes red (full `make test-server` — unitest ignores gleeunit's `-n` filter, so don't target one test), then `git checkout` to revert. Injecting eu.posthog.com into connect-src flipped the lock red = proof it catches any directive addition, not a tautology.
- **Testing a pi extension that self-registers `setInterval` callbacks** (orchestrator-nefario-conflict-sensor, 5 Aug): each `start()` pushes TWO callbacks (pane tick + PR tick) — a per-scenario tick handle MUST be captured at start time; a fixed `callbacks[1]` index silently runs scenario 1's closure against every other scenario's data (ticks stay silent, assertions pass by luck until a re-arm case exposes it).

### Shell / git
- **`gh pr create --body "$(heredoc)"` chokes on embedded quotes/backticks** (packet-plumber-setup-brief, 6 Aug): use `--body-file <file>` for any non-trivial PR body. (Reusable across jobs.)
- **`git checkout -- <file>` after a sed-tamper test-run wipes ALL uncommitted work in that file** (righttenantry-draft-grace-period, 3 Aug): revert tamper lines with sed on the exact line, never `checkout`.

### BMAD docs workflow (finlit-gdd-amendments, 5 Aug)
- **Amendments to LOCKED content need an explicit renegotiation section + inline `[AMENDED — A#]` tags + register-row updates** — silent edits get caught by the review swarm every time.
- **"12+"-style open caps invite implementers to invent numbers** — pin the unlock ladder (per-gate assignments, definitions like "first $500 = lifetime total_earned", offline fallbacks) in the amendment itself.
- **Docs-vs-code honesty**: when an amendment supersedes a code-side pin, say "supersedes — code-side change, out of scope" not "replaced" (reviewer checked disk and caught the overclaim).

### RT repo specifics (one-offs)
- **`(xmax = 0) AS is_new` in an upsert RETURNING codegens cleanly as `Bool`** (righttenantry-oauth-posthog-fix, 5 Aug) — atomic insert-vs-update flag, reviewers prefer it over a pre-check SELECT.
- **Analytics bridge snippets live in 4 places** (righttenantry-oauth-posthog-fix, 5 Aug): Makefile + Dockerfile perl chains, each with a substring-pin guard — any snippet change must hit all 4, and the guard pin must be a substring UNIQUE to the changed arm. Cookie lifetimes (`rt_landlord_id` 60s vs sentinels 10s) are a cross-cutting contract pinned in 3 tests + 2 guard lists.
- **`rt_consent_test=1` auto-accepts with analytics:false** (righttenantry-form-e2e-pass, 3 Aug) — for analytics E2E legs, click the real banner's Accept-all.
- **PostHog `_is_bot()` drops ALL capture for HeadlessChrome UAs** (righttenantry-form-e2e-pass, 3 Aug) — local analytics E2E sees zero network events; wrap `window.posthog.capture` in-page and assert the call stream instead.
- **form-bug-hunt email template `test+{SCENARIO}-{RUN_ID}@example.com` produces `/` in local parts** → `shared/email.is_valid` rejects (righttenantry-form-e2e-pass, 3 Aug); shard says fixed in SKILL.md (sanitise `/`→`-`, ≤64 chars). Also Resend 422s example.com locally — use `delivered+tag@resend.dev`.
- **Vacancy has NO `closed_at`** (righttenantry-draft-grace-period, 3 Aug): manual-close moment = `closed_notified_at`; `vacancy.updated_at` never bumps on close (editable-fields-only trigger) — don't anchor time-based logic to it.
- **Copy fix touching a user-visible phrase: grep `_bmad-output/creative-campaign/*copy-sheet*` too** (righttenantry-self-employed-copy-fix, 4 Aug) — production copy sheets carry verbatim sentences and silently reintroduce old copy downstream.
- **`.env.test` is tracked (NOT gitignored)** (righttenantry-self-employed-copy-fix, 4 Aug): placeholder secrets only; repoint DATABASE_URL port + `git checkout .env.test` after — never let real secrets land in it.
- **Rebasing copy PRs: negative pins from a superseded ruling must be RE-POINTED, not just conflict-resolved** (righttenantry-self-employed-sweep, 4 Aug): #573's `string.contains("employer, if you") |> should.be_false` silently contradicted the new scoped text.

### Coordination / herdr
- **`HERDR_*` env vars go STALE across Herdr restarts** (finlit-architecture-v1, 3 Aug): re-resolve with `herdr pane current --current` before splitting; layout JSON gives the real ids.

### Corroborations of EXISTING store entries (not new — listed for completeness)
- **lavish end-session strands queued prompts → check `~/.lavish-axi/state.json`** — corroborated by finlit-architecture-v1 (3 Aug) + the gcp-cost-analysis mid-review-cache anecdote (different lavish facet).
- **lavish markdown→HTML via `marked --gfm -o` file write (no pipe)** — corroborated by packet-plumber-architecture-v1 (7 Aug, 78KB doc → 98KB HTML, tail verified).
- **multi-edit `edit` atomicity** — corroborated + extended by righttenantry-form-copy-revision (5 Aug): a CROSS-FILE batch fails wholesale on the first mismatch; dropping a trailing `,` from oldText leaves `",,"` doubles (perl `s/",,",/"` rescued).
- **Squirrel whitespace churn** — extended by righttenantry-oauth-posthog-fix (5 Aug): churn hits `ai/sql.gleam` + `application/sql.gleam` + `inbound_email/sql.gleam` (store only names ai/sql.gleam).
- **RT `dot_env.load_default()` overrides process env** — corroborated by self-employed-sweep (4 Aug) + form-nojs-submit-fix (4 Aug); new nuance: `.env.test` is a tracked, cleaner alternative (self-employed-copy-fix).
- **test-DB port 54321 contention → own container** — corroborated by self-employed-sweep (4 Aug): "54321/54322 were both taken by sibling jobs."
- **`--headless --check-only` invalid → use `--import` then `--quit-after 600`** — corroborated by packet-plumber-setup-brief (6 Aug).
