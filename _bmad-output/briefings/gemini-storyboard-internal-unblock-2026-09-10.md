# Internal resolution — owner handoff and scoped BMAD binding

## Authority and disposition

The approved initial Gemini pilot remains US$5 TOTAL / 2–3 useful images / exact gemini-3.1-flash-image. No image has yet been generated. The 54 UNKNOWN / S47 started evidence remains valid; do not fabricate unstarted status. These are internal coordination/configuration blockers, not a reason to re-ask the user for already-granted spending approval.

This is an explicit narrow amendment to the earlier no-repair/no-retry instruction, solely for the configuration binding described below. It does NOT authorize a framework rewrite, weakening a guard, reading raw workflow sources as execution instructions, skipping review or resetting a native campaign.

## 1. Obtain the native owner's factual shot handoff now

Silas routes pNS's preferred 2–3 representative pilot shot IDs to the retained pP5 owner and requests a READ-ONLY factual response: for each, has shot-specific native staging, animation or rendering begun? Confirm unstarted only from the owner's actual knowledge/records, identify evidence/date and name any shared-asset-only work separately. If an initially proposed shot is started or genuinely unknown, choose another owner-confirmed unstarted shot. Do not wait for a new exhaustive audit of all 54 before confirming just the needed pilot subset.

This authorizes pP5 to answer from its retained session and narrow local records. It does not authorize live Blender/MCP inspection, process probes, a render, new source editing or changing the S47 queue/guards. Silas handles the ordinary owner handoff; no user question is needed to establish what our own production owner has worked on. S47 stays excluded.

Preserve the existing evidence JSON/Markdown; append a dated owner-confirmation supplement rather than relabeling old UNKNOWN evidence. pNS can then select the confirmed subset.

The absence of OLD per-shot cloud-clearance receipts is not a second permission gate. The current approved pilot grant already permits the selected original/project-owned references needed for the selected shots. Record their selection/provenance against that grant. Do not upload CHARGE/BMS/restricted third-party images or waive genuine uncertainty about reference ownership.

## 2. Exact BMAD error and supported local binding correction

Gru read the actual error and renderer/config metadata, without running a workflow:

`HALT: ambiguous config value implementation_artifacts found at: modules.bmm.implementation_artifacts, modules.gds.implementation_artifacts`

Both installed modules currently set implementation_artifacts to `{project-root}/_bmad-output/implementation-artifacts` and planning_artifacts to `{project-root}/_bmad-output/planning-artifacts`. The renderer rejects duplicate SHORT keys even when values coincide. It already supports fully qualified `{{config.modules.bmm.implementation_artifacts}}` and `{{config.modules.bmm.planning_artifacts}}` through `_CONFIG_TOKEN` and `_lookup`.

pP9 may perform ONE narrowly scoped configuration-hygiene recovery:
1. Preserve the failed invocation/output. Create a small job-local copy of the existing canonical bmad-build skill under an ignored scratch directory inside its own worktree, with final directory name `bmad-build`. Do NOT modify the canonical `/Users/moses/code/.agents/skills/bmad-build`, the shared `_bmad` symlink target, central config, renderer code, or tracked upstream skill defaults. A BMM-specific project binding must not become a global regression for GDS-only projects.
2. In that job-local copy ONLY, replace exact tokens `{{.implementation_artifacts}}` and `{{.planning_artifacts}}` with their fully qualified BMM forms above. This orchestrator code task uses BMM. No other byte changes, workflow/review-layer edits, disabled errors or hard-coded absolute output paths.
3. Verify canonical source equals the local copy after reversing ONLY those two substitutions; preserve source/copy hashes and a compact diff. This is mechanical template binding, not bypassing workflow execution. If that equality fails or actual module values differ from the values above, STOP and report.
4. Under this new explicit recovery disposition, invoke the unchanged mandatory render command ONCE, from the same worktree, using its actual project root and the corrected job-local `--skill` directory. No changed cwd. Read/follow ONLY the absolute generated workflow it prints on success. If it fails again, report the exact output and HALT—no retry or expanding repair. Never run the raw source workflow directly.
5. On successful rendering, resume the already-authorized generic skill implementation and its prescribed review/verification. All snapshots/config selection records remain local evidence; do not include the temporary BMAD copy or unrelated files in the Gemini PR. Report the small binding issue for a separate future tooling fix, without dispatching that campaign now.

This local correction is limited to the two demonstrated ambiguous field bindings. It is NOT permission to choose arbitrary values to make the gate pass. Original source and first HALT remain preserved.

## 3. Correct relay transcription, not the approval

Actual approval brief SHA (freshly recomputed by Gru):
`8bbeaa08896aa42e1c033f54b0eb9dc18f054f68caf36ea06bf081eaeb84bb73`

The earlier one-a-short digest in a relay was a transcription error; the source approval file is unchanged. Read it from disk rather than retyping. The latest evidence relay carries the correct value.

The core ledger notes show `US` and `/bin/bash` where dollar amounts were intended: shell expansion corrupted the notes. Silas owns correction with a new literal note sourced from the approval file, using argv-safe quoting, not another interpolated shell payload. The approved limit is US$5 TOTAL shared across both jobs; it is neither missing nor unlimited. Preserve the malformed historical notes as corrected history.

## Routing and reporting

- Existing pP9/core and pNS/pilot, same sessions/Astra xhigh. No new owner/fleet.
- Silas relays/verifies both dispositions and gets the pP5 factual response without touching native production.
- First useful image remains the single coordinated live integration check, after genuine helper readiness. No duplicate billed probes or waiting on docs publication.
- Report actual images when ready. A confirmed subset or rendered workflow is intermediate progress, not generation success.
