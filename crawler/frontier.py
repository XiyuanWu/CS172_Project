"""URL frontier (queue + BFS depth tracking).

Owned by: Prathmesh Jain

Agreed interface (dev-doc-a.md, section 5):
    Frontier.add(url, depth)
    Frontier.next() -> (url, depth)
    Frontier.is_empty() -> bool

Behavioral requirements:
    * BFS order (FIFO). Pages at depth d are crawled before depth d+1.
    * `add` should silently drop URLs whose depth exceeds CONFIG.max_hops.
    * Deduplication is NOT done here - that is P5's responsibility.
    * Thread-safe: multiple threads may call add() and next() concurrently.
"""

from __future__ import annotations

import queue

from typing import Tuple

from config import CONFIG


class Frontier:
    def __init__(self) -> None:
        self._queue: queue.Queue[Tuple[str,int]] = queue.Queue()

    def add(self, url: str, depth: int) -> None:
        if depth > CONFIG.max_hops:
            return
        self._queue.put((url,depth))

    def next(self) -> Tuple[str, int]:
        return self._queue.get_nowait() # Dequeue, but safe for multithreading

    def is_empty(self) -> bool:
        return self._queue.empty()

    def __len__(self) -> int:
        return self._queue.qsize()
    

# Tests
if __name__ == "__main__":
    print("Test: Single Threaded Flow (In case multithreading is not implemented by P3)")
    f = Frontier()

    f.add("https://www.ucr.edu", 0)
    f.add("https://www.ucr.edu/about-ucr", 1)
    f.add("https://www.ucr.edu/academics", 1)
    f.add("https://housing.ucr.edu", 10) # Should not run
    f.add("https://www.ucr.edu/admissions", 1)
    f.add("https://www.ucr.edu/research", 1)
    f.add("https://campusmap.ucr.edu/?id=2106#!ct/71297,94076,94079,94080?s", 10) # Should not run

    print("Length: ", len(f), "Should be 5")

    while not f.is_empty():
        url, depth = f.next()
        print(f"depth = {depth} {url}")

    print("Empty:", f.is_empty())