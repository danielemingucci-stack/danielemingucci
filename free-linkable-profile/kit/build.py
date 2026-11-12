#!/usr/bin/env python3
"""Free Linkable Profile 0.1 — genera index.html da profile.json.

Uso:  python3 build.py            (legge profile.json, scrive index.html nella stessa cartella)
Non servono librerie: basta Python 3.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

TXT = {
    "it": {"about": "Informazioni", "work": "Esperienza", "education": "Formazione", "patents": "Brevetti",
           "publications": "Pubblicazioni", "projects": "Progetti", "certificates": "Licenze e certificazioni",
           "awards": "Premi e riconoscimenti", "volunteer": "Volontariato", "skills": "Competenze",
           "languages": "Lingue", "connections": "Collegamenti", "profiles": "Altri profili",
           "follow": "+ Segui", "contact": "Contatta", "contact_info": "Informazioni di contatto",
           "present": "Presente", "mutual": "Collegamento reciproco", "oneway": "In attesa di conferma",
           "made": "Profilo libero, senza piattaforma",
           "months": ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]},
    "en": {"about": "About", "work": "Experience", "education": "Education", "patents": "Patents",
           "publications": "Publications", "projects": "Projects", "certificates": "Licenses & certifications",
           "awards": "Honors & awards", "volunteer": "Volunteering", "skills": "Skills",
           "languages": "Languages", "connections": "Connections", "profiles": "Other profiles",
           "follow": "+ Follow", "contact": "Contact", "contact_info": "Contact info",
           "present": "Present", "mutual": "Mutual connection", "oneway": "Awaiting confirmation",
           "made": "A free profile, no platform in between",
           "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},
}


def e(value):
    return html.escape(str(value or ""), quote=True)


def link(url):
    """Accetta solo indirizzi web e mail: niente javascript: o simili."""
    url = str(url or "").strip()
    return url if re.match(r"^(https?://|mailto:)", url, re.I) else ""


def paragraphs(text):
    parts = [p.strip() for p in re.split(r"\n\s*\n", str(text or "")) if p.strip()]
    return "".join("<p>%s</p>" % e(p).replace("\n", "<br>") for p in parts)


def date(value, t):
    value = str(value or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})(-\d{2})?$", value)
    if m and 1 <= int(m.group(2)) <= 12:
        return "%s %s" % (t["months"][int(m.group(2)) - 1], m.group(1))
    return value


def period(start, end, t, open_ended=False):
    a, b = date(start, t), date(end, t)
    if a and (b or open_ended):
        return "%s – %s" % (a, b or t["present"])
    return a or b


def initial(name):
    name = str(name or "").strip()
    return e(name[0].upper()) if name else ""


def item(title, url="", role="", meta=None, desc="", logo=None):
    href = link(url)
    head = '<a href="%s">%s</a>' % (e(href), e(title)) if href else e(title)
    out = ['<div class="flp-item">']
    if logo is not None:
        out.append('<div class="flp-logo" aria-hidden="true">%s</div>' % initial(logo))
    out.append('<div class="flp-body"><h3>%s</h3>' % head)
    if role:
        out.append('<p class="flp-r">%s</p>' % e(role))
    for line in meta or []:
        if line:
            out.append('<p class="flp-q">%s</p>' % e(line))
    if desc:
        out.append('<div class="flp-d">%s</div>' % paragraphs(desc))
    out.append("</div></div>")
    return "".join(out)


def section(title, body):
    if not body:
        return ""
    return '<section class="flp-card flp-pad" aria-label="%s"><h2>%s</h2>%s</section>' % (e(title), e(title), body)


def join(parts, sep=" · "):
    return sep.join(str(p) for p in parts if p)


def build(profile):
    basics = profile.get("basics") or {}
    flp = profile.get("flp") or {}
    lang = flp.get("lang") if flp.get("lang") in TXT else "it"
    t = TXT[lang]
    theme = flp.get("theme") or {}
    name = basics.get("name") or ""
    loc = basics.get("location") or {}
    where = join([loc.get("city"), loc.get("region")], ", ")
    page_url = link(flp.get("url"))
    email = str(basics.get("email") or "").strip()
    mailto = "mailto:" + email if re.match(r"^[^@\s]+@[^@\s]+$", email) else ""
    follow = link(flp.get("follow")) or link(flp.get("feed"))
    image = link(basics.get("image"))
    cover = link(flp.get("cover"))

    css_vars = []
    for key, var in (("accent", "--flp-accent"), ("background", "--flp-bg"), ("card", "--flp-card"),
                     ("ink", "--flp-ink"), ("muted", "--flp-muted"), ("font", "--flp-font"),
                     ("titleFont", "--flp-title")):
        val = str(theme.get(key) or "")
        if val and not re.search(r"[;{}<>]", val):
            css_vars.append("%s:%s" % (var, val))

    # --- intestazione
    head = ['<section class="flp-card h-card" aria-label="%s">' % e(name)]
    head.append('<div class="flp-cover"%s></div>' % (' style="background-image:url(&quot;%s&quot;)"' % e(cover) if cover else ""))
    head.append('<div class="flp-head">')
    if image:
        head.append('<img class="flp-avatar u-photo" src="%s" alt="%s">' % (e(image), e(name)))
    else:
        head.append('<div class="flp-avatar flp-initial" aria-hidden="true">%s</div>' % initial(name))
    head.append('<h1 class="p-name">%s</h1>' % e(name))
    if basics.get("label"):
        head.append('<p class="flp-label p-job-title">%s</p>' % e(basics["label"]))
    contact = '<a href="%s">%s</a>' % (e(mailto), e(t["contact_info"])) if mailto else ""
    if where or contact:
        head.append('<p class="flp-where"><span class="p-locality">%s</span>%s%s</p>' % (e(where), " · " if where and contact else "", contact))
    buttons = []
    if follow:
        buttons.append('<a class="flp-btn flp-full" href="%s">%s</a>' % (e(follow), e(t["follow"])))
    if mailto:
        buttons.append('<a class="flp-btn%s u-email" href="%s">%s</a>' % ("" if follow else " flp-full", e(mailto), e(t["contact"])))
    site = link(basics.get("url"))
    if site:
        buttons.append('<a class="flp-btn u-url" rel="me" href="%s">%s</a>' % (e(site), e(re.sub(r"^https?://(www\.)?|/$", "", site))))
    if buttons:
        head.append('<div class="flp-actions">%s</div>' % "".join(buttons))
    head.append("</div></section>")

    main = ["".join(head)]
    if basics.get("summary"):
        main.append('<section class="flp-card flp-pad" aria-label="%s"><h2>%s</h2><div class="flp-about p-note">%s</div></section>'
                    % (e(t["about"]), e(t["about"]), paragraphs(basics["summary"])))

    main.append(section(t["work"], "".join(
        item(w.get("position"), "", join([w.get("name")]),
             [period(w.get("startDate"), w.get("endDate"), t, open_ended=True), w.get("location")],
             w.get("summary"), logo=w.get("name"))
        for w in profile.get("work") or [])))
    main.append(section(t["education"], "".join(
        item(s.get("institution"), s.get("url"), join([s.get("studyType"), s.get("area")], ", "),
             [period(s.get("startDate"), s.get("endDate"), t)], s.get("summary"), logo=s.get("institution"))
        for s in profile.get("education") or [])))
    main.append(section(t["patents"], "".join(
        item(p.get("name"), p.get("url"), "", [join([p.get("office"), p.get("number"), date(p.get("date"), t)])], p.get("summary"))
        for p in profile.get("patents") or [])))
    main.append(section(t["publications"], "".join(
        item(p.get("name"), p.get("url"), "", [join([p.get("publisher"), date(p.get("releaseDate"), t)])], p.get("summary"))
        for p in profile.get("publications") or [])))
    main.append(section(t["projects"], "".join(
        item(p.get("name"), p.get("url"), "", [period(p.get("startDate"), p.get("endDate"), t)], p.get("description"))
        for p in profile.get("projects") or [])))
    main.append(section(t["certificates"], "".join(
        item(c.get("name"), c.get("url"), c.get("issuer"), [date(c.get("date"), t)], "", logo=c.get("issuer") or c.get("name"))
        for c in profile.get("certificates") or [])))
    main.append(section(t["awards"], "".join(
        item(a.get("title"), "", "", [join([a.get("awarder"), date(a.get("date"), t)])], a.get("summary"))
        for a in profile.get("awards") or [])))
    main.append(section(t["volunteer"], "".join(
        item(v.get("position"), v.get("url"), v.get("organization"),
             [period(v.get("startDate"), v.get("endDate"), t, open_ended=True)], v.get("summary"), logo=v.get("organization"))
        for v in profile.get("volunteer") or [])))
    skills = [s.get("name") for s in profile.get("skills") or [] if s.get("name")]
    if skills:
        main.append(section(t["skills"], '<div class="flp-pills">%s</div>' % "".join("<span>%s</span>" % e(s) for s in skills)))
    main.append(section(t["languages"], "".join(
        item(l.get("language"), "", "", [l.get("fluency")]) for l in profile.get("languages") or [])))

    # --- colonna laterale: collegamenti e altri profili
    side = []
    conns = []
    for c in flp.get("connections") or []:
        url = link(c.get("url"))
        if not url:
            continue
        extra = ' data-flp-json="%s"' % e(link(c.get("json"))) if link(c.get("json")) else ""
        conns.append(
            '<div class="flp-item" data-flp-connection="%s"%s>'
            '<div class="flp-logo" data-flp-image aria-hidden="true">%s</div>'
            '<div class="flp-body"><h3><a href="%s" rel="contact">%s</a></h3>'
            '<p class="flp-q" data-flp-label></p><p class="flp-status" data-flp-status></p></div></div>'
            % (e(url), extra, initial(c.get("name")), e(url), e(c.get("name") or url)))
    side.append(section(t["connections"], "".join(conns)))
    profiles = ['<a rel="me" href="%s">%s</a>' % (e(link(p.get("url"))), e(p.get("network") or p.get("url")))
                for p in basics.get("profiles") or [] if link(p.get("url"))]
    if profiles:
        side.append(section(t["profiles"], '<nav class="flp-list">%s</nav>' % "".join(profiles)))
    side.append('<p class="flp-foot">%s · <a href="https://www.danielemingucci.com/free-linkable-profile/">Free Linkable Profile</a></p>' % e(t["made"]))

    # --- dati per i motori di ricerca (schema.org)
    person = {"@type": "Person", "name": name}
    if basics.get("label"):
        person["jobTitle"] = basics["label"]
    if basics.get("summary"):
        person["description"] = re.sub(r"\s+", " ", basics["summary"]).strip()
    if image:
        person["image"] = image
    if site:
        person["url"] = site
    if where:
        person["address"] = {"@type": "PostalAddress", "addressLocality": loc.get("city") or "", "addressRegion": loc.get("region") or ""}
    same = [link(p.get("url")) for p in basics.get("profiles") or [] if link(p.get("url"))]
    if same:
        person["sameAs"] = same
    current = [w.get("name") for w in profile.get("work") or [] if w.get("name") and not w.get("endDate")]
    if current:
        person["worksFor"] = [{"@type": "Organization", "name": n} for n in current]
    schools = [s.get("institution") for s in profile.get("education") or [] if s.get("institution")]
    if schools:
        person["alumniOf"] = [{"@type": "EducationalOrganization", "name": n} for n in schools]
    langs = [l.get("language") for l in profile.get("languages") or [] if l.get("language")]
    if langs:
        person["knowsLanguage"] = langs
    known = [link(c.get("url")) for c in flp.get("connections") or [] if link(c.get("url"))]
    if known:
        person["knows"] = [{"@type": "Person", "name": c.get("name") or "", "url": link(c.get("url"))}
                           for c in flp.get("connections") or [] if link(c.get("url"))]
    ld = {"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": person}
    if page_url:
        ld["url"] = page_url
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")

    description = join([basics.get("label"), where], " · ") or name
    return """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}{title_sep}{label}</title>
<meta name="description" content="{name} — {description}">
<meta property="og:type" content="profile">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{description}">
{og_image}{canonical}<link rel="alternate" type="application/json" title="Free Linkable Profile" href="profile.json">
{feed}<link rel="stylesheet" href="flp.css">
<script type="application/ld+json">{ld}</script>
</head>
<body class="flp"{style}>
<main class="flp-page" data-flp-profile="{profile_url}" data-flp-text-mutual="{mutual}" data-flp-text-oneway="{oneway}">
<div class="flp-col">{main}</div>
<aside class="flp-col">{side}</aside>
</main>
<script src="flp.js" defer></script>
</body>
</html>
""".format(
        lang=lang, name=e(name), title_sep=" — " if basics.get("label") else "", label=e(basics.get("label")),
        description=e(description),
        og_image='<meta property="og:image" content="%s">\n' % e(image) if image else "",
        canonical='<link rel="canonical" href="%s">\n' % e(page_url) if page_url else "",
        feed='<link rel="alternate" type="application/atom+xml" href="%s">\n' % e(link(flp.get("feed"))) if link(flp.get("feed")) else "",
        ld=ld_json, style=' style="%s"' % e(";".join(css_vars)) if css_vars else "",
        profile_url=e(page_url), mutual=e(t["mutual"]), oneway=e(t["oneway"]),
        main="".join(m for m in main if m), side="".join(s for s in side if s))


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "profile.json")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(src)), "index.html")
    with open(src, encoding="utf-8") as f:
        profile = json.load(f)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(build(profile))
    print("Scritto %s" % dst)


if __name__ == "__main__":
    main()
