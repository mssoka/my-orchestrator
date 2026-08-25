## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-613-615 · **Reviewed sha:** `552aea5` · **Reviewers:** 7/7 completed
**Verification:** 10/12 reviewer findings confirmed against the code — 2 discarded (both re-litigated the documented, user-flagged 320×480 corner trade-off that the round briefing explicitly scopes out; their in-scope residue — README prose accuracy — is kept as N4)

### Blockers (0)

None. Guards verified clean: no user-facing "Viewed"/"VIEWED" string literal survives anywhere in client/shared/server sources; the DB enum, refcheck trigger logic, and `vacancy.viewed_at` are untouched (git diff empty for `supabase/migrations/`); `consent.js` is byte-identical; the new hint copy is em-dash-free and joins the `no_em_dash_test` scan; the term "Viewing held" renders consistently from the single `label_for_slug_opt` source of truth (stepper stop, backward modal, audit trail) plus pill/detail-pill surfaces. Local `make test` green at the reviewed sha; evidence artifact present with vision-verified screenshots.

### Warnings (3)

- **W1 · Detail-page `VIEWING HELD` pill unpinned** [`client/src/pages/application_detail.gleam:566`] — every detail-page test renders the `Submitted` fixture (`client_test.gleam:2276`), so the Viewed pill arm never renders: reverting to `VIEWED` passes the entire suite. The added `>VIEWED<` absent pin is vacuous for this surface. 4/5 #613 surfaces are pinned; this is the fifth. *Fix: one detail test with a Viewed-status app asserting `VIEWING HELD` present / `>VIEWED<` absent.*
- **W2 · Unbounded multi-toast stack can reach the banner's buttons on small viewports** [`client/src/components/toast.gleam:34`] — the container has no max-height; 5 stacked toasts (~72px + 12px gaps, cap verified) reach y≈488. On 320×480/568 where the collapsed banner fits, 3–5 concurrent toasts (5–8s lifetimes) cover the bottom-aligned buttons and outrank the banner's z. The evidence validated a single toast only, so the README's "every case where the buttons actually ARE bottom-aligned" is overstated. Rare in practice and self-healing (dismissible, auto-dismisses). *Fix: bound the stack (max-height/overflow or clamp live toasts to 2–3) and/or scope the README guarantee to the single-toast case.*
- **W3 · Advisory test gate: CONCERNS** — P0 gaps: none (client-only copy/CSS diff). #615 pinned (class pin + evidence). #613 at 80% (W1). The W1 test lifts the gate to PASS.

### Notes (5)

- **N1 ·** Hint `is_current`-absence branch untested — only the title-present branch is pinned; nothing asserts the hint is omitted when the viewed stop IS current (the R1 review fix). Fold into the W1 fixture. [blind+tests agree]
- **N2 ·** Layout accommodation unpinned — neither the 6rem status track nor the pill `whitespace-nowrap` has a regression pin; reverting either silently overflows the leaderboard. This diff itself sets the class-pin precedent (toast test).
- **N3 ·** One-way z linkage — `z-[2147483001]` derives from `consent.js:393`'s `2147483000` via comment only; a future banner z raise silently re-hides toasts. Consider extending the toast test to read `consent.js` and assert the ordering.
- **N4 ·** Corner README prose vs its own geometry — the toast (y 80–152) does **not** intersect "Reject all" (y 9–52); only "Customize"/"Accept all" are overlapped, and the buttons are stacked, not a "row". Documentation-accuracy only; the trade-off itself is user-flagged and not re-litigated. [blind+acceptance agree]
- **N5 ·** "Viewing held" lives in four literals across three modules (incl. a hand-uppercased twin) — spec-sanctioned inline pattern for this diff; a follow-up could hoist status labels into `copy.gleam` consts.

### Reviewer agreement
N4 (blind + acceptance) and N1 (blind + tests) were independently confirmed by two lenses each — highest-confidence findings in this round.

**Verdict:** READY TO MERGE

_All guards held: enum/trigger/`viewed_at` untouched, `consent.js` untouched, one term everywhere, dash-free copy, local suite green at the sha. The three warnings are regression-pinning and boundary hardening — none block this merge; W1 is the one I'd fold in before or immediately after merge._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
