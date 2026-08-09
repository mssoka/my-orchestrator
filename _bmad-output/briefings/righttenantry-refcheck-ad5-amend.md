# Briefing: righttenantry-refcheck-ad5-amend

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (or wherever the architecture-refcheck doc lives — check; RT's integration is develop). PR targets the doc's branch.
- **Workflow:** targeted architecture-doc correction. Perkins: OFF (docs). Self-review: bmad-review-edge-case-hunter (verify the amendment is precise — only the sender-type correction, nothing else re-litigated).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

Correct AD-5 (and any related references) in the refcheck architecture doc: the "IE number" assumption is WRONG — Twilio doesn't support domestic IE numbers for SMS (they're voice-only landlines). The correct Ireland SMS sender is a **Registered Alphanumeric Sender ID**, not a phone number. This correction is needed BEFORE rc3-1 builds the sms_client, so it codes the right sender config.

## The finding (verified via Twilio's Ireland SMS Guidelines)

[Twilio Ireland SMS Guidelines](https://www.twilio.com/en-us/guidelines/ie/sms) confirm:
- **Domestic IE long code (IE number): NOT supported** for SMS — Irish Twilio numbers are voice-only landlines.
- **International long code (US number → IE):** unreliable (Meteor + Three block; best-effort).
- **Alphanumeric Sender ID:** ✅ supported, but **REQUIRES Global Pre-registration** (~2-week Twilio provisioning) + ComReg registration. Since July 3, 2025, unregistered Alpha Sender IDs arrive labelled "Likely Scam."
- **Short codes:** not supported in Ireland.

**Conclusion:** RT sends FROM a **Registered Alphanumeric Sender ID ("RTenTRY")** TO Irish mobiles. No from-number needed (the Alpha Sender ID IS the sender).

## The amendment

**File:** `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (AD-5 + any "IE number" / "from-number" / sender references for the SMS path).

**Change AD-5** from:
> "Twilio account + IE number + ComReg Sender-ID registration"

**to:**
> "Twilio account + **Registered Alphanumeric Sender ID ('RTenTRY')** + ComReg SMS Sender-ID registration. No IE number — Twilio's Irish numbers are voice-only (domestic long codes unsupported for SMS); Ireland SMS requires a Registered Alpha Sender ID as the sender (~2-week Twilio Global Pre-registration + ComReg registry, per [Twilio IE SMS Guidelines](https://www.twilio.com/en-us/guidelines/ie/sms)). Since 2025-07-03, unregistered Alpha Sender IDs arrive 'Likely Scam' overstamped."

**Also update:**
- The `notification/sms_client.gleam` row (§ dependencies table, ~line 834): "Twilio account + IE number + ComReg Sender-ID registration" → "Twilio account + Registered Alpha Sender ID + ComReg registration (no from-number; sender is the Alpha Sender ID)."
- The **env config** rc3-1 will read: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_ALPHA_SENDER` ("RTenTRY") — **NO `TWILIO_FROM` number** (the sender is the Alpha Sender ID, configured via a Twilio Messaging Service, not a number).
- Any other "IE number" / "from-number" / "sender number" references in the SMS path → "Registered Alphanumeric Sender ID."
- The Lookup API (line-type fraud signals, AD-10) uses the SAME Twilio creds (Account SID + Auth Token) — unchanged (no number needed for Lookup).

**Add an amendment note** (2026-08-08): AD-5 corrected — Twilio IE numbers are voice-only; the Ireland SMS sender is a Registered Alphanumeric Sender ID per Twilio's guidelines. Cite the guidelines URL.

## Constraints
- ONLY the sender-type correction (IE number → Alpha Sender ID) + the env-config adjustment + the amendment note. Do NOT re-litigate anything else (the cadence, the webhooks, the Lookup, the objection flow — all unchanged).
- No em-dashes in any user-facing copy (RT global ban — though this is an internal arch doc, keep it clean).
- The ComReg registration was already a tracked launch gate — it's now CENTRAL (required for ANY IE SMS, not just launch polish). Note that escalation in the amendment.

## Acceptance
- AD-5 + all SMS-sender references corrected (IE number → Registered Alpha Sender ID).
- Env config reflects `TWILIO_ALPHA_SENDER` (no from-number).
- Amendment note with provenance + the guidelines citation.
- Nothing else changed (scope-verified).
- After user approval (or direct — it's a factual correction the user explicitly requested): commit, push, open PR. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-ad5-amend working` at start
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-ad5-amend in-review "PR <url>"` when PR opens
- `herdr notification show "ad5-amend" --body "<one-line>"` on finish
- Final message: the AD-5 correction + the env-config change, confirmation scope was tight, PR URL.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-ad5-amend · base: develop
