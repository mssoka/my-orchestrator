# Sheep shards — 2026-09-09

## Coverage

Counting units: a **source file/job** is one field-note shard (job id = filename stem); an **entry** is one top-level bullet. Multi-clause bullets count once. Previously processed older-tail evidence can corroborate a candidate but is not counted as new material.

### Newly processed newer-mtime shards — 2 files / 2 jobs / 9 entries

1. `/Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-typography-video-study.md` — job `packet-plumber-3d-typography-video-study`; read in full; 3 entries dated 2026-09-08, all certainly after the marker.
2. `/Users/moses/code/_bmad-output/field-notes/youtube-channel-selva-electrica-assets-rigs.md` — job `youtube-channel-selva-electrica-assets-rigs`; read in full; 6 entries dated only 2026-09-07. Its mtime is 2026-09-07T23:53:35Z, after the 2026-09-07T00:39:44Z marker, but the bullets have no times. All 6 are therefore boundary-uncertain rather than claimed certainly new. No ledger cross-check was performed, per the explicit no-ledger instruction.

New-entry accounting: **3 certainly post-marker entries + 6 boundary-uncertain same-day entries = 9 inspected entries across 2 jobs**. The current dream's own notes were not present and were not counted.

### Older-tail screen — 211 files

Read all **2,424 lines / 279,928 bytes / 211 `## SOURCE` sections** in `/Users/moses/code/_bmad-output/memory/dream-2026-09-09/inputs/field-notes-older-tails.md`, covering every inventory row marked `newer_mtime:false`. No tail contained content clearly after the marker. The only 2026-09-07-dated older source was `dream-2026-09-07.md`; its mtime (2026-09-07T00:37:40Z) predates the marker, it is the prior dream's badge-out shard, and its material is already curated, so it was not counted as new. No plausible late backfill required full-file expansion.

Source gaps: **none for the required file/tail reads**. The only evidence gap is the missing per-entry time on the 6 Selva bullets.

## Candidate patterns

### 1. Gate the final evaluated representation, not an intermediate or normalized proxy

**Proposed lesson/target.** Add a concise 3D/visual-evidence facet to the existing “verification must bind to an independent anchor” lesson: acceptance evidence must name and observe the final evaluated representation. For captures, record decoded dimensions and last-change SHA and do not use a normalized crop as pixel-compliance proof. For Blender assets, test evaluated world-space geometry, the exact side/part and active modifier order, and saved/reopened timeline behavior separately from manual controls. Comments and source formulas are intent, not proof of the resulting contract.

**Independent evidence.**

- `/Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-typography-video-study.md:1` — 2026-09-08 — job `packet-plumber-3d-typography-video-study` — **new, certain** — “PP3D L1 captures at 0818afc2 decode as1600×450 despite base1600×900: capture runner fullscreen Canvas Items+Expand normalizes width retaining aspect. Carry dimensions and last-change SHA; never use normalized crops as default font-pixel compliance proof.”
- `/Users/moses/code/_bmad-output/field-notes/youtube-channel-selva-electrica-assets-rigs.md:5` — 2026-09-07 — job `youtube-channel-selva-electrica-assets-rigs` — **new intake, boundary-uncertain** — “Contact tests must observe evaluated world-space support, not a copied formula; scale targets need exact side/part plus enabled modifier order, and saved/append timeline reveal must be tested separately from manual sliders.”
- Same typography job, supporting facet rather than a third independent incident: `/Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-typography-video-study.md:3` — 2026-09-08 — “`hud.gd` calls560 a “cap” but assigns custom_minimum_size.x; distinguish comment intent from a proven max-width contract and credit existing1600×900 real-panel layout pins before proposing broader evidence.”
- Previously processed corroborator, not new count: `/Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-asset-scout.md:4` — 2026-09-04 — job `packet-plumber-3d-asset-scout` — “"Imports lie" quantified: authoring scales ranged 0.08x–25x across sources (power plant 1.33 m, farm house 25.3 m) — normalize by MEASURED world bbox (glTF accessor min/max × node-transform walk; ~80 lines of python, no Blender needed for GLB→GLB) and carry the factor in a `PP3D_NormalizedScale` root node; Sketchfab-sourced items go through the blender MCP `download_sketchfab_model` which accepts `target_size` and self-scales (still verify by measurement).”

**Novelty/dedup.** Possible addendum, not a new standalone doctrine. The cloned store already says verification needs an independent anchor and records that authoring scales lie. What is new is the explicit **final-stage transform chain**: viewport normalization, evaluated modifiers/world space, exact target part, and persisted/reloaded behavior.

**Counterevidence and limits.** Normalized captures, source formulas, comments, and manual sliders remain useful diagnostic evidence; they are rejected only when substituted for the final contract. Do not demand expensive end-to-end captures for pure functions whose output is itself the acceptance target. One of the two new independent jobs is date-boundary-uncertain.

**Disposition.** Promote as a short addendum to the curated independent-anchor/3D evidence entry; do not create another large AGENTS gotcha.

### 2. Artifact existence after a timeout proves liveness, not completion

**Proposed lesson/target.** Amend the existing timeout doctrine: after a client/tool timeout, first check whether the producer continued, but accept/publish only an attempt tied to an identity/receipt and proven fresh, complete, and exit-zero. Do not splice frames or scene state from timed-out partial attempts into an atomic gate.

**Independent evidence.**

- `/Users/moses/code/_bmad-output/field-notes/youtube-channel-selva-electrica-assets-rigs.md:6` — 2026-09-07 — job `youtube-channel-selva-electrica-assets-rigs` — **new intake, boundary-uncertain** — “Hybrid CPU+Metal produced long CPU path-tracing tails; process-local Metal-only finished the same 156-frame source in 537.52s without quality reduction or saved preferences. Keep UUID receipts/outputs and require complete exit-zero evidence before atomic gate publication; never splice a timed-out partial attempt.”
- Previously processed independent corroborator, not new count: `/Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-blender-sculpt.md:3-7` — 2026-08-23 — job `packet-plumber-v2-blender-sculpt` — “(2026-08-23) **Never trust a piped Blender run**: `blender -b -P … | grep`”. The following source lines record that the masked failure caused stale files to be compared and require checking the producer rc plus output freshness.

**Novelty/dedup.** Possible addendum. Curated memory already says a bridge timeout is not automatically job failure and to check the output artifact. The new evidence closes the unsafe inverse: an artifact may exist yet be stale or partial, so mere existence is not gate-worthy.

**Counterevidence and limits.** A transport timeout may occur while a server-side render completes successfully; therefore timeout must not trigger an automatic kill or duplicate render. Poll/check first. Conversely, exit zero alone is insufficient if the output belongs to an older attempt; pair it with attempt identity, freshness, and job-specific completeness (for example expected frame count).

**Disposition.** Promote as a one-sentence hardening addendum to the existing tool/bridge-timeout field note.

### 3. Tooling waivers are checkout-scoped capability decisions, not inherited global facts

**Proposed lesson/target.** Before applying a historical `bmad-build`/missing-renderer waiver, probe the exact dispatched worktree/install. Use the waiver only when that checkout actually lacks or fails the renderer; a successful render retires the waiver for that lane. Preserve explicit user/briefing rulings, but do not inherit an old repo's failure by assumption.

**Independent evidence.**

- `/Users/moses/code/_bmad-output/field-notes/youtube-channel-selva-electrica-assets-rigs.md:3` — 2026-09-07 — job `youtube-channel-selva-electrica-assets-rigs` — **new intake, boundary-uncertain** — “bmad-build render_skill.py succeeded in this worktree; do not apply the older missing-renderer waiver by assumption.”
- Previously processed independent contrast, not new count: `/Users/moses/code/_bmad-output/field-notes/righttenantry-agents-model-single-source.md:4` — 2026-09-05 — job `righttenantry-agents-model-single-source` — “bmad-quick-dev is GONE from the canonical home (successor bmad-build can't render — no `_bmad/scripts/render_skill.py`); standing waiver path worked: self-contained briefing + waiver note in PR body + run bmad-build's review-prompts (`review-prompts/*.md`) directly as herdr mega-minions — step-04 discipline without the renderer.”
- Previously processed mechanism corroborator: `/Users/moses/code/_bmad-output/field-notes/pp-funfix-118-124.md:3` — 2026-09-01 — job `pp-funfix-118-124` — “PP worktree bootstrap missed `_bmad` (fully git-ignored) — `ln -s <repo_root>/_bmad _bmad` from the worktree before any bmad-build step; the render_skill.py lives at `/Users/moses/code/_bmad/scripts/` (the MAIN repo's `_bmad/scripts/` does NOT carry it).”

**Novelty/dedup.** Possible correction/clarification. The newer curated entry already says “where the repo-local `_bmad` lacks” the renderer, but an older curated paragraph still reads broadly as a standing “on this install” waiver. The success case proves the scoped wording is the durable one.

**Counterevidence and limits.** Missing-renderer and ambiguous-token failures were real in several repos; this is not a proposal to erase their workaround or retry a known-broken render indefinitely. A current explicit waiver still controls. The newly observed success is one boundary-uncertain job; older failures establish variability, not a second new success.

**Disposition.** Amend the broad waiver wording to be checkout-scoped and probe-first; retain the repo-specific failure/workaround history.

## Watch items

- **Metal-only process-local rendering envelope (single new sighting).** `/Users/moses/code/_bmad-output/field-notes/youtube-channel-selva-electrica-assets-rigs.md:6`, 2026-09-07, job `youtube-channel-selva-electrica-assets-rigs`: “Hybrid CPU+Metal produced long CPU path-tracing tails; process-local Metal-only finished the same 156-frame source in 537.52s without quality reduction or saved preferences.” Useful for another same-scene confirmation, but one render is insufficient to establish a general Blender performance policy.

## Rejected/duplicate candidates

- **Direct Blender MCP as the current native-video route.** Already present verbatim in cloned `AGENTS.md` under “Video lane (standing rules, user-ruled 2026-09-07)”. The initial Higgsfield-401 route hold was superseded later that same job. No new policy proposal.
- **User visual verdict remains the premium acceptance gate.** Already covered by the user-play/look-session and merge-click aesthetic-verdict doctrine. The rejected toy humanoid/native moth detail is job history, not a general new rule.
- **Stale `HERDR_PANE_ID` after a workspace move.** The new Selva incident is a recurrence/facet of the existing workspace-move rule (“workspace MOVE mutates the pane id; re-capture post-move”) plus existing session-path forensics. Useful evidence, but not enough novelty for another entry.
- **Combine the transcript 403 and Higgsfield 401 into one “adjacent access is not authority” doctrine.** Rejected as over-abstract: one is an evidence-scope problem (transcript available, frames unavailable), the other was a production-route authorization halt immediately superseded by a user ruling. Keep the exact boundary claims in their job shards rather than conflate them.
- **`hud.gd` calls a minimum a cap.** Not promoted separately. It is one concrete example already absorbed by Candidate 1 and by the curated “documented/comment intent is not consumed behavior” doctrine.
- **Prior dream's 2026-09-07 edit/dispatch/ledger notes.** Tail-screened, pre-marker by mtime, and already curated; excluded from new material rather than re-proposed.
