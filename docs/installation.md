# Installation (Developer Setup)

This guide is for **developers** working on the project. It covers the full local setup for Part A (crawler) and Part B (indexer + Django search site).

End users who only want to run the project should read [`usage.md`](usage.md) instead.

## Prerequisites

- Python 3.10 or newer (`python --version` to check)
- `pip` (bundled with Python)
- Git
- For Part B (Option A — Docker): Docker Desktop installed and running
- For Part B (Option B — WSL2): Windows Subsystem for Linux 2 with Ubuntu

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

### 6.5 PyLucene Installation

PyLucene **cannot** be installed with `pip install pylucene`. It requires a
pre-built environment or a manual source build. Two supported options are
described below.

---

#### Option A — Docker (Recommended)

Docker provides a pre-built image with PyLucene already compiled, so no
manual JDK/Ant setup is needed.

**1. Install Docker Desktop**
Download from https://www.docker.com/products/docker-desktop and follow the
installer. Make sure Docker is running before continuing.

**2. Pull the PyLucene image**
```bash
docker pull coady/pylucene
```

**3. Run the indexer inside the container**

From the repo root:
```bash
docker run --rm \
  -v "$(pwd)":/app \
  -w /app \
  coady/pylucene \
  python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

On Windows (PowerShell), replace `$(pwd)` with `${PWD}`:
```powershell
docker run --rm -v "${PWD}:/app" -w /app coady/pylucene python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

The generated index will appear in `index/lucene_index/` on your host machine.

---

#### Option B — WSL2 (Windows Subsystem for Linux)

WSL2 lets you build and run PyLucene on Ubuntu inside Windows without Docker.

**1. Enable WSL2 and install Ubuntu**

In PowerShell (run as Administrator):
```powershell
wsl --install
```
Restart your machine, then open the Ubuntu app to finish setup.

**2. Install build dependencies inside Ubuntu**
```bash
sudo apt update
sudo apt install -y default-jdk ant python3-dev python3-pip gcc g++ make
```

Verify Java is installed:
```bash
java -version
```

**3. Download and build PyLucene**
```bash
# Download the source (check https://lucene.apache.org/pylucene/ for the latest version)
wget https://downloads.apache.org/lucene/pylucene/pylucene-9.10.0-src.tar.gz
tar -xzf pylucene-9.10.0-src.tar.gz
cd pylucene-9.10.0
```

Edit `Makefile` to set your Python path:
```makefile
PREFIX_PYTHON=/usr
ANT=ant
PYTHON=$(PREFIX_PYTHON)/bin/python3
JCC=$(PYTHON) -m jcc
NUM_FILES=8
```

Then build and install:
```bash
make
make install
```

**4. Navigate to the project and run the indexer**
```bash
cd /mnt/e/CS\ 172/CS172_Project/Web_Crawler
python -m indexer.build_index --crawl-dir crawled_pages --metadata crawled_pages/metadata.csv --index-dir index/lucene_index
```

---

> **Note:** PyLucene is only required to build the index and run searches.
> The Django dev server and crawler work without it.

## 7. Deactivate (when done)

```bash
deactivate
```
