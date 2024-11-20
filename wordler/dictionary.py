from typing import List, Tuple


def parse_down_each_line(lines: List[str]) -> List[Tuple[str, int]]:
    result = []
    for line in lines:
        word, freq = line.split()
        result.append((word, int(freq)))

    return result


def get_words_list() -> List[str]:
    def get_word(x): return x[0]
    with open("dictionary.txt") as f:
        parsed = parse_down_each_line(f.read().splitlines())
        return list(map(get_word, parsed))
