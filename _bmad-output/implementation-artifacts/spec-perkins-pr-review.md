---
title: 'Perkins — automated PR review (components 1–4)'
type: 'feature'
created: '2026-07-22'
status: 'done'
baseline_commit: '8b3e3112232e9206c29ba9ab79bec34c495ef955'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Gru detects merges/CI/reviews but nothing *produces* reviews —
the human is the only reviewer, and `gh` (as `mssoka`) cannot formally
review its own PRs (GitHub 422). Review bottlenecks on the human.

**Approach:** Implement Perkins per the authoritative spec
`docs/perkins-pr-review-plan.md` (copy it into the repo — currently
untracked): a `pr_review` opt-in ledger flag, a 5th nefario-watch sensor
that detects reviewable head shas, a GitHub-App token minter
(`bin/perkins-token`), and the playbook's Perkins operating section.
Component 5 (app setup) is already done; the dry run on RightTenantry PR
#540 is post-merge, not part of this change.

## Boundaries & Constraints

**Always:**
- Follow `docs/perkins-pr-review-plan.md` exactly — decisions are locked.
- `bin/ledger` + `bin/perkins-token`: python3 stdlib only (+ `openssl` CLI
  for perkins-token); one-line stderr + non-zero exit on failure.
- Sensor is detection-only: never writes the ledger, never touches panes.
- Durable dedup via ledger round rows (`parent=<job>`, `note` carries
  `sha=<full-sha>`); in-memory maps only suppress per-tick re-alerts.
- Never print/copy/commit the app private key; never commit `_bmad-output/`.
- All ledger testing on a throwaway copy (`DB`/`BACKUPS` sed'd to /tmp) —
  never run migrations against the live DB.

**Ask First:** none — spec approved, internal checkpoints pre-approved.

**Never:**
- Do not modify `.pi/extensions/gru.ts`.
- Do not change the `ledger` table view columns (plan: unchanged).
- Do not add GitLab support, retry logic for crashed Perkins panes, or any
  pane/ledger writes in the extension.
- Do not merge the PR.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| OPT_IN | `ledger add x pr_review=1` | row stores 1; `show` displays it; table view unchanged | unknown column rejected as today |
| MIGRATE | pre-existing DB without column | init() ALTERs; old rows read 0; rerun idempotent | guard via `PRAGMA table_info` |
| SENSOR_SKIP_INFLIGHT | round row status != done | no alert | silent |
| SENSOR_SKIP_SAME_SHA | round note contains head sha | no alert | silent |
| SENSOR_DEDUP_TICK | alerted sha, no round row yet | no repeat (in-memory map) | re-arms on sha change |
| SENSOR_CAP | 3 rounds + new sha | escalation once per sha | no r4 dispatch message |
| SENSOR_DISPATCH | pr_review=1, OPEN PR, fresh sha | dispatch message w/ round N + full sha | rides shared followUp injection |
| TOKEN_MINT | valid config/key | bare token on stdout | one-line stderr, exit≠0 |
| TOKEN_CACHE | cache <55 min old | reused, no network; file 0600 | `--refresh` bypasses |
| TOKEN_OWNER | `--owner` unknown / omitted with >1 installation | exit≠0 | omitted OK iff 1 installation |
| TOKEN_CHECK | `--check` | lists repos per installation | any failure → exit≠0 |

</frozen-after-approval>

## Code Map

- `bin/ledger` — add `pr_review` to COLUMNS, SCHEMA, init() migration, usage docstring.
- `.pi/extensions/nefario-watch.ts` — sensor #5 in `prTick` non-terminal branch; extend `inReviewJobs()`/`ReviewJob` with `pr_review`; header comment (sensor list + alert policy). `ciAlerted` is the pattern to mirror.
- `bin/perkins-token` — NEW executable: JWT(RS256, openssl) → installation token; per-owner cache; `--owner`/`--refresh`/`--check`.
- `docs/orchestration-playbook.md` — naming block + Perkins; intake opt-in step; "Perkins (automated PR review)" section (dispatch sequence, standing orders, round close-out, concurrency, re-review semantics); tracking section: four sensors → five.
- `docs/perkins-pr-review-plan.md` — copy from main checkout (untracked there) into the PR.
- `~/.config/perkins/config` — exists (app_id=4366368, installation_id_solarity-services); read-only input.

## Tasks & Acceptance

**Execution:**
- [x] `docs/perkins-pr-review-plan.md` — copy from `/Users/moses/code/docs/` — spec must ship with the PR.
- [x] `bin/ledger` — `pr_review INTEGER NOT NULL DEFAULT 0`: fresh schema + guarded ALTER in `init()`, COLUMNS, docstring — Component 1.
- [x] `.pi/extensions/nefario-watch.ts` — Perkins sensor per Component 2 + header comment — durable ledger dedup, in-flight/same-sha skip, `perkinsAlerted`, cap-3 escalation (`perkinsEscalated`), dispatch message.
- [x] `bin/perkins-token` — Component 3 token minter.
- [x] `docs/orchestration-playbook.md` — Component 4 amendments.
- [x] Ephemeral /tmp harness — exercise sensor SQL/dedup paths (in-flight, same-sha, cap, dispatch) — repo has no extension test infra (see deferred-work); harness is NOT committed.

**Acceptance Criteria:**
- Given a pre-existing ledger DB, when the new `bin/ledger` runs any command, then `pr_review` exists, old rows read 0, and a second run is a no-op.
- Given `pr_review=1` and an OPEN PR with unreviewed head sha, when prTick runs, then exactly one dispatch alert per sha fires; in-flight round, reviewed sha, or cap → correct skip/escalation.
- Given the live `~/.config/perkins`, when `bin/perkins-token --check` runs, then it lists `solarity-services/RightTenantry`, cache is 0600, rerun reuses it.
- Given the amended playbook, when read cold, then the Perkins section is internally consistent with the plan doc.

## Design Notes

- Perkins alerts ride prTick's single shared `sendMessage` (one injection
  per tick, the followUp/nextTurn semantics the plan specifies); the plan's
  message text becomes a `Perkins review pending:` entry inside it — avoids
  double wake-ups when CI/review alerts co-fire.
- Round rows loaded per job: `SELECT id, status, note FROM jobs WHERE
  parent = ?` (sqlite3 `-json`, same as existing helpers).
- JWT: `iat=now-60`, `exp=now+600`; base64url no-pad; `openssl dgst
  -sha256 -sign <key>`; cache JSON `{token, expires_at}` (0600), reused
  while >5 min remain.

## Verification

**Commands:**
- `python3 -m py_compile bin/ledger bin/perkins-token` — clean.
- `cp bin/ledger /tmp/ledger-test` (DB/BACKUPS sed'd to /tmp, seeded from live-DB copy) — migration: column added, old rows 0, `add`/`show` round-trip 1, rerun idempotent.
- `bin/perkins-token --check` (worktree copy) — lists `solarity-services/RightTenantry`; cache 0600; rerun reuses cache.
- `npx -y esbuild .pi/extensions/nefario-watch.ts --outfile=/dev/null` — parses clean.
- /tmp harness (stubbed pi.exec, /tmp DB, fabricated round rows) — assert in-flight skip, same-sha skip, cap escalation, dispatch case.

**Manual checks (if no CLI):**
- Playbook read-through: naming/intake/Perkins/tracking sections consistent with `docs/perkins-pr-review-plan.md`.

## Suggested Review Order

**Perkins sensor (the core logic)**

- The sensor itself: durable round-row dedup, in-flight/same-sha skip, cap escalation, dispatch message.
  [`nefario-watch.ts:488`](../../.pi/extensions/nefario-watch.ts#L488)

- Round-row query with `-perkins-r%` discriminator; null-on-error so transient DB failures never masquerade as "zero rounds".
  [`nefario-watch.ts:302`](../../.pi/extensions/nefario-watch.ts#L302)

- Missing-column fallback keeps merge/CI/review sensing alive on a pre-migration DB; Perkins stays off until `ledger` migrates.
  [`nefario-watch.ts:263`](../../.pi/extensions/nefario-watch.ts#L263)

- CHANGES_REQUESTED relay now carries the Perkins exception (skip re-request — new sha re-triggers).
  [`nefario-watch.ts:97`](../../.pi/extensions/nefario-watch.ts#L97)

**Ledger opt-in flag**

- Fresh schema + guarded, race-tolerant ALTER migration.
  [`ledger:68`](../../bin/ledger#L68)

- `pr_review` restricted to 0/1 at `add` — silent opt-in failure was the likely operator error.
  [`ledger:142`](../../bin/ledger#L142)

**Token minter (new executable)**

- RS256 JWT via openssl CLI, 9-min exp margin for clock skew.
  [`perkins-token:114`](../../bin/perkins-token#L114)

- CA-roots fallback chain (python.org macOS builds ship with zero roots — this bit me live).
  [`perkins-token:48`](../../bin/perkins-token#L48)

- Best-effort cache write; HTTP errors keep GitHub's response body; `--check` continues across installations.
  [`perkins-token:179`](../../bin/perkins-token#L179)

**Playbook operating docs**

- Gru dispatch sequence + round close-out with executable retry SQL and blocked-round recovery.
  [`orchestration-playbook.md:240`](../../docs/orchestration-playbook.md#L240)

- Perkins standing orders: mint-before-review ordering, absolute artifact paths (round worktree is destroyed at close-out).
  [`orchestration-playbook.md:299`](../../docs/orchestration-playbook.md#L299)

- Intake opt-in step 7 and the tracking section's fifth sensor entry.
  [`orchestration-playbook.md:74`](../../docs/orchestration-playbook.md#L74)

**Spec artifact**

- The authoritative spec, shipped with the PR (bot-login normalized to `perkins-review[bot]`).
  [`perkins-pr-review-plan.md:1`](../../docs/perkins-pr-review-plan.md#L1)
