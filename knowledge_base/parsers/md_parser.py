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

    def __init__(self):
        super().__init__()

    def parse(self, file_path: str) -> Document:
        """
        Reads a .md file and returns the corresponding Document object.

        Raises:
            DocumentParsingError: if the file cannot be read or decoded as text.
            EmptyDocumentError: if the file has no meaningful content.
        """

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                
        except OSError as error:
            raise DocumentParsingError(f"Impossibile leggere il file '{file_path}': {error}") from error
        except UnicodeDecodeError as error:
            raise DocumentParsingError(f"Contenuto non decodificabile in '{file_path}': {error}") from error

        content = content.strip()
        if not content:
            raise EmptyDocumentError(f"Il file '{file_path}' e' vuoto.")

        title = self._extract_title(content, file_path)
        document_date = self._extract_date(content)

        return Document(
            title=title,
            content=content,
            document_format=self.FORMAT_MD,
            source_path=file_path,
            document_date=document_date,
        )

    # ----------------------------------------------------------------------
    # Override methods
    # ----------------------------------------------------------------------

    def _extract_date(self, content: str) -> date:
        """
        Searches for a date in the content.
        If found, returns the date.
        Otherwise, falls back to the default behavior.
        """

        found_date = self._search_date_in_text(content)
        if found_date:
            return found_date

        return super()._extract_date(content)

    def _extract_title(self, content: str, file_path: str) -> str:
        """
        Uses the first Markdown heading as title.
        If no heading is found, falls back to the default behavior.
        """

        for line in content.splitlines():
            match = HEADING_PATTERN.match(line.strip())
            if match:
                return match.group(1).strip()

        return super()._extract_title(content, file_path)
