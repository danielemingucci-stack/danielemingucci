# Free Linkable Profile

Un profilo professionale, come quelli che conosci, ma sul tuo sito. Si presenta bene alle
persone, si fa trovare dai motori di ricerca e riconosce gli altri profili dello stesso tipo:
se due persone si collegano a vicenda, le due pagine se ne accorgono da sole. Senza
piattaforma in mezzo.

Versione 0.1.

## Cosa c'è nel kit

| File | A cosa serve |
| --- | --- |
| `profile.json` | I tuoi dati. È l'unico file che compili. |
| `build.py` | Genera `index.html` da `profile.json`. |
| `flp.css` | Lo stile. Colori e caratteri si scelgono in `profile.json`. |
| `flp.js` | Fa riconoscere tra loro i profili collegati. |
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

## Licenza

Il codice è distribuito con licenza MIT (vedi `LICENSE`): si può usare, modificare e
ridistribuire liberamente.

---

**English, in short.** A LinkedIn-style professional profile that lives on your own website.
Fill in `profile.json` (JSON Resume + an `flp` block), run `python3 build.py`, upload the four
files to a folder on your site. Profiles that list each other recognise the mutual connection
by reading each other's `profile.json`: no platform in between. Set `"lang": "en"` in `flp`
for English labels. See `SPEC.md`.
