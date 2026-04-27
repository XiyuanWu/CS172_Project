"""
Global configuration for the web crawler (Part A).

Owned by: Person 1 (setup + configuration).

Default values can be overridden from the command line in `main.py`
(see `--seed-file`, `--max-pages`, `--max-hops`, `--output-dir`,
`--allowed-domain`).

Other modules (P2 frontier / P3 downloader / P4 parser / P5 filters &
storage) should import from this module instead of hard-coding values:

    from config import CONFIG
    CONFIG.max_pages
"""

from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class CrawlerConfig:
    seed_file: str = "seed.txt"
    max_pages: int = 10000
    max_hops: int = 6
    output_dir: str = "crawled_pages"
    allowed_domain: str = ""

    request_timeout: float = 5.0
    max_retries: int = 2
    user_agent: str = (
        "CS172-Crawler/1.0 (+https://www.cs.ucr.edu; educational project)"
    )

    num_workers: int = 8
    polite_delay: float = 0.2

    skip_extensions: Tuple[str, ...] = field(
        default_factory=lambda: (
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".zip", ".tar", ".gz", ".rar", ".7z",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
            ".mp3", ".mp4", ".avi", ".mov", ".wmv", ".flv",
            ".css", ".js", ".ico",
        )
    )

    metadata_filename: str = "metadata.csv"


CONFIG = CrawlerConfig()
