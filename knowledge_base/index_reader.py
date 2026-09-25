import json

from .document import Document


class IndexReader:
    """
    A class for reading and filtering the knowledge base index
    """

    def __init__(self, index_path: str):
        self._index_path = index_path

    def read(self) -> list[Document]:
        """
        Returns the list of Document objects stored in the index file.

        Raises:
            TypeError: if the index file contains something that is not a valid Document.
        """

        with open(self._index_path, "r") as f:
            raw_documents = json.load(f)

        documents = []
        for raw_document in raw_documents:
            doc = Document.from_json(raw_document)

            if not isinstance(doc, Document):
                raise TypeError(f"Elemento non valido nell'indice: trovato {type(doc)}")

            documents.append(doc)

        return documents

    def filter(self, query: str) -> list[Document]:
        """
        Returns the Document objects whose content, title or short_content contains query.
        Search the query text in the title, in the content and in the short_content.

        Args:
            query: the string to search in the document list
        """

        documents = self.read()

        matching_documents = []
        for doc in documents:
            # Normalizzo le stringhe per confronti case-insensitive
            query_lower = query.lower()
            content = doc.content.lower()
            title = doc.title.lower()
            short_content = doc.short_content.lower()

            if query_lower in content or query_lower in title or query_lower in short_content:
                matching_documents.append(doc)

        return matching_documents

    def filter_by_format(self, format: str) -> list[Document]:
        """
        Returns the Document objects whose format matches the given format.
        
        Args:
            format: the format to filter by
        """
        documents = self.read()
        return [doc for doc in documents if doc.format == format]