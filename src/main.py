from inverted_index import InvertedIndex
from pathlib import Path
from time import time

CORPUS_PATH = "DEV"


def generate_report(inverted_index: InvertedIndex, length: float) -> None:
    """
    Collects analytics from InvertedIndex into a report.txt file
    """
    with open("report.txt", 'w', encoding="UTF-8") as report_file:
        report_file.write("Inverted Index indexing report:\n\n")
        report_file.write("Index creation took " + str(length) + " seconds\n")
        report_file.write("Number of indexed documents: " + str(inverted_index.getNumDocuments()) + '\n\n')
        report_file.write("Number of unique tokens: " + str(inverted_index.getNumUniqueTokens()) + '\n\n')

        index_byte_count = 0
        for i in range(0, inverted_index.getNumDumps()):
            file_path = Path(f"full_inverted_index.json")
            if file_path.exists():
                index_byte_count += file_path.stat().st_size
        report_file.write(f"Index size on disk: {str(index_byte_count / 1024)} KB ({str(index_byte_count)} bytes)\n")


def runIndexCorpus() -> None:
    inverted_index = InvertedIndex()
    start = time()
    inverted_index.create_index(CORPUS_PATH)
    end = time()
    length = end - start
    generate_report(inverted_index, length)


def run():
    user_answer = input("\nHello there!\n\nWelcome to MyWebSearchEngine!\n\nWould you like to initialize the corpus? (y/n) ")
    if user_answer.lower() == 'n':
        print("\nGreat, you chose \'n\' to JUMP RIGHT INTO SEARCHING!\n")
    elif user_answer.lower() == 'y':
        print("\nGreat, you chose \'y\' to INITIALIZE THE CORPUS\n\nBeginning Initialization...")
        runIndexCorpus()
    else:
        print("\nInvalid input was recieved.\nExiting...")
        return
    query = input("Please enter your search query: ")


if __name__ == "__main__":
    run()
