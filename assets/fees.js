/* Quran Online Tarteel - fee currency switcher (prices are already in the HTML; this only converts) */
(function () {
  var sw = document.querySelectorAll(".cur-switch");
  if (!sw.length) return;
  var cfg = JSON.parse(sw[0].getAttribute("data-fee-rates"));
  var SYM = { PKR: "Rs ", USD: "$", GBP: "£", CAD: "C$", AUD: "A$", AED: "AED " };
  function conv(pkr, cur) {
    if (cur === "PKR") return pkr;
    var o = cfg.ovr && cfg.ovr[cur];
    if (o && o[pkr] != null) return o[pkr];
    var st = cfg.step[cur];
    return Math.ceil(pkr / cfg.rates[cur] / st) * st;
  }
  function show(cur) {
    document.querySelectorAll(".fee[data-pkr]").forEach(function (e) {
      var v = conv(+e.getAttribute("data-pkr"), cur).toLocaleString("en-US"), sym = SYM[cur];
      if (/ $/.test(sym)) { e.innerHTML = '<span class="cs">' + sym.trim() + "</span> " + v; } else { e.textContent = sym + v; }
    });
    document.documentElement.classList.toggle("fees-pkr", cur === "PKR");
    document.querySelectorAll(".cur-switch button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-cur") === cur ? "true" : "false");
    });
  }
  var saved = null;
  try { saved = localStorage.getItem("qot-cur"); } catch (e) {}
  var locked = sw[0].hasAttribute("data-lock"); /* country pages always open in their own currency */
  var start = !locked && saved && SYM[saved] ? saved : sw[0].getAttribute("data-default");
  if (start !== sw[0].getAttribute("data-default") || start === "PKR") show(start);
  sw.forEach(function (s) {
    s.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-cur]");
      if (!b) return;
      var cur = b.getAttribute("data-cur");
      show(cur);
      if (!locked) { try { localStorage.setItem("qot-cur", cur); } catch (e) {} }
      if (typeof window.gtag === "function") window.gtag("event", "fee_currency", { currency: cur, page_path: location.pathname });
    });
  });
})();
