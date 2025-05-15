from inverted_index import InvertedIndex

CORPUS_PATH = "DEV"


def generate_report(inverted_index: InvertedIndex) -> None:
    """
    Collects analytics from InvertedIndex into a report.txt file
    """
    with open("report.txt", 'w', encoding="UTF-8") as report_file:
        report_file.write("Inverted Index indexing report:\n\n")
        report_file.write("The number of indexed documents was " + str(inverted_index.getNumDocuments()) + '\n\n')
        report_file.write("The number of unique tokens was " + str(inverted_index.getNumUniqueTokens()) + '\n\n')
        report_file.write("The total size (in KB) of the index on disk is " + "x" + '\n\n')
        report_file.write("Inverted Index Document ID Mapping: " + str(inverted_index.getDocIDMap()))


def run():
    inverted_index = InvertedIndex()
    inverted_index.create_index(CORPUS_PATH)
    generate_report(inverted_index)


if __name__ == "__main__":
    run()
