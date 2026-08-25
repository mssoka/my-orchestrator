### Story 5.11 — Diverse terminal types (schools, offices, homes)

- **Slice:** 5B · **Epic(s):** E3.1, E2.1 · **Systems:** catalogs `[ODN-5]` (node_types), director
  `[ODN-7]` (source_role selectors), growth (5.1 type pick).
- **Goal.** The terminal roster gains class analogues — residential / small-biz / campus — each with
  a **different, bounded demand profile** (volume, per-terminal cap =
  `cap_fraction_permille × throughput ÷ packet_bandwidth`, uniform; throughput); a campus emits far more than a home. Roster entries are catalog data
  (`node_types.json`), but a **new terminal role is a CODE change (Perkins r1 W7 — `Terminal_Role`
  is a closed enum `core/catalog.odin:22`): this card names the touch points** — the enum gains a
  variant + `role_from_name` (`core/catalog.odin:1011`) + the `collect_terminals` role selector
  (`core/flow.odin`) + the growth type-pick (`core/growth.odin`). Distinct shape/icon per type
  (never color alone `[E9.1]`).

**Given/When/Then:**
- **Given** the extended `node_types.json` roster (new `terminal_role`s + per-type cap/profile
  fields) and the demand specs whose source/sink selectors resolve against it;
- **When** the director spawns and growth (5.1) places terminals of the new types;
- **Then** each type emits its own bounded profile (campus >> home in volume and cap); the director's
  typed selectors resolve against the new types (era-gated); growth spawns the new types per its
  era gating, every spawn satisfying E31 validity + the 5.6 placement separation; the type is
  readable without color; replay is byte-identical `[E10]`; catalog fold → the slice's deliberate
  re-bless.

- **Edge-case contracts:** `[E10]` replay, `[E31]` spawn validity per type, `[E9.1]` never-color-
  alone. **Golden:** T1/T2 re-bless + a T2 frame with all three types visible.
- **Launchable increment:** run the app — homes trickle, campuses flood; the terminal roster reads
  as a spectrum.
