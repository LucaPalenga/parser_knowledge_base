import os

from ..exceptions import UnsupportedFormatError
from .csv_parser import CsvParser
from .md_parser import MarkdownParser
from .txt_parser import TxtParser
from .parser import Parser

# Mappa che collega ogni estensione alla classe parser corretta.
# NB: il valore è di tipo classe, l'istanza viene generata dal metodo get_parser_for
SUPPORTED_EXTENSIONS = {
    ".txt": TxtParser,
    ".csv": CsvParser,
    ".md": MarkdownParser,
}


def get_parser_for(file_path: str) -> Parser:
    """
    Check if the extension is supported and returns the correct parser
    instance, already configured with file_path.

    Raises:
        UnsupportedFormatError: if extension is not supported
    """

    _, extension = os.path.splitext(file_path)  # Returns a tuple (path, ext)
    parser_class = SUPPORTED_EXTENSIONS.get(extension.lower())

    if parser_class is None:
        raise UnsupportedFormatError(f"Estensione non supportata: '{extension}'")

    return parser_class(file_path)
