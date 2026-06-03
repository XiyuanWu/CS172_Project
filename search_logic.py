"""
Person 2 — Search Logic

Public function:
    search(query_text, index_dir="index", k=10)

Django should call this function.

Current behavior:
- Uses PyLucene if installed.
- Falls back to local HTML search if PyLucene is unavailable.
"""

import os
import csv
import re
from bs4 import BeautifulSoup


try:
    import lucene
    PYLUCENE_AVAILABLE = True
except ImportError:
    lucene = None
    PYLUCENE_AVAILABLE = False


OUTPUT_DIR = "output"
METADATA_FILE = "metadata.csv"


def clean_query(query):
    if query is None:
        return ""
    return query.strip().lower()


def tokenize(text):
    if text is None:
        return []
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def extract_html_fields(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = "Untitled"
    if soup.title and soup.title.text:
        title = soup.title.text.strip()

    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag.get("content").strip()

    updated_time = ""
    updated_tag = soup.find("meta", attrs={"property": "og:updated_time"})
    if updated_tag and updated_tag.get("content"):
        updated_time = updated_tag.get("content").strip()

    body = soup.get_text(" ", strip=True)

    return {
        "title": title,
        "description": description,
        "updated_time": updated_time,
        "body": body,
    }


def make_snippet(text, query_terms, max_length=220):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text).strip()
    lower_text = text.lower()

    first_match = -1

    for term in query_terms:
        pos = lower_text.find(term)
        if pos != -1:
            first_match = pos
            break

    if first_match == -1:
        snippet = text[:max_length]
    else:
        start = max(first_match - 80, 0)
        end = min(start + max_length, len(text))
        snippet = text[start:end]

    snippet = snippet.strip()

    if len(snippet) >= max_length:
        snippet += "..."

    return snippet


def score_document(query_terms, title, description, body, url):
    title_tokens = tokenize(title)
    description_tokens = tokenize(description)
    body_tokens = tokenize(body)
    url_tokens = tokenize(url)

    score = 0.0

    for term in query_terms:
        score += title_tokens.count(term) * 3.0
        score += description_tokens.count(term) * 2.0
        score += body_tokens.count(term) * 1.0
        score += url_tokens.count(term) * 0.5

    return score


def fallback_search(query_text, index_dir="index", k=10):
    query = clean_query(query_text)

    if not query:
        return []

    query_terms = tokenize(query)

    if not query_terms:
        return []

    metadata_path = os.path.join(OUTPUT_DIR, METADATA_FILE)

    if not os.path.exists(metadata_path):
        return []

    results = []

    with open(metadata_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            filename = row.get("filename", "")
            url = row.get("url", "")
            depth = row.get("depth", "")

            html_path = os.path.join(OUTPUT_DIR, filename)

            if not os.path.exists(html_path):
                continue

            with open(html_path, "r", encoding="utf-8", errors="ignore") as page:
                html = page.read()

            fields = extract_html_fields(html)

            score = score_document(
                query_terms=query_terms,
                title=fields["title"],
                description=fields["description"],
                body=fields["body"],
                url=url,
            )

            if score <= 0:
                continue

            snippet_source = fields["description"] or fields["body"]

            results.append({
                "title": fields["title"],
                "url": url,
                "filename": filename,
                "depth": depth,
                "updated_time": fields["updated_time"],
                "score": round(score, 3),
                "snippet": make_snippet(snippet_source, query_terms),
            })

    results.sort(key=lambda item: item["score"], reverse=True)

    ranked_results = []

    for rank, result in enumerate(results[:k], start=1):
        result["rank"] = rank
        ranked_results.append(result)

    return ranked_results


def pylucene_search(query_text, index_dir="index", k=10):
    """
    Future PyLucene implementation.

    Person 4's indexer should create these fields:
    title, body, description, url, filename, depth, updated_time

    This function will:
    - open the Lucene index from index_dir
    - parse query_text across title/description/body/url
    - retrieve top-k results with Lucene scores
    - return the same dictionary format as fallback_search
    """
    raise NotImplementedError(
        "PyLucene is not installed in this environment yet. "
        "Install PyLucene or use fallback_search for testing."
    )


def search(query_text, index_dir="index", k=10, use_pylucene=True):
    """
    Main public function for Django.

    Django should call:
        search(query_text, index_dir='index', k=10)

    If PyLucene is available, this will use PyLucene.
    Otherwise, it falls back to local HTML search for testing.
    """
    if use_pylucene and PYLUCENE_AVAILABLE:
        return pylucene_search(query_text, index_dir=index_dir, k=k)

    return fallback_search(query_text, index_dir=index_dir, k=k)


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:])

    results = search(query)

    if not results:
        print("No results.")
    else:
        for r in results:
            print("\nRank:", r["rank"])
            print("Title:", r["title"])
            print("Score:", r["score"])
            print("URL:", r["url"])
            print("File:", r["filename"])
            print("Snippet:", r["snippet"])