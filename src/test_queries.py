from time import time
from pathlib import Path
import json
import searcher


# THESE ARE THE 20 TEST QUERIES
TEST_QUERIES = {"cristina lopes", "green chair", "green chairs", "french wine", "tyler van huynh",
                "0", "uci cs 121", "", " ", "github",
                "123456789", "isaac reed", ".", "to be or not to be", "whitney houston",
                "information retrieval", "ACM", "how to create a search engine", "caesar and brutus", "hamlet"}


# Opens the term to file mapping file
term_to_file_path = Path("term_to_file_map.json")
if term_to_file_path.exists():
    with open(term_to_file_path, "r") as mapFile:
        term_to_file_map = json.load(mapFile)


# Tests all queries
accumulated_lengths = 0
for i, query in enumerate(TEST_QUERIES):
    start = time()
    urls = searcher.retrieveURLs(query, term_to_file_map)
    end = time()
    length = end - start
    accumulated_lengths += length
    print(f"{i + 1}. {query} took {length} seconds")
print(f"The average time needed to search all 20 queries was {accumulated_lengths / 20} seconds")
