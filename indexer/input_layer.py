"""Indexer input layer — Person 3.

Responsibilities:
  * Walk crawled_pages/ and locate HTML files.
  * Load and join metadata.csv so each page record carries its URL, depth,
    and any other stored fields.
  * Yield self-contained page dicts ready for the Lucene layer (Person 4).

Public API
----------
load_metadata(metadata_csv: Path) -> dict[str, dict]
    Returns a mapping  filename -> {url, depth, id}  built from metadata.csv.

iter_pages(crawl_dir: Path, metadata: dict) -> Iterator[dict]
    Yields one dict per page:
        {
            "filename":  "0001.html",
            "html":      "<html>...</html>",
            "url":       "https://example.com/page",
            "depth":     "2",
            "id":        "1",
        }
    Pages whose HTML file is missing or unreadable are skipped with a warning.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Iterator

log = logging.getLogger(__name__)


def load_metadata(metadata_csv: Path) -> dict[str, dict]:
    """Read metadata.csv and return a filename-keyed dict.

    Expected CSV columns (from Part A storage.py):  id, url, filename, depth

    Returns
    -------
    dict mapping  filename (str) -> {"id": str, "url": str, "depth": str}
    """
    if not metadata_csv.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_csv}")

    metadata: dict[str, dict] = {}

    with open(metadata_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get("filename", "").strip()
            if not filename:
                continue
            metadata[filename] = {
                "id":    row.get("id",    "").strip(),
                "url":   row.get("url",   "").strip(),
                "depth": row.get("depth", "0").strip(),
            }

    log.info("Loaded metadata for %d pages from %s", len(metadata), metadata_csv)
    return metadata


def iter_pages(
    crawl_dir: Path,
    metadata: dict[str, dict],
) -> Iterator[dict]:
    """Yield one page dict per HTML file found in crawl_dir.

    Only files listed in metadata are yielded so the metadata CSV acts as
    the authoritative index of what was crawled.  HTML files present on
    disk but absent from the CSV are silently ignored.

    Parameters
    ----------
    crawl_dir:
        Directory produced by Part A (contains 0001.html, 0002.html, …).
    metadata:
        Output of load_metadata().

    Yields
    ------
    dict with keys: filename, html, url, depth, id
    """
    if not crawl_dir.exists():
        raise FileNotFoundError(f"Crawl directory not found: {crawl_dir}")

    yielded = 0
    skipped = 0

    for filename, meta in metadata.items():
        html_path = crawl_dir / filename

        if not html_path.exists():
            log.warning("Missing HTML file: %s — skipping", html_path)
            skipped += 1
            continue

        try:
            html = html_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            log.warning("Cannot read %s: %s — skipping", html_path, exc)
            skipped += 1
            continue

        if not html.strip():
            log.warning("Empty HTML file: %s — skipping", filename)
            skipped += 1
            continue

        yield {
            "filename": filename,
            "html":     html,
            "url":      meta["url"],
            "depth":    meta["depth"],
            "id":       meta["id"],
        }
        yielded += 1

    log.info("iter_pages complete: %d yielded, %d skipped", yielded, skipped)
