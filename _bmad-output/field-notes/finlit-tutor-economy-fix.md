# finlit-tutor-economy-fix — field notes (badge-out shard)

- DeepSeek truncation bugs: check `user://tutor_llm_log.jsonl` FIRST — this one was `finish_reason: stop` on every call; the CLIENT-side word-cap was the guillotine, not max_tokens/thinking. And "trim at sentence boundary" must be abbreviation-aware — the persona is literally named Mrs. K (the guard once returned "Mrs." as the whole answer).
- "Theoretical max wage" thinking must include the parents allowance (+$1/drop): couch-only math left a $0 doctrine margin ($1,800 = exactly the duplex price at day 15). Edge hunter caught it; price went $1,800→$2,000.
- Repricing an economy silently REVALUES old saves (book value derives from current tables) — bump the save schema version and let the corrupt-recovery path (identity kept) absorb them, or you fabricate wealth-climb.
