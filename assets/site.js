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
      if (!ok) return;
      if (form._honey && form._honey.value) return; /* spam bot */

      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "_honey") data[k] = v; });
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
          track("generate_lead", { form_name: data.form_source || "form", course: data.course || "", page_path: location.pathname });
          card.classList.add("sent");
        })
        .catch(function () {
          btn.disabled = false;
          btn.innerHTML = label;
          if (err) err.style.display = "block";
        });
    });
  });

  var y = document.getElementById("qotYear");
  if (y) y.textContent = new Date().getFullYear();
})();
