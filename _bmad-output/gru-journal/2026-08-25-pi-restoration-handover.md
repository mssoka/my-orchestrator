# 2026-08-25 — pi/herdr restoration handover (from the DSH interlude)

Context: orchestration ran in DSH for ~1 day (2026-08-25) after the pi pivot.
User verdict: DSH's Silas lane cannot accept new tasks mid-turn, and its
workflow fan-out blocks Gru's turn — the user cannot converse while ops run.
Reverted to pi/herdr. Everything below is the live state at handover (~16:55Z).

## What was restored

- `my-orchestrator` re-cloned from origin (main @ ac9e0b4).
- `~/code/AGENTS.md` = the pi-era doc (from `dsh-orchestrator-setup/AGENTS.md.pre-dsh`).
- `~/code/bin` → `my-orchestrator/bin`; `~/code/.agents` → `my-orchestrator/.agents`;
  `~/code/.pi` → `my-orchestrator/.pi` (gru.ts / silas.ts / nefario-watch.ts intact).
- Ledger: the real 490-row DB moved back to `~/code/_bmad-output/orchestrator.db`
  (the one at that path was an empty shell, no jobs table — backed up as
  `orchestrator.db.empty-shell.bak`). Perkins rounds, field-notes, memory,
  quota-regime copied back; DSH-era briefs archived at
  `_bmad-output/briefs-archive/`.
- `dsh-orchestrator-setup/_bmad-output/` is ARCHIVED (see its ARCHIVED.md) — do not write there.
- herdr server never died (PID 83927). Night-watchman was in the launchd penalty
  box (program path vanished during the pivot); kickstarted back to exit-0 health.

## Runtime state at handover

- **Silas (pi) is ALIVE and mid-flight** on `silas-perkins-r1-completion`
  (Perkins r1 for PR #99, packet-plumber tie-deconflect): validating the 6 lens
  JSONs on disk, re-dispatching the missing codebase lens, then verify →
  consolidate → post verdict via perkins-token → ledger. Brief:
  `_bmad-output/briefs-archive/silas-perkins-r1-completion.md`.
  DO NOT double-dispatch that row.
- **Gru (pi) relaunched** on zai-coding-cn/glm-5.3 --thinking max in w85:p1.
- Provider regime: kimi-coding/k3 is 403 (billing-cycle quota wall, same as the
  DSH era); glm-5.3 probed OK via the env-cleared pi probe. Reasoning chain per
  playbook: k3 → glm-5.3 → HOLD. Everything rides glm-5.3 until k3's cycle flips.
- Orphan sweep done: stale lldb debug process (font-overhaul era) killed.

## Open board (ledger rows)

| Row | Status | Note |
|---|---|---|
| packet-plumber-v2-viscomm-tie-deconflect | in-review | PR #99 open vs v2; CI green; awaiting Perkins r1 verdict |
| packet-plumber-v2-viscomm-tie-deconflect-perkins-r1 | working | Silas completing (see above) |
| dsh-client-plugin-orchestrator-dashboard | in-review | PR #1 open (dashboard plugin) |
| dsh-dashboard-perkins-cap | dispatched | needs re-dispatch on pi lane (PerkinsRows slice(0,10) → cap 2 done rows); brief in briefs-archive |
| packet-plumber-v2-viscomm-gauge-telegraph | blocked | blocked_by tie-deconflict |
| packet-plumber-v2-viscomm-crisis-duck | clarifying | needs USER design ruling |
| packet-plumber-v2-viscomm-shape-vocab | blocked | era-gated |

- Human merges PR #99 and dashboard PR #1 — never us.
- Fixes from the r1 verdict relay to the tie minion, then r2 at the new sha.

## DSH interlude lessons worth keeping

- The DSH experiment's failure mode (for the record): one background ops agent
  cannot be interrupted with new work mid-turn; foreground fan-out starves the
  user lane. pi/herdr's persistent interleavable sessions remain the fit.
- The Perkins 7-lens / skill-file-first doctrine amendments made during the DSH
  day are real and carry over: load `~/.agents/skills/code-review/SKILL.md`
  (now correctly symlinked), run ALL lenses with verbatim briefs, blind =
  diff-ONLY. The AGENTS.md.pre-dsh already carries the 08-23-era lens doctrine;
  the 7-lens emphasis from 08-25 stands.

— the DSH orchestrator session (handing over and standing down)

## Post-handover fix (Gru, ~17:0xZ)

- `docs` symlink was MISSING from the restoration set (bin/.agents/.pi were
  symlinked, docs wasn't) — `/Users/moses/code/docs/` didn't exist, so the
  PLAYBOOK constant in gru.ts + silas.ts AND the AGENTS.md references were
  all dangling. Created `~/code/docs -> my-orchestrator/docs`. One canonical
  copy, zero duplicates.
