# Lens: Architecture (source: `architecture`) — Perkins RC3.5 r1

Read and follow `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/lens-prompts/_shared_context.md` first (inputs, invariants, output contract). Then apply this lens.

## YOUR LENS — architectural fit
Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions? (Compare to the `retention_job` / `verification_reminder_job` module split: `main/0` entry + pure-ish `run/...` worker + SQL. Compare `notify_reference_unreachable` to the `notify_reference_completed/declined/objected` siblings in `notification_dispatch.gleam`.)
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Key architecture questions for this PR:
- The cadence math computes the next horizon as `next_attempt_at + increment` (relative to the current horizon) rather than the spec's literal `created_at + offset` formula. Is this a sound deviation (self-healing after downtime) or a subtle drift bug? Trace whether, under normal 15-min operation starting from `next_attempt_at = created_at = now()`, the two formulas agree at every step.
- The send-then-claim ordering (send, then guarded claim) vs claim-then-send: is the tradeoff (duplicate message worst case, never a missing message) correct for email/SMS?
- The warm-handoff dispatch happens AFTER the guarded advance and is best-effort (result discarded). If dispatch fails, the landlord never gets the unreachable notification (§8.3 says T+96 IS the only notification; T+144 is silent). Is losing that notification acceptable?
- The `step_terminal` re-decodes `draft_answers` via `questions.decode_draft` to decide partial vs unreachable — is that consistent with how the form-handler stores drafts?

## OUTPUT
Write ONLY your JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/architecture.json`
Use `"source": "architecture"`. Then stop.
