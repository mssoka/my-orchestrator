---
name: code-review
description: "Spawn a parallel agent team to review a code diff from multiple angles: blind adversarial, edge cases, acceptance vs spec, security, architecture, codebase fit, and test coverage. Use when the user says 'code review', 'review this code', or '/code-review'."
allowed-tools: Agent, Read, Glob, Grep, Edit, Write, AskUserQuestion, Bash(git:*), Bash(gh:*), Bash(cat:*)
user-invocable: true
---

# Code Review — Parallel Agent Team

Spawns up to 7 specialist review agents in parallel against a code diff. Each agent has a fresh context window and a single lens. Findings are emitted as JSON, mechanically deduped, triaged, and consolidated into one actionable report. Matches `/review-plan` in shape so the two skills read identically.

All reviewers use `subagent_type: general-purpose`. The "specialist" framing lives in the prompt, not the agent type — fresh context is the real value of fan-out.

## Usage

**Automated headless callers (Perkins):** Steps 1, 4, and 5 do not apply — go straight to 'Headless / Automated Mode' at the bottom.

- `/code-review` — HALT and ask which diff source to review
- `/code-review staged` — review staged changes
- `/code-review uncommitted` — review staged + unstaged changes
- `/code-review vs main` / `/code-review branch diff` — diff current branch against a base
- `/code-review pr <N>` — review a GitHub PR by number via `gh pr diff`
- `/code-review <sha1>..<sha2>` — review a commit range
- `/code-review this diff` — review a diff pasted by the user

## Execution

### Step 1: Determine the Diff Source

Detect intent from the invocation text. Map these phrases to a source:

- `staged` / `staged changes` → `git diff --staged`
- `uncommitted` / `working tree` / `all changes` → `git diff HEAD`
- `branch diff` / `vs main` / `vs develop` / `against <branch>` → `git diff <base>...HEAD` (verify base branch exists; if not, HALT and ask)
- `commit range` / `<sha>..<sha>` / `last N commits` → `git diff <range>` (verify the range resolves; if not, HALT)
- `pr <N>` / `pull request <N>` → `gh pr diff <N>` (if `gh` is unavailable or the PR doesn't exist, HALT)
- `this diff` / pasted diff → use the pasted content (validate it parses as a unified diff)

If no intent match, HALT and ask:

> **What do you want to review?**
> - Uncommitted changes (staged + unstaged)
> - Staged changes only
> - Branch diff vs a base branch (which one?)
> - Specific commit range
> - A GitHub PR (which number?)
> - Provided diff (paste it)

Capture the result as `{diff_output}`. Verify it is non-empty — if empty, HALT and tell the user there is nothing to review.

Then ask:

> **Is there a spec, story, or plan file that describes what this diff is meant to do?**

- If yes: bind to `{spec_file}`, verify it exists, read it, set `{review_mode} = "full"`.
- If no: set `{review_mode} = "no-spec"` — the Acceptance Auditor layer will be skipped.

If `{spec_file}` frontmatter lists a `context` field with additional docs, load each; warn about any that can't be found. Capture all context text as `{context_docs}`.

Load `CLAUDE.md` (or equivalent project instructions) if present; capture as `{project_conventions}`. If absent, set to `"none"`.

**Sanity check:** if `{diff_output}` exceeds ~3000 lines, warn the user and offer to chunk the review by file group. If they agree, narrow `{diff_output}` to the first group and list the rest as follow-up runs. Otherwise proceed as-is.

Show a summary before continuing: files changed, lines +/-, `{review_mode}`, spec/context loaded.

### Step 2: Launch Parallel Review Agents

Spawn all active reviewers in a SINGLE message using the Agent tool. Each call has `subagent_type: general-purpose` and the prompt structure below.

**CRITICAL: All Agent calls MUST be in one message for true parallel execution.**

If `{review_mode} = "full"`, fire all 7 reviewers. If `{review_mode} = "no-spec"`, skip the Acceptance Auditor and fire 6.

#### Shared prompt block (sent to every reviewer EXCEPT Blind Hunter)

```
You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
{project_conventions}

--- DIFF ---
{diff_output}

--- SPEC / CONTEXT ---
{spec_file contents and context_docs if review_mode=full, else "none provided"}

--- YOUR LENS ---
{lens_brief_for_this_reviewer}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
```

#### Reviewer 1 — Blind Hunter (source: `blind`)

**Blind Hunter is an exception to the shared block.** It receives only the diff — no project conventions, no spec, no codebase access. This preserves the adversarial "fresh eyes with no framing" value.

Prompt:

```
You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
{diff_output}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
```

#### Reviewer 2 — Edge Case (source: `edge`)

Lens brief (follows the shared block):

```
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
```

#### Reviewer 3 — Acceptance Auditor (source: `acceptance`) — only if `{review_mode} = "full"`

Lens brief (follows the shared block):

```
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
```

#### Reviewer 4 — Security (source: `security`)

Lens brief:

```
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
```

#### Reviewer 5 — Architecture (source: `architecture`)

Lens brief:

```
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
```

#### Reviewer 6 — Codebase Fit (source: `codebase`)

Lens brief:

```
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
```

#### Reviewer 7 — Test Coverage (source: `tests`)

Lens brief:

```
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

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

**Default stance: every finding is presumed false-positive until you have re-verified it against the actual code yourself.** No reviewer claim reaches the report on the reviewer's word alone. The user has explicitly chosen accuracy over speed — if verification takes longer than the reviewer pass, that is the expected cost. Do not skip verifications to save time.

#### 3a. Parse and pre-filter

1. **Parse** each reviewer's JSON array. Malformed output → add that reviewer to `{failed_layers}`; drop its findings.
2. Collect every finding into a working set. Record `{total_findings}` count.

#### 3b. Verify every finding against the codebase (MANDATORY)

For each finding in the working set, decide one of three outcomes — **confirmed**, **rejected**, or **unverifiable-speculative** — by reading the actual code:

1. **`location` names a file:line, file:hunk, function, type, or symbol** (the common case):
   - Use the Read tool to open the cited file at the cited location. Read enough surrounding context to evaluate the claim — usually ±20 lines, more if the claim spans hunks or depends on caller behaviour.
   - Confirm ALL of:
     - The file exists at the path the finding claims.
     - The cited line/function/symbol exists at that location.
     - The `evidence` field's quoted lines match the actual file content verbatim (whitespace tolerance is fine; meaning must match).
     - The code behaves the way the finding claims — the bug, gap, or violation is genuinely present, not just plausibly inferable.
   - If ANY check fails → mark as **rejected** and DISCARD. Increment `{rejected_count}`. Do not "soften" it into a note. A hallucinated claim is not a real finding — it is noise that has historically misled the user, and dropping it is the whole point of this step.

2. **Claim depends on code outside the diff** (e.g. "this helper already exists", "this caller would break", "duplicates logic in X", "violates pattern in Y"):
   - Read those referenced files too. Confirm the assumed caller/helper/duplicate/pattern actually exists and behaves as claimed.
   - If the dependency doesn't hold → mark as **rejected** and DISCARD.

3. **`location: "N/A"` AND `evidence: "N/A"`** (a finding with no possible code anchor — e.g. "spec is missing X"):
   - These cannot be code-verified. Mark as **unverifiable-speculative**.
   - If severity was `blocker` → demote to `warning` and prepend `[unverified]` to the title. An unverifiable claim cannot block a merge.
   - If severity was `warning` or `note` → prepend `[unverified]` to the title and keep.

4. **`location: "N/A"` but `evidence` is non-empty** (reviewer quoted something without naming a file):
   - Grep for the quoted snippet across the repo. If you find it → verify per (1) using the located file.
   - If you cannot find it → mark as **rejected** and DISCARD.

Record per finding: `verification: "confirmed" | "rejected" | "unverifiable-speculative"`. Discard rejected findings entirely.

After 3b, log the validation outcome internally: `Verified: {confirmed}/{total_findings}; rejected {rejected_count} as unverifiable/false-positive; {unverifiable_speculative_count} kept as speculative.`

#### 3c. Consolidate the surviving findings

1. **Union** all surviving (confirmed + unverifiable-speculative) findings.
2. **Deduplicate** on the normalised pair `(lowercased_title, location)`. When merging duplicates:
   - Promote `source` to an array of all sources that reported the finding (e.g. `["blind","security"]`).
   - Keep the highest severity across duplicates (after the demotions in 3b).
   - Merge `detail` lines if they add non-overlapping information.
3. **Triage into severity buckets** (`blocker`, `warning`, `note`) using each finding's post-demotion `severity` field.
4. **Identify the Reviewer Agreement set**: findings whose `source` is now an array of length ≥ 2. When two independent reviewers confirm the same code-anchored finding, that is the highest-confidence signal in the report — surface it first.

### Step 4: Present Report

Output in this format:

```
## Code Review Report

**Diff source:** {source description — e.g. "branch diff develop...HEAD, 12 files, +340 −85"}
**Spec:** {spec_file path or "none provided"}
**Reviewers:** {completed_count}/{total} completed{" — failed: " + failed_layers if any}
**Verification:** {confirmed_count}/{total_findings} reviewer findings survived code re-verification — {rejected_count} discarded as false-positive{; if unverifiable_speculative_count > 0: ", " + unverifiable_speculative_count + " kept as [unverified] speculative"}

### BLOCKERS ({count})
{for each — title [sources], location, detail, recommended fix}

### WARNINGS ({count})
{same format}

### NOTES ({count})
{same format}

### Reviewer Agreement
{multi-source findings — higher confidence, prioritise first}

### Verdict
{One of: READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED}
{One-sentence justification}
```

**Verdict rule (same thresholds as `/review-plan`):**
- 0 BLOCKERS → READY TO MERGE
- 1–3 BLOCKERS → NEEDS CHANGES
- 4+ BLOCKERS → MAJOR REWORK NEEDED

If `{failed_layers}` is non-empty AND zero findings remain, warn that the review may be incomplete rather than declaring the diff clean.

Do NOT auto-fix yet. Present findings, then proceed to Step 5.

### Step 5: Interactive Fix Flow

After the report is presented, offer to work through the findings. The cadence is different per severity — BLOCKERS are always one-by-one; WARNINGS and NOTES offer batch options because they're less critical and the user may want to triage them as a group.

#### 5a. BLOCKERS — always one-by-one (no batch option)

If there are BLOCKERS, announce:

> "I'll walk through the {N} blockers one at a time. Each is critical, so I won't batch them."

For each BLOCKER, in order:

1. **Re-explain the issue in plain English** — restate the title, the file:line, what's wrong, why it's a blocker, and which reviewer(s) caught it. Don't just repeat the report prose — synthesise it so the user has full context without scrolling back.
2. **State the proposed fix** — describe what you would change and any trade-offs.
3. **HALT and ask the user** (use AskUserQuestion):
   - **Fix it now** — apply the fix, show the diff, mark this blocker resolved
   - **Leave as is** — skip this blocker, record as "user-acknowledged"
   - **Skip for now** — defer without resolution, return to it after the others
   - **Stop the fix flow** — halt the whole flow, summarise what's done and what's left
4. If **Fix it now**: make the edit, then move to the next blocker. If **Leave as is** or **Skip**: move on.

Do NOT batch-apply blocker fixes. Each gets its own explanation and confirmation.

#### 5b. WARNINGS — batch or one-by-one

If there are WARNINGS, HALT and ask (AskUserQuestion):

- **Fix all warnings** — I'll apply fixes for every warning and show you the combined diff at the end
- **Auto-fix non-controversial + walk controversial** — apply fixes for clear-cut, no-brainer warnings with an obvious, safe fix; walk one-by-one through warnings that involve a trade-off, design decision, or need clarification
- **Walk through one-by-one** — same cadence as blockers: re-explain, propose fix, decide each
- **Skip all warnings** — leave every warning as is (recorded as user-acknowledged)
- **Pick a subset** — I'll list them numbered; you tell me which to fix (e.g. "1, 3, 5")

If **Fix all**: apply every warning fix, then present the combined diff for final user review before considering the warnings resolved.
If **Auto-fix non-controversial + walk controversial**: partition the warnings using the controversy heuristic below; auto-apply the non-controversial set and show the combined diff for that batch; then walk the controversial set using the same 1-4 loop as blockers.
If **Walk through**: use the same 1-4 loop as blockers.
If **Skip all**: note them as acknowledged-but-unfixed.
If **Subset**: apply fixes for the chosen items only, then summarise.

**Controversy heuristic — when is a finding "non-controversial"?**

A finding is **non-controversial** (safe to auto-fix) when ALL of these hold:
- The fix is obvious and there is essentially one reasonable way to apply it
- The fix is mechanical / local in scope (typo, missing null check, unused import, clearly wrong variable, off-by-one with a single correct bound, missing `await`, missing error handler, obvious log-leak of a secret)
- No reasonable reviewer would debate the fix — it's a "yes, obviously" change
- The fix does not change public API shape, alter behaviour beyond the bug, or require a design decision
- No new dependency, architectural shift, or cross-cutting refactor is needed

A finding is **controversial** (walk one-by-one) if ANY of these hold:
- Multiple valid fixes exist with real trade-offs
- The fix changes public API, contracts, or observable behaviour beyond fixing the defect
- It requires a product / UX / policy decision (what should happen in this edge case?)
- It needs clarification from the user (intent is ambiguous)
- It requires a structural/architectural choice (rename a module, introduce an abstraction, pick a library)
- The reviewer's own recommendation was hedged ("consider", "might want to", "depends on")

When in doubt, treat the finding as controversial and walk it.

#### 5c. NOTES — batch, walk, skip, or ignore

If there are NOTES, HALT and ask (AskUserQuestion):

- **Fix all notes** — apply every note's suggested improvement
- **Auto-fix non-controversial + walk controversial** — apply the clear-cut notes automatically; walk one-by-one through notes that involve trade-offs or need a decision (same heuristic as WARNINGS above)
- **Walk through one-by-one** — re-explain + decide each
- **Ignore all notes** — drop them entirely, don't track
- **Pick a subset** — numbered selection

Notes are non-blocking, so "Ignore all" is a reasonable default and should be offered without nagging.

#### 5d. Final summary

Once all three severity tiers have been processed (or the user stopped the flow), present a final summary:

```
## Fix Flow Summary

- Blockers: {fixed count} fixed, {skipped count} skipped, {deferred count} deferred
- Warnings: {auto-fixed count} auto-fixed, {walked-fixed count} fixed after discussion, {skipped count} skipped
- Notes: {auto-fixed count} auto-fixed, {walked-fixed count} fixed after discussion, {ignored count} ignored

### Files changed
{list of files modified during the fix flow}

### Recommended next steps
- Run the test suite to confirm nothing regressed
- {if any deferred/skipped blockers remain} Address the {N} remaining blockers before merging
- {if commits haven't been made} Consider committing the fixes in logical groups
```

Do NOT auto-commit or auto-push. The user decides when to commit.

---

## Headless / Automated Mode (Perkins)

For automated reviewers (Perkins) running without a human in the loop. Steps 1, 4's interactive presentation, and 5 do NOT apply — there is nobody to ask, and nothing to fix. Everything is driven by explicit inputs.

### Inputs

- `{diff_file}` (required) — absolute path to the canonical diff (unified format). The caller saved these bytes; review exactly them. Never re-fetch or regenerate the diff.
- `{worktree}` (required) — absolute path to a checkout at exactly the reviewed state. Every verification read happens here.
- `{spec_files}` (required) — absolute paths to spec/context docs (briefing, issue dump), or the literal `none`. `none` → review_mode = no-spec; skip the Acceptance Auditor.
- `{out_dir}` (required) — absolute path for artifacts; create it if missing.
- `{prior_findings}` (optional) — absolute path to the previous round's `consolidated.json` (see 'Re-review' below).

Missing or invalid input (diff empty / not unified, worktree absent, spec file unreadable) → STOP with an error naming the input. Never halt to ask, never guess.

### The headless pass

1. **Big-diff policy (deterministic — never ask):** if the diff exceeds ~3000 lines, split it into file-group chunks (group by top-level directory, ≤ ~3000 lines each) and run one full lens wave per chunk, sequentially. Merge all chunk findings before verification. Record the chunking in the report header.
2. **Spawn the lenses as child panes** (herdr mega-minions), one per reviewer definition in this skill — prompts verbatim (shared block + lens brief, schema, accuracy mandate) plus the file-output contract below. Pane mechanics: do NOT repeatedly `herdr pane split --current` — it subdivides your own pane. Create a dedicated tab once, then split lens panes off a fresh pane in it (`herdr pane split <pane-id> --direction right|down`), labeling each `mm-<lens>[-<chunk>]`. Max 10 concurrent child panes; close every lens pane before finishing.
   - **File-output contract:** each lens writes ONLY its JSON array to `{out_dir}/<lens>.json` — paste the full absolute path into the lens brief (lenses must not derive it) — then stops.
   - **Blind Hunter isolation:** blindness is prompt-level in pane-world — the pane has tools and could read the repo. Do not pass it `{worktree}`, `{spec_files}`, or project conventions, and state explicitly that reading anything beyond the diff invalidates its lens.
3. **Wave validation + one retry:** before treating a wave as done, verify every expected `<lens>.json` exists at its exact path and parses as a JSON array. A lens that wrote elsewhere (derived a wrong path) is recovered by moving its file, not re-running. Missing or invalid → re-dispatch that lens ONCE (fresh pane, same brief). Second failure → add its source to `{failed_layers}` and proceed degraded.
4. **Verify + consolidate:** Step 3b (every finding re-verified against `{worktree}` — mandatory) and Step 3c (dedupe, triage, reviewer-agreement set) exactly as the interactive flow.
5. **Machine output, no fix flow:** write `{out_dir}/consolidated.json` — surviving findings (with `verification` status and merged `source` arrays), `{failed_layers}`, counts, and the verdict (same thresholds as interactive). The final message is the Step-4 report. There is NO Step 5: the caller maps the verdict to its own action (Perkins: its review-event table).

### Re-review (when `{prior_findings}` is set)

- **Fix audit first:** classify every prior finding against the current worktree as `fixed` or `still-present` — re-read the cited code, do not trust the prior file's wording. Lead the report with this audit.
- **Carry-forward marker:** still-present findings are reported as `still present since round <N>` — carried into the current triage, never double-counted as new.
- **New findings** go through the normal verify + consolidate pass.
