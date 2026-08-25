# Sheep findings — field-note shards (dream 2026-08-15)

## Candidate patterns

### C1 — ECMP mixed-tier bundles: min-cost relaxation must match the equality test
- Suggested target: docs/minion-field-notes.md (new line, PP sim-truth traps family)
- Evidence: packet-plumber-routing-bandwidth-cost (2026-08-13): "mixed-tier bundles price at the FATTEST member (min tier cost) — per-pipe min relaxation must match the ECMP equality test (`dist[v] + min_cost == dist[u]`), or a later cheaper member breaks the condition (unroutable). Two-pass collection (min cost first, then equality) is the deterministic shape."
- Why it matters: derived-state collection (routing tables, bundles) must compute the min and test membership against the SAME value in a fixed two-pass order, or membership silently breaks on later cheaper members — algorithmic-invariant class, generalizes to any relaxation+filter collection.

### C2 — App-layer UI is invisible to harness goldens; verify via scratch replica + pixel-scan, never vision models
- Suggested target: docs/minion-field-notes.md (new line; extends the rlsw/T2 entries)
- Evidence: packet-plumber-v2-5.3-pause-ux (date not stated in shard; rc window ~2026-08-14): "the harness T2 captures (world+forecast+health+banner) NEVER include it, so an overlay change shifts zero goldens; the app's own frame is verifiable only via a scratch replica using the rlsw shadow (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`) + `LoadImageFromScreen`, with pixel-scan (PIL) for overlap truth — vision models misjudge absolute coordinates."
- Why it matters: zero golden-shift on an app-layer change is NOT verification — app-frame truth needs a scratch capture + programmatic pixel scan; "vision models misjudge absolute coordinates" is a new trust rule for any visual-verification job.

### C3 — HUD placement must enumerate state-dependent occupancy, not default-state layout
- Suggested target: docs/minion-field-notes.md (new line, minor)
- Evidence: packet-plumber-v2-5.3-pause-ux (date not stated in shard; rc window ~2026-08-14): "top-left column carries the QoS readout when a pipe is selected and top-right hosts the forecast during a crisis pause, so 'top-left or top-right' chips collide in the exact pause-and-plan states; anchor the chip at `win_w/2 + 240` (tracks resize)."
- Why it matters: UI slots are occupied conditionally (selection state, crisis state) — a placement that fits idle collides in exactly the states the feature targets; enumerate occupied-states + anchor at a resize-tracking coordinate.

### C4 — Presentation-only rulings still earn a same-PR canon amendment citing the ruling source
- Suggested target: docs/minion-field-notes.md (addendum to the 2026-08-09 canon-amendment craft entry)
- Evidence: packet-plumber-v2-5.3-pause-ux (date not stated in shard; rc window ~2026-08-14): "A presentation-only ruling still earns a canon amendment in the SAME PR (GDD + art-direction + story-card status line): grep the pause canon first … state the ruling source (user ruling date + job id) so canon and code can never drift again."
- Why it matters: new facet beyond the codified blast-radius/house-style rules — even code-only presentation changes embodying a user ruling must amend canon in the same PR AND cite ruling source (date + job id) so canon/code drift is detectable.

### C5 — Single-field fan-out: sync every mirror surface when SEO copy changes
- Suggested target: docs/minion-field-notes.md (new line)
- Evidence: righttenantry-ctr-metadata-619 (2026-08-14): "`rent_post.title` is a single field feeding `<title>`, H1, JSON-LD headline and og:title — changing the SEO title changes the visible H1 by design … rpz's `WebApplication` JSON-LD description mirrored the old meta description and needed the same-string sync (mirror rule generalizes beyond OG)."
- Why it matters: one source field fans out to multiple surfaces (title tag, H1, JSON-LD, og:*) — a copy change must sync all mirrors in the same PR, and SEO copy may be user-visible by design (check the field doc before assuming presentation-only).

## Already codified (recurrence evidence only)

- Re-bless PROOF via catalog_hash splice — already codified (2026-08-13, "PP v2 golden discipline" ×6). Recurrence: routing-bandwidth-cost (2026-08-13) "all 16 demos did" — strengthens with a full-fleet proof instance.
- Narrow-tier max_span ≤ 10 silent draw rejection — already codified (2026-08-13, "reported success LIES" ×4). Recurrence: routing-bandwidth-cost (2026-08-13) "the 2.2 diamond's 13-spans reject at draw" — ×5, adds TEST-GEOMETRY framing (fixture diamonds must be span-legal).
- Odin `{{`/`}}` literal braces — already codified (2026-08-13 harness addendum, for JSON literals). Recurrence: routing-bandwidth-cost (2026-08-13) extends it to expectf/fmt strings generally.
- Lustre serialized-render pinning (`&#39;` escapes, attributes sorted by name) — already codified (2026-08-03 "assert Lustre's SERIALIZED render"). Recurrence: righttenantry-ctr-metadata-619 (2026-08-14), now on erlang target + metadata tags, adding `escape_for_html` + exact tag terminators "or they silently no-op" — strengthens with the metadata-test flavor.
- "Pin the RENDERED html, not source strings" (auto-appended `| RightTenantry` suffix, one description field → meta + og) — same 2026-08-03 serialized-render entry covers the class; the suffix/auto-append specifics are repo detail.
