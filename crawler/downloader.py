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

import logging
import socket
import time
from typing import Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import CONFIG

log = logging.getLogger(__name__)


def download(url: str) -> Tuple[Optional[str], int]:
    """Fetch a URL and return (html_text_or_None, http_status_code)."""

    request = Request(
        url,
        headers={
            "User-Agent": CONFIG.user_agent,
            "Accept": "text/html,application/xhtml+xml",
        },
    )

    attempts = CONFIG.max_retries + 1

    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=CONFIG.request_timeout) as response:
                status_code = response.getcode()

                if status_code < 200 or status_code >= 300:
                    return None, status_code

                content_type = response.headers.get("Content-Type", "").lower()

                if (
                    "text/html" not in content_type
                    and "application/xhtml+xml" not in content_type
                ):
                    return None, status_code

                charset = response.headers.get_content_charset() or "utf-8"
                raw_data = response.read()
                html = raw_data.decode(charset, errors="replace")

                return html, status_code

        except HTTPError as e:
            log.debug("HTTP error (%s) for %s", e.code, url)
            return None, e.code

        except socket.timeout:
            log.debug("Timeout attempt %d/%d for %s", attempt + 1, attempts, url)

        except URLError as e:
            log.debug(
                "Network error attempt %d/%d for %s: %s",
                attempt + 1,
                attempts,
                url,
                e,
            )

        except Exception as e:
            log.debug(
                "Unexpected error attempt %d/%d for %s: %s",
                attempt + 1,
                attempts,
                url,
                e,
            )

        if attempt < attempts - 1:
            time.sleep(0.5)

    return None, 0