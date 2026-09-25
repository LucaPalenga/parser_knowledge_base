from datetime import date

from ..document import Document
from .parser import Parser


class TxtParser(Parser):
    """
    Parses .txt files into Document objects.
    """

    FORMAT_TXT = "txt"

    def __init__(self, file_path: str):
        super().__init__(file_path)

    # ----------------------------------------------------------------------
    # Override methods
    # ----------------------------------------------------------------------

    def _get_format(self) -> str:
        return self.FORMAT_TXT

    def _extract_date(self, content: str) -> date:
        found_date = self._search_date_in_text(content)
        if found_date:
            return found_date

        return super()._extract_date(content)

    def _extract_title(self, content: str) -> str:
        for line in content.splitlines():
            stripped_line = line.strip()
            if stripped_line:
                return stripped_line

        return super()._extract_title(content)
