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
    - Architecture
    - The crawling or data collection strategy
    - Data structures employed
3. Limitations (if any) of system.
4. Instruction on how to deploy the system. Ideally, you should include a crawler.bat (Windows) or crawler.sh (Unix/Linux) executable file that takes as input all necessary parameters.
```
Example: [user@server]./crawler.sh <seed-File:seed.txt> <num-pages: 10000> <hops-away: 6> <output-dir>
```
5. Screenshots showing the system in action.
6. Zip file with your code.



## Part B: Build index and Web-based search interface

### B1: Build index using PyLucene

Index your data using PyLucene (or PyElasticSearch but not Solr) or an equivalent from your language of preference (ask for approval from instructor).

Write a program that uses the PyLucene libraries to index all the html files in the folder you created in Part A. Handle different fields like title, body, creation date (if available).

### B2. Create a Web-based interface

The interface should contain a textbox, and a search button. When you click search, you should see a list of results (e.g., first 10) returned by PyLucene for this query and their scores. The list should be ordered in decreasing order of score. Handle fields as you deem appropriate. For reddit, order by a combination of time and relevance; describe your ranking function.

We recommend Flask or Django for the Web app, but you are free to use your own Web-based programming language (at your own risk).

### Extra credit:

Web: Display a snippet for each result. You can use ideas discussed in class or your own ideas to come up with a good snippet generation algorithm. Don't use PyLucene-generated snippets.

Alternatively, you can use PageRank to rank pages, that is, you can allow the user to either rank by PyLucene ranking or by PageRank.

reddit: Allow ordering posts by votes, time, relevance or a combination of them (weight for each of the three factors).

Alternatively, you can use PageRank to rank posts, that is, you can allow the user to either rank by PyLucene score or by PageRank.

### Deliverables:

1. Collaboration Details: Description of contribution of each team member.
2. Overview of system, including (but not limited to):
    - Architecture
    - Index Structures
    - Search Algorithm
3. Limitations of system.
4. Instructions on how to deploy the system. Ideally, you should include an indexer.bat (Windows) or indexer.sh (Unix/Linux) executable file that takes as input all necessary parameters
```
Example: [user@server] ./indexer.sh <output-dir>
```
5. A web-application (e.g. Web Archive) that can be deployed to a webserver like Tomcat.
6. Screenshots showing the system in action.
7. Zip file with your code.


