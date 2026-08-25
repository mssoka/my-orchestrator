# packet-plumber-v2-5.3-pause-ux

- The app pause overlay (app/main.odin) is APP-LAYER ONLY — the harness T2 captures
  (world+forecast+health+banner) NEVER include it, so an overlay change shifts zero
  goldens; the app's own frame is verifiable only via a scratch replica using the rlsw
  shadow (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`) + `LoadImageFromScreen`, with
  pixel-scan (PIL) for overlap truth — vision models misjudge absolute coordinates.
- The top HUD band's only always-free slot is the gap between the Network Health card
  (right edge `win_w/2 + 230`) and the forecast panel (left edge `win_w - 250`) — the
  top-left column carries the QoS readout when a pipe is selected and top-right hosts
  the forecast during a crisis pause, so "top-left or top-right" chips collide in the
  exact pause-and-plan states; anchor the chip at `win_w/2 + 240` (tracks resize).
- A presentation-only ruling still earns a canon amendment in the SAME PR (GDD + art-
  direction + story-card status line): grep the pause canon first ("Pause-to-plan;
  color + icon + glow coding" is the indicator line), match house style, and state the
  ruling source (user ruling date + job id) so canon and code can never drift again.
