import tkinter as tk
from tkinter import messagebox, scrolledtext
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


def generate_search_report(query: str, length: float) -> None:
    """
    Collects analytics from searching, writing it into a searching_report.txt file
    """
    with open("searching_report.txt", 'a', encoding="UTF-8") as report_file:
        report_file.write(f"Searching the query \"{query}\" took " + str(length) + " seconds\n")


class SearchEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MyWebSearchEngine")
        self.root.configure(bg="white")

        # Creates the title label
        tk.Label(root, text="Welcome to MyWebSearchEngine!", font=("Helvetica", 22, "bold"), bg="white", fg="blue").pack(pady=10)

        # Creates the query entry box
        self.query_entry = tk.Entry(root, width=50, bg="white", fg="red")
        self.query_entry.pack(pady=5)

        # Creats the search button
        self.search_button = tk.Button(root, text="Search", command=self.perform_search)
        self.search_button.pack(pady=5)

        # Creates the results display
        self.results_display = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, bg="white", fg="blue")
        self.results_display.pack(padx=10, pady=10)

    def perform_search(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query.")
            return
        start = time()
        urls = retrieveURLs(query)
        end = time()
        generate_search_report(query, end - start)
        self.results_display.delete(1.0, tk.END)
        if len(urls) > 0:
            self.results_display.insert(tk.END, f"Found {len(urls)} result(s):\n\n")
            for i in range(min(len(urls), 5)):
                self.results_display.insert(tk.END, f"{i + 1}. {urls[i]}\n")
        else:
            self.results_display.insert(tk.END, "No URLs found for your query.\n")


def main():
    root = tk.Tk()
    app = SearchEngineGUI(root)
    root.mainloop()


def runUserInterface() -> str | None:
    user_answer = input("\nHello there!\n\nWelcome to MyWebSearchEngine!\n\nWould you like to initialize the corpus? (y/n) ")
    if user_answer.lower() == 'n':
        print("\nGreat, you chose \'n\' to jump right into searching!")
        print("Lauching GUI...")
    elif user_answer.lower() == 'y':
        print("\nGreat, you chose \'y\' to initalize the corpus!\n\nBeginning initialization...")
        runIndexCorpus()
    else:
        print("\nInvalid input was recieved.\nExiting...")
        return None

    main() # Begins the GUI


def run():
    runUserInterface()


if __name__ == "__main__":
    run()
