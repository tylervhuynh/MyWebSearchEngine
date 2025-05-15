from inverted_index import InvertedIndex

CORPUS_PATH = "DEV"


def generate_report(inverted_index: InvertedIndex) -> None:
    """
    Collects analytics from InvertedIndex into a report.txt file
    """
    print(inverted_index.getNumDocuments())
    print(inverted_index.getNumUniqueTokens())


def run():
    inverted_index = InvertedIndex()
    inverted_index.create_index(CORPUS_PATH)
    generate_report(inverted_index)


if __name__ == "__main__":
    run()
