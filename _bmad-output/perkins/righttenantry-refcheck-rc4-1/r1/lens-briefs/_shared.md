# SHARED CONTEXT — Perkins r1 lenses (righttenantry-refcheck-rc4-1)

You are one lens in a parallel code-review wave. Read-only access to the repository. Verify every claim against the actual codebase — no claim is taken at face value.

## Round & scope

- Round 1 of 3. PR #604 → `develop`. Reviewed sha `a7e8cee5af30bc3d8746d1613e7a70b89cec6272` (short `a7e8cee5`).
- **Scope:** Epic RC4 Story 1 — Detail Payload Extension (Backend Contract). `GET /api/v1/vacancies/:vid/applications/:aid` gains `reference_calls[]` (one stable server-computed entry per reference call: `reference_call_id`, `ref_slot`, `owner_label`, `status`, `outcome`, `attempt_count`, `next_attempt_at`, the attempt log, the stored `result` — **§4.2-stripped** — `display_disclaimer`, `hooks`) plus application-level `attestation_on_file` + `reference_contact_choice` (A4). The bridge from the collection engine (RC1–3 merged) to the RC4 panel UI (RC4.2+ later). The CLIENT UI is out of scope — only the contract + server logic.
- 16 files, ~+1469/−24. Full PR diff at `diff_file`. Review EXACTLY those bytes; the worktree is at the same sha for verification.
- base = `develop` (RC1–3 merged — do NOT re-open their findings; carry-forward only). rc3-7's `fraud_signals` shape is the strip source — merged + verified; completing §4.2's boundary strip is THIS PR's job.

## Inputs (absolute paths)

- `diff_file`: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1/diff.patch`
- `worktree`: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-1-r1` (detached at `a7e8cee5`; verify reads happen HERE)
- Round briefing (lens-guards + standing orders): `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc4-1-r1.md`
- Job briefing: `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-1.md`
- Story RC4.1 AC (epics file, Story RC4.1 at line ~607): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-1-r1/_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`
- Architecture (authoritative — §8.1 payload ~line 974, §8.2 hooks ~996, §9.5 disclaimer ~1075, §4.2 stripping ~741, AD-11 ~455, AD-2 ~184, A4/A5 in the epic amendments register ~line 44): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-1-r1/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`

## ⚠️ Lens-guards — the load-bearing checks of THIS round (verify, don't assume)

1. **🚨 §4.2 STRIPPING — THE load-bearing invariant.** Raw IPs/UAs inside `fraud_signals.form_session`, `form_token`, and `objection_detail.payload_ref` MUST NOT reach the serialized payload. The strip happens at the SQL read boundary (`jsonb #-` path-delete in `list_reference_calls_for_detail.sql`). **Check the ESCAPED wire form too** — a result document riding as a JSON string field ships its inner keys backslash-escaped (`\"referee_ip\"`), so a `string.contains(body, "\"referee_ip\"")` assertion is vacuously green while the IP is on the wire. Also check: the shape guards (`jsonb #-` THROWS on scalar/array intermediates — one corrupt row would 500 the whole read; the `jsonb_typeof` guards are the fix), and ANY field from the internal list present in the payload = a REAL blocker. The PR carries a neutralize-the-strip negative control — verify it's real (the test goes red when the strip is disabled).
2. **ONE STABLE CONTRACT [AR-RC13].** The panel renders ONLY from this payload — no client-side state-rule re-derivation. Hooks + disclaimers are server-computed. A client that re-derives hook/status rules, or a payload missing a §8.1 field the panel needs = a blocker. (RC4.2's UI doesn't exist — only the contract + server logic are in this PR.)
3. **AR21 CODECS — shared types, snake_case end-to-end, ROUND-TRIP tests.** DB → JSON → Gleam unbroken. A codec that breaks snake_case, or shared types without round-trip tests = a real defect.
4. **gleam_json 3.1.0 REALITY (no decode.any / json.from_dynamic).** This Gleam version has NO `decode.any` / `json.from_dynamic` — JSONB payload fields that can't be rebuilt as objects in shared codecs are carried as TEXT and stripped at the SQL read boundary (the `ai_analysis.category_scores` precedent). Do NOT flag "result carried as text instead of decoded" — that's the honest pattern in this stack. DO flag a decoder that tries a nonexistent API, or a field that round-trips wrong.
5. **HOOK EDGE STATES (§8.2).** `can_record_manual` (any non-terminal), `can_substitute_referee` (terminal objected/unreachable), `can_retry` (failed) correct across every lifecycle state — incl. skipped non-terminal, objected/unreachable → substitute, failed → retry, unknown enum values (hooks-vs-wire status divergence was a real pre-PR catch — verify the wire status and the hook computation can't diverge).
6. **display_disclaimer per §9.5 — VERBATIM CANON.** Written-channel results carry the §8.1 calibration copy verbatim (verification block present); minimal terminals carry none. The §8.1 canon string is: `Written response, provenance-checked — not verbally confirmed. A quick call to the referee is the strongest final check.` **RT CI ban: NO em-dashes in user-facing copy — flag any em-dash in shipped copy (the §8.1/§9.5 strings are canon; deviation = defect).** If the shipped string deviates from canon OR adds em-dashes outside the canon string = defect.
7. **`decode.optional_field` GOTCHA (known failure mode).** `decode.optional_field` expects `Decoder(t)` where `t` = the DEFAULT's type — Option fields need `decode.optional(inner)` as the FIELD decoder. A wrong wiring here silently mis-decodes Option fields — worth a look at every new optional_field.
8. **CORRUPT-ROW RESILIENCE.** The `jsonb_typeof` guards protect the read from one corrupt row 500-ing the whole endpoint (a real pre-PR catch). A read path missing the guard = a real defect.
9. **Story AC completeness** (epics file ~line 607): the payload must carry `reference_calls[]` per §8.1 AND `attestation_on_file` AND `reference_contact_choice` (A4) "plus the referee trios, so the panel can render the Off state and the pre-trigger state without extra fetches". Check whether `reference_contact_choice` and the referee trios actually reach the payload — the AC names them explicitly.
10. **rc3-7 advisory notes** were supposed to be swept in this PR (module doc, metadata, test-helper idiom, orphaned table) — the diff contains advisory edits to `webhooks.gleam` / `webhooks_test.gleam` / `reference_exit_routes_integration_test.gleam`; verify those claims are accurate and complete (the parameterized-token test-helper fix is one; check the others were actually done, not just claimed).

## OUTPUT CONTRACT (mandatory)

Write ONLY a single valid JSON array to your assigned output file (path given in your lens brief). No prose, no markdown fencing, no preamble. `[]` is valid and expected when you find nothing real. Do not invent findings to fill a quota.

Each element must match this schema exactly:
```json
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. If you cannot quote the lines, you have not verified it — drop the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```

ACCURACY MANDATE: every finding will be independently re-verified against the worktree before reaching the report. Findings whose `evidence` cannot be located, or whose claims contradict the actual code, are DISCARDED silently. Open the file. Read the lines. Quote them verbatim. Hedging ("might", "could") = you have not verified it → drop it. Accuracy > volume. Prefer fewer, well-grounded findings over many speculative ones.
