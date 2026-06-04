"""Indexer entry point.

P3 owns the input layer (walk `crawled_pages`, join `metadata.csv`).
P4 owns the Lucene layer (fields + analyzer + IndexWriter, plus the
`indexer.bat` / `indexer.sh` wiring).
"""
from __future__ import annotations

import argparse
import csv
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

try:
    import lucene
    from org.apache.lucene.analysis.standard import StandardAnalyzer
    from org.apache.lucene.document import Document, Field, StoredField, TextField
    from org.apache.lucene.index import IndexWriter, IndexWriterConfig
    from org.apache.lucene.store import FSDirectory
    from java.nio.file import Paths as JPaths
    PYLUCENE_AVAILABLE = True
except ImportError:
    PYLUCENE_AVAILABLE = False

log = logging.getLogger(__name__)


def _extract_fields(html: str) -> tuple[str, str, str]:
    """Return (title, description, body) extracted from raw HTML."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    desc_tag = (
        soup.find("meta", attrs={"name": "description"})
        or soup.find("meta", attrs={"property": "og:description"})
    )
    description = ""
    if desc_tag:
        description = (desc_tag.get("content") or "").strip()

    body = soup.get_text(separator=" ", strip=True)

    return title, description, body


def build_index(crawl_dir: Path, metadata_csv: Path, index_dir: Path) -> None:
    """Read crawled pages + metadata and write a Lucene index to index_dir."""
    if not PYLUCENE_AVAILABLE:
        raise RuntimeError("PyLucene is not installed. See docs/installation.md.")

    lucene.initVM()

    index_dir.mkdir(parents=True, exist_ok=True)
    directory = FSDirectory.open(JPaths.get(str(index_dir)))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(directory, config)

    rows_indexed = 0
    rows_skipped = 0

    with open(metadata_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("url", "").strip()
            filename = row.get("filename", "").strip()
            depth = row.get("depth", "0").strip()

            if not filename:
                rows_skipped += 1
                continue

            html_path = crawl_dir / filename
            if not html_path.exists():
                log.warning("Missing HTML file: %s — skipping", html_path)
                rows_skipped += 1
                continue

            try:
                html = html_path.read_text(encoding="utf-8", errors="replace")
            except OSError as e:
                log.warning("Cannot read %s: %s — skipping", html_path, e)
                rows_skipped += 1
                continue

            try:
                title, description, body = _extract_fields(html)
            except Exception as e:
                log.warning("Parse error for %s: %s — skipping", filename, e)
                rows_skipped += 1
                continue

            mtime = os.path.getmtime(html_path)
            updated_time = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            doc = Document()
            # Searchable + stored fields (TextField is tokenized and indexed)
            doc.add(TextField("title",       title or "",      Field.Store.YES))
            doc.add(TextField("body",        body,             Field.Store.YES))
            doc.add(TextField("description", description,      Field.Store.YES))
            doc.add(TextField("url",         url,              Field.Store.YES))
            # Stored-only fields (not tokenized, used only for result retrieval)
            doc.add(StoredField("filename",     filename))
            doc.add(StoredField("depth",        depth))
            doc.add(StoredField("updated_time", updated_time))

            writer.addDocument(doc)
            rows_indexed += 1

    writer.commit()
    writer.close()

    print(f"Index built: {rows_indexed} documents indexed, {rows_skipped} skipped.")
    print(f"Index written to: {index_dir}")
    log.info("Index built: %d documents indexed, %d skipped.", rows_indexed, rows_skipped)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Build the Part B Lucene index.")
    parser.add_argument("--crawl-dir", type=Path, default=Path("crawled_pages"))
    parser.add_argument("--metadata",  type=Path, default=Path("crawled_pages/metadata.csv"))
    parser.add_argument("--index-dir", type=Path, default=Path("index/lucene_index"))
    args = parser.parse_args(argv)

    build_index(args.crawl_dir, args.metadata, args.index_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
