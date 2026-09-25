# knowledge_base

Programma Python che, data una cartella di documenti in formati diversi (`.txt`, `.md`, `.csv`),
ne estrae contenuto e metadati, li normalizza in una rappresentazione comune (`Document`) e
costruisce un indice della knowledge base salvabile e ricaricabile in formato JSON.

## Struttura del progetto

```
knowledge_base/               <- il package
  document.py                   Modello del singolo documento normalizzato
  exceptions.py                 Eccezioni custom per la gestione degli errori
  index_builder.py              Crea l'indice dei documenti
  index_reader.py               Ricarica l'indice, ricerche, filtri e statistiche
  cli.py                        Interfaccia da riga di comando
  parsers/
    parser.py                   Classe base dei parser
    txt_parser.py               Parser per file .txt
    md_parser.py                Parser per file .md
    csv_parser.py               Parser per file .csv
    registry.py                 Mappa estensione -> classe parser

example/                      <- demo con archivio di prova
  documents/                    15 documenti di esempio (inclusi i casi limite)
  main.py                       Entry point della demo
```

`knowledge_base` è un package riusabile: riceve in input il percorso a una cartella qualsiasi
di documenti; `example/` è una demo che lo usa sull'archivio di prova.

## Installazione

In un ambiente virtuale:

```bash
python3 -m venv venv
source venv/bin/activate       
pip install git+https://github.com/LucaPalenga/parser_knowledge_base.git
```

## Esecuzione

Dopo aver clonato la repository (necessario per avere `example/` e l'archivio di prova,
che non fanno parte del package installato):

```bash
git clone https://github.com/LucaPalenga/parser_knowledge_base.git
cd parser_knowledge_base
python3 example/main.py
```

Questo:
1. Elabora tutti i file dentro `example/documents/`
2. Stampa un riepilogo finale (documenti elaborati / scartati, con motivazioni)
3. Salva l'indice in `example/index_output.json`
4. Apre un menu interattivo per elencare, cercare, filtrare i documenti e vedere le statistiche

In alternativa, il package espone direttamente la propria CLI, utilizzabile su una cartella
qualsiasi:

```bash
python3 -m knowledge_base.cli
```

## Archivio di prova

`example/documents/` contiene 15 documenti fittizi ma verosimili (policy aziendali,
verbali, procedure, inventari, anagrafiche...) nei tre formati supportati, più alcuni casi
limite pensati apposta per mettere alla prova il parser:

- `10_vuoto.txt` — file vuoto
- `11_caratteri_strani.txt` — emoji, accenti, lingue miste, simboli
- `12_file_corrotto.txt` — byte non validi in UTF-8
- `13_report_annuale_lunghissimo.md` — documento molto esteso (~2700 parole)
- `14_presentazione_prodotto.pptx` — estensione non gestita

I file problematici vengono segnalati e saltati durante l'elaborazione, senza interrompere
il parsing degli altri file.
