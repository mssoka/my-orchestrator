### Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair)

- **Slice:** 4 · **Epic(s):** E4.2, E4.3 · **Systems:** Crisis Surge (S4) `[ODN-4]`, director.
- **Goal.** The Surge archetype: a forecast 10× demand spike that cascades into saturation if
  the player is unprepared. Fires on schedule from the seed. Every crisis carries a structured
  `root_cause` (ref to the topology flaw) + a `preventive_redesign`.

**Given/When/Then:**
- **Given** the Surge SetPiece (in `crises.json`) + the Crisis Engine (downstream of flow,
  read-only topology view) `[ODN-4, REVIEW M1]`;
- **When** the surge SetPiece activates on schedule;
- **Then** the surge fires on schedule from the seed (deterministic); **no crisis without a
  resolvable root cause** + preventive redesign; **no crisis on a healthy within-capacity
  topology** `[AC-E13]`; one crisis per root-cause per activation (dedup, re-trigger only
  after `Crisis_Resolved`) `[E13]`; the Director never reads crisis state (structural —
  read-only view in) `[ODN-7, REVIEW M1]`.

- **Edge-case contracts:** `[AC-E13]` root-cause/fair, `[E13]` dedup. **Golden:** T1 +
  event-stream golden (`Crisis_Triggered{Surge}` within the scheduled window).
- **Launchable increment:** the surge hits on cue; you can see WHY (the root cause).
