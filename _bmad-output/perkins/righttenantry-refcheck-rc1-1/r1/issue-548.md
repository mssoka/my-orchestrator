title:	AI reference-check calls: landlord-facing feature (consent, status, transcript display)
state:	OPEN
author:	mssoka (MSS)
labels:	enhancement
comments:	3
assignees:	
projects:	
milestone:	
number:	548
--
**Type:** Feature — implementation anchor (landlord-facing side)
**Status:** Research complete → **RESUME** recommended. **No implementation yet** — architecture & UX to be designed first via the bmad method (see below).

## Context

Automatically call an applicant's references (previous landlord, employer)
with an AI voice agent instead of manual phone/email chasing. Viability
research is **done and merged** (PR #540, research issue #535):

- **Interactive HTML doc (start here):**
  `_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.html`
- Synthesis markdown:
  `_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md`
- Deep-dive threads (legal / providers / architecture / fraud / fallback):
  `_bmad-output/planning-artifacts/research/heist-535/`

Headlines: legal blocker refuted on primary sources (with flags below);
provider class identified (Retell/Vapi/Bland vs Twilio + OpenAI Realtime —
see providers thread); prior prototype exists, so resumption cost is low.

## Scope in THIS repo (per the research's architecture thread)

- Application flow: reference details capture + **consent/acknowledgement**
  wording (per Perkins r1 on #540: "acknowledgement" framing)
- Reference-call status tracking per application
  (pending → calling → completed / declined / no-answer → manual fallback)
- Landlord-facing display: transcript + structured reference summary +
  fraud signals
- Fallback path UI: reference declines/no-answer → current manual flow
- **Consumer** of the transcript → score handoff schema (contract shared
  with the RightTenantryAgents issue)

## Legal-review flags (from research — must be designed in, not bolted on)

- AI-disclosure announcement at call start (EU AI Act Art. 50, in force
  2 Aug 2026) + recording announcement
- Art. 22: decision-support only — no solely-automated decisions
- DPIA required; GDPR retention vs DPC delete-after-tenancy expectation
- ComReg CLI/Sender-ID considerations (see legal thread)

## Next step (bmad method — deliberate, not ad-hoc)

Before any code: **bmad-architecture + bmad-ux** working sessions with
Moses to produce the proper architecture and UX spec (handoff schema,
status model, consent copy, landlord display), then
bmad-create-epics-and-stories for the build plan. Companion issue:
RightTenantryAgents (voice orchestration side — link below).

