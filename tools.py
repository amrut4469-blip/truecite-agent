import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "TrueCite/0.1 (hackathon project)"}


def fetch_page(url, timeout=10):
    """Fetch a page and return clean text. Never raises; returns ok=False on failure."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = " ".join(soup.get_text(" ").split())
        return {"url": url, "ok": True, "text": text[:20000], "error": None}
    except Exception as e:
        return {"url": url, "ok": False, "text": "", "error": str(e)}


if __name__ == "__main__":
    good = fetch_page("https://en.wikipedia.org/wiki/Unified_Payments_Interface")
    bad = fetch_page("https://en.wikipedia.org/wiki/This_page_does_not_exist_xyz123")
    print("good:", good["ok"], len(good["text"]))
    print("bad:", bad["ok"], bad["error"])
