from inverted_index import InvertedIndex
from searcher import retrieveURLs
from pathlib import Path
from os import listdir
from time import time

CORPUS_PATH = "DEV"


def generate_index_report(inverted_index: InvertedIndex, length: float) -> None:
    """
    Collects analytics from InvertedIndex into an indexing_report.txt file
    """
    with open("indexing_index_report.txt", 'w', encoding="UTF-8") as report_file:
        report_file.write("Inverted Index indexing report:\n\n")
        report_file.write("Index creation took " + str(length) + " seconds\n")
        report_file.write("Number of indexed documents: " + str(inverted_index.getNumDocuments()) + '\n\n')
        report_file.write("Number of unique tokens: " + str(inverted_index.getNumUniqueTokens()) + '\n\n')

        index_byte_count = 0
        index_ranges_directory = Path("index_ranges")
        for filename in listdir(index_ranges_directory):
            file_path = index_ranges_directory / filename
            if file_path.is_file() and filename.endswith(".json"):
                index_byte_count += file_path.stat().st_size
        report_file.write(f"Index size on disk: {str(index_byte_count / 1024)} KB ({str(index_byte_count)} bytes)\n")


def runIndexCorpus() -> None:
    inverted_index = InvertedIndex()
    start = time()
    inverted_index.create_index(CORPUS_PATH)
    end = time()
    length = end - start
    print("\nCompleted indexing\n")
    generate_index_report(inverted_index, length)


def generate_search_report(length: float) -> None:
    """
    Collects analytics from searching, writing it into a searching_report.txt file
    """
    with open("searching_report.txt", 'w', encoding="UTF-8") as report_file:
        report_file.write("Searching report:\n\n")
        report_file.write("Searching took " + str(length) + " seconds\n")


def runSearch(query: str) -> list:
    urls = retrieveURLs(query)
    if len(urls) > 0:
        print("\nURLS FOUND:")
        for i in range(min(len(urls), 5)):
            print(f"{i + 1}: {urls[i]}")
    else:
        print("\nNO URLS FOUND:\n")


def runUserInterface() -> str | None:
    user_answer = input("\nHello there!\n\nWelcome to MyWebSearchEngine!\n\nWould you like to initialize the corpus? (y/n) ")
    if user_answer.lower() == 'n':
        print("\nGreat, you chose \'n\' to JUMP RIGHT INTO SEARCHING!")
    elif user_answer.lower() == 'y':
        print("\nGreat, you chose \'y\' to INITIALIZE THE CORPUS\n\nBeginning initialization...")
        runIndexCorpus()
    else:
        print("\nInvalid input was recieved.\nExiting...")
        return None

    while True:
        query = input("\nPlease enter your search query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        start = time()
        runSearch(query)
        end = time()
        # generate_search_report(end - start)


def run():
    runUserInterface()


if __name__ == "__main__":
    run()
