import json
import sys

from llm import ask  # llm.py runs neatlogs.init() first
from neatlogs import span
from tools import fetch_page
from wiki import search_wikipedia
from verify import verify_quote
from report import RunReport

DEFAULT_Q = "What is UPI in India and how did its usage grow?"


def parse_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    return json.loads(text)


def plan(question, report):
    prompt = (
        "You are a research planner. Give 2 short Wikipedia search terms that would "
        'find the best pages for this question. Reply ONLY as JSON: {"search_terms": ["..", ".."]}'
        "\n\nQuestion: " + question
    )
    return parse_json(ask(prompt, report, json_mode=True))["search_terms"][:2]


def gather(terms, report):
    pages = {}
    for term in terms:
        for url in search_wikipedia(term, limit=3):
            if url in pages:
                continue
            res = fetch_page(url)
            report.event("fetch", url=url, ok=res["ok"], error=res["error"])
            if res["ok"]:
                pages[url] = res["text"]
                break  # on failure the loop tries the next candidate URL
    return pages


def compose(question, pages, report):
    sources = "\n\n".join(f"SOURCE {u}\n{t[:8000]}" for u, t in pages.items())
    prompt = (
        "Answer the question using ONLY the sources below. Reply ONLY as JSON: "
        '{"answer": "short answer", "claims": [{"claim": "..", "url": "..", "quote": ".."}]}. '
        "Each quote must be copied exactly from that source (max 25 words).\n\n"
        f"Question: {question}\n\n{sources}"
    )
    return parse_json(ask(prompt, report, json_mode=True))


@span(kind="WORKFLOW", name="truecite_run")
def run(question):
    report = RunReport(question, "v1")
    try:
        terms = plan(question, report)
        report.event("plan", search_terms=terms)
        pages = gather(terms, report)
        if not pages:
            raise RuntimeError("no pages could be fetched")
        out = compose(question, pages, report)
        checked = []
        for c in out["claims"]:
            ok = c["url"] in pages and verify_quote(c["quote"], pages[c["url"]])
            report.event("verify", claim=c["claim"], url=c["url"], verified=ok)
            checked.append({**c, "verified": ok})
        total = len(checked)
        good = sum(c["verified"] for c in checked)
        report.set("answer", out["answer"])
        report.set("claims", checked)
        report.set("claims_total", total)
        report.set("claims_verified", good)
        report.set("unverified_in_final", total - good)
    except Exception as e:
        report.set("error", str(e))
    path = report.save()
    print("report:", path)
    print("claims:", report.data.get("claims_total"),
          "verified:", report.data.get("claims_verified"),
          "error:", report.data.get("error"))


if __name__ == "__main__":
    run(" ".join(sys.argv[1:]) or DEFAULT_Q)
