## 🤖 Perkins automated review — round 1
**Job:** righttenantry-dublin-rents-q2-2026 · **Reviewed sha:** `39d313d` · **Reviewers:** 7/7 completed
**Verification:** 11/13 findings confirmed against the code and live data sources — 2 discarded as false-positive

**Data verification (this round's core):** every rendered figure cross-checked against primary sources — Dublin 2-bed **€2,634**, national **€2,204**, **+1.4% QoQ**, Q1's record **4.4%**, Dublin **+6.5% y/y** confirmed via RTE (24 Aug) and The Journal (23 Aug) quoting the Daft Q2 2026 report; **€1,755/+5.0%** and **€1,503/+4.4%** confirmed via ESRI's RTB Rent Index Q4 2025 key findings. Three-figure discipline holds (asking / new-registered / existing-registered, correctly sourced and scoped). Surfacing verified mechanically: route + sitemap + hub derive from the `posts` const, hub sorts `published_iso` desc, OG card is a committed 1200×630 PNG pinned by the orphan test, suite green (1530 passed). cpi const already at 340bps/June (#526). OG aesthetics were KYLE-verified by the implementer; pixel checks here were mechanical only.

*Rejected as false-positives:* a blocker claiming "unverified figures + TODO markers" (the figures are verified above, and the `VERIFY before prod` comments are mandated by issue #529 — same pattern as Q1), and a note claiming the body overgeneralizes a "two-bed-specific" +1.4% (it's the all-market index; the copy is right).

### Blockers (0)
None.

### Warnings (3)
1. **Hub newest-first ordering has no test** (tests) — `resources_view.gleam:172`. Ordering is enforced only by the untested `list.sort`; existing `resources_view` tests assert og-card/tracking only. A dropped or inverted sort ships a stale quarter leading the hub, undetected — against the explicit acceptance criterion. *Fix: render the hub in a unit test and pin Q2's card before Q1's.*
2. **Q1→Q2 metric switch reads as a rent fall** (codebase) — Q1 says "city-centre two-bed, €2,828"; Q2 says "two-bed apartment, €2,634", both in identical TLDR shapes. A reader of both posts sees an apparent −€194 decline that is actually a geography switch. The series is never-edited, so Q2 is the place to note the basis change. *Fix: one clause in `measures_paras` noting the metric differs from Q1's city-centre figure.*
3. **Description promises "the gap by area" but no area-level data exists** (blind) — the figures are one Dublin row + two national rows; nothing within-Dublin. Phrase copied verbatim from Q1's description (pre-existing pattern; Q1 is frozen). *Fix: drop "by area" from Q2's description.*

### Notes (6)
1. **Em dash in user-facing copy** (`rent_post.gleam:122` — "June — a marked slowdown"). Q1's copy has none; four sibling content pages lock `—` out of rendered HTML as a brand-voice rule, and a prior round (refcheck-612) scrubbed em dashes from prose. Nothing fails today. *Fix: reword with a colon or comma.*
2. **Title hardcodes "2% Cap"** — blessed by the type doc ("issue-mandated … verbatim") and Q1 precedent; body copy derives from rpz. *Fix (later): guard the cpi-bump workflow to flag series titles if CPI ever drops below the 2% ceiling.*
3. **rent-increase-notice guide still deep-links the superseded Q1 post** (`rent_increase_notice_view.gleam:35,269`) — not registry-tracked; each quarterly release must bump it by hand. *[architecture + codebase agreement]* *Fix: derive the newest slug from `rent_post.posts` or retarget `/resources#rent-data`.*
4. **Per-post view tests render Q1 only** (`content_test.gleam:745`) — datePublished/rpz/FAQ pins won't catch a Q2-copy regression. *Fix: iterate `rent_post.posts`.*
5. **Doc-comment figure hygiene** (`rent_post.gleam:81-91`) — the comment's "+0.8% QoQ" appears in no launch coverage (confirm against the report PDF during the staging pass, or drop it), and it pairs "+1.4% QoQ" with the 2-bed €2,204 though 1.4% is the all-market index. Non-rendered; keep the `VERIFY` marker per the standing rule.
6. **Advisory test gate: PASS** — P0 100%, P1 100%, overall ~85%.

### Reviewer agreement
- Q1 deep-link staleness in the rent-increase-notice guide — flagged independently by architecture and codebase lenses.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
