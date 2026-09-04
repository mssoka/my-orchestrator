# Field notes — packet-plumber-3d-gdd-v1 (2026-09-04)

- The pi `edit` tool is **atomic across the whole edits[] array** — one failed
  oldText rolls back ALL edits in the call (my 4-edit lavish-round-1 apply
  silently lost 3 of 4 edits; caught by re-grep). Always re-grep after a
  multi-edit apply, and keep oldText minimal so a miss is diagnosable.
- `bin/ledger set <id> in-review` is guarded: it REFUSES unless the `pr`
  field is already set — run `bin/ledger pr <id> <url>` FIRST, then `set
  in-review` (or pass the URL in the note). Wrong order = refused, not warned.
- Lavish craft: the FIRST `poll --agent-reply` returns only the dom_snapshot
  (no feedback) — that's normal; re-poll to actually wait. The
  `_local-refs` loopback pattern (`python3 -m http.server 4388 --bind
  127.0.0.1 --dir <refs>` + `http://127.0.0.1:4388/...` img URLs) serves
  IP-sensitive frames in the review page with zero copying — verify a 200
  with curl before opening the session.
