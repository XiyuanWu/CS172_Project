"""Indexer entry point.

P3 owns the input layer (walk `crawled_pages`, join `metadata.csv`).
P4 owns the Lucene layer (fields + analyzer + IndexWriter, plus the
`indexer.bat` / `indexer.sh` wiring).

This file is a placeholder so the package structure exists; P3/P4 will
flesh it out.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def build_index(crawl_dir: Path, metadata_csv: Path, index_dir: Path) -> None:
    raise NotImplementedError(
        'indexer.build_index: implementation pending (P3 + P4).'
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Build the Part B Lucene index.')
    parser.add_argument('--crawl-dir', type=Path, default=Path('crawled_pages'))
    parser.add_argument('--metadata', type=Path, default=Path('crawled_pages/metadata.csv'))
    parser.add_argument('--index-dir', type=Path, default=Path('index/lucene_index'))
    args = parser.parse_args(argv)

    build_index(args.crawl_dir, args.metadata, args.index_dir)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
