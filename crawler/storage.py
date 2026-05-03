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

import csv
import os
import threading

from config import CONFIG

_counter = 0
_lock = threading.Lock()
_metadata_initialized = False


def _init_metadata(meta_path: str) -> None:
    """Write the CSV header if the metadata file does not exist yet."""
    global _metadata_initialized
    if not _metadata_initialized:
        if not os.path.exists(meta_path):
            with open(meta_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "url", "filename", "depth"])
        _metadata_initialized = True


def save_page(url: str, html: str, depth: int) -> str:
    """Persist `html` to disk and append a metadata row. Returns filename."""
    global _counter

    with _lock:
        _counter += 1
        page_id = _counter
        filename = f"{page_id:04d}.html"

        os.makedirs(CONFIG.output_dir, exist_ok=True)
        html_path = os.path.join(CONFIG.output_dir, filename)
        meta_path = os.path.join(CONFIG.output_dir, CONFIG.metadata_filename)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        _init_metadata(meta_path)
        with open(meta_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([page_id, url, filename, depth])

    return filename
