# Developer Documentation (Part A)

## 📌 1. Project Overview

This project aims to build a **web crawler** that automatically collects web pages starting from a small set of seed URLs. The crawler explores the web by following hyperlinks, stores downloaded HTML pages, and prepares the dataset for indexing in Part B (search engine).


## 🎯 Objectives

* Start from a list of seed URLs
* Crawl web pages up to a specified depth (hops)
* Collect a large dataset (target ~500MB)
* Avoid duplicate pages
* Store HTML files and metadata in a structured format


## 🧠 Core Idea

The web can be modeled as a **graph**:

* Pages = nodes
* Links = edges

The crawler performs a **Breadth-First Search (BFS)**:

```txt
Seed → Links → More Links → ...
```


## ⚙️ 2. System Workflow

### 🔁 High-Level Pipeline

```txt
Load Seeds
   ↓
Add to Queue (depth = 0)
   ↓
Loop:
   ↓
Take URL from queue
   ↓
Download HTML
   ↓
Save page
   ↓
Extract links
   ↓
Filter links (domain + duplicates)
   ↓
Add new URLs to queue (depth + 1)
   ↓
Repeat
```


## 🔄 Example Execution

```txt
seed.txt:
https://www.ucr.edu/

Step 1: Crawl homepage
Step 2: Extract ~50 links
Step 3: Crawl those 50 pages
Step 4: Extract ~500 links
...
```


## 📂 3. Project Structure

```txt
crawler_project/
│
├── seed.txt
├── config.py
├── main.py
├── requirements.txt
│
├── crawler/
│   ├── frontier.py        # Queue + BFS (P2)
│   ├── downloader.py      # HTTP requests (P3)
│   ├── parser.py          # Link extraction (P4)
│   ├── filters.py         # URL filtering (P5)
│   ├── storage.py         # Save HTML + metadata (P5)
│
└── crawled_pages/
    ├── 0001.html
    ├── 0002.html
    └── metadata.csv
```


## ⚙️ 4. Configuration

```python
SEED_FILE = "seed.txt"
MAX_PAGES = 10000
MAX_HOPS = 3
OUTPUT_DIR = "crawled_pages"
ALLOWED_DOMAIN = "ucr.edu"
REQUEST_TIMEOUT = 5
```


## 🔌 5. Core Function Interfaces

All components must follow these agreed interfaces:

```txt
load_seeds(file) → [urls]

download(url) → html, status_code

extract_links(html, base_url) → [urls]

is_valid_url(url) → True/False

save_page(url, html, depth) → filename

Frontier.add(url, depth)
Frontier.next() → (url, depth)
Frontier.is_empty() → True/False
```


## 👥 6. Task Distribution (Balanced)

### 👤 Person 1 — Setup + Configuration

* Create project structure
* Implement config system
* Load seed URLs
* Prepare `main.py` skeleton


### 👤 Person 2 — Frontier (Queue + BFS)

* Manage URL queue
* Track depth (hops)
* Control stopping conditions:

  * max pages
  * max hops


### 👤 Person 3 — Downloader

* Send HTTP requests
* Handle:

  * timeouts
  * errors (404, etc.)
  * redirects
* Return clean HTML


### 👤 Person 4 — Link Extraction

* Parse HTML
* Extract `<a href="">`
* Convert relative → absolute URLs
* Normalize URLs (remove fragments)


### 👤 Person 5 — Filtering + Storage

* Remove duplicate URLs
* Restrict domain (e.g., `.edu`)
* Skip non-HTML files
* Save pages + metadata


## 🔗 7. Component Interaction

```txt
Frontier (P2)
   ↓
Downloader (P3)
   ↓
Storage (P5)
   ↓
Parser (P4)
   ↓
Filter (P5)
   ↓
Frontier (P2)
```


## ⚡ 8. Parallel Development Strategy

### Step 1: Agree on interfaces (team)

### Step 2: Work in parallel

```txt
P1 → setup/config
P2 → queue
P3 → downloader
P4 → parser
P5 → filter/storage
```

### Step 3: Integration

* Connect all components
* Debug mismatches


## 📊 9. Data Storage Format

### HTML Files

```txt
crawled_pages/
    0001.html
    0002.html
```

### Metadata

```txt
id, url, filename, depth
1, https://www.ucr.edu, 0001.html, 0
```


## ⚠️ 10. Key Challenges

### 1. Duplicate URLs

```txt
page?id=1 vs page?id=1&
```

### 2. Infinite loops

```txt
A → B → A
```

### 3. Broken pages

* 404 errors
* timeouts

### 4. Relative URLs

```txt
/about → https://site.com/about
```


## 🚫 11. Limitations

* Cannot crawl JavaScript-rendered content
* Some websites block crawlers
* No full robots.txt compliance (simplified for project)
* Limited to static HTML pages


## 🚀 12. Expected Output

* Thousands of HTML files
* Structured metadata
* Clean dataset ready for indexing (Part B)


## 🎯 13. Summary

This project builds a foundational **web crawler system** that:

* explores the web like a graph
* collects large-scale data
* prepares for search engine construction

The system is modular, scalable, and designed for team collaboration.


## 🔥 Final Insight

```txt
Crawler = BFS over the web graph + data collection pipeline
```
