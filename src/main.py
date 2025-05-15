from inverted_index import InvertedIndex

CORPUS_PATH = "/DEV"


def run():
    inverted_index = InvertedIndex()
    inverted_index.create_index(CORPUS_PATH)


if __name__ == "__main__":
    run()
