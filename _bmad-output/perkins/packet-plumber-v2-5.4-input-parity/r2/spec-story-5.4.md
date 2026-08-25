### Story 5.4 — Touch + controller parity

- **Slice:** 5 · **Epic(s):** E7.1, E7.3 · **Systems:** Input parity `[ODN-12]`.
- **Goal.** The same game on touch + controller, via the intent layer (new device mappings
  onto the same intents; parity by construction `[FORGE #6]`).
- **Status:** implemented 2026-08-16 — PR open (the `app/input` intent layer: raw device
  events → typed `Intent` → one shared validated-Command executor; mouse behavior preserved
  exactly, touch (drag-draw/tap-select/two-finger-pan) + controller (node-select/aim-confirm/
  tier-class-cycle) map onto the same intents; `harness input-parity` — the T1 across-inputs
  golden: scripted device-event frames assert mouse == touch == controller command + hash
  streams, blessed as `goldens/input_parity_*.t1`; no `LOG_VERSION` bump — inputs are never
  serialized). **Scope flag:** two-finger pan maps to the `Pan` intent but the camera-fit view
  has no pan state — a deliberate no-op, flagged per `[§18 OQ-1]` (camera work is a later
  story, not this one).

**Given/When/Then:**
- **Given** the intent layer + touch (drag-draw, tap-select, two-finger pan) + controller
  (node-select, aim/confirm, tier/class cycling) mappings;
- **When** the player draws/selects via touch or controller;
- **Then** the resulting Commands are **the same shapes** as mouse `[ODN-12]`; landscape-only
  framing is a camera-fit decision (desktop-first launch) `[§18 OQ-1]`.

- **Edge-case contracts:** `[ODN-12]` input parity. **Golden:** T1 (same Command stream across
  inputs).
- **Launchable increment:** play on touch + controller, same as mouse.
