# Project Instructions

## Part A: Build a Web Crawler for html pages

Your application should read a file of seed  URLs.

The application should also input the number of pages to crawl and the number of levels (hops (i.e. hyperlinks) away from the seed URLs).

Optionally, you can filter the domains that your crawler should access, e.g. .edu or .gov only.

All crawled pages (html files) should be stored in a folder.

Python-based Scrapy will be the default crawler used in the discussion sessions. You can use other languages or libraries, like Java jsoup, but support for these will be limited.

You will be graded on the correctness and efficiency of your crawler (e.g., how does it handle duplicate pages? Does it prune pages outside the target domain? Or is the crawler multi-threaded?).


In all cases, you should collect at least 500 MB of raw data.




### Deliverables:

Report (4-5 pages) in pdf that includes:
1. Collaboration Details: Description of contribution of each team member.
2. Overview of system, including (but not limited to)
    - Architecture.
    - The crawling or data collection strategy.
    - Data structures employed.
3. Limitations (if any) of system.
4. Instruction on how to deploy the system. Ideally, you should include a crawler.bat (Windows) or crawler.sh (Unix/Linux) executable file that takes as input all necessary parameters.
```
Example: [user@server]./crawler.sh <seed-File:seed.txt> <num-pages: 10000> <hops-away: 6> <output-dir>
```

5. Screenshots showing the system in action.

2: Zip file with your code




## Part B: Build index and Web-based search interface

```


```