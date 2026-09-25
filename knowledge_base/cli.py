import os

from .index_builder import build_index
from .index_reader import IndexReader


def print_list(list_to_print, title):
    """
    Prints a title followed by a list of Document
    """
    print(f"\n{title}:\n", "\n".join(str(doc) for doc in list_to_print), sep="")


def main(documents_dir: str = None, output_path: str = "index_output.json"):
    """
    Builds the index from documents_dir, then opens the interactive menu.
    If documents_dir is not provided, it is asked to the user.
    """
    if documents_dir is None:
        documents_dir = input("Inserisci il percorso della cartella contenente i documenti: ")

    # Creo il json indice
    build_index(documents_dir, output_path)

    # Leggo il json e ricavo la lista di oggetti Document
    index_reader = IndexReader(output_path)
    documents = index_reader.read()

    print(f'L\'indice "{output_path}" è stato creato correttamente, come vuoi procedere?')

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
            format_choice = input("Inserisci il tipo di formato (txt, csv, md)")
            filtered_by_format = index_reader.filter_by_format(format_choice)
            print_list(filtered_by_format, "Lista filtrata (format = " + format_choice + ")")
        elif choice == "4":
            print("\nNumero di documenti per tipo di formato:", index_reader.count_by_format())
        elif choice == "5":
            longest_doc = index_reader.get_longest_document()
            print(f"\nIl documento più lungo è - {longest_doc.title} - con {longest_doc.word_count} parole")


if __name__ == "__main__":
    main()
