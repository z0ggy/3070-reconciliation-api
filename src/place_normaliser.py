import re
import unicodedata

"""
References:
    - https://stackoverflow.com/questions/51710082/what-does-unicodedata-normalize-do-in-python
"""


class PlaceNameNormaliser:
    """Normalise query string"""

    def remove_accents(self, text: str) -> str:
        """Remove accent letters from entity name"""

        # Split accent letters example: "ú" is split into "u" + accent mark.
        text = unicodedata.normalize("NFKD", text)

        # remove any accent marks
        return "".join(char for char in text if not unicodedata.combining(char))

    def lower_case_and_strip(self, text: str) -> str:
        """Convert entity to lower case and strip empty spaces."""
        return text.lower().strip()

    def convert_official_abbreviation(self, text: str) -> str:
        """Convert known Irish geographic abbreviation. Example: D.L.R. / DLR / D L R -> 'dlr'"""

        # Search regex pattern and replace abbreviation
        return re.sub(r"\bd\.?\s*l\.?\s*r\.?\b", "dlr", text, flags=re.IGNORECASE)

    def convert_county_abbreviation(self, text: str) -> str:
        """
        Convert county abbreviation examples:
        'Co Dublin', 'Co. Dublin' -> 'county dublin'
        'Dublin Co', 'Dublin Co.' -> 'dublin county'
        """

        # Co Dublin / Co. Dublin -> county dublin
        text = re.sub(r"\bco\.?\s+", "county ", text, flags=re.IGNORECASE)

        # Dublin Co / Dublin Co. -> dublin county
        text = re.sub(r"\s+co\.?$", " county", text, flags=re.IGNORECASE)

        return text

    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation symbols"""

        # Remove non letters characters
        return re.sub(r"[^a-z0-9\s-]", " ", text)

    def replace_dash(self, text: str) -> str:
        """Replace '-' (dash) symbol"""
        return text.replace("-", " ")

    def normalise_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def normalise(self, text: str) -> str:
        """Pipeline/wrapper for normalise text functions"""
        text = self.remove_accents(text)
        text = self.lower_case_and_strip(text)
        text = self.remove_punctuation(text)
        text = self.replace_dash(text)
        text = self.convert_official_abbreviation(text)
        text = self.normalise_whitespace(text)
        return text
