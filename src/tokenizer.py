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

def is_near_duplicate(frequencies, token_cache):
    for cached_dictionary in token_cache:
        intersections = number_of_intersections(frequencies, cached_dictionary)
        max_length = max(len(frequencies), len(cached_dictionary))
        if max_length == 0:
            continue  # Avoids division by zero
        similarity = intersections / max_length
        if similarity > 0.99:
            return True
    return False

def number_of_intersections(frequencies1: dict, frequencies2: dict):
    # First picks smaller dictionary to traverse with, all O(1) instructions
    if len(frequencies1) <= len(frequencies2):
        smaller_frequencies = frequencies1
        larger_frequencies = frequencies2
    else:
        smaller_frequencies = frequencies2
        larger_frequencies = frequencies1

    # Traverses one dictionary, seeking intersections, O(N)
    counter = 0
    for token in smaller_frequencies.keys():
        if token in larger_frequencies:
            counter += 1
    return counter
