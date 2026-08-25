# Perkins briefing — round 1: righttenantry-refcheck-rc3-7

- **PR:** https://github.com/solarity-services/RightTenantry/pull/603 (targets `develop`)
- **Reviewed sha:** `2bf2577025b41cb4121ed0da8f6294be92e556e9` (short `2bf2577`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-7-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-7.md` + story RC3.7 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (story RC3.7 full AC line 565, FR-RC12, AD-10, §6.4, §9.4) + the architecture `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (AD-10 fraud-honesty table, §4.2 internal-only IP/UA, §4.6/§6 result schema + fraud_signals column, §9.4) + GitHub issue #548 (dumped at `_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/issue-548.json`).
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (it ran a lavish clarify — decisions D1-D6; one flagged tradeoff for you: the line-type lookup runs SYNCHRONOUSLY in the trigger path, ~1s typical, no-ops on timeout; escape hatch = moving it to the sweep's T0 step if latency bites). Leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**RC3.7: Fraud-Signals Module — the closing RC3 sub-story.** An honest fraud-signals table per reference (`fraud.gleam`, AD-10): signals are clues about provenance, **never fabricated detections, never verdicts** — they never auto-reject or alter a score. v2-reserved signals emit `unknown`/`null`/`absent` rather than placeholders.
- **The signal table (exactly AD-10):** pure-DB (`contact_reused_within_application`, `contact_duplicate_of_applicant`, `contact_reused_across_applications`); Twilio Lookup (`line_type`, `voip_or_burner`); form_session (`completion_seconds`, `ip_matches_applicant`, `device_fingerprint_match` — UA compare, labelled **weak**); honest placeholders (`geo_vs_claimed_property` → `"unknown"`, `coached_answer_score` → `null`, `voice_matches_other_reference` → absent).
- **Wiring:** pure-DB at row creation; line-type before first send (RC2.3 trigger path); DB checks re-run at submission (contacts change via the correction loop); form_session at submission (referee IP/UA server-captured, compared to RC1's `application.submitted_ip_text`/`submitted_user_agent`); `referee_contact_invalid` recorded when a correction cycle fails (**supersedes `referee_number_wrong`**, §6.4).
- **Storage boundary:** signals land in `result.fraud_signals` (authoritative) + the denormalised column (AR-RC7); raw IPs/UAs internal-only (§4.2).
- **W1 carry from rc3-6:** the dead defense layer in `claim_webhook_event` should be dropped while in the reference_checks area.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 AD-10 HONESTY IS THE load-bearing invariant.** Signals are CLUES about provenance, NEVER fabricated detections, NEVER verdicts. They NEVER auto-reject and NEVER alter a score. The v2-reserved signals (`geo_vs_claimed_property` → `"unknown"`, `coached_answer_score` → `null`, `voice_matches_other_reference` → absent) MUST emit the honest placeholder, never a guess or a fabricated value. A fabricated signal, a placeholder that pretends to be real data, a signal that auto-rejects, or a signal that alters a score = a BLOCKER.
- **🚨 RAW IPs/UAs NEVER LEAVE THE SERVER (§4.2).** Only the DERIVED booleans (match/no-match) persist/transit. A raw IP/UA leaking into a response, a persisted field, or the notification payload = a BLOCKER (privacy). (The landlord panel — RC4.1 — is where the boundary is enforced for display; rc3-7 must keep the raws server-side.)
- **INNOCENT REUSE ≠ FRAUD.** A letting agent legitimately appearing across several applications is NOT fraud — the `contact_reused_across_applications` check MUST NOT false-positive on legit reuse (unit-test fixtures for this; verify they're real). A false-positive on innocent reuse = a real defect.
- **`referee_contact_invalid` SUPERSEDES `referee_number_wrong` (§6.4).** The old slug must be updated at the call site, NOT left alongside. Both present = a real defect.
- **The signal table matches AD-10 exactly.** Verify each signal is produced with the right semantics + the weak label on the UA compare (`device_fingerprint_match` is a WEAK signal — don't flag it as weak; that's the design). A signal missing or mis-scoped = a finding.
- **Form-session capture:** `completion_seconds` from `form_opened_at`→`submitted_at` + client focus time; IP/UA server-captured at submission; compared to RC1's captured values. Verify the capture is server-side (not client-trusted).
- **The flagged tradeoff (NOT a defect):** the line-type lookup runs synchronously in the trigger path (~1s typical, no-ops on timeout). The minion flagged it for review with an escape hatch (move to the sweep's T0 step). This is a flagged design tradeoff — do NOT flag it as a blocker; evaluate + note if it's a genuine risk (e.g., the timeout path leaves a stale/null signal).
- **External gate:** Twilio Lookup needs the Twilio keys (unprovisioned) — until then those signals emit `null`/`unknown` HONESTLY. Do NOT flag "line_type always null without keys" — that's the gate, and null is the honest value.
- **W1 carry from rc3-6** — verify the dead `claim_webhook_event` case is dropped (or note it if still present).
- **No em-dashes** in user-facing copy (the RT CI ban — APPLIES to RightTenantry).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; the implementing minion recovered it). Review the PR content as-is at the sha.
- **Do NOT re-open rc3-1…rc3-6 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- A **fabricated signal** (a placeholder passing as data, or a guess for geo/coached/voice) — a blocker (AD-10).
- A signal that **auto-rejects or alters a score** — a blocker (AD-10).
- **Raw IP/UA leaking** beyond the server (response/persisted/notification) — a blocker (§4.2).
- **Innocent reuse flagged as fraud** (a false-positive in the cross-application check) — a real defect.
- **`referee_number_wrong` still present** alongside `referee_contact_invalid` — a real defect (§6.4).
- A **client-trusted capture** (completion_seconds/IP/UA from the client instead of the server).
- An **em-dash in user-facing copy** (RT CI ban).
- A `make test` / `make build` / migration failure at `2bf2577`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 603 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `2bf2577`), `spec_files` = this briefing + the job briefing + RC3.7/FR-RC12/AD-10/§6.4/§9.4 + the architecture (AD-10, §4.2, §4.6/§6, §9.4) + issue #548, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 603 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 603 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `2bf2577`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc3-7 / **Reviewed sha:** 2bf2577 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-7-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. **BURST WARNING (proven 4x, mitigation now VALIDATED):** the ZAI account 429 trips at ~9+ concurrent glm panes, BUT **staggering the lens spawns (wave-1 ≤4 → wave-2 rest) keeps peak concurrency at ≤6 and avoids it entirely** (the pp-2.2 round this hour ran staggered with ZERO 429s). No other minion is working right now (the board is this round only), so even a modest stagger is safe. If a lens still 429s, one continue revives it.
