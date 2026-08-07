# Briefing: righttenantry-agent-model-flash

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (RT uses develop → main; PR targets develop)
- **Workflow:** quick-dev (config change + verification). Perkins: **ON** (code change affecting AI behavior + compliance judges — r1 fires on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

**Cost optimization:** switch ALL RT agent model usage — every analysis agent AND every judge agent — from the current model(s) to **Gemini 3.6 Flash** (the latest cost-efficient Gemini). This is driven by a large GCP bill where Vertex AI / Gemini API calls are ~55% of spend (€744 Jan–Aug). Flash is cheaper per-token; switching all agents compounds the savings.

## Where to look

The AI agent code lives in `server/src/ai/`. The model is configured somewhere in the call path — find it:
- Likely an **environment variable** (e.g. `RT_MODEL`, `GEMINI_MODEL`, `VERTEX_MODEL`) read by the Vertex AI / Gemini client, OR
- A **config constant / model string** in the AI client (`server/src/ai/ai_client.gleam` is the central client — start there), OR
- Per-agent model selection (analysis agents vs judge agents may have separate config).

`model_version` is logged/stored (seen in `ai_client.gleam`, `sql.gleam`) — trace backwards from where it's SET to find the source of the model string. Grep for the current model name strings (e.g. "gemini-2", "gemini-pro", "gemini-1.5", "flash", "pro") to locate every place a model is specified.

## The change

1. **Identify every model-selection point** for analysis agents AND judge agents. List them (file + line) in your self-report.
2. **Switch all to Gemini 3.6 Flash.** Use the exact, current Vertex AI / Gemini API model ID for "Gemini 3.6 Flash" — verify the correct string against the Vertex AI model registry / docs (don't guess the ID; a wrong string breaks every agent call). If the exact ID is ambiguous, surface it as a numbered question before changing.
3. **Consolidate** if the model is hardcoded in multiple places — prefer a single config point (env var or constant) that all agents read, so future model changes are one-line. If it's already centralized, just change the one value.
4. **Do NOT touch the retry/fail-fast logic.** The compliance-judge fail-fast behavior was recently fixed (fail-fast on compliance issues, no indefinite retries). Leave that intact — only change the MODEL, not the control flow.

## Critical: judge quality sanity-check

Judges gate compliance decisions (the fail-fast logic depends on judge rulings). A cheaper model *could* rule differently. Before the PR is merge-ready:

- **Compare Flash judge rulings vs the current model** on a sample of representative cases (if there's a test fixture / eval set of past rulings, run both models and diff the verdicts). 
- Flag in your self-report: do Flash judges agree with the prior model on compliance pass/fail? Any edge cases where they diverge?
- If divergence is significant, HALT and surface it — the user decides whether the cost saving is worth the ruling drift. Don't silently ship a judge that changes compliance behavior.

## Acceptance

- Every analysis agent + judge agent uses Gemini 3.6 Flash (verified — no stale model strings remain).
- `gleam test` / `make test-server` passes.
- The model is configured in ONE place (consolidated) if it wasn't already.
- Judge quality sanity-check done + reported (agreement rate, any divergences).
- Retry/fail-fast logic untouched.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Context (do not re-investigate — confirmed by Gru)

- GCP bill: Vertex AI €552.71 + Gemini API €191.44 = ~55% of €1,358 total (Jan–Aug). Switching to Flash targets the biggest spend bucket.
- The retry fail-fast fix is ALREADY DONE — this change is the model tier, a separate axis of optimization.
- Currency EUR; the savings motive is direct cost reduction.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-agent-model-flash working` at start (`clarifying` if you halt on the model ID or judge divergence)
- `/Users/moses/code/bin/ledger set righttenantry-agent-model-flash in-review "PR <url>"` when PR opens
- `herdr notification show "agent-model-flash" --body "<one-line>"` on finish
- Final message: summary, the list of model-selection points changed, the exact Gemini 3.6 Flash model ID used, judge quality comparison result (agreement %, divergences), PR URL.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-agent-model-flash
- base: develop
