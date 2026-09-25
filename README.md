# knowledge_base

Programma Python che, data una cartella di documenti in formati diversi (`.txt`, `.md`, `.csv`),
ne estrae contenuto e metadati, li normalizza in una rappresentazione comune (`Document`) e
costruisce un indice della knowledge base salvabile e ricaricabile in formato JSON.

## Struttura del progetto

```
python_exercises/
  knowledge_base/              <- il package
    document.py                  Modello del singolo documento normalizzato
    exceptions.py                Eccezioni custom per la gestione degli errori
    index_reader.py              Permette ricerche/filtri
    index_builder.py             Crea l'indice dei documenti
    parsers/
      parser.py                  Classe base astratta dei parser
      txt_parser.py              Parser per file .txt
      md_parser.py               Parser per file .md
      csv_parser.py              Parser per file .csv
      extensions.py              Estensioni supportate
    requirements.txt             

  TEST_knowledge_base/          <- test
    documents/                   15 documenti di esempio
    main.py                      Script di esempio
```

`knowledge_base` è un package riusabile, li riceve in input il percorso ai documenti di interesse (in questo caso `TEST_knowledge_base`).

## Come testarlo

Va lanciato come modulo (`-m`), dalla cartella `python_exercises/` (quella che
contiene sia `knowledge_base/` sia `TEST_knowledge_base/`), non con `python3 main.py` direttamente:

```bash
cd python_exercises
python3 -m TEST_knowledge_base.main
```

Questo:
1. Elabora tutti i file dentro `TEST_knowledge_base/documents/`
2. Stampa un riepilogo finale (documenti elaborati / scartati).
3. Salva l'indice in `TEST_knowledge_base/index_output.json`.
4. Poi fa qualche esempio di filtraggio su testo e formato.

## Archivio di prova

`TEST_knowledge_base/documents/` contiene 15 documenti fittizi ma verosimili (policy aziendali,
verbali, procedure, inventari, anagrafiche...) nei tre formati supportati, più 4 casi limite
pensati apposta per mettere alla prova il parser:

- `10_vuoto.txt` — file vuoto
- `11_caratteri_strani.txt` — emoji, accenti, lingue miste, simboli
- `12_file_corrotto.txt` — byte non validi in UTF-8
- `13_report_annuale_lunghissimo.md` — documento molto esteso (~2700 parole)
- `14_presentazione_prodotto.pptx` — estensione non gestita

Tutti questi casi vengono segnalati e saltati durante l'elaborazione, senza interrompere il parsing degli altri file.
