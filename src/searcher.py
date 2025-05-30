from nltk.stem import PorterStemmer
from tokenizer import tokenize
from posting import Posting
from pathlib import Path
import json


def fetchPostings(term: str) -> set[int]:
    """
    Fetches the postings for the given term by navigating to the
    corresponding Inverted Index range json file and hunting down
    the term's posting list. Returns empty if key not found or file
    is not found
    """
    postings = []
    first_char = term[0]
    if first_char.isdigit():
        first_char = "0-9"
    index_path = Path(f"index_ranges/{first_char}.json")
    if index_path.exists():
        with open(index_path, 'r') as indexFile:
            try:
                index = json.load(indexFile)
                # Returns the postings (only their docIDs), which can be altered later
                return set(posting["document_ID"] for posting in index[term])
            except KeyError:
                return postings
    return postings


def parseQueryTerms(query: str) -> list:
    """
    Parses the query by stripping it and making it lowecased,
    then stemming the terms, returning the list of parsed terms
    """
    # Strips and lowercases the entire query
    whole_query = query.strip().lower()
    # Tokenizes and stems the query
    query_tokens = tokenize(whole_query)
    stemmer = PorterStemmer()
    stemmed_terms = [stemmer.stem(term) for term in query_tokens]
    return stemmed_terms


def retrieveURLs(query: str) -> list[str]:
    queryTerms = parseQueryTerms(query)
    numQueryTerms = len(queryTerms)
    if numQueryTerms < 1:
        return []

    # Intersects docIDs to AND all query terms
    retrievedDocIDs = fetchPostings(queryTerms[0])
    for term in queryTerms[1:]:
        retrievedDocIDs &= fetchPostings(term)

    # Loads in the {document id: URL} mapping
    with open("document_id_map.json", 'r') as docIDMapFile:
        docIDMap = json.load(docIDMapFile)

    # Translates the retrieved document IDs to URLs
    retrievedURLs = []
    counter = 0
    for docID in retrievedDocIDs:
        if counter > 4: break
        url = docIDMap.get(str(docID))
        if url:
            retrievedURLs.append(url)
        counter += 1
    return retrievedURLs
