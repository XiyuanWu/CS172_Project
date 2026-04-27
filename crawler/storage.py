"""Page + metadata storage.

Owned by: Person 5.

Agreed interface (dev-doc-a.md, section 5):
    save_page(url, html, depth) -> filename

Behavioral requirements:
    * Save HTML files into CONFIG.output_dir as 0001.html, 0002.html, ...
      (zero-padded sequential ids).
    * Append a row to CONFIG.output_dir/CONFIG.metadata_filename with
      columns: id, url, filename, depth.
    * Be safe to call concurrently if P3 is multi-threaded (a lock is OK).
    * Return the saved filename (relative to output_dir).

This file is a STUB. Implementation is owned by P5.
"""

from __future__ import annotations


def save_page(url: str, html: str, depth: int) -> str:
    """Persist `html` to disk and append a metadata row. Returns filename."""
    raise NotImplementedError("P5: implement save_page(url, html, depth)")
