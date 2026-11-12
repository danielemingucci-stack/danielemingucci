/* Free Linkable Profile 0.1 — i profili si riconoscono tra loro, senza piattaforma.
   Per ogni collegamento della pagina: legge il profile.json dell'altro sito e controlla
   se anche lui collega questo profilo. Se sì, il collegamento è reciproco.
   Nessun dato viene inviato: sono solo letture di file pubblici. */
(function () {
  "use strict";
  function norm(u) {
    try {
      var x = new URL(u, location.href);
      return (x.host.replace(/^www\./, "") + x.pathname.replace(/index\.html$/, "").replace(/\/+$/, "")).toLowerCase();
    } catch (e) { return ""; }
  }
  function safeImage(u) {
    try { return new URL(u).protocol === "https:" ? u : ""; } catch (e) { return ""; }
  }
  var root = document.querySelector("[data-flp-profile]");
  if (!root) return;
  var me = norm(root.getAttribute("data-flp-profile"));
  var txtMutual = root.getAttribute("data-flp-text-mutual") || "Collegamento reciproco";
  var txtOneWay = root.getAttribute("data-flp-text-oneway") || "In attesa di conferma";

  Array.prototype.forEach.call(document.querySelectorAll("[data-flp-connection]"), function (el) {
    var url = el.getAttribute("data-flp-connection");
    var json = el.getAttribute("data-flp-json");
    if (!json) {
      try { json = new URL("profile.json", /\/$/.test(url) ? url : url + "/").href; } catch (e) { return; }
    }
    var status = el.querySelector("[data-flp-status]");
    fetch(json, { mode: "cors", credentials: "omit" })
      .then(function (r) { if (!r.ok) throw new Error("http"); return r.json(); })
      .then(function (p) {
        var basics = (p && p.basics) || {};
        var label = el.querySelector("[data-flp-label]");
        if (label && typeof basics.label === "string") label.textContent = basics.label.slice(0, 160);
        var img = el.querySelector("[data-flp-image]");
        var src = typeof basics.image === "string" ? safeImage(basics.image) : "";
        if (img && src) {
          var pic = document.createElement("img");
          pic.className = img.className; pic.alt = ""; pic.loading = "lazy"; pic.src = src;
          img.parentNode.replaceChild(pic, img);
        }
        var list = (p && p.flp && Array.isArray(p.flp.connections)) ? p.flp.connections : [];
        var back = list.some(function (c) { return c && norm(c.url) === me; });
        if (back) el.classList.add("flp-mutual");
        if (status) status.textContent = back ? txtMutual : txtOneWay;
      })
      .catch(function () { /* il sito non espone un profilo leggibile: resta un semplice link */ });
  });
})();
