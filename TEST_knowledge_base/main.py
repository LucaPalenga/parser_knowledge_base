import os

from knowledge_base.index_builder import build_index
from knowledge_base.index_reader import IndexReader

if __name__ == "__main__":
    # Percorso della cartella "documents" 
    documents_dir = os.path.join(os.path.dirname(__file__), "documents")

    # Percorso per il json di output
    output_path = os.path.join(os.path.dirname(__file__), "index_output.json")

    # Creo il json indice
    build_index(documents_dir, output_path)

    # Leggo il json e ricavo la lista di oggetti Document
    index_reader = IndexReader(output_path)
    documents = index_reader.read()

    # Esempio di lista filtrata per query
    filtered_list = index_reader.filter("policy")
    print("\nLista filtrata (query = policy):", filtered_list)
    
    # Esempio di lista filtrata per tipo di formato
    filtered_by_format = index_reader.filter_by_format("txt")
    print("\nLista filtrata (format = txt):", filtered_by_format)
