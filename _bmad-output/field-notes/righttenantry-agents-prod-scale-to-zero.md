# field-notes: righttenantry-agents-prod-scale-to-zero

- 2026-09-04: `ledger set <id> in-review` is REFUSED until the PR URL is on the row (`!! in-review requires a PR URL`) — the natural order is backwards: run `ledger pr <id> <url>` BEFORE `set in-review` (error is loud, no harm, but it's a guaranteed re-run otherwise).
- 2026-09-04: RT `.github/workflows/deploy-to-prod.yml` path filter EXCLUDES `deployment/terraform/**` and NO CI runs terraform (prod workflow = `gcloud run deploy --source .`, inherits Terraform-managed flags) — tfvars PRs are merge-inert; "merge ≠ prod change" is a workflow-read fact, state it in the PR body every time.
- 2026-09-04: RT pre-commit hooks build a `.venv` via uv (149 packages, ~1 min) even on a tfvars-only commit in a fresh worktree — slow first commit is the hook bootstrap, not a hang.
- 2026-09-04: RT pins terraform values in tests/unit/test_concurrency.py — grep that file BEFORE flipping any prod tfvars value (a value flip without the pin flip = red suite on the NEXT unrelated PR, since pr-checks skips deployment/ paths; it detonated on the #177 promote).
- 2026-09-04: comment-mentions of `attr = value` in tfvars false-match unanchored `re.search` extractors (comment precedes assignment in file order) — anchor value-parsing regexes to line starts (re.MULTILINE) and prove with a negative control (revert the value → suite must FAIL).
