from difflib import SequenceMatcher

"""
References:
    - https://stackoverflow.com/questions/10018679/python-find-closest-string-from-a-list-to-another-string
    - https://docs.python.org/3/library/difflib.html
    - https://docs.python.org/3/library/difflib.html#sequencematcher-objects
    - https://www.geeksforgeeks.org/python/sort-in-python/
"""


class SimilarityScore:
    """
    compare two normalized strings and return similarity score.
    query: str represent normalised input query.
    candidate: str represent normalised official name from dataset.
    """

    def calculate_score(self, query: str, candidate: str) -> float:
        if not query or not candidate:
            return 0.0

        if query == candidate:
            return 1.0

        elif query in candidate:
            return 0.9

        elif candidate in query:
            return 0.9

        else:
            return SequenceMatcher(None, query, candidate).ratio()
