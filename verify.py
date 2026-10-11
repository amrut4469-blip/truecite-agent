import re


def _norm(s):
    s = s.lower()
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"[^a-z0-9% ]+", " ", s)
    return " ".join(s.split())


def verify_quote(quote, page_text):
    """True only if the quote really appears in the page text (after normalizing)."""
    q = _norm(quote)
    return len(q) >= 15 and q in _norm(page_text)


if __name__ == "__main__":
    page = "UPI was launched in 2016 by NPCI. It allows instant bank-to-bank transfers."
    print(verify_quote("launched in 2016 by NPCI", page))
    print(verify_quote("launched in 2012 by RBI", page))
