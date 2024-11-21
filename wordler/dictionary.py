from typing import List


def get_words_list() -> List[str]:
    with open("dictionary.txt") as f:
        return f.read().splitlines()
