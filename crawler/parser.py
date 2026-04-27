"""HTML link extraction and URL normalization.

Owned by: Person 4.

Agreed interface (dev-doc-a.md, section 5):
    extract_links(html, base_url) -> [urls]

Behavioral requirements:
    * Parse all <a href="..."> hyperlinks from `html`.
    * Convert relative URLs to absolute URLs using `base_url`.
    * Remove URL fragments (#section).
    * Normalize URLs (lowercase scheme/host, strip default ports, etc.)
      so '<base>/page' and '<base>/page/' don't both pass through later
      duplicate checks if they really point to the same resource.
    * Return de-duplicated URLs in encounter order.

This file is a STUB. Implementation is owned by P4.
"""

from __future__ import annotations

from typing import List


def extract_links(html: str, base_url: str) -> List[str]:
    """Return a list of absolute, normalized URLs found in `html`."""
    raise NotImplementedError("P4: implement extract_links(html, base_url)")
