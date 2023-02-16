from src.utils import get_only_nouns


def test_get_only_nouns_from_words() -> None:
    words = ["стали", "бегал", "катер", "ветер"]

    nouns = get_only_nouns(words)

    assert nouns == ["катер", "ветер"]
