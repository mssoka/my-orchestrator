# Mayor (pi orchestrator) — fresh-machine setup guide

Replicates the orchestrator setup: one pi **mayor** session at a root
directory that holds all repos, enforcing dispatch-only behavior via a
project-local pi extension, with Herdr worktrees for sub-agents and
bmad-quick-dev for execution.

Target state you are building:

```
<root>/                              # e.g. ~/code — contains all repos
├── .pi/extensions/mayor.ts          # the hook (enforcement)
├── .agents/skills/bmad-*            # BMAD skills (from fresh install, step 3)
├── _bmad/                           # BMAD project config (from fresh install)
├── AGENTS.md / CLAUDE.md            # slim pointers only
├── docs/orchestration-playbook.md   # operating procedure
├── _bmad-output/                    # created by the BMAD installer (step 3)
│   ├── orchestrator-jobs.yaml       # durable job ledger (orchestrator-owned)
│   └── briefings/_template.md       # briefing template (orchestrator-owned)
└── <repo1>/ <repo2>/ ...            # repos, each with .git and its own _bmad/
```

## 1. Prerequisites

- Node 22+ and pi: `npm i -g @earendil-works/pi-coding-agent` (setup used pi 0.80.x)
- Herdr ≥ 0.7.4 (terminal multiplexer for agents; see its own docs/repo)
- `git`, plus `gh` and/or `glab` for PR/MR creation by sub-agents
- LLM provider credentials configured for pi

## 2. Clone the orchestrator meta repo

The root is itself a git repo with a whitelist `.gitignore` — it tracks
only the orchestrator system files. Cloning is the entire "copy" step:

```bash
git clone git@github.com:mssoka/my-orchestrator.git <root>
```

Tracked: `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `docs/`,
`_bmad-output/` (ledger + briefing template), `.pi/extensions/`.

Not tracked, by design:

- `_bmad/`, `.agents/skills/` → fresh BMAD install (step 3)
- The project repos themselves → clone each separately into `<root>`
- `.env` files → never in git; recreate them in each repo on the new
  machine. The dispatch bootstrap symlinks env files from repo roots, so
  jobs that need env cannot run until they exist.

Before first use, open `_bmad-output/orchestrator-jobs.yaml` and confirm
`jobs: []` (the ledger travels with the repo; reset it if it carried
state over).

## 3. Install BMAD fresh

BMAD is installer-managed and installed **per project** — nothing is
symlinked between repos. The reference machine has a real `_bmad/` in the
root and in every repo, produced by running the installer in each.

```bash
cd <root>
npx bmad-method@latest install   # reference: v6.10.0, modules core + bmm + tea + cis
```

Then run the same installer once in each repo you intend to dispatch work
to. This is required: the playbook's worktree bootstrap does
`cp -R <repo_root>/_bmad <worktree>/_bmad`, so a repo without `_bmad/`
cannot be dispatched.

Install answers live in `_bmad/config.toml`, which the installer regenerates
on every run. Overrides live in `_bmad/custom/` and are never touched by the
installer — but note `_bmad/` is **not** tracked by the meta repo, so they
do not travel via git: re-answer the installer prompts on the new machine,
or copy `config.toml` (team) / `config.user.toml` (personal) over by hand.

The installer also drops `bmad-*` skills into `.agents/skills/` at each
install location, and creates `_bmad-output/` with the module artifact
subdirs (`planning-artifacts/`, `implementation-artifacts/`,
`test-artifacts/`). The root `.agents/skills` copy is the source of truth
for the global symlinks in step 5.

## 4. Fix hardcoded paths

The setup hardcodes the root path and the orchestrator workspace ID in a few
places. After cloning, substitute your new root path:

```bash
cd <root>
rg -l '/Users/moses/code' .pi docs AGENTS.md _bmad-output \
  | xargs sed -i '' 's|/Users/moses/code|<root>|g'
```

Places to verify by hand:

| File | What to check |
|---|---|
| `.pi/extensions/mayor.ts` | `MAYOR_DIR`, `PLAYBOOK`, `LEDGER` constants |
| `docs/orchestration-playbook.md` | root path refs; workspace ID (step 6) |
| `_bmad-output/briefings/_template.md` | standing-orders path |
| `AGENTS.md` | root path |
| `_bmad-output/orchestrator-jobs.yaml` | `orchestrator_workspace:` (step 6) |

## 5. Make skills visible to pi

bmad skills must resolve from any cwd (worktrees included), so symlink the
root's installed skills into pi's global skills dir. The herdr skill lives
in `~/.agents/skills`:

```bash
mkdir -p ~/.pi/agent/skills
for d in <root>/.agents/skills/bmad-*; do
  ln -sfn "$d" ~/.pi/agent/skills/
done
ln -sfn ~/.agents/skills/herdr ~/.pi/agent/skills/herdr
```

## 6. Create the orchestrator workspace in Herdr

Workspace IDs are auto-assigned — you will not get `w7`. Create the
workspace, then find its real ID:

```bash
herdr workspace list   # note the id, e.g. w3
```

Then update the ID everywhere the old one appears:

```bash
rg -n 'w7' .pi/extensions/mayor.ts docs/orchestration-playbook.md \
  _bmad-output/orchestrator-jobs.yaml
```

(sed-replace `w7` → your ID in those three files.)

## 7. Launch and smoke-test

1. Inside Herdr, in the orchestrator workspace, `cd <root>` and run `pi`.
2. The hook fires `session_start` → the startup checklist arrives as a user
   message → the mayor reads playbook + ledger and replies with a readiness
   report (active/blocked/free slots).
3. Confirm the system prompt contains "Mayor standing orders" (it is injected
   every turn and survives compaction).
4. Optional: dispatch one tiny job end-to-end to validate worktree creation,
   pane moves, briefing handoff, and ledger updates.

## 8. Notes

- The hook only fires when `cwd` is exactly the root — sessions in repos or
  worktrees are unaffected (by design: nothing outside the mayor session
  orchestrates).
- Mayor never implements in main checkouts and never merges PRs; max 3
  concurrent task panes.
- Env files are symlinked (not copied) into worktrees at dispatch — see the
  playbook's bootstrap step.
- If the harness ever changes (Claude Code, Codex, ...), port the hook; the
  trimmed `AGENTS.md`/`CLAUDE.md` stay as-is.
