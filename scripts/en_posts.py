#!/usr/bin/env python3
"""Traduzioni inglesi degli scritti: da _posts/ a _en/.

  python3 scripts/en_posts.py stato
      Quanti post sono tradotti e quanti mancano.
  python3 scripts/en_posts.py da-tradurre [parole] [scritti|taccuino]
      Stampa i prossimi post senza traduzione (dal più recente), fino a circa N parole, così:
          @@@ 2026-11-09-lavoro-opera-azione
          Titolo
          <p>corpo in HTML…</p>      (i tag molto lunghi compaiono come <#1>, <#2>… e vanno lasciati dove sono)
  python3 scripts/en_posts.py applica FILE
      Legge un file nello stesso formato, con titolo e corpo tradotti, e scrive i file in _en/.
      Se un blocco ha solo il titolo, il corpo resta quello originale (post senza testo).
      Un corpo fatto solo di "=" lascia il testo originale (già in inglese, o poesie e canzoni di altri).
  python3 scripts/en_posts.py resto
      Copia in _en/ così come sono i post che restano (già in inglese, solo nomi o link).
  python3 scripts/en_posts.py generici
      Traduce da solo i post senza testo con titolo generico (Immagine, Video…).

Ogni file in _en/ ha lo stesso nome dell'originale e vive in /en/scritti/<titolo>/.
"""
import glob
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, "_posts"), os.path.join(ROOT, "_en")
GENERIC = {"Immagine": "Image", "Video": "Video", "Citazione": "Quote", "Link": "Link", "Audio": "Audio",
           "Appunto": "Note", "Foto": "Photo", "Senza titolo": "Untitled"}


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    fm, body = m.group(1), m.group(2)
    title = re.search(r'^title:\s*(.*)$', fm, re.M).group(1).strip()
    if title[:1] == title[-1:] == '"':
        title = title[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    elif title[:1] == title[-1:] == "'":
        title = title[1:-1].replace("''", "'")
    raw = "{% raw %}" in body
    body = body.replace("{% raw %}", "").replace("{% endraw %}", "").strip("\n")
    return fm, title, body, raw


def words(body):
    return len(re.sub(r"<[^>]+>", " ", body).split())


def stem(path):
    return os.path.splitext(os.path.basename(path))[0]


def slug(st):
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", st)


def sources():
    out = []
    for path in glob.glob(os.path.join(SRC, "*")):
        fm, title, body, raw = parse(path)
        cat = "scritti" if "scritti" in re.search(r"^categories:.*$", fm, re.M).group(0) else "taccuino"
        out.append({"path": path, "stem": stem(path), "fm": fm, "title": title, "body": body, "raw": raw, "cat": cat,
                    "ext": os.path.splitext(path)[1]})
    out.sort(key=lambda p: p["stem"], reverse=True)
    return out


def done():
    return {stem(p) for p in glob.glob(os.path.join(DST, "*"))}


def write(post, title, body):
    fm = []
    for line in post["fm"].split("\n"):
        if re.match(r"^(title|permalink|layout|lang|orig):", line):
            continue
        fm.append(line)
    quoted = '"%s"' % title.replace("\\", "\\\\").replace('"', '\\"')
    own = re.search(r"^permalink:\s*(\S+)", post["fm"], re.M)
    url = own.group(1) if own else "/scritti/%s/" % slug(post["stem"])
    head = ["title: " + quoted] + fm + ['orig: "%s"' % post["stem"], "permalink: /en%s" % url]
    text = "---\n" + "\n".join(head) + "\n---\n"
    text += ("{% raw %}\n" + body + "\n{% endraw %}\n") if post["raw"] else (body + "\n")
    os.makedirs(DST, exist_ok=True)
    open(os.path.join(DST, post["stem"] + post["ext"]), "w", encoding="utf-8").write(text)


LONG = re.compile(r"<[^<>]{80,}>")


def compact(body):
    """I tag molto lunghi (immagini con srcset, link con dati) diventano <#1>, <#2>…: non vanno tradotti."""
    n = [0]

    def sub(m):
        n[0] += 1
        return "<#%d>" % n[0]
    return LONG.sub(sub, body)


def expand(translated, source):
    """Rimette al loro posto i tag lunghi dell'originale."""
    tags = LONG.findall(source)
    used = [int(x) for x in re.findall(r"<#(\d+)>", translated)]
    if sorted(used) != list(range(1, len(tags) + 1)):
        return None
    out = re.sub(r"<#(\d+)>", lambda m: tags[int(m.group(1)) - 1], translated)
    # <@em1>, <@em2>…: riprende tale e quale dall'originale l'ennesimo <em>…</em> (versi citati, da non tradurre)
    ems = re.findall(r"<em>.*?</em>", source, re.S)
    try:
        return re.sub(r"<@em(\d+)>", lambda m: ems[int(m.group(1)) - 1], out)
    except IndexError:
        return None


def shape(html):
    tags = Counter(re.findall(r"<\s*([a-zA-Z0-9]+)", html))
    urls = Counter(re.findall(r'(?:href|src)="([^"]*)"', html))
    return tags, urls


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stato"
    posts, have = sources(), done()
    if cmd == "stato":
        for cat in ("scritti", "taccuino"):
            todo = [p for p in posts if p["cat"] == cat and p["stem"] not in have]
            total = sum(1 for p in posts if p["cat"] == cat)
            print("%s: %d tradotti su %d · mancano %d post, %d parole"
                  % (cat, total - len(todo), total, len(todo), sum(words(p["body"]) + len(p["title"].split()) for p in todo)))
    elif cmd == "da-tradurre":
        budget = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
        only = sys.argv[3] if len(sys.argv) > 3 else None
        order = [p for p in posts if p["cat"] == "scritti"] + [p for p in posts if p["cat"] == "taccuino"]
        used = 0
        for p in order:
            if p["stem"] in have or (only and p["cat"] != only):
                continue
            w = words(p["body"]) + len(p["title"].split())
            if used and used + w > budget:
                break
            used += w
            print("@@@ " + p["stem"])
            print(p["title"])
            if words(p["body"]):
                print(compact(p["body"]))
    elif cmd == "applica":
        by_stem = {p["stem"]: p for p in posts}
        text = open(sys.argv[2], encoding="utf-8").read()
        n = 0
        for block in re.split(r"^@@@ ", text, flags=re.M)[1:]:
            lines = block.split("\n")
            st, title, body = lines[0].strip(), lines[1].strip(), "\n".join(lines[2:]).strip("\n")
            post = by_stem.get(st)
            if not post:
                print("!! sconosciuto:", st)
                continue
            if not title:
                print("!! senza titolo:", st)
                continue
            if title == "=":                 # anche il titolo resta com'è
                title = post["title"]
            if body.strip() == "=":          # il corpo resta com'è (già in inglese, o testo di altri lasciato in originale)
                body = post["body"]
            elif not body:
                if words(post["body"]):
                    print("!! manca il corpo:", st)
                    continue
                body = post["body"]
            else:
                body = expand(body, post["body"])
                if body is None:
                    print("!! segnaposto <#n> non corrispondenti:", st)
                    continue
            if shape(body) != shape(post["body"]):
                a, b = shape(post["body"]), shape(body)
                print("?? struttura diversa:", st, dict((a[0] - b[0]) + (b[0] - a[0])), list((a[1] - b[1]) + (b[1] - a[1]))[:3])
            write(post, title, body)
            n += 1
        print("%d traduzioni scritte in _en/" % n)
    elif cmd == "resto":
        # i post rimasti (già in inglese, solo nomi o link, testi di altri) passano così come sono
        n = 0
        for p in posts:
            if p["stem"] not in have:
                write(p, p["title"], p["body"])
                n += 1
        print("%d post copiati senza modifiche" % n)
    elif cmd == "generici":
        n = 0
        for p in posts:
            if p["stem"] not in have and not words(p["body"]) and p["title"] in GENERIC:
                write(p, GENERIC[p["title"]], p["body"])
                n += 1
        print("%d post senza testo tradotti" % n)


if __name__ == "__main__":
    main()
