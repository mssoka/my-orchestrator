# SDK and pricing evidence

## Pinned, inspected offline

- `google-genai==2.22.0`, `Pillow==12.3.0`, `pytest==9.1.1`.
- `types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"],
  candidate_count=1, max_output_tokens=..., image_config=types.ImageConfig(
  aspect_ratio=..., image_size=...))`.
- `types.Content(role="user", parts=[types.Part.from_text(text=...),
  types.Part.from_bytes(data=bytes, mime_type="image/png"), ...])`.
- `genai.Client(api_key=os.environ["GOOGLE_AI_API_KEY"], vertexai=False,
  http_options=types.HttpOptions(timeout=TIMEOUT_MS,
  retry_options=types.HttpRetryOptions(attempts=1)))` (Gemini API, not implicit
  Vertex/ADC credential routing).
- `client.models.generate_content(model="gemini-3.1-flash-image",
  contents=[one_user_content], config=config)`; no chat, streaming, history,
  file-upload API, thought signatures, auth/quota probes or retry loop.
- `response_format` is **not** a `GenerateContentConfig` field. Response images
  arrive as `Part.inline_data.data` bytes through the SDK; no additional base64
  decode is applied. `Part.thought` distinguishes thought parts from finals.
- `GenerateContentResponse.usage_metadata.model_dump(mode="json",
  exclude_none=True)` preserves SDK usage fields, including thought counts and
  modality details if supplied. Missing counts are not invented.

Tests construct actual SDK types and intercept `genai.Client` and
`models.generate_content` at the SDK boundary. Network traps remain in force.
This proves local shapes and request content, **not server compatibility or
model availability**. Installed SDK inspection requires no client or key.

## Official reference basis (spec checked 2026-09-10)

- [Image generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Exact model](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image)
- [Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Official Python SDK](https://github.com/googleapis/python-genai)

The parent fetched the official image/pricing/model pages and queried the official
SDK README via Context7 `/googleapis/python-genai` on 2026-09-10. This public-doc
research and dependency installation used network; Gemini transport did not. The spec pins `gemini-3.1-flash-image`, fourteen
ratios and `512`/`1K`/`2K`/`4K`, 131072 input and 32768 output token ceilings.

Standard pricing at that check: input **$0.50/M**, text/thought output **$3/M**,
image output **$60/M**. **No free image tier.** Resolution and output content
change actual usage. Published output-only equivalents: 512 = 747 image tokens
(~$0.045), 1K = 1120 (~$0.067), 2K = 1680 (~$0.101), 4K = 2520 (~$0.151).
These exclude input/reference and text/thinking charges and are estimates, not a
bill. Actual billed dollars remain unknown; preserve usage for later reconciliation.

Every attempt reserves the entire input ceiling plus the entire output ceiling
priced at the higher image rate (including potential thought/text output):

```text
131072 × $0.50 / 1,000,000 + 32768 × $60 / 1,000,000
= $2.031616 reserved per attempt
```

This intentionally over-reserves, even if the configured output cap is lower.
The model's input ceiling bounds the reserve rather than an offline token-count
estimate; an oversized input may be rejected by the server and still consumes
an attempt. No token-count API is called. Provider ceilings/rates are assumptions,
not a contractual bill bound. Reconfirm prices and approvals outside preparation
if those assumptions change. Taxes, currency conversion, other clients and other
budget directories are not tracked.

Shared admission checks **both** cumulative reserves and cumulative attempt
count, under an exclusive lock. Success, refusal, transient error, timeout,
transport failure and unknown crash all retain the full reserve. A manual
transient retry reserves another full attempt. Policy is immutable and MOCK/LIVE
budgets are separate. Nothing auto-refunds based on usage; actual usage receipts
are evidence, not a billing reconciliation engine.
