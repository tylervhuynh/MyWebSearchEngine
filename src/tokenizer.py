"""
tokenize(text_file_path) takes an input string content representing a text string
and returns a list of the tokens contained in the string. Here, a token is defined as:
"a sequence of alphanumeric characters, independent of capitalization".
"""
def tokenize(content: str) -> list[str]:
    tokens = []
    valid_characters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                        's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
                        '2', '3', '4', '5', '6', '7', '8', '9'}
    token = ""
    for character in content:
        if character in valid_characters: # Ensuring "bad inputs" are skipped over
            token += character
        else:
            if token != "":
                tokens.append(token.lower())
                token = ""
    if token != "":
        tokens.append(token.lower())
    return tokens


"""
compute_word_frequencies(tokens) takes in a list of tokens and counts the number of
occurrences of each token in the token list, returning a dictionary with tokens as keys
and their respective frequencies as values.
"""
def compute_word_frequencies(tokens: list) -> dict:
    frequencies = {}
    for token in tokens: # O(N), traversing through N tokens
        if token not in frequencies:
            frequencies[token] = 1 # Adds token to frequencies dictionary
        else:
            frequencies[token] += 1 # Increments token's frequency in dictionary
    return frequencies


"""
print_tokens(token_dict) takes in a dictionary containing tokens and their frequencies
and prints out the contents in sorted decreasing order determined by their frequencies.
"""
def print_tokens(token_dict: dict) -> None:
    if len(token_dict) < 1: return # Returns if token_dict is empty
    inverse_dict = {}

    # Creates an inverted dictionary storing frequencies as keys
    # and their respective tokens in a list as the value: O(N)
    for token, frequency in token_dict.items():
        if frequency not in inverse_dict:
            inverse_dict[frequency] = [token]
        else:
            inverse_dict[frequency].append(token)

    # Sorts frequencies in descending order, O(Nlogn)
    sorted_frequencies = sorted(inverse_dict.keys(), reverse=True)

    # Double for-loop is still O(N) since it essentially traverses all tokens
    for frequency in sorted_frequencies:
        for token in inverse_dict[frequency]:
            print(f'{token} -> {frequency}')
