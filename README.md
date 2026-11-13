# danielemingucci.com

## Scrivere: l'editor

Vai su **danielemingucci.com/scrivi/** ed entra con il tuo token GitHub (vedi sotto).
- **Scritti**: "New Scritto", titolo, testo, immagine se vuoi, poi **Save**. Dopo un paio di minuti è online.
- **Archivio Tumblr**: i post importati, per correggere titoli e testi. Non toccare le righe `{% raw %}` e `{% endraw %}`.
- **Curriculum**: tutte le sezioni come su LinkedIn, da riempire una voce alla volta. Online su danielemingucci.com/curriculum/

### Il token (una volta sola)
GitHub › Settings › Developer settings › Personal access tokens › Fine-grained tokens › Generate new token.
Repository access: solo `danielemingucci`. Permissions › Contents: Read and write. Copialo e incollalo nell'editor.

## Collegamenti, in automatico
Una volta al giorno GitHub controlla i collegamenti del profilo: se una persona ha cambiato indirizzo
(e il trasloco è confermato dal vecchio e dal nuovo indirizzo) lo aggiorna da solo nel curriculum.
Per farlo subito: Actions › "Collegamenti → aggiornati" › Run workflow.

## Tumblr → sito, in automatico
Due volte al giorno GitHub controlla dacco1971.tumblr.com e porta sul sito i post nuovi (solo i tuoi, non i reblog).
Per farlo subito: Actions › "Tumblr → sito" › Run workflow.

## Come aggiungere uno scritto

1. Apri la cartella `_posts` e scegli **Add file › Create new file**.
2. Nome del file: `ANNO-MESE-GIORNO-titolo.md`, per esempio `2026-11-09-lavoro-opera-azione.md`.
   La data nel nome è la data di pubblicazione.
3. Scrivi in cima queste righe, poi il testo sotto:

```
---
title: "Lavoro, opera, azione"
immagine: /img/scritti/lavoro-opera-azione.jpg
tumblr: https://dacco1971.tumblr.com/post/...
---

Il testo, un paragrafo per riga vuota.

> Una citazione si scrive così.

Il *corsivo* tra asterischi, il **grassetto** tra due asterischi.
```

`immagine` e `tumblr` sono facoltativi: se non servono, togli la riga.
Le immagini vanno nella cartella `img/scritti`.

4. **Commit changes.** Dopo un paio di minuti lo scritto è online in
   `danielemingucci.com/scritti/titolo/`, ed entra da solo nell'elenco degli scritti,
   nella pagina Aria e, se è il più recente, sulla soglia.

## Il sito in inglese
Tutto ciò che è in italiano ha una versione inglese sotto `/en/` (in alto, dopo "Profilo", c'è **EN** / **IT**).

- **Home e cinque mondi**: le pagine in `en/` si rigenerano da quelle italiane con `python3 scripts/en_pages.py`
  (le traduzioni dei testi sono dentro lo script; se manca una frase, lo script si ferma e dice quale).
- **Testi dell'interfaccia** (menu, pulsanti, etichette): `_data/t.yml`, nelle due lingue.
- **Curriculum in inglese**: `_data/cv_en.yml`, dall'editor alla voce "Curriculum (English)".
- **Scritti e taccuino**: le traduzioni stanno in `_en/`, un file per ogni post di `_posts/`, con lo stesso nome.
  `python3 scripts/en_posts.py stato` dice quanti post non hanno ancora la traduzione (per esempio quelli nuovi arrivati
  da Tumblr o scritti dall'editor); `da-tradurre` li elenca e `applica` scrive le traduzioni.
  Un post senza traduzione compare solo in italiano: dalla sua pagina, EN porta all'elenco inglese.
- Poesie e canzoni di altri autori, e alcune citazioni lunghe, nella versione inglese restano in originale.

