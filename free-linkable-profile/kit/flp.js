/* Free Linkable Profile 0.2 — i profili si riconoscono tra loro, senza piattaforma.
   1. Collegamenti: per ognuno legge il profile.json dell'altro sito e controlla se anche lui
      collega questo profilo. Se sì, il collegamento è reciproco.
   2. Trasloco: se un profilo dichiara flp.movedTo, segue il nuovo indirizzo.
   3. Vetrina: una pagina con data-flp-showcase mostra un profilo che vive su un altro sito.
   Nessun dato viene inviato: sono solo letture di file pubblici.
   I dati letti da altri siti entrano nella pagina solo come testo, mai come HTML. */
(function () {
  "use strict";

  var TXT = {
    it: { about: "Informazioni", work: "Esperienza", education: "Formazione", patents: "Brevetti",
          publications: "Pubblicazioni", projects: "Progetti", certificates: "Licenze e certificazioni",
          awards: "Premi e riconoscimenti", volunteer: "Volontariato", skills: "Competenze",
          languages: "Lingue", connections: "Collegamenti", profiles: "Altri profili",
          follow: "+ Segui", contact: "Contatta", contact_info: "Informazioni di contatto",
          present: "Presente", mutual: "Collegamento reciproco", oneway: "In attesa di conferma",
          original: "Profilo originale", unreachable: "Il profilo non è raggiungibile in questo momento.",
          months: ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"] },
    en: { about: "About", work: "Experience", education: "Education", patents: "Patents",
          publications: "Publications", projects: "Projects", certificates: "Licenses & certifications",
          awards: "Honors & awards", volunteer: "Volunteering", skills: "Skills",
          languages: "Languages", connections: "Connections", profiles: "Other profiles",
          follow: "+ Follow", contact: "Contact", contact_info: "Contact info",
          present: "Present", mutual: "Mutual connection", oneway: "Awaiting confirmation",
          original: "Original profile", unreachable: "This profile cannot be reached right now.",
          months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] }
  };

  /* ---------- indirizzi ---------- */
  function norm(u) {
    try {
      var x = new URL(u, location.href);
      return (x.host.replace(/^www\./, "") + x.pathname.replace(/index\.html$/, "").replace(/\/+$/, "")).toLowerCase();
    } catch (e) { return ""; }
  }
  function web(u) {
    try { var x = new URL(String(u)); return /^https?:$/.test(x.protocol) ? x.href : ""; } catch (e) { return ""; }
  }
  function mail(u) {
    u = String(u || "").trim();
    return /^[^@\s<>"']+@[^@\s<>"']+$/.test(u) ? "mailto:" + u : "";
  }
  function safeImage(u) {
    try { return new URL(String(u)).protocol === "https:" ? String(u) : ""; } catch (e) { return ""; }
  }
  function jsonUrl(url) {
    try { return new URL("profile.json", /\/$/.test(url) ? url : url + "/").href; } catch (e) { return ""; }
  }
  function str(v, max) { return typeof v === "string" || typeof v === "number" ? String(v).slice(0, max || 4000) : ""; }
  function arr(v) { return Array.isArray(v) ? v.filter(function (x) { return x && typeof x === "object"; }).slice(0, 200) : []; }

  /* Legge un profilo; se si è trasferito (flp.movedTo) segue il nuovo indirizzo, al massimo tre volte. */
  function load(url, json, hops) {
    var j = json || jsonUrl(url);
    if (!j) return Promise.reject(new Error("url"));
    return fetch(j, { mode: "cors", credentials: "omit" })
      .then(function (r) { if (!r.ok) throw new Error("http"); return r.json(); })
      .then(function (p) {
        var to = p && p.flp ? web(p.flp.movedTo) : "";
        if (to && norm(to) !== norm(url) && (hops || 0) < 3) return load(to, null, (hops || 0) + 1);
        return { profile: p || {}, url: url };
      });
  }

  /* Gli indirizzi che valgono come "questo profilo": quello attuale, più i precedenti
     (flp.previous) solo se il vecchio indirizzo conferma il trasloco verso questo. */
  function mine(root) {
    var me = norm(root.getAttribute("data-flp-profile"));
    var prev = (root.getAttribute("data-flp-previous") || "").split(/\s+/).filter(Boolean).slice(0, 5);
    return Promise.all(prev.map(function (u) {
      return fetch(jsonUrl(u), { mode: "cors", credentials: "omit" })
        .then(function (r) { if (!r.ok) throw new Error("http"); return r.json(); })
        .then(function (p) { return p && p.flp && norm(web(p.flp.movedTo)) === me ? norm(u) : ""; })
        .catch(function () { return ""; });
    })).then(function (ok) { return [me].concat(ok.filter(Boolean)); });
  }

  /* ---------- collegamenti ---------- */
  function connections(root) {
    var nodes = root.querySelectorAll("[data-flp-connection]");
    if (!nodes.length) return;
    var txtMutual = root.getAttribute("data-flp-text-mutual") || TXT.it.mutual;
    var txtOneWay = root.getAttribute("data-flp-text-oneway") || TXT.it.oneway;
    mine(root).then(function (addresses) {
      Array.prototype.forEach.call(nodes, function (el) {
        var url = el.getAttribute("data-flp-connection");
        load(url, el.getAttribute("data-flp-json")).then(function (res) {
          var p = res.profile, basics = (p && p.basics) || {};
          if (norm(res.url) !== norm(url)) {           /* l'altro si è trasferito: il link lo segue */
            var a = el.querySelector("a[rel~='contact']");
            if (a && web(res.url)) a.href = web(res.url);
          }
          var label = el.querySelector("[data-flp-label]");
          if (label) label.textContent = str(basics.label, 160);
          var img = el.querySelector("[data-flp-image]");
          var src = safeImage(basics.image);
          if (img && src) {
            var pic = document.createElement("img");
            pic.className = img.className; pic.alt = ""; pic.loading = "lazy"; pic.src = src;
            img.parentNode.replaceChild(pic, img);
          }
          var back = arr(p.flp && p.flp.connections).some(function (c) { return addresses.indexOf(norm(c.url)) >= 0; });
          if (back) el.classList.add("flp-mutual");
          var status = el.querySelector("[data-flp-status]");
          if (status) status.textContent = back ? txtMutual : txtOneWay;
        }).catch(function () { /* il sito non espone un profilo leggibile: resta un semplice link */ });
      });
    });
  }

  /* ---------- vetrina: disegna un profilo che vive altrove ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function anchor(href, text, cls, rel) {
    var a = el("a", cls, text); a.href = href; if (rel) a.rel = rel; return a;
  }
  function paragraphs(text, into) {
    str(text).split(/\n\s*\n/).forEach(function (p) { if (p.trim()) into.appendChild(el("p", "", p.trim())); });
    return into;
  }
  function join(parts, sep) { return parts.filter(Boolean).join(sep || " · "); }
  function date(v, t) {
    v = str(v, 40).trim();
    var m = /^(\d{4})-(\d{2})(-\d{2})?$/.exec(v);
    return m && +m[2] >= 1 && +m[2] <= 12 ? t.months[+m[2] - 1] + " " + m[1] : v;
  }
  function period(a, b, t, open) {
    a = date(a, t); b = date(b, t);
    return a && (b || open) ? a + " – " + (b || t.present) : (a || b);
  }
  function item(title, url, role, meta, desc, logo) {
    var box = el("div", "flp-item");
    if (logo !== undefined) { var l = el("div", "flp-logo", str(logo, 80).trim().charAt(0).toUpperCase()); l.setAttribute("aria-hidden", "true"); box.appendChild(l); }
    var body = el("div", "flp-body"), h = el("h3");
    if (web(url)) h.appendChild(anchor(web(url), str(title, 300))); else h.textContent = str(title, 300);
    body.appendChild(h);
    if (role) body.appendChild(el("p", "flp-r", role));
    (meta || []).forEach(function (m) { if (m) body.appendChild(el("p", "flp-q", m)); });
    if (desc) body.appendChild(paragraphs(desc, el("div", "flp-d")));
    box.appendChild(body);
    return box;
  }
  function section(title, nodes) {
    if (!nodes.length) return null;
    var s = el("section", "flp-card flp-pad");
    s.setAttribute("aria-label", title);
    s.appendChild(el("h2", "", title));
    nodes.forEach(function (n) { s.appendChild(n); });
    return s;
  }
  function add(col, node) { if (node) col.appendChild(node); }

  function render(root, p, origin) {
    var basics = p.basics || {}, flp = p.flp || {};
    var lang = TXT[flp.lang] ? flp.lang : (TXT[root.getAttribute("data-flp-lang")] ? root.getAttribute("data-flp-lang") : "it");
    var t = TXT[lang];
    var name = str(basics.name, 200), label = str(basics.label, 300);
    var loc = basics.location || {};
    var where = join([str(loc.city, 100), str(loc.region, 100)], ", ");
    var mailto = mail(basics.email);
    var follow = web(flp.follow) || web(flp.feed);
    var main = el("div", "flp-col"), side = el("aside", "flp-col");

    var head = el("section", "flp-card h-card");
    head.setAttribute("aria-label", name);
    var cover = el("div", "flp-cover");
    if (safeImage(flp.cover)) cover.style.backgroundImage = 'url("' + encodeURI(safeImage(flp.cover)) + '")';
    head.appendChild(cover);
    var hd = el("div", "flp-head");
    if (safeImage(basics.image)) {
      var pic = el("img", "flp-avatar u-photo"); pic.src = safeImage(basics.image); pic.alt = name; hd.appendChild(pic);
    } else {
      var ini = el("div", "flp-avatar flp-initial", name.trim().charAt(0).toUpperCase()); ini.setAttribute("aria-hidden", "true"); hd.appendChild(ini);
    }
    hd.appendChild(el("h1", "p-name", name));
    if (label) hd.appendChild(el("p", "flp-label p-job-title", label));
    if (where || mailto) {
      var w = el("p", "flp-where");
      if (where) w.appendChild(el("span", "p-locality", where));
      if (where && mailto) w.appendChild(document.createTextNode(" · "));
      if (mailto) w.appendChild(anchor(mailto, t.contact_info));
      hd.appendChild(w);
    }
    var actions = el("div", "flp-actions");
    if (follow) actions.appendChild(anchor(follow, t.follow, "flp-btn flp-full"));
    if (mailto) actions.appendChild(anchor(mailto, t.contact, "flp-btn u-email" + (follow ? "" : " flp-full")));
    if (web(basics.url)) actions.appendChild(anchor(web(basics.url), web(basics.url).replace(/^https?:\/\/(www\.)?|\/$/g, ""), "flp-btn u-url"));
    if (actions.childNodes.length) hd.appendChild(actions);
    head.appendChild(hd);
    main.appendChild(head);

    if (str(basics.summary)) {
      var about = el("section", "flp-card flp-pad");
      about.setAttribute("aria-label", t.about);
      about.appendChild(el("h2", "", t.about));
      about.appendChild(paragraphs(basics.summary, el("div", "flp-about p-note")));
      main.appendChild(about);
    }
    add(main, section(t.work, arr(p.work).map(function (x) {
      return item(x.position, "", str(x.name, 300), [period(x.startDate, x.endDate, t, true), str(x.location, 200)], x.summary, str(x.name)); })));
    add(main, section(t.education, arr(p.education).map(function (x) {
      return item(x.institution, x.url, join([str(x.studyType, 200), str(x.area, 200)], ", "), [period(x.startDate, x.endDate, t)], x.summary, str(x.institution)); })));
    add(main, section(t.patents, arr(p.patents).map(function (x) {
      return item(x.name, x.url, "", [join([str(x.office, 200), str(x.number, 100), date(x.date, t)])], x.summary); })));
    add(main, section(t.publications, arr(p.publications).map(function (x) {
      return item(x.name, x.url, "", [join([str(x.publisher, 200), date(x.releaseDate, t)])], x.summary); })));
    add(main, section(t.projects, arr(p.projects).map(function (x) {
      return item(x.name, x.url, "", [period(x.startDate, x.endDate, t)], x.description); })));
    add(main, section(t.certificates, arr(p.certificates).map(function (x) {
      return item(x.name, x.url, str(x.issuer, 200), [date(x.date, t)], "", str(x.issuer) || str(x.name)); })));
    add(main, section(t.awards, arr(p.awards).map(function (x) {
      return item(x.title, "", "", [join([str(x.awarder, 200), date(x.date, t)])], x.summary); })));
    add(main, section(t.volunteer, arr(p.volunteer).map(function (x) {
      return item(x.position, x.url, str(x.organization, 200), [period(x.startDate, x.endDate, t, true)], x.summary, str(x.organization)); })));
    var skills = arr(p.skills).map(function (s) { return str(s.name, 100); }).filter(Boolean);
    if (skills.length) {
      var pills = el("div", "flp-pills");
      skills.forEach(function (s) { pills.appendChild(el("span", "", s)); });
      add(main, section(t.skills, [pills]));
    }
    add(main, section(t.languages, arr(p.languages).map(function (x) { return item(x.language, "", "", [str(x.fluency, 100)]); })));

    /* dichiarazione dell'originale */
    var note = el("section", "flp-card flp-pad flp-notice");
    note.appendChild(el("h2", "", t.original));
    note.appendChild(anchor(web(origin), web(origin).replace(/^https?:\/\/(www\.)?/, ""), "", "canonical"));
    side.appendChild(note);

    add(side, section(t.connections, arr(flp.connections).filter(function (c) { return web(c.url); }).map(function (c) {
      var box = el("div", "flp-item");
      box.setAttribute("data-flp-connection", web(c.url));
      if (web(c.json)) box.setAttribute("data-flp-json", web(c.json));
      var lg = el("div", "flp-logo", str(c.name, 80).trim().charAt(0).toUpperCase());
      lg.setAttribute("data-flp-image", ""); lg.setAttribute("aria-hidden", "true");
      var body = el("div", "flp-body"), h = el("h3");
      h.appendChild(anchor(web(c.url), str(c.name, 200) || web(c.url), "", "contact"));
      var lb = el("p", "flp-q"); lb.setAttribute("data-flp-label", "");
      var st = el("p", "flp-status"); st.setAttribute("data-flp-status", "");
      body.appendChild(h); body.appendChild(lb); body.appendChild(st);
      box.appendChild(lg); box.appendChild(body);
      return box;
    })));
    var others = arr(basics.profiles).filter(function (x) { return web(x.url); });
    if (others.length) {
      var nav = el("nav", "flp-list");
      others.forEach(function (x) { nav.appendChild(anchor(web(x.url), str(x.network, 100) || web(x.url))); });
      add(side, section(t.profiles, [nav]));
    }

    while (root.firstChild) root.removeChild(root.firstChild);
    root.appendChild(main); root.appendChild(side);
    root.setAttribute("data-flp-profile", web(origin));
    root.setAttribute("data-flp-text-mutual", t.mutual);
    root.setAttribute("data-flp-text-oneway", t.oneway);
    if (name) document.title = name + (label ? " — " + label : "");
    var canon = document.querySelector('link[rel="canonical"]');
    if (canon && web(origin)) canon.href = web(origin);
  }

  function showcase(root) {
    var url = root.getAttribute("data-flp-showcase");
    load(url).then(function (res) {
      render(root, res.profile, res.url);
      connections(root);
    }).catch(function () {
      var wait = root.querySelector("[data-flp-wait]");
      var lang = TXT[root.getAttribute("data-flp-lang")] ? root.getAttribute("data-flp-lang") : "it";
      if (wait) wait.textContent = TXT[lang].unreachable;
    });
  }

  var vetrina = document.querySelector("[data-flp-showcase]");
  if (vetrina) { showcase(vetrina); return; }
  var root = document.querySelector("[data-flp-profile]");
  if (root) connections(root);
})();
