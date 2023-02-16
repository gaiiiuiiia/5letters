from src.main import parse_word, filter_words


def test_filter_word() -> None:
    word = "м-ошка"
    words = ["кошка", "лимон", "мошка"]
    parsed_word = parse_word(word)

    res = filter_words(words, parsed_word)

    assert res == ["кошка"]

    word = "фы?вка?"
    words = ["фывки", "фавкы", "фывка"]
    parsed_word = parse_word(word)

    res = filter_words(words, parsed_word)

    assert res == ["фавкы"]

    word = "ко?ш-ка"
    words = ["кафка"]
    parsed_word = parse_word(word)

    res = filter_words(words, parsed_word)

    assert [] == res


def test_parse_word() -> None:
    res = parse_word("ко-ш-л-а?н")
    assert res.correct[0] == "к"
    assert res.correct[5] == "н"
    assert {"о", "ш", "л"} == res.exclude
    assert "а" in res.wrong[4]

    res = parse_word("до?м?и?ш-ко")
    assert res.correct[0] == "д"
    assert res.correct[5] == "к"
    assert res.correct[6] == "о"
    assert "о" in res.wrong[1]
    assert "м" in res.wrong[2]
    assert "и" in res.wrong[3]
    assert {"ш"} == res.exclude

    res = parse_word("да?")
    assert res.correct[0] == "д"
    assert "а" in res.wrong[1]

    res = parse_word("д?а")
    assert res.correct[1] == "а"
    assert "д" in res.wrong[0]
