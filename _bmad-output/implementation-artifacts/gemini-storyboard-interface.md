# Corrected Gemini storyboard interface — v1

Recipient: **Silas only**, for the retained pNS executor. Supersedes the provisional
handoff. Parent offline checks passed; **prescribed parent review pending**.
No request, credential read, upload or live image was performed by core.
Do not interpret this file as a pilot success, new spend grant or global install.

## Exact isolated package and commands

```bash
PY=/Users/moses/.herdr/worktrees/my-orchestrator/gemini-storyboard-skill/.scratch/gemini-venv/bin/python
SKILL=/Users/moses/.herdr/worktrees/my-orchestrator/gemini-storyboard-skill/.agents/skills/gemini-storyboard
ABS_OUTPUT_ROOT=/Users/moses/code/_local-refs/selva-gemini-pilot-20260910/runs
ABS_SHARED_LIVE_BUDGET=/Users/moses/code/_local-refs/selva-gemini-pilot-20260910/live-budget-v1

# Read-only schema/help from any cwd; no credentials/client/network.
"$PY" "$SKILL/scripts/storyboard.py" --help
# pNS prepares its own manifest; core never edits channel files.
"$PY" "$SKILL/scripts/storyboard.py" plan --manifest ABS_MANIFEST --output-root "$ABS_OUTPUT_ROOT"
# plan prints ABS_RUN = OUTPUT_ROOT/video.id/run_id
# Only the already authorized executor, after corrected parent readiness:
"$PY" "$SKILL/scripts/storyboard.py" generate --run ABS_RUN --live \
  --approved-by pNS --approval-id gemini-storyboard-live-pilot-approval-2026-09-10 \
  --accept-cost --budget-dir "$ABS_SHARED_LIVE_BUDGET"
```

Use the user's existing configured shell; `GOOGLE_AI_API_KEY` must be inherited.
Helper explicitly maps it to `genai.Client(api_key=...)`, with Vertex disabled,
timeout bounded and SDK attempts=1. No key argv, startup-file display, key receipt,
environment dump, auth/quota probe or duplicate paid test. Core tests use only
synthetic key values injected at the fake SDK boundary.

The exact package/version/file hashes live in
[package manifest](gemini-storyboard-package-manifest.json) — regenerate it from
the final tree with the snippet in
[offline verification](../../.agents/skills/gemini-storyboard/references/offline-verification.md)
whenever package files change; never hand-edit hashes. Python 3.14.0;
`google-genai==2.22.0`, `Pillow==12.3.0`, `pytest==9.1.1` in that venv.
[Offline verification](../../.agents/skills/gemini-storyboard/references/offline-verification.md)
is preserved. Installed shape: `GenerateContentConfig(response_modalities,
image_config=ImageConfig(...))`; exact model `gemini-3.1-flash-image`.

## Input/output contract

- [SKILL.md](../../.agents/skills/gemini-storyboard/SKILL.md)
- [Template](../../.agents/skills/gemini-storyboard/templates/video.json)
- [Full contract](../../.agents/skills/gemini-storyboard/references/contract.md)
- [Pricing](../../.agents/skills/gemini-storyboard/references/sdk-pricing.md)

Manifest requires approved video/style direction: medium, shape language, palette,
materials, lighting, camera/composition, mood, continuity and exclusions. Every
shot requires story beat, subjects, action, location, framing, lighting, supplied
section and timing (explicit or unknown). References require stable ID, role,
provenance, actual PNG/JPEG/WebP, and external-use permission. Both text and exact
reference bytes reach the request. No hidden film defaults or executor ID pin.

`plan` exclusively creates immutable run/reference snapshots under
`ABS_OUTPUT_ROOT/video.id/run_id`. These exact cached bytes, generated outputs,
attempt receipts, HTML cards and review records stay **outside all repositories**;
no reference/output copy into the channel or core worktree. Directories are not
created by this handoff; the authorized plan/generation commands create them.
The single budget path above is shared across both jobs/all pilot attempts.

Run output: `manifest.json`, `plan.json`, `plan.html` (dry cards, NOT generated
images), `seal.json`, `execution.json`, `references/`, per-attempt
`attempts/ID/{reservation.json,request.json,receipt.json,final.*,card.html}`
and `review.json` after a real human look decision.
Receipts retain model/config/hash/usage/safety/review disposition. Bill unknown;
reservation is not actual spending. No transport retries or silent overwrites.
`--resume` skips every attempted shot, including unknown/timeouts; never repeats it.

## Ratified pilot selection — job-specific, never a core default

Preserve the complete inventory **S09/S14/S29**. Select **S09 + S14** only, each
owner-confirmed `not_started`; keep S29 `selected:false`, without spend. S47 and
all started/unknown production remain untouched. Per user ruling the aggregate
cap is US$5, fixed reserve US$2.031616/attempt, **US$4.063232 for the pair**; no
third attempt or correction fits the remaining reserve. Set manifest budget
`{"limit_usd":"5","max_attempts":2}`. No further two-shot ratification owed.

The W attachment disposition is already authorized; **no core conversion**:
- Outside-repo derivative: `/Users/moses/code/_local-refs/selva-gemini-pilot-20260910/caminante-concept.png`
- PNG 960×540; SHA256 `27cd857249342b6fd62f0a0283c6f8e1885983315c4131caf9082d23a39c4510`
- Authoritative untouched SVG SHA256 `8aaca9ea3575550eb85afeadf8dd69e0117f387f8e97b2233eaac626d21d56cd`
- Disposition JSON SHA256 `15d4a588f685cfd49a00b5f7c30adb39b3a091e6430f8350e76444f4ad68fa84`
- Existing derivative: `rsvg-convert 2.62.1`; identity/wardrobe/cuff-sleeve only,
  not rough illustration finish/native W production. Source files remain untouched.

## Review boundary

Parent-corrected **139 offline tests**, **12/12 mutations** pass; no live/aesthetic
claim. Prescribed BMAD independent review remains pending at this revision.
When readiness is released, the first useful image doubles as live integration;
no PR/merge wait. pNS inspects actual originals, presents shot-labelled comparison
in lavish and records the human look disposition before any expansion. The helper's
`review` command requires genuine successful LIVE bytes and actual human inspection;
mock/dry receipts cannot authorize expansion. This handoff grants no new scope.
