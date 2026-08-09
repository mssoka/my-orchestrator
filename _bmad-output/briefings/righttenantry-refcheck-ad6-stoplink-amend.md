# Briefing: righttenantry-refcheck-ad6-stoplink-amend

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (or wherever the refcheck arch doc lives). PR targets develop.
- **Workflow:** targeted architecture-doc amendment (the objection-path consequence of the one-way Alpha Sender ID). Perkins: OFF (docs). Self-review: bmad-review-edge-case-hunter (verify EVERY reply-STOP reference is caught + amended; nothing half-done).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

Amend the refcheck architecture's **objection path**: the Registered Alphanumeric Sender ID "RTenantry" (AD-5, corrected in #592) is **one-way / non-replyable** — so the inbound STOP-by-SMS-reply path (AD-6 / Q3 / §5.5) is dead as written. A referee can't text STOP back to an alphanumeric sender. Shift SMS objection to a **stop-link web route** (the standard A2P pattern for non-replyable senders). This must land **before rc3-2 (message templates) + rc3-6 (webhooks)** so they build the right path.

## The finding (the consequence Gru missed proactively)

- Alpha Sender IDs are **outbound-only** (one-way branded SMS — per [Twilio Alphanumeric Sender IDs](https://www.twilio.com/docs/numbers-and-senders/alphanumeric-senders)).
- AD-6 / Q3 / §5.5 specified **SMS STOP via verified inbound Twilio webhook** (referee texts STOP back).
- **Incompatible** — the referee literally cannot reply to "RTenantry." The inbound STOP-reply path is dead.
- The OTHER objection channels still work: web-form decline-with-objection (the referee's form route), flagged email reply. Only the SMS-reply is broken.

## The amendment (the stop-link redesign)

### AD-6 + §5.5 + Q3 (the objection path)
**Replace** the inbound SMS STOP-reply with a **stop-link web route**:
- Every reference-check SMS includes a **stop-link**: e.g. `righttenantry.ie/reference/[token]/decline` (reuse the capability-token route family — the referee already has a token for the form).
- The referee taps the link → the route handles the objection: writes the `reference_objection_log` row (Art 21 evidence), sets outcome `objected`, nulls `next_attempt_at`, blocks all future messages on every channel — the same sticky objection semantics as the reply-STOP path, just triggered via a web tap instead of an SMS reply.
- **The inbound Twilio webhook is no longer needed for STOP.** It may still serve **delivery status callbacks** (SMS delivery failure → `awaiting_correction` per AD-7) — narrow its scope accordingly (don't remove it outright if delivery callbacks use it; just remove the STOP-reply responsibility).

### Downstream story implications (note in the amendment, don't rewrite the stories)
- **rc3-2 (message templates):** every SMS template includes the stop-link (not "reply STOP"). The Art 14 notice + the opt-out both point to the link.
- **rc3-6 (webhooks):** scope narrows — the inbound Twilio webhook handles **delivery callbacks** (SMS failure → awaiting_correction), NOT inbound STOP. The stop-link route owns objections.
- **Compliance:** the stop-link route must satisfy the same Art 21 evidence requirement as the reply path (the `reference_objection_log` row is the evidence; the trigger is a web tap, which is arguably CLEANER evidence than an SMS reply — logged, timestamped, token-bound).

### Amendment note
Add a dated amendment note (2026-08-08): the Alpha Sender ID "RTenantry" is one-way (outbound-only); the SMS objection path shifted from inbound STOP-reply to a stop-link web route. Cite the Twilio one-way nature. Note this is the consequence of the AD-5 sender correction (#592) that should have been caught proactively.

## Constraints
- Find + amend **EVERY** reply-STOP / inbound-SMS-STOP reference in the architecture (grep: "STOP", "reply", "inbound webhook", "SMS.*objection", "AD-6", "Q3", "§5.5"). Don't leave any half-amended.
- The objection SEMANTICS are unchanged (sticky `objected` outcome, Art 21 log, blocks all channels) — only the TRIGGER changes (web tap vs SMS reply).
- Don't touch the web-form-decline or email-reply objection channels (they still work).
- Don't redesign rc3-2/rc3-6 themselves — just note the implication so they build the right path.
- No em-dashes in user-facing copy (RT global ban).

## Acceptance
- AD-6 + §5.5 + Q3 + all reply-STOP references amended to the stop-link route.
- The inbound-webhook scope narrowed (delivery callbacks, not STOP).
- Downstream implications noted for rc3-2/rc3-6.
- Amendment note with provenance.
- After user approval: commit, push, open PR. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-ad6-stoplink-amend working` at start
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-ad6-stoplink-amend in-review "PR <url>"` when PR opens
- `herdr notification show "ad6-stoplink-amend" --body "<one-line>"` on finish
- Final message: the reply-STOP → stop-link amendment + where it landed, the webhook scope change, the rc3-2/rc3-6 implications, PR URL.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-ad6-stoplink-amend · base: develop
