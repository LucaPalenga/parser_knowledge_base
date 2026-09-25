import csv

from .parser import Parser


class CsvParser(Parser):
    """
    Parses plain .csv files into Document objects.
    """

    FORMAT_CSV = "csv"

    def __init__(self, file_path: str):
        super().__init__(file_path)

    # ----------------------------------------------------------------------
    # Override methods
    # ----------------------------------------------------------------------

    def _get_format(self) -> str:
        return self.FORMAT_CSV

    def _get_content(self) -> str:
        """
        Returns the content of the csv file.
        """
        with open(self._file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
        content = ", ".join(str(row) for row in rows)
        
        return content
