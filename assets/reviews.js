/* Quran Online Tarteel - reviews (shown as plain text only) */
(function () {
  var API = "/api/reviews";
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function stars(n) { return "★★★★★".slice(0, n) + "☆☆☆☆☆".slice(0, 5 - n); }
  function when(ms) { try { return new Date(ms).toLocaleDateString(undefined, { month: "short", year: "numeric" }); } catch (e) { return ""; } }

  var form = document.querySelector("[data-review-form]");
  var secs = document.querySelectorAll("[data-reviews]");
  if (!secs.length && !form) return;
  var max = 6; secs.forEach(function (s) { max = Math.max(max, +(s.getAttribute("data-limit") || 6)); });
  fetch(API + "?limit=" + max).then(function (r) { return r.json(); }).then(function (d) {
    if (form) setupForm(d && d.sitekey);
    if (!d || !d.count) return; /* nothing is shown until real reviews exist */
    secs.forEach(function (sec) {
      var grid = sec.querySelector(".rv-grid"), sum = sec.querySelector(".rv-sum"), lim = +(sec.getAttribute("data-limit") || 6);
      d.reviews.slice(0, lim).forEach(function (r) {
        var c = el("article", "rv-card");
        var s = el("div", "rv-stars", stars(r.stars)); s.setAttribute("aria-label", r.stars + " out of 5 stars"); c.appendChild(s);
        c.appendChild(el("p", "rv-body", "\u201c" + r.body + "\u201d"));
        var who = el("div", "rv-who");
        who.appendChild(el("b", null, r.name));
        who.appendChild(el("span", null, [r.who === "My child" ? "Parent" : (r.who === "Myself" ? "Student" : ""), r.course, r.country, when(r.created)].filter(Boolean).join(" \u00b7 ")));
        c.appendChild(who);
        grid.appendChild(c);
      });
      if (sum) sum.textContent = d.avg + " out of 5 from " + d.count + (d.count === 1 ? " family review" : " family reviews");
      sec.hidden = false;
    });
  }).catch(function () { if (form) setupForm(""); });
  if (!form) return;

  var tsToken = "";
  function setupForm(sitekey) {
    var box = form.querySelector(".rv-ts"), b = form.querySelector("button[type=submit]");
    if (!sitekey) { b.disabled = true; form.querySelector(".rv-msg").textContent = "Reviews are opening very soon, in sha Allah."; return; }
    window.qotTs = function () {
      window.turnstile.render(box, { sitekey: sitekey, theme: "light", callback: function (t) { tsToken = t; }, "expired-callback": function () { tsToken = ""; } });
    };
    var sc = document.createElement("script");
    sc.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=qotTs"; sc.async = true; sc.defer = true;
    document.head.appendChild(sc);
  }
  var msg = form.querySelector(".rv-msg"), btn = form.querySelector("button[type=submit]");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.turnstile = tsToken || data["cf-turnstile-response"] || "";
    if (!data.stars) { msg.textContent = "Please choose a star rating."; msg.className = "rv-msg bad"; return; }
    if (!data.name || data.name.trim().length < 2 || !data.review || data.review.trim().length < 20) { msg.textContent = "Please add your name and a few words (at least 20 letters)."; msg.className = "rv-msg bad"; return; }
    if (!data.turnstile) { msg.textContent = "Please complete the security check above."; msg.className = "rv-msg bad"; return; }
    btn.disabled = true; btn.textContent = "Sending...";
    var fail = function (t) { msg.textContent = t; msg.className = "rv-msg bad"; btn.disabled = false; btn.textContent = "Publish my review"; tsToken = ""; if (window.turnstile) window.turnstile.reset(); };
    fetch(API, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d.ok) return fail(d.error || "Sorry, something went wrong.");
        form.innerHTML = '<div class="rv-thanks"><b>JazakAllahu khayran!</b><span>Your review is now on our website. Thank you for helping other families.</span></div>';
        if (typeof window.gtag === "function") window.gtag("event", "review_submit", { stars: data.stars });
      })
      .catch(function () { fail("Sorry, your review did not send. Please try again."); });
  });
})();
