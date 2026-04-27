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


def is_valid_url(url: str) -> bool:
    """Return True if `url` is HTTP(S), in-domain, and not a skipped type."""
    raise NotImplementedError("P5: implement is_valid_url(url)")


def has_visited(url: str) -> bool:
    raise NotImplementedError("P5: implement has_visited(url)")


def mark_visited(url: str) -> None:
    raise NotImplementedError("P5: implement mark_visited(url)")
