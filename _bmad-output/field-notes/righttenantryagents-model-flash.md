# righttenantryagents-model-flash — field notes

- Briefing forensics can be STALE relative to merged work — this job's
  briefing said `config.py` default was still `gemini-3.5-flash`, but PR
  #164 had already moved `config.py` + the default-tier Terraform vars to
  `gemini-3.6-flash`. The real delta was only the 5 Pro-tier vars. Always
  `grep` disk for the current model strings before trusting a briefing's
  "current state" (ground-truth-first); also sweep `deployment/README.md`
  + `.env.example` — both carried the old tier and would've shipped stale.
- Isolated single-agent judge checks are fast BUT get confounded when the
  agent carries a `web_search` (Brave) tool and the dev env has no
  `BRAVE_API_KEY`: `consistency_checker` on Flash retried the failing
  tool in a slow loop while Pro tried once and moved on — a dev-env
  artifact, not a model-quality signal (prod has Brave). For judge
  sanity-checks, confirm Brave is present or pick a tool-free path.
- Don't attempt inline full-pipeline eval head-to-heads: each evalset case
  ran >10 min (anonymizer slow-mode + multi-agent) and the repo's own
  strategy routes full evals to **staging deploy** for that reason. The
  non-streaming Runner path works; the `StreamingMode.SSE` path hits an
  `httpx` `readline(max_line_length=...)` version mismatch in this venv —
  use default `run_config` (non-streaming).
