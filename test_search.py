from search_logic import search

results = search("computer science", index_dir="index/lucene_index")
for r in results:
    print(r)
