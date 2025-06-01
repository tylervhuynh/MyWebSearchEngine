from time import time
from pathlib import Path
import json
import searcher

# THESE ARE THE 20 TEST QUERIES
TEST_QUERIES = {"cristina lopes", "green chair", "green chairs", "french wine", "tyler van huynh",
                "0", "uci 121", "", " ", "github",
                "", "", "", "", "",
                "", "", "", "", ""}


# Opens the term to file mapping file
term_to_file_path = Path("term_to_file_map.json")
if term_to_file_path.exists():
    with open(term_to_file_path, "r") as mapFile:
        term_to_file_map = json.load(mapFile)

# Tests all queries
for i, query in enumerate(TEST_QUERIES):
    start = time()
    urls = searcher.retrieveURLs(query, term_to_file_map)
    end = time()
    print(f"{i + 1}. {query} took {end - start} seconds")
