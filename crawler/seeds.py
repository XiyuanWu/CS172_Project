"""Seed URL loading utilities.

Owned by: Person 1.

Interface (agreed in dev-doc-a.md, section 5):
    load_seeds(file) -> [urls]
"""

from __future__ import annotations

import os
from typing import List


def load_seeds(path: str) -> List[str]:
    """Read seed URLs from a text file.

    Format:
        - One URL per line.
        - Blank lines are ignored.
        - Lines starting with '#' are treated as comments and ignored.
        - Surrounding whitespace is stripped.

    Args:
        path: Path to the seed file.

    Returns:
        A de-duplicated list of seed URLs in the order they first appear.

    Raises:
        FileNotFoundError: If `path` does not exist.
        ValueError: If the file contains no usable seed URLs.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Seed file not found: {path}")

    seeds: List[str] = []
    seen = set()
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line in seen:
                continue
            seen.add(line)
            seeds.append(line)

    if not seeds:
        raise ValueError(f"Seed file '{path}' contains no URLs")
    return seeds
