import os

from knowledge_base.index_builder import build_index
from knowledge_base.index_reader import IndexReader

def print_list(list_to_print, title):
    print(f"\n{title}:\n", "\n".join(str(doc) for doc in list_to_print), sep="")

if __name__ == "__main__":

    documents_dir = input("Il programma in automatico parserà i documenti nella cartella /documents, vuoi inserire un percorso custom? (y/n)")
    if documents_dir == "y":
        documents_dir = input("Inserisci il percorso della cartella contenente i documenti")
    else:
        documents_dir = os.path.join(os.path.dirname(__file__), "documents")

    # Percorso per il json di output
    output_path = os.path.join(os.path.dirname(__file__), "index_output.json")

    # Creo il json indice
    build_index(documents_dir, output_path)

    # Leggo il json e ricavo la lista di oggetti Document
    index_reader = IndexReader(output_path)
    documents = index_reader.read()

    print("L'indice \"index_output.json\" è stato creato correttamente, come vuoi procedere?")

    while True:
        choice = input("\n1 - Visualizza la lista di documenti \n2 - Filtra per parola chiave \n3 - Filtra per tipologia di documento \n4 - Estrai il numero di documenti per tipo di formato \n5 - Il documento più lungo \n0 - Esci\n")
        if choice == "0":
            break
        elif choice == "1":
            print_list(documents, "Lista di documenti")
        elif choice == "2":
            query = input("Inserisci la parola chiave")
            filtered_list = index_reader.filter(query)
            print_list(filtered_list, "Lista filtrata (query = " + query + ")")
        elif choice == "3":
            format = input("Inserisci il tipo di formato (txt, csv, md)")
            filtered_by_format = index_reader.filter_by_format(format)
            print_list(filtered_by_format, "Lista filtrata (format = " + format + ")")
        elif choice == "4":
            dict_docs_format = {}
            for doc in documents:
                format = doc.format
                if format in dict_docs_format:
                    dict_docs_format[format] += 1
                else:
                    dict_docs_format[format] = 1
            print("\nNumero di documenti per tipo di formato:", dict_docs_format)
        elif choice == "5":
            max_words = 0
            for doc in documents:
                words_count = doc.word_count
                if words_count > max_words:
                    max_words = words_count
                    longest_doc = doc
            print(f"\nIl documento più lungo è - {longest_doc.title} - con {max_words} parole")
