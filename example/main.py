import os

from knowledge_base.cli import main

if __name__ == "__main__":

    documents_dir = input("Il programma in automatico parserà i documenti nella cartella /documents, vuoi inserire un percorso custom? (y/n)")
    if documents_dir == "y":
        documents_dir = input("Inserisci il percorso della cartella contenente i documenti")
    else:
        documents_dir = os.path.join(os.path.dirname(__file__), "documents")

    # Percorso per il json di output
    output_path = os.path.join(os.path.dirname(__file__), "index_output.json")

    main(documents_dir, output_path)
