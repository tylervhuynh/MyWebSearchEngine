"""
inverted_index.py contains the InvertedIndex data structure
"""
from pathlib import Path
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
import warnings
from nltk.stem import PorterStemmer
from tokenizer import tokenize, compute_word_frequencies, is_near_duplicate, number_of_intersections
from posting import Posting
import json


class InvertedIndex:
    def __init__(self):
        self._buffer = {}
        self._docID_map = {}
        self._num_unique_tokens = 0
        self._num_documents = 0
        self._num_dumps = 0
    
    def getInvertedIndex(self):
        return self._buffer
    
    def getDocIDMap(self):
        return self._docID_map
    
    def getNumUniqueTokens(self):
        return self._num_unique_tokens
    
    def getNumDocuments(self):
        return self._num_documents
    
    def getNumDumps(self):
        return self._num_dumps
    
    def incrementUniqueTokens(self):
        self._num_unique_tokens += 1
    
    def incrementDocuments(self):
        self._num_documents += 1
    
    def dumpPartialIndex(self):
        self._num_dumps += 1
        serializable_buffer = {}
        for term, postings in self._buffer.items():
            serializable_buffer[term] = [posting.to_dict() for posting in postings]
        with open(f"partial_index{self._num_dumps}.json", 'w') as partial_index:
            json.dump(serializable_buffer, partial_index)
            self._buffer.clear() # Clears out buffer after having stored its contents
    
    def add_posting(self, token, frequency, document_id):
        """
        Creates a new Posting object out of the token, frequency, and document ID
        and adds it to the inverted index
        """
        new_posting = Posting(document_id, frequency)
        if token in self._buffer.keys():
            self._buffer[token].append(new_posting)
        else:
            self.incrementUniqueTokens()
            self._buffer[token] = [new_posting]
    
    def parse_content(self, file_contents: str, document_id: str, text_cache: set, token_cache: list) -> None:
        """
        Parses the text of the HTML file contents, tokenizing all words and
        calculating how frequently they occur in the file.
        """
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
        soup = BeautifulSoup(file_contents, 'lxml')
        content = soup.get_text()

        # Filtering for low/high information (<10 words or >1000000)
        word_count = len(content)
        if word_count < 10 or word_count > 100000:
            return

        # Filters exact duplicates
        if content not in text_cache:
            text_cache.add(content)
            if len(text_cache) > 20: # Limit cache size
                text_cache.pop()
        else:
            return

        # Filters near duplicates
        frequencies = compute_word_frequencies(content)
        if is_near_duplicate(frequencies, token_cache):
            return  # Too similar to a recent page
        token_cache.append(frequencies)
        if len(token_cache) > 20: # Limit cache size
            token_cache.pop(0)

        # Tokenizing
        token_list = tokenize(content)
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in token_list]
        token_frequencies = compute_word_frequencies(stemmed_tokens)
        for token, frequency in token_frequencies.items():
            self.add_posting(token, frequency, document_id)

        # Determines if a partial index must be stored on disk
        if self.getNumDocuments() % 15000 == 0:
            self.dumpPartialIndex()

    def parse_file(self, path_to_file: str, text_cache: set, token_cache: list) -> None:
        """
        Parses the given .json file by opening it and parsing its content
        """
        try:
            # Opens .json file and loads the contents, essentially accessing the webpage
            with open(path_to_file, 'r') as file:
                json_file = json.load(file)
                file_contents = json_file["content"]
                document_id = self.getNumDocuments() + 1
                self._docID_map[document_id] = json_file["url"]

                # Increments the "unique documents found" counter and parses contents
                self.incrementDocuments()
                self.parse_content(file_contents, document_id, text_cache, token_cache)
        except FileNotFoundError:
            print(f"Error: The file {path_to_file} was not found.")
        except PermissionError:
            print(f"Error: You do not have permission to read {path_to_file}.")
        except json.JSONDecodeError as e:
            print(f"Failed to parse {path_to_file}: {e}")
    
    def parse_subdomain(self, path_to_subdomain: Path, text_cache: set, token_cache: list) -> None:
        """
        Parses the input subdomain directory by passing each webpage file into
        the parse_file() method
        """
        subdomain_path = Path(path_to_subdomain)
        
        # Instantly returns if subdomain path is not a valid directory
        if not subdomain_path.is_dir():
            return

        # Iterates through the subdomain's webpages, parsing it's files
        webpages_iterable = subdomain_path.iterdir()
        for webpage in webpages_iterable:
            if webpage.is_file():
                self.parse_file(str(webpage), text_cache, token_cache)
    
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

        # Instant return if the path is not a valid directory
        if not directory_path.is_dir():
            return

        # Iterates through every subdomain in the directory
        subdomains_iterable = directory_path.iterdir()

        text_cache = set()
        token_cache = []
        # count = 0
        for subdomain in subdomains_iterable:
            # if count > 6: break
            # print(subdomain)
            self.parse_subdomain(subdomain, text_cache, token_cache)
            # count += 1

        self.dumpPartialIndex()
