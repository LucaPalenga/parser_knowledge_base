import json
import os

from knowledge_base.document import Document
from knowledge_base.exceptions import DocumentParsingError
from knowledge_base.parsers.registry import get_parser_for


def build_index(documents_dir: str, output_path: str = None):
    """
    Process all documents from documents_dir and save the index output file into output_path.

    Args:
        documents_dir: path to documents
        output_path: path to output file

    Returns:
        The list of Document objects that were successfully processed.
    """

    file_names = os.listdir(documents_dir)

    # Definisco esplicitamente il tipo di oggetti che avrà la lista
    # in questo modo mi è più facile accedere ai metodi dell'oggetto Document
    documents: list[Document] = []

    processed_count = 0
    skipped_count = 0

    for file_name in file_names:
        file_path = os.path.join(documents_dir, file_name)

        try:
            parser = get_parser_for(file_path)

            document = parser.parse()
            documents.append(document)

        except DocumentParsingError as error:
            print(f"[SALTATO] {file_name}: {error}")
            skipped_count += 1
            continue

        processed_count += 1
        print(f"[OK] {file_name} -> {document.title}")

    print()
    print(f"Documenti elaborati: {processed_count}")
    print(f"Documenti saltati: {skipped_count}")

    if output_path:
        with open(output_path, "w") as fout:
            json.dump([doc.to_json() for doc in documents], fout, indent=2)

    return documents
