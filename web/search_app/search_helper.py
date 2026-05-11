"""Search helper module (P1).

Centralizes PyLucene JVM init and searcher access in one place so the
Django view (P2) does not call PyLucene directly. P2 implements the body
of `search`; this stub keeps the route working before that lands.

Expected return shape from `search`:
    list[dict] with keys: title, url, score, snippet (optional)
sorted by `score` in decreasing order.
"""
from __future__ import annotations

from typing import List, Dict, Any

from django.conf import settings


def init_jvm() -> None:
    """Attach the current thread to the PyLucene JVM.

    P2 will replace this stub with the real `lucene.initVM(...)` /
    `lucene.getVMEnv().attachCurrentThread()` calls.
    """
    return None


def open_searcher():
    """Return a Lucene IndexSearcher for `settings.INDEX_DIR`.

    P2 will implement this on top of PyLucene `DirectoryReader.open(...)`.
    """
    raise NotImplementedError(
        'search_helper.open_searcher: PyLucene wiring pending (P2).'
    )


def search(query: str, top_k: int | None = None) -> List[Dict[str, Any]]:
    """Run a query and return ranked results.

    P2 will implement the body: parse the query, search via PyLucene,
    collect (doc, score) pairs, sort by score descending, return top_k.
    """
    raise NotImplementedError(
        'search_helper.search: PyLucene search + ranking pending (P2).'
    )
