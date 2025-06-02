from nltk.stem import PorterStemmer
from tokenizer import tokenize
from posting import Posting
from pathlib import Path
import json


def fetchPostings(term: str, term_to_file_map: dict, loaded_files: dict) -> list[int]:
    """
    Fetches the postings for the given term by navigating to the
    corresponding Inverted Index range json file and hunting down
    the term's posting list. Returns empty if key not found or file
    is not found
    """
    postings = []
    file_name = term_to_file_map.get(term)
    if file_name == None:
        return postings
    # Uses cache of loaded files to prevent some opening of json files
    if file_name not in loaded_files:
        index_path = Path(f"index_ranges/{file_name}")
        if not index_path.exists():
            return postings
        with open(index_path, 'r') as indexFile:
            loaded_files[file_name] = json.load(indexFile)
    return loaded_files[file_name].get(term, [])


def parseQueryTerms(query: str) -> set:
    """
    Parses the query by stripping it and making it lowecased,
    then stemming the terms, returning the list of parsed terms
    """
    # Strips and lowercases the entire query
    whole_query = query.strip().lower()
    # Tokenizes and stems the query
    query_tokens = tokenize(whole_query)
    stemmer = PorterStemmer()
    stemmed_terms = set(stemmer.stem(term) for term in query_tokens)
    return stemmed_terms


def retrieveURLs(query: str, term_to_file_map: dict) -> list[str]:
    queryTerms = parseQueryTerms(query)
    numQueryTerms = len(queryTerms)
    if numQueryTerms < 1:
        return []
    
    term_postings = []
    loaded_files = {}
    for term in queryTerms:
        postings = fetchPostings(term, term_to_file_map, loaded_files)
        if len(postings) == 0:
            return []
        term_postings.append(postings)

    # Gets the common docIDs
    common_doc_ids = set() # Holds all docIDs in a set (for ease of intersecting)
    for posting in term_postings[0]:
        common_doc_ids.add(posting['document_ID'])

    for postings in term_postings[1:]: # Goes through postings, adding them to a current set that will be intersected
        current_ids = set()
        for posting in postings:
            current_ids.add(posting['document_ID'])
        common_doc_ids = common_doc_ids.intersection(current_ids) # Intersects (ANDs) common docIDs

    if len(common_doc_ids) == 0:
        return []

    # Adds up all the tf-idf scores for common docIDs
    doc_scores = {}
    for postings in term_postings:
        for posting in postings:
            doc_id = posting['document_ID']
            if doc_id in common_doc_ids:
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = 0
                doc_scores[doc_id] += posting['tf_idf']

    # Sorts the docIDs by tf-idf scores in a general "max element" sorting fashion
    sorted_docids = []
    while len(doc_scores) > 0:
        max_doc = None
        max_score = -1
        for doc_id in doc_scores:
            if doc_scores[doc_id] > max_score:
                max_score = doc_scores[doc_id]
                max_doc = doc_id
        sorted_docids.append(max_doc)
        del doc_scores[max_doc]
        if len(sorted_docids) == 5:
            break

    # Loads the docID to URL map
    with open("document_id_map.json", 'r') as docIDMapFile:
        doc_id_map = json.load(docIDMapFile)

    # Builds the final list of URLs
    result_urls = []
    for doc_id in sorted_docids:
        doc_id_str = str(doc_id)
        if doc_id_str in doc_id_map:
            result_urls.append(doc_id_map[doc_id_str])

    return result_urls
