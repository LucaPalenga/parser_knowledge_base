import os

from ..exceptions import UnsupportedFormatError
from .csv_parser import CsvParser
from .md_parser import MarkdownParser
from .txt_parser import TxtParser
from .parser import Parser

# Registro che collega ogni estensione al parser che sa gestirla.
# Per supportare un nuovo formato basta creare la classe parser, importarla qui
# sopra e aggiungere una riga al dizionario: nessun altro file va toccato.
PARSERS_BY_EXTENSION = {
    ".txt": TxtParser(),
    ".csv": CsvParser(),
    ".md": MarkdownParser(),
}


def get_parser_for(file_path: str) -> Parser:
    """
    Check if the extension is supported and returns the correct parser

    Raises:
        UnsupportedFormatError: if extension is not supported
    """

    _, extension = os.path.splitext(file_path)  # Returns a tuple (path, ext)
    parser = PARSERS_BY_EXTENSION.get(extension.lower())

    if parser is None:
        raise UnsupportedFormatError(f"Estensione non supportata: '{extension}'")

    return parser
