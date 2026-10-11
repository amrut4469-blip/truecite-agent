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
