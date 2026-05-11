# Installation (Developer Setup)

This guide is for **developers** working on the project. It covers the full local setup for Part A (crawler) and Part B (indexer + Django search site).

End users who only want to run the crawler should read [`usage.md`](usage.md) instead.

## Prerequisites

- Python 3.10 or newer (`python --version` to check)
- `pip` (bundled with Python)
- Git
- For Part B: a JDK 11+ on PATH (needed by PyLucene when it lands; not required for plain Django dev)

## 1. Clone the repo

```bash
git clone <repo-url>
cd CS172_Project
```

## 2. Create a virtual environment

Run this once in the project root:

```bash
python -m venv .venv
```

The `.venv/` folder is already covered by `.gitignore`.

## 3. Activate the virtual environment

Activate it **every time you open a new terminal**.

**Windows — PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows — CMD:**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

You should now see `(.venv)` at the start of your prompt. Verify:

```bash
python -c "import sys; print(sys.executable)"
```

The path should contain `.venv`.

## 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

Rerun this whenever `requirements.txt` changes.

## 5. Part A (crawler) — verify

The crawler does not need extra config to import. Smoke test:

```bash
python -c "from crawler.frontier import Frontier; print('crawler ok')"
```

To actually run a crawl, see [`usage.md`](usage.md).

## 6. Part B (search site) — current state

Part B is **in progress**. The Django project skeleton exists; the indexer and PyLucene search wiring are not implemented yet.

### 6.1 Django project layout

```
web/
├── manage.py
├── search_site/      # Django project package (settings, root urls)
└── search_app/       # Django app (views, urls, search_helper)
```

Shared Part B paths are defined in `web/search_site/settings.py`:

```python
CRAWL_OUTPUT_DIR = REPO_ROOT / 'crawled_pages'
INDEX_DIR        = REPO_ROOT / 'index' / 'lucene_index'
SEARCH_TOP_K     = 10
```

### 6.2 Run Django checks

From the repo root:

```bash
python web/manage.py check
```

Expected: `System check identified no issues`.

### 6.3 Run the dev server

```bash
python web/manage.py runserver
```

Open <http://127.0.0.1:8000/>. The search box renders; submitting a query currently surfaces a placeholder error from `search_app/search_helper.py` (real PyLucene search is pending — P2's task).

### 6.4 Indexer

The package `indexer/` ships with a CLI skeleton:

```bash
python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

Currently raises `NotImplementedError` (P3 + P4 will fill in the real logic).

### 6.5 PyLucene (not installed yet)

PyLucene installation is platform-specific and will be documented separately when wired in. It is **not** required to start the Django dev server or to work on the indexer scaffolding.

## 7. Deactivate (when done)

```bash
deactivate
```
