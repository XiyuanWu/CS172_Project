"""
Person 2 — Search Logic

Responsibilities:
1. Parse query
2. Call PyLucene
3. Retrieve scores
4. Sort top-k
5. Handle field analyzers

Expected index fields:
title
body
description
url
filename
depth
updated_time
"""


try:
    import lucene

    from org.apache.lucene.store import FSDirectory
    from org.apache.lucene.index import DirectoryReader
    from org.apache.lucene.search import IndexSearcher

    from org.apache.lucene.queryparser.classic import (
        MultiFieldQueryParser
    )

    from org.apache.lucene.analysis.standard import (
        StandardAnalyzer
    )

    PYLUCENE_AVAILABLE = True

except ImportError:

    PYLUCENE_AVAILABLE = False


DEFAULT_FIELDS = [
    "title",
    "description",
    "body",
    "url"
]


FIELD_BOOSTS = {
    "title": 3.0,
    "description": 2.0,
    "body": 1.0,
    "url": 0.5
}


def parse_query(query_text):

    query = query_text.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    return query


def sort_results(results, k):

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:k]


def pylucene_search(
    query_text,
    index_dir="index",
    k=10
):

    if not PYLUCENE_AVAILABLE:

        raise RuntimeError(
            "PyLucene not installed."
        )

    lucene.initVM()

    directory = FSDirectory.open(
        index_dir
    )

    reader = DirectoryReader.open(
        directory
    )

    searcher = IndexSearcher(
        reader
    )

    analyzer = StandardAnalyzer()

    parser = MultiFieldQueryParser(
        DEFAULT_FIELDS,
        analyzer
    )

    parser.setMultiFields(
        DEFAULT_FIELDS
    )

    query = parser.parse(
        query_text
    )

    hits = searcher.search(
        query,
        k
    )

    results = []

    for rank, hit in enumerate(
        hits.scoreDocs,
        start=1
    ):

        doc = searcher.doc(
            hit.doc
        )

        results.append({

            "rank": rank,

            "title":
                doc.get("title"),

            "url":
                doc.get("url"),

            "filename":
                doc.get("filename"),

            "score":
                round(
                    hit.score,
                    4
                ),

            "snippet":
                doc.get(
                    "description"
                )
        })

    reader.close()

    return sort_results(
        results,
        k
    )


def search(
    query_text,
    index_dir="index",
    k=10
):

    query = parse_query(
        query_text
    )

    return pylucene_search(
        query,
        index_dir=index_dir,
        k=k
    )


if __name__ == "__main__":

    import sys

    query = " ".join(
        sys.argv[1:]
    )

    if not query:

        print(
            "Usage: python search_logic.py QUERY"
        )

        exit()

    try:

        results = search(
            query
        )

        for r in results:

            print()

            print(
                "Rank:",
                r["rank"]
            )

            print(
                "Title:",
                r["title"]
            )

            print(
                "Score:",
                r["score"]
            )

            print(
                "URL:",
                r["url"]
            )

    except Exception as e:

        print(
            "Search failed:"
        )

        print(e)