"""
posting.py contains a Posting class which represents an inverted index posting
"""

class Posting:
    def __init__(self, documentID, term_frequency, important, tf_idf=0):
        self._documentID = documentID
        self._term_frequency = term_frequency
        self._important = important
        self._tf_idf = tf_idf

    def getDocID(self) -> str:
        return self._documentID

    def getTermFrequency(self) -> str:
        return self._term_frequency
    
    def getImportant(self) -> bool:
        return self._important
    
    def getTfIdf(self) -> float:
        return self._tf_idf
    
    def setTfIdf(self, new_tf_idf: float) -> None:
        self._tf_idf = new_tf_idf

    def to_dict(self):
        return {"document_ID": self._documentID, "term_frequency": self._term_frequency, "important": self._important, "tf_idf": self._tf_idf}
