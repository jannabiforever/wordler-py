from typing import List, Dict
from collections import Counter
from math import log
import logging
from .guess import Guesser, Guess, compute_correctness
from .dictionary import get_words_list


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="naive_guesser.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def score_from_poss(possibility: float) -> float:
    if possibility == 0:
        return 0
    return -possibility * log(possibility)


class NaiveGuesser(Guesser):
    def __init__(self):
        self.words = get_words_list()

    def guess(self, history: List[Guess]) -> str:
        if len(history) > 0:
            self._exclude_impossible(history[-1])
        scores = self._compute_scores()

        return max(scores.keys(), key=lambda x: scores[x])

    def _exclude_impossible(self, guess: Guess) -> None:
        self.words = list(filter(lambda x: guess.matches(x), self.words))

    def _compute_scores(self) -> Dict[str, float]:
        scores = {}
        for word in self.words:
            scores[word] = self._compute_score(word)
            logger.info(f"Score for {word}: {scores[word]}")

        return scores

    def _compute_score(self, word: str) -> float:
        assert word in self.words

        crts_counter = Counter()
        for answer in self.words:
            # in case `answer` is the correct word
            crts_counter[compute_correctness(answer, word)] += 1

        crts_poss = list(
            map(lambda c: c / len(self.words), crts_counter.values())
        )

        return sum(map(score_from_poss, crts_poss))


if __name__ == "__main__":
    print(len(NaiveGuesser().words))
