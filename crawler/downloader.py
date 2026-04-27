"""HTTP downloader.

Owned by: Person 3.

Agreed interface (dev-doc-a.md, section 5):
    download(url) -> (html, status_code)

Behavioral requirements:
    * Honor CONFIG.request_timeout and CONFIG.user_agent.
    * Follow redirects.
    * Return (html_text, status_code) on success.
    * On timeout / network error / non-HTML / non-2xx response, return
      (None, status_code_or_0) so the caller can skip the page.
    * Only return content whose Content-Type indicates HTML.

This file is a STUB. Implementation is owned by P3.
"""

from __future__ import annotations

from typing import Optional, Tuple


def download(url: str) -> Tuple[Optional[str], int]:
    """Fetch `url` and return (html_text_or_None, http_status_code)."""
    raise NotImplementedError("P3: implement download(url)")
