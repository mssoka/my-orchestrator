# righttenantry-dublin-rents-q2-2026 (2026-08-24)

- OG-card orphan test (`content_pages_point_at_their_own_og_cards_test`) fails on ANY committed `priv/static/og/*.png` not pinned in its pairs list — every new series post needs its card pinned there (plus the `let assert Ok(post)` lookup).
- Worktree bootstrap missed `server/.env -> ../.env` (main checkout has it) — without it `make run` panics "DATABASE_URL not set"; add the symlink before smoke-testing.
- og cards: `rsvg-convert -w 1200 -h 630 card.svg -o card.png` is the pipeline (PNG 1200x630 RGB); verify the render via `bin/vision-read` — and never sed a `</` inside an SVG text tag (it ate `</text>`).
- Data note for next quarter: verify figures against the live reports (Daft PDF/press + rtb.ie "latest" page — Q1 2026 RTB index still unpublished as of this PR; Q4 2025 rows stay dated explicitly).
