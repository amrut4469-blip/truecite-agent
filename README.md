# TrueCite

A research agent that answers a question with Wikipedia sources and checks that every quote really exists in the fetched page. Built solo for #neatHack.

## How it works
1. LLM plans 2 Wikipedia search terms.
2. Python fetches the pages (`tools.py`, `wiki.py`); a failed fetch returns an error instead of crashing.
3. LLM writes an answer as claims, each with a source URL and an exact quote.
4. Python verifies each quote against the page text (`verify.py`, no LLM).
5. v2 builds the final answer only from verified claims.
6. Every run writes a local JSON report to `runs/` and a neatlogs trace.

Gemini errors (503): `llm.py` retries, then falls back to a second model.

## Run
    pip install -r requirements.txt
    cp your keys into .env (GEMINI_API_KEY, NEATLOGS_API_KEY)
    python agent.py          # v1
    python agent.py --v2     # v2
    python metrics.py        # numbers in the answer not backed by a verified quote

## Evidence (see `evidence/` and `runs/`)
- Before/after: `evidence/before_after.md`. One run per version: unbacked numbers in the answer went 2 to 0. Both runs made 2 LLM calls; v2 used more tokens (LLM variation, not a v2 effect).
- neatlogs: `evidence/neatlogs_v1_before_trace.png`, `neatlogs_v2_after_trace.png`.
- Recovery: `evidence/neatlogs_v2_503_retry_fallback_failed.png` and `runs/run_20261011_132755_v2.json`: Gemini returned 503 four times (retries, then model fallback); the agent failed gracefully with a report. A later run succeeded.
- Entire: `evidence/entire_checkpoint_*.txt`.
- Public post: https://x.com/AmrutWalke55/status/2109198109444329935

## Honest notes
- cfo.ai: not used. Signup needs a card and I could not provide one, so there is no cfo.ai business plan.
- neatlogs showed some traces as processing or incomplete (platform ingestion issue on Oct 11), so local JSON reports are kept as backup.
- Small evaluation: one question, one run per version.
