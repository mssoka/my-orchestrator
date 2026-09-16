# Field notes — righttenantry-agents-model-single-source

- 2026-09-05: BSD (macOS) sed has no `0,/re/` address — a "mutation test" silently mutates NOTHING; worse, `git checkout -- <file>` afterwards nuked my real unstaged edits. Mutation tests: python replace + cp backup + diff-verify restore, never sed+checkout.
- 2026-09-05: bmad-quick-dev is GONE from the canonical home (successor bmad-build can't render — no `_bmad/scripts/render_skill.py`); standing waiver path worked: self-contained briefing + waiver note in PR body + run bmad-build's review-prompts (`review-prompts/*.md`) directly as herdr mega-minions — step-04 discipline without the renderer.
- 2026-09-05: `herdr agent wait <pane> --until idle` is the working syntax (skill doc's `herdr wait agent-status --status` is a newer/other CLI); `--until done` fires only in background panes, `idle` when seen.
