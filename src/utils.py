import pymorphy2


def create_fixed_len_words(
        word_len: int,
        result_filename: str,
        source_filename: str,
        source_encoding: str = "windows-1251",
) -> None:
    with open(source_filename, mode="r", encoding=source_encoding) as words:
        with open(result_filename, mode="w", encoding="utf-8") as result_file:
            result_file.write(
                "\n".join(
                    set([word.strip().lower() for word in words if len(word.strip()) == word_len])
                )
            )


def get_only_nouns(words: list[str], lang: str = "ru") -> list[str]:
    morph = pymorphy2.MorphAnalyzer(lang=lang)

    res = []

    for word in words:
        parses = morph.parse(word)
        parse_with_max_score = max(parses, key=lambda parse: parse.score)
        if parse_with_max_score.tag.POS == "NOUN" and parse_with_max_score.word == word:
            res.append(word)

    return res
