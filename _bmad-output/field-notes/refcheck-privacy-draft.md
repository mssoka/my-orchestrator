# Field notes — righttenantry-refcheck-privacy-draft (2026-08-02)

- `element.unsafe_raw_html` CANNOT emit a standalone HTML comment (lustre 5.6 wraps inner_html in `<tag>…</tag>`; a `!--` tag renders `<!-->TEXT</!-->` and LEAKS visible text) — for a rendered comment, post-render `string.replace` on the exact serialized open tag + a presence/uniqueness test pin.
- `functions.edit` batches are ATOMIC — one bad `oldText` rejects every edit in the call, and `gleam format` reflows split strings between runs; re-read the formatted file before re-issuing a failed batch.
- Privacy-page copy tests must assert the RENDERED form: apostrophes come back as `&#39;` (houdini escape) — "landlord's" in an h2 pin fails against raw text.
