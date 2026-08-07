# Briefing: righttenantry-gcp-cost-analysis

- **Repo:** orchestrator root (`/Users/moses/code`) — this is an analysis/viz task, not a repo deliverable. Work in the orchestrator root; no PR needed (output is a lavish HTML artifact + a markdown analysis).
- **Workflow:** lavish skill (render the analysis as a rich, reviewable HTML dashboard). Use Python to parse the CSVs; build the viz via lavish.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (analysis/viz deliverable, not code).

## ⚠️ AMENDMENT (from Gru, pre-dispatch — reshapes the analysis; do not lose the original MoM-by-service ask, ADD these on top)

1. **SPLIT ALL COSTS BY PROJECT — this is the KEY INSIGHT.** The Gemini API + any Veo costs are **BLENDED**: they include BOTH RT-agent usage AND the user's **personal YouTube channel** work (image generation via Gemini, video generation via Veo). The monthly cost tables have a **PROJECT** column in their line items. Group by project to separate: **RT business** (`righttenantry`, `righttenantry-staging`) vs **personal YouTube content** (whatever project the image/video gen runs under — possibly `iginsider` or a `gen-lang-client-*` project). The user needs to know **how much is business vs personal**.
2. **Retry-fix context (already done — do NOT re-recommend).** The RT agent retry logic was **ALREADY fixed recently** (fail-fast on compliance-judge issues, no indefinite retries). So retry-related Vertex AI waste is addressed going forward. In the monthly trend, **check whether the LLM cost spike was BEFORE that fix** — if so, that confirms retries were the driver. Note the fix as **"already done"** in the recommendations (don't recommend it again).
3. **ULTIMATE GOAL = COST SAVINGS.** Frame the entire dashboard + recommendations around **WHERE TO CUT**. Two distinct buckets the user cares about:
   - **(a) RT business cost** — compute right-sizing, LLM efficiency, the agents service.
   - **(b) YouTube content cost** — cheaper alternatives to Gemini image gen + Veo video gen; flag the spend so the user can decide on alternatives.
   Make the savings recommendations **concrete and ranked by € impact**.
4. **FURTHER CLARIFICATION (Gru, in-flight): the Gemini API cost is TRIPLE-BLENDED**, not just YouTube. It is (1) **RT Facebook ad creative generation** (business), (2) **RT agent usage** (business), AND (3) **personal YouTube content**. So the project split cleanly separates **personal-YouTube from RT-business**, BUT **FB-ads + agents WITHIN the righttenantry project stay blended** — billing data can't split use-cases within a single project. **Note this limitation explicitly in the dashboard**: the Gemini figure is a mix of ad creative + agents + personal, and only the *project boundary* (personal vs business) is cleanly separable. Flag that deeper use-case attribution (FB-ads vs agents) would need the user's own usage logs.

---

## Mission

The user received a large GCP bill for the RT-Solarity billing account (€1,358.17 pre-tax, Jan–Aug 2026). He wants a **month-over-month cost breakdown by service** — a trend view showing how each service's cost is moving — presented as a **lavish HTML dashboard**. He also wants the cost drivers diagnosed (WHY is it expensive, and what to do about it).

This is NOT a code change. The deliverable is understanding: a clear, visual month-over-month breakdown + a cost-driver diagnosis + actionable recommendations.

## The data (6 CSVs already staged at `/Users/moses/code/_bmad-output/billing/`)

| File | What it is | Structure |
|---|---|---|
| `reports-jan-aug-2026-by-service.csv` | Jan–Aug aggregate, grouped by **Service** | Flat CSV: Service description, Service ID, List cost (€), Subtotal (€), % change. **This is the cleanest service breakdown.** |
| `cost-table-2026-04.csv` | **April** invoice cost table (detailed line items) | Invoice format: header rows (Invoice number/date/due date) THEN a line-item table (Service, Description/SKU, Quantity, Cost). ~19910 bytes. **Parse past the header rows.** |
| `cost-table-2026-05.csv` | **May** invoice cost table | Same invoice format. ~28KB (biggest month — flag this). |
| `cost-table-2026-06.csv` | **June** invoice cost table | Same format. ~25KB. |
| `cost-table-2026-07.csv` | **July** invoice cost table | Same format. ~18KB. |
| `breakdown-jan-jul-2026-summary.csv` | Jan–Jul high-level summary | Single row: Usage cost, discounts, subtotal, tax (€302.61), total **€1,618.32 incl. tax**. Use for reconciliation only. |

### Parsing guidance
- The 4 monthly cost tables are **invoice-format** (not flat CSV). They start with metadata rows (`Invoice number`, `Invoice date`, `Due date`), then a line-item section. **Inspect each file's structure first** (read the raw content) to find where the per-SKU line items begin. Group line items by Service to get per-month-per-service costs.
- The Reports CSV is already grouped by service over Jan–Aug — use it as the authoritative service breakdown and to validate your monthly aggregation.
- Reconcile totals: Reports CSV (Jan–Aug, pre-tax €1,358.17) vs the monthly tables (Apr–Jul) vs the breakdown (Jan–Jul, €1,315.71 pre-tax / €1,618.32 incl tax). Note any discrepancies.
- Currency: **EUR (€)** throughout.

## What the user already knows (Gru's preliminary read — verify + expand, don't contradict without evidence)

The aggregate breakdown (Jan–Aug):
- 🤖 **LLM/AI (Vertex AI + Gemini API): €744.15 = 54.8%** — the agents' API calls
- 🖥️ **Cloud Run: €583.62 = 43.0%** — always-on compute (both services, min-instances 1)
- 🔧 Everything else: €30.40 = 2.2%

The likely cost driver: the **`right-tenantry-agents`** Cloud Run service (ADK reference-check + compliance agents) — it's BOTH the Vertex AI / Gemini LLM calls AND an always-on instance (min 1, max 20, concurrency 20, up since Jul 22). Verify against the monthly data: is the LLM cost concentrated in the months after the agents went live? Is Cloud Run steady or growing?

## The lavish dashboard (what to build)

A single rich HTML dashboard the user can review in-browser. Include:

### 1. Headline summary
- Total cost (Jan–Aug), pre-tax + the tax/total from the breakdown.
- The headline insight in one sentence (e.g. "55% of the bill is LLM API calls from the agents service").

### 2. Month-over-month trend (the core ask)
- A **monthly total cost** trend (Apr–Jul at minimum; if you can derive Jan–Mar from the breakdown/reports, include them).
- A **per-service monthly breakdown** — stacked or grouped, showing how Cloud Run, Vertex AI, Gemini API, and others move month-to-month. The user wants to SEE which service is growing vs steady.
- Highlight any **spike month** (May is the biggest file — investigate why).

### 3. Service breakdown (Jan–Aug aggregate)
- Table: Service | Cost (€) | % of total | bucket (LLM / Compute / Infra).
- Visual: donut or bar chart by service.

### 4. Cost-driver diagnosis
- Which service is the dominant cost? Is it growing or stable month-over-month?
- Tie it back to the architecture: Cloud Run compute = the two always-on services (righttenantry app + right-tenantry-agents); Vertex AI + Gemini = the agents' LLM calls (reference checks, compliance runs, retries — note RT-PROD-C in Sentry showed AiAnalysisRetryExhausted = retries = extra LLM cost).
- Is the cost proportional to usage (applications processed) or fixed (always-on)? This determines the fix.

### 5. Recommendations (actionable, ranked by savings)
Likely candidates (validate against data, rank by € impact):
- **Scale the agents service to zero** when idle (min-instances 1 → 0) — kills idle compute. Trade-off: cold-start latency on first request.
- **Reduce LLM call volume** — the reference-check/compliance agents may be over-calling or retrying (the COMPLIANCE_VIOLATION retries = wasted spend). Audit the retry logic + prompt efficiency.
- **Cheaper model tier** — if the agents use an expensive Gemini/Vertex model for tasks a cheaper one handles, switch.
- **Right-size Cloud Run** — the main app (512Mi/1 CPU) may be over-provisioned for its traffic.
- **Disable Container Registry Vulnerability Scanning** (€13.23) if not needed.

## Deliverables

1. **Lavish HTML dashboard** rendered via the lavish skill — the primary deliverable. Post the review URL.
2. **Markdown analysis** at `_bmad-output/billing/rt-gcp-cost-analysis-2026-08.md` — the written breakdown, findings, recommendations (the source content the lavish renders).
3. **The parsing script** at `_bmad-output/billing/parse_costs.py` (so the analysis is reproducible when next month's bill arrives).

## Constraints

- Do NOT make any GCP changes (no scaling, no disabling services) — this is analysis only. Recommendations go in the report; the user decides.
- Do NOT enable BigQuery billing export or touch any billing config without explicit instruction.
- All figures in EUR. Be precise (cite the exact CSV numbers).
- If a month's data can't be parsed cleanly, say so — don't fabricate.

## Review loop (lavish — the deliverable IS the lavish)

The dashboard itself is the lavish artifact. Post the review URL. Do NOT open a PR (this is analysis, not code). Badge out + self-report when the lavish is posted and the markdown analysis is written.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-gcp-cost-analysis working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note righttenantry-gcp-cost-analysis "lavish dashboard posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set righttenantry-gcp-cost-analysis done "analysis complete: <paths>"` when finished
- `herdr notification show "gcp-cost-analysis" --body "<one-line>"` on finish
- Final message: summary, lavish URL, the headline finding (biggest cost driver + MoM trend direction), top recommendation.

## Dispatch parameters

- repo: orchestrator (root)
- repo_root: /Users/moses/code
- slug: righttenantry-gcp-cost-analysis
- base: main (no PR expected)
