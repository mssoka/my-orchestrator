---
name: review-plan
description: "Spawn a parallel agent team to review an implementation plan from multiple angles: adversarial, security, edge cases, architecture, codebase fit, and test coverage. Use when the user says 'review plan', 'review this plan', or 'review the plan'."
allowed-tools: Agent, Read, Glob, Grep, Edit, Write, AskUserQuestion, Bash(cat:*), Bash(git:*)
user-invocable: true
---

# Plan Review — Parallel Agent Team

Spawns 6 specialist review agents in parallel to stress-test an implementation plan before execution begins. Each agent has a fresh context window and a single lens. Findings are emitted as JSON, mechanically deduped, triaged, and consolidated into one actionable report.

All reviewers use `subagent_type: general-purpose`. The "specialist" framing lives in the prompt, not the agent type — fresh context is the real value of fan-out.

## Usage

`/review-plan` — reviews the plan in the current conversation context

## Prerequisites

- A plan must exist in the current conversation (plan mode, a `.md` plan file, or equivalent)
- The plan should reference specific files, modules, or areas of the codebase

## Execution

### Step 1: Extract the Plan and Load Context

1. Locate the plan in the current conversation. If none exists, tell the user:
   > "No plan found in this conversation. Create a plan first, then run `/review-plan`."
2. Capture the full plan text as `{plan_content}`.
3. Load `CLAUDE.md` (or equivalent project instructions) if present; capture as `{project_conventions}`. If absent, set to `"none"`.
4. Run `git diff --stat` if recent changes exist — helps reviewers sanity-check the plan's assumptions about current state.

### Step 2: Launch Parallel Review Agents

Spawn all 6 agents in a SINGLE message using the Agent tool. Each call has `subagent_type: general-purpose` and the prompt structure below.

**CRITICAL: All 6 Agent calls MUST be in one message for true parallel execution.**

#### Shared prompt block (sent to every reviewer)

Every reviewer's prompt begins with:

```
You are reviewing an implementation plan, not code. You have read-only access to the repository and may verify the plan's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
{project_conventions}

--- PLAN ---
{plan_content}

--- YOUR LENS ---
{lens_brief_for_this_reviewer}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: adversarial | security | edge | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | plan-section | N/A>",
  "evidence": "<the exact lines you READ — quoted verbatim from either the plan text or the codebase file you opened. Use 'N/A' ONLY for findings about something genuinely absent (e.g. 'plan never mentions auth'). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified — code claims against the actual codebase, plan claims against the actual plan text — before it reaches the report. Findings that fail verification are DISCARDED SILENTLY: they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- If you cite a file, function, or symbol: open the file, read the lines, paste them into `evidence`. Do not guess from the filename, do not assume from similar-looking code, do not generalise from one example to the rest.
- If you cite a plan section: paste the exact plan text in `evidence`. Do not paraphrase.
- Hedging language ("might", "could", "possibly", "potentially") is a signal you have not actually verified. Either verify and report crisply, or do not report.
- A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
```

#### Reviewer 1 — Adversarial (source: `adversarial`)

Lens brief:

```
You are a cynical, jaded reviewer with zero patience for sloppy work. Assume problems exist. Be skeptical of everything. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Requirements traceability: does every stated requirement map to a concrete plan step?
- Acceptance criteria: are they clear, testable, objectively verifiable?
- Scope drift: does the plan deliver exactly what was asked, not more, not less?
- Implied requirements: what's assumed but not stated?
- Logical gaps: unstated steps, unchecked dependencies, hand-waving.
```

#### Reviewer 2 — Security (source: `security`)

Lens brief:

```
OWASP-oriented security review of the planned changes. Identify:
- Auth/authz gaps in new endpoints, routes, or flows
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling
- Data exposure (logs, responses, client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
```

#### Reviewer 3 — Edge Case (source: `edge`)

Lens brief:

```
You are a pure path tracer. Do not comment on whether the plan is good or bad — list only unhandled paths.

Method: mechanically walk every branching path and boundary condition implied by the plan. Derive the relevant edge classes from the plan itself — no fixed checklist. Examples: missing else/default, unguarded inputs, off-by-one loops, arithmetic overflow, implicit type coercion, race conditions, timeout gaps, concurrent operations, external service unavailability (DB, APIs, auth), boundary values (empty lists, nulls, zero counts, max sizes), states the plan doesn't account for.

For each path, determine whether the plan handles it. Report ONLY unhandled paths; discard handled ones silently. No editorializing.
```

#### Reviewer 4 — Architecture (source: `architecture`)

Lens brief:

```
Architectural fit review. Given the plan and the codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
```

#### Reviewer 5 — Codebase Fit (source: `codebase`)

Lens brief:

```
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, and types referenced in the plan actually exist?
- Are the plan's assumptions about existing code accurate?
- Does the plan account for existing tests it might break?
- Are naming conventions and style consistent with the project?
- Does the plan duplicate logic that already exists? (Point to the existing helper in `location`.)
- Are required dependencies (imports, packages) available or do they need adding?
```

#### Reviewer 6 — Test Coverage (source: `tests`)

Lens brief:

```
Test coverage readiness via traceability analysis.

For each plan item, trace to an existing or planned test. Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- DB operations without integration coverage
- State transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%
```

#### Partial-failure handling

If a reviewer fails, times out, or returns something that isn't valid JSON, add its `source` tag to `{failed_layers}` (comma-separated) and proceed with the remaining reviewers. Do not retry the failed reviewer automatically.

### Step 3: Validate and Consolidate Findings

**Default stance: every finding is presumed false-positive until you have re-verified it against the actual code or plan text yourself.** No reviewer claim reaches the report on the reviewer's word alone. The user has explicitly chosen accuracy over speed — if verification takes longer than the reviewer pass, that is the expected cost. Do not skip verifications to save time.

#### 3a. Parse and pre-filter

1. **Parse** each reviewer's JSON array. Malformed output → add that reviewer to `{failed_layers}`; drop its findings.
2. Collect every finding into a working set. Record `{total_findings}` count.

#### 3b. Verify every finding against its source of truth (MANDATORY)

For each finding in the working set, decide one of three outcomes — **confirmed**, **rejected**, or **unverifiable-speculative** — by reading the actual code or plan text:

1. **`location` names a file:line, file:hunk, function, type, or symbol in the codebase**:
   - Use the Read tool to open the cited file. Read enough surrounding context to evaluate the claim — usually ±20 lines, more if the claim depends on callers or related code.
   - Confirm ALL of:
     - The file exists at the path the finding claims.
     - The cited line/function/symbol exists there.
     - The `evidence` field's quoted lines match the actual file content (whitespace tolerance is fine; meaning must match).
     - The plan's claim about that code holds — the assumption, the conflict, the missing dependency is genuinely present, not just plausibly inferable.
   - If ANY check fails → mark as **rejected** and DISCARD. Increment `{rejected_count}`. Do not "soften" into a note. A hallucinated claim is noise that has historically misled the user — dropping it is the whole point of this step.

2. **`location` names a plan section**:
   - Re-read that section of `{plan_content}`. Confirm the `evidence` snippet really appears there, and that the reviewer's reading of it is accurate (not a misinterpretation of the plan's words).
   - If the plan doesn't say what the reviewer claims it says → mark as **rejected** and DISCARD.

3. **Claim depends on code outside the directly-cited location** (e.g. "this helper already exists", "this caller would break", "duplicates logic in X", "violates the pattern in Y"):
   - Read those referenced files too. Confirm the assumed caller/helper/duplicate/pattern actually exists and behaves as claimed.
   - If the dependency doesn't hold → mark as **rejected** and DISCARD.

4. **`location: "N/A"` AND `evidence: "N/A"`** (a finding with no possible anchor — e.g. "plan omits X entirely"):
   - These cannot be code-verified, but a "plan omits X" claim CAN be verified by grepping the plan for any mention of X. Do that grep before accepting.
   - If the plan does mention X and the reviewer simply missed it → mark **rejected** and DISCARD.
   - If the plan genuinely doesn't mention X → mark as **unverifiable-speculative**.
   - If severity was `blocker` → demote to `warning` and prepend `[unverified]` to the title. An unverifiable claim cannot block implementation.
   - If severity was `warning` or `note` → prepend `[unverified]` to the title and keep.

5. **`location: "N/A"` but `evidence` is non-empty** (reviewer quoted something without naming a file):
   - Grep for the quoted snippet across the repo and across the plan. If you find it → verify per (1) or (2).
   - If you cannot find it → mark as **rejected** and DISCARD.

Record per finding: `verification: "confirmed" | "rejected" | "unverifiable-speculative"`. Discard rejected findings entirely.

After 3b, log the validation outcome internally: `Verified: {confirmed}/{total_findings}; rejected {rejected_count} as unverifiable/false-positive; {unverifiable_speculative_count} kept as speculative.`

#### 3c. Consolidate the surviving findings

1. **Union** all surviving (confirmed + unverifiable-speculative) findings.
2. **Deduplicate** on the normalised pair `(lowercased_title, location)`. When merging duplicates:
   - Promote `source` to an array of all sources that reported the finding (e.g. `["architecture","codebase"]`).
   - Keep the highest severity across duplicates (after the demotions in 3b).
   - Merge `detail` lines if they add non-overlapping information.
3. **Triage into severity buckets** (`blocker`, `warning`, `note`) using each finding's post-demotion `severity` field.
4. **Identify the Reviewer Agreement set**: findings whose `source` is now an array of length ≥ 2. When two independent reviewers confirm the same code-anchored finding, that is the highest-confidence signal — surface it first.

### Step 4: Present Report

Output in this format:

```
## Plan Review Report

**Plan:** {short plan title or 1-line summary}
**Reviewers:** {completed_count}/6 completed{" — failed: " + failed_layers if any}
**Verification:** {confirmed_count}/{total_findings} reviewer findings survived re-verification — {rejected_count} discarded as false-positive{; if unverifiable_speculative_count > 0: ", " + unverifiable_speculative_count + " kept as [unverified] speculative"}

### BLOCKERS ({count})
{for each — title [sources], location, detail, recommended fix}

### WARNINGS ({count})
{same format}

### NOTES ({count})
{same format}

### Reviewer Agreement
{multi-source findings — higher confidence, prioritise first}

### Verdict
{One of: READY TO IMPLEMENT | NEEDS REVISION | MAJOR REWORK NEEDED}
{One-sentence justification}
```

**Verdict rule:**
- 0 BLOCKERS → READY TO IMPLEMENT
- 1–3 BLOCKERS → NEEDS REVISION
- 4+ BLOCKERS → MAJOR REWORK NEEDED

If `{failed_layers}` is non-empty AND zero findings remain, warn that the review may be incomplete rather than declaring the plan clean.

### Step 5: Auto-Integrate Valid Recommendations

After presenting the report, act as an editor for the plan: triage every finding, discard the noise, auto-apply valid non-controversial recommendations to the plan file, and only pull the user in for items that require a real decision.

**Do NOT ask the user for blanket permission at this stage.** Integration of non-controversial fixes is automatic.

#### 5a. Triage every finding into one of three buckets

For each BLOCKER, WARNING, and NOTE in the report, classify as:

- **DISCARD** — noise, false positive, or non-applicable (reviewer misread the plan, recommendation contradicts an explicit constraint, or the finding is speculative with no supporting evidence). Drop silently; record a count for the summary.
- **AUTO-INTEGRATE** — valid AND non-controversial. Apply directly to the plan without asking.
- **NEEDS DECISION** — valid but controversial, ambiguous, or requires a design/product/UX choice. Defer to a one-by-one walkthrough with the user.

**Controversy heuristic — when is a recommendation "non-controversial"?**

A recommendation is **non-controversial** (auto-integrate) when ALL of these hold:
- The fix to the plan is obvious and there is essentially one reasonable way to apply it
- It's a clarification, a missed acceptance criterion, a clearly-correct reference to an existing file/function, a mechanical correction (typo, wrong path, missing step, obvious missing test case for a P0 happy path)
- No reasonable reviewer would debate it — it's a "yes, obviously" change
- It does not alter scope, public API shape, or the plan's stated goals beyond closing the gap the reviewer found
- It does not require a product / UX / policy decision or architectural choice
- No new dependency, pivot, or cross-cutting refactor is implied

A recommendation is **controversial / needs decision** if ANY of these hold:
- Multiple valid approaches exist with real trade-offs
- It changes scope, public API, contracts, or product behaviour beyond closing the gap
- It requires a product / UX / policy decision
- It needs clarification from the user (the reviewer's own recommendation is hedged: "consider", "might want to", "depends on")
- It requires a structural/architectural choice (introduce an abstraction, pick a library, rename a module)
- Two reviewers gave contradictory recommendations

When in doubt, treat as NEEDS DECISION.

BLOCKERS default to NEEDS DECISION unless the fix is purely mechanical (e.g. "plan references `src/foo.ts` but the file is `src/foo.tsx`"). Most BLOCKERS should go through the walkthrough.

#### 5b. Auto-integrate the non-controversial bucket

Apply every AUTO-INTEGRATE recommendation to the plan directly. This typically means editing the plan text to add missed steps, fix references, tighten acceptance criteria, add missing test cases, or correct small factual errors.

After applying, announce what was integrated:

```
## Auto-Integrated Updates ({count})

The following recommendations were applied to the plan directly (non-controversial):

- [source] {one-line summary of the change} — {where in the plan it landed}
- ...

## Discarded ({count})
{brief count; optional one-line reasons if the user would benefit}
```

#### 5c. Walk through NEEDS DECISION items one-by-one

If any findings landed in NEEDS DECISION, announce:

> "I'll walk through the {N} items that need a decision one at a time."

For each NEEDS DECISION finding, in order (BLOCKERS first, then WARNINGS, then NOTES):

1. **Re-explain the issue in plain English** — restate the title, what the reviewer found, which reviewer(s) caught it, and why it's controversial (the trade-off or decision required).
2. **Present the options** — list the viable fixes with their trade-offs. If the reviewer proposed one, include it; surface plausible alternatives too.
3. **HALT and ask the user** (use AskUserQuestion):
   - **Apply option A / B / C ...** — integrate the chosen option into the plan
   - **Leave the plan unchanged** — acknowledge the finding but don't modify the plan
   - **Skip for now** — defer, return to it after the others
   - **Stop the walkthrough** — halt; summarise what's integrated and what's pending
4. If the user picks an option: edit the plan accordingly, then move to the next item.

#### 5d. Final summary

Once auto-integration and the walkthrough are done (or the user stopped), present:

```
## Plan Integration Summary

- Auto-integrated: {count} recommendations applied directly
- Walked through: {count} controversial items — {integrated count} integrated, {declined count} declined, {deferred count} deferred
- Discarded: {count} findings dropped as noise / non-applicable

### Plan changes
{brief summary of the shape of the updates — which sections grew, which acceptance criteria were added, etc.}

### Recommended next steps
- Re-read the updated plan end-to-end before implementing
- {if any deferred items remain} Resolve the {N} deferred decisions before starting
```
