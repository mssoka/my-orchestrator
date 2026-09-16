# OpenAI quota hold — GLM interim routing (2026-09-10)

## User rulings (verbatim)

1. > we've hit the limit in openai. finish the perkin's roung with glm5.3 but pause any on-going model/asset work until we get access to more openapi tokens so we are back to the glm family until then for all other tasks.
2. > image generation, should not be paused. we don't need to model good with 3d assets for that.

## Regime

- **OpenAI/ChatGPT plan capped** ~10:48Z 2026-09-10 (pane message: "Try again in ~6638 min" ≈ 2026-09-15). Act on user confirmation of new tokens, never on the provider's stated time.
- **Perkins r1 (PP3D PR #22)** posted CHANGES_REQUESTED (1 blocker F01 static tooling-coverage gate, 24 warnings, 9 notes) — round COMPLETE; finish on glm-5.3 instruction partially moot. **F01 fix + all PP3D model/asset work DEFERRED until tokens return.**
- **Image generation EXEMPT from the pause** (ruling 2): Selva Gemini storyboard pilot S09+S14 proceeds (reserved US$4.063232 inside approved US$5; S29 held; exact `gemini-3.1-flash-image`). Executor = retained pNS **on glm-5.3**; minimal direct official-SDK script authorized (core helper pP9 stays frozen at its BMAD halt). All approval-brief rules unchanged: opaque key handling, provenance/usage receipts, no CHARGE/BMS/third-party uploads, no duplicate paid probes. First useful image = live integration check; images go to user review.
- **Paused:** pP5 Selva 3D assets (Astra-dependent), any visual/aesthetic verdicts (user-gated), all new OpenAI launches.
- **Routing clarification (user, ~16:1xZ):** "we have vision skill. if we need visuals. astra is if we need 3d work." Visual/screenshot verification does NOT wait for the hold — the vision skill covers it. Astra-waiting = true 3D craft only; those go to a GitHub issue (PP3D #25 created). k3 also available per user ("current models we have available k3, glm") — **SUPERSEDED 09-11 ~07:4xZ: k3 tokens exhausted; GLM-only interim until further notice; vision routes via local lmstudio (glm-4.6v-flash) with gemma --fast as disclosed last resort.** "if it's just code, then glm5.3 can continue working on it" — code/tooling lanes resume on glm-5.3 @ max: PR #22 F01 fix (pMY redirected to glm-5.3; Perkins r2 also glm-5.3, user-sanctioned), Gemini skill core (pP9 redirected, resumes BMAD binding recovery + implementation). PR #22's blocker is the F01 static tooling-coverage gate — pure code, zero asset work.
- **Interim routing for all other tasks:** `zai-coding-cn/glm-5.3` @ max thinking, full path mandatory. Text-only — vision caveat on any look work; aesthetic verdicts stay user-gated.
- **Identity sessions:** Silas died on the cap at ~10:48Z; Gru revived him in-place on glm-5.3 @ max (10:50Z), but that session then EXITED (~10:53Z, resume hint printed). The USER then relaunched Silas FRESH (session `01a08af4-c3e0-729e-93c4-19a701e8a2cc`, 10:54:51Z) on **`zai-coding-cn/glm-5.3-flash`** per their correction — thinking reads `high` (flash ceiling on the registry; user was mid-typing a /thinking command in-pane — left to them). Old 54MB session `01a07bb7` preserved. Gru re-sent the full regime handover as steering to the fresh session (10:57Z). The user ALSO flipped Gru to **glm-5.3 @ max** (session model_change trail confirms). Watchman pins (Luna for Silas, Astra for Gru) are WRONG for the hold duration — relaunch Silas on glm-5.3-flash, Gru on glm-5.3, until the hold lifts.
- This hold supersedes the pending general GLM matrix proposal **for its duration**; GPT-chain routing (Astra 3D/reasoning, Luna COO) resumes when the user confirms more OpenAI tokens.
- **Thinking-level ruling (user, 2026-09-10 ~12:2xZ):** glm-5.3 (pro) = **max**; glm-5.3-flash = **high**. Current panes already match — do NOT patch the flash registration to expose max (its clamp to high is now the desired behavior). Relaunch pins during hold: Silas = glm-5.3-flash @ high; Gru = glm-5.3 @ max; minions/Perkins = glm-5.3 @ max. silas.ts still pins Luna @ max at session_start — flaps on relaunch during the hold (observed 10:54:58Z, corrected 15s later); tame at hold lift or accept meanwhile.

## Second hold — 2026-09-14

User, verbatim: **"we are out of tokens with astra. openai."** then **"so we are back to glm fully."** Same regime re-applies in full (glm-5.3 @ max code/general/minions/Perkins; glm-5.3-flash @ high Silas; Gru glm-5.3 @ max; watchman Luna/Astra pins invalid for the duration; resume ONLY on explicit user confirmation of OpenAI tokens, never a probe-up). Differences from the first hold:

- **PP3D PR42 warning-fix lane was ALREADY on glm-5.3 @ max** (user's scoped model choice minutes earlier) — unaffected; fresh Perkins rounds stay glm-5.3 @ max.
- **Selva artist (w9Z:p1)** completed the `blender-music-video` skill install at the cap moment (real dir `/Users/moses/code/.agents/skills/blender-music-video/` — SKILL.md/scripts/tests/references/examples/validation present, NOT a worktree symlink; artist claims 32 tests + native integration checks passed, `/skill:blender-music-video` invocable — Silas owes independent validation + future-job discovery check). Flipped in place to glm-5.3 @ max; any further pixel/aesthetic verification DEFERRED to hold lift (user-gated).
- **Silas died on the cap mid-relay** (Codex usage limit) — revived same pane/session via `/model zai-coding-cn/glm-5.3-flash` + `/thinking high` + continue (footer verified).
- The 2026-09-12 lift note in the project AGENTS.md is historical for the hold duration; the GPT chain is suspended, not retired.

## Resume trigger

User confirms more OpenAI tokens available → restore GPT-chain model policy, update watchman pin back to Luna, unpause pP9/pP5/PP3D-fix lanes, resume normal routing. Preserve all frozen state verbatim through the hold.
