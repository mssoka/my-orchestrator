# Briefing: righttenantryagents-compliance-guard-hardening

- **Repo:** /Users/moses/code/RightTenantryAgents
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantryAgents/compliance-guard-hardening
- **Branch:** `compliance-guard-hardening` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion standing orders"** and follow it exactly. Step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. Self-report every status transition: `/Users/moses/code/bin/ledger set righttenantryagents-compliance-guard-hardening <status> "<note>"`. When blocked or finished: `herdr notification show "righttenantryagents-compliance-guard-hardening" --body "<one-line status>"`. Never merge the PR.

## Skills policy

- **Your workflow:** `bmad-quick-dev`.
- **Mega-minions:** review swarm uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter` (name it explicitly when you spawn them).

## Context

Deferred hardening items from the PR #161 compliance-pipeline review loops. The user has **dismissed items 3 (figure-attribution guard) and 4 (judges' schema escape)** — accepted as-is. This job implements **items 7, 8, and 9**. Items 5/6 belong to a sibling job — do not touch them.

**Item details (read first):** `/Users/moses/code/RightTenantryAgents/_bmad-output/implementation-artifacts/deferred-work.md`, sections "Repair request loses duplicate-ground violations", "Compliance guard residual edges", "Compliance repair pass — loop-5 residual edges" (deferred 2026-07-19). This file is gitignored — read it at that absolute main-checkout path; your worktree will not have it. PR #161 has the review-loop history.

## Task (items 7–9, each with unit tests)

7. **Duplicate-ground violations lose a ground** — when a second violation on an already-scrubbed span gets "span not found", merge its ground into the matching coalesced slot's grounds list in the repair request instead of dropping it, so the repair agent picks the rewrite playbook with full information.
8. **Guard residual edges:**
   a. **Separator-less reintroduction** — extend the `span_absent` normalization so comparison also happens with spaces removed (catch "civilpartner" / "HAPsupported"); keep the existing verbatim + punctuation-normalized checks.
   b. **Currency symbol↔code false-trips** — treat same-currency alias rewrites as equivalent ("€51,000"→"EUR 51,000") and affix reorders ("€-51,000"→"-€51,000") as benign. Use an explicit alias map (€↔EUR, $↔USD, £↔GBP). **€→$ must still fail** — different currency is a fact change. Test both directions.
9. **Loop-5 residuals:**
   a. **Scrub eats paragraph breaks** — when a scrubbed span is adjacent to or straddles a `\n\n` junction, preserve/reinsert the break so the paragraph-parity guard doesn't cement a flattened count (and a repair that restores the break isn't rejected).
   b. **Flood truncation** — the ≥20-slot worst case truncates repair output → fail-closed halt. Fix proportionately: configure `max_output_tokens` for the repair agent (see `tenant_scorer/config.py`) sized for the worst case, and/or chunk the repair request. No unbounded machinery.
   c. **Dangling affixes** — after a scrub, clean orphaned currency/unit affixes adjacent to the removed span ("She receives € monthly." must not ship a lone "€"). Cosmetic-only; keep it deterministic and narrow.
   d. **Caps-table namespacing** — re-key `_SLOT_MAX_LENGTHS` by qualified path (parent + leaf), not bare leaf name, so future `details`/`label` fields can't inherit unrelated caps. **Fluency floor:** only assess — if a cheap deterministic check suffices, add it; if it needs an LLM judge (new machinery), HALT with a numbered clarify question instead of building it.

**Constraints:** the fail-closed posture is sacred — real violations still halt non-retryable; the re-judge stays the backstop. Proportionate fixes only, no new subsystems. Code anchors: `tenant_scorer/callbacks/compliance_scrub.py`, `tenant_scorer/agents/compliance_repair.py`, `tenant_scorer/agents/inline_judge.py`, `tenant_scorer/callbacks/compliance_enforcement.py`, `tenant_scorer/config.py`.

## Local step (main checkout, gitignored — no commit)

Update `/Users/moses/code/RightTenantryAgents/_bmad-output/implementation-artifacts/deferred-work.md`: mark item 3 **Dismissed** (user decision 2026-07-21 — attribution risk accepted, prompt-mitigated) and item 4 **Dismissed** (retryable classification accepted as intended behavior); mark items 7/8/9 **In progress — this job**; leave 5/6 marked for job `righttenantryagents-compliance-analytics-model-pin`.

## Env / bootstrap

- No `.env` files in the main checkout — nothing symlinked.
- `_bmad` project config was copied into the worktree.

## Verify

`make test` and `make lint` from the worktree. Final message: per-item approach summary, test counts, anything re-deferred (with why), PR URL. PR description must carry **"Decisions & rationale"** — especially the currency alias-map boundary and the 9b sizing choice.

## Model policy

Unset — pi default model resolution. Applies to any mega-minions you spawn (close them when done).
