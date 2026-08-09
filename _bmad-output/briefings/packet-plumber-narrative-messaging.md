# Briefing: packet-plumber-narrative-messaging

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in the repo root on a feature branch off `main` (PR targets main)
- **Workflow:** **gds-create-narrative** + the storyteller craft (Sophia). This is a NARRATIVE + MESSAGING + TONE deliverable — propose the voice; the user reacts via lavish. Orchestration overrides per standing orders. Self-review before PR: bmad-review-edge-case-hunter + bmad-editorial-review-prose (messaging copy must be tight).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (creative/docs deliverable).

## Mission

Produce the **narrative + messaging + tone spec** for Packet Plumber — the voice that makes "save the internet" feel *real*, urgent, and personality-driven. The GDD cites **Two Point Hospital's crisis-management personality** as a reference — so the tone lives somewhere between genuine stakes (the internet is breaking) and characterful warmth (not grimdark). This runs IN PARALLEL with the prototype fun-test and feeds both the in-game copy AND the Steam-page story pitch.

## Source material (read ALL)

1. **`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`** — the experience: *"The internet is breaking. Millions can't watch YouTube. YOU are the only thing standing between civilization and 'Error 404.'"* The pitch sells the EXPERIENCE.
2. **`_bmad-output/planning-artifacts/gdds/.../gdd.md`** — the 6 eras (ARPANET → Email/Web → Streaming Surge → Real-Time → Cloud → Software-Defined Edge), the 9 packet types, the crisis model, the "Error 404" loss state, the satirical brands (YouTune, Glitch, Amazoon). The Two Point Hospital personality reference.
3. **`_bmad-output/planning-artifacts/gdds/.../epics.md`** + **decision-log.md** — the design intent.
4. **`/Users/moses/code/docs/game-design-references.md`** — Tyroller (experience-first; the capsule/trailer is the story) + Brush.

## What to define (the narrative + messaging + tone spec)

### 1. TONE / VOICE (the core — the user explicitly wants this pinned)
- Define the **tone spectrum**: where does Packet Plumber sit? (Urgent-but-warm? Wry? Personality-driven like Two Point Hospital? Earnest-heroic?) Propose the voice with rationale + examples.
- The **narrator/persona**: who's speaking to the player? (A weary CIO? An upbeat AI ops assistant? The internet itself?) The voice the player hears in alerts, era-transitions, the tutorial.
- **Tone consistency rules** — how the voice bends across calm (redesign mode) vs crisis (triage mode) vs celebration (surge survived).

### 2. The core narrative
- The **"save the internet" framing** — made concrete. Who is the player? Why are THEY the only one? The fantasy setup.
- **Era-by-era story beats** — each of the 6 eras as a narrative chapter: what's the internet BECOMING, what's the stakes shift, the signature moment (the streaming surge, the always-on real-time era, the cloud explosion, the SDN abstraction). The internet evolves as a CHARACTER.
- The **loss narrative** — what does "Error 404" MEAN in-fiction? (Civilization loses connection; the stakes of failure.)

### 3. In-game MESSAGING (the copy the player reads)
- **Crisis alerts** — the warning/escalation copy (node 🟡→🔴, the forecast "weather report", the surge incoming). Urgent but clear.
- **Era-transition moments** — the "the internet has evolved" beats (new packet types appear, infrastructure ages). Milestone copy.
- **Success/celebration copy** — "surge survived," SLA restored, era advanced.
- **The tutorial/onboarding voice** — how the player learns (the GDD's "discover through consequence" — the voice guides without hand-holding).
- **Satirical brand names** — flesh out the roster (YouTune = YouTube, Glitch = Twitch, Amazoon = Amazon, + banking/gaming/IoT equivalents). Consistent naming conventions.

### 4. The Steam-page story pitch
- The capsule/trailer narrative (Tyroller: design the appeal first). The one-paragraph + the taglines that sell the EXPERIENCE.

## Deliverable + placement
- Narrative/messaging spec at `_bmad-output/planning-artifacts/narrative/narrative-v1.md` (or per the skill's structure).
- Include **concrete copy samples** (write actual alert lines, era-transition text, brand names, taglines) — not just descriptions of tone. The user reacts to REAL words.

## Constraints (do not violate — forge/GDD-locked)
- **Experience-first** (Tyroller): the narrative serves the "save the internet" fantasy.
- **Two Point Hospital personality reference** — characterful, not grimdark. Urgent stakes + warmth.
- **Satirical brands only** (YouTune, Amazoon, Glitch...) — never real trademarks.
- **No em-dashes** in any copy (global ban, CI-guarded).
- The voice must work **cross-culturally** (the internet fantasy is universal; avoid region-specific idioms that don't translate — the forge noted the "usually a parent" expat-incoherence lesson).
- Crises are FAIR/predictable — the messaging never blames the player unfairly; it telegraphs (the "you should have seen this coming" design).

## Review loop (lavish — BEFORE the PR)
Creative deliverable: render via **lavish** with the tone/voice demonstrated (actual copy samples, era-story beats, the Steam pitch, the brand roster) + post the review URL. The user reacts to the proposed voice. Do NOT open the PR until the verdict.

## Acceptance
- Narrative + messaging + tone spec with CONCRETE copy (alerts, era-beats, brands, taglines, the Steam pitch).
- A pinned tone/voice with rationale + the narrator persona.
- Era-by-era story beats.
- No em-dashes, satirical brands only, cross-culturally clean.
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-narrative-messaging working` at start
- `/Users/moses/code/bin/ledger note packet-plumber-narrative-messaging "lavish review posted: <url>"` when up
- `/Users/moses/code/bin/ledger set packet-plumber-narrative-messaging in-review "PR <url>"` when PR opens
- `herdr notification show "pp-narrative" --body "<one-line>"` on finish
- Final message: the tone/voice summary + key copy samples, lavish URL, open questions.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-narrative-messaging · base: main
