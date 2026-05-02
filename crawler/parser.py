"""HTML link extraction and URL normalization.

Owned by: Jake Wang.

Agreed interface (dev-doc-a.md, section 5):
    extract_links(html, base_url) -> [urls]

Behavioral requirements:
    * Parse all <a href="..."> hyperlinks from `html`.
    * Convert relative links to absolute URLs using `base_url`.
    * Remove URL fragments (#section).
    * Normalize URLs (lowercase scheme/host, strip default ports, etc.)
      so '<base>/page' and '<base>/page/' don't both pass through later
      duplicate checks if they really point to the same resource.
    * Skip non-http/https URLs (e.g. mailto:, javascript:) and empty hrefs.
    * Return de-duplicated URLs in encounter order.
"""

from __future__ import annotations
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse, urlunparse


def extract_links(html: str, base_url: str) -> List[str]:
    
    # List of uncleaned URLs or local links found in html
    hrefs = []

    # Parse HTML with BeautifulSoup/lxml for all <a href> link strings
    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all("a", href=True):
        hrefs.append(tag["href"]) # Append raw href string, e.g. "/about" or "https://..."

    # For each <a href>: urljoin -> urldefrag -> normalize
    # and prune blank results or non-http/https URLs (e.g., mailto:, javascript:)
    results = []
    seen = set()

    for href in hrefs:
        # skip if empty href
        if not href:
            continue

        # relative to absolute
        absolute = urljoin(base_url, href)

        # strip fragment (#section)
        defragged, _ = urldefrag(absolute)

        # normalize
        parsed = urlparse(defragged)

        # skip non-http/https URLs
        if parsed.scheme not in ("http", "https"):
            continue

        # extract scheme/host/port; hostname is always lowercase, unlike netloc
        host = parsed.hostname or ""
        port = parsed.port
        scheme = parsed.scheme.lower()

        # strip default ports so http://site.com:80 and http://site.com are treated the same
        if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
            port = None

        # rebuild netloc (host:port), omitting port when it was stripped above
        netloc = host if port is None else f"{host}:{port}"
        # strip trailing slash so /page/ and /page count as the same URL; keep bare /
        path = parsed.path.rstrip("/") or "/"

        # reassemble the full normalized URL from its components
        normalized = urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))

        # Step 4: de-duplicate
        if normalized not in seen:
            seen.add(normalized)
            results.append(normalized)

    return results
