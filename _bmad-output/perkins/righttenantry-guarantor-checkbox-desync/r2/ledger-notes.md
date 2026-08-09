id             righttenantry-guarantor-checkbox-desync
repo           RightTenantry
repo_root      /Users/moses/code/RightTenantry
slug           guarantor-checkbox-desync
base           develop
model          
worktree       /Users/moses/.herdr/worktrees/RightTenantry/guarantor-checkbox-desync
pane_id        w1T:p7Z
tab_id         w1T:t1P
status         in-review
started_at     2026-08-04T01:23:58Z
briefing       /Users/moses/code/_bmad-output/briefings/righttenantry-guarantor-checkbox-desync.md
pr             https://github.com/solarity-services/RightTenantry/pull/577
result         
github_issue   
parent         
note           dispatched 2026-08-04: user-reported guarantor checkbox self-marking (stale persisted flag; green-lies family) + class audit of all conditional toggles + new bug-hunt scenario; Perkins armed
pr_review      1

events:
  2026-08-04T01:23:58Z  — -> dispatched  added
  2026-08-04T01:24:53Z  dispatched -> working  reading briefing + field notes, starting investigation
  2026-08-04T01:50:04Z  working -> working  REDIRECTED 2026-08-04 (user ruling Option A): desync hypothesis DEAD — application_handler.gleam:552-559 force_required:never_rented is a DELIBERATE vetting bundle (first-timer: landlord-ref replaced by character-ref + guarantor). New shape: never_rented -> guarantor DECLARED required up front (honest copy, auto-expand, step-level gating); renter path stays optional w/ checked-state fidelity preserved; self-marking killed via explanation; scenario reshaped; desync class-audit -> REPORT ONLY (fix only on evidence). Same branch/PR continues. Relay verified (minion working).
  2026-08-04T01:54:56Z  working -> working  REDIRECT: force_required is deliberate (Option A ruling) — keep rule, fix UX incoherence: required path declared in copy + step-level block; class-audit report-only
  2026-08-04T02:03:44Z  working -> working  FINAL POLICY + ADDITION relayed (user, 2026-08-04): force_required = never_rented OR {student, unemployed}; retired optional-hint, NEVER pre-ticked. Both silent mechanisms killed (autoTickGuarantor JS + has_guarantor_default_check view) — checkbox means the applicant's last action. Declared-required copy per cohort; step-level gating. POINT-OF-SELECTION signaling added: inline notes at the never-rented tick + student/unemployed choice (honest-conditionals, appear/disappear), checklists gain the guarantor line on all surfaces (W1a doctrine). Counsel-pack flag in PR: student requirement tracks age in practice — ruled market-standard; equality-law note for counsel. Test matrix {never-rented}x{5 statuses}x{present/absent} + scenario mirrors. Supersedes the 'retires the rule' reading (human renegotiation doctrine cited).
  2026-08-04T02:05:58Z  working -> working  COPY AMENDMENT relayed (user): drop 'usually a parent' everywhere (expat incoherence — assumes local family); definition-based shape (18+ steady verifiable income; parent/relative/friend/employer); Ireland-vs-foreign guarantor acceptance PARKED as landlord-policy in the PR body; grep-clean required.
  2026-08-04T22:26:46Z  working -> working  RELAUNCHED on deepseek-v4-flash 08-04T22:25Z (model switch): old kimi session killed via send-keys C-c (its 403-dead turn never processed 'exit'), new session verified (file 22-25-44, pane working). Spec-correction order delivered FIRST (user-emphasized): product-decision block renegotiated 2026-08-04 — force_required = never_rented OR {student,unemployed} SERVER-ENFORCED; retired optional-hint never pre-ticked; both silent ticks killed everywhere; step-level blocking; submit error states requirement. Uncommitted B-direction diff superseded — build from corrected spec.
  2026-08-04T22:49:10Z  working -> in-review  PR #577: fix: guarantor required-cohort UX coherence — declared-required, no self-marking (deepseek-v4-flash, 2026-08-04 policy)
  2026-08-04T22:49:10Z  in-review -> in-review  pr: https://github.com/solarity-services/RightTenantry/pull/577
  2026-08-04T22:49:10Z  in-review -> in-review  22:48Z clean finish on deepseek-v4-flash: PR #577. Full test matrix evidenced (required cohorts, retired optional, kept-on-error, check->uncheck desync fixed, no-JS box never pre-ticked). 380 int + 112 js green. Spec corrected (renegotiated 2026-08-04, force_required SERVER-enforced). Class-audit: draft layer CLEAN — real desync was validation-vs-persistence null-out. Counsel flag: student tracks age (equality-law note), retired excluded. Parked: Ireland-vs-foreign acceptance (landlord policy). Perkins r1 will fire on deepseek.
  2026-08-04T23:17:15Z  in-review -> in-review  Perkins r1 APPROVED 0B/1W — escalated to Gru (merge when ready). W1: student fixture missed the retired migration (sibling fixtures were migrated); false-confidence test (dead copy-string assertion). One-line fix candidate pre- or post-merge.
  2026-08-04T23:24:04Z  in-review -> in-review  W1 fix relayed to w1T:p7Z (working): migrate the missed student fixture -> retired (sibling-fixture pattern); verify the test passes for the RIGHT reason (co-applicant-name-only error, no guarantor errors on retired primary). Push re-fires Perkins on the new sha. Escalate if retired reveals a real bug.
  2026-08-04T23:29:23Z  in-review -> in-review  23:28Z W1 fix pushed (279a661): student->retired fixture migration + dead-string removed from form_copy.gleam (No Tech Debt); 2 live negative pins (no requirement row, no guarantor field errors); MUTATION CHECK proves the pins bite (student->fails, retired->passes). No real bug under retired (verified: retired primary = exactly one co-applicant-name error as intended). 380/380 integration green. Perkins r2 fires on 279a661. Merge-ready again post-r2.
