# Briefing: righttenantry-refcheck-rc3-7

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, base `develop` **after #602 merges**).
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion. Perkins: **ON** (fraud/privacy code + the honesty invariant). Self-review: bmad-review-edge-case-hunter (innocent-reuse, the no-fabricate/no-auto-reject rule, raw-IP/UA containment).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **Perkins:** ON (glm-5.2 fallback).
- **bmad-quirk heads-up:** the create-story/dev-story tooling mis-resolves edits to the main checkout. **Verify every edit lands in YOUR worktree** (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Story **RC3.7: Fraud-Signals Module** — the closing RC3 sub-story. Build `fraud.gleam` (AD-10): an honest fraud-signals table per reference. The load-bearing rule — **AD-10 honesty**: signals are clues about provenance, **never fabricated detections, never verdicts** — they never auto-reject or alter a score, and the v2-reserved signals emit `unknown`/`null`/`absent` rather than placeholders. This is the last RC3 piece; RC4 (landlord panel) will DISPLAY these, but rc3-7 just computes + persists them.

## The story (acceptance — from epic Story RC3.7 + AD-10)

1. **The signal table (exactly AD-10):**
   - **pure DB:** `contact_reused_within_application`, `contact_duplicate_of_applicant`, `contact_reused_across_applications`
   - **Twilio Lookup:** `line_type` / `voip_or_burner`
   - **form_session:** `completion_seconds`, `ip_matches_applicant`, `device_fingerprint_match` (UA compare, labelled **weak**)
   - **honest placeholders (NEVER fabricated):** `geo_vs_claimed_property` → `"unknown"`, `coached_answer_score` → `null`, `voice_matches_other_reference` → absent.
2. **Wiring:** pure-DB checks run at row creation; line-type lookup before first send (RC2.3 trigger path; pre-existing rows keep nulls honestly); DB checks **re-run at submission** (contacts change via the correction loop); `form_session` computes at submission (`form_opened_at`→`submitted_at` + client focus time, referee IP/UA server-captured, compared to `application.submitted_ip_text`/`submitted_user_agent`); `referee_contact_invalid` recorded when a correction cycle fails (wired into RC3.5/RC4.3; **supersedes `referee_number_wrong`**, §6.4).
3. **Storage boundary:** land in `result.fraud_signals` (authoritative) + the denormalised column (AR-RC7); **raw IPs/UAs never leave the server** (internal-only, §4.2); **no signal ever auto-rejects or alters a score** (AD-10, §9.4).

**Files:** `server/src/reference_checks/fraud.gleam` (new) · wiring into `trigger.gleam`, `form_handler.gleam`, `sweep.gleam`.

## Carry-forwards (read the merged work)
- **RC1** — `application.submitted_ip_text` / `submitted_user_agent` (the fraud comparator captured at submission).
- **rc3-2/3.3/3.5/3.6** — the send / form-session / sweep / webhook machinery; rc3-7 wires into the trigger + form + sweep paths.
- **rc3-5** — the wrong-contact correction cycle; rc3-7 logs `referee_contact_invalid` on its second failure.
- **W1 from rc3-6** (carried): drop the **dead defense layer in `claim_webhook_event`** (the unreachable case) while you're in the reference_checks area — small cleanup.

## Source material (read)
1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — Story RC3.7 (full AC, line 565) + FR-RC12 (line 80) + AD-10 honesty table + §6.4 (`referee_contact_invalid` supersedes `referee_number_wrong`) + §9.4.
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — AD-10 (fraud honesty table), §4.2 (internal-only IP/UA), §4.6/§6 (result schema + `fraud_signals` column), §9.4.
3. **RC1** + **rc3-2/3.5** (merged) — the capture + trigger + sweep this plugs into.

## Constraints (load-bearing — RT-specific)
- **AD-10 honesty is the core invariant:** never fabricate a signal; never auto-reject or alter a score. The v2-reserved signals (`geo`, `coached`, `voice`) MUST emit `unknown`/`null`/`absent`, never a placeholder or guess.
- **Innocent reuse must not read as fraud** — a letting agent legitimately appearing across several applications is NOT fraud (unit-test fixtures for this).
- **Raw IPs/UAs never leave the server** (§4.2) — only the derived booleans (match/no-match) persist/transit.
- **`referee_contact_invalid` supersedes `referee_number_wrong`** (§6.4) — update the call site, don't leave both.
- **External gate:** Twilio Lookup (`line_type`/`voip_or_burner`) needs the Twilio keys (still unprovisioned) — the RC2.1 Lookup client exists; until keys land, those signals emit `null`/`unknown` **honestly** (not a fabricated value).
- **No em-dashes** in user-facing copy (RT CI ban).

## Verify
- Every signal in the AD-10 table produced, with the honest placeholders exactly (`unknown`/`null`/`absent`).
- Innocent-reuse fixtures pass (letting-agent-across-applications ≠ fraud); a weak UA compare is labelled weak.
- `referee_contact_invalid` fires on correction-cycle second failure; `referee_number_wrong` superseded.
- Raw IPs/UAs internal-only (the §4.2 boundary); signals land in `result.fraud_signals` + the column.
- No signal alters a score or rejects (AD-10); `make test-server` green.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set righttenantry-refcheck-rc3-7 working` at start
- `bin/ledger set righttenantry-refcheck-rc3-7 in-review "PR <url>"` + `bin/ledger pr righttenantry-refcheck-rc3-7 <url>`
- `herdr notification show "refcheck-rc3-7" --body "<one-line>"` on finish
- Final message: the fraud-signals summary, the honesty-invariant verification, whether RC4.1 (landlord panel payload) is next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-7 · base: develop
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: 548
