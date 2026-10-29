/* Quran Online Tarteel - site script (menu, forms, WhatsApp, tracking) */
(function () {
  var LEAD_EMAIL = "rehanabashir6543@gmail.com";
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/" + LEAD_EMAIL;
  var WA_NUMBER = "923350548488";
  var WA_DEFAULT = "Assalamu alaikum, I would like to know more about your online Quran classes.";

  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }

  /* ---- header menu ---- */
  var head = document.getElementById("qotHead");
  var burger = document.getElementById("qotBurger");
  if (head && burger) {
    burger.addEventListener("click", function () {
      var open = head.classList.toggle("qot-open");
      burger.setAttribute("aria-expanded", open);
    });
    document.querySelectorAll("#qotMenu a").forEach(function (a) {
      a.addEventListener("click", function () {
        if (a.hasAttribute("data-courses") && window.innerWidth <= 1024) return;
        head.classList.remove("qot-open");
        burger.setAttribute("aria-expanded", false);
      });
    });
    var key = document.body.getAttribute("data-nav");
    var cur = key && document.querySelector('#qotMenu a[data-nav="' + key + '"]');
    if (cur) cur.classList.add("active");
  }

  /* ---- WhatsApp links: open chat with a ready message ---- */
  document.querySelectorAll("a[data-wa]").forEach(function (a) {
    var msg = a.getAttribute("data-wa") || WA_DEFAULT;
    a.href = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg);
    a.target = "_blank";
    a.rel = "noopener";
    a.addEventListener("click", function () {
      track("whatsapp_click", { link_location: a.getAttribute("data-wa-loc") || "page", page_path: location.pathname });
    });
  });

  /* ---- "How did you hear about us?": pick an option OR type one (required) ---- */
  document.querySelectorAll(".heard").forEach(function (box) {
    var sel = box.querySelector("select");
    var txt = box.querySelector(".heard-other");
    if (!sel || !txt) return;
    var msg = document.createElement("div");
    msg.className = "heard-msg"; msg.setAttribute("role", "alert");
    msg.textContent = "Please choose an option or type where you heard about us.";
    box.appendChild(msg);
    function clear() { box.classList.remove("bad"); sel.style.borderColor = ""; txt.style.borderColor = ""; }
    sel.addEventListener("change", function () { if (sel.value) txt.value = ""; clear(); });
    txt.addEventListener("input", function () { if (txt.value.trim()) sel.value = ""; clear(); });
  });

  /* ---- lead forms -> email via FormSubmit ---- */
  document.querySelectorAll("[data-form]").forEach(function (card) {
    var form = card.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (f) {
        var bad = !String(f.value || "").trim();
        f.style.borderColor = bad ? "#c0392b" : "";
        if (bad) ok = false;
      });
      var hb = form.querySelector(".heard");
      if (hb) {
        var hs = hb.querySelector("select"), ht = hb.querySelector(".heard-other");
        if (!hs.value && !String(ht.value || "").trim()) {
          hb.classList.add("bad"); hs.style.borderColor = "#c0392b"; ht.style.borderColor = "#c0392b";
          ok = false;
        }
      }
      if (!ok) { var first = form.querySelector('[style*="c0392b"]'); if (first) first.focus(); return; }
      if (form._honey && form._honey.value) return; /* spam bot */

      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "_honey") data[k] = v; });
      var other = String(data.heard_other || "").trim().slice(0, 80);
      delete data.heard_other;
      data.heard_about = data.heard_about || "Other: " + other;
      data.page = location.href;
      data._subject = "New lead: " + (data.form_source || "Website form") + " - Quran Online Tarteel";
      data._template = "table";
      data._captcha = "false"; data._cc = "zainulabideen4356@gmail.com"; /* copy of every lead, never shown on the site */

      var btn = form.querySelector("button[type=submit]");
      var label = btn.innerHTML;
      btn.disabled = true;
      btn.textContent = "Sending...";
      var err = card.querySelector(".form-error");
      if (err) err.style.display = "none";

      fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok || String(res.j.success) === "false") throw new Error("send failed");
          track("generate_lead", { form_name: data.form_source || "form", course: data.course || "", heard_about: data.heard_about, page_path: location.pathname });
          card.classList.add("sent");
        })
        .catch(function () {
          btn.disabled = false;
          btn.innerHTML = label;
          if (err) err.style.display = "block";
        });
    });
  });

  /* since-2010 ribbon: keep the years current + sit just under the header */
  var now = new Date().getFullYear();
  document.querySelectorAll("[data-yr-now]").forEach(function (e) { e.textContent = now; });
  document.querySelectorAll("[data-yr-count]").forEach(function (e) { e.textContent = now - 2010; });
  if (head) {
    var setH = function () { document.documentElement.style.setProperty("--qot-head-h", head.offsetHeight + "px"); };
    setH(); window.addEventListener("resize", setH);
  }

  /* duas library: copy a dua (Arabic + transliteration + meaning) */
  document.querySelectorAll(".dua-copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var card = document.getElementById(b.getAttribute("data-copy"));
      if (!card) return;
      var parts = [card.querySelector("h2"), card.querySelector(".dua-ar"), card.querySelector(".dua-tr"), card.querySelector(".dua-mean")]
        .filter(Boolean).map(function (e) { return e.innerText.trim(); });
      var text = parts.join("\n\n") + "\n\n" + location.href.split("#")[0] + "#" + card.id;
      var done = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy dua"; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {}); 
      track("dua_copy", { dua: card.id, page_path: location.pathname });
    });
  });

  document.querySelectorAll("a[data-track]").forEach(function (a) {
    a.addEventListener("click", function () { track(a.getAttribute("data-track"), { page_path: location.pathname }); });
  });

  /* duas pages: one dua at a time with a numbered navigator (all duas stay in the HTML for Google) */
  var lay = document.querySelector(".dua-layout");
  if (lay) {
    var cards = [].slice.call(lay.querySelectorAll(".dua"));
    var links = [].slice.call(lay.querySelectorAll(".dua-nav a"));
    var pager = lay.querySelector(".dua-pager"), pos = lay.querySelector(".dp-pos");
    var prev = lay.querySelector(".dp-prev"), next = lay.querySelector(".dp-next"), all = lay.querySelector(".dn-all");
    var cur = 0;
    var show = function (i, scroll, user) {
      cur = Math.max(0, Math.min(cards.length - 1, i));
      cards.forEach(function (c, k) { c.classList.toggle("on", k === cur); });
      links.forEach(function (a, k) { a.classList.toggle("on", k === cur); if (k === cur) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      pos.textContent = (cur + 1) + " of " + cards.length;
      prev.disabled = cur === 0; next.disabled = cur === cards.length - 1;
      var act = links[cur];
      if (act && window.innerWidth <= 900) { /* centre the active number in the strip without moving the page */
        var strip = act.parentNode; while (strip && strip !== lay && strip.scrollWidth <= strip.clientWidth) strip = strip.parentNode;
        if (strip && strip !== lay) strip.scrollLeft = act.offsetLeft - (strip.clientWidth - act.offsetWidth) / 2;
      }
      if (scroll) { var top = lay.getBoundingClientRect().top + window.pageYOffset - (window.innerWidth <= 900 ? 150 : 100); window.scrollTo({ top: top, behavior: "smooth" }); }
      if (user && history.replaceState) history.replaceState(null, "", "#" + cards[cur].id);
    };
    lay.classList.add("paged"); pager.hidden = false;
    links.forEach(function (a, k) { a.addEventListener("click", function (e) { if (!lay.classList.contains("paged")) return; e.preventDefault(); show(k, true, true); }); });
    prev.addEventListener("click", function () { show(cur - 1, true, true); });
    next.addEventListener("click", function () { show(cur + 1, true, true); });
    all.addEventListener("click", function () {
      var paged = lay.classList.toggle("paged"); pager.hidden = !paged;
      all.textContent = paged ? "View all on one page" : "Show one at a time"; all.setAttribute("aria-pressed", String(!paged));
    });
    var start = 0, h = location.hash.replace("#dua-", ""); if (/^\d+$/.test(h)) start = parseInt(h, 10) - 1;
    show(start, false);
  }

  /* duas library: topic tabs + search */
  var lib = document.querySelector(".lib-grid");
  if (lib) {
    var tiles = [].slice.call(lib.querySelectorAll(".lib-tile")), q = document.getElementById("libq"), cat = "all";
    var empty = document.querySelector(".lib-empty");
    var apply = function () {
      var term = (q && q.value || "").trim().toLowerCase(), n = 0;
      tiles.forEach(function (t) {
        var ok = (cat === "all" || (" " + t.getAttribute("data-cat") + " ").indexOf(" " + cat + " ") > -1) && (!term || t.getAttribute("data-kw").indexOf(term) > -1);
        t.hidden = !ok; if (ok) n++;
      });
      if (empty) empty.hidden = n > 0;
    };
    document.querySelectorAll(".lib-tab").forEach(function (b) {
      b.addEventListener("click", function () {
        cat = b.getAttribute("data-cat");
        document.querySelectorAll(".lib-tab").forEach(function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", String(x === b)); });
        apply();
      });
    });
    if (q) q.addEventListener("input", apply);
  }

  /* tasbih counter for step-by-step azkar (e.g. 33 + 33 + 33 + 1) */
  document.querySelectorAll(".dua-has-steps").forEach(function (card) {
    var steps = [].slice.call(card.querySelectorAll(".ds-step")), box = card.querySelector(".tasbih");
    if (!steps.length || !box) return;
    var tap = box.querySelector(".tb-tap"), num = box.querySelector(".tb-num"), of = box.querySelector(".tb-of"),
        lbl = box.querySelector(".tb-lbl"), stepTxt = box.querySelector(".tb-step"), reset = box.querySelector(".tb-reset");
    var si = 0, n = 0;
    var render = function () {
      steps.forEach(function (s, k) { s.classList.toggle("on", k === si); s.classList.toggle("done", k < si); });
      if (si >= steps.length) { num.textContent = "\u2713"; of.textContent = ""; lbl.textContent = "Completed, masha'Allah"; stepTxt.textContent = "All done"; tap.disabled = true; return; }
      var t = +steps[si].getAttribute("data-target");
      num.textContent = n; of.textContent = "of " + t; lbl.textContent = "Tap to count"; tap.disabled = false;
      stepTxt.textContent = "Step " + (si + 1) + " of " + steps.length;
    };
    tap.addEventListener("click", function () {
      var t = +steps[si].getAttribute("data-target");
      n++; if (navigator.vibrate) navigator.vibrate(12);
      if (n >= t) { si++; n = 0; }
      render();
    });
    reset.addEventListener("click", function () { si = 0; n = 0; render(); });
    box.hidden = false; render();
  });

  var y = document.getElementById("qotYear");
  if (y) y.textContent = new Date().getFullYear();
})();
