import os
from datetime import date, datetime

from ..document import Document
from ..exceptions import DocumentParsingError, EmptyDocumentError


# Formati di data riconosciuti in un testo libero
DATE_PATTERNS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
)


class Parser:
    """
    Base class for all format-specific document parsers.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path

    def parse(self) -> Document:
        """
        Gets a path file and returns a Document object.
        """
        try:
            content = self._get_content()

        except OSError as error:
            raise DocumentParsingError(f"Impossibile leggere il file '{self._file_path}': {error}") from error
        except UnicodeDecodeError as error:
            raise DocumentParsingError(f"Contenuto non decodificabile in '{self._file_path}': {error}") from error

        content = content.strip()
        
        if not content:
            raise EmptyDocumentError(f"Il file '{self._file_path}' e' vuoto.")
        

        title = self._extract_title(content)
        document_date = self._extract_date(content)

        return Document(
            title=title,
            content=content,
            document_format=self._get_format(),
            source_path=self._file_path,
            document_date=document_date,
        )
        
    # ----------------------------------------------------------------------
    # Getters
    # ----------------------------------------------------------------------

    def _get_format(self) -> str:
        """
        Returns the document format.
        """
        return None

    def _get_content(self) -> str:
        """
        Returns the content of the file.
        This is a common behavior, can be overridden by subclasses if needed.
        """
        with open(self._file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        return content


    def _extract_date(self, content: str) -> date:
        """
        Returns the date found in the content, or None if no date is found.
        Must be implemented properly by subclasses.
        """
        return None

    def _extract_title(self, content: str) -> str:
        """
        Returns the file title user friendly.
        Must be implemented if necessary by subclasses.

        Args:
            content (str): The content of the document.

        Returns:
            str: The title of the document.
        """

        file_name, _ = os.path.splitext(os.path.basename(self._file_path))
        return file_name.replace("_", " ")


    def _search_date_in_text(self, text: str) -> date:
        """
        Search in the text the first date recognizable (yyyy-mm-dd or dd/mm/yyyy).
        """

        for word in text.split():
            for date_format in DATE_PATTERNS:
                try:
                    return datetime.strptime(word, date_format).date()
                except ValueError:
                    continue

        return None
