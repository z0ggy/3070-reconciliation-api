import re
import unicodedata

"""
References:
    - https://stackoverflow.com/questions/51710082/what-does-unicodedata-normalize-do-in-python
    - https://github.com/utkdigitalinitiatives/geonames-reconcile
    - https://github.com/elyase/geotext/blob/master/geotext/geotext.py
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

        # Search regex pattern and replace abbreviation.
        return re.sub(r"\bd\.?\s*l\.?\s*r\.?\b", "dlr", text, flags=re.IGNORECASE)

    def convert_county_abbreviation(self, text: str) -> str:
        """
        Convert county abbreviation examples:
        'Co Dublin', 'Co. Dublin' -> 'county dublin'
        'Dublin Co', 'Dublin Co.' -> 'dublin county'
        """

        # Co Dublin / Co. Dublin -> county dublin.
        text = re.sub(r"\bco\.?\s+", "county ", text, flags=re.IGNORECASE)

        # Dublin Co / Dublin Co. -> dublin county.
        text = re.sub(r"\s+co\.?$", " county", text, flags=re.IGNORECASE)

        return text

    def convert_county_of(self, text: str) -> str:
        """Convert 'county of dublin' to 'county dublin'."""
        return re.sub(r"\bcounty\s+of\s+", "county ", text, flags=re.IGNORECASE)

    def remove_country_suffix(self, text: str) -> str:
        """
        Remove broad country suffixes.

        Example:
        'Dublin, Ireland' -> 'dublin'
        'Dublin Ireland' -> 'dublin'
        """

        text = re.sub(r"\bireland\b", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"\beire\b", " ", text, flags=re.IGNORECASE)

        return text

    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation symbols"""

        # Remove non letters characters except: dashes, spaces, slashes.
        return re.sub(r"[^a-z0-9\s/-]", " ", text)

    def replace_separators(self, text: str) -> str:
        """Replace dash and slash separators with spaces."""

        text = text.replace("-", " ")
        text = text.replace("/", " ")
        return text

    def normalise_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def normalise_base(self, text: str) -> str:
        """
        Base normaliser, country context ('Ireland' or 'Éire') is preserved.
        """
        if not text:
            return ""

        text = self.remove_accents(text)
        text = self.lower_case_and_strip(text)

        # Handle special abbreviations before punctuation is removed.
        text = self.convert_official_abbreviation(text)

        # Clean punctuation and separators.
        text = self.remove_punctuation(text)
        text = self.replace_separators(text)
        text = self.normalise_whitespace(text)

        # Normalise geographic cues.
        text = self.convert_county_of(text)
        text = self.convert_county_abbreviation(text)

        return self.normalise_whitespace(text)

    def normalise(self, text: str) -> str:
        """
        Normalise a place name for text matching.

        Country context is removed to preserve the behaviour from
        previous sprints.
        Example: normaliser.normalise("Dublin, Ireland") >>> "dublin"
        """
        text = self.normalise_base(text)
        text = self.remove_country_suffix(text)

        return self.normalise_whitespace(text)

    def normalise_with_context(self, text: str) -> str:
        """
        Normalise a query while keeping the country context.
        Example: normaliser.normalise_with_context("Dublin, Ireland") >>> "dublin ireland"
        """
        return self.normalise_base(text)
