# Resolve Free21.1 — verify direct API access before building MCP/skill plumbing

User originally asked to set up Resolve MCP, then supplied samuelgursky/davinci-resolve-mcp, and now asks **"do they expose api that the mcp is using anyway? can we use skills?"**

Gru decision: perform a SHORT, harmless capability probe under this setup request. Do not spend a new implementation lane building a wrapper over inaccessible APIs. This is ordinary read-only setup investigation; no fresh user approval for basic probes. Silas may handle as a small ops probe or delegate one helper as appropriate; do not interrupt current Selva/PP3D owners or run a fleet.

## Known facts

- Installed `/Applications/DaVinci Resolve/DaVinci Resolve.app`,21.1.0/build21.1.00017; fresh installer receipt `com.blackmagic-design.ManifestLite`21.1 and free-edition ReadMe. Resolve is running; PID47955 was an earlier observation, NOT future authority.
- Actual SDK `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.md` documents Python/Lua, bundled `Contents/Applications/ResolvePython`, `Contents/Libraries/Fusion/fuscript`, and Studio external-scripting settings. A skill can call authorized scripting directly; MCP is optional, not the source of capabilities.
- Upstream current v3.2.0 SHA c8fbe1887324de9d897e6036efcde60417e33e8c. Its Python bridge was verified on Free21.0.x, NOT21.1. README is stale on issue203's latest reports: https://github.com/samuelgursky/davinci-resolve-mcp/issues/203#issuecomment-5604750410 reports no Py3 console; #issuecomment-5638490830 reports Lua files enumerate but even print/file probes don't run on one Apple-Silicon Free21.1 install. These are third-party reports, not measurements of our machine.

## Follow-up: establish the live prerequisite (Gru application, 2026-09-13)

The first probe verified both bundled interpreters but ran while Resolve was absent. Its nil handles do NOT establish Free-edition incompatibility. Preserve that result as inconclusive for live access.

Under the original setup request, a single ordinary launch of the installed Resolve app **when it is not running** is permitted. This is not permission to kill/restart a running app, alter startup/security settings, choose/switch/create projects, accept licenses, or dismiss consequential dialogs. Leave an already-running app alone. After normal startup finishes, repeat only documented read-only product/version/project-manager/current-project-handle queries. A valid API/project-manager handle with no current project is useful positive evidence, not a failed probe. If setup, permissions or project context genuinely prevent further testing, report that precise limitation without inventing an edition verdict.

For external Python, use the SDK's documented environment variables scoped to the probe process, including the actual `RESOLVE_SCRIPT_LIB` path. A default path guessed relative to the system Python executable is not proof of API incompatibility and does not require patching the SDK. No persistent configuration change. Attempt harmless in-app Lua only through available documented access; no permissions bypass or project creation. Keep a finite follow-up (<=10min), preserve user work, and report actual capability rather than another wrapper installation.

## Probe and report

Target <=15min investigation, no downloads/installs unless truly necessary for a minimal user-scoped probe. First read actual local documentation/tool help. Use only documented interfaces and read-only calls: product/version and whether the current project handle is available. No project creation/import/edit/render/switch, no source-media upload, no touching the live project DB. Do not execute upstream installer or write global client configs yet.

Where supported, inspect direct Python/Lua access and in-app Lua execution. Menu appearance alone is not evidence that a script executes or has API access. Use a unique harmless stdout/scratch marker to distinguish no execution from no API handle. Bound each external probe, reap only its own child if needed; never kill/restart Resolve/user apps or broaden permissions. If UI access requires unavailable OS permissions, report that rather than bypassing it or guessing. No binary patching, licensing circumvention, paid purchase, downgrade or default-security weakening.

Deliver a concise matrix: direct Python, direct Lua, in-app Lua — tested result/untested limitation, exact observed version, next viable route. If live access works, recommend thin skill+helper CLI; if not, distinguish offline export-file tooling from live editing. No claim that a skill unlocks Studio features. Preserve only compact new probe evidence; don't create a large review/report framework.

## Context / routing

- Owner context: managed youtube-channel studio tooling; no changes to its main checkout or existing production worktree.
- Skills: installed context7-docs and Pi docs/skills.md; gds-investigate only as a scoped read-only investigation, no bootstrap/review fleet. Custom skill/CLI implementation is a later step after capability is actually proven.
- Model if delegated: openai-codex/gpt-5.6-sol / xhigh (non-3D integration probe). Existing production parents remain Astra/xhigh.
- No PR required for probe; no Lavish approval gate. Report actual capability or concrete incompatibility to Gru. Do not automatically register an offline MCP server as if it controls the running editor.
