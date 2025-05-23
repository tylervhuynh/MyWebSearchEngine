def retrieveURLs(query: str):
    query_terms = query.strip().lower().split()
    for term in query_terms:
        first_char = term[0]
