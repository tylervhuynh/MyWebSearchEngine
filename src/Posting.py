"""
Posting.py holds a Posting class which represents an inverted index posting
"""

class Posting():
    def __init__(self, document_name, term_frequency):
        self.document_name = document_name
        self.term_frequency = term_frequency
