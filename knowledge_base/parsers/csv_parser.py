import csv

from ..document import Document
from ..exceptions import DocumentParsingError, EmptyDocumentError
from .parser import Parser


class CsvParser(Parser):
    """
    Parses plain .csv files into Document objects.
    """

    FORMAT_CSV = "csv"

    def __init__(self):
        super().__init__()

    def parse(self, file_path: str) -> Document:
        """
        Reads a .csv file and returns the corresponding Document object.

        Raises:
            DocumentParsingError: if the file cannot be read or decoded as text.
            EmptyDocumentError: if the file has no meaningful content.
        """

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            # Normalizzo le righe del CSV in un unico testo, così il contenuto
            # ha lo stesso tipo (str) di quello prodotto dagli altri parser, ed
            # è utilizzabile per conteggio parole e ricerca per parola chiave.
            content = ", ".join(str(row) for row in rows)
            
            if not content.strip():
                raise EmptyDocumentError(f"Il file '{file_path}' e' vuoto.")

            # CsvParser non fa override: usa i fallback della classe base
            # (titolo dal nome del file, nessuna data individuabile).
            title = self._extract_title(content, file_path)
            document_date = self._extract_date(content)

        except OSError as error:
            raise DocumentParsingError(f"Impossibile leggere il file '{file_path}': {error}") from error
        except UnicodeDecodeError as error:
            raise DocumentParsingError(f"Contenuto non decodificabile in '{file_path}': {error}") from error
   
      
        return Document(
            title=title,
            content=content,
            document_format=self.FORMAT_CSV,
            source_path=file_path,
            document_date=document_date
        )