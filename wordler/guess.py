from abc import ABC, abstractmethod
from typing import List, Tuple
from enum import Enum


class Correctness(Enum):
    CORRECT = 1  # Green
    MISPLACED = 2  # Yellow
    WRONG = 3  # Gray


def correctness_from_string(s: str) -> Tuple[Correctness, Correctness, Correctness, Correctness, Correctness]:
    assert len(s) == 5
    crts = []
    for char in s:
        match char:
            case "C": crts.append(Correctness.CORRECT)
            case "M": crts.append(Correctness.MISPLACED)
            case "W": crts.append(Correctness.WRONG)
            case _: raise ValueError(f"Invalid character: {char}")

    return tuple(crts)


def is_misplaced(letter: str, answer: str, used: List[bool]) -> bool:
    assert len(letter) == 1
    assert len(answer) == 5

    return any(a == letter and not used for a, used in zip(answer, used))


def compute_correctness(answer: str, guess: str) -> Tuple[Correctness, Correctness, Correctness, Correctness, Correctness]:
    assert len(answer) == 5
    assert len(guess) == 5

    result: List[Correctness] = [Correctness.WRONG] * 5
    misplaced = [0] * 26  # Count of each letter in the answer

    # correct letters
    for i in range(5):
        if answer[i] == guess[i]:
            result[i] = Correctness.CORRECT
        else:
            misplaced[ord(answer[i].upper()) - ord("A")] += 1

    # misplaced letters
    for i in range(5):
        if result[i] == Correctness.WRONG:
            idx = ord(guess[i].upper()) - ord("A")
            if misplaced[idx] > 0:
                result[i] = Correctness.MISPLACED
                misplaced[idx] -= 1

    return (result[0], result[1], result[2], result[3], result[4])


class Guess:
    """A guess of a word.
    It contains the correctness of each letter in the word.
    """

    def __init__(self, word: str, mask: Tuple[Correctness, Correctness, Correctness, Correctness, Correctness]):
        assert len(word) == 5

        self.word = word
        self.mask = mask

    def matches(self, other: str) -> bool:
        """ Check if the guess would be possible to observe when `word` is the correct answer."""

        assert len(other) == 5

        used = [False] * 5

        # Check Correct Letters
        for i, (a, b) in enumerate(zip(self.word, other)):
            if a == b:
                if self.mask[i] != Correctness.CORRECT:
                    return False
                used[i] = True
            elif self.mask[i] == Correctness.CORRECT:
                return False

        # Check Misplaced Letters
        for a, (w, m) in enumerate(zip(self.word, self.mask)):
            if m == Correctness.CORRECT:
                continue
            if is_misplaced(w, other, used) != (m == Correctness.MISPLACED):
                return False

        return True


class Guesser(ABC):
    @abstractmethod
    def guess(self, history: List[Guess]) -> str:
        """Guess the next word based on the history of guesses.

        Args:
            history: A list of previous guesses.

        Returns:
            str: The best word for coming next.
        """
        pass
