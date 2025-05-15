"""
inverted_index.py contains the InvertedIndex data structure
"""
from pathlib import Path
import json


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
    
    def parse_file(self, path_to_file: str) -> None:
        try:
            with open(path_to_file, 'r') as file:
                json_file = json.load(file)
                file_contents = json_file["content"]
                self.parse_contents(file_contents)
        except json.JSONDecodeError as e:
            print(f"Failed to parse {path_to_file}: {e}")
        except FileNotFoundError:
            print(f"Error: The file {path_to_file} was not found.")
        except PermissionError:
            print(f"Error: You do not have permission to read {path_to_file}.")
    
    def parse_subdomain(self, path_to_subdomain: Path) -> None:
        """
        Parses the input subdomain directory by passing each webpage file into
        the parse_file() method
        """
        subdomain_path = Path(path_to_subdomain)
        if not subdomain_path.is_dir():
            return

        webpages_iterable = subdomain_path.iterdir()
        for webpage in webpages_iterable:
            if webpage.is_file():
                self.parse_file(str(webpage))
    
    def create_index(self, path_to_corpus: str) -> None:
        """
        create_index() develops the inverted index by iterating through subdomains and their 
        respective webpages in a corpus directory, strictly parsing only directories formatted
        with the structure: Directory/Subdomains -> Subdomain/.json file
        JSON fields format:
        “url” : contains the URL of the page. (ignore the fragment part, if you see it)
        “content” : contains the content of the page, as found during crawling
        "encoding" : an indication of the encoding of the webpage
        """
        directory_path = Path(path_to_corpus)
        if not directory_path.is_dir():
            return

        subdomains_iterable = directory_path.iterdir()
        for subdomain in subdomains_iterable:
            self.parse_subdomain(subdomain)
