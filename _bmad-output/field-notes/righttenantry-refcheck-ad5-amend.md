# Field notes — righttenantry-refcheck-ad5-amend (2026-08-08)

- **A briefing can carry a typo in a load-bearing proper noun.** Gru's briefing
  gave the Alpha Sender ID as `RTenTRY`; the canon (ComReg gate doc) is `RTenantry`.
  I committed `RTenTRY` before Gru caught it — a name/identifier supplied by the
  briefing should be grepped against the canon doc BEFORE the first commit (the
  same "briefing's stated value can be wrong" trap as the model-tier / mechanism
  gotchas, now extending to proper nouns). Fix cost a force-push amend; cheap here
  only because no PR was open yet.
- **Edge-case-hunter on a doc amendment must re-check HEADINGS/siblings of the
  named target, not just the named lines.** The briefing named AD-5 body + the
  deps row; the AD-5 *heading* still said "launch dependency" while the corrected
  body said "central dependency, not just launch polish" — a silent internal
  contradiction. The heading was part of AD-5 and the escalation was mandated,
  so fixing it was in-scope precision, not re-litigation.
- **Amending a sender type can break a sibling channel that the briefing fenced
  as out-of-scope.** Making the IE SMS sender a (non-replyable) Alpha Sender ID
  means the inbound STOP-by-SMS-reply webhook (AD-6/Q3) can't receive replies.
  Briefing said webhooks/objection-flow "unchanged" — so I did NOT redesign it,
  but surfaced it as a flagged consequence in the PR + escalation rather than
  leave the doc silently inconsistent. The right move when an in-scope change
  has a load-bearing out-of-scope consequence: flag + escalate, don't silently
  expand scope and don't silently leave the gap.
