# Briefing (follow-up task, same job): righttenantry-ai-reference-calls-research — interactive HTML documentation

- **Repo/worktree/branch/base:** unchanged — this pane's cwd, branch `ai-reference-calls-research`, PR #540 targets `develop`.
- **Original briefing:** `/Users/moses/code/_bmad-output/briefings/righttenantry-ai-reference-calls-research.md` (context; its standing orders apply in full).
- **Type:** docs artifact. Deliverable is one self-contained interactive HTML page consolidating the research, added to the existing PR.

## Mission

Moses is reading the report and finds the markdown hard to parse. Build a
**single, self-contained, highly interactive HTML documentation page** that
consolidates ALL of the following sources (no substance loss):

1. Synthesis report (750 lines):
   `_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md`
2. Mega-minion thread reports (the heist-535 crew outputs, ~1,700 lines total):
   - `_bmad-output/planning-artifacts/research/heist-535/legal.md`
   - `_bmad-output/planning-artifacts/research/heist-535/providers.md`
   - `_bmad-output/planning-artifacts/research/heist-535/architecture.md`
   - `_bmad-output/planning-artifacts/research/heist-535/fraud.md`
   - `_bmad-output/planning-artifacts/research/heist-535/fallback.md`

## Pre-answered decisions (do NOT halt to clarify these)

- **One single `.html` file**, all CSS/JS inlined — no external CDNs, fonts, or
  assets. Must work opened from disk with no network. Vanilla JS, no build step.
- **Location:** same directory as the synthesis report
  (`_bmad-output/planning-artifacts/research/`), named
  `domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.html`.
- **Same branch, same PR** — commit on `ai-reference-calls-research` and push;
  PR #540 updates automatically. Do not open a new PR. **Never merge.**
- Markdown sources stay untouched — the HTML is an additional reading surface.

## Required interactivity (the point of the exercise)

- Fixed sidebar TOC with scroll-spy highlighting the active section; collapses
  per top-level section (synthesis + one per thread report).
- Collapsible `<details>`-style subsections so long threads are skimmable.
- Client-side full-text search box that filters/highlights matching sections.
- Anchor deep-links on every heading (hover link icon).
- Sticky header with the report title, dark/light toggle, back-to-top button.
- Citations rendered as a linked references section; in-text citation markers
  jump to their reference entry.
- A "Recommendation" callout near the top (resume/shelve verdict, provider
  pick) — the reader's most-wanted answer first.
- Print stylesheet (clean fallback when printed/PDF'd).

## Content fidelity (acceptance)

- Every finding, citation, table, and the final recommendation from all six
  source files must appear in the HTML. Reorganize for navigation, but drop
  nothing; do not editorialize or "improve" the research content.
- Verify before committing: programmatically confirm every source file is
  incorporated (e.g. checklist of section headings per source) and that the
  HTML has zero external asset references. State the verification in your
  final message.

## Standing orders & skills policy

- Playbook "Minion standing orders" applies in full (ledger self-report with
  job id `righttenantry-ai-reference-calls-research`, notification on finish,
  env files read-only, never merge).
- **Skills policy:** workflow skill = **bmad-quick-dev**. Internal approval
  checkpoints are pre-approved — proceed without halting; only halt for
  genuine blockers. Mega-minions are not expected for this task; if you do
  spawn a review pass, use **bmad-review-adversarial-general** /
  **bmad-review-edge-case-hunter** and badge out every pane you create.
- Final message: summary, files changed, PR URL (still #540), and the
  verification evidence (sources incorporated, zero external assets).
