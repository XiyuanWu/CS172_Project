"""URL frontier (queue + BFS depth tracking).

Owned by: Person 2 - Prathmesh Jain

Agreed interface (dev-doc-a.md, section 5):
    Frontier.add(url, depth)
    Frontier.next() -> (url, depth)
    Frontier.is_empty() -> bool

Additions (for the multi-threaded crawler):
    Frontier.task_done()  -- worker calls this after a URL is fully
                             processed (downloaded, parsed, children added).
    Frontier.join()       -- main thread blocks until every URL ever
                             added has been task_done()'d.

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
        """Enqueue (url, depth). Silently drops if depth > CONFIG.max_hops."""
        if depth > CONFIG.max_hops:
            return
        self._queue.put((url,depth))

    def next(self) -> Tuple[str, int]:
        """Pop and return the next (url, depth) in BFS (FIFO) order.
        
        Multi-threaded callers must call task_done() after fully
        processing the returned URL (downloaded + parsed + children
        added). Single-threaded callers can ignore task_done().
        """
        return self._queue.get_nowait() # Dequeue, but safe for multithreading

    def is_empty(self) -> bool:
        """True if there are no URLs waiting right now.

        In multi-threaded use, this is a snapshot. The queue may
        appear empty while a worker is about to add() more URLs, so
        end-of-crawl detection should use join(), not is_empty().
        """
        return self._queue.empty()

    def __len__(self) -> int:
        """Number of URLs currently waiting (approximate under threads)."""
        return self._queue.qsize()
    
    def task_done(self) -> None:
        """Signal that a URL returned by next() is fully processed.

        Multi-threaded use only. Must be called exactly once for each
        URL returned by next(), AFTER any child URLs have been add()'d.
        This is what allows join() to know when the entire crawl is
        complete.
        """
        self._queue.task_done()

    def join(self) -> None:
        """Block until every URL ever add()'d has been task_done()'d.

        Multi-threaded use only. Used by main.py to detect end-of-crawl
        without the race condition that is_empty() has under threads.
        """
        self._queue.join()
    



# Tests
if __name__ == "__main__":
    print("Test 1: Single Threaded Flow (In case multithreading is not implemented)")
    f = Frontier()

    f.add("https://www.ucr.edu", 0)
    f.add("https://www.ucr.edu/about-ucr", 1)
    f.add("https://www.ucr.edu/academics", 1)
    f.add("https://housing.ucr.edu", 10) # Should not run
    f.add("https://www.ucr.edu/admissions", 1)
    f.add("https://www.ucr.edu/research", 1)
    f.add("https://campusmap.ucr.edu/?id=2106#!ct/71297,94076,94079,94080?s", 10) # Should not run

    print("Length: ", len(f), "(Should be 5)")

    while not f.is_empty():
        url, depth = f.next()
        print(f"depth = {depth} {url}")

    print("Empty:", f.is_empty())


    print("\nTest 2: Multithreaded Flow")

    import threading
    import random
    
    f = Frontier()

    def producer(producer_id: int) -> None:
        for i in range(5):
            depth = random.choice([0,1,10])
            f.add(f"https://www.ucr.edu/p{producer_id}-{i}", depth)

    threads = [threading.Thread(target=producer,args=(i,)) for i in range(4)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"4 concurrent threads running producer, len = {len(f)}")

    url_counter = 0
    while not f.is_empty():
        url, depth = f.next()
        url_counter += 1
        print(f"counter = {url_counter} depth = {depth} {url}")
    

    print("\nTest 3: Multithreaded queue end")

    f = Frontier()
    crawled = []
    crawled_lock = threading.Lock()

    f.add("https://www.ucr.edu", 0)

    def test_worker(worker_id:int) -> None:
        while True:
            try:
                url, depth = f.next()
                print(f"worker = {worker_id} depth = {depth} {url}")
            except queue.Empty:
                import time
                time.sleep(0.1)
                continue

            with crawled_lock:
                crawled.append(url)
            
            # Fake Child links getting added
            if depth == 0:
                for i in range(3):
                    f.add(f"https://www.ucr.edu/child{i}", 1)
            elif depth == 1:
                for i in range(2):
                    f.add(f"{url}/grandchild{i}", 2)

            f.task_done()

    workers = [threading.Thread(target=test_worker, args=(i,), daemon=True) for i in range(3)]

    for w in workers:
        w.start()
    
    f.join()

    print(f"crawl finished. crawled {len(crawled)} URLs (expected 10)")
    print(f"  examples: {crawled[:4]} ...")
