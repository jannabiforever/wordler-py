from typing import List


def get_words_list() -> List[str]:
    def get_word(x): return x[0]
    with open("dictionary.txt") as f:
        parsed = f.read().splitlines()
        return list(map(get_word, parsed))
