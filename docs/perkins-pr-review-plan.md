# Perkins — automated PR review (implementation plan)

Status: **approved direction, pre-implementation**. Naming + decisions locked
2026-07-22. This doc is the spec for the implementation job; the briefing can
point at it directly.

## Naming

- **Perkins** — the PR-review minion (after Mr. Perkins, Bank of Evil: Gru
  pitches a plan, Perkins approves it or sends it back). One Perkins pane per
  review round, label `perkins-<slug>-r<N>`, ledger id `<job-id>-perkins-r<N>`.
- The cast is now: **Gru** orchestrates, **minions** build, **mega-minions**
  assist a minion, **Perkins** reviews and signs off. The human still merges.

## Locked decisions

| # | Decision | Choice |
|---|----------|--------|
| 1 | Trigger | **A2** — new 5th sensor in nefario-watch (self-healing across Gru restarts; new head sha re-triggers) |
| 2 | Approval policy | **C1** — Perkins may APPROVE and REQUEST_CHANGES; the human remains the only merger |
| 3 | Round cap | **3 automated rounds per PR**, then escalate to the human |
| 4 | Swarm | **Full 7 perspectives** (per the `code-review` skill) |
| 5 | Scope | **GitHub only** (consistent with the existing review sensor) |
| 6 | Activation | **Opt-in per job** via briefing flag → ledger column `pr_review`. Big changes get Perkins; small changes rely on quick-dev's built-in review |
| 7 | Identity | **GitHub App** (`perkins-review`, owned by `solarity-services`, visibility "any account" — installed on `solarity-services` only for now; reviews post as `perkins-review[bot]`) |

## Why a GitHub App (context for the implementer)

`gh` on this machine authenticates as `mssoka`, and minions open PRs as
`mssoka` — GitHub rejects formal reviews (APPROVE / REQUEST_CHANGES) on your
own PRs with 422. A GitHub App gives Perkins its own actor (`perkins-review[bot]`),
short-lived installation tokens, and org-grade scoping. The whole identity
mechanism is one indirection — `GH_TOKEN=$(bin/perkins-token) gh pr review ...`
— so it can be swapped without touching anything else.

## End-to-end flow

```
minion opens PR, ledger in-review + pr_review=1
  → Perkins sensor (nefario-watch, 5-min tick) sees OPEN PR, head sha S,
    pr_review=1, no in-flight round, no prior round on S
  → injects "Perkins review pending" → Gru dispatches perkins-<slug>-r1
  → Perkins: detached worktree @ S → 7 mega-minion lenses → JSON findings
    → Gru-side verification pass → consolidate → verdict
    → GH_TOKEN=$(bin/perkins-token) gh pr review --approve|--request-changes
  → Perkins closes its mega-minions, ledger done, exits
  → existing review sensor detects the perkins-review[bot] review:
      CHANGES_REQUESTED → relay to implementing minion (existing behavior)
      APPROVED          → notify human "merge when ready" (existing behavior)
  → minion fixes, pushes (sha S′), sets ledger in-review
  → Perkins sensor re-alerts on S′ → round 2 … cap 3 → then escalate to human
```

No changes needed to the existing review sensor, CI sensor, PR watcher, or
close-out flow. Perkins *speaks GitHub*; everything downstream already works.

---

## Component 1 — `bin/ledger`: `pr_review` column

- Add `pr_review` to `COLUMNS`; fresh schema gets
  `pr_review INTEGER NOT NULL DEFAULT 0`.
- Migration for existing DBs in `init()`: check `PRAGMA table_info(jobs)`;
  if missing, `ALTER TABLE jobs ADD COLUMN pr_review INTEGER NOT NULL DEFAULT 0`.
- No new subcommands. Rounds are plain rows with `parent` set; sha/round live
  in `note` (`sha=<full-sha> round <N>`). Queries the sensor needs are plain
  SQL against the DB (it already execs sqlite3 directly).
- Acceptance: `ledger add x pr_review=1` and `ledger show x` display it;
  pre-existing rows read `0`; `ledger` table view unchanged.

## Component 2 — nefario-watch: sensor #5 (Perkins sensor)

Lives inside the existing `prTick` non-terminal branch (after the review
sensor), reusing `prInfo()`'s `headSha`. Behavior:

1. Extend `inReviewJobs()` SELECT with `pr_review` (keep it generic — the
   other sensors share this query). Perkins logic only runs for
   `pr_review = 1` jobs.
2. Load rounds from the ledger (durable dedup — survives Gru restarts,
   unlike the in-memory maps):
   `SELECT id, status, note FROM jobs WHERE parent = ?`
   - **In flight**: any round with `status != 'done'` → skip silently.
   - **Sha already reviewed**: any round whose `note` contains the current
     head sha → skip silently.
3. **In-memory** `perkinsAlerted: Map<job_id, sha>` (mirrors `ciAlerted`) so
   a pending dispatch doesn't re-alert every 5 min while Gru works.
   Re-arms when the sha changes.
4. **Round cap**: `rounds = count(children)`. If `rounds >= 3` and a new sha
   arrives → inject the escalation message (once per sha, in-memory
   `perkinsEscalated` map): *"Perkins round cap (3) reached for `<job>` —
   human review needed: `<pr>`"*.
5. Otherwise inject (deliverAs `followUp` + `triggerTurn`; `nextTurn` on the
   initial pass):
   ```
   [nefario-watch] Perkins review pending:
   - <job-id>: <pr-url> — head <short-sha> — dispatch Perkins round <N>
     per playbook 'Perkins (automated PR review)'. Ledger round rows:
     parent=<job-id>, note must carry sha=<full-sha>.
   ```
6. Update the extension's header comment (sensor list + alert policy) —
   that comment is the operational doc a cold Gru session reads.

Detection-only contract unchanged: the sensor never writes the ledger and
never touches panes; Gru dispatches.

## Component 3 — `bin/perkins-token`: installation-token minter

Python3 stdlib + `openssl` CLI (same constraints as `bin/ledger`):

- Reads config from `~/.config/perkins/config` (0600, outside any repo):
  `app_id`, `key_path` (default `~/.config/perkins/app-key.pem`), and one
  installation id per installed account: `installation_id_<login>=…`.
  Currently only `installation_id_solarity-services` exists; adding the
  `mssoka` installation later is one install click + one config line.
- `bin/perkins-token --owner <login>` selects the installation for the
  repo's owner (Gru/Perkins parse the owner from the PR URL — the ledger
  has it). With exactly one installation configured, `--owner` is optional;
  an owner with no configured installation → exit non-zero → comment
  fallback (below).
- Mints a JWT (RS256, `openssl dgst -sha256 -sign`), exchanges it at
  `POST /app/installations/{installation_id}/access_tokens`
  (via `urllib`; `api.github.com`), prints the token to stdout.
- Caches **per installation** at `~/.config/perkins/token-cache-<owner>`
  (0600) with `expires_at`; reuses while >5 min remain (installation tokens
  live 1h). `--refresh` bypasses.
- `--check`: mint a token per configured installation and
  `GET /installation/repositories` — prints which repos each can see. Used
  for setup validation and dry-run.
- Exit non-zero with a one-line stderr reason on any failure (missing key,
  unknown owner, 401, network) — Perkins maps that to the comment fallback
  (below).

## Component 4 — playbook: "Perkins (automated PR review)" section

Updates to `docs/orchestration-playbook.md`:

1. **Naming block**: add Perkins (per above).
2. **Intake**: new step — for large/risky jobs, opt in to Perkins: put
   `pr_review: true` in the briefing and pass `pr_review=1` in `ledger add`.
   Default stays off.
3. **Perkins section** with the Gru dispatch sequence:

   1. On the sensor message, verify: job still `in-review`; PR still OPEN;
      refresh head sha (`gh pr view <pr> --json state,headRefOid`) — use the
      freshest sha, not the alerted one.
   2. Round `N` = existing round rows for the job + 1. If N > 3 → escalate
      to the user instead of dispatching (belt-and-braces; sensor already
      enforces).
   3. `git -C <repo_root> fetch origin <slug>` then
      `git -C <repo_root> worktree add --detach \
        ~/.herdr/worktrees/<repo>/perkins-<slug>-r<N> <sha>`
      — detached at the exact reviewed sha, immune to mid-review pushes.
      No env/bootstrap (read-only review).
   4. Write briefing `_bmad-output/briefings/perkins-<job-id>-r<N>.md`
      (required sections below).
   5. Pane into the orchestrator workspace (panes-first rule), label
      `perkins-<slug>-r<N>`; launch `cd <worktree> && pi` and hand over:
      *"Read the playbook 'Perkins standing orders' and the briefing at
      `<path>`, then begin."*
   6. `ledger add <job-id>-perkins-r<N> parent=<job-id> repo=<repo> \
        repo_root=<root> slug=perkins-<slug>-r<N> worktree=<wt> \
        pane_id=<p> tab_id=<t> pr=<pr> briefing=<path> \
        note="sha=<full-sha> round <N>"`
   7. **Round close-out** (on Perkins pane-done, reported by the pane
      watcher): verify the review actually posted
      (`gh pr view <pr> --json reviews` — latest by `perkins-review[bot]`); then
      `ledger set <round-id> done "<verdict + review-url>"` + `clear-pane`;
      close panes (Perkins must have badged out its mega-minions — verify
      with `herdr agent list`); `git worktree remove --force <wt>`.
      If the review did NOT post (crash/token failure): flip the same round
      row back to `dispatched` with the new pane id and retry once; second
      failure → `blocked` + tell the user.

4. **Perkins standing orders** (also pasted into every Perkins briefing):

   - You are Perkins. You review; you never fix, push, or merge. You never
     touch the implementing minion's worktree or pane.
   - Context: PR URL + number, reviewed sha, repo_root, the **original job
     briefing** and **GitHub issue** (your spec), and your cwd — a detached
     worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
   - Save the canonical diff first:
     `gh pr diff <pr>` → `_bmad-output/perkins/<job-id>/r<N>/diff.patch`.
     Every lens reviews these identical bytes.
   - Spawn the **7 lenses** as mega-minions in one wave
     (`herdr pane split --current`, label `mm-<lens>-r<N>`), per the
     `code-review` skill's reviewer definitions: **blind** (diff only — no
     repo access, no framing), **edge**, **acceptance** (briefing + issue as
     spec), **security**, **architecture**, **codebase**, **tests**. Each
     writes one JSON findings array (skill schema: source/severity/category/
     title/location/evidence/detail/recommended_fix, accuracy mandate
     verbatim) to `_bmad-output/perkins/<job-id>/r<N>/<lens>.json`, then
     stops. You MUST close every mega-minion pane before finishing.
   - **Verification pass (mandatory, per the skill's Step 3b):** every
     finding is presumed false-positive until you re-verify it against the
     worktree yourself. Discard rejected findings; demote unverifiable
     blockers to `[unverified]` warnings. Record the counts.
   - Consolidate: dedupe on (title, location), merge sources, triage into
     blocker/warning/note, surface the reviewer-agreement set first.
   - **Verdict → review event** (C1):
     - 0 blockers → `--approve`
     - 1–3 blockers → `--request-changes`
     - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
     - **Degraded guard:** any lens failed AND zero findings remain → do NOT
       approve; `--comment` instead and flag Gru ("incomplete review").
   - Post as the app (owner parsed from the PR URL):
     `GH_TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>) \
       gh pr review <pr> --<event> --body-file <body.md>`
     Token failure → fall back to `gh pr comment <pr> --body-file <body.md>`,
     note `fallback-comment` in your ledger note, and call it out in your
     final message.
   - Body format:
     ```
     ## 🤖 Perkins automated review — round <N> of 3
     **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
     **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

     ### Blockers (n) / ### Warnings (n) / ### Notes (n)
     ### Reviewer agreement
     **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

     _Address findings and push — I re-review automatically on the new sha.
     After round 3, the human takes over._
     ```
   - Before posting, re-fetch `headRefOid`. If it moved mid-review, post
     anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
     will follow" in the body.
   - Self-report: `ledger set <round-id> working` at start; final message =
     verdict + review URL + findings counts.
   - Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
     fixing is the implementing minion's job, triggered by the review relay.

5. **Concurrency**: a Perkins round = 8 panes (Perkins + 7 lenses). Two
   concurrent rounds ≈ 18 panes + Gru — against the ~20 safety valve, so
   serialize rounds when the workspace is crowded (hold the second dispatch
   and tell the user).

6. **Re-review semantics note** (amend the tracking section): when the
   review sensor relays Perkins' CHANGES_REQUESTED, the minion's usual
   "re-request review" step is unnecessary — the new sha is what re-triggers
   Perkins. Minion just fixes, pushes, and sets the ledger back to
   `in-review`.

## Component 5 — GitHub App setup (human task, ~20 min)

Only the user can do this (org admin + browser):

1. github.com → Settings → Developer settings → GitHub Apps → New (owner:
   `solarity-services`).
   - Name: `Mr Perkins` (fallback `perkins-review` if taken) · Homepage:
     `https://github.com/mssoka/my-orchestrator` (cosmetic)
   - Callback/Setup URLs: none · **Webhook: Active unchecked**
   - Permissions (Repository only): **Pull requests: read & write**,
     **Contents: read** (Metadata: read is auto-added)
   - **Where can this GitHub App be installed? → Any account** — required
     so it can be installed on both `solarity-services` and `mssoka`.
2. Generate a private key → save as `~/.config/perkins/app-key.pem` (0600).
3. **Install** on `solarity-services` → selected repos (RightTenantry,
   add more later). Note the **installation id** from the installation URL
   (`github.com/organizations/solarity-services/settings/installations/<id>`).
   *(Personal `mssoka` repos deferred — to add later: app public page →
   Install → choose `mssoka`, then add `installation_id_mssoka=…` to the
   config.)*
4. Write `~/.config/perkins/config`: `app_id=… key_path=…`
   `installation_id_solarity-services=…`
5. Validate: `bin/perkins-token --check` lists the installed repos.

## Rollout

1. **App setup** (human, above) — can happen in parallel with the build.
2. **Dispatch the implementation minion** (repo `my-orchestrator`, base
   `main`, briefing points at this doc). Scope: components 1–4.
   Dogfood note: *this* PR can't be Perkins-reviewed end-to-end (the sensor
   ships in it; the Gru extension loads at session start). Validate on #540
   instead (step 3), and after merge + Gru restart the sensor is live.
3. **Dry run on PR #540** (open, authored by `mssoka` — the exact self-review
   case): Gru manually dispatches `righttenantry-ai-reference-calls-research-perkins-r1`
   per the playbook sequence (no sensor needed). Validates: swarm quality,
   token minting, review posts as `perkins-review[bot]`, the existing review sensor
   detects and classifies it, the relay reaches the implementing minion.
4. **Go live**: after the implementation PR merges, pull main in
   `/Users/moses/code` and restart the Gru session (extensions load at
   session start). From then on, any job dispatched with `pr_review=1` gets
   Perkins automatically. Optionally flip the flag on the
   `ai-reference-calls-research` job to make the dry run sensor-driven too.

## Failure modes (spec'd above, collected)

| Case | Behavior |
|------|----------|
| Gru down when PR opens | Sensor re-alerts after restart (durable ledger dedup — no duplicate rounds, no lost rounds) |
| Push mid-review | Perkins posts against the sha it reviewed, notes the drift; new sha triggers the next round |
| Perkins crash pre-post | Gru flips the same round row back to `dispatched` and retries once; then `blocked` + user |
| Token mint failure | Perkins falls back to `gh pr comment`, flags `fallback-comment` in ledger + final message |
| Round cap (3) hit, new sha | Escalation message to the human; no r4 |
| Perkins' own review | Does not retrigger Perkins (trigger is the sha, not review events) |
| PR merged while round in flight | Sensor skips terminal states; Gru abandons the round (close panes + worktree, round row → `done` with note) |
| GitLab PR URL | Sensor never matches (PR_URL regex) — silent, as today |

## Open items for the user

1. ~~App visibility~~ — resolved: `perkins-review` created ("any account"),
   installed on `solarity-services` only for now.
2. Flip `pr_review=1` on the existing #540 job so the dry run is
   sensor-driven, or keep the dry run manual?
