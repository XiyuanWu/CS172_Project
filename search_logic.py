"""
Person 2 — Search Logic

Responsibilities:
- Parse user query
- Call Lucene searcher
- Get scores
- Return top-k results sorted by score
"""

from typing import List, Dict, Any


DEFAULT_SEARCH_FIELDS = {
    "title": 3.0,
    "description": 2.0,
    "body": 1.0,
    "url": 0.5,
}


def clean_query(query_text: str) -> str:
    """Clean and validate user query."""
    if query_text is None:
        return ""

    return query_text.strip()


def search(query_text: str, index_dir: str = "index", k: int = 10) -> List[Dict[str, Any]]:
    """
    Main function Django will call.

    Returns:
        List of result dictionaries ordered by decreasing Lucene score.
    """
    query_text = clean_query(query_text)

    if not query_text:
        return []

    # TODO: Replace this placeholder with PyLucene search code.
    # This lets Person 1 build Django around your interface immediately.
    results = [
        {
            "rank": 1,
            "title": "Placeholder Result",
            "url": "https://example.com",
            "filename": "0001.html",
            "score": 0.0,
            "snippet": f"Search logic received query: {query_text}",
        }
    ]

    return results[:k]


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    if not query:
        print("Usage: python search_logic.py <search query>")
        sys.exit(1)

    results = search(query)

    for result in results:
        print(f"{result['rank']}. {result['title']}")
        print(f"Score: {result['score']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")
        print()