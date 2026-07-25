# Briefing: righttenantry-uk-expansion-domain-research

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd, branch `uk-expansion-domain-research`
- **Base:** `develop`
- **GitHub issue:** #534 — reference with `Refs #534`, do NOT close
- **Type:** evidence-gathering research. Deliverable is a cited markdown
  research report committed on the branch. **Do NOT open a PR** (explicit
  standing-orders override — a later collation job merges your report with a
  sibling's and opens the single PR).

## Mission

Run the **bmad-domain-research** skill as your operating workflow to gather
the cited evidence for issue #534: *"Explore UK expansion: Rightmove
applicant intake + GTM route"*.

Follow the skill's activation exactly (resolve customization via
`_bmad/scripts/resolve_customization.py`, load `_bmad/bmm/config.yaml`, honor
`planning_artifacts` for output location, create the output file from the
skill's `research.template.md` per its naming convention).

**⛔ Web-search risk (field note from job 535, 2026-07-21):** the web-search
quota was exhausted during that job, with a reset noted as 2026-08-06. Test
search with a trivial query FIRST. If search is unavailable, halt as
`blocked` immediately (ledger + notification) — do not write an uncited
report from memory. Also: the search tool may default to region=cn —
explicitly steer queries to UK/Irish sources (`site:gov.uk`,
`site:rightmove.co.uk`, etc.) and say in the report if you couldn't.

**Topic discovery is pre-answered** (skill's interactive clarify overridden;
internal checkpoints pre-approved — proceed without halting):

- **Topic:** UK rental-portal applicant-intake landscape and compliance
  deltas for RightTenantry (Irish tenant-screening product) expanding to the
  UK. Deep on the five threads below; broad UK market sizing is out of scope.
- **Goals:** give Moses verified, cited evidence to pick GTM route A
  (manual landlord forwarding), route B (agents-first), or stay
  Ireland-only.

## The five evidence threads (from issue #534)

1. **Rightmove listing rules:** can private landlords list directly, or is
   it letting-agents-only? Verify against Rightmove's actual terms AND
   against intermediaries that syndicate to Rightmove (e.g. OpenRent) —
   what do they cost, how does syndication work, who owns applicant
   communications in that arrangement?
2. **Rightmove enquiry mechanics:** what exactly does a landlord/agent get
   when an applicant enquires (email notification? in-portal inbox? API?
   webhook?) — i.e. is there ANY automatable hook an intake flow could
   attach to, even unofficially (email parsing)?
3. **GTM route A funnel evidence:** benchmarks/data on email-forwarding
   funnel drop-off (enquiry → form-sent → form-completed) vs. automated
   intake. Hard data preferred; clearly label estimates.
4. **Other UK portals:** do Zoopla, OpenRent, or SpareRoom offer email/API/
   webhook hooks closer to the DAFT.ie automated flow? Per-portal verdict
   table.
5. **Compliance deltas:** UK tenant-referencing norms, Right to Rent
   checks (landlord/agent legal duty — who must do what), UK GDPR / ICO
   vs. Ireland's DPC, any consent/recording differences relevant to
   screening automation.

Prioritize primary sources (Rightmove/Zoopla/OpenRent/SpareRoom official
docs & terms, gov.uk, ICO). Every load-bearing claim gets a citation; flag
anything you could not verify.

## Structure

You may fan out mega-minions (one per thread works well;
`herdr pane split --current --direction right|down --no-focus`, launch `pi`,
hand over a thread brief). **Max 10 concurrent**, close every pane you
create before finishing. Synthesize the single report yourself.

## Standing orders (orchestration overrides)

- Playbook "Minion standing orders" applies except where overridden here:
  - **Skills policy:** your workflow skill = **bmad-domain-research**.
    Mega-minions run research threads (no bmad skill needed); any review
    pass uses **bmad-review-adversarial-general** /
    **bmad-review-edge-case-hunter**.
  - Clarify pre-answered above; internal skill checkpoints pre-approved.
    Only halt for genuine blockers (e.g. web search dead).
  - **No PR.** Commit on `uk-expansion-domain-research`,
    `git push -u origin uk-expansion-domain-research`. Never merge anything.
- Env files symlinked from the main checkout are **read-only**; never
  commit secrets.
- Self-report every transition:
  `/Users/moses/code/bin/ledger set righttenantry-uk-expansion-domain-research <status> "<note>"`
  (`working` at start; `in-review` when the report is pushed = deliverable
  ready for collation).
- On blocked/finished:
  `herdr notification show "righttenantry-uk-expansion-domain-research" --body "<one-line>"`

## Close-out

Final message: summary, report file path, per-thread headline findings
(one line each), anything flagged unverifiable.
