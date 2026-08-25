# Perkins briefing — round 1: packet-plumber-v2-3.5-node-placement

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/30 (targets `v2`)
- **Reviewed sha:** `666b08247e6b9052e84a628680665cd135868e4c` (short `666b082`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.5-node-placement-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-3.5-node-placement.md` + story 3.5 + 5.1 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (amended 2026-08-12 commit 9a5a35b on v2: routers NEVER director-spawned; terminals spawn, the player places routers) + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[E10]` replay determinism, `[ODN-2]` edit fast-path, `[ODN-5]` catalogs fail-fast, §11.7). No GitHub issue.
- **prior_findings:** none (this is r1 — the quick-fix port). CONTEXT: the implementing minion's badge-out (Cmd_Place_Router junction-kind only, terminals never placable; map-grid + 7-tile min-separation validation; port limits on draws via catalog port_capacity / .Router_Ports_Full; CMD_TAG_PLACE_ROUTER + LOG_VERSION 2→3, old logs reject cleanly; `at <n>ms place <type> <x> <y>` demo verb + place.dem T2 golden; tray ported (link chips select tier, router chips arm placement, click drop / click-again/ESC/right-click cancels, validity ghost); 70 core (9 new) / 10 demos / 69 drift / lint green; negative controls bite; the mandated LOG_VERSION re-bless changed exactly ONE byte (version field 2→3) per existing log — every .t1 manifest + T2 PNG untouched; ZERO catalog changes (cat.hash fold); PLACEMENT_MIN_SEP_TILES = 7 as a core const; no inventory/economy) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Story 3.5 — Restore player node placement (user ruling 2026-08-12: "nodes spawn, but I need to be able to place routers").** Ports the prototype's `Cmd_Place_Router` + hardware tray + placement mode into v2: the player picks a router chip from the tray (link chips select draw tier as before), arms placement, clicks the map to drop a validated junction, cancels with click-again/ESC/right-click; placed routers then accept drag-drawn pipes. Replay-safe (LOG_VERSION 2→3, old logs rejected cleanly, byte-identical replay [E10]).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 TERMINALS NEVER PLACABLE — THE canon (story 5.1 amendment).** Routers are NEVER director-spawned; terminals spawn, the PLAYER places routers. A path that player-places a terminal, or lets the director spawn a router = a REAL blocker.
- **🚨 REPLAY DETERMINISM [E10] + the LOG_VERSION re-bless discipline.** Placement records into the action log; same seed + same commands → identical map. The mandated LOG_VERSION 2→3 re-bless must have changed exactly the version byte — **verify the .t1 manifests and T2 PNGs are untouched** (a silent re-bless of golden content = a blocker). Old (v2) logs must reject cleanly (the 1.2→2 precedent).
- **🚨 ZERO CATALOG CHANGES (claimed).** cat.hash folds catalog bytes and the replay gate rejects on drift — the minion deliberately made no catalog changes (adding router types/balance fields would nuke every golden). VERIFY: if this PR touches the catalogs, that's a finding (or a deliberate, documented, golden-accounted change). The tray + port limits are claimed catalog-driven (port_capacity; mid/high routers land automatically when their era story adds them — currently only basic should exist). Do NOT flag "mid/high routers not in the tray" — that's the design; DO flag an invented balance.
- **VALIDATION.** Span + 7-tile min-separation (PLACEMENT_MIN_SEP_TILES = 7, a core const ported from the prototype's growth_min_dist_tiles) + no overlap + placement area; rejections return the existing `Edit_Error` style; the port-check + min-separation neutralization must make the new tests go RED (negative controls claimed). A validation hole (placing on top of an existing node, inside the forbidden band, or past the placement area) = a blocker.
- **PORT LIMITS ON DRAWS.** After placement, junction port limits apply to connections (basic 4 / mid 8 / high 16 per GDD — wired from the catalog; `.Router_Ports_Full` error when exceeded). A draw that ignores port capacity = a real defect.
- **EDIT FAST-PATH [ODN-2]** — the command flows through `Command_Bus.validate` → apply like the existing commands. A bypass of the authority (a direct mutation outside the command bus) = a blocker.
- **NO INVENTORY/ECONOMY (later story, NOT a defect).** v2 has none — do NOT flag "placement is free" / "no resource cost".
- **The prototype is REFERENCE-ONLY** (port the logic; the v2 command set is the authority). Do NOT flag "missing the prototype's draw/upgrade/demolish/lane-weights/pipe-priority/junction-triage commands" — those are later stories; 3.5 ports ONLY the PLACE command.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–3 + the harness merged; #29's Demo_Replay single-source + era-in-log-header semantics are in base).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

### Legitimate findings here would be
- **A terminal-placable path, or a director-spawned router** — a blocker [5.1 canon].
- **A determinism break** (unseeded RNG draw, map-iter order, a command not recorded, LOG_VERSION not bumped / old logs not rejected) — a blocker [E10].
- **A silent re-bless** (golden content changed beyond the mandated version byte) — a blocker.
- **A catalog change** (unless deliberate + golden-accounted) — a blocker [cat.hash fold].
- **A validation hole** (overlap / separation / area bypass) or a neutralization that doesn't go red — a blocker.
- **A draw ignoring port capacity** — a real defect.
- **A command-bus bypass [ODN-2]** — a blocker.
- **An `odin test` / `odin build` / `harness` failure at `666b082`** (core 70, demos 10 incl. place, drift 69).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 30 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.5-node-placement/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `666b082`), `spec_files` = this briefing + the job briefing + stories 3.5/5.1 + the architecture (`[E10]`/`[ODN-2]`/`[ODN-5]`/§11.7), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.5-node-placement/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 30 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 30 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `666b082`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-3.5-node-placement / **Reviewed sha:** 666b082 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-3.5-node-placement-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek (kimi's 403 is a false dawn — no k3 flips until the user explicitly says so; never glm-5.2). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
