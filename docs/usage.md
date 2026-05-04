# Usage (Part A)

By default, the crawler now writes to `crawled_pages` and targets at least **500MB** of HTML data.

After each dequeued URL, it sleeps for **`polite_delay` seconds** (default `0.2` in `config.py`) to reduce request rate.

## Quick run

Use the launcher script for your platform:

### Windows

```bat
.\crawler.bat seed.txt 0 6 crawled_pages
```

### macOS / Linux

```bash
./crawler.sh seed.txt 0 6 crawled_pages
```

## Direct Python command

You can also run the crawler entry point directly:

```bash
python main.py --seed-file seed.txt --max-pages 0 --max-hops 6 --target-size-mb 500
```

Equivalent positional form:

```bash
python main.py seed.txt 0 6 crawled_pages --target-size-mb 500
```

## Optional flags

- Restrict crawl to a domain suffix: `--allowed-domain ucr.edu`
- Enable debug logs: `-v` or `--verbose`
- Set size stop target (MB): `--target-size-mb 500`
- Pause between URLs: `--polite-delay 0.5` (or `--polite-delay 0` to turn off)
- `--max-pages 0` means no page-count cap (recommended when targeting 500MB)
- Show all options: `python main.py --help`

Example:

```bash
python main.py --seed-file seed.txt --max-pages 0 --max-hops 6 --target-size-mb 500 --allowed-domain ucr.edu -v
```

## Sharing crawled data (Part A → Part B)

Do **not** commit raw `crawled_pages/*.html` to a public Git repo: saved pages often contain third-party JavaScript or URL parameters that look like API keys to automated secret scanners.

Recommended instead:

- Zip `crawled_pages/` (including `metadata.csv`) and share via course submission, team drive, or a **GitHub Release** asset.
- Or document the same `seed.txt` + crawler command so teammates can reproduce the crawl locally.
