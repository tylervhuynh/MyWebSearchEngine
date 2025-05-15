"""
posting.py contains a Posting class which represents an inverted index posting
"""

class Posting:
    def __init__(self, documentID, term_frequency):
        self._documentID = documentID
        self._term_frequency = term_frequency

    def getDocID(self) -> str:
        return self._documentID

    def getTermFrequency(self) -> str:
        return self._term_frequency

    def incrementTermFrequency(self) -> None:
        self._term_frequency += 1
