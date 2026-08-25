# Briefing — packet-plumber-v2-5.8-qos-panel (QoS panel + assignment-driven auto-reservation)

- **Job id:** `packet-plumber-v2-5.8-qos-panel`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-5.8-qos-panel`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (canon-surface gameplay code — QoS semantics + serialization).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` — sibling jobs (5.6/5.3/5.7) may merge while you work; rebase onto
  origin/v2 when they do (you share `app/main.odin` + `core/qos.odin`).
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will be
  red/not-started until the user fixes it. NOT a code failure. Run the FULL local suite
  green (`odin test`, `harness run`) before opening the PR; Perkins verifies locally.

## Mission — make QoS legible: a real panel + assignment-driven bandwidth splits
(user design ruling 2026-08-14)

**The problem the user found:** the QoS mechanic exists but is invisible. Today: with a
pipe selected, `1/2` picks a class and `E/S/B` assigns its lane (per-pipe override,
GDD M2), and right-click cycles an opaque "emphasis dial" (story 3.2, weight presets
from `balance.json`). Players cannot see what any of it does. The user's mental model:
*assign a packet type to a lane → that lane gets a defined bandwidth reservation* — and
he ruled the design (below).

**The design (user-ruled — BOTH, auto by default + manual for the tinkerer):**

1. **QoS panel** — selecting a pipe shows a panel (replacing the invisible dial):
   per-type rows (class → lane assignment, clickable or E/S/B), the resulting lane
   split with real numbers, and a manual-edit affordance. The right-click dial RETIRES
   into the panel (keep right-click as a shortcut that opens/cycles the panel's
   emphasis presets only if it stays discoverable — else remove it; document your
   choice).
2. **Auto-reservation (default, the easy path):** the lane weight split FOLLOWS the
   player's type→lane assignments, from a fixed ladder (user's numbers): **1 lane used
   = 100% · 2 lanes = 70/30 · 3 lanes = 50/30/20**. Assign streaming→Express and
   Express reserves its share automatically. The ladder lives in `balance.json`
   (data-driven, ODN-5 — not hardcoded literals; §16.3 greps for that).
3. **Manual override (the advanced path):** a per-pipe weight editor — the player
   tweaks the %s directly (this realizes the GDD M2 "full per-lane WFQ weights are a
   depth layer" line). Manual pipes are marked as such in the panel (and revertible to
   auto).
4. **Canon-safe boundary (load-bearing):** the type→lane CALL stays 100% player-owned —
   every type still rides Standard until the player categorizes it (08-12 canon).
   ONLY the bandwidth split auto-follows. The `Cmd_Set_Emphasis` / weight command path
   (3.2) stays the serialized mechanism — the auto-ladder COMPUTES a weight set from
   the lane assignments and writes it through the SAME command path, so replay
   equality `[E10]` holds by construction. If the computation needs a new command
   shape, STOP and flag before inventing one (LOG_VERSION discipline).
5. **Harder-eras / "advanced mode" gating** of manual editing = FUTURE knob — document
   as `[ASSUMPTION]` in the PR body + story card; do not build it.
6. **Canon amend rides this PR** (precedent: 3.2/3.3 carried their canon): update
   GDD `gdd.md` §M2 lever #2 (the emphasis-dial MVP line becomes: dial evolved into
   the QoS panel with assignment-driven auto-splits (50/30/20 ladder) + manual
   override) and add a cross-ref line in the architecture's ODN-3 section. Keep both
   edits SMALL and precise.
   **UPDATE: this canon amend is ALREADY DONE (commit `5f51236` on v2 — GDD M2 +
   ODN-3 + balance.json fields).** Read the canon at start and align — do not
   re-amend; if the implementation needs a different ladder value, STOP and flag
   instead of changing the doc.

**Acceptance:**

1. Select a pipe → QoS panel shows per-type lane assignments + the resulting split
   with numbers; assigning a type to a lane updates the split per the ladder
   (1/100, 2→70/30, 3→50/30/20) — visible immediately.
2. Manual override: edit weights per pipe; panel marks manual pipes; revert to auto
   works.
3. Lane widths on the pipe visual reflect the split (the painted-lane canon); node
   serialization (Express → Standard → Best-effort) uses the split.
4. Replay equality: runs with assignments/overrides replay byte-identical `[E10]`.
5. Existing goldens: T1/T2 MUST NOT shift for logs with no QoS edits; goldens WITH
   QoS edits that changed semantics may need mechanical re-bless — apply the 4.3
   discipline (provable fold only, zero unexplained pixel drift) or STOP and flag.
   New goldens: T2 of a 3-lane 50/30/20 assignment + a manual-override pipe.
6. Full local suite green.
7. PR body carries the story 5.8 card in
   `_bmad-output/planning-artifacts/sprints/stories-v2.md` + the GDD/arch amend +
   the `[ASSUMPTION]` notes.

**Scope guard:** the panel + auto-ladder + manual override only. No economy, no
advanced-mode gating, no new command kinds, no node-triage UI (junctions forward
per-packet, canon), no balance retuning.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.8-qos-panel
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
