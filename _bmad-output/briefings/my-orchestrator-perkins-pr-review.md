# Briefing: my-orchestrator-perkins-pr-review

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion
standing orders"** first — it governs clarify halts, ledger self-reporting,
mega-minions, env files, and PR etiquette. Branch: `perkins-pr-review`,
base: `main`, PR target: `main`.

## Task

Implement **Perkins — automated PR review** for the Gru orchestrator, per the
spec at `/Users/moses/code/docs/perkins-pr-review-plan.md`. That document is
the authoritative spec — read it fully before writing code. It is currently
**untracked in the main checkout**: copy it into your worktree at
`docs/perkins-pr-review-plan.md` and include it in your PR.

Scope = plan components 1–4 (component 5, GitHub App setup, is already done):

1. **`bin/ledger`** — add `pr_review INTEGER NOT NULL DEFAULT 0` column:
   fresh schema + `ALTER TABLE` migration in `init()` (guard with
   `PRAGMA table_info`), add to `COLUMNS`, update the usage docstring.
2. **`.pi/extensions/nefario-watch.ts`** — sensor #5 (Perkins sensor) inside
   the existing `prTick` non-terminal branch, exactly per the plan's
   Component 2: extend `inReviewJobs()` with `pr_review`; durable,
   ledger-driven dedup via round rows (`parent = <job>`, `note` carries
   `sha=<full-sha>`); skip when a round is in flight or the sha was already
   reviewed; in-memory `perkinsAlerted` map (mirrors `ciAlerted`) against
   per-tick re-alerts; round cap 3 → once-per-sha escalation message;
   inject the dispatch message (followUp + triggerTurn; nextTurn on the
   initial pass). Update the extension's header comment (sensor list +
   alert policy). Detection-only: never write the ledger, never touch panes.
3. **`bin/perkins-token`** — GitHub App installation-token minter, python3
   stdlib + `openssl` CLI, per Component 3: config at
   `~/.config/perkins/config` (`app_id`, `key_path`,
   `installation_id_<login>=…`), JWT (RS256) →
   `POST /app/installations/{id}/access_tokens` via `urllib`, per-owner
   cache (`token-cache-<owner>`, 0600, reuse >5 min), `--owner <login>`
   (optional when one installation configured; unknown owner → non-zero
   exit), `--refresh`, `--check` (mint + `GET /installation/repositories`,
   print visible repo names). Non-zero exit + one-line stderr on any
   failure.
4. **`docs/orchestration-playbook.md`** — per Component 4: Perkins in the
   naming block; intake step for the `pr_review` opt-in flag; the full
   **"Perkins (automated PR review)"** section (Gru dispatch sequence,
   Perkins standing orders + briefing requirements, round close-out,
   concurrency note, re-review semantics note); close-out amendments if
   needed.

## Repo map (my-orchestrator = /Users/moses/code)

- `bin/ledger` — job-ledger CLI (python3 stdlib). DB is hardcoded to
  `/Users/moses/code/_bmad-output/orchestrator.db` (the LIVE ledger).
- `.pi/extensions/nefario-watch.ts` — pi project extension, loads only in
  the Gru session; currently running version stays live until Gru restarts.
- `.pi/extensions/gru.ts` — Gru enforcement extension. Do NOT modify.
- `docs/orchestration-playbook.md` — operational doc you'll amend.
- `docs/perkins-pr-review-plan.md` — THE SPEC (untracked; copy in).
- `_bmad-output/` — runtime state (db, briefings, backups). Never commit.
- `~/.config/perkins/` — app config + private key (outside repo).
  `bin/perkins-token` reads these at runtime. NEVER print the key, never
  copy it anywhere, never commit it. Reading `config` is fine.

## Env / bootstrap

- `_bmad` was copied from the main checkout; `.env` was **symlinked** —
  treat it read-only (standing orders).
- Your worktree's `bin/ledger` still points at the LIVE DB. **All ledger
  functional testing goes through a throwaway copy**: `cp bin/ledger
  /tmp/ledger-test` with `DB`/`BACKUPS` sed'd to `/tmp`, seeded from a copy
  of the live DB. Do not run migration experiments against the live DB.

## Verify (the done bar)

1. `python3 -m py_compile bin/ledger bin/perkins-token` clean.
2. Ledger migration on the throwaway copy: column added, pre-existing rows
   read `pr_review=0`, `add`/`show` round-trip `pr_review=1`, second run
   idempotent.
3. `/Users/moses/code/bin/perkins-token --check` (your worktree copy)
   **lists `solarity-services/RightTenantry`** — live validation of the app
   setup (read-only, safe). Cache file created with 0600; rerun reuses it.
4. Sensor SQL dedup logic exercised against a /tmp DB copy with fabricated
   round rows: in-flight skip, same-sha skip, cap escalation, dispatch case.
5. `npx -y esbuild .pi/extensions/nefario-watch.ts --outfile=/dev/null`
   parses clean (syntax floor; tsc only if you can resolve the pi types).
6. Playbook read-through: new sections internally consistent with the plan.
7. `gh pr create --base main` — PR body includes the **Decisions &
   rationale** section (standing orders) and notes the manual dry-run of
   Perkins on RightTenantry PR #540 as the post-merge validation step.

## Model policy

Unset — pi default resolution. Spawn any mega-minions with plain `pi`.

## Skills policy

- **Your workflow skill: `bmad-quick-dev`** — follow its step files, with
  the two orchestration overrides from standing orders (step-01 clarify →
  numbered questions then HALT for Gru's relay; internal approval
  checkpoints pre-approved).
- Mega-minions (optional, e.g. a pre-PR review swarm):
  `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`.
  Max 10 concurrent; close every one before finishing.
