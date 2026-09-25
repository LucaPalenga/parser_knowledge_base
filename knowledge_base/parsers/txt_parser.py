from datetime import date

from ..document import Document
from ..exceptions import DocumentParsingError, EmptyDocumentError
from .parser import Parser


class TxtParser(Parser):
    """
    Parses .txt files into Document objects.
    """

    FORMAT_TXT = "txt"

    def __init__(self):
        super().__init__()

    def parse(self, file_path: str) -> Document:
        """
        Reads a .txt file and returns the corresponding Document object.

        Args:
            file_path: path of document

        Raises:
            DocumentParsingError: if the file cannot be read or decoded as text.
            EmptyDocumentError: if the file has no meaningful content.

        Return:
            Document object 
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
            document_format=self.FORMAT_TXT,
            source_path=file_path,
            document_date=document_date,
        )

    # ----------------------------------------------------------------------
    # Override methods
    # ----------------------------------------------------------------------

    def _extract_date(self, content: str) -> date:
        """
        Search in the text the first date recognizable (yyyy-mm-dd or dd/mm/yyyy).
        If it doesn't find anything, it falls back to the default behavior of the base class.
        """

        found_date = self._search_date_in_text(content)
        if found_date:
            return found_date

        return super()._extract_date(content)

    def _extract_title(self, content: str, file_path: str) -> str:
        """
        Uses the first non-empty line as title.
        If no line is found, falls back to the default behavior.
        """

        for line in content.splitlines():
            stripped_line = line.strip()
            if stripped_line:
                return stripped_line

        return super()._extract_title(content, file_path)
