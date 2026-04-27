"""URL frontier (queue + BFS depth tracking).

Owned by: Person 2.

Agreed interface (dev-doc-a.md, section 5):
    Frontier.add(url, depth)
    Frontier.next() -> (url, depth)
    Frontier.is_empty() -> bool

Behavioral requirements:
    * BFS order (FIFO). Pages at depth d are crawled before depth d+1.
    * `add` should silently drop URLs whose depth exceeds CONFIG.max_hops.
    * Should be safe to call from a single producer; thread-safety is the
      implementer's choice depending on whether P3 is multi-threaded.

This file is a STUB. Implementation is owned by P2.
"""

from __future__ import annotations

from typing import Tuple


class Frontier:
    def __init__(self) -> None:
        raise NotImplementedError("P2: implement Frontier.__init__")

    def add(self, url: str, depth: int) -> None:
        """Enqueue (url, depth) if depth is within CONFIG.max_hops."""
        raise NotImplementedError("P2: implement Frontier.add")

    def next(self) -> Tuple[str, int]:
        """Pop and return the next (url, depth) in BFS order."""
        raise NotImplementedError("P2: implement Frontier.next")

    def is_empty(self) -> bool:
        raise NotImplementedError("P2: implement Frontier.is_empty")

    def __len__(self) -> int:
        raise NotImplementedError("P2: implement Frontier.__len__")
