#!/usr/bin/env bash
# Unix/Linux launcher for the CS172 web crawler (Part A).
#
# Usage:
#     ./crawler.sh <seed-file> <num-pages> <hops-away> <output-dir> [extra args]
#
# Example:
#     ./crawler.sh seed.txt 10000 6 crawled_pages
#     ./crawler.sh seed.txt 10000 6 crawled_pages --allowed-domain ucr.edu -v

set -euo pipefail

if [ "$#" -lt 4 ]; then
    echo "Usage: $(basename "$0") <seed-file> <num-pages> <hops-away> <output-dir> [extra args]" >&2
    exit 1
fi

SEED="$1"
NPAGES="$2"
HOPS="$3"
OUTDIR="$4"
shift 4

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

exec "$PYTHON" "$SCRIPT_DIR/main.py" \
    --seed-file "$SEED" \
    --max-pages "$NPAGES" \
    --max-hops "$HOPS" \
    --output-dir "$OUTDIR" \
    "$@"
