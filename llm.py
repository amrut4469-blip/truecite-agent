import os
import time
from dotenv import load_dotenv

load_dotenv()

import neatlogs

neatlogs.init(
    api_key=os.environ["NEATLOGS_API_KEY"],
    workflow_name="truecite",
    instrumentations=["google_genai"],
)

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODELS = ["gemini-3.8-flash", "gemini-3.6-flash"]


def ask(prompt, report, json_mode=False):
    """Call Gemini. On failure retry once, then fall back to the next model."""
    config = None
    if json_mode:
        config = types.GenerateContentConfig(response_mime_type="application/json")
    for model in MODELS:
        for attempt in (1, 2):
            t0 = time.time()
            try:
                r = client.models.generate_content(model=model, contents=prompt, config=config)
                usage = getattr(r, "usage_metadata", None)
                report.event("llm_call", model=model, attempt=attempt,
                             seconds=round(time.time() - t0, 2),
                             tokens=getattr(usage, "total_token_count", None))
                return r.text
            except Exception as e:
                report.event("llm_error", model=model, attempt=attempt, error=str(e)[:200])
                time.sleep(3)
    raise RuntimeError("all models failed")
