"""
posting.py contains a Posting class which represents an inverted index posting
"""

class Posting:
    def __init__(self, documentID, term_frequency, position=0):
        self._documentID = documentID
        self._term_frequency = term_frequency
        self._position = position

    def getDocID(self) -> str:
        return self._documentID

    def getTermFrequency(self) -> str:
        return self._term_frequency
    
    def getPosition(self) -> int:
        return self._position
