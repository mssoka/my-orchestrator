### Story 7.2 — Audio juice (1–2 stings)

- **Slice:** 7 · **Epic(s):** E8.3 · **Systems:** Audio (minimal) `[ODN-15]`.
- **Goal.** 1–2 Suno stings (crisis alert + arrival click) with variant selection from the
  **app-owned cosmetic rng** (determinism-neutral).

**Given/When/Then:**
- **Given** the raudio layer + the cosmetic rng;
- **When** a crisis fires (or a packet arrives);
- **Then** a sting plays; the SFX variant pick draws from the **app-owned cosmetic rng only**
  (never the sim rng) `[ODN-15]`; every audio alert is captioned on-screen.

- **Edge-case contracts:** `[ODN-15]` cosmetic rng. **Golden:** T1 (audio events don't perturb
  the sim hash).
- **Launchable increment:** the game sounds like saving the internet (just enough).
- **Status:** implemented 2026-08-17 — PR open (the app audio module `app/audio` — crisis
  sting + arrival click via raudio, variants from the app-owned cosmetic rng `[ODN-15]`,
  procedural placeholders behind the `assets/audio` drop-in contract, alert captions;
  the `audio` T1 determinism golden: consumer interleaved live vs the no-consumer replay
  gate, byte-identical).
