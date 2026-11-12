# danielemingucci.com

## Scrivere: l'editor

Vai su **danielemingucci.com/scrivi/** ed entra con il tuo token GitHub (vedi sotto).
- **Scritti**: "New Scritto", titolo, testo, immagine se vuoi, poi **Save**. Dopo un paio di minuti è online.
- **Archivio Tumblr**: i post importati, per correggere titoli e testi. Non toccare le righe `{% raw %}` e `{% endraw %}`.
- **Curriculum**: tutte le sezioni come su LinkedIn, da riempire una voce alla volta. Online su danielemingucci.com/curriculum/

### Il token (una volta sola)
GitHub › Settings › Developer settings › Personal access tokens › Fine-grained tokens › Generate new token.
Repository access: solo `danielemingucci`. Permissions › Contents: Read and write. Copialo e incollalo nell'editor.

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
