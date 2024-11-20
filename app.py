from wordler.naive_guesser import NaiveGuesser
from wordler.guess import Guess, Correctness, correctness_from_string
import time

supported_engines = [
    ("Naive Guesser", "Very simple guesser that guesses the word with the highest entropy.")
]

if __name__ == "__main__":
    print("Welcome to Wordle Solver!")
    for i, engine in enumerate(supported_engines):
        engine_name = engine[0]
        engine_desc = engine[1]
        print(f"[{i + 1}] {engine_name}: {engine_desc}")

    while True:
        engine_choice = int(input("Choose an engine: "))
        if engine_choice in range(1, len(supported_engines) + 1):
            break
        print("Invalid choice. Try again.")

    print(f"Initializing {supported_engines[engine_choice - 1][0]}...")
    start = time.time_ns()
    match engine_choice:
        case 1:
            guesser = NaiveGuesser()
        case _:
            raise ValueError("Unreachable code")

    print(f"Initialized in {(time.time_ns() - start) / (1000 ** 2):.2f} ms.")

    game_history = []
    while len(game_history) == 0 or game_history[-1].mask != [Correctness.CORRECT] * 5:
        print(f"Guessing ...")
        guess = guesser.guess(game_history)
        print(f"Guessing {guess}")
        correctness = correctness_from_string(input("Enter correctness: "))
        game_history.append(Guess(guess, correctness))
