# Perkins briefing — round 1: packet-plumber-v2-ux-font-resize

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/52 (targets `v2`)
- **Reviewed sha:** `91f7730a6c589836573dbd589d7b658f34607436` (short `91f7730`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-ux-font-resize-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-ux-font-resize.md` + the USER REPORT (font illegible + window un-resizable; the prototype `/Users/moses/code/packet-plumber-prototype-ref` is the reference). No GitHub issue.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Local verification at the sha remains ground truth.

## What the PR does (review scope)

**USER-REPORT fix — two UX defects, ONE PR:**
- **Part 1 — the font:** v2 rendered the raylib DEFAULT font (illegible on the light
  canvas). Replaced with a readable bitmap font (bundled asset, license-documented —
  strong x-height, open counters), loaded via the codebase's font path (app-layer
  init; NO system font loading — ODN-1). Size + contrast audit: HUD/legend/stat text
  minimums raised (nothing below ~14px effective at 1280×720; the footer SLA rows +
  strain legend were the offenders).
- **Part 2 — window resize:** `FLAG_WINDOW_RESIZABLE` at init (prototype pattern);
  layout via the existing scale path (render target fit / letterbox, no distortion);
  HUD readable + non-overlapping at default AND the min-clamp; pause edge-chip
  (5.3-ux), QoS panel, and weather report survive resize; WIN_W/WIN_H threading
  centralized.
- **Presentation-only invariant (load-bearing):** resize never touches the sim,
  serialization, or replay — NO LOG_VERSION change; the harness runs fixed-size
  regardless; T1/T2 goldens captured at canonical 1280×720 do not shift due to
  resize CODE. The ONLY golden movement allowed is the deliberate T2 font fold
  (glyph-carrying T2s re-blessed + LISTED in the PR body — the 5.3-ux pattern).
  T1 (sim-level) goldens MUST NOT shift — a T1 move = a determinism break.
- Verification (minion-claimed): full local suite green; before/after screenshots
  (font close-ups; resize at 1280×720 / ~1600×900 / min-clamp / non-16:9).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — T1 immutability.** Sim-level T1 goldens MUST be byte-identical
  (font + resize are presentation-only). If ANY T1 hash moved, that is a
  determinism break — a blocker (STOP-worthy). Verify by diffing the golden
  inventory against the merge-base.
- **🚨 The T2 fold must be DELIBERATE + TEXT-ONLY.** Every re-blessed T2 must be
  listed in the PR body, and the fold must be glyph rendering only (font swap) —
  NO semantic drift hidden in a re-bless (no gameplay/state change riding the
  golden update). The resize code itself must not shift ANY golden (harness is
  fixed-size).
- **Font asset determinism:** the new font is a bundled asset (app-layer init) —
  the harness must still render deterministically with it; no system-font loading,
  no file reads at sim level (ODN-1).
- **Resize presentation-only:** no sim/serialization/replay changes, no
  LOG_VERSION bump; the min-clamp prevents HUD collapse; no distortion (letterbox
  if aspect drifts); the pause edge-chip, QoS panel, and weather report survive at
  default AND min-clamp.
- **Readability canon:** HUD/legend/stat text readable on the light canvas (size +
  contrast — the a11y canon, 7.3 adjacency). A "readable font but tiny unreadable
  text" outcome = a finding.
- **Base = `v2`** — includes the full shipped line (5.5/5.6/5.3/5.7/5.3-ux/5.8/5.1).
  5.2 (node-health) is in flight and touches `app/render/view.odin` (health rings)
  — it may merge mid-round; carry-forward only, do NOT re-open settled findings.
- **Scope guard:** font + window ONLY — no new HUD surfaces, no visibility/gauge
  work (queued separately), no 5.2 health-ring changes, no input-parity work.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-ux-font-resize/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-ux-font-resize/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-ux-font-resize-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
