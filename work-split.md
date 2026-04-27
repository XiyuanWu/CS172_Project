

### **P1 — Project setup + config + seed loader**

Owns:

```txt
project structure
requirements.txt
config file
read seed.txt
command-line arguments
```

Example config:

```txt
seed_file
max_pages
max_hops
output_dir
allowed_domain
```

---

### **P2 — Crawl frontier / queue manager**

Owns:

```txt
URL queue
depth tracking
max hops
max pages stopping logic
BFS behavior
```

This person handles:

```txt
(url, depth)
```

---

### **P3 — Downloader**

Owns:

```txt
HTTP request
timeout
status code
redirects
only return valid HTML
```

Function:

```txt
download(url) → html, status_code
```

---

### **P4 — Link extraction + URL cleaning**

Owns:

```txt
parse HTML
extract <a href="">
relative URL → absolute URL
remove #section
normalize URLs
```

Function:

```txt
extract_links(html, base_url) → urls
```

---

### **P5 — URL filtering + storage + metadata**

Owns:

```txt
visited set
duplicate checking
domain filtering
skip pdf/images
save HTML files
write metadata.csv
```

Function:

```txt
filter_and_save(url, html, depth)
```

---

## Pipeline

```txt
P1: load config + seeds
        ↓
P2: choose next URL from queue
        ↓
P3: download HTML
        ↓
P4: extract links
        ↓
P5: filter duplicates + save page
        ↓
P2: add clean new URLs back to queue
```

## Report split

```txt
P1: setup/config/seed design
P2: BFS frontier and depth control
P3: downloading/error handling
P4: link extraction/normalization
P5: filtering/storage/metadata
```
