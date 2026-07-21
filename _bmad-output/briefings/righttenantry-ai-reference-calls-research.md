# Briefing: righttenantry-ai-reference-calls-research ("heist")

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd, branch `ai-reference-calls-research`
- **Base:** `develop` — PR targets **`develop`**
- **GitHub issue:** #535 (research informs it — reference with `Refs #535`, do NOT close)
- **Type:** viability research, not code. Deliverable is a research document + recommendation, committed on the branch and opened as a PR.

## Mission

Run the **bmad-domain-research** skill as your operating workflow to assess the
viability of GitHub issue #535: *"Explore automated AI reference-check calls for
applicants"* — automatically calling an applicant's references (previous
landlord, employer) with an AI voice agent instead of manual phone/email
chasing.

**⛔ The skill requires web search.** If web search is unavailable in your
environment, halt as `blocked` and say so (ledger + notification).

Follow the skill's activation exactly (resolve customization via
`_bmad/scripts/resolve_customization.py`, load `_bmad/bmm/config.yaml`, honor
`planning_artifacts` for output location, create the output file from the
skill's `research.template.md` per its naming convention).

**Topic discovery is pre-answered** (the skill's interactive clarify is
overridden by this briefing; see standing orders below):

- **Topic:** AI-voice-agent automated reference checking for rental tenant
  screening — regulatory, provider, and architectural viability for an
  Irish landlord-facing product (RightTenantry), with UK as a later expansion.
- **Goals:** give Moses enough verified, cited evidence to make the issue's
  "resume or shelve" decision; if resume, name the provider class, outline the
  consent flow, and sketch the transcript → structured-reference handoff schema.
- **Scope:** deep on the five open questions below; broad market sizing is
  out of scope.

## The issue's open questions (the research threads)

1. **Consent / legality (Ireland first, UK note):** automated calling +
   recording — GDPR lawful basis, disclosure at call start, ePrivacy rules on
   automated calls, ComReg considerations. Cite primary sources
   (GDPR/ePrivacy text, DPC/ComReg guidance) where possible.
2. **Provider choice:** dedicated voice-AI platforms (Retell / Vapi / Bland
   class) vs. Twilio + OpenAI Realtime API. Cost per *completed* reference
   call, Irish/EU number support, latency, recording/consent features, EU data
   residency / DPA availability. Note: Moses prototyped with a provider
   transcribed from a voice note as "Trilu" — determine the most likely
   actual provider (Retell? Twilio?) from current market evidence and say so.
3. **Architecture:** voice-call orchestration + transcript → structured
   reference summary feeding the scoring pipeline lands in `RightTenantryAgents`
   (ADK); reference status + transcript/summary display for landlords lands in
   this repo. Propose the transcript → score handoff schema.
4. **Fraud safeguards:** detecting coached/fake references; cross-checking
   phone-number ownership against claimed reference identity.
5. **Fallback path:** reference doesn't answer or declines to talk to an AI →
   fall back to the current manual flow.

Prior context: a working prototype existed (voice-AI provider + OpenAI) and was
paused for prioritisation, so resumption cost is low — factor that in.

## "Heist" structure (mega-minions encouraged)

You are the crew lead. You may spawn mega-minions
(`herdr pane split --current --direction right|down --no-focus`, then
`herdr pane run <pane> "pi"`, wait for idle, hand over the thread brief) for
parallel research threads — e.g. one per open question above, legal and
provider being the heaviest. **Max 10 concurrent mega-minion panes**, batch if
needed, and **close every pane you create before finishing**. Synthesize their
findings into the single research document yourself.

## Standing orders (orchestration overrides)

- Read `/Users/moses/code/docs/orchestration-playbook.md` section "Minion
  standing orders" — it applies in full, with these notes:
  - The bmad-quick-dev step-01 clarify override applies analogously: if you
    have genuine blocking questions, ask them numbered and HALT; Gru relays
    answers. Internal skill checkpoints (scope confirmations, outline
    approvals) are **pre-approved** — proceed without halting.
  - Work entirely inside this pane's cwd on branch `ai-reference-calls-research`.
- Env files: `.env` is symlinked from the main checkout — **read-only**
  (replace symlink with a copy first if you truly must edit, and call it out).
  `.env.example` / `.env.test` are normal tracked files. Never commit secrets.
- Self-report every status transition:
  `/Users/moses/code/bin/ledger set righttenantry-ai-reference-calls-research <status> "<one-line note>"`
  (`working` when you start, `blocked`/`clarifying` if halted, `in-review` when
  the PR opens).
- When blocked or finished:
  `herdr notification show "righttenantry-ai-reference-calls-research" --body "<one-line status>"`

## Deliverable & close-out

1. The research document at the skill's conventional path
   (`{planning_artifacts}/research/domain-<slug>-research-2026-07-21.md`),
   with citations, covering all five threads, ending in a clear
   **Recommendation: resume or shelve** section (provider pick, consent-flow
   outline, handoff-schema sketch if resume).
2. Commit on `ai-reference-calls-research`, `git push -u origin
   ai-reference-calls-research`, open a PR to `develop`
   (`gh pr create --base develop`) whose body carries a **"Decisions &
   rationale"** section and `Refs #535`. **Never merge.**
3. Final message: summary, files changed, PR URL.
