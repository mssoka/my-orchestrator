# Field notes shard — righttenantry-refcheck-local-test (2026-08-14)

- Referee form renders ALL question forms stacked in the DOM (one visible): unscoped `[data-testid=reference-continue]` clicks silently re-submit the FIRST (identity) form forever — scope every click/fill to `[data-question][data-current="true"]`, and treat "page didn't advance" as a selector bug before a server bug.
- Refcheck + apply POSTs are timing-gated (floor 500ms/2s, stale-cap): sleep ≥2-3s AFTER the page renders BEFORE submitting; a rejected submission leaves the page's `_form_loaded_at` stale, so reload fresh instead of retrying.
- Local RT sandbox: :4000 may be sibling-owned (run :4100 via a gitignored `server/.env` copy, blanking Resend/Twilio/AI); `seed-refcheck-fixture.py` must resolve applications by the submit's own unique email — "latest application" queries race parallel jobs; the global sweep claims ALL due rows, so `--no-sweep` fixtures get swept mid-test by sibling runs.
