# Perkins briefing — round 1: righttenantry-refcheck-rc4-1

- **PR:** https://github.com/solarity-services/RightTenantry/pull/604 (targets `develop`)
- **Reviewed sha:** `a7e8cee5af30bc3d8746d1613e7a70b89cec6272` (short `a7e8cee5`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-1-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-1.md` + Story RC4.1 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (full AC ~line 607) + the architecture `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (§8.1 `reference_calls[]` + calibration copy, §8.2 hooks, §9.5 `display_disclaimer`, §4.2 stripping, A4/A5, AR21 codec convention). GitHub issue: 548.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (reference_calls[] with one stable server-computed contract; §4.2 strip at the SQL read boundary via jsonb `#-` + `jsonb_typeof` guards; hooks + display_disclaimer per §8.2/§9.5; 106 shared + 471 client + 1476 server unit + 498 integration green; make format/test/build clean; edge-case-hunter self-review caught 4 real issues pre-PR — vacuous strip guard, hooks-vs-wire status divergence, non-forward-tolerant decoder, corrupt-result read failure — all fixed) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Epic RC4 Story 1 — Detail Payload Extension (Backend Contract):** `GET /api/v1/vacancies/:vid/applications/:aid` gains `reference_calls[]` — one stable server-computed entry per call: `reference_call_id`, `ref_slot`, `owner_label`, `status`, `outcome`, `attempt_count`, `next_attempt_at`, the attempt log, the stored `result` (**stripped**), `display_disclaimer`, hooks — plus application-level `attestation_on_file` + `reference_contact_choice` (A4). The bridge from the collection engine (RC1–3, merged) to the RC4 panel UI (RC4.2–4.4 later).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 §4.2 STRIPPING — THE load-bearing invariant.** Raw IPs/UAs inside `fraud_signals.form_session`, `form_token`, and `objection_detail.payload_ref` MUST NOT reach the serialized payload. The strip happens at the SQL read boundary (`jsonb #-`). **The assertions must check the ESCAPED wire form too** — a result document riding as a JSON string field ships its inner keys backslash-escaped (`\"referee_ip\"`), so a `string.contains(body, "\"referee_ip\"")` assertion is vacuously green while the IP is on the wire. A strip that only works unescaped, or a missing shape guard (`jsonb #-` THROWS on scalar/array intermediates — one corrupt row would 500 the whole read), or any field from the internal list present in the payload = a REAL blocker. The PR carries a neutralize-the-strip negative control — verify it's real (the test goes red when the strip is disabled).
- **ONE STABLE CONTRACT [AR-RC13].** The panel renders ONLY from this payload — no client-side state-rule re-derivation. Hooks + disclaimers are server-computed. A client that re-derives hook/status rules, or a payload missing a §8.1 field the panel needs = a blocker. (RC4.2's UI doesn't exist yet — the CLIENT is out of scope; only the contract + server logic are in this PR.)
- **AR21 CODECS — shared types, snake_case end-to-end, ROUND-TRIP tests.** DB → JSON → Gleam unbroken. A codec that breaks snake_case, or shared types without round-trip tests = a real defect.
- **gleam_json 3.1.0 REALITY (no decode.any / json.from_dynamic).** This Gleam version has NO `decode.any` / `json.from_dynamic` — JSONB payload fields that can't be rebuilt as objects in shared codecs are carried as TEXT and stripped at the SQL read boundary (the `ai_analysis.category_scores` precedent). Do NOT flag "result carried as text instead of decoded" — that's the honest pattern in this stack. DO flag a decoder that tries a nonexistent API, or a field that round-trips wrong.
- **HOOK EDGE STATES.** `can_record_manual` (any non-terminal), `can_substitute_referee` (terminal objected/unreachable), `can_retry` (failed) correct across every lifecycle state — incl. skipped non-terminal, objected/unreachable → substitute, failed → retry, unknown enum values (hooks-vs-wire status divergence was a real pre-PR catch — verify the wire status and the hook computation can't diverge).
- **display_disclaimer per §9.5 — VERBATIM CANON.** Written-channel results carry the §8.1 calibration copy verbatim (verification block present); minimal terminals carry none. **RT CI ban: NO em-dashes in user-facing copy** — flag any em-dash in shipped copy (the §8.1/§9.5 strings are canon; deviation = defect).
- **`decode.optional_field` GOTCHA (known failure mode).** `decode.optional_field` expects `Decoder(t)` where `t` = the DEFAULT's type — Option fields need `decode.optional(inner)` as the FIELD decoder. A wrong wiring here silently mis-decodes Option fields — worth a look.
- **CORRUPT-ROW RESILIENCE.** The `jsonb_typeof` guards protect the read from one corrupt row 500-ing the whole endpoint (a real pre-PR catch). A read path missing the guard = a real defect.
- **base = `develop`** (RC1–3 merged — do NOT re-open their findings; carry-forward only). rc3-7's `fraud_signals` shape is the strip source — it's merged + verified; the strip completing §4.2 is THIS PR's job.
- **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR content as-is at the sha.
- **Em-dashes in code/commits are fine; in USER-FACING COPY they are banned (RT CI).**

### Legitimate findings here would be
- **Any §4.2-listed field present in the serialized payload** (form_token, objection_detail.payload_ref, raw IPs/UAs) — a blocker. Including the escaped-wire-form leak.
- **The strip's shape guards missing** (jsonb `#-` throwing on a corrupt row → 500) — a blocker.
- **A client-side re-derivation** (the contract isn't one-stable) — a blocker [AR-RC13].
- **A hook edge state wrong** (esp. unknown enum values, skipped non-terminal) — a real defect [§8.2].
- **A codec breaking snake_case or without round-trip tests** — a real defect [AR21].
- **display_disclaimer missing/wrong on a written-channel result, or present on a minimal terminal, or deviating from the §8.1 canon copy (incl. em-dashes)** — a real defect [§9.5].
- **A `decode.optional_field` mis-wiring** or a nonexistent-API decoder — a real defect.
- **A `make format` / `make build` / `make test-server` / `make test-shared` failure at `a7e8cee5`.**

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 604 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `a7e8cee5`), `spec_files` = this briefing + the job briefing + Story RC4.1 + the architecture (§8.1/§8.2/§9.5/§4.2/A4/A5/AR21), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 604 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 604 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `a7e8cee5`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc4-1 / **Reviewed sha:** a7e8cee5 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc4-1-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek (kimi's 403 is a false dawn — no k3 flips until the user explicitly says so; never glm-5.2). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
