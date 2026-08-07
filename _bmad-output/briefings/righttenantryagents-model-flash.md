# Briefing: righttenantryagents-model-flash

- **Repo:** RightTenantryAgents (`/Users/moses/code/RightTenantryAgents`, remote: `solarity-services/RightTenantryAgents`)
- **Worktree:** standard minion worktree off `develop` (base branch is develop; PR targets develop)
- **Workflow:** quick-dev (config change, forensics already done — execute, don't re-discover). Perkins: **ON** (code change affecting all AI agents + compliance judges — r1 fires on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

**Cost optimization:** switch ALL 12 RT agents from their current models to **Gemini 3.6 Flash** (`gemini-3.6-flash`). Driven by the GCP bill — Vertex AI / Gemini API is ~55% of spend (€744 Jan–Aug). This is the single biggest cost lever after the retry-fix (already done).

## Forensics (ALREADY DONE by the prior minion — do not re-investigate, just execute)

The model config is **centralized** and lives in TWO places:

1. **`tenant_scorer/config.py`** — model selection: env var > `DEFAULT_MODEL` > hardcoded `'gemini-3.5-flash'`. This is the code fallback.
2. **Terraform `variables.tf`** — the PROD values are env-overridden via Terraform. A code-only PR changes the fallback but NOT prod (env overrides win). **Both surfaces must change** or the PR is a prod no-op.

### Current prod model tiers (both must move to gemini-3.6-flash)

**Default tier** (currently `gemini-3.5-flash`) — 7 agents:
- document_extractor, anonymizer, pii_reviewer, income_verifier, reference_validator, rental_history_verifier, inline judges

**Pro tier** (currently `gemini-3.1-pro-preview`) — 5 agents:
- risk_scorer, verification_compliance_judge, final_compliance_reviewer, consistency_checker, personal_statement_analyzer

### Model ID (confirmed — do not guess)
**`gemini-3.6-flash`** — GA 21 Jul 2026, available on Vertex AI. Use this exact ID.

## The change

1. **config.py**: change the default/fallback model to `gemini-3.6-flash`.
2. **variables.tf**: change the Terraform-managed prod env values — BOTH the default-tier agents AND the 5 Pro-tier agents — to `gemini-3.6-flash`. All 12 agents on one model.
3. **Verify every model-selection point** is covered (grep for `gemini-3.5-flash`, `gemini-3.1-pro-preview`, `gemini-3`, any model strings). No stale references remain. List them in your self-report.
4. **Consolidate** if there are scattered hardcoded model strings — prefer the single config point.

## Why the Pro→Flash move is safe (verified, not assumed)

The user's concern was that switching the 5 Pro agents to Flash is a "downgrade." It is NOT — **verified via Artificial Analysis** (independently confirmed by Gru before dispatch):

| Metric | gemini-3.6-flash | gemini-3.1-pro-preview | Winner |
|---|---|---|---|
| Intelligence Index (v4.1: incl. GPQA Diamond, Humanity's Last Exam, AA-Omniscience) | **50** | 46 | 3.6 Flash |
| Price / 1M tokens | **$1.16** | $1.74 | 3.6 Flash (33% cheaper) |
| Output speed | **220 tok/s** | 122 tok/s | 3.6 Flash (1.8× faster) |

3.6 Flash is **more intelligent, cheaper, AND faster** than the 3.1 Pro it replaces. It is an upgrade on every axis. User rationale: all on 3.6 Flash now; revisit the high-stakes agents only when a NEW Pro beats 3.6 Flash.

## Guard: judge sanity-check (light)

Even though Flash is more intelligent per benchmarks, compliance judges are high-stakes (they gate EU AI Act Annex III rulings + the fail-fast logic). Keep this light safety net:
- **Compare Flash judge rulings vs current model** on a sample of representative compliance cases (if a test fixture / eval set exists, run both and diff verdicts).
- Report the agreement rate + any divergences in your self-report.
- If divergence is significant, HALT and surface it. Risk bar is LOW (Flash is more intelligent), but verify rather than assume.

## Hard constraint

**Do NOT touch the retry / fail-fast logic.** The compliance-gate fail-fast behavior was fixed in #156 (constrained LLM repair pass inside gate loops, non-retryable halt). Leave that intact — this change is the MODEL TIER only, a separate axis.

## Acceptance

- All 12 agents use `gemini-3.6-flash` (no stale `gemini-3.5-flash` or `gemini-3.1-pro-preview` references in config or Terraform).
- Both `config.py` AND `variables.tf` changed (prod will actually move).
- `pytest` (or the repo's test suite) passes.
- Judge sanity-check done + reported.
- Retry/fail-fast logic untouched (diff confirms no changes to the gate/repair code).
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantryagents-model-flash working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantryagents-model-flash in-review "PR <url>"` when PR opens
- `herdr notification show "rta-model-flash" --body "<one-line>"` on finish
- Final message: summary, the list of model-selection points changed (config.py + variables.tf lines), confirmation all 12 agents now on gemini-3.6-flash, judge quality comparison result, PR URL.

## Dispatch parameters

- repo: RightTenantryAgents
- repo_root: /Users/moses/code/RightTenantryAgents
- slug: righttenantryagents-model-flash
- base: develop
