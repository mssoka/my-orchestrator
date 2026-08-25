# LENS: architecture (source tag: `architecture`) — Perkins r1 refcheck rc4-1

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Architectural fit review against the spec + surrounding codebase. Given the diff:

- **One stable contract (AR-RC13):** the panel must render ONLY from this payload; hooks + disclaimers server-computed; no client-side state-rule re-derivation. Is the contract complete enough for RC4.2's panel (the §8.1 fields + hooks + disclaimers + attestation_on_file + reference_contact_choice + referee trios)? Any §8.1 field missing? Any state the panel needs that the payload can't answer without a second fetch?
- **§4.2 strip placement:** strip at the SQL read boundary (jsonb `#-`) — does this match the architecture's "the landlord API (AD-11) strips them" and the `ai_analysis.category_scores` precedent of carrying JSONB-as-text? Is the belt-and-braces `verify_payload_has_no_internal_fields` reasonable or redundant? Is the strip in the right layer?
- **Degradation posture:** read failure → empty array / false (panel renders pre-trigger state rather than failing the detail page). Reasonable? Does it mask real errors (silent `_` catch-all)? Compare with how the rest of `handle_get_detail` treats its sidecars.
- **`display_disclaimer` computation:** server-rendered per channel per §9.5 — the implementation keys off "verification block present" as a proxy for written-channel. Is that the right discriminator vs the stored `channel: "form"/"manual"` field? (The §9.5 rule is channel-based; the code uses verification-presence. Are they equivalent for v1 rows? A `manual`-channel row WITH verification — does it get the disclaimer? Should it?)
- **Hook computation placement:** `compute_hooks` in the handler vs the shared codec — fine? The decode-fallback design (unknown status → Failed render + Failed hooks) — agree with the "hooks can never diverge from wire status" goal?
- **Module boundaries:** new code lives in `application/application_detail_handler.gleam` + `application/sql.gleam` (Squirrel-generated) + `shared/reference_call.gleam` — does the reference-check domain belong in `reference_checks/` instead? Is the coupling acceptable? (Story files say `application_detail_handler.gleam` — the architecture AD-11 rationale names it. Note only if genuinely wrong.)
- **Future-proofing:** RC4.2–4.4 build on this contract — any shape choice that will force a breaking change? (e.g. `result` as text vs object; `outcome` as Option; the hooks object extensibility.)
- **AR21:** shared types + codecs with round-trip tests — does the codec convention match the repo's canonical compilation-boundary pattern (compare `shared/application.gleam` codec style)? snake_case unbroken?
- Does complexity match the problem? Premature abstraction? Unnecessary coupling?

Verify claims against the actual worktree files before filing.
