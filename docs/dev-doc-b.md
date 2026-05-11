# Developer Documentation (Part B)

## 1. Project Overview

This part builds a **search engine** on top of the Part A corpus: HTML pages under `crawled_pages/` (and optional `metadata.csv`). The work has two main tracks: **(B1)** build a Lucene index with **PyLucene**, and **(B2)** expose search through a **Django** web app (search box, results list, relevance scores). The team does **not** use Reddit data from Part A; ranking focuses on Lucene default scoring unless extended later.


## Objectives

* Index all HTML from Part A with useful fields (e.g., title, body, URL, depth, timestamps if present in metadata).
* Provide a scriptable build step (`indexer.bat` / `indexer.sh`) aligned with course deliverables.
* Ship a small Django application: query input, search action, top-k results (e.g., 10) with scores in **decreasing** score order.
* Document architecture, index layout, and how search and scoring work for the final report.


## Core Idea (Target Implementation)

**Indexing:** Each crawled page becomes one **Lucene document** with multiple **fields** (stored and/or searchable). A single **index directory** on disk is produced by an offline indexer program.

**Searching:** The web app opens a **read-only** `IndexSearcher` over that directory, runs a user query (e.g., `MultiFieldQueryParser` or equivalent), and maps hits to rows in the UI (title, URL, snippet optional, score).

```txt
Part A HTML + metadata  →  Indexer (PyLucene)  →  index/
                                              ↘
                                    Django  →  User browser
```


## 2. System Workflow (Target)

### High-Level Pipeline

```txt
(One-time or refresh) Build index:
  Read crawled_pages/*.html + metadata.csv
       ↓
  Parse / strip boilerplate (optional)
       ↓
  Build Lucene Document (fields: title, body, url, ...)
       ↓
  IndexWriter.addDocument(...)
       ↓
  Commit / close  →  index/ on disk

(Runtime) Search:
  User submits query in browser
       ↓
  Django view receives q
       ↓
  IndexSearcher.search(query, k)
       ↓
  Sort by Lucene score (descending)
       ↓
  Render template with results + scores
```

### Stop / Scope Notes

* Index only what Part A produced; missing files or malformed HTML should be skipped or logged without crashing the whole batch.
* Default **k** for the UI (e.g., 10) should match the assignment example unless the team agrees otherwise.


## 3. Project Structure (Target)

```txt
CS172_Project/
│
├── crawler/                  # Part A (unchanged role)
├── crawled_pages/            # Part A output (local; may be gitignored)
├── main.py
├── config.py
│
├── indexer/                  # Part B: indexing code
│   ├── build_index.py        # Entry: crawl dir → Lucene index
│   └── (helpers for parsing fields)
│
├── index/                    # Part B: generated Lucene index (gitignored)
│   └── (Lucene segment files)
│
├── web/                      # Part B: Django project root
│   ├── manage.py
│   ├── search_site/          # Django *project* package: settings, root urls
│   └── search_app/           # Django *app*: views, app urls, templates
│
├── indexer.bat
├── indexer.sh
├── requirements.txt          # append PyLucene, Django, etc.
└── docs/
    ├── dev-doc-a.md
    └── dev-doc-b.md
```

Notes:

* `indexer/` — Python code that **builds** the search index (reads HTML + metadata, writes index files).
* `index/` — generated **Lucene index data** on disk; read by Django at query time. Not source code.
* `search_site/` — Django **project** (global settings, root `urls.py`).
* `search_app/` — Django **app** (views, templates, app routes) inside the project.


## 4. Configuration (Illustrative)

Paths and constants should be centralized (e.g., `config.py` or Django `settings.py` + env):

```python
# Example only — align with actual repo layout
CRAWL_OUTPUT_DIR = "crawled_pages"
METADATA_CSV = "crawled_pages/metadata.csv"
LUCENE_INDEX_DIR = "index/lucene_index"
SEARCH_TOP_K = 10
```

Django should read the same index path in development and document overrides for deployment.


## 5. Core Responsibilities and Interfaces (Team Agreement)

Agree early on function boundaries and who owns files:

```txt
build_index(crawl_dir, metadata_path, index_dir) → None   # creates / overwrites index

open_searcher(index_dir) → IndexSearcher (or thin wrapper)

search(searcher, query_string, k) → list of {url, title, score, ...}
```

The Django layer should depend on a **small** Python API (wrapper module) so PyLucene JVM usage stays in one place and is easier to test.


## 6. Task Distribution (Balanced)

### Person 1 — Django Setup

* Create project + app
* Routes + templates + static dirs
* Search helper module (JVM / searcher)


### Person 2 — Search Logic

* Parse query
* Call PyLucene + get scores
* Sort top-k by score
* Partially Fields + analyzer


### Person 3 — Indexer Input

* `requirements.txt` + PyLucene install note
* Walk `crawled_pages`
* Join `metadata.csv`


### Person 4 — Indexer Core

* Fields + analyzer + `Document`
* Run `IndexWriter`
* `indexer.bat` / `indexer.sh`


### Person 5 — Frontend

* Search box + result list
* Basic styling
* E2E + screenshots + report


## 7. Component Interaction (Target Runtime)

```txt
indexer/build_index.py:
  Walk + join (Person 3)
       ↓
  Document + IndexWriter (Person 4)
       ↓
  index/

Django:
  shell + helper (Person 1)  →  search + rank (Person 2)  →  template (Person 5)
```


## 8. Index and Metadata Expectations

### Source files

```txt
crawled_pages/
    0001.html
    0002.html
    metadata.csv
```

### Index (on disk)

Opaque Lucene files under `index/`; team documents field names and types in the report.

### Typical metadata columns (align with Part A)

```txt
id, url, filename, depth
```

Additional columns from Part A, if any, can be mapped to Lucene fields when useful.


## 9. Key Challenges

### 1. PyLucene environment

JVM and native bindings differ by OS; everyone should verify indexer import and a minimal index write early.

### 2. HTML noise

Boilerplate, nav, and scripts can dominate `body`; optional stripping improves relevance (team tradeoff vs time).

### 3. Index and web process lifecycle

Indexer is offline; Django must not try to write the index at request time. Rebuild index when corpus changes.

### 4. Consistency of URL and file keys

Metadata `filename` must match on-disk HTML names for joins.


## 10. Limitations (Expected)

* Ranking is **Lucene default** unless the team adds boosts or extra credit (PageRank, custom snippets).
* No Reddit-specific ranking (not in scope for this team’s Part A data).
* Very large indexes may need JVM heap tuning; document any constraints on grader hardware.


## 11. Expected Output

* Runnable `indexer.bat` / `indexer.sh` and a populated `index/` after a successful run.
* Runnable Django app showing top results with scores for sample queries.
* Updated developer docs and report-ready description of architecture and search behavior.


## 12. Summary

Part B turns the Part A crawl into a **queryable index** and a **minimal web front end**, with **offline indexing** separate from **online search** in Django.

## Final Insight

```txt
Part B = offline Lucene index build  +  online Django query and ranked result display
```
