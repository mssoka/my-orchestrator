# RT-Solarity GCP cost analysis — Jan–Aug 2026

**Billing account:** RT-Solarity (010FC8-663B-2D-2AE43C) · **Currency:** EUR · **Sources:** six CSVs in `_bmad-output/billing/` · **Reproducible:** `python3 _bmad-output/billing/parse_costs.py` → `costs.json` · **Dashboard:** `rt-gcp-cost-dashboard.html` (lavish review)

> Per the brief: every cost is **grouped by GCP project**; the retry-fix is already done (not re-recommended); everything is framed around **cost savings**.
> **Amendment (use-case attribution):** the `iginsider` project's Gemini API is a **triple-blended bucket** — RT Facebook-ad creative (business) + RT agent usage (business) + personal YouTube. GCP bills project + service + SKU, not which app made a call, so **only the project boundary is cleanly separable**. Splitting the blended bucket needs your own usage logs. Analysis only — **no GCP changes were made.**

---

## 1. Headline

- **Total Jan–Aug: €1,358.17 pre-tax** (+ €302.61 tax Jan–Jul = **€1,618.32** total).
- **≥85.9% is cleanly RT business: €1,166.74** (all under the `righttenantry` projects).
- The remaining **€191.44 (14.1%)** is the **blended Gemini API bucket** (FB ads + agents + YouTube) — not cleanly attributable.
- The two clean-business drivers are **Cloud Run €583.62 (43.0%)** and **Vertex AI €552.71 (40.7%)** — together **83.7%** of the bill.
- **Agents' LLM cost is already falling** — Vertex AI went €250.92 (May) → €43.27 (Jul), **−83%**, confirming the retry-fix is working.
- **Cloud Run is now the #1 lever**: fixed/always-on, *growing* (€70.59 → €144.16/mo), not proportional to usage.

## 2. Clean business vs blended Gemini API

The agents' LLM calls all bill under `righttenantry`(/staging) as **Vertex AI** — clean business. The **Gemini API** service all bills under `iginsider`, a shared project serving FB-ad creative + agents + YouTube, so it's blended.

| Bucket | Project(s) | Jan–Aug pre-tax | Share | What it is |
|---|---|---:|---:|---|
| **Clean business** | `righttenantry` + `-staging` | €1,166.74 | **≥85.9%** | Cloud Run compute + agents Vertex AI LLM + infra |
| **Blended** | `iginsider` (Gemini API) | €191.44 | 14.1% | FB-ad creative + agents + YouTube — **not separable from billing** |
| **Total** | | **€1,358.17** | 100% | |

> **Limitation:** the true business share is **higher than 85.9%** — it is that floor plus the FB-ads and agents portions of the blended bucket. Pinning it needs per-call usage logs.

### Monthly split (pre-tax)

| Month | Clean business | Blended (Gemini API) | Total pre-tax | + tax | invoice total |
|---|---:|---:|---:|---:|---:|
| Apr | 225.26 | 32.90 | 258.16 | 59.38 | 317.54 |
| May | 450.97 | 25.70 | 476.67 | 109.64 | 586.35 |
| Jun | 255.43 | 99.90 | 355.33 | 81.74 | 437.07 |
| Jul | 192.57 | 32.94 | 225.51 | 51.86 | 277.36 |
| **Apr–Jul** | **1,124.23** | **191.44** | **1,315.67** | **302.62** | **1,618.29** |

June's blended jump (€99.90) was dominated by Veo video generation.

## 3. Month-over-month by service (core ask)

| Service (pre-tax €) | Apr | May | Jun | Jul | Jan–Aug | % | bucket |
|---|---:|---:|---:|---:|---:|---:|---|
| Cloud Run | 70.59 | 189.98 | 137.10 | 144.16 | **583.62** | 43.0% | business |
| Vertex AI | 145.55 | **250.92** | 112.96 | 43.27 | **552.71** | 40.7% | business |
| Gemini API | 32.90 | 25.70 | 99.90 | 32.94 | **191.44** | 14.1% | **blended** |
| Container Registry Vuln Scanning | 7.89 | 5.34 | 0.00 | 0.00 | 13.23 | 1.0% | business |
| Artifact Registry | 0.52 | 3.14 | 4.01 | 3.78 | 12.09 | 0.9% | business |
| Secret Manager · Dataplex · other | 0.71 | 1.59 | 1.36 | 1.36 | 5.08 | 0.4% | business |

**Trend read:** Vertex AI spikes in May then declines steeply (the retry-fix). Cloud Run is steady-to-growing (the always-on baseline that doesn't move with traffic).

## 4. By project — agents migrated to prod, staging wound down

| Project (pre-tax €) | Apr | May | Jun | Jul | Apr–Jul | bucket |
|---|---:|---:|---:|---:|---:|---|
| `righttenantry` (prod) | 46.42 | 178.55 | 191.03 | 188.68 | 604.68 | business |
| `righttenantry-staging` | 178.84 | 272.42 | 64.40 | 3.89 | 519.55 | business |
| `iginsider` (Gemini API) | 32.90 | 25.70 | 99.90 | 32.94 | 191.44 | **blended** |

## 5. Cost-driver diagnosis

- **Cloud Run — fixed, always-on, growing.** Min-instances keeps instances warm 24/7 regardless of traffic. CPU instance-billing dominates (July: €126.65 CPU + €21.10 memory). Not proportional to applications processed → mostly idle compute. *Caveat: billing CSVs don't split Cloud Run by service name.*
- **Vertex AI — variable, per-call.** Agents' Gemini LLM. €250.92 May spike → €112.96 → €43.27. **Retry-fix confirmed working.** Remaining lever: heavy use of **Gemini Pro** (≈5–10× Flash); caching already in use. *(A slice of the blended Gemini API bucket is also agent usage → total agents-LLM = Vertex €552.71 + unknown part of Gemini €191.44.)*
- **Gemini API — blended, unattributable.** Veo video gen €153.81 (€0.345/s, likely YouTube) + Gemini image gen €37.63 (FB-creative or thumbnails).

### Gemini API deep-dive (by SKU; use-case not separable)

| Component | Apr | May | Jun | Jul | total |
|---|---:|---:|---:|---:|---:|
| Veo video gen | 30.52 | 24.63 | 70.65 | 28.01 | **153.81** |
| Gemini image gen | 2.38 | 1.07 | 29.25 | 4.93 | **37.63** |

**Veo SKU pricing (from your own June usage):**

| Veo tier | €/sec | €/min | vs 720p Fast |
|---|---:|---:|---:|
| Generation 1080p (standard) | 0.345 | 20.7 | **4.0×** |
| Fast Generation 1080p | 0.103 | 6.2 | 1.2× |
| Fast Generation 720p | 0.086 | 5.2 | baseline |

~408s generated, almost all at 1080p-standard. At 720p-Fast pricing that volume would be ~€35 instead of ~€141 — a **~75% cut** on the Veo line, regardless of which use-case drove it.

## 6. Recommendations — ranked by € impact

### (a) Business — RT (cleanly attributable)

| # | Action | Est. €/mo | €/yr | Confidence | Trade-off / note |
|---|---|---:|---:|---|---|
| 1 | **Scale idle Cloud Run services to min-instances 0** (esp. agents) | **50–90** | ~600–1,100 | medium | Cold-start latency (~2–5s). CSVs don't split Cloud Run by service — confirm agents vs main-app in GCP metrics first. |
| 2 | **Prefer Gemini Flash over Pro** for routine agent steps | **20–60** | ~240–720 | medium | Where output quality tolerates Flash; keep Pro for the judge step. Caching already in use. |
| 3 | **Prune old Artifact Registry images** (storage growing) | **3–8** | ~40–100 | high | Quick win; set image-tag retention. |

### (b) Blended Gemini API bucket — pricing levers (use-case-agnostic)

| # | Action | Est. €/mo | Confidence | Note |
|---|---|---:|---|---|
| 4 | **Veo: 1080p-standard → 720p-Fast** (or 1080p-Fast); 75% cheaper/sec — applies for YouTube or FB-ad video | **22–52** | high | When actively generating. Alternatives: Runway/Pika/Kling free tiers, local models. |
| 5 | **Attribute the bucket via per-call tagging** (use-case label per call → logs) | enabler | high | No immediate €, but unlocks targeted cuts. Image-gen €37.63 is the most ambiguous (FB-creative vs thumbnails). |

### ✅ Already done — do not re-do

- **Agents retry-fix** (fail-fast on compliance-judge) — Vertex AI €250.92 → €43.27 (May→Jul, −83%). Working.
- **Container Registry Vulnerability Scanning** — €0 since June (was €13.23 Apr–May). Resolved.
- **Staging wind-down** — `righttenantry-staging` €272.42 → €3.89 (May→Jul); agents migrated to prod.

## 7. Run-rate

July (post-retry-fix baseline): **€225.51/mo pre-tax** (clean business €192.57 + blended €32.94) → **~€3.3k/yr** at current run-rate. Applying recs 1–2 could bring clean business to ~€120–150/mo.

## 8. Forward-looking instrumentation — BigQuery billing export (enabled on request)

To close the two attribution gaps, the user approved enabling BigQuery billing export. **Forward-only** — it captures from enablement; the Jan–Aug CSV history is not backfilled.

**Done from here (analysis minion, billing-admin on RT-Solarity):**
- Created dataset `righttenantry:billing_export` (EU multi-region), owned by `mssokabi@gmail.com` + projectOwners.

**You do (console-only — gcloud has no export command):**
1. GCP Console → **Billing** (RT-Solarity) → **Billing export**.
2. **Detailed usage cost** tab → *Edit settings* → Project `righttenantry`, Dataset `billing_export` → **Save**. (This resource-level export gives `resource.name` — gap #1.)
3. Optionally repeat on **Standard usage cost** for the daily export.

**After ~24h the tables appear** (`gcp_billing_export_resource_v1_010FC8_663B_2AE43C`, `gcp_billing_export_v1_010FC8_663B_2AE43C`); loads once/day.

**Attribution queries:**
```sql
-- Gap #1: Cloud Run by service (separates agents from main app, no app change)
SELECT resource.name, ROUND(SUM(cost),2) AS cost_eur
FROM `righttenantry.billing_export.gcp_billing_export_resource_v1_010FC8_663B_2AE43C`
WHERE service.description='Cloud Run' AND cost_type='regular'
GROUP BY 1 ORDER BY 2 DESC;

-- Gap #2: Gemini API by use-case  (REQUIRES apps to set a `use_case` label per call)
SELECT lbl.value AS use_case, ROUND(SUM(cost),2) AS cost_eur
FROM `righttenantry.billing_export.gcp_billing_export_resource_v1_010FC8_663B_2AE43C`,
     UNNEST(labels) AS lbl
WHERE service.description='Gemini API' AND lbl.key='use_case' AND cost_type='regular'
GROUP BY 1 ORDER BY 2 DESC;
```

**Gap #2 needs a code change:** the RT apps + YouTube workflow must tag every Gemini/Veo call with a `use_case` label (`fb_ads` | `agents` | `youtube`). Recommend a small minion task in the `righttenantry` repo for that — it's what makes the FB-ads/agents/YouTube split queryable. (Gap #1 is solved by export alone — `resource.name` names each Cloud Run service.)

## 9. Reconciliation, sources & caveats

- **Sources:** `reports-jan-aug-2026-by-service.csv` (aggregate), four `cost-table-2026-{04,05,06,07}.csv` invoice tables (parsed `Cost type=Usage` rows, summed net of spending-based discounts), `breakdown-jan-jul-2026-summary.csv` (totals). Parser `parse_costs.py` → `costs.json`.
- **Reconciliation:** Apr–Jul invoice totals (incl tax) = €1,618.29 ≈ breakdown Jan–Jul €1,618.32 (within €0.03 rounding) ⇒ the four invoices fully cover Jan–Jul (GCP bills in arrears; Jan–Mar negligible). Reports Jan–Aug €1,358.17 − breakdown Jan–Jul €1,315.71 ⇒ **Aug partial ≈ €42** (not yet invoiced).
- **Business/blended classification:** every Vertex-AI + Cloud-Run + infra line is under `righttenantry`(/staging) ⇒ €1,166.74 is **cleanly business**. The Gemini-API service (€191.44) is entirely under `iginsider`, a **shared project** serving FB-ad creative + agents + YouTube — **not separable** from billing. So "business ≥ 85.9%" is a floor, not an exact figure.
- **Caveats:** (1) Cloud Run not split by service name — agents-vs-main-app split needs GCP per-service metrics. (2) Gemini-API use-case split needs your own application logs. (3) August is partial. (4) Tax shown is Jan–Jul; the €42 Aug estimate is pre-tax only. (5) All usage net of GCP spending-based discounts.
