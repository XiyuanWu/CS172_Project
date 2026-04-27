"""Crawler entry point.

Owned by: Person 1.

Wires together the components owned by P2-P5:

    seeds (P1) -> Frontier (P2) -> downloader (P3) ->
        storage (P5) -> parser (P4) -> filters (P5) -> Frontier (P2)

Usage (matches the deliverable spec in instructions.md):

    python main.py --seed-file seed.txt --max-pages 10000 \
                   --max-hops 6 --output-dir crawled_pages

Positional form (compatible with crawler.sh / crawler.bat):

    python main.py seed.txt 10000 6 crawled_pages

Run `python main.py --help` for the full list of options.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import List, Optional

from config import CONFIG
from crawler.seeds import load_seeds


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="crawler",
        description="CS172 web crawler (Part A).",
    )
    p.add_argument("seed_file", nargs="?", default=None,
                   help="Positional: path to seed file (default from --seed-file).")
    p.add_argument("max_pages", nargs="?", type=int, default=None,
                   help="Positional: maximum pages to crawl.")
    p.add_argument("max_hops", nargs="?", type=int, default=None,
                   help="Positional: maximum depth (hops) from seeds.")
    p.add_argument("output_dir", nargs="?", default=None,
                   help="Positional: directory for saved HTML + metadata.")

    p.add_argument("--seed-file", dest="seed_file_opt", default=None,
                   help="Path to seed URL file (one URL per line).")
    p.add_argument("--max-pages", dest="max_pages_opt", type=int, default=None,
                   help="Maximum number of pages to crawl.")
    p.add_argument("--max-hops", dest="max_hops_opt", type=int, default=None,
                   help="Maximum depth (hops) away from seed URLs.")
    p.add_argument("--output-dir", dest="output_dir_opt", default=None,
                   help="Directory for saved HTML pages and metadata.csv.")
    p.add_argument("--allowed-domain", dest="allowed_domain", default=None,
                   help="Restrict crawl to this domain suffix (e.g. 'ucr.edu').")
    p.add_argument("--workers", dest="workers", type=int, default=None,
                   help="Number of concurrent download workers.")
    p.add_argument("--timeout", dest="timeout", type=float, default=None,
                   help="Per-request HTTP timeout in seconds.")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Enable DEBUG-level logging.")
    return p


def apply_cli_overrides(args: argparse.Namespace) -> None:
    """Mutate the global CONFIG based on CLI arguments."""
    seed_file = args.seed_file_opt or args.seed_file
    if seed_file is not None:
        CONFIG.seed_file = seed_file

    max_pages = args.max_pages_opt if args.max_pages_opt is not None else args.max_pages
    if max_pages is not None:
        CONFIG.max_pages = max_pages

    max_hops = args.max_hops_opt if args.max_hops_opt is not None else args.max_hops
    if max_hops is not None:
        CONFIG.max_hops = max_hops

    output_dir = args.output_dir_opt or args.output_dir
    if output_dir is not None:
        CONFIG.output_dir = output_dir

    if args.allowed_domain is not None:
        CONFIG.allowed_domain = args.allowed_domain
    if args.workers is not None:
        CONFIG.num_workers = args.workers
    if args.timeout is not None:
        CONFIG.request_timeout = args.timeout


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def ensure_output_dir() -> None:
    os.makedirs(CONFIG.output_dir, exist_ok=True)


def run_crawl(seeds: List[str]) -> None:
    """Drive the BFS crawl by orchestrating P2-P5 modules.

    NOTE: This function depends on the implementations owned by P2-P5.
    Until those are filled in, calling it will raise NotImplementedError
    from the relevant stub. That is expected during early integration.
    """
    log = logging.getLogger("crawler.main")

    from crawler.frontier import Frontier
    from crawler.downloader import download
    from crawler.parser import extract_links
    from crawler.filters import is_valid_url, has_visited, mark_visited
    from crawler.storage import save_page

    frontier = Frontier()
    for url in seeds:
        if is_valid_url(url) and not has_visited(url):
            frontier.add(url, 0)
            mark_visited(url)

    pages_saved = 0
    started = time.time()

    while not frontier.is_empty() and pages_saved < CONFIG.max_pages:
        url, depth = frontier.next()
        log.debug("Fetching depth=%d url=%s", depth, url)

        html, status = download(url)
        if html is None:
            log.debug("Skip url=%s status=%s", url, status)
            continue

        save_page(url, html, depth)
        pages_saved += 1
        if pages_saved % 50 == 0:
            elapsed = time.time() - started
            log.info("Saved %d pages (%.1f pages/s, frontier=%d)",
                     pages_saved, pages_saved / max(elapsed, 1e-6), len(frontier))

        if depth >= CONFIG.max_hops:
            continue

        for link in extract_links(html, url):
            if not is_valid_url(link):
                continue
            if has_visited(link):
                continue
            mark_visited(link)
            frontier.add(link, depth + 1)

    elapsed = time.time() - started
    log.info("Crawl finished: %d pages in %.1fs", pages_saved, elapsed)


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    apply_cli_overrides(args)
    setup_logging(args.verbose)

    log = logging.getLogger("crawler.main")
    log.info("Configuration: seed_file=%s max_pages=%d max_hops=%d "
             "output_dir=%s allowed_domain=%r workers=%d",
             CONFIG.seed_file, CONFIG.max_pages, CONFIG.max_hops,
             CONFIG.output_dir, CONFIG.allowed_domain, CONFIG.num_workers)

    try:
        seeds = load_seeds(CONFIG.seed_file)
    except (FileNotFoundError, ValueError) as e:
        log.error("Failed to load seeds: %s", e)
        return 2

    log.info("Loaded %d seed URL(s) from %s", len(seeds), CONFIG.seed_file)
    ensure_output_dir()

    try:
        run_crawl(seeds)
    except NotImplementedError as e:
        log.error("Crawler component not yet implemented: %s", e)
        log.error("This is expected until P2-P5 finish their modules.")
        return 3
    except KeyboardInterrupt:
        log.warning("Interrupted by user.")
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())
