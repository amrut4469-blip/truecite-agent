import requests
from tools import HEADERS


def search_wikipedia(query, limit=3):
    """Return Wikipedia page URLs for a search query. Returns [] on any failure."""
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "opensearch", "search": query, "limit": limit, "format": "json"},
            headers=HEADERS,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()[3]
    except Exception:
        return []


if __name__ == "__main__":
    print(search_wikipedia("Unified Payments Interface"))
