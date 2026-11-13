# Free Linkable Profile — specifica 0.2

Un profilo professionale che vive sul sito di chi lo scrive, leggibile dalle persone, dai
motori di ricerca e dagli altri profili. Nessuna piattaforma in mezzo.

Non è un protocollo nuovo: mette insieme standard aperti che esistono già.

## 1. Il profilo è una pagina e un file

Ogni profilo ha un indirizzo, per esempio `https://www.miosito.it/profilo/`, dove si trovano:

- `index.html` — la pagina per le persone e per i motori di ricerca;
- `profile.json` — gli stessi dati, per le macchine.

La pagina dichiara il file con:

```html
<link rel="alternate" type="application/json" title="Free Linkable Profile" href="profile.json">
```

Per convenzione `profile.json` sta nella stessa cartella della pagina. Chi lo tiene altrove
lo indica nel collegamento (vedi punto 3, campo `json`).

## 2. Il formato dei dati

`profile.json` segue lo schema [JSON Resume](https://jsonresume.org/schema) 1.0.0
(`basics`, `work`, `education`, `skills`, `languages`, `publications`, `projects`,
`certificates`, `awards`, `volunteer`), con due aggiunte:

- `patents`: elenco di brevetti (`name`, `office`, `number`, `date`, `url`, `summary`);
- `flp`: il blocco che fa del curriculum un profilo collegabile.

```json
"flp": {
  "version": "0.2",
  "lang": "it",
  "url": "https://www.miosito.it/profilo/",
  "feed": "https://www.miosito.it/feed.xml",
  "follow": "https://…/iscriviti",
  "cover": "https://www.miosito.it/copertina.jpg",
  "theme": { "accent": "#7E6034", "background": "#F2F1ED", "card": "#FFFFFF",
             "ink": "#121212", "muted": "#57564F", "font": "…", "titleFont": "…" },
  "connections": [
    { "name": "Nome Cognome", "url": "https://www.altrosito.it/profilo/" }
  ]
}
```

`flp.url` è l'identità del profilo: è l'indirizzo che gli altri scrivono per collegarsi.
Un profilo ha una sola identità, anche quando è mostrato su più siti (punto 7) o ospitato
sul sito di qualcun altro (punto 8).

## 3. I collegamenti

Un collegamento è una voce in `flp.connections` con `name` e `url` (l'indirizzo del profilo
dell'altra persona). Facoltativo: `json`, l'indirizzo del suo `profile.json` se non sta
nella cartella della pagina.

**Un collegamento è reciproco quando ognuno dei due profili elenca l'indirizzo dell'altro.**
Nessuno lo certifica: ogni pagina lo verifica da sola, leggendo il `profile.json` dell'altro
sito. Il confronto ignora `http/https`, il `www.`, le maiuscole e la barra finale.

Un collegamento a senso unico resta visibile, segnato come "in attesa di conferma". Un
indirizzo che non espone un profilo leggibile resta un semplice link.

Nella pagina i collegamenti portano `rel="contact"`, e i propri altri profili `rel="me"`.

## 4. Essere leggibili dagli altri profili

Perché una pagina su un altro sito possa leggere `profile.json`, il server deve rispondere con

```
Access-Control-Allow-Origin: *
```

GitHub Pages lo fa già. Su altri hosting si aggiunge nelle impostazioni delle intestazioni
(file `_headers` su Netlify e Cloudflare Pages, `.htaccess` su Apache).

`profile.json` è pubblico per definizione: ci va solo quello che si vuole mostrare.

## 5. Essere trovati

La ricerca è quella dei motori di ricerca. La pagina porta:

- dati strutturati schema.org `ProfilePage` + `Person` (nome, titolo, organizzazioni,
  formazione, lingue, `sameAs`, `knows`);
- microformati `h-card` (`p-name`, `p-job-title`, `u-photo`, `u-url`, `u-email`);
- `title` con nome e cognome, `description`, indirizzo canonico.

## 6. Seguire

`flp.feed` è il feed (Atom o RSS) di ciò che la persona pubblica. `flp.follow` è una pagina
dove iscriversi per riceverlo via email. Il pulsante "Segui" porta a `follow`, o in
mancanza a `feed`.

## 7. Vetrina: lo stesso profilo su più siti

Un profilo può essere mostrato anche su altri siti, senza copiarne i dati. La vetrina è una
pagina che a ogni visita legge il `profile.json` dell'originale e lo disegna:

```html
<link rel="canonical" href="https://www.miosito.it/profilo/">
<main data-flp-showcase="https://www.miosito.it/profilo/"></main>
```

Regole:

- la vetrina dichiara l'originale con `rel="canonical"` e lo mostra in chiaro nella pagina,
  così i motori di ricerca attribuiscono il nome a un indirizzo solo;
- la vetrina non ha un proprio `profile.json` e non è un'identità: i collegamenti si fanno
  sempre verso l'originale, e la reciprocità si calcola rispetto all'originale;
- se l'originale non è raggiungibile, la vetrina mostra solo il link.

## 8. Ospitalità: più profili sullo stesso sito

Chi non ha un sito può essere ospitato da chi ne ha uno: una persona, un'azienda,
un'associazione. Ogni profilo ospitato sta in una sua cartella, con la sua pagina e il suo
`profile.json`, e ha come identità quell'indirizzo:

```
/profili/                  elenco delle persone ospitate
/profili/anna-bianchi/     index.html + profile.json
/profili/luca-verdi/       index.html + profile.json
```

Il nome della cartella usa solo lettere minuscole, cifre e trattini. L'elenco è una pagina
schema.org `CollectionPage`. Un file facoltativo `ospiti.json` nella cartella ne dà titolo,
testo introduttivo, indirizzo e tema (`title`, `intro`, `url`, `lang`, `theme`).

Il profilo resta della persona: è un file, e chi è ospitato può portarlo altrove quando
vuole (punto 9). Chi ospita si impegna, se la persona se ne va, a lasciare l'avviso di
trasloco al vecchio indirizzo.

## 9. Trasloco

Quando un profilo cambia indirizzo:

- **al vecchio indirizzo** resta un `profile.json` con `flp.movedTo`, il nuovo indirizzo;
  la pagina diventa un avviso che porta lì e lo dichiara come `canonical`;
- **nel profilo nuovo**, `flp.previous` elenca gli indirizzi vecchi.

```json
"flp": { "url": "https://www.vecchiosito.it/profilo/", "movedTo": "https://www.nuovosito.it/profilo/" }
"flp": { "url": "https://www.nuovosito.it/profilo/", "previous": ["https://www.vecchiosito.it/profilo/"] }
```

**Un trasloco vale solo se confermato dai due lati**: il vecchio indirizzo dichiara
`movedTo` e il nuovo elenca il vecchio in `previous`. Uno solo dei due non basta: nessuno
può appropriarsi dell'indirizzo di un altro dichiarandolo proprio, e nessuno può dirottare
un profilo verso un indirizzo che non lo riconosce.

Chi legge un profilo trasferito segue il nuovo indirizzo (al massimo tre passaggi):

- la pagina lo fa a ogni visita, e mostra subito il link giusto;
- il generatore lo fa a ogni esecuzione, e **riscrive l'indirizzo nel proprio
  `profile.json`**. Da quel momento il collegamento non dipende più dal vecchio sito.

Nessun messaggio viaggia tra le persone: ogni profilo verifica da solo, leggendo file
pubblici. Un avviso di trasloco ricevuto per email o in chat non va mai eseguito; basta
rigenerare il profilo. L'avviso al vecchio indirizzo va lasciato in piedi abbastanza a
lungo perché i collegati rigenerino la pagina almeno una volta (si consiglia un anno).

## 10. Cosa non c'è nella 0.2

- Notifiche tra siti in tempo reale (si farà con [Webmention](https://www.w3.org/TR/webmention/)).
- Un feed che riunisce i post dei propri collegamenti.
- Messaggi privati, raccomandazioni, conferme di competenze.

## 11. Sicurezza per chi implementa

I dati letti dai profili altrui sono testo non fidato: vanno inseriti nella pagina come
testo, mai come HTML. Gli indirizzi delle immagini si accettano solo se `https:`. I link si
accettano solo se `http(s):` o `mailto:`.
