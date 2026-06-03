#!/usr/bin/env bash
# Unix/macOS launcher for the CS172 search index builder (Part B).
#
# Usage:
#     ./indexer.sh [--crawl-dir DIR] [--metadata CSV] [--index-dir DIR]
#
# Defaults:
#     --crawl-dir  crawled_pages
#     --metadata   crawled_pages/metadata.csv
#     --index-dir  index/lucene_index
#
# Example:
#     ./indexer.sh
#     ./indexer.sh --crawl-dir crawled_pages --index-dir index/lucene_index

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

exec "$PYTHON" "$SCRIPT_DIR/indexer/build_index.py" "$@"
