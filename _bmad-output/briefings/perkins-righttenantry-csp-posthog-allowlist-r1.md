# Perkins briefing — round 1: righttenantry-csp-posthog-allowlist

- **PR:** https://github.com/solarity-services/RightTenantry/pull/585 (targets `develop`)
- **Reviewed sha:** `b37c2d741b44dfe62dd388f01e3f71ff323c34f2` (head `csp-posthog-allowlist`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-csp-posthog-allowlist-r1` — pinned at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec (what you review against):** the original job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-csp-posthog-allowlist.md` **AS AMENDED by the user's ruling below**. There is NO GitHub issue for this job.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## ⚠️ CRITICAL CONTEXT — this is a user-ruled NO-OP (read before any lens)

The original job briefing's *mission* was "add `https://eu.posthog.com` to CSP `script-src` + `connect-src`." **That mission was DISPROVEN and OVERRIDDEN.** The implementing minion verified against disk + PostHog's own docs that:

- PostHog events + the array script are **same-origin proxied** (`api_host: "/_ph"`, assets `/_ph_assets/static/array.js`) — both already covered by CSP `'self'`; the proxy is deliberate (evades ad blockers, per `form_view.gleam:220`).
- `ui_host: "https://eu.posthog.com"` is **links/navigation only**, NOT a `script-src`/`connect-src` fetch (PostHog `PostHogConfig` reference).
- So under normal traffic the browser makes **no direct fetch to eu.posthog.com**.

The **user ruled Q3 = no-op**: the `CSP_ENFORCE=true` flip is already safe; `eu.posthog.com` needs NO allowlist. The PR's entire purpose is a **documenting code comment** explaining why `eu.posthog.com` is intentionally absent, so the question isn't re-litigated.

**Therefore the correct, desired state of this PR is:**
- `server/src/csp.gleam` gains comment lines documenting the rationale.
- **ZERO changes to any CSP directive value** (`script-src`, `connect-src`, `img-src`, `style-src`, `frame-src` must be byte-identical to `develop`).
- The nonce-based inline-script mechanism is **untouched**.

### Lens-guard (do NOT generate false findings)

- **Do NOT flag "eu.posthog.com is missing from connect-src/script-src" as a defect.** Its absence is the *whole point* and is user-ruled. A lens that "discovers" PostHog needs allowlisting is re-litigating a question the user already closed — that is a FALSE POSITIVE, not a finding.
- **The acceptance criterion is the no-op:** verify the diff is comment-only and that no directive value or nonce logic changed. The review's job is to *confirm* the no-op is truly a no-op (nothing functional touched), NOT to re-derive whether eu.posthog.com should be allowlisted.
- Verify the comment's technical claims are accurate (the proxy paths, the ui_host-is-links-only claim) — an *inaccurate* documenting comment IS a legitimate finding.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 585 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd, `spec_files` = this briefing (which carries the user's no-op ruling as the spec; there is no GitHub issue — skip the `gh issue view` dump), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r1`, and `prior_findings` = none (round 1). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`
  2. If that failed (non-zero exit): fall back to `gh pr comment 585 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 585 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** righttenantry-csp-posthog-allowlist · **Reviewed sha:** b37c2d7 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _No-op doc-comment PR (user-ruled Q3): the reviewed change is comment-only by design; eu.posthog.com is intentionally absent._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `b37c2d7`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-csp-posthog-allowlist-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
