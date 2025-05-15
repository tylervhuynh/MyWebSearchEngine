"""
inverted_index.py contains the InvertedIndex data structure
"""
from pathlib import Path


class InvertedIndex:
    def __init__(self):
        self._buffer = {}
        self._num_unique_tokens = 0
        self._num_documents = 0
    
    def getInvertedIndex(self):
        return self._buffer
    
    def getNumUniqueTokens(self):
        return self._num_unique_tokens
    
    def getNumDocuments(self):
        return self._num_documents
    
    def incrementUniqueTokens(self):
        self._num_unique_tokens += 1
    
    def incrementDocuments(self):
        self._num_documents += 1
    
    def parse(self, path_to_corpus: str) -> None:
        """
        parse() method assists in parsing multiple files in a corpus directory and
        strictly parses directories formatted with the structure:
        Directory/Subdomains -> Subdomain/.JSON file

        JSON fields format:
        “url” : contains the URL of the page. (ignore the fragment part, if you see it)
        “content” : contains the content of the page, as found during crawling
        "encoding" : an indication of the encoding of the webpage
        """
        directory_path = Path(path_to_corpus)
        if not directory_path.is_dir():
            return

        try:
            subdomains_iterable = directory_path.iterdir()
            for subdomain in subdomains_iterable:
                print("YASSS")
        except FileNotFoundError:
            print(f"Error: The file {directory_path} was not found.")
        except PermissionError:
            print(f"Error: You do not have permission to read {directory_path}.")
    
    def create_index(self, path_to_corpus: str) -> None:
        self.parse(path_to_corpus)
