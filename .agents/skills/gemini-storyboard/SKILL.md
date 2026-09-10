---
name: gemini-storyboard
description: Plan portable, reference-conditioned storyboard look targets offline, then optionally execute separately approved budgeted single-turn Gemini image requests. Use for new videos with explicit approved direction, unstarted selected shots, and cloud-permitted image references. Never treats generated images as animation or native-production proof.
---

# Gemini storyboard

One helper: [scripts/storyboard.py](scripts/storyboard.py). No application
registration, film defaults, chat history, native production, audio analysis,
authentication probing, or transport borrowed from another skill.

## Read before use

- [Manifest/CLI contract](references/contract.md)
- [SDK shapes, pricing and uncertainty](references/sdk-pricing.md)
- [Offline verification and limitations](references/offline-verification.md)
- [Editable manifest template](templates/video.json)

The template deliberately **fails validation** until filled in. Never manufacture
human approval or cloud permission to make it pass. Confirm selected shots are
`not_started`; missing/started/unknown status fails closed. Film story/style is
entirely user data. Omit optional `start_frame` / `end_frame` unless supplied;
leave timing `unknown` unless explicit timing was provided.

## Setup and cwd-independent usage

macOS/Linux, Python 3.11+ (verified with 3.14), a local filesystem with POSIX
`flock`, exclusive creation and fsync. Paths below are explicit absolute paths;
set `SKILL` to **this SKILL.md's containing directory**, not the current cwd.

```bash
SKILL=/absolute/path/to/.agents/skills/gemini-storyboard
PY=/absolute/path/to/venv/bin/python
# Provision dependencies separately; this install step can use network.
python3 -m venv /absolute/path/to/venv
"$PY" -m pip install -r "$SKILL/requirements.txt"
# Offline alternative: add --no-index --find-links /absolute/path/to/wheelhouse
"$PY" "$SKILL/scripts/storyboard.py" --help
cp "$SKILL/templates/video.json" /absolute/path/to/project/video.json
```

Fill the copied template from human-approved direction and reference provenance.
Reference paths resolve relative to the **manifest**, never the shell cwd.
Choose a new video ID/run ID namespace, explicit budget, and at most three initial
selected illustrations. Keep all intended shots in the inventory for later look review.
All cache/output bytes must live in an approved **outside-repository** output root;
select that path explicitly. A zero budget is allowed for planning only.

```bash
"$PY" "$SKILL/scripts/storyboard.py" plan \
  --manifest /absolute/path/to/project/video.json \
  --output-root /absolute/path/to/storyboard-runs
# Prints /absolute/path/to/storyboard-runs/VIDEO_ID/RUN_ID
RUN=/absolute/path/to/storyboard-runs/VIDEO_ID/RUN_ID
"$PY" "$SKILL/scripts/storyboard.py" generate --run "$RUN" \
  --mock --budget-dir /absolute/path/to/shared-MOCK-budget
"$PY" -m pytest "$SKILL/tests" -q
"$PY" "$SKILL/tests/mutations.py"
```

These plan/mock/test operations need no key or network. `plan.json` contains
prompts, selected/excluded shots, config, reference hashes and conservative cost
caveats; `plan.html` renders the same dry-run prompt cards (never images). Exact image bytes and escaped HTML cards live under
`$RUN/attempts/ATTEMPT_ID/`. MOCK cards are unmistakably labelled; their tiny
synthetic image proves plumbing, **not aesthetic quality**.

## Explicit live action — NOT part of initial implementation or verification

Do not run this section during preparation. The caller must have explicit human
spend approval and be the designated executor, with approved reference external use
and one agreed shared budget directory across all runs. Never read/display startup
files, source `.env`, print credentials, probe auth/quota, or upload test references.
Launch from the user's already-configured shell with `GOOGLE_AI_API_KEY` inherited;
the helper maps it explicitly in-process to `genai.Client(api_key=...)` only after
live gates/reservation. SDK default variable names are **not** used as fallback.
No key CLI flag, credential file or environment dump.

A live run must be a fresh offline plan, not a converted MOCK run. `approved-by`
is an operator assertion, not authentication; enforce designated ownership outside
this local tool. `approval-id` must identify the separate approved pilot/spend
record, never an invented token.

```bash
# DESIGNATED EXECUTOR ONLY, after approval; NOT an offline verification command:
"$PY" "$SKILL/scripts/storyboard.py" generate --run "$RUN" --live \
  --approved-by AUTHORIZED_EXECUTOR --approval-id ACTUAL_APPROVAL_RECORD --accept-cost \
  --budget-dir /absolute/path/to/shared-LIVE-budget
```

Stop after the initial **small approved sample** (maximum three illustrations).
Each attempt conservatively reserves US$2.031616; US$5 can admit **two**, not three.
Do not lower the reserve or quietly change the approved selection to fit a budget. A human must open the real stored
images and inspect the look, then explicitly record their decision:

```bash
"$PY" "$SKILL/scripts/storyboard.py" review --run "$RUN" \
  --reviewer 'Actual human name' --decision approve \
  --notes 'Actual findings from inspecting these exact images' \
  --human-look-confirmed
```

Do not run this command on a human's behalf without their actual review.
Mock/dry/incomplete/refused evidence cannot be reviewed into live approval.
For expansion, make a **new run ID**, choose `sampling.stage: expansion`, and
set `sampling.review_path` to the absolute sample `review.json` path. Keep the
same direction revision, shot inventory, reference declarations and config;
only change selection/run ID/sampling/budget/approval metadata. Changed look
scope needs a new small sample and real human review. Every live expansion still
needs separate explicit spend authorization and uses the same shared budget.

## Interruption and revision rules

- SDK retry attempts = **1 total attempt**. Timeout/transport/crash means unknown
  usage, retained reserve, and stop. Never assume a timeout means no charge.
- `generate ... --resume` skips **all attempted** shots, including unknown ones.
  It only submits unattempted work, with the identical mode, approval and budget
  binding. It is not a retry switch.
- Only a recorded transient HTTP response (429/500/502/503/504) permits a manual
  `--retry-attempt ATTEMPT_ID --allow-transient-retry` invocation with the original
  flags. It reserves again, never overwrites, and cannot combine with `--resume`.
- A new prompt/revision/reference requires a new run ID and resupplied reference
  bytes in one single turn. Never overwrite an existing namespace or board.
- Shared reserves are never automatically released, even on failure. Preserve
  the entire budget directory and run directories. Do not split/reset budgets
  to bypass a cap. Corrupt/partial journals require human reconciliation.

Read the contract's trust and durability limitations before any approved pilot.
Inspect actual sample images for style/identity, shot readability, anatomy/artifacts
and story beat, then present originals and shot-labelled cards in **lavish** when
available. Technical decoding or mock imagery is not the human look verdict.
Keep integration in the caller's workflow; do not duplicate this implementation.
