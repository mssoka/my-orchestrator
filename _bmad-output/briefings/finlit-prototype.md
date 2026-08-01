# Briefing: finlit-prototype

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: `git@github.com:solarity-services/finlit.git`)
- **Worktree:** this pane's cwd (`prototype` worktree, branch `prototype`, base `origin/main`)
- **Skills policy:** workflow = **gds-agent-game-solo-dev** (Indie Quick Flow — you wrote this spec; follow it exactly. Orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay, lavish session when practical; internal checkpoints pre-approved). Review pass: **gds-code-review** or **bmad-review-edge-case-hunter** before the PR, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Build the **playable Quick Flow prototype** per your ready-for-dev spec:

`_bmad-output/implementation-artifacts/spec-quick-prototype-finlit-street.md` (PRIMARY — follow it exactly)

Canon context (read as needed): `_bmad-output/planning-artifacts/briefs/brief-FinLit-2026-07-31/brief.md` + `addendum.md` (merged game brief; OQ3 ruled: tutor is child-initiated "?" button), and the brainstorm memlog for anything the spec defers.

## Environment (verified)

- **Godot 4.7.1.stable** installed 2026-07-31: `godot` on PATH (`/opt/homebrew/bin/godot`). Use headless for verification: project must import + run clean via `godot --headless --path <project-dir> --quit-after <n>`.
- Stack A per the spec (Godot 4.7 + thin local pieces). No backend, no accounts, no LLM — the `tutor.gd` scripted stand-in seam exactly as specced.

## Scope discipline

- Prototype slice ONLY, per the spec — the minute-one loop, street, core interactions as specced. No scope creep into backend, market, seasons logic beyond the spec's seams.
- Follow the spec's project layout (directory, scene structure). If the spec is genuinely ambiguous on a layout point, decide + record; if it's a requirement contradiction, HALT with numbered questions.
- This is a CODE job: regular PR pattern (no lavish pre-PR); lavish only for clarify questions if you have them.

## Acceptance

- Everything the spec's verify steps require passes; project imports + runs headless clean (zero script errors); the spec's "ready" checklist is ticked with evidence in your final message.
- Commit on `prototype`, `git push -u origin prototype`, `gh pr create --base main` titled "feat: quick-flow prototype slice (spec-quick-prototype-finlit-street)" with a **Decisions & rationale** section + how-to-run notes for Moses. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` present incl. gds module; no env files in this repo). Godot import artifacts (`.godot/`) must NOT be committed — add to `.gitignore` if the spec/repo doesn't already.

## Verify

Headless import + run clean; `git status` shows no `.godot/` or export artifacts staged; `git diff --stat` confined to the prototype layout + any `.gitignore` touch.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-prototype working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-prototype in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-prototype <url>`
- On blocked/finished: `herdr notification show "finlit-prototype" --body "<one-line>"`
- Final message: summary, files changed, PR URL, how-to-run, verify evidence, open questions.

## Amendment 2026-07-31 (relayed in-pane, delivered)

Integrate a REAL LLM call behind the spec's tutor.gd seam — evaluation rig
for integrate-vs-drop. DeepSeek direct (OpenAI-compatible):
POST https://api.deepseek.com/chat/completions, model deepseek-v4-flash,
Bearer $DEEPSEEK_API_KEY from env (never committed; .env gitignored +
symlinked by Gru). SUPERSEDES the OpenRouter note in ruled OQ3 (same
cheapest-tier intent, vendor named). Ruled design stands: child-initiated
"?" button only, no free-form chat; locked Mrs. K persona; pseudonymous
payload (player state + child's options, zero PII); age-bracketed depth.
Guardrails: scope-locked system prompt, ~80-word cap, timeout + scripted
fallback on any error, local parent-reviewable jsonl call log. Scripted
stand-in stays default/offline; LLM path activates only when the key is
present; debug toggle scripted-vs-LLM for the same trigger.
