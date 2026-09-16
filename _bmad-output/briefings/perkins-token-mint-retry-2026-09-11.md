# Tooling fix — perkins-token bounded mint retry

## Defect (issue-class, observed 2026-09-10)

`bin/perkins-token --owner <owner>` mint flaked ONCE at PR #22 r4 close (PP3D): silent EMPTY token → the round fell back to a plain comment (verdict preserved but the formal perkins-review trail lost). The SAME mint succeeded on a manual retry ~15 min later (formal APPROVED posted from the preserved verdict body). Signature: transient mint failure, no retry logic, silent fallback.

## Fix

In `bin/perkins-token`: add a bounded mint retry — 1–2 automatic retries with a short backoff (~30s, matching the proven manual-retry window) before the empty-token fallback fires. Log mint failures LOUDLY (stderr note per attempt: attempt n/N failed). The comment-fallback path stays as the LAST resort (it preserved the verdict — keep it).

## Bounds

- Touch ONLY `bin/perkins-token` (the retry/backoff/logging logic). No other tooling files.
- No behavior change to the SUCCESS path (same token format, same stdout-only discipline — stderr for the new attempt logging ONLY).
- glm-5.3 @ max. No OpenAI. No editor/GUI.
- pr_review=0 (Silas tooling, self-edit precedent); focused PR to main; user merges.
- VERIFY: shellcheck-level sanity + a dry syntax pass; do NOT hit the real mint endpoint repeatedly (one verification mint max, then report).
