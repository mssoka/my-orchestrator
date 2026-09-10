---
title: 'Reusable Gemini storyboard skill'
type: 'feature'
created: '2026-09-10'
status: 'in-review'
baseline_commit: '54164326422a736c41bff1429a83002401e378a8'
route: 'dispatch'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Future videos need reference-conditioned storyboard targets without reusing another film's identity, starting existing production, or accidentally spending money during preparation.

**Approach:** One portable skill and Python CLI consumes an explicit video/style/reference/shot manifest, plans offline, and separately supports budgeted single-turn Gemini image requests. Film direction is entirely input data. Images are look targets, never animation/native-production proof.

## Boundaries & Constraints

**Always:** Pin `gemini-3.1-flash-image`. Require approved direction, explicit shot eligibility, selected reference provenance and external-use permission. Preserve prompt/reference/output hashes, revisions, unknown usage and attempts. Require a small initial sample and actual human look approval before expansion. Use official SDK shapes verified offline. Initial implementation and all tests are offline; only pNS may execute the separately approved shared pilot. Follow generated BMAD workflow/review layers. Communicate interface via Silas only.

**Never:** Read keys or startup files during this job; make Gemini calls, probe auth/quota, upload references, edit live root/channel/native files, duplicate implementation, infer audio timing, hard-code film identity, silently retry timeouts, overwrite boards, merge PRs, or claim a live pilot passed.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Plan | Complete manifest; no key | Prompts, selected/excluded shots, hashes, config, cost caveats, no transport | Useful validation errors |
| Eligibility | Selected started/unknown/missing status | No request/output board | Fail closed |
| References | Missing ID/file, malformed image/MIME, no cloud permission | No submission | Fail closed before client creation |
| Success | Mock SDK response with thought and final image | Decode/preserve only final image; shot card says MOCK | Refusal/no image never success |
| Interruption | Timeout, transport failure, crash after reservation | Attempt retained, usage unknown, conservative reserve retained | No implicit retry; stop |
| Resume/revision | Same run or revised manifest | Resume only unattempted work; revision needs new run ID | Immutable inputs and outputs |
| Expansion | No approved real sample review | No wider live run | Reject mock/dry approval evidence |

</frozen-after-approval>

## Code Map

- `.agents/skills/hf-generate/` and `comfy-run/`: packaging precedent only; do not modify or reuse transport/auth.
- `.agents/skills/gemini-storyboard/`: new isolated package; no application registration needed. Pi discovers nested SKILL.md from trusted project/global skill directories.
- `docs/orchestration-playbook.md` Minion standing orders: internal spec approvals pre-approved, prescribed independent review required.
- `.scratch/bmad-binding/`: ignored recovery evidence, canonical reverse-equality hashes and one successful render; exclude from PR.
- Official Google docs: image generation supports 14 ratios and 512/1K/2K/4K; model limits 131072 input/32768 output. Pricing checked 2026-09-10: standard input $0.50/M, text/thought $3/M, image $60/M. No free image tier.
- Installed `google-genai==2.22.0`: GenerateContentConfig(response_modalities, image_config), Part.from_bytes; HttpOptions timeout milliseconds, HttpRetryOptions(attempts=1). No response_format field. Pillow verifies bytes/MIME. Tests intercept SDK boundary, never transport.

## Tasks & Acceptance

**Execution:**
- [x] `.agents/skills/gemini-storyboard/scripts/storyboard.py` — implement strict manifest validation, deterministic planning, SDK request builder, conservative budget/attempt journal, single-turn response extraction, immutable run/review records and HTML cards — portable one-helper interface.
- [x] `.agents/skills/gemini-storyboard/templates/video.json` — document required input fields without film-specific defaults; optional start/end frames and explicitly unknown timing.
- [x] `.agents/skills/gemini-storyboard/tests/` — create two contrasting synthetic manifests/references; mock SDK responses and assert all matrix failures, namespace/conditioning, budget/retry/resume and negative/mutation legs.
- [x] `.agents/skills/gemini-storyboard/SKILL.md`, `references/contract.md`, `references/sdk-pricing.md`, `requirements.txt` — document setup, cwd-independent paths, explicit live action, sample/look gate, cost uncertainty, retries, credential safety and SDK pin.
- [x] `_bmad-output/implementation-artifacts/gemini-storyboard-interface.md` — write stable CLI/schema/path/readiness handoff; relay through Silas without edits to channel repository.
- [x] `.agents/skills/gemini-storyboard/references/offline-verification.md` — preserve exact commands/counts/SDK evidence and review limitations after verification.

**Acceptance Criteria:**
- Given contrasting synthetic projects, when planned with the same executable, then every supplied style/story field reaches actual request contents, selected images become SDK byte parts, and namespaces/ref hashes differ without shared state.
- Given any required direction/ref/status/config omission, when validated, then no transport is invoked and a named validation error is returned.
- Given offline mock response/error cases, when executed, then final/thought/refusal/malformed/usage/error distinctions and immutable receipts match the matrix and all money/attempt bounds hold.
- Given a fresh agent in another cwd, when following SKILL.md and template, then all links/commands resolve and offline verification requires neither keys nor network.
- Given the focused PR, when reviewed, then it contains only the generic package and job-owned evidence, carries prescribed review results, and discloses no real image/aesthetic/live acceptance.

## Implementation Notes

- Implemented one isolated helper with manifest v1, explicit plan/generate/review, POSIX locks, immutable snapshots/receipts and shared conservative reservations. No live/channel/native/root changes.
- Offline verification after review round 1: 151 tests passed; 13/13 behavioral guard mutations killed (earlier 112/10 and 139/12 counts superseded); canonical/recovery hashes and reverse-equality checks unchanged (16/16). Exact evidence and limitations are in [offline verification](../../.agents/skills/gemini-storyboard/references/offline-verification.md).
- [Interface handoff](gemini-storyboard-interface.md) relayed through Silas only. No live pilot, actual human look approval or aesthetic acceptance claimed.
- Implementation handoff is ready for the parent generated BMAD independent review layers. Review round 1 (three glm-5.3 xhigh layers) completed and triaged; all patch-routed findings applied, rejections documented in the Review Triage Log.

- Parent acceptance audit corrected explicit GOOGLE_AI_API_KEY mapping, required style/story/reference roles, generic executor identity, optional start/end illustration labels, safety/modality receipts and dry cards. Revised 139-test suite and 12/12 mutations pass. Published no live claim. The helper's fixed reserve remains US$2.031616; authorized two-shot selection and exact outside-repo namespaces are isolated in the job handoff, not runtime defaults.

## Review Triage Log

Layers: blind-hunter, edge-case-hunter, verification-gap (glm-5.3 xhigh; parent flipped from Codex by usage cap, glm fallback window). Every finding verified against the tree; two-layer conflicts re-verified by direct recomputation.

| # | Finding (layer) | Verdict | Evidence / route |
|---|---|---|---|
| 1 | Manifest `requirements.txt` hash wrong (blind) | false | Recomputed `shasum -a 256`: `994ef162…47dd32` matches the manifest byte-for-byte; verification-gap independently confirmed all 13 entries. |
| 2 | Package manifest hand-maintained, can rot (blind) | low | Real maintenance risk on a job-owned evidence file. patch: regenerate from final tree; document the regeneration snippet. |
| 3 | Verification paths recreate a deleted budget dir (blind) | low | `lock()`+`journal()` would fabricate policy/journal; gate still fails closed ("sample not complete" / "local attempts missing"), but the side effect and misleading error are real. patch: existence pre-check in `evidence()`. |
| 4 | Mid-run cap exhaustion loses printed receipts, exit 2 (blind, edge) | low → reject | Receipts stay durable on disk with cards; cap is only reachable when selection exceeds affordable attempts — the documented pilot config (2 selected, 2 attempts) never hits it; `--resume` is the documented recovery. A contract reshape fails the trivial-fix bar for an edge not met in everyday use. |
| 5 | `httpx` imported in error path, undeclared (blind) | low | Transitive today; a future SDK change would break failure classification. patch: pin `httpx==0.28.1`. |
| 6 | Non-`StoryboardError` exceptions escape as tracebacks (blind) | low | Missing-dependency ImportError gives an opaque traceback. patch: friendly exit 2 for ImportError; genuinely unexpected crashes stay loud. |
| 7 | Run-tree doc inventories disagree (blind) | low | contract.md lacks `plan.html`; interface listing lacks `seal.json`/`execution.json`/`reservation.json`/`review.json`. patch: complete both listings. |
| 8 | Journal rows parsed loosely: duplicate keys, `1.0`/`True` sequence, extra fields (blind, edge) | low | Tool-written rows make this unlikely, but strictness is a direct correction consistent with the manifest posture. patch: strict key-set + `type(...) is int` sequence. |
| 9 | Retry semantics under-documented/under-tested (blind) | low | Retry processes only the retried shot; bare `--allow-transient-retry` rejection untested. patch: contract sentence + two cheap tests. |
| 10 | `illustration: start/end` pairing unenforced; lone start accepted; no transformation state required (blind, edge) | low (partial) | patch: require `direction.transformation` when `illustration != single` (edge-hunter's version). Cross-shot pairing enforcement rejected: operator naming discipline is documented; pairing machinery would over-constrain creative labeling with no demonstrated failure. |
| 11 | Missing `GOOGLE_AI_API_KEY` detected only after reservation; mislabeled `transport_error` (blind) | medium | Verified: `create_client()` runs inside the per-attempt try, so an absent key burns US$2.031616 and mislabels the receipt; `test_no_sdk_credential_fallback` codified the misbehavior. patch: pre-flight key-presence check before any reservation; test updated to expect `credentials` error, zero client calls, zero reservations. |
| 12 | `--mock` silently accepts live-only approval flags (blind) | low | Mock `execution.json` records meaningless approval values. patch: reject approval/accept-cost flags in mock mode. |
| 13 | Outside-repository rule unenforced; path strictness inconsistent (blind) | false | Repo-boundary enforcement is an operator/namespace duty by the documented trust model (handoff fixes the approved outside-repo namespaces); generic git detection would add false surface. Relative `--output-root` resolves deterministically; exclusivity is absolute-path based. `--budget-dir` absoluteness is deliberate (cross-cwd shared state). |
| 14 | Reference `path` traversal/symlinks uncontained (blind) | false | The manifest is operator-authored trusted input — the tool already runs with the operator's full privileges; contract.md documents the trust limits ("not a tamper-proof approval authority", adversarial-symlink warning). No privilege boundary is crossed. |
| 15 | Stale spec counts "112 tests / 10 mutations" vs 139/12 (blind, verification-gap) | low | Confirmed stale line in Implementation Notes. patch: correct to the parent-corrected counts. |
| 16 | Machine-specific absolute paths in tracked `_bmad-output` artifacts (blind) | false | The interface handoff's absolute paths ARE the requested deliverable (exact interpreter/namespaces for pNS); portability AC targets the package, which is cwd-independent (cross-cwd test, manifest-relative reference resolution). |
| 17 | `BLOCKED_REASON_UNSPECIFIED` block evidence lost (edge) | false | UNSPECIFIED means not blocked; the response proceeds to normal candidate handling. Genuine blocks carry real values and are recorded. |
| 18 | Safety-adjacent finish reasons (`LANGUAGE`/`SPII`/`IMAGE_OTHER`/`IMAGE_RECITATION`) mislabeled incomplete (edge) | low | Verified against the installed enum (closed set). patch: added to the refusal set; `MAX_TOKENS`/`MALFORMED_FUNCTION_CALL`/`OTHER`/`NO_IMAGE`/tool-call reasons stay incomplete. |
| 19 | RecursionError on deeply nested manifest JSON (edge) | low | Real escape from `read_json`. patch: add `RecursionError` to the handled tuple. |
| 20 | NaN/Infinity usage crashes receipt serialization (edge) | false | Verified: pydantic rejects non-finite numbers in the typed int fields (`Input should be a finite number`), so NaN usage is unreachable through the SDK boundary. |
| 21 | Typo'd `--run` creates stray directory + `.lock` (edge) | low | `lock(run)` mkdirs before `load_run` fails. patch: `manifest.json` existence pre-check in `generate`/`review_run`. |
| 22 | Exit status 1 never verified; `return 0` mutation survives (verification-gap, pre-verified) | patch (filed) | Gap layer read all tests and grepped `returncode`; filed disposition accepted per workflow. patch: main-level exit-code assertions (1 on non-success receipt, 0 on success). |
| 23 | Template's deliberate validation failure unpinned (verification-gap, pre-verified) | patch (filed) | No test loads the shipped template; the fail-closed onboarding property is the safety contract. patch: `validate(read_json(template))` must raise. |
| 24 | Budget-dir absolute guard untested (verification-gap, pre-verified) | patch (filed) | Filed evidence accepted. patch: one-line rejection test. |
| 25 | 19 MiB request gate untested (verification-gap, pre-verified) | patch (filed) | Only offline protection against server-rejected oversized requests. patch: noise-PNG oversized-request plan test. |
| 26 | Gap-layer screening notes (docs static, greenfield scope) | note-only | No defect filed. |

Grouping: highest verdict medium (#11); all survivors route **patch** (direct corrections, no public surface added beyond two rejection guards); no intent_gap/bad_spec; no loopback. Rejections carry their refutations above.

## Spec Change Log

## Review Triage Log

## Design Notes

Use explicit `plan`, `generate`, and `review` commands. A run is namespaced by video ID/run ID and immutable manifest hash; exclusive creation prevents collision. A shared budget directory with an exclusive lock and append-only attempt reservations counts every attempt across runs, including unknown interruptions. Never release reserves automatically; this is deliberately conservative, not an actual bill. SDK retries disabled; manual retry only for a recorded transient response with explicit permission, not timeout. No chat history/thought-signature handling: revisions resupply selected image references in a new single turn. HTML cards link exact stored bytes with escaped manifest text and label mocks clearly.

## Verification

**Commands:**
- `.scratch/gemini-venv/bin/python -m pytest .agents/skills/gemini-storyboard/tests -q` — all tests pass with network traps.
- `.scratch/gemini-venv/bin/python .agents/skills/gemini-storyboard/tests/mutations.py` — each guard mutation fails its targeted offline test, pristine suite remains green.
- Cross-cwd CLI help/plan with no key and transport denied — succeeds; live without positive approval/budget fails before transport.
- `git diff --check` — no whitespace defects; canonical recovery source hashes unchanged.
