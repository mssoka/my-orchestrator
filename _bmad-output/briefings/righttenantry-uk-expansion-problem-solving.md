# Briefing: righttenantry-uk-expansion-problem-solving

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd, branch `uk-expansion-problem-solving`
- **Base:** `develop`
- **GitHub issue:** #534 — reference with `Refs #534`, do NOT close
- **Type:** structured decision analysis. Deliverable is a markdown analysis
  document committed on the branch. **Do NOT open a PR** (explicit
  standing-orders override — a later collation job merges your analysis
  with a sibling's evidence report and opens the single PR).

## Mission

Run the **bmad-cis-problem-solving** skill as your operating workflow on the
decision at the heart of issue #534: *"Explore UK expansion: Rightmove
applicant intake + GTM route."*

**The challenge (pre-answered — do NOT halt to clarify; internal skill
checkpoints pre-approved):**

RightTenantry isn't getting enough customers in Ireland (small market). UK
launch was shelved because the Irish intake moat — DAFT.ie automatically
sending the RightTenantry application form to every enquirer — has no
Rightmove equivalent. **Decision needed: route A (private landlords
manually forward the form to each enquirer), route B (sell to letting
agents who already own applicant comms), or stay Ireland-only until an
automated UK intake hook exists.**

**A sibling minion is running bmad-domain-research in parallel** to gather
the cited evidence (Rightmove rules, portal hooks, compliance deltas, funnel
data). Do NOT duplicate deep web research — reason from the issue text,
domain reasoning, and clearly-labelled general knowledge. **State every
assumption explicitly** (numbered list) so the collation pass can test each
one against the evidence report. Where your analysis hinges on an unknown,
name it as such rather than resolving it by fiat.

## What the analysis must produce

1. **Problem reframing:** is the real problem "no automated intake hook",
   "UK funnel economics", or "single-market concentration"? At least two
   distinct reframes, with implications of each.
2. **Option generation beyond the menu:** routes A and B as given, PLUS at
   least two options the issue didn't list — e.g. re-automating around
   Rightmove (parsing enquiry-notification emails into auto-replies),
   OpenRent-as-channel, portals-with-hooks-first (Zoopla/SpareRoom),
   or staying Ireland-only but expanding the funnel (other Irish channels).
   Treat these as starting seeds, not constraints.
3. **Structured evaluation:** criteria matrix (funnel viability, CAC,
   time-to-first-customer, engineering cost, compliance burden,
   strategic positioning) with scores AND the reasoning behind each score.
4. **Pre-mortem on the leading option:** how it fails, early-warning
   signals, mitigations.
5. **Recommendation logic:** a decision rule ("if evidence shows X about
   Rightmove hooks, then route Y") rather than an unconditional pick —
   the evidence lands in the sibling report.
6. **Explicit assumption ledger** (numbered) for the collation pass.

## Standing orders (orchestration overrides)

- Playbook "Minion standing orders" applies except where overridden here:
  - **Skills policy:** your workflow skill = **bmad-cis-problem-solving**.
    Mega-minions (if you spawn any, max 10, badge out all) for a review
    pass use **bmad-review-adversarial-general** /
    **bmad-review-edge-case-hunter**.
  - **No PR.** Commit on `uk-expansion-problem-solving`,
    `git push -u origin uk-expansion-problem-solving`. Never merge anything.
- Env files symlinked from the main checkout are **read-only**; never
  commit secrets.
- Output path: `_bmad-output/planning-artifacts/research/problem-solving-uk-expansion-534-2026-07-23.md`
- Self-report every transition:
  `/Users/moses/code/bin/ledger set righttenantry-uk-expansion-problem-solving <status> "<note>"`
  (`working` at start; `in-review` when the analysis is pushed = deliverable
  ready for collation).
- On blocked/finished:
  `herdr notification show "righttenantry-uk-expansion-problem-solving" --body "<one-line>"`

## Close-out

Final message: summary, file path, the reframes in one line each, your
leading option + decision rule, assumption count.
