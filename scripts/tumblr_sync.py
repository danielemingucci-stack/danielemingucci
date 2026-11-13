"""Porta sul sito i nuovi post di dacco1971.tumblr.com (solo i propri, non i reblog).
Gira su GitHub Actions ogni 12 ore. Si ferma al primo post gia' presente nel sito."""
import json,re,html,unicodedata,datetime,os,glob,urllib.request
BLOG="https://dacco1971.tumblr.com"
POSTS=os.path.join(os.path.dirname(__file__),"..","_posts")
def slugify(s):
    s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()
    s=re.sub(r"[^a-z0-9]+","-",s).strip("-")
    return s[:60].rstrip("-")
def text(h): return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h or ""))).strip()
def words(s,n=9):
    w=s.split(); return " ".join(w[:n])+("…" if len(w)>n else "")
def tidy_title(t):
    t=t.strip().strip(".:").strip()
    if t and t.upper()==t and any(c.isalpha() for c in t): t=t[0]+t[1:].lower()
    return t
def clean(b):
    b=b or ""
    b=re.sub(r"<p>\s*(<br\s*/?>)?\s*</p>","",b)
    b=re.sub(r'\sdata-npf=\'[^\']*\'','',b)
    b=re.sub(r'\s(width|height)="\d+"','',b) if "<iframe" not in b else b
    return b.strip()

def fetch(start):
    req=urllib.request.Request(f"{BLOG}/api/read/json?num=50&start={start}",headers={"User-Agent":"danielemingucci.com sync"})
    t=urllib.request.urlopen(req,timeout=60).read().decode("utf-8")
    t=re.sub(r"^var tumblr_api_read = ","",t).rstrip().rstrip(";")
    return json.loads(t)["posts"]
def slim(p):
    o={"id":p["id"],"type":p["type"],"date":p["date-gmt"],"slug":p.get("slug") or "","url":p["url-with-slug"],"tags":p.get("tags") or []}
    keys={"regular":["regular-title","regular-body"],"photo":["photo-caption"],"quote":["quote-text","quote-source"],"link":["link-text","link-url","link-description"],"video":["video-caption","video-source"],"audio":["audio-caption","id3-title"],"conversation":["conversation-title","conversation-text"]}.get(p["type"],[])
    for k in keys:
        if p.get(k): o[k]=p[k]
    if p["type"]=="photo":
        o["photos"]=[x["photo-url-1280"] for x in p.get("photos") or []] or [p.get("photo-url-1280")]
        o["photos"]=[u for u in o["photos"] if u]
    if p["type"]=="video" and p.get("video-player"): o["player"]=p["video-player"]
    return o
known=set()
for f in glob.glob(os.path.join(POSTS,"*")):
    m=re.search(r"^tumblr: .*/post/(\d+)",open(f,encoding="utf-8").read(),re.M)
    if m: known.add(m.group(1))
existing={os.path.basename(f)[:-5] for f in glob.glob(os.path.join(POSTS,"*.html"))}
new=[]; stop=False
for start in range(0,500,50):
    page=fetch(start)
    if not page: break
    for p in page:
        if p.get("reblogged-from-url") or p.get("reblogged-root-url"): continue
        if str(p["id"]) in known: stop=True; break
        new.append(slim(p))
    if stop: break
for p in reversed(new):
    d=datetime.datetime.strptime(p["date"],"%Y-%m-%d %H:%M:%S GMT").replace(tzinfo=datetime.timezone.utc)
    t=p["type"]; title=""; body=""; cat="taccuino"; img=None
    if t=="regular":
        cat="scritti"; b=clean(p.get("regular-body",""))
        title=tidy_title(p.get("regular-title",""))
        if not title:
            m=re.match(r"\s*<(p|h1|h2|h3)[^>]*>(.*?)</\1>",b,re.S)
            first=text(m.group(2)) if m else ""
            if m and 0<len(first)<=90 and not first.endswith(("…","...")) and len(text(b))>len(first)+40:
                title=tidy_title(first); b=b[m.end():].strip()
                b=re.sub(r"^(<p>\s*(<br\s*/?>)?\s*</p>\s*)+","",b)
            else:
                title=words(text(b))
        body=b
    elif t=="photo":
        cap=clean(p.get("photo-caption","")); ph=p.get("photos") or []
        img=ph[0] if ph else None
        title=words(text(cap),8) or "Immagine"
        body="".join(f'<img src="{u}" alt="" loading="lazy">' for u in ph)+cap
    elif t=="quote":
        q=p.get("quote-text",""); src=p.get("quote-source","")
        title=words(text(q),8)
        body=f"<blockquote><p>{q}</p></blockquote>"+(f'<p class="fonte">{src}</p>' if src else "")
    elif t=="link":
        title=text(p.get("link-text","")) or p.get("link-url","")
        body=f'<p><a href="{html.escape(p.get("link-url",""),quote=True)}">{p.get("link-text") or p.get("link-url")}</a></p>'+clean(p.get("link-description",""))
    elif t=="video":
        cap=clean(p.get("video-caption","")); pl=p.get("video-source") or p.get("player") or ""
        title=words(text(cap),8) or "Video"
        body=(f'<div class="video">{pl}</div>' if "<iframe" in pl else "")+cap
    elif t=="audio":
        cap=clean(p.get("audio-caption",""))
        title=words(text(cap),8) or text(p.get("id3-title","")) or "Audio"
        body=cap+f'<p><a href="{p["url"]}">Ascolta su Tumblr</a></p>'
    elif t=="conversation":
        title=text(p.get("conversation-title","")) or words(text(p.get("conversation-text","")),8)
        body=p.get("conversation-text","")
    title=title or "Senza titolo"
    slug=slugify(p.get("slug") or title) or str(p["id"])
    # l'indirizzo è /scritti/<slug>/: se un altro post (anche di un altro giorno) ha già questo slug, lo rendo unico
    if slug in {re.sub(r"^\d{4}-\d{2}-\d{2}-","",x) for x in existing}: slug=f"{slug}-{str(str(p['id']))[-6:]}"
    existing.add(f"{d.strftime('%Y-%m-%d')}-{slug}")
    fm=["---",f"title: {json.dumps(title,ensure_ascii=False)}",f"date: {d.strftime('%Y-%m-%d %H:%M:%S')} +0000",f"categories: [{cat}]",f"formato: {t}",f"tumblr: {p['url']}"]
    tags=[x for x in (p.get("tags") or []) if x]
    if tags: fm.append("tags: "+json.dumps(tags,ensure_ascii=False))
    if img: fm.append(f"immagine: {img}")
    fm.append("---")
    open(os.path.join(POSTS,f"{d.strftime('%Y-%m-%d')}-{slug}.html"),"w",encoding="utf-8").write("\n".join(fm)+"\n{% raw %}\n"+body+"\n{% endraw %}\n")
    print("nuovo:",cat,title)
print(f"{len(new)} post nuovi")
