### Story 6.1 — Era definition (Email→Streaming data)

- **Slice:** 6 · **Epic(s):** E5.1 · **Systems:** Era FSM (S6) `[ODN-16]`.
- **Goal.** Era data (Era 2→3: per-era packet types, demand signature, infrastructure) loaded
  from `eras.json`; the era FSM advances the active era.

**Given/When/When/Then:**
- **Given** the `eras.json` catalog + the era FSM;
- **When** an era advance fires;
- **Then** the new era's unlocks load (streaming becomes available, new demand signature);
  catalog data is integer-only + fail-fast validated `[ODN-5]`; no mid-crisis demand spawn
  `[E14]`.

- **Edge-case contracts:** `[E14]` no-mid-crisis spawn. **Golden:** T1 of the era-advanced
  state.
- **Launchable increment:** the internet evolves — new traffic appears.

