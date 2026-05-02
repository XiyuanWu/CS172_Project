"""URL filtering: duplicates, allowed domain, file extensions.

Owned by: Person 5.

Agreed interface (dev-doc-a.md, section 5):
    is_valid_url(url) -> bool

Plus a 'visited' tracking helper used by the main loop:
    mark_visited(url)
    has_visited(url) -> bool

Behavioral requirements:
    * Reject non-http(s) URLs.
    * If CONFIG.allowed_domain is non-empty, reject URLs whose host does
      not end with the allowed domain (e.g. 'ucr.edu' should match
      'www.ucr.edu' and 'cs.ucr.edu').
    * Reject URLs whose path ends with an extension in CONFIG.skip_extensions.
    * `has_visited` / `mark_visited` operate on a shared visited set.

This file is a STUB. Implementation is owned by P5.
"""

from __future__ import annotations

import threading
from urllib.parse import urlparse

from config import CONFIG

_visited: set[str] = set()
_lock = threading.Lock()


def is_valid_url(url: str) -> bool:
    """Return True if `url` is HTTP(S), in-domain, and not a skipped type."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in ("http", "https"):
        return False

    if CONFIG.allowed_domain:
        host = parsed.netloc.lower().split(":")[0]
        domain = CONFIG.allowed_domain.lower()
        if host != domain and not host.endswith("." + domain):
            return False

    path_lower = parsed.path.lower()
    if any(path_lower.endswith(ext) for ext in CONFIG.skip_extensions):
        return False

    return True


def has_visited(url: str) -> bool:
    with _lock:
        return url in _visited


def mark_visited(url: str) -> None:
    with _lock:
        _visited.add(url)
