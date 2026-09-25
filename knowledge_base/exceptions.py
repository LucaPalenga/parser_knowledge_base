class DocumentParsingError(Exception):
    """
    Raised when a document's content cannot be read or decoded correctly.
    """


class EmptyDocumentError(DocumentParsingError):
    """
    Raised when a document has no content.
    """


class UnsupportedFormatError(DocumentParsingError):
    """
    Raised when a file extension has no registered parser.
    """
