# Constellation v2 — same live PP3D planet, NOT Odin/Dublin

## Latest user ruling (verbatim)

> For the constellation, we are using, there's nothing like Dublin board. what we are using is the current planet map we have for example we have level 1 we want to just display that same planet and all the assets and all the animations maintained in just a flat map. map so like um we don't have the tiny planets but the same look exactly the tiny planets it look but flat. We want to see the water bodies, the boats, the land, the greenery, everything should remain exactly the same.

Follow-up, verbatim:
> I hope that is clear. If it's not clear, then you should make sure you seek clarification because I don't want this to be done wrongly. I don't want to see the Odin map in the 3D game.

## Binding interpretation — no ambiguity on the reference

**The reference is the CURRENT PP3D planet and its actual live world. There is NO Odin or Dublin map to reproduce, import, restyle from, or show in the 3D game.** The earlier Odin-framing phrase in Gru's brief was wrong for this task and is superseded. The stored `packet-plumber/goldens/dublin_board/30000ms.png` is NOT an approved target. Do not use its map geometry, palette, roads, framing design or UI as the flat mode.

The requested change is spatial presentation: take the same current planet and flatten it. Retain its existing art, materials, colors, water bodies, land/coast relationships, greenery, boats, other present assets and running animations. It must remain the same living scene—not a screenshot, generic 2D map, substitute board, static duplicate, or newly generated geography. Sim/game state and animation continuity survive both directions of the morph; do not freeze, reset or replace them to make a still appear correct.

Level1 is the user's concrete example/reference. The already-briefed shared/all-level support remains; do not invent different worlds for later levels. Earlier explicit water-present, no surrounding starfield/space in flat mode, and smooth reversible zoom-out morph requirements remain. Removing the surrounding space is not permission to redesign the planet's content or art. Changes inherently required by flattening/projection must not be disguised as exact equality of every screen pixel.

## Acceptance / clarification discipline

- Inspect the ACTUAL current PP3D world/canonical assets and code, then implement same-world projection. Closed PR26 mechanics may be reused only after verification; its rejected presentation and any Odin golden are not targets.
- Compare globe/flat at matched simulation state: the same terrain/water, assets, boats/greenery and current animation state must be accounted for. Preserve existing visual character and behavior, rather than ticking only object-count or byte-hash checks.
- Running water/boat/other scene animations continue in flat mode and through reversible transition; state/progression does not restart. Demonstrate this within the existing bounded test/capture allowance, not by a still alone. If additional native motion evidence is genuinely needed, request a narrow allowance; no undeclared run, fake motion verification or budget reset.
- Before a deliberate omission, aesthetic substitution, animation compromise, or alternative to same-world flattening: STOP and seek clarification through Silas/Gru. The user explicitly prefers clarification to a wrong implementation. Explain the concrete unresolved choice; do not reopen the already-answered 'which reference?' question.
- Final look acceptance stays user-owned. No claim of exact visual/behavioral parity before actual evidence.

## Immediate routing

This resolves pYQ's Q1 in chat. Silas relays the complete ruling to the SAME `packet-plumber-3d-constellation-view-v2` parent w85:pYQ on Astra/xhigh. Resume that existing row/session/worktree after normal resolution of its specific Lavish question. No duplicate parent, no new dispatch, no restart of the old PR26 lane.

The open clarification session is `http://127.0.0.1:4387/session/2cb962423d2e9009`, artifact `/Users/moses/.herdr/worktrees/packet-plumber-3d/constellation-view-v2/.lavish/constellation-v2-reference.html`. The user need not answer twice. Check for any newer pending user feedback first; preserve/deliver it if present. With none, normally end this exact agent-owned clarification session so the foreground poll returns and the queued ruling is processed; do not kill the poll, inject a forged user answer, consume unrelated feedback or reopen an ended session.

Gru has amended both staged v2 and release briefs to remove the misleading Odin target. This separate file is the full user-wording source. Same skills (`bmad-build`, native Astra vision, full `code-review` at PR), model Astra/xhigh, main base, pr_review1 and existing finite native allowance. No new native entries, external reference campaign, game launch, code change by Silas/Gru, or change to other jobs. The unrelated router-placement issue #34 is future-only and MUST NOT be folded into this task.
