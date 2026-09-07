# Quota regime policy — standing notes (probes overwrite quota-regime.json; policy lives here)

## 2026-09-07 — SUPERSEDED by the GPT chain (user ruling): the quota regime below is RETIRED.
- Reasoning tier (Gru/Bob/Perkins + all 3D work) = `openai-codex/gpt-6-astra` @ xhigh;
  minions/mega-minions (non-3D) = `openai-codex/gpt-5.6-sol` @ xhigh; Silas = `openai-codex/gpt-5.6-luna` @ max.
- Subscription billing: the failure mode is rate-limit/auth, not per-token balance. Probe-first still applies
  (`bin/quota-probe` default = openai-codex/gpt-6-astra); the chatty-OK false-DOWN matcher bug still applies
  (reply CONTENT decides). k3/glm/deepseek doctrine below is ARCHIVED for the record only.
- Vision: all three GPT models are natively multimodal — native vision on the chain; KYLE routing only for
  legacy blind sessions.

---
# Quota regime policy — standing notes (probes overwrite quota-regime.json; policy lives here)

## 2026-09-04 ~05:00Z — USER RULING: "we are out of kimi" (relayed by Gru)
- kimi k3 weekly 7-day cap (hit 2026-09-04 ~04:57Z): NO plan upgrade — k3 stays
  OUT until the window resets on its own. Do not schedule anything off the
  provider's stated reset time; only the probe decides (standing law).
- Reasoning tier rides `zai-coding-cn/glm-5.3` probe-gated per playbook Model
  policy; HOLD if glm-5.3 dies too (no v4-pro, no flash for reasoning).
- Vision: KYLE (zai-coding-cn/glm-5.3-flash, natively multimodal) is the
  screening layer for visual lanes while k3 is out; k3's inline vision returns
  only when the probe flips it back.
- E1 precedent (packet-plumber-3d-e1-tiny-planet): where a lane exits on a
  USER-PLAY gate, the play session IS the look verdict — no k3 aesthetic
  re-check owed post-hoc.
