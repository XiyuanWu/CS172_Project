# Usage

End-user guide for Part A (crawler) and Part B (search index + web app). For developer setup (venv, project layout), see [`installation.md`](installation.md).

---

## Part A

By default, the crawler writes to `crawled_pages` and targets at least **500MB** of HTML data.

After each dequeued URL, it sleeps for **`polite_delay` seconds** (default `0.2` in `config.py`) to reduce request rate.

### Quick run

Use the launcher script for your platform.

**Windows:**

```bat
.\crawler.bat seed.txt 0 6 crawled_pages
```

**macOS / Linux:**

```bash
./crawler.sh seed.txt 0 6 crawled_pages
```

### Direct Python command

You can also run the crawler entry point directly:

```bash
python main.py --seed-file seed.txt --max-pages 0 --max-hops 6 --target-size-mb 500
```

Equivalent positional form:

```bash
python main.py seed.txt 0 6 crawled_pages --target-size-mb 500
```

### Optional flags

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

### Sharing crawled data (Part A → Part B)

Do **not** commit raw `crawled_pages/*.html` to a public Git repo: saved pages often contain third-party JavaScript or URL parameters that look like API keys to automated secret scanners.

Recommended instead:

- Zip `crawled_pages/` (including `metadata.csv`) and share via course submission, team drive, or a **GitHub Release** asset.
- Or document the same `seed.txt` + crawler command so teammates can reproduce the crawl locally.

---

## Part B

Build a Lucene index from Part A crawl data, start Django, and search in the browser.

### What you need first

| Requirement | Location | How to get it |
|-------------|----------|---------------|
| Crawled HTML + metadata | `crawled_pages/` + `crawled_pages/metadata.csv` | Run Part A above **or** unzip a teammate's shared `crawled_pages` folder |
| Lucene index | `index/lucene_index/` | Built locally with the indexer (see **Build the search index** below) |
| PyLucene | Python import `lucene` | **Not** installable via `pip`; see **Install PyLucene** below |

The Django UI alone is not enough — without crawl data, an index, and PyLucene, searches will fail.

### Quick start checklist

From a fresh clone, a typical first-time setup looks like this:

```txt
1. Clone repo + create/activate .venv
2. pip install -r requirements.txt
3. Install PyLucene (Docker on Windows, or native on macOS/Linux/WSL)
4. Place or crawl data into crawled_pages/
5. Build index:  indexer.bat   (Windows)  or  ./indexer.sh
6. Start site:   python web/manage.py runserver
7. Open http://127.0.0.1:8000/ and search
```

### Clone and Python environment

```bash
git clone <repo-url>
cd CS172_Project
python -m venv .venv
```

Activate the virtual environment **every time** you open a new terminal.

**Windows — PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Verify the venv is active (path should contain `.venv`):

```bash
python -c "import sys; print(sys.executable)"
```

### Install pip packages

From the repo root:

```bash
pip install -r requirements.txt
```

This installs Django, BeautifulSoup, and Part A crawler libraries. It does **not** install PyLucene.

Smoke test the web project:

```bash
python web/manage.py check
```

Expected: `System check identified no issues`.

### Install PyLucene

PyLucene wraps Apache Lucene in Java. It **cannot** be installed with `pip install pylucene`.

Pick **one** method below. Use the same Python environment for indexing **and** for running the Django server.

> **Tip:** Python **3.10–3.12** is the safest range for PyLucene builds. Very new versions (e.g. 3.14) may not be supported yet.

**Option A — Docker (recommended on Windows)**

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and make sure it is running.
2. Pull the image: `docker pull coady/pylucene`
3. Use this image to **build the index**. For **search in Django**, you still need PyLucene importable in your local `.venv` — on Windows the practical approach is often:
   - build the index with Docker, then
   - run Django from **WSL2** or **macOS/Linux** where PyLucene is installed natively, **or**
   - install WSL2 and build PyLucene there for both indexer and search (see Option B).

Build index only (Docker) — Windows PowerShell, from repo root:

```powershell
docker run --rm -v "${PWD}:/app" -w /app coady/pylucene python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

macOS / Linux:

```bash
docker run --rm -v "$(pwd)":/app -w /app coady/pylucene python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

The index files appear in `index/lucene_index/` on your machine.

**Option B — WSL2 (Windows) or native Linux / macOS**

Build PyLucene from source inside Ubuntu (WSL) or on macOS/Linux. Full steps are in [`installation.md`](installation.md) §6.5 Option B.

After `make install`, verify from the repo root:

```bash
python -c "import lucene; print('PyLucene OK')"
```

If that succeeds, use the same Python for indexer and Django.

**Option C — macOS / Linux (teammate laptop)**

Many teammates run Part B entirely on macOS or Linux with PyLucene built once in their venv. Same commands as below — no Docker required if `import lucene` works.

### Get crawl data

The indexer reads HTML files and joins rows from `metadata.csv`.

**Reuse team data (fastest):**

- Ask a teammate for a zip of `crawled_pages/` (including `metadata.csv`).
- Extract into the repo root so you have:

```txt
crawled_pages/
├── metadata.csv
├── 0001.html
├── 0002.html
└── ...
```

**Crawl yourself:**

Example on Windows:

```bat
.\crawler.bat seed.txt 0 6 crawled_pages
```

> Do not commit `crawled_pages/*.html` to a public Git repo. Share via zip, drive, or GitHub Release.

### Build the search index

From the repo root, with PyLucene available in your active Python (or via the Docker command above).

**Windows:**

```bat
indexer.bat
```

**macOS / Linux:**

```bash
chmod +x indexer.sh
./indexer.sh
```

**Direct Python (all platforms):**

```bash
python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

**Success looks like:**

```txt
Index built: 1234 documents indexed, 5 skipped.
Index written to: index/lucene_index
```

After this, `index/lucene_index/` should contain Lucene segment files (not just `.gitkeep`).

**Optional — test search in the terminal:**

```bash
python test_search.py
```

Or:

```bash
python search_logic.py computer science
```

You should see ranked results with titles, URLs, and scores.

### Run the search website

From the repo root:

```bash
python web/manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

- Type a query (e.g. `computer science`) and click **Search**.
- Results show title, URL, snippet, and Lucene **score** (higher = more relevant).
- Default: top **10** results (`SEARCH_TOP_K` in `web/search_site/settings.py`).

If another app is already on port 8000, use another port:

```bash
python web/manage.py runserver 8001
```

Then open **http://127.0.0.1:8001/**.

### When to rebuild the index

Rebuild when:

- You receive an updated `crawled_pages/` folder
- You run a new crawl in Part A
- Index files under `index/lucene_index/` are missing or corrupted

Re-run `indexer.bat` / `./indexer.sh` (or the Docker command). Restart Django if it was already running.

### Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `PyLucene not installed` | `import lucene` fails in your venv | Complete **Install PyLucene**; verify with `python -c "import lucene"` |
| Search page loads but no results / index error | `index/lucene_index/` empty or missing | Run **Build the search index** after you have `crawled_pages/` |
| `Missing HTML file` warnings during indexing | `metadata.csv` references files not on disk | Re-sync crawl data with teammates |
| Wrong site (e.g. another project's homepage) | Port 8000 used by another server | Use `runserver 8001` or stop the other process |
| Yellow Django error page on search | Uncaught backend error with `DEBUG=True` | Check terminal traceback; usually PyLucene or missing index |
| Teammate's laptop works, yours does not | Missing data, PyLucene, or index on your machine | Follow the Part B checklist; do not skip PyLucene or indexing |

### Paths reference

Configured in `web/search_site/settings.py`:

| Setting | Default path |
|---------|----------------|
| Crawl output | `crawled_pages/` |
| Lucene index | `index/lucene_index/` |
| Top-k results | `10` |

Search logic lives in `search_logic.py`; Django calls it through `web/search_app/search_helper.py`.
