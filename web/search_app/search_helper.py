"""Search helper module (P1/P2).

Centralizes PyLucene JVM init and searcher access in one place so the
Django view does not call PyLucene directly.

Expected return shape from `search`:
    list[dict] with keys: title, url, score, snippet (optional)
sorted by `score` in decreasing order.
"""
from __future__ import annotations

import sys
import os
from typing import List, Dict, Any

from django.conf import settings

# Allow search_logic.py to be imported from the repo root
_REPO_ROOT = str(settings.REPO_ROOT)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from search_logic import search as _search  # noqa: E402


def init_jvm() -> None:
    """Attach the current thread to the PyLucene JVM (handled by search_logic)."""
    return None


def open_searcher():
    """Searcher is managed internally by search_logic.pylucene_search."""
    pass


def search(query: str, top_k: int | None = None) -> List[Dict[str, Any]]:
    """Run a query and return ranked results sorted by score descending."""
    k = top_k if top_k is not None else settings.SEARCH_TOP_K
    return _search(query, index_dir=str(settings.INDEX_DIR), k=k)
