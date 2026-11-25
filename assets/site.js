/* Quran Online Tarteel - site script (menu, forms, WhatsApp, tracking) */
(function () {
  var LEAD_EMAIL = "rehanabashir6543@gmail.com";
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/" + LEAD_EMAIL;
  var LEADS_ENDPOINT = "https://script.google.com/macros/s/AKfycbx78kWzrSTfShYs0jTbOocbTC3xK93Ov410mH3ge2UFL6wYAbVO-0-Pk0_cJfUxXco/exec"; /* Google Apps Script in hangul522@gmail.com: emails the lead + saves it to a Google Sheet */
  var WA_NUMBER = "923345259952";
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

  /* ---- WhatsApp country code picker (required) ---- */
  var CC = [["AF","Afghanistan",93],["AL","Albania",355],["DZ","Algeria",213],["AS","American Samoa",1],["AD","Andorra",376],["AO","Angola",244],["AI","Anguilla",1],["AG","Antigua and Barbuda",1],["AR","Argentina",54],["AM","Armenia",374],["AW","Aruba",297],["AU","Australia",61],["AT","Austria",43],["AZ","Azerbaijan",994],["BS","Bahamas",1],["BH","Bahrain",973],["BD","Bangladesh",880],["BB","Barbados",1],["BY","Belarus",375],["BE","Belgium",32],["BZ","Belize",501],["BJ","Benin",229],["BM","Bermuda",1],["BT","Bhutan",975],["BO","Bolivia",591],["BQ","Bonaire, Sint Eustatius and Saba",599],["BA","Bosnia and Herzegovina",387],["BW","Botswana",267],["BR","Brazil",55],["IO","British Indian Ocean Territory",246],["BN","Brunei",673],["BG","Bulgaria",359],["BF","Burkina Faso",226],["BI","Burundi",257],["CV","Cabo Verde",238],["KH","Cambodia",855],["CM","Cameroon",237],["CA","Canada",1],["KY","Cayman Islands",1],["CF","Central African Republic",236],["TD","Chad",235],["CL","Chile",56],["CN","China",86],["CX","Christmas Island",61],["CC","Cocos (Keeling) Islands",61],["CO","Colombia",57],["KM","Comoros",269],["CG","Congo",242],["CK","Cook Islands",682],["CR","Costa Rica",506],["HR","Croatia",385],["CU","Cuba",53],["CW","Curaçao",599],["CY","Cyprus",357],["CZ","Czechia",420],["CI","Côte d'Ivoire",225],["CD","DR Congo",243],["DK","Denmark",45],["DJ","Djibouti",253],["DM","Dominica",1],["DO","Dominican Republic",1],["EC","Ecuador",593],["EG","Egypt",20],["SV","El Salvador",503],["GQ","Equatorial Guinea",240],["ER","Eritrea",291],["EE","Estonia",372],["SZ","Eswatini",268],["ET","Ethiopia",251],["FK","Falkland Islands (Malvinas)",500],["FO","Faroe Islands",298],["FJ","Fiji",679],["FI","Finland",358],["FR","France",33],["GF","French Guiana",594],["PF","French Polynesia",689],["GA","Gabon",241],["GM","Gambia",220],["GE","Georgia",995],["DE","Germany",49],["GH","Ghana",233],["GI","Gibraltar",350],["GR","Greece",30],["GL","Greenland",299],["GD","Grenada",1],["GP","Guadeloupe",590],["GU","Guam",1],["GT","Guatemala",502],["GG","Guernsey",44],["GN","Guinea",224],["GW","Guinea-Bissau",245],["GY","Guyana",592],["HT","Haiti",509],["VA","Holy See (Vatican City State)",39],["HN","Honduras",504],["HK","Hong Kong",852],["HU","Hungary",36],["IS","Iceland",354],["IN","India",91],["ID","Indonesia",62],["IR","Iran",98],["IQ","Iraq",964],["IE","Ireland",353],["IM","Isle of Man",44],["IL","Israel",972],["IT","Italy",39],["JM","Jamaica",1],["JP","Japan",81],["JE","Jersey",44],["JO","Jordan",962],["KZ","Kazakhstan",7],["KE","Kenya",254],["KI","Kiribati",686],["KW","Kuwait",965],["KG","Kyrgyzstan",996],["LA","Laos",856],["LV","Latvia",371],["LB","Lebanon",961],["LS","Lesotho",266],["LR","Liberia",231],["LY","Libya",218],["LI","Liechtenstein",423],["LT","Lithuania",370],["LU","Luxembourg",352],["MO","Macao",853],["MG","Madagascar",261],["MW","Malawi",265],["MY","Malaysia",60],["MV","Maldives",960],["ML","Mali",223],["MT","Malta",356],["MH","Marshall Islands",692],["MQ","Martinique",596],["MR","Mauritania",222],["MU","Mauritius",230],["YT","Mayotte",262],["MX","Mexico",52],["FM","Micronesia",691],["MD","Moldova",373],["MC","Monaco",377],["MN","Mongolia",976],["ME","Montenegro",382],["MS","Montserrat",1],["MA","Morocco",212],["MZ","Mozambique",258],["MM","Myanmar",95],["NA","Namibia",264],["NR","Nauru",674],["NP","Nepal",977],["NL","Netherlands",31],["NC","New Caledonia",687],["NZ","New Zealand",64],["NI","Nicaragua",505],["NE","Niger",227],["NG","Nigeria",234],["NU","Niue",683],["NF","Norfolk Island",672],["KP","North Korea",850],["MK","North Macedonia",389],["MP","Northern Mariana Islands",1],["NO","Norway",47],["OM","Oman",968],["PK","Pakistan",92],["PW","Palau",680],["PS","Palestine",970],["PA","Panama",507],["PG","Papua New Guinea",675],["PY","Paraguay",595],["PE","Peru",51],["PH","Philippines",63],["PL","Poland",48],["PT","Portugal",351],["PR","Puerto Rico",1],["QA","Qatar",974],["RO","Romania",40],["RU","Russia",7],["RW","Rwanda",250],["RE","Réunion",262],["BL","Saint Barthélemy",590],["SH","Saint Helena, Ascension and Tristan da Cunha",290],["KN","Saint Kitts and Nevis",1],["LC","Saint Lucia",1],["MF","Saint Martin (French part)",590],["PM","Saint Pierre and Miquelon",508],["VC","Saint Vincent and the Grenadines",1],["WS","Samoa",685],["SM","San Marino",378],["ST","Sao Tome and Principe",239],["SA","Saudi Arabia",966],["SN","Senegal",221],["RS","Serbia",381],["SC","Seychelles",248],["SL","Sierra Leone",232],["SG","Singapore",65],["SX","Sint Maarten (Dutch part)",1],["SK","Slovakia",421],["SI","Slovenia",386],["SB","Solomon Islands",677],["SO","Somalia",252],["ZA","South Africa",27],["KR","South Korea",82],["SS","South Sudan",211],["ES","Spain",34],["LK","Sri Lanka",94],["SD","Sudan",249],["SR","Suriname",597],["SJ","Svalbard and Jan Mayen",47],["SE","Sweden",46],["CH","Switzerland",41],["SY","Syria",963],["TW","Taiwan",886],["TJ","Tajikistan",992],["TZ","Tanzania",255],["TH","Thailand",66],["TL","Timor-Leste",670],["TG","Togo",228],["TK","Tokelau",690],["TO","Tonga",676],["TT","Trinidad and Tobago",1],["TN","Tunisia",216],["TR","Turkey",90],["TM","Turkmenistan",993],["TC","Turks and Caicos Islands",1],["TV","Tuvalu",688],["AE","UAE",971],["UG","Uganda",256],["UA","Ukraine",380],["GB","United Kingdom",44],["US","United States",1],["UY","Uruguay",598],["UZ","Uzbekistan",998],["VU","Vanuatu",678],["VE","Venezuela",58],["VN","Vietnam",84],["VG","Virgin Islands, British",1],["VI","Virgin Islands, U.S.",1],["WF","Wallis and Futuna",681],["EH","Western Sahara",212],["YE","Yemen",967],["ZM","Zambia",260],["ZW","Zimbabwe",263],["AX","Åland Islands",358]];
  var CC_TOP = ["US","GB","CA","AU","NZ","IE","ZA","AE","SA","QA","KW","OM","BH","PH","PK"];
  var CC_BY = {}; CC.forEach(function (c) { CC_BY[c[0]] = c; });
  var CC_NAME = {"United States":"US","United Kingdom":"GB","Canada":"CA","Australia":"AU","New Zealand":"NZ","Ireland":"IE","South Africa":"ZA","UAE":"AE","Saudi Arabia":"SA","Qatar":"QA","Kuwait":"KW","Oman":"OM","Bahrain":"BH","Philippines":"PH","Pakistan":"PK"};
  function ccImg(r) { var i = document.createElement("img"); i.src = "/assets/flags/" + r.toLowerCase() + ".svg"; i.alt = ""; i.width = 20; i.height = 15; i.loading = "lazy"; i.decoding = "async"; i.className = "cc-flag"; return i; }
  function ccGuess() {
    var tz = ""; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
    var m = {"Asia/Karachi":"PK","Asia/Dubai":"AE","Asia/Riyadh":"SA","Asia/Qatar":"QA","Asia/Kuwait":"KW","Asia/Muscat":"OM","Asia/Bahrain":"BH","Asia/Manila":"PH","Europe/London":"GB","Europe/Dublin":"IE","Africa/Johannesburg":"ZA","Pacific/Auckland":"NZ"};
    if (m[tz]) return m[tz];
    if (/^Australia\//.test(tz)) return "AU";
    if (/^America\/(Toronto|Vancouver|Edmonton|Winnipeg|Halifax|Regina|St_Johns|Moncton|Montreal)$/.test(tz)) return "CA";
    if (/^(America\/(New_York|Chicago|Denver|Los_Angeles|Phoenix|Detroit|Anchorage|Indiana|Kentucky|Boise)|Pacific\/Honolulu)/.test(tz)) return "US";
    return "";
  }
  var ccOpen = null;
  document.addEventListener("click", function (e) { if (ccOpen && !ccOpen.contains(e.target)) ccOpen.classList.remove("open"), ccOpen = null; });
  document.querySelectorAll('form input[name="whatsapp"]').forEach(function (inp) {
    var form = inp.form;
    var sel = document.createElement("select");
    sel.name = "country_code"; sel.required = true; sel.className = "cc-native"; sel.tabIndex = -1; sel.setAttribute("aria-hidden", "true");
    var ph = document.createElement("option"); ph.value = ""; sel.appendChild(ph);
    CC.forEach(function (c) { var o = document.createElement("option"); o.value = c[0]; sel.appendChild(o); });
    var box = document.createElement("div"); box.className = "cc";
    var btn = document.createElement("button"); btn.type = "button"; btn.className = "cc-btn"; btn.setAttribute("aria-haspopup", "listbox"); btn.setAttribute("aria-label", "Country code");
    var panel = document.createElement("div"); panel.className = "cc-panel";
    var search = document.createElement("input"); search.type = "search"; search.className = "cc-search"; search.placeholder = "Search country or code"; search.setAttribute("aria-label", "Search country or code"); search.autocomplete = "off";
    var list = document.createElement("ul"); list.className = "cc-list"; list.setAttribute("role", "listbox");
    function item(c, top) {
      var li = document.createElement("li"); li.setAttribute("role", "option"); li.dataset.r = c[0];
      li.dataset.k = (c[1] + " +" + c[2] + " " + c[0]).toLowerCase();
      li.appendChild(ccImg(c[0]));
      var nm = document.createElement("span"); nm.className = "cc-name"; nm.textContent = c[1]; li.appendChild(nm);
      var cd = document.createElement("span"); cd.className = "cc-code"; cd.textContent = "+" + c[2]; li.appendChild(cd);
      if (top) li.className = "cc-top";
      li.addEventListener("click", function () { pick(c[0]); close(); btn.focus(); });
      return li;
    }
    CC_TOP.forEach(function (r) { if (CC_BY[r]) list.appendChild(item(CC_BY[r], true)); });
    var sep = document.createElement("li"); sep.className = "cc-sep"; sep.setAttribute("aria-hidden", "true"); list.appendChild(sep);
    CC.forEach(function (c) { list.appendChild(item(c, false)); });
    panel.appendChild(search); panel.appendChild(list);
    function pick(r) {
      sel.value = r || "";
      btn.innerHTML = "";
      if (r && CC_BY[r]) { btn.appendChild(ccImg(r)); var t = document.createElement("span"); t.textContent = "+" + CC_BY[r][2]; btn.appendChild(t); }
      else { var p = document.createElement("span"); p.className = "cc-ph"; p.textContent = "Code"; btn.appendChild(p); }
      btn.style.borderColor = "";
    }
    function close() { box.classList.remove("open"); if (ccOpen === box) ccOpen = null; }
    function filter() {
      var q = search.value.trim().toLowerCase().replace(/^00/, "+");
      list.querySelectorAll("li").forEach(function (li) {
        if (li.className === "cc-sep") { li.style.display = q ? "none" : ""; return; }
        li.style.display = !q ? "" : (li.classList.contains("cc-top") ? "none" : (li.dataset.k.indexOf(q) > -1 ? "" : "none"));
      });
    }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (box.classList.contains("open")) { close(); return; }
      if (ccOpen) ccOpen.classList.remove("open");
      box.classList.add("open"); ccOpen = box; search.value = ""; filter(); list.scrollTop = 0;
      if (window.matchMedia("(hover:hover)").matches) search.focus();
    });
    search.addEventListener("input", filter);
    search.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(); btn.focus(); }
      if (e.key === "Enter") { e.preventDefault(); var f = [].find.call(list.querySelectorAll("li[data-r]"), function (li) { return li.style.display !== "none"; }); if (f) { pick(f.dataset.r); close(); btn.focus(); } }
    });
    box.appendChild(btn); box.appendChild(panel); box.appendChild(sel);
    var wrap = document.createElement("div"); wrap.className = "phone-wrap";
    inp.parentNode.insertBefore(wrap, inp); wrap.appendChild(box); wrap.appendChild(inp);
    inp.placeholder = "Phone number";
    var csel = form && form.querySelector('[name="country"]');
    var pageC = document.querySelector('[name="country"] option[selected], input[type="hidden"][name="country"]');
    var pageCode = pageC && CC_NAME[pageC.value || pageC.textContent];
    pick((csel && CC_NAME[csel.value]) || pageCode || ccGuess());
    var touched = false;
    list.addEventListener("click", function () { touched = true; });
    if (csel) csel.addEventListener("change", function () { if (!touched && CC_NAME[csel.value]) pick(CC_NAME[csel.value]); });
    form._ccBtn = btn;
  });
  function fullPhone(form, raw) {
    var sel = form.querySelector('select[name="country_code"]');
    var c = sel && CC_BY[sel.value];
    raw = String(raw || "").trim();
    var digits = raw.replace(/\D/g, "");
    if (!c) return raw;
    var code = String(c[2]);
    if (/^(\+|00)/.test(raw)) { digits = digits.replace(/^00/, ""); if (digits.indexOf(code) === 0) digits = digits.slice(code.length); }
    digits = digits.replace(/^0+/, "");
    return "+" + code + " " + digits;
  }

  /* ---- lead forms -> email via FormSubmit ---- */
  document.querySelectorAll("[data-form]").forEach(function (card) {
    var form = card.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (f) {
        var v = String(f.value || "").trim();
        var bad = !v;
        if (!bad && f.type === "email") bad = !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
        if (!bad && f.name === "whatsapp") bad = v.replace(/\D/g, "").length < 6;
        f.style.borderColor = bad ? "#c0392b" : "";
        if (bad) ok = false;
      });
      if (form._ccBtn) form._ccBtn.style.borderColor = form.country_code && !form.country_code.value ? "#c0392b" : "";
      if (!ok) { var first = form.querySelector('[style*="c0392b"]:not(.cc-native)'); if (first) first.focus(); return; }
      if (form._honey && form._honey.value) return; /* spam bot */

      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "_honey") data[k] = v; });
      if (data.whatsapp) data.whatsapp = fullPhone(form, data.whatsapp);
      if (data.country_code && CC_BY[data.country_code]) data.country_code = "+" + CC_BY[data.country_code][2] + " (" + CC_BY[data.country_code][1] + ")";
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

      var waLines = ["Assalamu alaikum, I just filled the form on your website.", ""];
      [["name", "Name"], ["whatsapp", "WhatsApp"], ["email", "Email"], ["country", "Country"], ["student", "Who will learn"], ["course", "Course"], ["preferred_time", "Preferred time"], ["message", "Message"]].forEach(function (p) {
        if (data[p[0]]) waLines.push(p[1] + ": " + data[p[0]]);
      });
      var wa = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(waLines.join("\n"));
      function send(url, payload, plain) {
        return fetch(url, {
          method: "POST",
          headers: plain ? { "Content-Type": "text/plain;charset=utf-8" } : { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify(payload),
          redirect: "follow"
        })
          .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
          .then(function (res) { if (!res.ok || String(res.j.success) === "false") throw new Error("send failed"); });
      }
      function done(via) {
        track("generate_lead", { form_name: data.form_source || "form", course: data.course || "", heard_about: data.heard_about, page_path: location.pathname, sent_via: via });
        card.classList.add("sent");
      }
      send(LEADS_ENDPOINT, data, true)
        .then(function () { done("sheet"); })
        .catch(function () { return send(FORM_ENDPOINT, data).then(function () { done("formsubmit"); }); })
        .catch(function () {
          btn.disabled = false;
          btn.innerHTML = label;
          if (err) {
            err.innerHTML = 'Our form is busy right now. Please send your details on WhatsApp instead, they are already filled in for you.<a class="form-wa" target="_blank" rel="noopener" href="' + wa + '">Send my details on WhatsApp</a>';
            err.querySelector("a").addEventListener("click", function () { track("whatsapp_click", { link_location: "form-fallback", page_path: location.pathname }); track("generate_lead", { form_name: data.form_source || "form", course: data.course || "", page_path: location.pathname, sent_via: "whatsapp_fallback" }); });
            err.style.display = "block";
          }
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
