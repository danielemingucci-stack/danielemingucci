#!/usr/bin/env python3
"""Genera le versioni inglesi (en/*.html) della home e dei cinque mondi a partire dalle pagine
italiane, e aggiunge a entrambe il cambio lingua. Ogni testo visibile deve avere una traduzione
qui sotto: se ne manca una lo script si ferma e dice quale.

Uso:  python3 scripts/en_pages.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index", "acqua", "terra", "aria", "fuoco", "quinto"]

SAME = {"Daniele Mingucci", "Daniele", "Mingucci", "Stramba", "Traspality", "Books121", "Capital Units", "Kerga",
        "Up to Cinema", "MNG-crea", "Tumblr", "Substack", "Peerlist", "dacco@mng-crea.com", "AI", "Online",
        "Co-Founder, STRAMBA India", "Inventor in Chief · CTO &amp; CEO, STRAMBA Italy", "Founder · attitude branding",
        "· Privacy · Cookie policy", "width=device-width, initial-scale=1", "https://www.danielemingucci.com/img/boat.jpg",
        "{{ ultimo.title | escape }}", "{{ post.title | escape }}", "far west", "IT", "EN", "English", "Italiano"}

EN = {
    "Daniele Mingucci — inventore, imprenditore, autore. Stramba, Traspality, Books121, Capital Units, MNG-crea, scritti e romanzi.":
        "Daniele Mingucci — inventor, entrepreneur, author. Stramba, Traspality, Books121, Capital Units, MNG-crea, writings and novels.",
    "Mondi": "Worlds", "Acqua": "Water", "Terra": "Earth", "Aria": "Air", "Fuoco": "Fire",
    "Il quinto elemento": "The fifth element", "I mondi": "The worlds",
    "Acqua · Mare": "Water · Sea", "Terra · Startup": "Earth · Startups", "Aria · Parole": "Air · Words",
    "Fuoco · Linguaggi": "Fire · Languages", "Altrove": "Elsewhere", "Profilo": "Profile",
    "Innovazione · Impresa · Comunicazione": "Innovation · Enterprise · Communication",
    "Mondi paralleli. Uno alla volta.": "Parallel worlds. One at a time.",
    "Mare · Stramba": "Sea · Stramba",
    "Startup · Traspality, Books121, Capital Units": "Startups · Traspality, Books121, Capital Units",
    "Parole · scritti e romanzi": "Words · writings and novels",
    "Linguaggi · MNG-crea": "Languages · MNG-crea",
    "Ultimo scritto · {% include data.html d=ultimo.date %}": "Latest piece · {% include data.html d=ultimo.date %}",
    "Ultimo scritto · 9 novembre 2026": "Latest piece · 9 November 2026",
    "Lavoro, opera,": "Labour, work,", "azione": "action",
    "Arendt, la Vita Activa, e il senso del fare.": "Arendt, the Vita Activa, and the meaning of making.",
    "Tutti gli scritti": "All writings",
    "© 2026 MNG-Crea · Riccione RN, Italia · P.IVA 04615660406 ·": "© 2026 MNG-Crea · Riccione RN, Italy · VAT no. IT04615660406 ·",
    "Scrivi": "Write",
    "Daniele Mingucci — Acqua": "Daniele Mingucci — Water",
    "Daniele Mingucci a prua, sotto l'albero di STRAMBA": "Daniele Mingucci at the bow, beneath the STRAMBA mast",
    "Immagini": "Images", "La vela di STRAMBA": "The STRAMBA sail", "Mare": "Sea",
    "Un sistema velico brevettato, nato da un'intuizione e sviluppato fino a un prototipo in mare dal 2021.":
        "A patented sail system, born of an intuition and developed into a prototype that has been at sea since 2021.",
    "Oggi il progetto guarda al trasporto marittimo e alla decarbonizzazione delle navi cargo, con un percorso di licenza internazionale attraverso STRAMBA India.":
        "Today the project looks to maritime transport and the decarbonisation of cargo ships, with an international licensing path through STRAMBA India.",
    "Entra in stramba.it ↗": "Visit stramba.it ↗",
    "[Immagine da aggiungere: il prototipo in navigazione]": "[Image to be added: the prototype under sail]",
    "Prossimo mondo": "Next world",
    "Daniele Mingucci — Terra": "Daniele Mingucci — Earth",
    "Un libro di Books121 passa di mano": "A Books121 book changes hands",
    "Startup": "Startups",
    "Piattaforme per la qualità, l'editoria e il valore d'impresa. Ognuna ha qui la sua presentazione e il proprio sito di riferimento.":
        "Platforms for quality, publishing and business value. Each has its presentation here and its own website.",
    "Online in beta": "Online in beta",
    "Trasparenza e qualità in un unico strumento. Le imprese raccontano il proprio operato e, raccontandolo, lo certificano.":
        "Transparency and quality in a single tool. Companies tell the story of what they do and, by telling it, certify it.",
    "Al centro c'è l'identità: la qualità come carattere distintivo, non come standard uguale per tutti.":
        "Identity is at the centre: quality as a distinguishing trait, not as a standard that is the same for everyone.",
    "Entra in traspality.com ↗": "Visit traspality.com ↗",
    "Un modello di circolazione per i libri di carta: si paga la lettura, non il possesso.":
        "A circulation model for paper books: you pay for reading, not for owning.",
    "I lettori leggono su carta a prezzi digitali; autori ed editori conoscono finalmente i propri lettori, uno a uno.":
        "Readers read on paper at digital prices; authors and publishers finally get to know their readers, one by one.",
    "Entra in books121.com ↗": "Visit books121.com ↗",
    "Valore d'impresa": "Business value",
    "Uno strumento per misurare il valore oltre il dato finanziario.": "A tool for measuring value beyond the financial figures.",
    "Impegno, talento, relazioni e conoscenza diventano capitale riconosciuto, che le aziende possono mettere in campo accanto alle forme classiche di partecipazione.":
        "Commitment, talent, relationships and knowledge become recognised capital, which companies can bring into play alongside the classic forms of participation.",
    "Entra in capitalunits.org ↗": "Visit capitalunits.org ↗",
    "In sviluppo": "In development",
    "Porto di Riccione": "Port of Riccione",
    "Un porto per grandi imbarcazioni nel cuore della città, unico sull'Adriatico.":
        "A harbour for large vessels in the heart of the town, the only one of its kind on the Adriatic.",
    "L'elettrificazione dal basso, a partire dai concessionari.": "Electrification from the ground up, starting with the dealerships.",
    "Storie di qualità portate fino al cinema, con team professionali.": "Quality stories taken all the way to the cinema, with professional teams.",
    "Daniele Mingucci — Aria": "Daniele Mingucci — Air",
    "Una Olivetti Lettera 22 con un foglio scritto": "An Olivetti Lettera 22 with a typed sheet",
    "Scritti": "Writings", "Romanzi": "Novels", "Copertina": "Cover", "Parole": "Words",
    "Scritti su lavoro, impresa, innovazione e cultura. E i romanzi.": "Writings on work, business, innovation and culture. And the novels.",
    "Taccuino": "Notebook",
    "9 novembre 2026": "9 November 2026", "21 ottobre 2026": "21 October 2026", "17 settembre 2026": "17 September 2026",
    "24 agosto 2026": "24 August 2026", "17 agosto 2026": "17 August 2026",
    "Il terzo settore dell'": "The third sector of ", "artigianato": "craftsmanship",
    "Crescita e": "Growth and", "Artigianato digitale": "Digital craftsmanship",
    "L'innovazione è una": "Innovation is a", "colpa": "fault",
    "I nuovi scritti, via email.": "New writings, by email.",
    "Iscriviti su Substack": "Subscribe on Substack",
    "Romanzi pubblicati e in preparazione, tra impresa, invenzione e storie d'amore.":
        "Novels published and in the making, between enterprise, invention and love stories.",
    "Tutti i libri": "All the books",
    "Daniele Mingucci — Fuoco": "Daniele Mingucci — Fire",
    "Un fiume tra gli argini di una città, in bianco e nero": "A river between the embankments of a city, in black and white",
    "Linguaggi": "Languages",
    "Consulenza di attitude branding: identità, linguaggi e strategie di comunicazione per imprese e progetti.":
        "Attitude branding consultancy: identity, languages and communication strategies for companies and projects.",
    "Oltre vent'anni alla guida di un'agenzia di comunicazione. Il lato creativo vive su mng-crea.com.":
        "More than twenty years at the head of a communication agency. The creative side lives at mng-crea.com.",
    "Entra in mng-crea.com ↗": "Visit mng-crea.com ↗",
    "Ritratto di Daniele Mingucci": "Portrait of Daniele Mingucci",
    "Fondatore di STRAMBA, sistemi velici brevettati per la nautica e il trasporto marittimo. Ideatore di piattaforme per la qualità, l'editoria e il valore d'impresa. Oltre vent'anni alla guida di un'agenzia di comunicazione, una laurea in Lettere Classiche, diversi romanzi.":
        "Founder of STRAMBA, patented sail systems for boating and maritime transport. Creator of platforms for quality, publishing and business value. More than twenty years at the head of a communication agency, a degree in Classics, several novels.",
    "Contatti": "Contact", "Curriculum completo →": "Full profile →",
    "I nuovi scritti,": "New writings,", "via email.": "by email.",
    "Torna alla soglia": "Back to the threshold", "Tutti i": "All the", "mondi": "worlds",
}

ATTR = re.compile(r'((?:aria-label|alt|content)=")([^"]*[A-Za-zÀ-ú][^"]*)(")')
NODE = re.compile(r"(>)(\s*)([^<>]*?[A-Za-zÀ-ú][^<>]*?)(\s*)(<)")


def split_page(html):
    """Separa stile e script (che non si traducono) dal resto."""
    return re.split(r"(<style.*?</style>|<script.*?</script>|\{%.*?%\})", html, flags=re.S)


def tr(text, missing):
    if text in SAME or text.startswith(("{%", "{{")) or re.fullmatch(r"[\W\d]*", text):
        return text
    if text in EN:
        return EN[text]
    missing.add(text)
    return text


def lang_link(html, href, label, name, lang):
    """Voce di cambio lingua nel menu, subito dopo Profilo; e i link hreflang nella testa."""
    html = re.sub(r'\s*<a [^>]*data-lingua[^>]*>.*?</a>', "", html)
    m = re.search(r'(<a href="[^"]*" data-menu style="([^"]*)">[^<]*</a>)', html)
    if not m:
        raise SystemExit("Menu non trovato")
    link = '\n  <a href="%s" data-lingua hreflang="%s" lang="%s" aria-label="%s" style="%s">%s</a>' % (href, lang, lang, name, m.group(2), label)
    return html.replace(m.group(1), m.group(1) + link, 1)


def hreflang(html, page):
    it = "/" if page == "index" else "/%s.html" % page
    en = "/en/" if page == "index" else "/en/%s.html" % page
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', "", html)
    html = re.sub(r'<style id="menu-stretto">.*?</style>\n', "", html, flags=re.S)
    tight = ('<style id="menu-stretto">@media (max-width:440px){nav a[aria-label],nav a[data-menu]{padding-left:6px !important;'
             'padding-right:6px !important}nav a[data-menu],nav a[data-lingua]{margin-left:2px !important;'
             'letter-spacing:.14em !important}nav a[data-lingua]{padding-left:8px !important;padding-right:4px !important}}</style>\n')
    html = html.replace("</head>", tight + "</head>", 1)
    tags = "".join('<link rel="alternate" hreflang="%s" href="https://www.danielemingucci.com%s">\n' % (code, url)
                   for code, url in (("it", it), ("en", en), ("x-default", it)))
    return html.replace("</head>", tags + "</head>", 1), it, en


def main():
    missing = set()
    os.makedirs(os.path.join(ROOT, "en"), exist_ok=True)
    for page in PAGES:
        path = os.path.join(ROOT, page + ".html")
        html = open(path, encoding="utf-8").read()
        html, it, en = hreflang(html, page)
        html = lang_link(html, en, "EN", "English", "en")
        open(path, "w", encoding="utf-8").write(html)

        out = []
        for part in split_page(html):
            if part.startswith(("<style", "<script", "{%")):
                out.append(part)
                continue
            part = ATTR.sub(lambda m: m.group(1) + tr(m.group(2), missing) + m.group(3), part)
            part = NODE.sub(lambda m: m.group(1) + m.group(2) + tr(m.group(3), missing) + m.group(4) + m.group(5), part)
            out.append(part)
        e = "".join(out)
        e = e.replace('<html lang="it">', '<html lang="en">', 1)
        e = e.replace("Ultimo scritto · {%", "Latest piece · {%")
        e = re.sub(r'(src|href)="img/', r'\1="/img/', e)
        e = re.sub(r"url\((['\"]?)img/", r"url(\1/img/", e)
        for a in ("/curriculum/", "/scritti/", "/taccuino/"):
            e = e.replace('href="%s"' % a, 'href="/en%s"' % a)
        e = lang_link(e, it, "IT", "Italiano", "it")
        if e.startswith("---"):
            head, body = e[3:].split("---\n", 1)
            head = re.sub(r"\npermalink:.*", "", head).rstrip("\n")
            head += "\nlang: en\npermalink: %s\n" % ("/en/" if page == "index" else "/en/%s.html" % page)
            assign = ("{%- assign en_scritti = site.en | where_exp: \"p\", \"p.categories contains 'scritti'\" "
                      "| sort: \"date\" | reverse -%}\n")
            body = body.replace("site.categories.scritti", "en_scritti")
            body = body.replace("{{ ultimo.excerpt | strip_html", "{{ ultimo.excerpt | default: ultimo.content | strip_html")
            e = "---" + head + "---\n" + assign + body
        open(os.path.join(ROOT, "en", page + ".html"), "w", encoding="utf-8").write(e)
    if missing:
        print("Testi senza traduzione (aggiungili in EN dentro scripts/en_pages.py):")
        for m in sorted(missing):
            print("  ", m)
        sys.exit(1)
    print("Pagine inglesi generate in en/")


if __name__ == "__main__":
    main()
