# Briefing: packet-plumber-v2-viscomm-regression-audit

READ-ONLY forensic audit. NO code changes, NO branch commits, NO PR.
Deliverable = an evidence-graded findings report + lavish HTML review.
You are auditing, not fixing. Fix routing is the user's decision AFTER review.

## Context

The v2 viscomm lane implements visual-communication effects from the Indie
Game Clinic video "Visual Communication: Why Game Art Matters"
(https://www.youtube.com/watch?v=SV1BBtD3hY4 — 2025-12-19). The lane landed:

- PR #99  tie-deconflect (merged 08-25): route_tie telegraph de-conflicted
  from the congestion-warning hue (audit finding A).
- PR #100 gauge-telegraph (merged 08-25): gauges LERP to new values, never
  snap; terminal snap pinned (audit finding B).
- PR #102 crisis-duck (merged 08-26): non-involved network desaturates
  during crisis; halo raw blend; packet chain pins (audit finding C).
- PR #95  dublin-map-beautify (merged 08-24): environmental look polish.

The LAST LOOK change is PR #105 look-zoom-language (merge 03dd6f8,
2026-08-27): L1 scale covenant + laneless link ladder; L2 toward-space
ladder + dusk dial; L3 reduced-motion PINS THE BREATH; L4 ruled node
ladder + SPRITES-ONLY Dublin + ring floor. It reworked app/render heavily:
dublin.odin (-165 net, the draw path went sprites-only), view.odin
(rewritten, +473/-402 across render/), wire_path.odin trimmed,
sprites.odin, crisis.odin, assist.odin touched.

USER REPORT: after #105, some of the viscomm video effects LOOK LOST.
Your job: determine, per effect, whether it is INTACT / DEGRADED / LOST /
FLAG-GATED, with mechanical evidence and the exact severing commit+hunk.

## Reference: effect classes from the video (map to the lane)

1. Count-up lerp — values tween to new state (player sees change via
   movement). Lane: gauge-telegraph (#100), counters.
2. Flash-before-drain / chunking — drained segment flashes before
   disappearing (health-bar class). Lane: gauge/crisis edges.
3. Attention via CONTRAST — reserve high-contrast for what matters NOW;
   desaturate the irrelevant. Lane: crisis-duck desat (#102), dusk dial.
4. Distinct telegraphs per meaning — never reuse one signal for two
   meanings. Lane: tie-deconflect (#99) — route_tie vs congestion hue.
   NOTE: the LINK CONGESTION PULSE itself (links pulsating as they
   congest) is a pre-existing effect the lane built AROUND (#99
   de-conflicted route_tie from its hue) — audit it as its own row;
   user-named keep candidate.
5. Idle/breath movement — cheapest attention draw is motion. Lane: the
   breath (pinned by L3 reduced-motion), node ladder life.
6. Gestalt grouping/hierarchy — pairing, scale covenant, ring floor,
   node ladder. Lane: #105 itself (verify not accidentally regressive).
7. Affordance cues — object look implies behavior. Lane: packet chain
   pins, silhouettes.

## Method (evidence first, always)

1. **Inventory.** Build the full effect inventory from: the video classes
   above; the prior design-audit artifacts at
   `_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/`
   (kyle-findings.md, design-audit.html — findings A/B/C spawned the
   lane); PR bodies of #95/#99/#100/#102/#105 (`gh pr view`); the
   look_l1/l2/l4 + palette_polish + pullback tests (each test pins an
   intended visual behavior — read what they assert).
2. **Path trace, BEFORE vs AFTER.** BEFORE = 088cf00 (parent of the #105
   branch, i.e. post-#104). AFTER = 03dd6f8 (current v2 HEAD). For each
   effect: is the code path still REACHED? Prime suspects: (a) dublin
   draw went sprites-only — viscomm draws that lived on the old vector
   path may no longer render; (b) view.odin rewrite — path-walk/ladder
   changes may skip overlay layers; (c) L3 reduced-motion "pins the
   breath" — check whether the pin gates MORE than the breath (a
   too-broad pin = lerps/flashes dead); (d) flag lattice defaults — an
   effect silently gated off by default is LOST-BY-FLAG.
3. **Mechanical proof.** The repo has pixel/capture gates — build and
   capture at BOTH commits (byte/hash/capture-diff is ground truth;
   look_l*_test show the harness idioms). Where a behavior needs motion,
   use multi-frame captures or the harness's animation stepping.
   KYLE-class vision (your model is natively multimodal) may CORROBORATE
   a visual difference — screening only; pixel measurements decide.
   Vision craft: prompts to files, absolute out paths, read findings from
   disk.
4. **KEEP/LEAVE decision menu (the deliverable's final section).** Per
e   effect: added-by PR → status (INTACT / DEGRADED / LOST / FLAG-GATED)
   → evidence (test, capture-diff numbers, code path trace) → if lost:
   the exact commit + hunk that severed it + the minimal restore hook
   (describe, do NOT implement) → **a KEEP / LEAVE recommendation line
   with one-line rationale**. The user will rule keep-vs-leave per row off
   this menu; rank restore candidates if several are lost.

   USER PREFERENCE (explicit, on record 2026-08-27): the user LIKED
   "links pulsating when congesting" — the link congestion pulse.
   Audit it as a first-class effect row: its BEFORE (088cf00) behavior
   (pulse cadence, hue, trigger threshold) vs AFTER (03dd6f8) state.
   If lost or degraded, it is restore-candidate #1 unless evidence says
   otherwise.

## Constraints

- READ-ONLY on the repo: no commits, no pushes, no file edits inside
  packet-plumber working code. Captures/reports go to
  `_bmad-output/implementation-artifacts/packet-plumber-v2-viscomm-regression-audit/`.
- Do NOT touch the mechanics-quinn design session or its surface —
  different lane, in flight.
- bash on this machine is 3.2 — no arrays in any sweep/wave script.
- Perkins/fix rounds are OUT of scope; an appendix "restore options"
  (ranked, with risk) ends the report. No fix implementation.
- This is a NO-PR job: on finish run
  `herdr notification show "packet-plumber-v2-viscomm-regression-audit" --body "<one-line summary + report path>"`
  (verify shown:true in the result), then `bin/ledger set <id> done` is
  SILAS' — do NOT write ledger transitions; report to Gru instead.
- Lavish: the report is a DOCS deliverable — render the findings table +
  before/after captures to a lavish HTML artifact for the user's review
  (loopback-serve if assets 403 — see lavish skill; _local-refs doctrine
  if user-dropped assets appear).

## Skills policy

- Primary: `gds-investigate` (forensic, evidence-graded findings).
- Report render: `lavish`.

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max (vision INLINE —
  native multimodal; no KYLE spawn needed).
- No mega-minion dispatch expected; if one is needed, name the model
  explicitly in the spawn.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-viscomm-regression-audit
- base: v2 (audit range 088cf00..03dd6f8; HEAD = 03dd6f8)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: none — READ-ONLY, no PR
- worktree: Silas' call — default main checkout (read-only =
  parallel-safe vs in-flight jobs; the evidence-job doctrine); if the
  main checkout is held by a sibling, a detached worktree at 03dd6f8.
- notification: `herdr notification show` on finish (shown:true verified)
