# Reliable Blender MCP startup / explicit enable

## Authorization and task
User asked whether Blender MCP was required because it did not start after the minion restarted Blender. Gru distinguished interactive MCP from native batch renders and found existing addon auto-start code, but NO separate enable/startup script in the inspected project/startup locations. After Gru asked, "Shall I have Silas add a reliable startup/enable mechanism and verify it at a safe restart?", user answered **yes**.

Implement a reliable, documented startup/enable mechanism and PROVE it at a safe restart. This authorizes narrowly scoped local setup and a coordinated enable/restart, not interruption of active work or indiscriminate Blender/process/prefs changes. Silas owns operational scheduling and delivery. Separate tooling lane; do not fold into open vision/video/config PRs or Selva/PP3D feature code.

## Known evidence (do not re-infer)
- Interactive Selva Blender is controlled through `blender_execute_blender_code`. Concrete successful results were observed before the user toggled it off.
- Native `Blender -b <library> --python premium_render.py` workers need NO MCP listener; installed addon start() deliberately refuses background mode. That behavior is correct and must remain.
- Installed addon: `/Users/moses/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py`.
- register() defines Scene.blendermcp_auto_start_server default=True and starts BlenderMCPServer on addon registration when the saved scene flag is true; default port 9876. Startup/bind errors stop it. This is NOT proof it survives user restart workflow.
- User explicitly said earlier successful enable was MANUAL, then disabled it. Gru's subsequent real `blender_get_scene_info` call failed: "Could not connect to Blender. Make sure the Blender addon is running." No restart/fix was attempted during that test.
- Prior live listener/bridge PIDs are HISTORICAL, not safe action targets. Re-resolve processes/session endpoints immediately before any intervention.
- Selva parent `w85:pMS` owns the shared interactive Blender and has unsaved/generated creative work plus native workers to preserve. PP3D `w85:pMY` must not take that scene. Their tools/helpers may change; census current ownership rather than guessing.

## Requirements / acceptance
1. Diagnose exact startup failure class using installed code, addon registration state, enable/autostart settings, startup flags, saved-scene properties and logs. Separate normal interactive launch, file-open/restart, optional factory-startup invocation, manual STOP, disabling auto-start, disabling the addon, port conflict and background workers. Do not claim a cause from the default=True line alone.
2. Provide a small operator/agent-facing command or supported local startup hook to explicitly ENABLE/START, CHECK STATUS and deliberately STOP/DISABLE automatic startup. Choose the narrowest reliable documented mechanism; avoid competing implementations and duplicate server lifecycles. Commands must clearly distinguish installed/enabled/listening/connected and print useful failures.
3. Interactive Blender startup should reliably establish the local addon listener in the supported normal launch/restart path, with bounded readiness/handshake checks. Explicit enable can bootstrap when MCP is unavailable; never require a functioning MCP connection to repair that same connection.
4. Preserve user control: no watchdog that repeatedly undoes a deliberate STOP. Define/document temporary stop vs persistent auto-start/addon disable; persistent opt-out stays off until explicit enable. The user's current **yes** authorizes ONE coordinated enable/setup/test; it is not perpetual permission to reverse future manual disables.
5. Idempotent enable/start: repeated calls produce ONE owner/listener, no duplicate Blender sessions/addon copies, no busy loop. Default bind stays loopback only (127.0.0.1/localhost); do not expose arbitrary Python execution to the LAN. Never kill an unrelated process to free a port. On conflict, report owning process and fail safely.
6. Background render/validation workers remain listener-free and unaffected. Do not change render-job code merely to satisfy connectivity. Distinguish an idle MCP client process from a live addon listener and prove the connection reaches the CORRECT interactive instance/file/scene.
7. Preserve preferences/addon version/install provenance. If an installed addon change is necessary, prefer supported extension/configuration hooks; otherwise carry a hash/version-gated, backed-up, reversible installer patch with tests and durable tracked source. Do not silently edit an ignored installed file with no restoration path. Do not reinstall Higgsfield or add new cloud services.
8. Do not broadly enable automatic execution of arbitrary .blend Python, loosen security settings or inject unverified keystrokes into the focused app. Use trusted, explicitly installed local code and a known target.
9. Logs/receipts record timestamps, supported Blender/addon version, enable state, endpoint, action/result and handshake; no credentials or sensitive unrelated scene content. Script output/error must be accurate (no successful message after connection failure).

## Safe restart / proof contract
- Read-only inventory first; coordinate with Silas and Selva parent for an explicit safe checkpoint. Verify no active RENDER/OBJECT_BAKE/COMPOSITE/native render worker or other user operation will be interrupted. If a render is active, stage/test in isolation and wait for its completion; no kill/restart just to clear the gate.
- Have the owning parent save/verify its working project, preserve the correct file/scene path and checkpoint evidence, and acknowledge the restart before it happens. Preserve other scenes and user preferences; no factory-reset of the live scene.
- Prefer isolated test configuration/profile/port for failure and idempotency tests. Never compete for the live owner's port merely to test a collision case.
- At the safe live checkpoint: perform the supported restart without a manual addon-panel click, then a FRESH MCP get_scene_info round-trip proving the listener and correct owner/project are back. Old established TCP connections and old receipts do not count. Report exact command/hook, times and returned scene identity.
- Test enable twice, deliberate stop, persistent opt-out and explicit re-enable; verify background worker remains listener-free; simulate startup/port failure safely. Restore the user-approved enabled final state after the agreed test, except if user changes direction.
- If live restart cannot yet be scheduled safely, report precisely "implemented/tested in isolation; live restart proof pending" with the named safe-checkpoint trigger. Never mark complete on unit tests alone.
- Resume Selva's SAME minion/session/worktree/scene writer after the proof. No agent re-dispatch or model switch. PP3D work and unrelated native GPU jobs remain untouched.

## Delivery / scope
- Focused tracked tooling/config/docs changes in orchestrator-root worktree, conventional PR versus fresh origin/main; no merge authorization. Preserve all unrelated local modifications and open PR branches.
- Automated tests cover states and failure paths; live restart receipt proves actual behavior. Include concise operator usage, supported launch modes, install/uninstall/rollback and how to intentionally leave it disabled.
- Check active Blender/video agent instructions and relevant lifecycle/sensor configs for the new startup contract and stale assumptions; amend only what's necessary, preserving background-worker distinction. Small targeted doc edits: lavish not needed, PR directly.
- Notify Gru with PR URL, actual state (installed vs merely proposed), tests, live restart evidence, current Selva readiness, any remaining blocker and the exact enable/status/disable commands. No "done" before live proof or clearly named pending trigger.

## Skills policy
- bmad-build for meaningful tooling implementation and independent review. The mixed-module renderer was repaired in the separate #23 lane; verify bootstrap/rooting correctly and use the compliant rendered workflow, not raw-source fallback.
- context7-docs/current installed Blender MCP and Blender documentation for startup/addon APIs; inspect local addon too (local version differs from generic upstream).
- No large planning/lavish detour for this narrowly authorized ops fix.

## Model policy
Tooling minion and non-3D helpers: `openai-codex/gpt-5.6-sol`, xhigh. Silas stays Luna/max. Existing Selva/PP3D art/3D agents remain Astra/xhigh. If genuine 3D scene work is required, it stays with the owning Astra agent; the ops worker must not author/change creative content. Pin full identifiers/thinking and verify session provenance.

## Dispatch parameters
repo: orchestrator root
repo_root: /Users/moses/code
slug: blender-mcp-reliable-startup
job_id: my-orchestrator-blender-mcp-reliable-startup
base: main (fresh origin/main)
model: openai-codex/gpt-5.6-sol
thinking: xhigh
pr_review: 0 (ops-tooling; bmad-build independent review + live restart proof required)
worktree: isolated; never switch live orchestrator checkout
coordination: Selva owns shared Blender; safe saved checkpoint BEFORE live enable/restart testing
completion: focused PR + actual install/state receipt + verified safe live restart + resumed owner; no merge
