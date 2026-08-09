# Field notes — righttenantry-gcp-cost-analysis

- 2026-08-06 (lavish mid-review): after overwriting the dashboard HTML mid-review
  (Gru's "Gemini API is triple-blended, not personal" correction), the browser kept
  serving the CACHED old version — the user said "nice" to the stale "personal"
  framing. The poll's `dom_snapshot` was the only ground truth that the old content
  was still on screen. Lesson: after a mid-review file rewrite, either
  `lavish-axi <file> --reopen` or explicitly tell the reviewer to reload AND verify
  via the NEXT poll's dom_snapshot that the new content actually rendered before
  trusting any "looks good" verdict.
- 2026-08-06 (GCP cost attribution): a single GCP project can serve MULTIPLE
  use-cases — `iginsider` blended RT Facebook-ad creative + RT agents + personal
  YouTube. Never assume one project = one use-case; group by project but FLAG
  use-case blending and require app-side resource/call LABELS to attribute.
  The project boundary is the only clean line billing data gives you.
- 2026-08-06 (GCP billing export): `gcloud` has NO billing-export command and the
  public Cloud Billing v1 API does not expose the BigQuery export config — enabling
  it is CONSOLE-ONLY. From a minion shell you can create the target dataset (`bq mk`)
  and write the attribution queries, but flipping the export is the user's 4 console
  clicks. Required role: billing admin (`billing.accounts.update`). The Detailed
  (resource-level) export's `resource.name` splits Cloud Run by service with NO app
  change; use-case attribution inside a project still needs app labels.
