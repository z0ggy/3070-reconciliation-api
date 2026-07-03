from src.similarity_score import SimilarityScore

"""
References:
    - https://docs.pytest.org/en/stable/
"""

scorer = SimilarityScore()


def test_empty_query():
    assert scorer.calculate_score("", "dublin") == 0.0


def test_exact_match():
    assert scorer.calculate_score("dublin", "dublin") == 1.0


def test_high_score_match():
    assert scorer.calculate_score("dublin", "county dublin") == 0.9


def test_fuzzy_match():
    score = scorer.calculate_score("dublinn", "dublin")
    assert 0.45 < score <= 0.9
