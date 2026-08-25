# Briefing — packet-plumber-terminology-audit (networking-first vocabulary: audit → user verdict → rename PR)

- **Job id:** `packet-plumber-terminology-audit`
- **Repo:** packet-plumber · **Base:** `v2` @ latest · **Slug:** `pp-terminology-audit`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-investigate` (the coinage inventory sweep — exhaustive,
  evidence-cited) + `lavish` (the decision artifact — the user rules on borderline
  rows in-browser BEFORE any rename PR).
- **Perkins:** the eventual rename PR carries `pr_review: 1` (canon docs + code
  identifiers; cheap insurance). Phase 1 (audit) is no-PR.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders.
- **NO-PR signal for Phase 1:** on presenting the lavish artifact, run
  `herdr notification show "packet-plumber-terminology-audit" --body "audit table
  ready for user verdict"`.

## Mission — Phase 1: the terminology audit (USER CANON, ruling 2026-08-15)

**The ruling (verbatim context):** the user is a network engineer; the game is a
networking game; therefore **real networking terms unless the software term is more
accurate** (arrays, stack, pool — keep), and **game-identity words stay** (bundle,
demolish, severance — Mini Motorways lineage, not networking claims). Known example
from the user: "drop ladder" → **drop precedence** (RFC 2597 AF semantics: BE sheds
first, next victim only once the lower rung is exhausted — that's precedence).

**Phase 1 deliverable — a lavish decision table:**

1. **Inventory:** grep the coinage across code comments, GDD, architecture doc,
   stories-v2, sprint-plan, project-context — every recurring project-coined term
   with its meaning in-mechanic + where it lives (counts per surface).
2. **The table, three verdict columns:**
   - ✅ RENAME (coinage where a networking term is equal-or-more accurate) — propose
     the term + RFC/industry citation where one exists (drop ladder → drop
     precedence; audit "lane" → class queue, "strain/pressure" → congestion/
     utilization, etc. — YOU find the rest).
   - 🛑 KEEP-SOFTWARE (arrays, stack, pool, queue — more accurate than any
     networking gloss).
   - 🛑 KEEP-GAME-IDENTITY (bundle, demolish, severance, set-piece, era...).
   - ❓ BORDERLINE (genuinely arguable — the USER rules these in the lavish review).
3. **Rename-cost column** for every ✅: which surfaces (comments/docs only vs
   identifiers), serialized-contract impact (must be NONE — enum/struct
   serialization is by value/layout, prove it), golden impact (NONE expected —
   prose/comments don't render; if a term appears in a rendered HUD string, flag it
   as a T2 golden-fold candidate).
4. **Proposed canon line** for the GDD decision-log (the terminology rule, so future
   stories inherit it — including the queued visibility job, whose HUD surfaces will
   USE these terms).

**Phase 2 (ONLY after the user's lavish verdict):** the rename PR — comments, docs,
non-serialized identifiers per the ruled table; serialized contracts + LOG_VERSION
untouched; T1/replay byte-identity proven in the PR body; the GDD canon line lands
in the same PR. Queue note: Silas serializes the PR behind 5.2's merge (comment-level
overlap with in-flight 5.2 is likely).

**Scope guard:** vocabulary ONLY. No mechanic, balance, rendering, or behavior
changes. No HUD string changes in Phase 2 unless the verdict explicitly rules a
rendered string (then it's a deliberate T2 fold, listed).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: pp-terminology-audit
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1   (phase-2 PR only)
```
