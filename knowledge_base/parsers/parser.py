import os
from datetime import date, datetime

from ..document import Document

# Formati di data riconosciuti in un testo libero
DATE_PATTERNS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
)


class Parser:
    """
    Base class for all format-specific document parsers.
    """

    def __init__(self):
        pass

    def parse(self, file_path: str) -> Document:
        """
        Gets a path file and returns a Document object.
        """

        raise NotImplementedError("Subclasses must implement this method")

    def _extract_date(self, content: str) -> date:
        """
        Returns the date found in the content, or None if no date is found.
        Must be implemented properly by subclasses.
        """
        return None

    def _extract_title(self, content: str, file_path: str) -> str:
        """
        Returns the file title user friendly.
        Must be implemented if necessary by subclasses.

        Args:
            content (str): The content of the document.
            file_path (str): The path of the file.

        Returns:
            str: The title of the document.
        """

        file_name, _ = os.path.splitext(os.path.basename(file_path))
        return file_name.replace("_", " ")


    @staticmethod
    def _search_date_in_text(text: str) -> date:
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
