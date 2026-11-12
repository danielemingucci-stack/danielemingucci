# Prompt di installazione

Copia tutto il testo qui sotto e incollalo al tuo assistente AI (Claude, ChatGPT, Gemini…), insieme alla cartella del kit e a quello che hai per raccontarti: un curriculum, il PDF del profilo LinkedIn, o anche solo due righe scritte da te.

---

Voglio pubblicare sul mio sito un profilo professionale con il kit **Free Linkable Profile**, che ti allego. Il kit contiene:

- `profile.json`: i miei dati, nel formato JSON Resume più un blocco `flp`;
- `build.py`: genera `index.html` da `profile.json` (Python 3, nessuna libreria);
- `flp.css` e `flp.js`: stile e riconoscimento reciproco tra profili;
- `SPEC.md`: le regole del formato.

Fai queste cose, nell'ordine:

1. **Chiedimi i dati che mancano**, una sezione alla volta: nome, titolo in una riga, città, email di contatto, due o tre frasi di presentazione, esperienze (ruolo, azienda, inizio, fine), formazione, competenze, lingue, e quello che ho tra pubblicazioni, brevetti, progetti, certificazioni, premi, volontariato. Se ti ho allegato un curriculum o un PDF, prendi i dati da lì e chiedimi solo conferma. **Non inventare niente**: quello che non so o non ti dico resta vuoto.
2. **Chiedimi l'indirizzo** dove vivrà il profilo sul mio sito (per esempio `https://www.miosito.it/profilo/`) e mettilo in `flp.url`. Chiedimi anche, se li ho: l'indirizzo di una mia foto, di un'immagine di copertina, del feed dei miei articoli (`flp.feed`) e della pagina per iscriversi alla mia newsletter (`flp.follow`).
3. **Adatta i colori e i caratteri** in `flp.theme` a quelli del mio sito: chiedimeli, oppure leggili dal sito se te lo indico.
4. **Chiedimi i collegamenti**: persone che conosco e che hanno a loro volta un profilo di questo tipo. Per ognuna servono nome e indirizzo del suo profilo, da mettere in `flp.connections`.
5. **Compila `profile.json`**, controlla che sia JSON valido, poi esegui `python3 build.py` e mostrami il risultato.
6. **Dimmi come caricarlo** sul mio sito: i quattro file `index.html`, `profile.json`, `flp.css`, `flp.js` vanno nella stessa cartella, all'indirizzo scelto al punto 2. Chiedimi su cosa è fatto il mio sito (WordPress, GitHub Pages, Netlify, un hosting con FTP…) e dammi i passi esatti per quel caso.
7. **Controlla l'ultima cosa**: perché gli altri profili possano riconoscere il mio, `profile.json` deve essere leggibile da altri siti (intestazione `Access-Control-Allow-Origin: *`). Dimmi se il mio hosting lo fa già o come attivarlo.

Regole: il profilo è mio e resta sul mio sito. Non aggiungere servizi esterni, tracciamenti o script oltre a quelli del kit. Quando in futuro ti chiederò di aggiornare il profilo, modifica solo `profile.json` e rigenera `index.html`.
