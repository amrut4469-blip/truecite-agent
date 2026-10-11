import glob
import json
import re
import sys


def nums(text):
    text = re.sub(r"(?<=\d),(?=\d)", "", text)
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def measure(path):
    d = json.load(open(path))
    answer_nums = nums(d.get("answer", ""))
    backed = set()
    for c in d.get("claims", []):
        if c.get("verified"):
            backed |= nums(c["quote"])
    unbacked = sorted(answer_nums - backed)
    return {
        "file": path,
        "version": d.get("agent_version"),
        "claims_total": d.get("claims_total"),
        "claims_verified": d.get("claims_verified"),
        "answer_numbers": len(answer_nums),
        "numbers_not_backed": len(unbacked),
        "not_backed_list": unbacked,
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("runs/*.json"))[-1]
    print(json.dumps(measure(path), indent=2))
