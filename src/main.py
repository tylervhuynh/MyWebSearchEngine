from inverted_index import InvertedIndex
from pathlib import Path

CORPUS_PATH = "DEV"


def generate_report(inverted_index: InvertedIndex) -> None:
    """
    Collects analytics from InvertedIndex into a report.txt file
    """
    with open("report.txt", 'w', encoding="UTF-8") as report_file:
        report_file.write("Inverted Index indexing report:\n\n")
        report_file.write("Number of indexed documents: " + str(inverted_index.getNumDocuments()) + '\n\n')
        report_file.write("Number of unique tokens: " + str(inverted_index.getNumUniqueTokens()) + '\n\n')

        index_byte_count = 0
        for i in range(0, inverted_index.getNumDumps()):
            file_path = Path(f"partial_index{i + 1}.json")
            if file_path.exists():
                index_byte_count += file_path.stat().st_size
        report_file.write(f"Index size on disk: {str(index_byte_count / 1024)} KB ({str(index_byte_count)} bytes)\n")


def run():
    inverted_index = InvertedIndex()
    inverted_index.create_index(CORPUS_PATH)
    generate_report(inverted_index)


if __name__ == "__main__":
    run()
