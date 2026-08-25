# righttenantry-demo-pdf-watermark

## Task

Every PDF generated in RT demo mode carries a visible DEMO watermark.
User ruling (2026-08-24): "the PDF files in DEMO should have
watermarks saying demo." Nothing produced in demo mode may be
mistaken for a real document.

## Rules (hard)

1. **Reuse the canonical demo check** landed by
   righttenantry-demo-bulk-invite-guard (that job is pinning the
   detector NOW — do NOT invent a second one; if it is not merged yet,
   base on its merged head).
2. **Watermark every PDF generation path** in demo mode — survey ALL
   PDF producers (leases/tenancy agreements, invoices, statements,
   reports, exports — grep the codebase; the PR body lists every path
   found + every path watermarked, or explicitly why excluded).
3. **The watermark**: diagonal "DEMO", semi-transparent, on EVERY page
   (standard document watermark — unobtrusive to read through,
   unmistakable at a glance). Real-mode PDFs byte-identical (no
   watermark path executes).
4. If the codebase has a central PDF renderer, watermark THERE (one
   seam); only go per-producer if producers bypass the central one —
   document the choice.

## Acceptance

- Demo: every PDF path produces a watermarked PDF (per-page DEMO
  diagonal); real mode: byte-identical to current.
- Tests: demo mode watermark present on at least two distinct PDF
  paths; real mode unchanged.
- PR body: the producer survey + the seam chosen + sample watermark
  render.
- pr_review: 1.

## HOLD / release (dispatch mechanics)

- HELD, PANELESS, behind righttenantry-demo-bulk-invite-guard's merge
  (it owns the canonical demo detector). Release = its merge close-out
  -> resolve fresh develop head, THEN dispatch.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-demo-pdf-watermark
- base: develop (fresh head at release)
- model: deepseek-v4-flash
- worktree: yes (at release)
- pr_review: 1
- blocked_by: righttenantry-demo-bulk-invite-guard (release = its
  merge close-out)
