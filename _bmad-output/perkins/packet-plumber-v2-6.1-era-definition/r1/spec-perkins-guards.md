## r1 guards (round-specific — fresh PR, the era-FSM canon)

**The ONE hard blocker class — the era FSM honors the determinism spine
AND the data contracts:**

- **The FSM advance is replay-deterministic by construction:** Cmd_Era_Advance
  is a LOGGED action-log command (E10 — replay identity for fired AND
  deferred advances must hold); era_step lives at the reserved [LATER]
  seam (arch §6.6); the E14 no-mid-crisis deferral (an active crisis
  holds the advance until it clears) must be deterministic — verify the
  deferral test uses a REAL engine crisis (not a stub) and replay
  identity is asserted for both the fired and the deferred path.
- **eras.json honors the data-driven contract [ODN-5]:** integer-only +
  fail-fast at load; the TWO load-time invariants (the
  roster/unlock tables must exactly equal the era_introduced-derived
  sets; every demand entry class must be in its era's roster) — verify
  the invariants are real (a violating row FAILS load, mutation-checked)
  and non-circular (they can't silently pass with a wrong table).
- **LOG_VERSION 4→5 is honest:** the log header now carries the run-setup
  era; the golden era_advance.dem (era 2→3 flip, streaming spawns) is the
  T1 of the era-advanced state, replay-verified. Verify the version bump
  is confined to the header (byte-compare old-format logs) and the golden
  is byte-stable.
- **The deliberate re-bless (the eras.json catalog fold) is
  cause-partitioned:** fold-check PASS (boot's tick-1 shift is the catalog
  fold alone), T2 pixels byte-identical, log re-bless header-only (version
  byte + catalog_hash — byte-verified). Verify the partition mechanically
  (PNG diff + log byte-compare vs v2).
- **The 6.2 gate surface is present, not built:** era_advance_blocked +
  the unlock queries exist as the seam for 6.2 — verify they're read-only
  surface (no advance logic smuggled in). Follow-ups named in the PR
  (6.2 advance conditions, 6.3 legacy decay, eras 1/2 re-tune + eras
  4-6 content, the app-side trigger) must NOT be in this diff — scope
  creep = blocker-class.
- **The 6 new FSM tests + 20 catalog fail-fast rows are non-vacuous:**
  mutation-check the E14 deferral and at least one invariant.

**What NOT to re-litigate:** the 5.11 roster + era gates + W9 honest pin
(4-round approved); the 5.12 estates ruling + group uplink aggregation
(1-round approved); the #65 sprite canon (lavish-APPROVED); the
5.9/5.10 accumulator contracts; the fold-check harness (N11 of 5.11 —
done); the fallback-model caveat.

**Verdict severity:** cap lifted — if the FSM is replay-deterministic
(both paths), the invariants bite, the version bump + re-bless are
partition-exact, and the scope guard held, APPROVE. Warnings ≠ blockers.

**CI note:** GitHub Actions on Packet-Plumber is org-billing-blocked
(runners never start — the retired-caveat class) — NOT a signal; the
local suite is ground truth (minion reports 10/10 gates, 205 core
tests).
