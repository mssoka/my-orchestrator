# Briefing: righttenantry-refcheck-autoloop

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (PR targets develop). Develop is current.
- **Workflow:** **bmad-dev-auto** — the unattended development loop. Read the skill at `/Users/moses/.agents/skills/bmad-dev-auto/SKILL.md` (or the installed location) + follow it. Auto-pick the next story from the sprint tracker, implement, verify, PR, loop. Perkins: **ON per story** (each PR gets r1).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; r1 per story PR).

## Mission

Run the **bmad-dev-auto unattended loop** on the RT Reference-Checking v1 sprint (issue #548). The sprint paused at **rc2-2** (3/18 done: rc1-1, rc1-2, rc2-1). Auto-execute the next stories in sequence, one PR each, until you hit a genuine blocker.

## The loop

1. **Read the sprint tracker:** `_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml` — the authoritative story list + status. The next story is **rc2-2** (viewed application status end-to-end), then rc2-3.
2. **Per story (one iteration):** auto-pick the next non-done story → create the story spec (bmad-create-story) if the file doesn't exist → implement (bmad-dev-story) → verify (tests) → open PR targeting develop → update the tracker (story → done/review). Then loop to the next story.
3. **HALT conditions** (stop the loop + self-report):
   - You reach **rc3-1** (`sms-client-twilio-lookup-infrastructure-slice`) — it's **externally gated on Twilio account + IE number provisioning** (billing owner: Moses; code no-ops without keys). Do NOT attempt rc3-1; halt before it (after rc2-3) + flag the gate.
   - A genuine clarifying question (numbered, HALT for Gru relay).
   - A dependency you can't resolve (e.g., rc2-3 needs rc2-2 merged first — if so, note it + halt for the merge).

So the expected run: **rc2-2 → rc2-3 → HALT at rc3-1 (Twilio gate).** Two stories, two PRs, then blocked by the external dependency.

## Source material (read — the spec)

1. **`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`** — the tracker (story list, status, sequencing notes, external gates). THE source of truth for what's next.
2. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — the story acceptance criteria (rc2-2: viewed status end-to-end; rc2-3: trigger-on-viewed start/skip APIs).
3. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — the data contract (AD-13 → rc2-2/rc2-3).
4. **Prior refcheck stories for PATTERNS** (rc1-1 #557, rc1-2 #562, rc2-1 #558 — migration + codec + UI conventions to match).

## Constraints (RT-specific)
- **No em-dashes in user-facing copy** (RT global ban, CI-guarded).
- Follow the established application_status conventions (Submitted/Reviewing/Shortlisted/Approved/Reject; `viewed` slots after Shortlisted).
- One PR per story (don't batch rc2-2 + rc2-3 into one PR — separate, for review).
- rc2-3 builds on rc2-2 — if rc2-2's PR must merge before rc2-3 can start cleanly, note it + halt for the merge (don't stack unsafely).

## Self-report (per story + on halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-2 working` at start (rc2-2); create + transition rc2-3 rows as you reach them
- Per story: `ledger set <story-slug> in-review "PR <url>"` when each PR opens
- On HALT (rc3-1 gate or blocker): `herdr notification show "refcheck-autoloop" --body "<one-line>"` + final message: which stories shipped (PR URLs), where you halted + why (the Twilio gate), what's next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-autoloop · base: develop
