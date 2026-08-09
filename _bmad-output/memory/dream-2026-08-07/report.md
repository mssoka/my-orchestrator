# Dream report — 2026-08-07

Material: **22 new field-note shards**, **8 journal files** (Gru 07-31→08-02;
Silas 08-03→08-07; ~95 timestamped entries), **~400 ledger events across ~56
jobs** — since **2026-08-03T11:12:13Z**. Sheep: sheep-shards (w1T:pE6),
sheep-journals (w1T:pE7), sheep-ledger (w1T:pE8) — findings in sibling files;
all badged out and closed before this report.

Store copies with all **auto** edits applied, diff-ready:
`_bmad-output/memory/dream-2026-08-07/store/` (diff vs live: field-notes
+63/-1 lines; AGENTS.md +65 lines — 7 new/amended field-note entries +
2 gotcha amendments + 6 new gotchas + 1 prune).

## Proposal summary

| # | Title | Target | Class | Sightings |
|---|---|---|---|---|
| P1 | agent-browser `click` no-ops on JS controls → eval-drive | field-notes (Tooling) | auto ✓ | 5 jobs |
| P2 | RT worktrees ship no node_modules → `make build` fails on tailwind | field-notes (Tooling) | auto ✓ | 4 jobs |
| P3 | ground-truth-first → the BRIEFING itself can be stale/wrong | field-notes (amend) | auto ✓ | 4 jobs |
| P4 | `--experimental-strip-types` rejects param-properties + `const enum` | field-notes (Tooling) | auto ✓ | 2nd sighting |
| P5 | relative paths resolve to MAIN checkout / script dir, not worktree | field-notes (Tooling) | auto ✓ | 2 jobs |
| P6 | 2-hunter review swarms earn their panes; budget an R2 (R1 fixes bug) | field-notes (Conventions) | auto ✓ | 3 jobs |
| P7 | under-locked change: coverage-gap + non-unique guard-pin | field-notes (Recurring) | auto ✓ | 2 jobs |
| P8 | `set in-review "<url>"` does NOT populate `pr` | AGENTS.md gotcha | auto ✓ | 3+ (verified) |
| P9 | glm-5.2 = 4th incident class → deepseek redirect, not continue | AGENTS.md gotcha (amend) | auto ✓ | 5+ |
| P10 | kill a dead pi via `herdr pane process-info` → `kill <pid>` | AGENTS.md gotcha | auto ✓ | 3 (verified) |
| P11 | Perkins close-out recovery flavors + deepseek leaves worktree | AGENTS.md gotcha (amend) | auto ✓ | 10/3 |
| P12 | serialize-hold for pane capacity: pre-create round row | AGENTS.md gotcha | auto ✓ | ≥5 |
| P13 | dual-gate echo: relaunch `env -u PI_SILAS PI_GRU=1 pi` | AGENTS.md gotcha | auto ✓ | journaled-unfiled |
| P14 | "moot on merge" not default; merged-mid-round → FYI + audit | AGENTS.md gotcha | auto ✓ | 2+ |
| P15 | in-repo follow-up jobs: Gru's dispatch = prior pane free | AGENTS.md gotcha | auto ✓ | packet-plumber chain |
| — | prune stray `pproved p13` corruption in Recurring review | field-notes | auto ✓ | — |

**15 proposals, all auto.** Plus 3 user-ack items (UA1–UA3 below) and a
large watch list.

---

## Proposals

### P1 — agent-browser `click` silently no-ops on JS-driven controls → drive via `eval`
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry — `click` no-ops on below-fold / sticky-bar-overlap /
  `type=button`+JS-validated stepper buttons and the re-snapshot reads STALE
  state; reliable recipe = `eval scrollIntoView({behavior:'instant'})` →
  `eval el.click()` (or click `label[for=]`), read state from DOM; `fill`
  can't set `input[type=date]` (set `.value` + dispatch input/change);
  radios need `checked=true` + events. Default session is SHARED
  machine-wide → always `--session <job-id>`.
- Evidence: righttenantry form-e2e-pass 2026-08-03 ("4/5 mega-minions hit
  the same three traps independently"), form-resume-progress-fix 08-03,
  form-nojs-submit-fix 08-04, self-employed-copy-fix 08-04,
  self-employed-sweep 08-04 (session-hijack sub-point).
- Reasoning: the strongest cluster of the pass — 5 jobs, one explicitly
  noting 4/5 minions hit it independently. Nothing about agent-browser is in
  the store; every sighting cost a stuck/re-read E2E step.

### P2 — Fresh RT worktrees ship no `node_modules` → `make build` fails on `tailwindcss`
- Target: `docs/minion-field-notes.md` (Tooling traps, RT crew) · Class: **auto** (applied)
- Change: new entry — worktree bootstrap copies only git-tracked files, so
  `make build` fails `tailwindcss: command not found` while `make test`
  never notices (js-tests run on bare node). Fixes by scope: symlink
  `<repo_root>/node_modules`, or `npm ci`, or `make build-server` /
  `test-server` for server-only work.
- Evidence: csp-posthog-allowlist 08-06, csp-enforce-allowlist 08-05,
  form-resume-progress-fix 08-03, draft-grace-period 08-03.
- Reasoning: 4 sightings, 3 different fixes offered — a bootstrap gap
  (playbook Dispatch step 4 only symlinks env files). Bites at build time
  only. (Structural counterpart = UA2.)

### P3 — ground-truth-first extends to the BRIEFING itself (stale state / wrong paths / wrong mechanisms)
- Target: `docs/minion-field-notes.md` (amend ground-truth-first) · Class: **auto** (applied)
- Change: 2026-08-07 addendum — a briefing's "current state", file paths,
  and rationales can be STALE (forensics pre-date a merged PR) or WRONG (a
  security-control mechanism disk + vendor docs disprove); `grep`/`find`
  disk for the real current state, verify any stated mechanism, escalate
  rather than improvise.
- Evidence: righttenantryagents-model-flash 08-07 (PR #164 had already
  moved the model tier), packet-plumber-setup-brief 08-06 (paths under
  orchestrator root vs repo root), righttenantry-csp-posthog-allowlist
  08-06 (briefing's CSP rationale FALSE), righttenantry-agent-model-flash
  08-06 ("AI code in server/src/ai/" was the orchestration layer). Two
  sheep (shards #1 + journals #20) converged independently.
- Reasoning: the existing entry covers review findings + reviewer mechanism
  claims; the NEW source is the briefing itself — a minion's ground truth
  of last resort, and it drifted on state, location, and a security
  rationale in one window.

### P4 — `node --experimental-strip-types` rejects constructor parameter-properties + `const enum`
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry (promotes the dream-2026-08-03 "parse-test strip-types"
  watch item) — the flag rejects TS ctor parameter properties ("not
  supported in strip-only mode"; declare field + assign in body) and can't
  run non-erasable runtime enums / `const enum` (use plain `const` Sets);
  parse-test any `.ts` extension before commit.
- Evidence: orchestrator-nefario-conflict-sensor 08-05 (2nd sighting; 1st
  was the dream-2026-08-03 watch item).
- Reasoning: the previous dream explicitly said "amend on second
  sighting"; this supplies the concrete rejection list. Pairs with the
  in-store backtick-kills-extension gotcha.

### P5 — Relative paths surprise in worktrees: edit/git → MAIN checkout; ESM → script dir
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry — relative-path edit/write tools + `git` resolved to
  the MAIN checkout (one commit landed on local `main`); ESM relative
  imports resolve against the script's dir, not `cwd`. Use absolute
  worktree paths for file tools + git; keep scratch importers inside the
  worktree.
- Evidence: finlit-e2-7 08-05 (committed to local main, recovered via
  stash + branch move), orchestrator-nefario-conflict-sensor 08-05 (ESM).
- Reasoning: 2 sightings, one HIGH-severity (work landed on main). Same
  root cause (relative ≠ worktree); the absolute-path rule is cheap and
  prevents the worst case.

### P6 — 2-hunter review swarms earn their panes on big docs; budget an R2 (R1 fixes introduce bugs)
- Target: `docs/minion-field-notes.md` (Conventions) · Class: **auto** (applied)
- Change: new entry — on a high-stakes doc every downstream agent reads, a
  2-hunter swarm (adversarial-general + edge-case-hunter) catches real
  contradictions the author is blind to; verify every finding against disk;
  budget an R2/self-review pass after applying R1 (R1 fixes introduce
  their own bugs).
- Evidence: packet-plumber-architecture-v1 08-07 (40 findings, all legit),
  finlit-architecture-v1 08-03 (R2 caught a defective rounding formula
  written to fix R1), finlit-gdd-amendments 08-05 (silent-edit catches).
- Reasoning: review swarms are standard, but the durable novel kernel is
  "R1 fixes introduce bugs → budget R2" (a recurrence of the rework-
  introduces-blocker theme from a positive-convention angle).

### P7 — Under-locked change: coverage-gap + non-unique guard-pin
- Target: `docs/minion-field-notes.md` (Recurring review findings) · Class: **auto** (applied)
- Change: new entry — (a) COVERAGE-GAP: a changed component lacks the
  per-component assertion test its siblings have; (b) GUARD-PIN NOT UNIQUE:
  a substring-pin isn't unique to its target → regression not pinned. When
  adding/changing a component, mirror siblings' tests + make every guard
  uniquely identify its target.
- Evidence: righttenantryagents-model-flash Perkins r1 N3 08-07 (3 of 5
  Pro agents had no model-assertion test), righttenantry-oauth-posthog-fix
  Perkins r1 W1 08-05 (reset-arm guard not unique → OPEN follow-up).
- Reasoning: distinct from the existing token/PII-across-seams entry
  (over-leaking vs under-locking); a minion-facing Perkins-finding
  taxonomy that costs an open follow-up each time.

### P8 — `ledger set <id> in-review "<url>"` does NOT populate the `pr` field
- Target: `AGENTS.md` gotchas · Class: **auto** (applied)
- Change: new gotcha — `set` updates only `status` + writes an event-row
  note; `pr` is set ONLY by `ledger pr <id> <url>`. Verify with
  `ledger show <id>` first (the table view lies — gotcha #1), and if `pr`
  is genuinely empty, follow the transition with `ledger pr`.
- Evidence: sheep-journals (3+ sightings: packet-plumber-setup #1, gdd #2;
  the lesson then propagated — csp + architecture minions ran `ledger pr`
  themselves). **Verified against the ledger source**: `bin/ledger` lines
  152-164 (`set` → `UPDATE jobs SET status=?`) vs 168-175 (`pr` →
  `UPDATE jobs SET pr=?`).
- Reasoning: appeared to CONTRADICT gotcha #1's 2026-07-21 note ("Gru
  wrote redundant `ledger pr` on a field that WAS set"). The verification
  resolved it: the two gotchas are complementary — #1 = don't FALSELY
  claim pr missing (table lies); P8 = `set` genuinely doesn't set pr, so
  `show`-verify then `pr` if empty. Wording cross-references #1 to keep
  them harmonized.

### P9 — glm-5.2 is a 4th provider-incident class; durable fix = deepseek redirect, not `continue`
- Target: `AGENTS.md` gotchas (amend "Provider incidents come in 3 classes") · Class: **auto** (applied)
- Change: 2026-08-07 addendum — glm-5.2 fails at LAUNCH (bare label →
  opencode, no key) AND mid-turn (429); `continue` may revive a 429 once
  but it re-429s → redirect to deepseek. Full path `zai-coding-cn/glm-5.2`
  auths where bare fails. Also `PI_MODEL` env silently overrides the
  dispatched `--model` (check it / the jsonl when provenance matters). And
  a quota-403 at STARTUP is continue-revivable once quota returns (lighter
  than the mid-work sweep+regenerate doctrine).
- Evidence: finlit-e2-1/e2-7 08-04/05 (auth + 429, deepseek redirect),
  orchestrator-nefario-conflict-sensor 08-05 (PI_MODEL override),
  draft-grace-period-perkins-r1 08-03 (quota-startup continue-revivable).
- Reasoning: the gotcha's 3 classes are all `continue`-or-sweep; glm-5.2's
  durable fix is a MODEL REDIRECT — a distinct recovery. The
  quota-at-startup distinction stops a fresh Silas from over-applying the
  heavy sweep doctrine. (Minion-facing bare-label routing already lives in
  field-notes — not duplicated here.)

### P10 — Killing a stuck/403-dead pi: `exit` fails, C-c isn't uniform → `herdr pane process-info` → `kill <pid>`
- Target: `AGENTS.md` gotchas · Class: **auto** (applied)
- Change: new gotcha — `exit` typed into a dead pi does nothing; C-c
  sometimes leaves the TUI alive. Reliable: `herdr pane process-info
  --pane <p>` → `kill <pid>` (the `node` pid) → pane drops to shell; verify
  session-file state before relaunch.
- Evidence: Silas 08-04 (3 sightings across the quota-403 + glm dead-pane
  sweep). **Verified `herdr pane process-info` exists** (returns
  `foreground_processes[].pid`).
- Reasoning: the gotchas cover DETECTING a dead pi but not KILLING one;
  this is the concrete recovery path, exercised 3× this window.

### P11 — Perkins close-out recovery flavors + deepseek leaves the worktree behind
- Target: `AGENTS.md` gotchas (amend "Perkins can self-close its round row") · Class: **auto** (applied)
- Change: 2026-08-07 addendum — self-close is now the NORM (10/10 rounds
  clean); capture verdict at/before close-out every time. New post-failure
  flavors: dies pre-POST → Silas posts from complete artifacts
  (`body.md`+`consolidated.json`); token-mint fail → fallback-comment.
  deepseek self-closes the ROW but leaves the WORKTREE + lens panes →
  always verify+sweep at close-out.
- Evidence: guarantor-autofill-fix-perkins-r1 08-05 (died pre-post →
  posted from artifacts; token-mint → fallback-comment); sheep-ledger
  round table (10/10 self-close clean); Silas 08-04/06 (deepseek worktree
  left behind, 3rd sighting).
- Reasoning: extends the self-close gotcha from "ledger note the verdict"
  to the full close-out recovery set; the deepseek-worktree corollary
  prevents stale worktrees accumulating.

### P12 — Serialize-hold for pane capacity: pre-create the round row to dedup the sensor
- Target: `AGENTS.md` gotchas · Class: **auto** (applied)
- Change: new gotcha — near the valve cap, hold the next Perkins round
  behind an in-flight one: pre-create its ledger row (`dispatched`, full
  sha in note) so the Perkins sensor doesn't re-fire, release on the
  in-flight round's close-out.
- Evidence: Silas 08-03 (serialize-hold ×3 on #569/#570/#571), 08-04
  (e2-1/e2-7 release), 08-05 (oauth r1) — ≥5 sightings; "now standard ops."
- Reasoning: standard but undocumented; a fresh Silas re-derives it. (This
  absorbs part of dream-2026-08-03's pending P13 user-ack — see UA3.)

### P13 — Launching Gru with BOTH PI_GRU=1 AND PI_SILAS=1 duplicates watcher alerts
- Target: `AGENTS.md` gotchas · Class: **auto** (applied)
- Change: new gotcha — both extensions fire in Gru's pane → alerts echo;
  relaunch `env -u PI_SILAS PI_GRU=1 pi`. Distinct from the cwd-gate gotcha
  (this is the env-var gate).
- Evidence: Gru 08-01 Addendum 3 (journaled, but never filed). The
  dream-2026-08-03 watch item explicitly asked "was the relaunch
  journaled?" — confirmed YES, journaled-but-unfiled.
- Reasoning: closes a previous-dream open loop with a one-line recovery.

### P14 — "Moot on merge" is NOT the default for a mid-flight Perkins round
- Target: `AGENTS.md` gotchas · Class: **auto** (applied)
- Change: new gotcha — terminal merge of an APPROVED PR → sweep in-flight
  round as moot. Deliberate PRE-VERDICT merge → r1 continues to verdict on
  the merged sha as an FYI review (no rework loop unless user says; findings
  → follow-up notes); a fresh post-merge AUDIT round may be dispatched
  (FYI-only, COMMENTED, no cap) and its blockers become NEW jobs. Unsure →
  sweep fast + re-dispatch.
- Evidence: form-e2e-pass / #564 08-03 (user merged pre-verdict → FYI r1 +
  post-merge audit → audit B1 spawned form-nojs-submit-fix); finlit#11 08-05
  (no audit-intent → swept as moot). Two sheep (journals #17 + ledger).
- Reasoning: the merged-mid-round handling is non-obvious and the
  audit-finding-becomes-new-job rule was load-bearing this window. (Absorbs
  more of dream-2026-08-03's pending P13 — see UA3.)

### P15 — In-repo (no-worktree) follow-up jobs: Gru's fresh dispatch = the prior pane is free
- Target: `AGENTS.md` gotchas · Class: **auto** (applied)
- Change: new gotcha — an in-repo follow-up needs the working tree free, so
  Gru's dispatch IS the signal the prior pane is done → close it + sync base
  FIRST (avoids the packet-plumber GDD→architecture working-tree conflict).
  Pane creation = `herdr tab create --cwd <repo>`; close-out closes the pane
  BEFORE deleting the branch (shared working tree).
- Evidence: packet-plumber pipeline 08-06/07 (setup→gdd→architecture→
  sprint-plan, all in-repo; the GDD→architecture conflict was hit, the
  architecture→sprint close-first avoided it).
- Reasoning: in-repo jobs recur (packet-plumber, analysis jobs); the
  "Gru's dispatch = prior pane free" signal and the close-before-branch
  ordering are non-obvious.

---

## User-ack items (NOT applied — structural/policy)

- **UA1 — AGENTS.md gotchas section is growing fast** (now ~17 live →
  ~25 with this pass's 8). It is read every Gru/Silas turn, so length has a
  real context cost. Consider a themed structural split (dispatch /
  Perkins / provider / ledger / pane-forensics subsections) — a structural
  edit, user-ack. If growth continues, propose next dream.
- **UA2 (note) — playbook worktree-bootstrap could symlink `node_modules`
  for JS repos** (Dispatch step 4) — the structural counterpart to P2.
  Currently minion-facing only (field-note); the bootstrap fix would
  prevent the failure class entirely. Low-risk playbook edit.
- **UA3 (note) — dream-2026-08-03 P13 (playbook Perkins-ops codification)
  is partly absorbed** by P12 (serialize-hold) + P14 (moot-on-merge) as
  gotchas. The remainder (formal skip-row policy, proactive-r2+-vs-sensor-
  r1 framing, Silas startup catch-up gap) is still a recommended user-ack
  playbook edit; this window's evidence reinforces it.

---

## Watch items (anecdotes — tracked, not proposed)

**Met the ≥2-sighting bar but demoted to control gotcha-section growth
(promote next window if they recur):**
- Clarify-halt relay + direct-to-pane user turn stales the escalation →
  stand Gru down (3 sightings 08-06; channel-hygiene, Silas-judgement
  territory).
- Closing a Perkins parent pane cascades its lens children → don't
  error-loop (2 sightings 08-05/06; the "watcher pane-vanished self-
  inflicted" 2nd sighting — niche Perkins headless parenting).
- Co-touch / file-overlap check at PR merge → conditional rebase heads-up
  (3 sightings 08-03; working practice, prevents spurious rebases).

**Single-sighting, tracked:**
- `gh repo delete` needs `delete_repo` scope — not grantable non-
  interactively from a pane (mssoka stray-repo 08-06).
- Close-out `pull --ff-only origin <base>` assumes the main checkout sits
  on `<base>`; diverged → don't force, report (RT-Agents 08-07).
- `git checkout -- <file>` after a sed-tamper wipes ALL uncommitted work —
  revert tamper with sed on the exact line (draft-grace-period 08-03).
- `gh pr create --body "$(heredoc)"` chokes on quotes/backticks →
  `--body-file` (packet-plumber-setup 08-06; reusable shell lesson).
- `HERDR_*` env vars go STALE across Herdr restarts → `herdr pane current
  --current` before splitting (finlit-architecture 08-03).
- Linked-worktree: `test -d .git/rebase-merge` is WRONG (`.git` is a
  gitfile) → `git status` is the authority (finlit-e2-7 08-05).
- Lavish mid-review file rewrite → browser serves CACHED old version →
  `dom_snapshot` is ground truth; `--reopen` or reload+verify-next-poll
  (gcp-cost-analysis 08-06).
- Invariant TEST only proves value if it BITES — negative control (inject
  X, confirm red, revert) + no-op-via-byte-diff (csp-posthog 08-06;
  single job but generalizable — likely promote next dream).
- Wrong-repo / no-knob clarify → halt + re-dispatch + reframe scope with
  data (agent-model-flash arc 08-06; partly covered by P3).
- `rg` through the harness MASKS `gemini-*` tokens as `n.*`; `cat`/`read`
  shows real strings (agent-model-flash 08-06).
- Perkins headless lenses spawn at ~/code → sessions land in Gru's session
  dir (benign unless a lens acts on Gru orders) (Silas 08-05).
- `custom_message` count == 0 does NOT mean silas.ts unarmed (it injects
  via systemPrompt augmentation) — refines the pane-forensics gotcha
  (Silas 08-05).
- `gh pr diff` 406s on huge rename diffs → generate locally (form-e2e-pass
  08-03; effectively 1 incident).
- Various Godot engine one-offs (disabled-Button swallows clicks; FileAccess
  flush; root-window 64×64 vs content; GDScript 4.7 `rfind`/ternary-
  inference), Sentry/CSP one-offs (classic vs new CLI token; junk CSP
  reports), Chrome autofill internals (kTypeValueFormFillingLimit, CDP
  Autofill), RT repo specifics (`(xmax=0) AS is_new`; analytics-bridge
  4-place guards; PostHog `_is_bot()` drops HeadlessChrome; vacancy
  `closed_notified_at`; copy-sheet re-introduction; `.env.test` tracked;
  rebase negative-pins re-pointing) — all single-sighting, repo/domain-
  specific; retained in the sheep shards for reference.

**Previous watch items checked — NO 2nd sighting this window (still
watching):** non-blocking clarify (escalate without status flip); ledger
event text strips `$` (only prose-escaping found); `gleam format` all
packages; form.js `_form_loaded_at` IIFE; upload-slot `.field-error`
display:flex; Supabase security-definer RLS; test-DB `:54323` debris.

**Gru journal gap (recurring flag):** Gru has NO journal files for
08-03..08-07 (5 days). User rulings + strategic intent for that span live
ONLY in Silas's journal + the ledger (mitigated by the dual-read journals
sheep). Previous dream also flagged a Gru backfill gap — still open; Gru
owns journals.

---

## Pruned / rejected candidates (with why)

- **sheep-journals "#2 glm-5.2 bare label"** — **already in store**
  (field-notes "glm-5.2 bare-label routing bug" section + a Recurring
  entry). The sheep was briefed only on gotchas, not field-notes, so it
  missed it. NOT re-proposed; the NEW operational framing (4th incident
  class → deepseek redirect) IS new → that's P9.
- **sheep-journals "#21 edit atomicity"** — **already in store**
  (dream-2026-08-03 P1, field-notes Tooling traps). Same briefing-scope
  miss. NOT re-proposed. (Cross-file-batch corollary from form-copy-revision
  is already covered by "atomic per call.")
- **sheep-ledger "gcp-cost no-PR compliance gap"** — **already in store**
  (AGENTS.md gotcha added 2026-08-07). sheep-ledger correctly noted this.
- **sheep-journals "#13 lavish minion-steward as primary pattern"** —
  state.json stranding is **already in field-notes**; the "always dispatch
  a minion to own the lavish session" framing is playbook-level. Demoted to
  report-only to avoid over-codifying (same reasoning dream-2026-08-03 used
  to reject briefing lens-guards).
- **sheep-journals "#9 Perkins lenses spawn at ~/code (benign)"** —
  hypothetical failure ("a lens ever acts on Gru orders"); low value.
  Watch only.
- **sheep-journals "#1 set≠pr (initially appeared to contradict gotcha
  #1)"** — NOT rejected: verified against ledger source → REAL and
  complementary to #1 → became P8 (verification story in P8 reasoning).
- **"Hold-release for pane capacity" (dream-2026-08-03 watch)** — promoted
  to P12 (≥5 sightings).
- **"Watcher pane-vanished self-inflicted" (watch)** — 2nd sighting
  confirmed (lens cascade) but demoted to watch (niche); see watch list.
- **"Parse-test strip-types" (watch)** — promoted to P4.
- **"Dual-gate echo" (watch)** — promoted to P13.
- **"Provider instability clustering" (watch)** — absorbed into P9.

---

*End of dream report — 2026-08-07. Store copies diff-ready at
`_bmad-output/memory/dream-2026-08-07/store/`. Silas close-out: apply the
15 auto edits, escalate UA1–UA3 to Gru, write the `last-dream` marker,
`ledger set dream-2026-08-07 done`, commit `dream 2026-08-07: <one-liner>`.*
