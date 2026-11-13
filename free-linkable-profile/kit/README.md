# Free Linkable Profile

Un profilo professionale, come quelli che conosci, ma sul tuo sito. Si presenta bene alle
persone, si fa trovare dai motori di ricerca e riconosce gli altri profili dello stesso tipo:
se due persone si collegano a vicenda, le due pagine se ne accorgono da sole. Senza
piattaforma in mezzo.

Versione 0.2.

## Cosa c'è nel kit

| File | A cosa serve |
| --- | --- |
| `profile.json` | I tuoi dati. È l'unico file che compili. |
| `build.py` | Genera le pagine: il tuo profilo, una vetrina, i profili ospitati. |
| `flp.css` | Lo stile. Colori e caratteri si scelgono in `profile.json`. |
| `flp.js` | Fa riconoscere tra loro i profili collegati, segue i traslochi, disegna le vetrine. |
| `PROMPT.md` | Il prompt da dare a un assistente AI perché faccia tutto con te. |
| `SPEC.md` | Le regole del formato, per chi vuole capirle o reimplementarle. |

## Installarlo

**Con un assistente AI (consigliato).** Apri `PROMPT.md`, copia il testo e dallo al tuo
assistente insieme a questa cartella e al tuo curriculum. Ti fa le domande, compila i dati,
genera la pagina e ti dice come caricarla sul tuo sito.

**A mano.**

1. Compila `profile.json`.
2. Esegui `python3 build.py`: crea `index.html`.
3. Carica `index.html`, `profile.json`, `flp.css` e `flp.js` in una cartella del tuo sito,
   per esempio `/profilo/`.

Per aggiornare il profilo: modifica `profile.json`, riesegui `build.py`, ricarica i file.

## Collegarsi

In `profile.json`, dentro `flp.connections`, aggiungi nome e indirizzo del profilo di chi
conosci. Quando anche l'altra persona aggiunge il tuo, sulle due pagine compare
"Collegamento reciproco".

## Lo stesso profilo su un altro sito (vetrina)

Il profilo ha una casa sola, ma puoi mostrarlo anche altrove, per esempio sul sito della
tua azienda. Sul secondo sito:

```
python3 build.py --vetrina https://www.miosito.it/profilo/
```

Crea la cartella `vetrina` con `index.html`, `flp.css` e `flp.js`: caricala sul secondo
sito. La pagina legge i dati dall'originale a ogni visita, quindi si aggiorna da sola, e
dichiara l'originale ai motori di ricerca. I colori sono quelli del `profile.json` che sta
accanto a `build.py`, se c'è.

## Ospitare chi non ha un sito

Prepara una cartella con una sottocartella per persona, ognuna con il suo `profile.json`
(in `flp.url` va l'indirizzo che avrà sul tuo sito):

```
profili/anna-bianchi/profile.json
profili/luca-verdi/profile.json
```

Poi:

```
python3 build.py --ospiti profili
```

Genera la pagina di ognuno e l'elenco delle persone ospitate. Carica tutta la cartella.
Titolo e testo dell'elenco si scelgono in un file `profili/ospiti.json`:
`{"title": "Le nostre persone", "intro": "…", "url": "https://www.miosito.it/profili/"}`.

## Cambiare indirizzo (trasloco)

1. Nel profilo nuovo aggiungi `"previous": ["https://vecchio-indirizzo/"]` dentro `flp`.
2. Al vecchio indirizzo lascia un `profile.json` con `"movedTo": "https://nuovo-indirizzo/"`
   dentro `flp`, e riesegui `build.py`: la pagina diventa un avviso che porta al nuovo.

Chi era collegato a te resta collegato, senza fare niente: ogni volta che qualcuno esegue
`build.py`, il programma controlla i suoi collegamenti e, se uno si è trasferito, aggiorna
da solo l'indirizzo nel suo `profile.json`. Il trasloco è accettato solo se confermato sia
dal vecchio indirizzo sia dal nuovo. Lascia l'avviso al vecchio indirizzo per almeno un anno.

Non serve avvisare nessuno, e non fidarti di messaggi che ti chiedono di cambiare un
indirizzo a mano. Per generare la pagina senza rete: `python3 build.py --senza-rete`.

## Licenza

Il codice è distribuito con licenza MIT (vedi `LICENSE`): si può usare, modificare e
ridistribuire liberamente.

---

**English, in short.** A LinkedIn-style professional profile that lives on your own website.
Fill in `profile.json` (JSON Resume + an `flp` block), run `python3 build.py`, upload the four
files to a folder on your site. `build.py --vetrina URL` makes a showcase page of a profile
hosted elsewhere; `build.py --ospiti FOLDER` builds many hosted profiles plus a directory;
`flp.movedTo` / `flp.previous` handle a change of address. Profiles that list each other recognise the mutual connection
by reading each other's `profile.json`: no platform in between. Set `"lang": "en"` in `flp`
for English labels. See `SPEC.md`.
