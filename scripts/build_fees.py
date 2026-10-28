#!/usr/bin/env python3
"""Build every fee block on the site from data/fees.json.

Run from the repo root:  python3 scripts/build_fees.py
Change a price once in data/fees.json, run this, commit -> the whole site updates.
Blocks live between <!--FEES:...--> and <!--/FEES--> markers and are fully regenerated.
"""
import json, math, re, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "fees.json")))
RATES = {k: v for k, v in D["rates"].items() if k.isupper()}
STEP = D["round_step"]
DAYS = D["plans_days"]
C = {c["id"]: c for c in D["courses"]}
SYM = {"PKR": "Rs ", "USD": "$", "GBP": "£", "CAD": "C$", "AUD": "A$", "AED": "AED "}
CUR_ORDER = ["USD", "GBP", "CAD", "AUD", "AED", "PKR"]
CUR_LABEL = {"USD": "US $", "GBP": "UK £", "CAD": "CA $", "AUD": "AU $", "AED": "AED", "PKR": "PKR"}


def conv(pkr, cur):
    if cur == "PKR":
        return pkr
    step = STEP[cur]
    return int(math.ceil(pkr / RATES[cur] / step) * step)


def fmt(pkr, cur):
    v = conv(pkr, cur)
    return SYM[cur] + f"{v:,}"


def fmt_html(pkr, cur):
    v = f"{conv(pkr, cur):,}"
    sym = SYM[cur]
    return f'<span class="cs">{sym.strip()}</span> {v}' if sym.endswith(" ") else sym + v


def cell(pkr, cur):
    main = f'<span class="fee" data-pkr="{pkr}">{fmt_html(pkr, cur)}</span>'
    if cur == "PKR":
        return main
    return main


def switcher(cur, lock=False):
    rates = html.escape(json.dumps({"rates": RATES, "step": STEP}), quote=True)
    btns = "".join(
        f'<button type="button" data-cur="{c}" aria-pressed="{"true" if c == cur else "false"}">{CUR_LABEL[c]}</button>'
        for c in CUR_ORDER)
    lk = ' data-lock="1"' if lock else ""
    return (f'<div class="cur-switch" data-fee-rates="{rates}" data-default="{cur}"{lk}>'
            f'<span class="cur-label" id="curLbl">Show fees in</span>'
            f'<div class="cur-btns" role="group" aria-labelledby="curLbl">{btns}</div></div>')


def head_row(first):
    th = "".join((f'<th scope="col" class="pop"><em>Popular</em>{d} days<span>a week</span></th>' if d == 4 else f'<th scope="col">{d} days<span>a week</span></th>') for d in DAYS)
    return f'<thead><tr><th scope="col">{first}</th>{th}</tr></thead>'


def course_table(c, cur, title_tag="h3", link=True, prefix=""):
    rows = "".join(
        f'<tr><th scope="row">{mins} min<span>per class</span></th>'
        + "".join(f'<td>{cell(p, cur)}</td>' for p in prices) + "</tr>"
        for mins, prices in c["prices"].items())
    name = c["name"]
    if link and c.get("page") and os.path.exists(os.path.join(ROOT, c["page"], "index.html")):
        name = f'<a href="{prefix}{c["page"]}/">{name}</a>'
    return (f'<div class="fee-card"><{title_tag}><span class="fc-dot" aria-hidden="true"></span>{name}</{title_tag}>'
            f'<div class="fee-scroll"><table class="fee-table">{head_row("Class length")}<tbody>{rows}</tbody></table></div></div>')


def overview_table(ids, cur, prefix):
    rows = ""
    for cid in ids:
        c = C[cid]
        mins = "30" if "30" in c["prices"] else "45"
        nm = f'<a href="{prefix}{c["page"]}/">{c["name"]}</a>' if os.path.exists(os.path.join(ROOT, c["page"], "index.html")) else c["name"]
        rows += (f'<tr><th scope="row">{nm}<span>{mins} min classes</span></th>'
                 + "".join(f'<td>{cell(p, cur)}</td>' for p in c["prices"][mins]) + "</tr>")
    return (f'<div class="fee-card fee-card-wide"><div class="fee-scroll"><table class="fee-table">'
            f'{head_row("Course")}<tbody>{rows}</tbody></table></div></div>')


def note(prefix, cur):
    return '<p class="fee-note fee-disc"><span class="fd-ico" aria-hidden="true">&#10022;</span><b>Family discount:</b> more than one child, or a mother and child, learning with us? You get a special family discount. <a href="https://wa.me/923350548488" data-wa="Assalamu alaikum, more than one person in my family wants to learn. Please tell me about the family discount." data-wa-loc="fee-discount" class="in-link">Just ask us on WhatsApp</a>.</p>'


def section(inner, eyebrow, h2, sub, bg="bg-cream-2", sid="fees"):
    return (f'<section class="sec {bg} fee-sec" id="{sid}"><div class="container"><div class="section-head">'
            f'<span class="eyebrow">{eyebrow}</span><h2>{h2}</h2><p>{sub}</p></div>{inner}</div></section>')


def put(s, key, block, where):
    """Remove any old fee block, then insert it: where="hero" -> right after the hero section,
    where="section2" -> after the first section that follows the hero."""
    start, end = f"<!--FEES:{key}-->", "<!--/FEES-->"
    s = re.sub(re.escape(start) + r".*?" + re.escape(end), "", s, flags=re.S)
    h = s.index('<section class="page-hero')
    i = s.index("</section>", h) + len("</section>")
    if where == "section2":
        i = s.index("</section>", s.index("<section", i)) + len("</section>")
    return s[:i] + start + block + end + s[i:]


def hero_price(s, low, cur):
    """One line under the hero intro: From <price> a month - 2 free classes first."""
    s = re.sub(r"<!--FEEHERO-->.*?<!--/FEEHERO-->", "", s, flags=re.S)
    line = (f'<!--FEEHERO--><p class="hero-price"><span class="hp-from">From</span> <span class="fee" data-pkr="{low}">{fmt_html(low, cur)}</span>'
            f'<span class="hp-per"> a month</span><span class="hp-dot">&middot;</span><span class="hp-trial">2 free classes first</span></p><!--/FEEHERO-->')
    m = re.search(r'<p class="hero-lead">.*?</p>', s[s.index('<section class="page-hero'):], re.S)
    i = s.index('<section class="page-hero') + m.end()
    return s[:i] + line + s[i:]


# ---------- per-page configuration ----------
COURSE_PAGES = {
    "noorani-qaida-online": ["qaida"],
    "learn-quran-online-for-beginners": ["nazra"],
    "online-tajweed-classes": ["tajweed"],
    "online-hifz-program": ["hifz"],
    "quran-translation-tafseer-classes": ["tafseer"],
    "online-islamic-studies": ["islamic"],
    "juz-amma-memorization-online": ["juzamma"],
    "online-salah-classes": ["salah"],
    "online-duas-course": ["duas"],
    "40-hadith-for-kids": ["hadith40"],
    "quran-classes-for-new-muslims": ["newmuslim"],
}
AUDIENCE_PAGES = {
    "online-quran-classes-for-kids": (["qaida", "nazra", "tajweed", "hifz", "islamic", "juzamma", "salah", "duas", "hadith40"], "USD"),
    "online-quran-classes-for-women": (["qaida", "nazra", "tajweed", "hifz", "tafseer", "islamic", "salah", "duas", "newmuslim"], "USD"),
}
COUNTRY = {
    "online-quran-classes-usa": ("USD", "the USA", "US dollars"),
    "online-quran-classes-uk": ("GBP", "the UK", "pounds"),
    "online-quran-classes-canada": ("CAD", "Canada", "Canadian dollars"),
    "online-quran-classes-australia": ("AUD", "Australia", "Australian dollars"),
    "online-quran-classes-uae": ("AED", "the UAE", "dirhams"),
    "online-quran-classes-pakistan": ("PKR", "Pakistan", "rupees"),
}
OVERVIEW = ["qaida", "nazra", "tajweed", "hifz", "tafseer", "islamic", "juzamma", "salah", "duas", "hadith40", "newmuslim"]
ENROL = '<section class="cta-sec dark pattern-dark" id="enrol">'


def p2(cid, mins, i, cur):  # formatted single price
    return fmt(C[cid]["prices"][mins][i], cur)


def how_much_answer(cur, place=None):
    f = lambda cid, mins, i: fmt(C[cid]["prices"][mins][i], cur)
    where = f" in {place}" if place else ""
    return (f"Monthly fees{where} start at {f('qaida','30',0)} for Noorani Qaida, 2 days a week with 30 minute classes. "
            f"Quran reading (Nazra) is {f('nazra','30',0)} for 2 days, {f('nazra','30',1)} for 4 days and {f('nazra','30',2)} for 5 days a week. "
            + ("" if cur == "PKR" else "It is the same fair fee we charge in Pakistan, simply converted to your currency. ") +
            f"Every new student starts with 2 free classes, so you pay nothing until you decide to continue. See the full fees table for every course.")


def course_answer(cid, cur="USD"):
    c = C[cid]
    def line(cc):
        return "; ".join(f"{mins} minute classes are " + ", ".join(f"{fmt(p, cc)} for {d} days" for p, d in zip(pr, DAYS)) + " a week"
                         for mins, pr in c["prices"].items())
    return (f"{c['name']} fees are monthly, per student: {line(cur)}. In Pakistan, {line('PKR')}. "
            "The first 2 classes are free, and families with more than one student get a family discount.")


def set_faq(s, qname, answer, add_if_missing=False):
    """Set answer text for question `qname` in JSON-LD and visible FAQ. Optionally add the Q if missing."""
    esc = answer.replace('"', '\\"')
    pat = re.compile(r'("name": "' + re.escape(qname) + r'", "acceptedAnswer": \{"@type": "Answer", "text": ")[^"]*(")')
    if pat.search(s):
        s = pat.sub(lambda m: m.group(1) + esc + m.group(2), s, count=1)
        vpat = re.compile(r'(<h3>' + re.escape(qname) + r'</h3>.*?<div class="ans">).*?(</div>)', re.S)
        s = vpat.sub(lambda m: m.group(1) + answer_html(answer) + m.group(2), s, count=1)
    elif add_if_missing:
        s = s.replace('{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [',
                      '{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "'
                      + qname + '", "acceptedAnswer": {"@type": "Answer", "text": "' + esc + '"}}, ', 1)
        s = s.replace('<div class="faq-wrap">',
                      '<div class="faq-wrap"><details class="faq"><summary><h3>' + qname +
                      '</h3><span class="pm"><svg><use href="#i-plus"/></svg></span></summary><div class="ans">'
                      + answer_html(answer) + '</div></details>', 1)
    return s


PREFIX = "../"


def answer_html(a):
    return a.replace("See the full fees table for every course.",
                     f'See the full <a href="{PREFIX}fees/" class="in-link">fees table for every course</a>.')


def set_offer(s, cid):
    c = C[cid]
    low = min(min(v) for v in c["prices"].values())
    high = max(max(v) for v in c["prices"].values())
    offers = [
        {"@type": "Offer", "category": "Free trial", "price": "0", "priceCurrency": "USD", "description": "2 free trial classes"},
        {"@type": "AggregateOffer", "category": "Subscription", "priceCurrency": "USD",
         "lowPrice": str(conv(low, "USD")), "highPrice": str(conv(high, "USD")),
         "description": "Monthly plan, 2, 4 or 5 days a week, live 1-on-1 with a female teacher"},
        {"@type": "AggregateOffer", "category": "Subscription", "priceCurrency": "PKR",
         "lowPrice": str(low), "highPrice": str(high),
         "description": "Monthly plan in Pakistan, 2, 4 or 5 days a week"},
    ]
    return re.sub(r'"offers": (\{[^{}]*\}|\[.*?\])\}</script>',
                  lambda m: '"offers": ' + json.dumps(offers, ensure_ascii=False) + '}</script>', s, count=1)


def write(path, s):
    open(path, "w").write(s)


def main():
    global PREFIX
    PREFIX = "../"
    # course pages
    for page, ids in COURSE_PAGES.items():
        p = os.path.join(ROOT, page, "index.html")
        if not os.path.exists(p):
            continue  # page not built yet; its fees still show on the fees, country and audience pages
        s = open(p).read()
        inner = switcher("USD") + '<div class="fee-grid">' + "".join(course_table(C[i], "USD", link=len(ids) > 1, prefix=PREFIX) for i in ids) + "</div>" + note(PREFIX, "USD")
        name = C[ids[0]]["name"] if len(ids) == 1 else "Noorani Qaida and Quran Reading"
        s = put(s, "course", section(inner, "Monthly Fees", f"{name} Fees", "Simple monthly plans for 2, 4 or 5 days a week. Pick the class length that suits you."), "section2")
        s = hero_price(s, min(min(C[i]["prices"][m][0] for m in C[i]["prices"]) for i in ids), "USD")
        for i in ids[:1] if len(ids) == 1 else ids:
            s = set_faq(s, f"How much do {C[i].get('faq_name', C[i]['name'])} classes cost?", course_answer(i), add_if_missing=True)
        s = set_offer(s, ids[-1] if page != "learn-quran-online-for-beginners" else "nazra")
        write(p, s)
    # audience pages
    for page, (ids, cur) in AUDIENCE_PAGES.items():
        p = os.path.join(ROOT, page, "index.html")
        s = open(p).read()
        inner = switcher(cur) + overview_table(ids, cur, PREFIX) + note(PREFIX, cur)
        s = put(s, "overview", section(inner, "Monthly Fees", "Fees for Every Course", "Monthly fee per student for 2, 4 or 5 days a week. 45 minute class fees are on the fees page."), "section2")
        s = hero_price(s, min(C[i]["prices"][min(C[i]["prices"])][0] for i in ids), cur)
        write(p, s)
    # country pages
    for page, (cur, place, word) in COUNTRY.items():
        p = os.path.join(ROOT, page, "index.html")
        s = open(p).read()
        inner = '<div class="fee-grid">' + "".join(course_table(C[i], cur, prefix=PREFIX) for i in OVERVIEW) + "</div>" + note(PREFIX, cur)
        s = put(s, "country", section(inner, "Fees in " + word.title(),
                                      f"Online Quran Class Fees in {place}",
                                      f"Monthly fee per student in {word} for every course, 2, 4 or 5 days a week."), "hero")
        s = hero_price(s, min(C[i]["prices"][min(C[i]["prices"])][0] for i in OVERVIEW), cur)
        for q in re.findall(r'"name": "(How much [^"]*)"', s)[:1]:
            s = set_faq(s, q, how_much_answer(cur, place))
        write(p, s)
    fees_page()
    import glob
    for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
        ensure_script(f)
    print("fees built")


FEES_FAQ = [
    ("How much do online Quran classes cost?", None),
    ("Are there free classes before paying?",
     "Yes. Every new student gets 2 free trial classes with a female teacher. We do not ask for card or payment details to book them."),
    ("Why are your fees lower than other online Quran academies?",
     "We keep one fair fee for every family. Our overseas fees are simply our Pakistan fee converted to your currency and rounded up a little for exchange rates, so a family in London or Toronto pays the same as a family in Lahore. The teaching is the same: live, one-to-one, with a female teacher."),
    ("How do I pay from the USA, UK, Canada, Australia or the UAE?",
     "Families abroad usually pay by bank transfer or Western Union, or a relative in Pakistan pays for them by JazzCash, Easypaisa or bank transfer. We share the payment details on WhatsApp after your free classes. We do not take card or PayPal payments at the moment."),
    ("How do I pay in Pakistan?",
     "You can pay by JazzCash, Easypaisa or bank transfer. The fee is paid monthly, in advance."),
    ("Do I pay per class or per month?",
     "Plans are monthly and paid in advance, based on how many days a week you study (2, 4 or 5) and how long each class is."),
    ("Is there a discount for siblings?",
     "Yes, families with more than one student get a small family discount. Message us on WhatsApp with how many children, or a mother and child, will study and we will tell you your family fee."),
    ("What happens if the teacher misses a class?",
     "Our teachers are human too, and sometimes life happens: an illness, load-shedding or an internet problem at the teacher's end. Whenever a class is missed from our side, we always make it up, at the weekend or on any weekday your child is free. Not a single lesson is lost, and we are truly grateful for your patience and understanding."),
    ("What if my child misses a class?",
     "Please let your teacher know as early as you can. Classes missed by the student are not automatically made up, but if your teacher has a free slot she will try her best to fit one in."),
    ("Can I get a refund?",
     "Yes. If you have paid but decide not to start, you get a full refund. If you stop in the middle of a month, we refund 50% of that month's fee."),
    ("Are classes held on Eid and public holidays?",
     "Classes are off on Eid and on Pakistan's public holidays, such as 9th and 10th Muharram and 12 Rabi ul Awwal. These days are not made up. In Ramadan, class timings change and we agree new times with you."),
    ("Are books, tests or certificates included?",
     "Your teacher shares the pages you need as pictures, so you do not have to buy anything to start. If you would like a printed book, she will tell you which one to buy. We do not run formal tests, reports or certificates. Instead, your teacher keeps you updated on WhatsApp about how the student is doing."),
    ("Can I change my teacher or class time?",
     "Yes. If you would like a different teacher, we arrange one within 2 to 3 days. A new class time is possible whenever your teacher is free at that time."),
    ("Can I change my plan later?",
     "Yes. You can move to more or fewer days a week from the next month. Just tell us on WhatsApp before your next payment."),
]


def faq_html(items):
    out = []
    for i, (q, a) in enumerate(items):
        op = " open" if i == 0 else ""
        out.append(f'<details class="faq"{op}><summary><h3>{q}</h3><span class="pm"><svg><use href="#i-plus"/></svg></span></summary><div class="ans">{a}</div></details>')
    return "".join(out)


def faq_ld(items):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in items]},
        ensure_ascii=False)


def fees_page():
    global PREFIX
    PREFIX = "../"
    p = os.path.join(ROOT, "fees", "index.html")
    s = open(p).read()
    q = C["qaida"]["prices"]["30"]; n = C["nazra"]["prices"]
    lows = [min(min(c["prices"][m][i] for m in c["prices"]) for c in C.values()) for i in range(3)]
    cards = ""
    meta = [("2 Days Plan", "About 8 to 9 classes a month", "Great for busy schedules and older students", ""),
            ("4 Days Plan", "About 16 to 17 classes a month", "Steady progress without rushing", " feat"),
            ("5 Days Plan", "About 20 to 22 classes a month", "Best for Qaida, Hifz and fast progress", "")]
    for d, low, (h, cnt, why, feat) in zip(DAYS, lows, meta):
        tag = '<span class=tag>Most popular</span>' if feat else ""
        btn = "btn-gold" if feat else "btn-dark"
        cards += (f'<div class="price-card{feat}">{tag}<h3>{h}</h3><div class="from">from</div>'
                  f'<div class="days"><span class="fee" data-pkr="{low}">{fmt_html(low, "USD")}</span></div>'
                  f'<div class="per">a month</div>'
                  f'<ul><li>{cnt}</li><li>Live 1-on-1 with a female teacher</li><li>30 or 45 minute classes</li><li>{why}</li></ul>'
                  f'<a href="https://wa.me/923350548488" data-wa="Assalamu alaikum, I would like to know more about the {d} days a week plan." data-wa-loc="fees-card" class="btn {btn}">Ask About This Plan</a></div>')
    plans = (f'<section class="sec bg-cream" id="plans"><div class="container"><div class="section-head"><span class="eyebrow">Plans</span>'
             f'<h2>Choose How Many Days a Week You Study</h2><p>One fair monthly fee per student, wherever you live. Every plan starts with 2 free classes.</p></div>'
             + switcher("USD") + f'<div class="fgrid">{cards}</div></div></section>')
    table = section(
        '<div class="fee-grid">' + "".join(course_table(c, "USD", prefix=PREFIX) for c in C.values()) + "</div>"
        + note(PREFIX, 'USD'),
        "Fee Table", "Monthly Fees for Every Course",
        "Live one-to-one classes with a female teacher, 2, 4 or 5 days a week. Tap a currency above to see fees in your money.",
        bg="bg-cream-2", sid="fee-table")
    inc = ["Live one-to-one classes with a female teacher", "The same teacher every class",
           "Book pages shared by your teacher as pictures", "WhatsApp updates from your teacher on how the student is doing",
           "Parents can sit in on any lesson", "WhatsApp video, Skype, Google Meet or Zoom, whichever you prefer",
           "Class times in any time zone"]
    exc = ["Printed books (optional; your teacher tells you which one to buy)", "Formal tests, reports or certificates",
           "Class recordings (we never record lessons, for your privacy)"]
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    included = (f'<section class="sec bg-white" id="included"><div class="container"><div class="section-head"><span class="eyebrow">Know Before You Pay</span>'
                f'<h2>What Your Monthly Fee Includes</h2><p>No hidden extras. Here is exactly what you get, and how to pay.</p></div>'
                f'<div class="inc-grid"><div class="inc-card"><h3>Included</h3><ul class="checks">{li(inc)}</ul></div>'
                f'<div class="inc-card"><h3>Not included</h3><ul class="crosses">{li(exc)}</ul></div>'
                f'<div class="inc-card"><h3>How to pay</h3><p><b>In Pakistan:</b> JazzCash, Easypaisa or bank transfer.</p>'
                f'<p><b>From abroad:</b> bank transfer or Western Union, or a relative in Pakistan can pay for you by JazzCash, Easypaisa or bank transfer.</p>'
                f'<p>Fees are paid monthly, in advance. We share payment details on WhatsApp after your <a href="{PREFIX}free-trial/" class="in-link">2 free classes</a>.</p></div></div></div></section>')
    block = plans + table + included
    # replace from Plans section up to the enrol CTA (first build) or marker block (later builds)
    start = "<!--FEES:page-->"
    if start in s:
        s = re.sub(re.escape(start) + r".*?<!--/FEES-->", lambda m: start + block + "<!--/FEES-->", s, count=1, flags=re.S)
    else:
        a = s.index('<section class="sec bg-cream"><div class="container"><div class="section-head"><span class="eyebrow">Plans</span>')
        b = s.index(ENROL)
        s = s[:a] + start + block + "<!--/FEES-->" + s[b:]
    # FAQ
    items = [(qq, aa if aa else how_much_answer("USD").replace(" See the full fees table for every course.", " The fee table above shows every course in your currency.")) for qq, aa in FEES_FAQ]
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
               lambda m: '<script type="application/ld+json">' + faq_ld(items) + "</script>", s, count=1, flags=re.S)
    s = re.sub(r'(<h2>Fees: Frequently Asked Questions</h2></div><div class="faq-wrap">).*?(</div></div></section>)',
               lambda m: m.group(1) + faq_html(items) + m.group(2), s, count=1, flags=re.S)
    # hero points + meta
    s = re.sub(r'(<ul class="hero-points">).*?(</ul>)', lambda m: m.group(1) + "".join(
        f'<li><span class="tick"><svg width="14" height="14"><use href="#i-tick"/></svg></span>{t}</li>' for t in
        ["2 free classes first", f"From {fmt(lows[0], 'USD')} a month", "Same fair fee worldwide", "Family discount"]) + m.group(2), s, count=1, flags=re.S)
    desc = (f"Online Quran classes fees from {fmt(lows[0], 'USD')} a month (Rs {lows[0]:,}). Live 1-on-1 classes with female teachers, "
            f"2, 4 or 5 days a week, for kids and women. Start with 2 free classes.")
    s = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), s)
    write(p, s)


def ensure_script(path):
    s = open(path).read()
    s = re.sub(r'\n<script src="[^"]*assets/fees\.js[^"]*" defer></script>', "", s)
    if "cur-switch" in s:
        m = re.search(r'(<script src="([^"]*)assets/site\.js[^"]*" defer></script>)', s)
        s = s.replace(m.group(1), m.group(1) + f'\n<script src="{m.group(2)}assets/fees.js" defer></script>', 1)
    write(path, s)


if __name__ == "__main__":
    main()
