import os
from dotenv import load_dotenv
load_dotenv()

import neatlogs
neatlogs.init(
    api_key=os.environ["NEATLOGS_API_KEY"],
    workflow_name="truecite",
    instrumentations=["google_genai"],
)

from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
r = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say hi in one short sentence.",
)
print(r.text)
