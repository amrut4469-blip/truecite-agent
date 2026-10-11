import json
import os
import time
from datetime import datetime


class RunReport:
    """Local JSON record of one agent run (backup evidence if neatlogs ingestion fails)."""

    def __init__(self, question, version):
        self.started = time.time()
        self.data = {
            "question": question,
            "agent_version": version,
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "events": [],
        }

    def event(self, kind, **info):
        self.data["events"].append({
            "t": round(time.time() - self.started, 2),
            "kind": kind,
            **info,
        })

    def set(self, key, value):
        self.data[key] = value

    def save(self, folder="runs"):
        os.makedirs(folder, exist_ok=True)
        self.data["duration_s"] = round(time.time() - self.started, 2)
        name = datetime.now().strftime("run_%Y%m%d_%H%M%S") + f"_{self.data['agent_version']}.json"
        path = os.path.join(folder, name)
        with open(path, "w") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        return path


if __name__ == "__main__":
    r = RunReport("test question", "test")
    r.event("fetch", url="https://example.com", ok=False, error="404")
    r.event("fetch", url="https://example.org", ok=True)
    r.set("result", "demo")
    print(r.save(folder="/tmp/truecite_test"))
