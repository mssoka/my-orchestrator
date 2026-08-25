# Briefing — righttenantry-refcheck-followup-607 (#607 follow-up intake)

- **Job id:** `righttenantry-refcheck-followup-607`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-followup-607`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (app-surface hardening + an architecture-level guard — the U3
  scope guard reserves `pr_review=0` for CI/ops-tooling only).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` (RC4.1–4.4 merged — the RC4 series is complete). Rebase onto
  origin/develop if it moves mid-work; clean-rebase hygiene (`git diff --check` before
  force-with-lease).

## Mission (GitHub issue #607 — the five carried advisories)

The RC4 line shipped; Perkins' carried warnings are filed in **#607** (read the issue body —
it is the canonical spec). Implement ALL FIVE items. Each was non-blocking at verdict time;
each is a real hardening candidate.

| # | Item | Source | Acceptance |
|---|---|---|---|
| 1 | **Escaped-form markers** — extend the marker set to cover `form_token` + `payload_ref` | #604 r1 (§4.2 payload strip) | Markers cover EVERY payload field; a test proves the strip holds AND the markers now catch what they missed. Defense-in-depth, not a strip replacement. |
| 2 | **Unknown-outcome fallback** — explicit behavior contract for the hooks object when an outcome is unknown (currently implicit) | #604 r1 | A NAMED fallback rule in the hooks contract + a test pinning it. |
| 3 | **Timeline sort format-mix inversion** — the attempt timeline sorts inconsistently across mixed datetime formats | #605 r1 | A mixed-format fixture sorts correctly; pin it so it cannot regress. |
| 4 | **Em-dash pin gap** — the global em-dash ban has no lint enforcement | #605 r1 | A lint/check that FAILS on em-dash; wired into the CI gate. |
| 5 | **AR-RC13 systemic guard** — client-side re-derivation of terminality/substitution instead of using server hooks is the bug class that blocked BOTH RC4.2-r1 and RC4.3-r1 | systemic (RC4.2 r1 + RC4.3 r1) | A durable architecture-level guard (lint rule / test rule / shared-type guard) making the server hooks the single source of truth; PROVE the guard would have caught the historical re-derivations (walk it against the fixed code or the PR diffs); document the guard in the architecture doc as the AR-RC13 lesson entry. |

**Repo map:** `server/` (payload strip §4.2, hooks, webhooks) · `client/` (reference panel,
timeline component) · `shared/` (codecs/types) · `scripts/`/`Makefile` (lint + test entry
points) · architecture canon: `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` + `epics-reference-checking-v1-2026-07-30.md` (AR-RC13 lives there).

**Verify:** full test suite green, new pins green (items 1–3, 5), lint green + CI gate wired
(item 4), PR body maps each issue item → fix → pin. Launchable increment where practical.

**Scope guard:** the five #607 items ONLY — no unrelated refactors, no design changes. Each
fix stays minimal; where an item has a plausible alternative reading, prefer the more
restrictive one and flag it in the PR body.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-followup-607
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 607
pr_review: 1
```
