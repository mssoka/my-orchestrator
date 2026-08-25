# Briefing — silas-perkins-r1-completion (COO ops: finish + post Perkins r1)

You are SILAS (COO — deterministic ops). Gru stays with the user; you own this
round end-to-end. Model note: this dispatch runs on the DSH session default;
any mega-minion you spawn must pin its model explicitly in the spawn prompt and
you record it in your final ledger note.

## Target

- PR: https://github.com/solarity-services/Packet-Plumber/pull/99 (base v2)
- Reviewed sha: 4b3a8874f2c97ba70cb74f36545708082f5e6115 (CI 4/4 green)
- Round dir (out_dir): /Users/moses/code/dsh-orchestrator-setup/_bmad-output/perkins/packet-plumber-v2-viscomm-tie-deconflict/r1/
- Round worktree (read-only for you; NEVER commit/push from it; leave it CLEAN):
  /Users/moses/code/packet-plumber-wt-viscomm-tie
- Skill (the authority — read it first): /Users/moses/.agents/skills/code-review/SKILL.md
  (tracked copy: /Users/moses/code/dsh-orchestrator-setup/skills/code-review/SKILL.md)
- Spec (acceptance lens's spec): /Users/moses/code/dsh-orchestrator-setup/_briefs/packet-plumber-v2-viscomm-tie-deconflict.md
- Ledger CLI: /Users/moses/code/dsh-orchestrator-setup/bin/ledger
- Round row: packet-plumber-v2-viscomm-tie-deconflict-perkins-r1
- Job row: packet-plumber-v2-viscomm-tie-deconflict

## State (verified by Gru)

The skill-run lens wave already ran. Files in out_dir:
- blind.json (3287B), edge.json (1882B), acceptance.json (2174B),
  architecture.json (1160B), tests.json (4189B) — PRESENT, parse-check them.
- security.json (3B) — parse-check; "[]\n" is a VALID empty array.
- codebase.json — MISSING. (The orchestrator's wave validation wrongly checked
  agent return values, not the files; the file contract is what counts.)

## Task (in order)

1. Validate every <lens>.json in out_dir parses as a JSON array; record counts.
2. Re-dispatch the MISSING codebase lens ONCE as a mega-minion (your subagent
   tool), VERBATIM per the skill: shared prompt block + Reviewer 6 (Codebase
   Fit) brief + the skill's JSON schema + accuracy mandate + file-output
   contract (write ONLY its array to out_dir/codebase.json). Root it in the
   round worktree. If it fails once, retry once more; then mark codebase in
   failed_layers and proceed degraded (do NOT approve-only on a degraded wave
   with zero findings — the skill's degraded guard).
3. Execute Step 3 EXACTLY as the skill's "Step 3: Validate and Consolidate
   Findings" (3a/3b/3c): verify EVERY finding against the round worktree
   (confirmed / rejected / unverifiable-speculative; rejected = discarded,
   never softened). You may do this yourself or spawn one fresh verifier
   mega-minion — your call, but the verification must be independent of the
   lens contexts. Tests-lens mutation probes are allowed IN THE WORKTREE only
   if you/it revert every mutation (git checkout -- <file>) and git status
   ends CLEAN.
4. Write out_dir/consolidated.json per the skill (surviving findings with
   verification status + merged source arrays, failed_layers, counts, verdict).
5. Compose the review body: the skill's Step-4 report format, prefixed with a
   header: "## Perkins automated review - round 1 / Job: packet-plumber-v2-viscomm-tie-deconflict / Reviewed sha: 4b3a887 / Reviewers: <x>/7 completed / Verification: <confirmed>/<total> confirmed, <rejected> discarded".
   Save it to out_dir/verdict.md.
6. Post as the perkins-review app:
   - TOKEN=$(/Users/moses/code/dsh-orchestrator-setup/bin/perkins-token --owner solarity-services)
     — capture STDOUT ONLY, NEVER append 2>&1.
   - If TOKEN is EMPTY (check the string, not $?): fall back to
     `gh pr comment 99 --body-file out_dir/verdict.md` and ledger-note
     "fallback-comment" on the round row.
   - Else map verdict to event: 0 blockers -> GH_TOKEN=$TOKEN gh pr review 99
     --approve --body-file ...; 1-3 blockers -> --request-changes; 4+ ->
     --request-changes with the body leading "MAJOR REWORK".
     Run gh from /Users/moses/code/packet-plumber.
7. Ledger: bin/ledger set <round-row> done "verdict <VERDICT> posted
   (<event>)"; bin/ledger note <round-row> with counts + failed_layers +
   posting method + any mega-minion models used. bin/ledger note <job-row>
   "perkins r1 verdict posted; fixes pending relay". Do NOT set the job row
   done (human merge closes it).
8. Final message back to Gru: verdict, blocker/warning/note counts, the
   blocker titles verbatim, failed_layers, posting method, worktree clean
   confirmation.

## Hard rules

- Never modify the PR, never push, never merge. Review only.
- The worktree ends `git status --porcelain` EMPTY.
- The skill file is the authority; where this brief and the skill disagree,
  the skill wins — note the disagreement in your final message.
