from datetime import date

SHORT_CONTENT_LENGTH = 200


class Document:
    """
    Represents a single document normalized into a common structure
    """

    # ----------------------------------------------------------------------
    # PROPERTIES
    # ----------------------------------------------------------------------
    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def short_content(self) -> str:
        return self._short_content

    @property
    def date(self) -> date:
        return self._date

    @property
    def format(self) -> str:
        return self._format

    @property
    def source_path(self) -> str:
        return self._source_path

    @property
    def word_count(self) -> int:
        return self._word_count
        
    def __init__(
        self,
        title: str,
        content: str,
        document_format: str,
        source_path: str,
        document_date: date = None,
        short_content: str = None,
    ):
        """
        Initialize a Document object.

        Args:
            title (str): The title of the document.
            content (str): The normalized full content of the document.
            document_format (str): The original format of the document (e.g. "txt", "md", "csv").
            source_path (str): Path of the source file the document was parsed from.
            document_date (date): The date associated with the document, if present.
            short_content (str): A short excerpt of the document. If not provided,
                it is derived automatically from the content.
        """

        self._title = title
        self._content = content
        self._format = document_format
        self._source_path = source_path
        self._date = document_date
        self._word_count = len(content.split())
        self._short_content = short_content or self._build_excerpt(content)

    def _build_excerpt(self, content: str, length: int = SHORT_CONTENT_LENGTH) -> str:
        """
        Builds a short excerpt of the content, truncated on a word boundary.
        """

        content = content.strip()
        if len(content) <= length:
            return content
        return content[:length].rsplit(" ", 1)[0] + "..."

    # ----------------------------------------------------------------------
    # Serialization/Deserialization
    # ----------------------------------------------------------------------

    def to_json(self) -> dict:
        """
        Returns a JSON representation of the Document object.
        """

        return {
            "title": self._title,
            "short_content": self._short_content,
            "date": self._date.isoformat() if self._date else None,
            "content": self._content,
            "format": self._format,
            "source_path": self._source_path,
            "word_count": self._word_count,
        }

    def from_json(data: dict):
        """
        Returns a Document from a JSON.
        """

        document_date = None
        if data["date"] is not None:
            document_date = date.fromisoformat(data["date"])

        return Document(
            title=data["title"],
            content=data["content"],
            document_format=data["format"],
            source_path=data["source_path"],
            document_date=document_date,
            short_content=data["short_content"],
        )
    
    def __repr__(self) -> str:
        return f"Document - {self._title}, {self._format}"
