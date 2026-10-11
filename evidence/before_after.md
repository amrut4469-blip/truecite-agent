# TrueCite: before vs after

Same question, one run each. Source: runs/*.json and metrics.py.

| Metric | v1 (before) | v2 (after) |
|---|---|---|
| Claims verified | 4/4 | 4/4 |
| Numbers in final answer | 7 | 5 |
| Numbers NOT backed by a verified quote | 2 ['2021', '500'] | 0 [] |
| LLM calls | 2 | 2 |
| Tokens (local report) | 3953 | 5952 |
| LLM errors | 0 | 0 |

Caveats: one run per version, LLM output varies between runs; latency is not
compared because Gemini was slower during the v1 run; v2 answers are assembled
from verified claims so they are shorter.

Token note: v2 used more tokens than v1 in these runs (local report 5952 vs 3953). The v2 change is code-only (no extra LLM call, both runs made 2 calls), so this is LLM output variation, not a cost saving or cost increase from v2. Neatlogs counts 71 + 4379 = 4450 tokens for the v2 trace, which differs from the local report's total; both are kept as evidence.
