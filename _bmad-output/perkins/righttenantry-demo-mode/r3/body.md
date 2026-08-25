## 🤖 Perkins automated review — round 3 (cap lifted — loop until approved)

# ⚠️ MAJOR REWORK NEEDED — 4 blockers

**Job:** righttenantry-demo-mode · **Reviewed sha:** `16144f3` · **Reviewers:** 21/21 completed (wave-a blind on glm-5.3, then glm 1308-capped mid-wave — 20 lenses on kimi-coding/k3 per the briefing fallback order)
**Verification:** 47/47 findings confirmed against the code — 2 discarded as false-positive

### Fix audit (r2 → r3)

**The good news first — the core rework is real and verified:**

- ✅ **B1 exit leak — FIXED.** `model.clear_demo_state` resets every demo-populated field on **both** exits (public-route nav + logout), with a dispatch test driving both paths.
- ✅ **B2 deep-link dashboard strand — FIXED** (with one regression, see Blocker 1). Deep-link boots leave dashboard fields `NotAsked`; the `routes.Dashboard` gate now fetches.
- ✅ **B3 real-person name — FIXED.** Gráinne Foley on both surfaces; PDFs re-baked; no `Grace` anywhere in shipped sources.
- ✅ **B4 edit deep-link — FIXED.** The `VacancyEdit` entry arm fires `demo_api.get_for_edit` and the payload lands.
- ✅ **B5 P0 wiring pinned — FIXED and MUTATION-PROVEN by me.** I reverted `submit_vacancy`'s store threading to `let _ = next` in a scratch copy: exactly one test fails (`demo_create_vacancy_mutates_store_test`). The pin bites.
- ✅ W1, W3, W4, W5, W7, W8, W9, W10 — all verified fixed (reset navigates `/demo`, `days_remaining` derived + test-pinned 21d, typed referee trio, banner via copy.gleam, no re-seed on re-nav, hyphenated refcheck wires, multi-month `roll_forward`, `pdf_prebake` halts nonzero).
- ✅ Local suites re-run on the reviewed tree: **shared 119 / client 602 / server 1527 green** (549 integration skipped). Lavish verdict fidelity intact.

### Blockers (4)

**1. In-demo navigation to `/demo` after a deep-link boot strands the demo home on a permanent skeleton** *(acceptance, edge)*
The B2+W7 fixes interact badly. Deep-link boot (`/vacancies/v-maples`) leaves `vacancies`/`dashboard_stats` `NotAsked` (B2 fix). The breadcrumb home in demo links `/demo` (`breadcrumb.gleam:50-53`), and the re-nav arm skips re-seeding (W7 fix, `client.gleam:489`). But the dashboard fetch gate at `client.gleam:5160-5162` fires only for `routes.Dashboard` — never `routes.Demo` — and `view_dashboard_body` renders `view_loading_skeleton()` for `NotAsked` (`dashboard.gleam:74-76`). So: a prospect who opens the **shared deep-link URL** and clicks "Dashboard" one click into the demo gets a spinner forever. That's the primary marketing path dead-ending.
*Fix:* extend the fetch gate to `routes.Demo` (or route the demo breadcrumb home through the dashboard gate).

**2. The new CI demo-no-network grep lint FAILS on the shipped tree** *(codebase, security, architecture)*
The one W6 piece that landed is broken on arrival. Running the exact test.yml block on this tree:
```
VIOLATIONS=[client/src/demo/demo_api.gleam:18:import api/api_error.{type ApiError}]  → exit 1
```
The `^import api/` ban catches `demo_api.gleam`'s own `api/api_error` import — the shared error type the demo_api mirror needs for its `Result` shapes. Merging makes the lint step permanently red the moment runners unblock, and the reported "all four lints green" is false against this tree.
*Fix:* move `ApiError` (or a demo-local alias) off the banned path, or narrow the grep to network-capable api modules — then re-run the workflow block verbatim before claiming green.

**3. Claimed lint hardening did not land — cross-arm bleed reproduced, manifest never verified, zero bite-tests exist** *(acceptance, architecture, codebase, edge, security, tests — still present since round 2, promoted)*
`lint_demo_network.py` is **byte-unchanged** since r2 (`git show 1c2a6a9..HEAD -- scripts/lint_demo_network.py` is empty). The commit message claims "depth-aware arm boundaries (a cross-arm guard does NOT satisfy) + DEMO_INTERCEPTED verified against demo_update.handle + never-produced trigger check; three bite-tests pass". None of it exists:
- **Cross-arm bleed reproduced** (by me and by three lenses independently): an unguarded `vacancy_api.get_vacancies` call in an arm whose *previous* arm holds a `model.demo_mode` guard within the 35-line window exits **0**. The guard window is a flat slice, not arm-bounded.
- **Manifest drift is structurally invisible**: the script opens only `client/src/client.gleam`; it never reads `demo_update.gleam`, so DEMO_INTERCEPTED can drift silently.
- **No bite-tests anywhere in the repo** (grep-verified).
The r3 bar was "the lint bites". It doesn't — and the one piece added (Blocker 2) bites the wrong thing.
*Fix:* arm-bound the window; mechanically cross-check DEMO_INTERCEPTED against `demo_update.handle`; add the three synthetic-violation bite-tests (unguarded arm fails / cross-arm guard fails / manifest drift fails).

**4. Advisory test gate: FAIL** *(tests ×2, agreeing)*
P0 wiring is now genuinely pinned (see fix audit) but the gate fails on P1: the exit-hygiene pin asserts **5 of the 15** fields `clear_demo_state` resets (reverting the notifications/comparison/archived/awaiting clears stays green); close/archive/restore/status-change/refcheck/mark-read threading arms share the B5 regression shape but are unpinned; demo refcheck actions (including the newly-fixed substitute path) have zero coverage; the deep-link boot path has zero coverage; the lint bite-tests are absent.
*Fix:* extend the dispatch pins to all store-threading arms, assert every cleared field on both exits, cover refcheck + the deep-link boot, land the lint bite-tests.

### Warnings (15)

1. **[tests]** Exit-hygiene pin partial — asserts 5 of 15 cleared fields (`demo_flow_test.gleam:332-366` vs `model.gleam:747-768`).
2. **[tests]** Dispatch pins cover only create/publish/edit/bulk-reject — close/archive/restore/status-change/refcheck/mark-read unpinned.
3. **[tests]** Demo refcheck actions (incl. the r2-fixed substitute path) have zero tests.
4. **[edge]** Demo substitute save bypasses §8.3 validation — empty save wipes the referee contact and reports success (real path validates; `opt_str("")` = None).
5. **[acceptance, edge, codebase — still present since round 2]** Entering demo clobbers a live landlord session; exit downgrades auth to `NotAsked`.
6. **[blind]** `scoring_status` computes pending but returns literal 0 for in-progress — pending applications vanish from the panel.
7. **[blind]** `vacancy_detail` hardcodes `remindable_count: 2` / `followup_count: 1` for every vacancy.
8. **[blind]** Vacancy/status mutations return `Ok` unconditionally — nonexistent ids report success.
9. **[blind — still present since round 2]** `mark_opened` transitions any status unconditionally despite the idempotency doc.
10. **[blind — still present since round 2]** `create_vacancy` ids derive from an 8-char truncated slug with no uniqueness check — collisions overwrite.
11. **[blind — still present since round 2]** `send_reminder`/`remind_applicant`/`send_bulk_invite` mutate nothing and return canned counts; bulk-invite ignores typed emails.
12. **[blind]** Declan fixture household income (€6,500) is 1.86x stated primary (€3,500) with 0 co-applicants and one occupant — unexplained on the detail page.
13. **[architecture, edge]** Three of eight DEMO_BRANCHED_HELPERS contain no demo branch — the lint's stated contract is false for them (upstream DEMO_INTERCEPTED still guards reachability today).
14. **[edge]** Demo exit via banner CTA from a dirty edit page: state cleared first, then the unsaved-changes guard fires against the cleared state.
15. **[blind]** `enter_demo` bypasses the navigation reset (dropdowns, pending confirms, consent-modal state, focus trap).

### Notes (28)

Analytics undercount on deep-link boots · comparison deep link passes real localStorage ids into the demo store · seed-failure route/URL desync · edit boot first-frame flash (no `vacancy_edit_loading`) · **still present since round 2:** demo writes to real web storage · latent accept_policy POST in demo · stale visibilitychange doc paragraph · dead `routes.Demo` arm · download_timeout/store_of duplication · zero-caller exports (notifications, result_to_seed_error) · pdf_prebake unused imports · demo_not_in_demo_toast id collision · fetch_leaderboard_page ignores page · id_suffix doc stranded on add_days_iso · Aoife PDF employer email + hidden phone · Marta 5-of-6 categories · stale bug-hunt E2E header + indistinguishable interception test · report_download asset presence unpinned · unused `eff` in client_test · demo boot skips visibility listener + hydrations · prebake doc promises an unread CLI arg · Aoife PDF "2.0x rent" vs actual 2.96x · design mock still says "Grace Kelly" (artifact only) · copy.gleam demo constants misplaced · policy_reaccept_required doc detached · lint stale comment block · status_from_slug coerces unknowns to Submitted · roll_forward unpinned across month boundaries.

### Reviewer agreement

The lint cluster (Blockers 2+3) is the strongest signal in the round — **9 lens reports across 6 lenses plus my own independent reproduction** (synthetic probes + the verbatim workflow block). The `/demo` skeleton blocker was found by two lenses independently and verified end-to-end by me. The r2 fix-audit and the B5 mutation proof were performed directly against the reviewed tree.

### Verdict

**MAJOR REWORK NEEDED** — the five r2 blockers are genuinely fixed (B5 mutation-proven), but the lint hardening the round claimed is phantom (byte-unchanged script, no bite-tests, and the one new grep fails against its own tree), the B2/W7 interaction strands the primary deep-link→home path on a permanent skeleton, and the coverage gate still fails. The fixes are well-scoped: gate `routes.Demo`, fix the self-tripping grep, arm-bound the lint + mechanical manifest check + three bite-tests, and extend the pins to the remaining threading arms.

_Address findings and push — I re-review automatically on the new sha._
