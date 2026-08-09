#!/usr/bin/env python3
"""Parse GCP billing CSVs for the RT-Solarity billing account.

Reproducible cost analysis for the righttenantry-gcp-cost-analysis job.
Run:  python3 _bmad-output/billing/parse_costs.py
Writes: _bmad-output/billing/costs.json  (machine-readable, for the dashboard)
Prints: human-readable reconciliation + breakdown tables.

Amendment-aware: splits every cost BY PROJECT into
  - business (righttenantry + righttenantry-staging)
  - personal (iginsider  ->  Gemini image gen + Veo video gen)
and frames findings around COST SAVINGS.
"""

import csv
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))

# Project classification (Amendment point 1)
PERSONAL_PROJECTS = {"iginsider"}
BUSINESS_PROJECTS = {"righttenantry", "righttenantry-staging"}

# Monthly invoice cost tables (invoice-format CSVs)
MONTH_FILES = {
    "2026-04": "cost-table-2026-04.csv",
    "2026-05": "cost-table-2026-05.csv",
    "2026-06": "cost-table-2026-06.csv",
    "2026-07": "cost-table-2026-07.csv",
}

# Known totals for reconciliation
REPORTS_FILE = "reports-jan-aug-2026-by-service.csv"
BREAKDOWN_FILE = "breakdown-jan-jul-2026-summary.csv"
REPORTS_JAN_AUG_PRETAX = 1358.17
BREAKDOWN_JAN_JUL_PRETAX = 1315.71
BREAKDOWN_JAN_JUL_TOTAL = 1618.32  # incl tax


def bucket(project):
    if project in PERSONAL_PROJECTS:
        return "personal"
    if project in BUSINESS_PROJECTS:
        return "business"
    return "other"


def parse_invoice(path):
    """Parse a GCP invoice-format cost-table CSV.

    Returns (items, tax_by_project, total_row_cost).
    items: only 'Usage' cost-type rows -> net cost (incl negative discount rows).
    """
    with open(path, newline="", encoding="utf-8") as f:
        lines = f.read().splitlines()

    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("Billing account name,Billing account ID,Project name"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"No header row found in {path}")

    items = []
    tax_by_project = defaultdict(float)
    total_row_cost = None
    for r in csv.reader(lines[header_idx + 1:]):
        if len(r) < 18:
            continue
        project = r[2].strip()
        service = r[5].strip()
        sku = r[7].strip()
        credit_type = r[10].strip()
        cost_type = r[11].strip()
        cost_raw = r[17].strip().replace(",", "")
        try:
            cost = float(cost_raw)
        except ValueError:
            continue

        if cost_type == "Tax":
            tax_by_project[project] += cost
        elif cost_type == "Total":
            total_row_cost = cost
        elif cost_type == "Rounding error":
            pass
        elif cost_type == "Usage":
            amt_raw = r[14].strip().replace(",", "")
            try:
                usage_amount = float(amt_raw) if amt_raw else None
            except ValueError:
                usage_amount = None
            items.append({
                "project": project,
                "bucket": bucket(project),
                "service": service,
                "sku": sku,
                "credit_type": credit_type,
                "cost": cost,
                "usage_amount": usage_amount,
                "usage_unit": r[15].strip(),
                "usage_start": r[12].strip(),
                "usage_end": r[13].strip(),
            })
    return items, dict(tax_by_project), total_row_cost


def parse_reports(path):
    """reports-jan-aug-2026-by-service.csv -> {service: subtotal_eur}."""
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            svc = (row.get("Service description") or "").strip()
            sub = (row.get("Subtotal (€)") or "").strip()
            if not svc or not sub:
                continue
            try:
                out[svc] = float(sub)
            except ValueError:
                pass
    return out


def main():
    # ---- parse all months ----
    months = {}  # month -> {items, tax_by_project, total_incl_tax, pretax}
    for month, fname in MONTH_FILES.items():
        items, tax, total_incl_tax = parse_invoice(os.path.join(HERE, fname))
        pretax = round(sum(i["cost"] for i in items), 2)
        months[month] = {
            "items": items,
            "tax_by_project": tax,
            "total_incl_tax": total_incl_tax,
            "pretax": pretax,
        }

    reports = parse_reports(os.path.join(HERE, REPORTS_FILE))

    # ---- per month x project (pre-tax) ----
    by_month_project = {}  # month -> project -> pretax
    by_month_bucket = defaultdict(lambda: defaultdict(float))  # month -> bucket -> pretax
    for month, data in months.items():
        proj_sum = defaultdict(float)
        for it in data["items"]:
            proj_sum[it["project"]] += it["cost"]
            by_month_bucket[month][it["bucket"]] += it["cost"]
        by_month_project[month] = {p: round(v, 2) for p, v in proj_sum.items()}
        by_month_bucket[month] = {b: round(v, 2) for b, v in by_month_bucket[month].items()}

    # ---- per month x service (pre-tax) ----
    by_month_service = {}
    for month, data in months.items():
        svc_sum = defaultdict(float)
        for it in data["items"]:
            svc_sum[it["service"]] += it["cost"]
        by_month_service[month] = {s: round(v, 2) for s, v in svc_sum.items()}

    # ---- Veo (personal video) and image-gen spend ----
    veo_keywords = ("Veo",)
    img_keywords = ("Image Image", "Image Text", "image output token", "image input token",
                    "Generate_content image", "Generate_content text")
    veo_by_month = defaultdict(float)
    img_by_month = defaultdict(float)
    for month, data in months.items():
        for it in data["items"]:
            if it["project"] not in PERSONAL_PROJECTS:
                continue
            sku_l = it["sku"].lower()
            if any(k.lower() in sku_l for k in veo_keywords):
                veo_by_month[month] += it["cost"]
            elif any(k.lower() in sku_l for k in img_keywords):
                img_by_month[month] += it["cost"]

    # ---- Jan-Aug aggregate split (from reports: Gemini API = personal, rest = business) ----
    # Verified from invoices: Gemini API appears ONLY under iginsider (personal);
    # Vertex AI + Cloud Run + everything else appear ONLY under righttenantry(+/staging).
    jan_aug_personal = reports.get("Gemini API", 0.0)
    jan_aug_business = sum(v for k, v in reports.items() if k != "Gemini API")
    jan_aug_total = sum(reports.values())

    # ---- aggregate Apr-Jul per bucket + per project (from invoices, exact) ----
    apr_jul_bucket = defaultdict(float)
    apr_jul_project = defaultdict(float)
    apr_jul_service = defaultdict(float)
    for month, data in months.items():
        for it in data["items"]:
            apr_jul_bucket[it["bucket"]] += it["cost"]
            apr_jul_project[it["project"]] += it["cost"]
            apr_jul_service[it["service"]] += it["cost"]
    apr_jul_bucket = {k: round(v, 2) for k, v in apr_jul_bucket.items()}
    apr_jul_project = {k: round(v, 2) for k, v in apr_jul_project.items()}
    apr_jul_service = {k: round(v, 2) for k, v in apr_jul_service.items()}

    # ---- Vertex AI month series (agents LLM cost) ----
    vertex_by_month = {m: round(by_month_service[m].get("Vertex AI", 0.0), 2) for m in months}
    cloudrun_by_month = {m: round(by_month_service[m].get("Cloud Run", 0.0), 2) for m in months}
    gemini_by_month = {m: round(by_month_service[m].get("Gemini API", 0.0), 2) for m in months}

    # ---- console output ----
    print("=" * 70)
    print("RECONCILIATION")
    print("=" * 70)
    for month in MONTH_FILES:
        d = months[month]
        tax = sum(d["tax_by_project"].values())
        print(f"{month}: pre-tax {d['pretax']:>9.2f} + tax {tax:>7.2f} = "
              f"{d['pretax']+tax:>9.2f}  (invoice total incl tax: {d['total_incl_tax']})")
    apr_jul_pretax = sum(months[m]["pretax"] for m in MONTH_FILES)
    apr_jul_tax = sum(sum(months[m]["tax_by_project"].values()) for m in MONTH_FILES)
    print(f"Apr-Jul pre-tax: {apr_jul_pretax:.2f}   tax: {apr_jul_tax:.2f}   "
          f"total: {apr_jul_pretax+apr_jul_tax:.2f}")
    print(f"Breakdown Jan-Jul total (incl tax): {BREAKDOWN_JAN_JUL_TOTAL}  "
          f"<- should match Apr-Jul total")
    print(f"Reports Jan-Aug pre-tax: {REPORTS_JAN_AUG_PRETAX}  |  "
          f"Breakdown Jan-Jul pre-tax: {BREAKDOWN_JAN_JUL_PRETAX}  |  "
          f"=> Aug partial ~ {REPORTS_JAN_AUG_PRETAX-BREAKDOWN_JAN_JUL_PRETAX:.2f}")

    print("\n" + "=" * 70)
    print("JAN-AUG BUSINESS vs PERSONAL  (from reports; Gemini API = personal)")
    print("=" * 70)
    print(f"BUSINESS (RT):   €{jan_aug_business:>8.2f}  ({jan_aug_business/jan_aug_total*100:5.1f}%)")
    print(f"PERSONAL (iginsider): €{jan_aug_personal:>5.2f}  ({jan_aug_personal/jan_aug_total*100:5.1f}%)")
    print(f"TOTAL pre-tax:   €{jan_aug_total:>8.2f}")

    print("\n" + "=" * 70)
    print("APR-JUL PER PROJECT (pre-tax, exact from invoices)")
    print("=" * 70)
    hdr = f"{'project':<28}" + "".join(f"{m:>10}" for m in MONTH_FILES) + f"{'total':>10}"
    print(hdr)
    for proj in sorted(apr_jul_project):
        row = f"{proj:<28}"
        for m in MONTH_FILES:
            row += f"{by_month_project[m].get(proj, 0.0):>10.2f}"
        row += f"{apr_jul_project[proj]:>10.2f}"
        print(row)

    print("\n" + "=" * 70)
    print("APR-JUL PER SERVICE (pre-tax)")
    print("=" * 70)
    print(hdr)
    services_sorted = sorted(apr_jul_service, key=lambda s: -apr_jul_service[s])
    for svc in services_sorted:
        row = f"{svc:<28}"
        for m in MONTH_FILES:
            row += f"{by_month_service[m].get(svc, 0.0):>10.2f}"
        row += f"{apr_jul_service[svc]:>10.2f}"
        print(row)

    print("\n" + "=" * 70)
    print("APR-JUL PER BUCKET (pre-tax)  business vs personal")
    print("=" * 70)
    print(f"{'bucket':<28}" + "".join(f"{m:>10}" for m in MONTH_FILES) + f"{'total':>10}")
    for b in ("business", "personal", "other"):
        row = f"{b:<28}"
        for m in MONTH_FILES:
            row += f"{by_month_bucket[m].get(b, 0.0):>10.2f}"
        row += f"{apr_jul_bucket.get(b, 0.0):>10.2f}"
        print(row)

    print("\n" + "=" * 70)
    print("PERSONAL (iginsider) BREAKDOWN: Veo video vs image gen (pre-tax)")
    print("=" * 70)
    print(f"{'component':<28}" + "".join(f"{m:>10}" for m in MONTH_FILES) + f"{'total':>10}")
    for name, series in (("Veo video gen", veo_by_month), ("Gemini image gen", img_by_month)):
        row = f"{name:<28}"
        for m in MONTH_FILES:
            row += f"{series.get(m, 0.0):>10.2f}"
        row += f"{sum(series.values()):>10.2f}"
        print(row)

    print("\n" + "=" * 70)
    print("KEY SERVICE MoM (Vertex AI = agents LLM, Cloud Run = compute, Gemini = personal)")
    print("=" * 70)
    print(f"{'service':<28}" + "".join(f"{m:>10}" for m in MONTH_FILES))
    for name, series in (("Cloud Run (compute)", cloudrun_by_month),
                         ("Vertex AI (agents LLM)", vertex_by_month),
                         ("Gemini API (personal)", gemini_by_month)):
        row = f"{name:<28}"
        for m in MONTH_FILES:
            row += f"{series.get(m, 0.0):>10.2f}"
        print(row)

    # ---- write JSON ----
    out = {
        "reports_jan_aug_by_service": reports,
        "reports_jan_aug_pretax_total": round(jan_aug_total, 2),
        "breakdown_jan_jul_pretax": BREAKDOWN_JAN_JUL_PRETAX,
        "breakdown_jan_jul_total_incl_tax": BREAKDOWN_JAN_JUL_TOTAL,
        "aug_partial_estimate": round(REPORTS_JAN_AUG_PRETAX - BREAKDOWN_JAN_JUL_PRETAX, 2),
        "months": list(MONTH_FILES),
        "by_month": {
            m: {
                "pretax": months[m]["pretax"],
                "tax": round(sum(months[m]["tax_by_project"].values()), 2),
                "total_incl_tax": months[m]["total_incl_tax"],
                "by_project": by_month_project[m],
                "by_bucket": by_month_bucket[m],
                "by_service": by_month_service[m],
                "veo": round(veo_by_month.get(m, 0.0), 2),
                "image_gen": round(img_by_month.get(m, 0.0), 2),
            }
            for m in MONTH_FILES
        },
        "apr_jul": {
            "by_bucket": apr_jul_bucket,
            "by_project": apr_jul_project,
            "by_service": apr_jul_service,
            "pretax_total": round(apr_jul_pretax, 2),
        },
        "jan_aug_split": {
            "business": round(jan_aug_business, 2),
            "personal": round(jan_aug_personal, 2),
            "total": round(jan_aug_total, 2),
        },
        "vertex_by_month": vertex_by_month,
        "cloudrun_by_month": cloudrun_by_month,
        "gemini_by_month": gemini_by_month,
    }
    out_path = os.path.join(HERE, "costs.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    sys.exit(main())
