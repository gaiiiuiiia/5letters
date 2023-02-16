from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict

from utils import get_only_nouns

EXCLUDE_LETTER_SIGN = "-"
WRONG_POSITION_SIGN = "?"


@dataclass
class ParsedWord:
    correct: dict
    wrong: DefaultDict[int, set[str]]
    exclude: set


def main() -> None:
    words = get_only_nouns(load_words("russian5.txt"))
    word_len = 5
    print(f"--- {word_len}букв ---")
    print("введи запрос, например ко?ш-ка")
    print("обе буквы `к` стоят на своих местах,\n"
          "буквы `ш` нет в слове,\n"
          "а буква `о` не на своем месте.\n")
    while True:
        try:
            user_input = input("запрос:... ")
        except KeyboardInterrupt:
            break
        parsed_word = parse_word(user_input)
        words = filter_words(words, parsed_word)

        print(words)


def parse_word(word: str) -> ParsedWord:
    correct_position_letters = {}
    wrong_position_letters = defaultdict(set)
    excluded_letters = set()

    current_letter_index = 0
    for index in range(len(word) - 1):
        current_letter = word[index]
        next_letter = word[index + 1]
        if next_letter == EXCLUDE_LETTER_SIGN:
            excluded_letters.update(set(current_letter))
            current_letter_index += 1
            continue
        if next_letter == WRONG_POSITION_SIGN:
            wrong_position_letters[current_letter_index].update(set(current_letter))
            current_letter_index += 1
            continue
        if current_letter not in {EXCLUDE_LETTER_SIGN, WRONG_POSITION_SIGN}:
            correct_position_letters[current_letter_index] = current_letter
            current_letter_index += 1

        if index + 1 == len(word) - 1:
            correct_position_letters[current_letter_index] = next_letter

    return ParsedWord(correct_position_letters, wrong_position_letters, excluded_letters)


def filter_words(words: list[str], parsed_word: ParsedWord) -> list[str]:
    def filter_func(word: str) -> bool:
        for index, letter in parsed_word.correct.items():
            if word[index] != letter:
                return False

        for index, letters in parsed_word.wrong.items():
            if word[index] in letters:
                return False
            if len(letters & set(word)) != len(letters):
                return False

        if len(set(word) & parsed_word.exclude):
            return False

        return True

    return list(filter(filter_func, words))


def load_words(filename: str) -> list[str]:
    with open(filename, mode="r", encoding="utf-8") as words:
        return list(set([word.strip() for word in words.readlines()]))


if __name__ == '__main__':
    main()
