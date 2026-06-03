"""
Person 2 — Search interface
"""

import os
import csv
from bs4 import BeautifulSoup


def clean_query(query):
    return query.strip().lower()


def extract_title(html):
    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        return soup.title.text.strip()

    return "Untitled"


def search(query_text, index_dir="index", k=10):
    """
    Temporary implementation.
    Keeps same interface that PyLucene will use later.
    """

    query = clean_query(query_text)

    if not query:
        return []

    metadata = "output/metadata.csv"

    if not os.path.exists(metadata):
        return []

    results = []

    with open(metadata, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        rank = 1

        for row in reader:

            filename = row["filename"]
            html_file = os.path.join("output", filename)

            if not os.path.exists(html_file):
                continue

            with open(html_file, "r", encoding="utf-8", errors="ignore") as page:
                html = page.read()

            title = extract_title(html)

            if query in html.lower():

                results.append({
                    "rank": rank,
                    "title": title,
                    "url": row["url"],
                    "filename": filename,
                    "score": 1.0,
                })

                rank += 1

            if len(results) >= k:
                break

    return results


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