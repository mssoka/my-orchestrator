# User ruling: GPT role and 3D routing (2026-09-07)

## Task
Execute the user's new model policy, superseding prior role model pins. Resolve exact installed/authenticated model identifiers, verify supported thinking levels, and make launch-time policy persistent. Gru delegates operational execution to Silas.

User wording:
> I just subscribed to gpt. so here is the new play. "/model openai-codex/gpt-6-astra" is the reasoning model runs on xhigh by default. all minions that need to work with blender should also use astra and the same thinking level. since astra is good with 3D. otherwise they run on sol xhigh. Sila runs on luna max thinking. Perkins, bob run on Astra. mega minions on Sol. but all 3D work like the game or the blender animation should be on Astra.

## Acceptance
- Gru/reasoning, Perkins round mains, Bob: openai-codex/gpt-6-astra, xhigh.
- All agents performing 3D work (including game, Blender animation, and 3D mega-minions): Astra, xhigh. This overrides generic role defaults.
- Other minions and mega-minions: Sol, xhigh. Non-3D review lens mega-minions follow Sol; 3D lenses follow Astra.
- Silas: Luna, max thinking. Exact Sol/Luna provider/model IDs must come from the available registry, never guessed; if ambiguous ask Gru for clarification.
- Verify authentication/liveness and actual session modelId + thinking level; do not claim a switch from prose or a command alone. If xhigh/max requires a pi-specific representation, verify the mapping from installed documentation rather than silently downgrading.
- Inspect active sessions and apply this user ruling safely with preserved context; no indiscriminate kill/re-dispatch. Report any review-provenance concern before altering an in-flight review. Coordinate Gru's own switch explicitly, not by killing the active session.
- Update playbook role/model policy, applicable identity extensions, watchman/relauncher defaults, quota/routing policy, dispatch and lens templates, and other active sources of old pins. Grep watcher/sensor configs for retired doctrine. Clear inherited PI_MODEL/PI_PROVIDER where relevant so old pins cannot override the ruling.
- Read pi docs and relevant examples fully before modifying pi-related code/configuration. Scope changes to routing/defaults; preserve unrelated work.
- Tests prove role + 3D override selection and intended thinking mapping. No legacy fallback silently overriding this ruling; report unavailable models and ask for fallback authorization.
- Deliver exact model identifiers, verified effective thinking levels, changed persistent surfaces, live switch receipts, any blockers, and PR URLs to Gru.

## Skills policy
Use bmad-build for meaningful tooling changes; use the installed pi documentation for extensions/models/thinking settings. Small targeted canon/config amendments: lavish not needed, PR directly. All operations and ledger transitions belong to Silas.

## Model policy
This ruling governs this task. Resolve and verify before dispatch; do not guess Sol/Luna IDs. Do not let the old extension pin undo a live switch.

## Follow-up routing correction (2026-09-07)
Silas verified PR #20 already merged at 19de900 (reviewed head 3e3c929). The later vision amendment 05d36a9 is NOT contained in origin/main. Do not push more work to the merged PR or claim that amendment shipped.

Gru decision: proceed on existing parked row `model-policy-vision-routing-followup-2026-09-07`; open ONE focused follow-up PR for the already-authorized missing vision consistency delta. Resolve fresh origin/main and verify commit containment/diff, preserve 05d36a9 and the existing worktree, reconcile onto the current base without unrelated changes. Re-run the policy and relevant helper/generated-role checks on the actual proposed head. Small targeted ops/canon amendment: lavish not needed, PR directly; pr_review=0. No merge authorization. Report exact new PR URL, base/head and verification receipt. This continues the existing user ruling, not a new creative/feature scope.

## Dispatch parameters
repo: orchestrator root
repo_root: /Users/moses/code
slug: model-policy-gpt-2026-09-07
base: resolve current remote base
model: Sol xhigh for non-3D implementation, exact ID pending registry verification
pr_review: 0 (targeted ops/config policy lane)
worktree: required for tracked orchestrator-root edits; never switch the live root checkout
