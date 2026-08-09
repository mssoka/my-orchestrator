# Field notes: packet-plumber-narrative-messaging (2026-08-07)

- Briefing banned em-dashes "CI-guarded", but disk shows NO em-dash CI guard in
  packet-plumber (no .github/workflows, no markdownlint/textlint/pre-commit) and
  the lavish-approved GDD uses 173 em-dashes; the brief's own locked alert
  `YOU_TUNE: DOWN — 2.3B` contains one. Verified against disk, surfaced to user
  as an open decision; kept all NEW copy em-dash-free, locked string verbatim.
  Generalizes (field-notes rule): briefing "constraints/current-state" can be
  stale; grep disk before honoring a CI claim.
- lavish on a ~49KB creative doc: `npx -y marked --gfm -o body.html doc.md`
  (file write, no pipe) + a node-assembled themed HTML shell rendered cleanly;
  user verdict was a terse "read good." + Send&End = approval; confirmed via
  ~/.lavish-axi/state.json `sessions/<id>/chat[].text` (no stranded prompts).
- Self-review (edge-case-hunter) caught a real constraint violation: banking
  copy said "DROPPING" but banking SLA is zero-drops `[GDD § M2]`; fixed to
  STALLING (transactions hang, packets never drop). Cross-check every copy
  sample against locked MECHANICS, not just tone.
