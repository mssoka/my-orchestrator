## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-ux-font-resize · **Reviewed sha:** `91f7730` · **Reviewers:** 7/7 completed
**Verification:** 23/24 findings confirmed against the code — 1 discarded as false-positive

**Load-bearing checks (Perkins ran locally at the sha):** lint all gates green · harness **28/28 demos green, run twice (deterministic)** · `odin build app` clean · **T1 state-hash goldens + `.log.bin` replay logs byte-identical** (0 diffs, `core/` untouched, LOG_VERSION unchanged) · the 24 re-blessed T2 PNGs match the PR body inventory **exactly 1:1** · contrast ratios in the PR body all reproduce (WCAG math) · contested text widths measured from the committed TTF (exact advance metrics).

### Blockers (0)

None.

### Warnings (8)

1. **[6 reviewers] Font loads via CWD-relative runtime read with silent `GetFontDefault` fallback** — `app/render/view.odin:443-458`. Blast radius narrowed on verification: wrong-cwd launches exit loudly at the `data/*.json` catalog reads first, so the silent path needs `data/` present but `assets/fonts/` missing — but in that state the app silently re-renders the illegible default font (the reported defect resurfaces) and a harness re-bless would poison goldens with the wrong font, no diagnostic. The repo already embeds assets via `#load` (`palette.json`, `assist.json`); `rl.LoadFontFromMemory` over an embedded blob eliminates the cwd dependence entirely.
2. **[3 reviewers] Assist route-tie caption renders at 11px** — `app/render/assist.odin:466-471` (`fs := i32(max(11, s * 0.30))` → 11px at 1280×720). Player-facing reading text below the PR's own "nothing below ~14px" canon; `assist.odin` was outside the audit's file set. Fix: floor at 14.
3. **[2 reviewers] Bottom-right mode label (+ transient nudge) overlaps the tray chips for widths < ~1256px — including the min clamp** — `app/main.odin:1258`. Geometry: label x = `win_w−320` = 832 vs tray right edge 884 at 1152 (6 chips, 616px, centered). Confirmed in your own committed min-clamp capture (the text overprints the "high" chip — it transcribes as "highassist: fu…"). New overlap zone introduced by this PR (the fixed-1280 window never collided). Fix: `x = max(win_w−320, tray_right+12)`.
4. **Run hint runs ~38px under the health card for widths < ~1230 — including the min clamp** — `app/main.odin:1148`. Measured hint width 372.8px (ends x=385) vs card left edge 347 at 1152; the card draws after the hint, hiding its tail (pixels confirm glyphs terminate flush at the card edge). The Design Notes' claim that the hints "clear the card's left edge at min width too" is false below ~1230. Clears 25px at the 1280 default, so the launch AC holds.
5. **[2 reviewers] Pause-chip two-line threshold (104px) is below the hint's real rendered width** — `app/main.odin:383-384`. Exact TTF metrics: "P/Space to resume" @12px + spacing 1 = **121.0px** (+8 inset → needs 129); `chip_w` caps at 120. For widths 1208–1238 the hint can touch the weather-report card; at wider sizes it always overhangs the chip rect ~9px (cosmetic). Raise the threshold to 130 or shorten the hint.
6. **Font-load fallback branch has zero coverage** — the spec's I/O matrix declares it, no test exercises it (`view.odin:451-458`).
7. **Resize/HUD-adaptivity math (min clamp, `chip_w` clamp, 104 threshold, anchor math) has no automated coverage** — the only verification is manual screenshots, which demonstrably missed warnings 3–4.
8. **Advisory test gate: CONCERNS** — P0 100% (T1 immutability + T2 determinism pinned by the golden suite), P1 ~70% (new presentation math + fallback untested).

### Notes (7)

- `draw_health_ring`'s comment still says "the font is the raylib default" — now false (`view.odin:379`).
- Frozen spec says `SetWindowMinSize` before init; code correctly calls it after (`main.odin:173`) — spec text inaccuracy only.
- "spacing 1 — the same spacing raylib's DrawText used" is inaccurate for ≥20px text: raylib used `fontSize/10` (2px/char at 22px, 3px at 30px), so the title/toasts now render 21–58px narrower. Goldens absorbed it; the comment misleads (`main.odin:1366`, `view.odin:427`). *(The reviewer's "0.0f" mechanism was discarded as false-positive; re-verified against raylib source.)*
- Three copy-paste `*_text` procs in `palette.odin` — one darken helper would do.
- Pause-chip gap constants (240/260) re-encode health-card/forecast geometry from other files — they'll silently drift when those cards change (5.2+/queued HUD work).
- Popover demolish 13→14px + game-over toast y-move shipped with no verification of any kind.
- Sub-min-size windows rely entirely on the WM honoring `SetWindowMinSize` (defense-in-depth gap; unreachable in practice on macOS).

### Reviewer agreement
W1 (6/7 lenses — font cwd/silent-fallback), W2 (3 lenses — 11px tie caption), W3 (2 lenses — tray overlap), W5 (2 lenses — chip threshold). The four multi-source findings all survived independent code + pixel re-verification.

**Verdict:** READY TO MERGE

Both user-reported defects are fixed and verified; the presentation-only invariants all hold (T1 byte-identical, fold deliberate + exactly listed, harness fixed-size, no sim/serialization/replay contact). The 8 warnings are real but none violate the spec's named ACs — the two new min-clamp overlap zones (3–4) and the 11px caption (2) are the ones I'd fix first; all are small, localized pushes.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
