# Field notes — packet-plumber-ue-slice-1

- UE-MCP bridge: `ue-mcp init` is pty-only; deploy via the package's
  `dist/deploy-cli.js` directly, then REBUILD (a stale editor instance shows
  "Incompatible or missing module"). The bridge port.json goes STALE on
  editor restarts — rewrite it from `Saved/UE_MCP_Bridge/instances/<pid>.json`;
  pkill misses old editors (kill by pid — multiple instances share the
  project and confuse everything). Stale `Binaries/Mac/*.dylib` pile up (43!)
  and the editor loads the HIGHEST — a full wipe+relink can produce an
  INCOMPATIBLE module stamp; keep at least one old dylib.
- C++-only UUserWidget (no designer asset) must build its tree in
  `RebuildWidget()` — NativeConstruct runs after the Slate widget exists and
  setting RootWidget there silently renders nothing. Same for
  `GetCachedGeometry` at construct time: fall back to the design size and
  re-fit on tick.
- UE UMG canvas is DPI-SCALED: the widget geometry (e.g. 1896x1081) is the
  layout truth, NOT the game viewport (1280x730) — the fit must use the
  widget's local size or everything renders shifted. Runtime
  AddChildToCanvas in NativeTick never paints — pre-create the pool in a
  layout pass (RebuildWorld) and only reposition in tick; every ClearWorld
  must be paired with a pool rebuild; FSlateRoundedBoxBrush ImageSize
  defaults to ZERO (explicit it or the widget is invisible).
- VERIFY SCREENSHOTS WITH PIXEL SCANS, not vision alone: the r1
  "mid-traversal" frame had zero dot pixels (the vision model hallucinated
  it — I trusted a single vision read). The dot was ALSO genuinely broken
  (the cascade above). After fixing, pixel-scan (4 positions across 12
  frames) + vision agreed. Never re-bless evidence on a vision claim.
- UE global `FIntPoint` (TIntPoint<int>) collides with `PP::FIntPoint` in
  engine-side files — qualify `PP::FIntPoint` everywhere outside the sim
  headers. The editor re-writes the AndroidFileServer section into
  DefaultEngine.ini on EVERY boot — disabling the plugin fixes it.
- Enhanced Input runtime actions must be created in the CONTROLLER
  CONSTRUCTOR — SetupInputComponent runs BEFORE BeginPlay, so BeginPlay-
  created actions are null at bind time (dead mouse, masked by MCP-bridge
  drawing). The module test binds + Execute()s the returned binding to
  synthesize the trigger headlessly.
- Test-module headers: the game module's headers must live in
  `Source/PacketPlumber/Public/` for the tests module to include them; the
  API macro (PACKETPLUMBER_API) is auto-defined by UBT — mark cross-module
  classes with it.
