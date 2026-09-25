import re
from datetime import date

from ..document import Document
from ..exceptions import DocumentParsingError, EmptyDocumentError
from .parser import Parser

# Riconosce una riga di intestazione Markdown tipo "# Titolo" o "## Titolo".
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.*)")


class MarkdownParser(Parser):
    """
    Parses .md files into Document objects.
    """

    FORMAT_MD = "md"

    def __init__(self, file_path: str):
        super().__init__(file_path)

    # ----------------------------------------------------------------------
    # Override methods
    # ----------------------------------------------------------------------

    def _get_format(self) -> str:
        return self.FORMAT_MD

    def _extract_date(self, content: str) -> date:
        found_date = self._search_date_in_text(content)
        if found_date:
            return found_date

        return super()._extract_date(content)

    def _extract_title(self, content: str) -> str:
        for line in content.splitlines():
            match = HEADING_PATTERN.match(line.strip())
            if match:
                return match.group(1).strip()

        return super()._extract_title(content)
