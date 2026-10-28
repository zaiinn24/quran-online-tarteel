#!/usr/bin/env python3
"""Build the Duas & Azkar library (/duas-azkar/ hub + topic pages) from scripts/duas_data.py.
Quran text: King Fahd Complex Uthmani text via quran-json (dist/quran.json), path in QURAN_JSON env or default scratch path."""
import os, re, json, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
from duas_data import PAGES, ORDER
from faqlib import details, ld

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QJ = os.environ.get("QURAN_JSON", os.path.join(ROOT, "data", "quran-uthmani.json"))
Q = json.load(open(QJ))
SITE = "https://quranonlinetarteel.net/"
TPL = open(os.path.join(ROOT, "resources", "how-many-rakats", "index.html")).read()
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def verse(s, a, w0=0, w1=None):
    words = Q[s - 1]["verses"][a - 1]["text"].split(" ")
    seg = " ".join(words[w0:(w1 + 1 if w1 is not None else None)])
    end = f' ({str(a).translate(AR_DIGITS)})' if (w1 is None) else ""
    return seg + end


def arabic(x):
    if x == "QULS":
        return "<br>".join(f'<span class="q-surah">{arabic(("S", n))}</span>' for n in (112, 113, 114))
    if isinstance(x, list):
        return " ".join(arabic(v) for v in x)
    if isinstance(x, tuple) and x[0] == "Q":
        return verse(*x[1:])
    if isinstance(x, tuple) and x[0] == "S":
        n = x[1]
        return " ".join(verse(n, i + 1) for i in range(len(Q[n - 1]["verses"])))
    return H.escape(x)


def frame_ar(text):
    return ('<svg class="illus" viewBox="0 0 480 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Arabic calligraphy">'
            '<defs><linearGradient id="dag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2c47e"/><stop offset="1" stop-color="#a97f2e"/></linearGradient>'
            '<linearGradient id="dabg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e261a"/><stop offset="1" stop-color="#14110c"/></linearGradient>'
            '<radialGradient id="dagl" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#c79b45" stop-opacity=".4"/><stop offset="1" stop-color="#c79b45" stop-opacity="0"/></radialGradient>'
            '<pattern id="dapat" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M20 3l5 12 12 5-12 5-5 12-5-12-12-5 12-5z" fill="none" stroke="#c79b45" stroke-opacity=".14"/></pattern></defs>'
            '<path d="M60 400V170C60 80 150 22 240 22s180 58 180 148V400Z" fill="url(#dabg)"/><path d="M60 400V170C60 80 150 22 240 22s180 58 180 148V400Z" fill="url(#dapat)"/>'
            '<ellipse cx="240" cy="200" rx="190" ry="150" fill="url(#dagl)"/>'
            '<path d="M48 400V168C48 72 142 10 240 10s192 62 192 158V400" fill="none" stroke="url(#dag)" stroke-width="2.5"/>'
            '<path d="M72 400V172C72 92 156 36 240 36s168 56 168 136V400" fill="none" stroke="#c79b45" stroke-opacity=".35"/>'
            '<circle cx="240" cy="96" r="16" fill="#e2c47e"/><circle cx="246.7" cy="91.5" r="13.4" fill="#2a2318"/>'
            f'<text x="240" y="225" text-anchor="middle" font-family="Amiri, serif" font-size="{44 if len(text) < 14 else 34}" fill="#fbf7ee">{text}</text>'
            '<path d="M150 262H330" stroke="url(#dag)" stroke-width="2"/><path d="M196 280H284" stroke="#c79b45" stroke-opacity=".5" stroke-width="1.5"/>'
            '<g fill="#e2c47e" opacity=".75"><rect x="234" y="300" width="12" height="12" transform="rotate(45 240 306)"/></g></svg>')


def count_label(c):
    if not c:
        return ""
    return f'<span class="dua-count">{"Once" if c == "1" else c + (" times" if c.isdigit() else "")}</span>'


def card(i, item):
    when, ar, tr, en, ur, cnt, ref = item
    is_q = isinstance(ar, (tuple, list)) or ar == "QULS"
    return (f'<article class="dua{" dua-q" if is_q else ""}" id="dua-{i}"><div class="dua-head"><h2>{H.escape(when)}</h2>{count_label(cnt)}</div>'
            f'<p class="dua-ar" lang="ar" dir="rtl">{arabic(ar)}</p>'
            f'<p class="dua-tr"><span class="lbl">Transliteration</span>{H.escape(tr)}</p>'
            f'<div class="dua-mean"><p><span class="lbl">English</span>{H.escape(en)}</p><p><span class="lbl">Roman Urdu</span>{H.escape(ur)}</p></div>'
            f'<div class="dua-foot"><span class="dua-ref"><b>Reference:</b> {ref}</span><button type="button" class="dua-copy" data-copy="dua-{i}">Copy dua</button></div></article>')


def head(s, title, desc, url, crumbs, faqs, article=True):
    s = re.sub(r"<title>.*?</title>", f"<title>{H.escape(title)}</title>", s, count=1)
    for a in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'(<meta ' + re.escape(a) + r' content=")[^"]*(")', lambda m: m.group(1) + H.escape(desc) + m.group(2), s)
    for a in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta ' + re.escape(a) + r' content=")[^"]*(")', lambda m: m.group(1) + H.escape(title) + m.group(2), s)
    s = s.replace(SITE + "resources/how-many-rakats/", url)
    lds = []
    if article:
        lds.append({"@context": "https://schema.org", "@type": "Article", "headline": re.sub(r"\s*\|.*", "", title), "description": desc, "url": url,
                    "inLanguage": "en", "datePublished": "2026-10-29", "dateModified": "2026-10-29",
                    "author": {"@type": "Organization", "name": "Quran Online Tarteel", "url": SITE},
                    "publisher": {"@type": "Organization", "name": "Quran Online Tarteel", "url": SITE}, "mainEntityOfPage": url})
    lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    block = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds) + (ld(faqs) + "\n" if faqs else "")
    s = re.sub(r'(<script type="application/ld\+json">.*?</script>\n?)+', lambda m: block, s, count=1, flags=re.S)
    return s


def build_page(slug, P, prefix="../../"):
    url = f"{SITE}duas-azkar/{slug}/"
    s = head(TPL, P["title"], P["desc"], url, [("Home", SITE), ("Duas & Azkar", SITE + "duas-azkar/"), (re.sub(r"<[^>]+>", "", P["h1"]), url)], P["faqs"])
    hero = (f'<section class="page-hero pattern-dark dua-hero"><div class="container page-hero-grid"><div class="hero-text">'
            f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{prefix}">Home</a><span>/</span><a href="../">Duas &amp; Azkar</a></nav>'
            f'<span class="eyebrow">{P["eyebrow"]}</span><h1>{P["h1"]}</h1><p class="hero-lead">{H.escape(P["desc"])}</p></div>'
            f'<div class="hero-right"><div class="illus-wrap">{frame_ar(P["ar_title"])}</div></div></div></section>')
    lab = lambda w: re.sub(r"\s*\(.*?\)", "", w).strip()
    n = len(P["items"])
    toc = "".join(f'<li><a href="#dua-{i+1}" data-i="{i+1}"><b>{i+1}</b><span>{H.escape(lab(it[0]))}</span></a></li>' for i, it in enumerate(P["items"]))
    cards = "".join(card(i + 1, it) for i, it in enumerate(P["items"]))
    related = "".join(f'<a class="chip" href="../{o}/">{H.escape(re.sub(r"<[^>]+>", "", PAGES[o]["h1"]))}</a>' for o in ORDER if o != slug)
    body = (f'<section class="sec bg-white"><div class="container"><div class="article prose duas-article">'
            f'<p class="lead-p">{P["intro"]}</p>'
            f'<div class="dua-layout"><aside class="dua-nav" aria-label="Duas on this page"><div class="dn-head"><span class="dn-n">{n}</span><span>duas on this page</span></div>'
            f'<ol>{toc}</ol><button type="button" class="dn-all" aria-pressed="false">View all on one page</button></aside>'
            f'<div class="dua-stage">{cards}<div class="dua-pager" hidden><button type="button" class="dp-prev">&larr; Previous</button>'
            f'<span class="dp-pos"></span><button type="button" class="dp-next">Next &rarr;</button></div></div></div>'
            f'<div class="dua-learn"><div><h3>Learn these duas with a female teacher</h3><p>Correct Arabic pronunciation, meaning and a daily habit, in live one-to-one lessons for kids and women.</p></div>'
            f'<div class="acts"><a href="{prefix}online-duas-course/" class="btn btn-gold">Online Duas Course</a><a href="{prefix}free-trial/" class="btn btn-dark">Book 2 Free Classes</a></div></div>'
            f'<p class="dua-source">Sources: Arabic of the hadith duas from Hisn al-Muslim and the cited hadith collections (sunnah.com); Quran text from the King Fahd Complex Uthmani script. English and Roman Urdu meanings written by Quran Online Tarteel.</p>'
            f'</div></div></section>'
            f'<section class="sec bg-cream" style="padding:64px 0"><div class="container"><div class="section-head" style="margin-bottom:22px"><span class="eyebrow">More Duas</span><h2>Explore the Duas &amp; Azkar Library</h2></div>'
            f'<div class="chip-row" style="justify-content:center">{related}</div></div></section>')
    a = s.index('<section class="page-hero')
    b = s.index('<section class="cta-sec')
    s = s[:a] + hero + body + s[b:]
    s = re.sub(r'<h2>How Many Rakats: Questions Answered</h2>', f'<h2>{H.escape(re.sub(r"<[^>]+>", "", P["h1"]))}: Questions Answered</h2>', s)
    i = s.index('id="faq"'); fa = s.index('<div class="faq-wrap">', i) + len('<div class="faq-wrap">'); fb = s.index('</div></div></section>', fa)
    s = s[:fa] + details(P["faqs"]) + s[fb:]
    s = s.replace('value="Guide: How Many Rakats"', f'value="Duas: {slug}"').replace('<body data-nav="resources">', '<body data-nav="duas">')
    d = os.path.join(ROOT, "duas-azkar", slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(s)


def build_hub():
    url = SITE + "duas-azkar/"
    title = "Duas & Azkar in English and Urdu | Masnoon Duas with Meaning"
    desc = "A free library of authentic duas and azkar from the Quran and Sunnah: morning and evening azkar, duas after namaz, daily duas for kids, Rabbana duas and more, in English and Roman Urdu."
    faqs = [("Are these duas authentic?", "Yes. Every dua is from the Quran or from authentic hadith, with its reference. The Arabic is taken from Hisn al-Muslim and the King Fahd Complex Quran text."),
            ("Can my child learn these duas with a teacher?", "Yes. Our female teachers teach duas with correct pronunciation and meaning in the <a href=\"../online-duas-course/\" class=\"in-link\">online duas course</a>, with 2 free classes."),
            ("Are the translations in Urdu?", "Each dua has its meaning in English and in Roman Urdu (Urdu written in English letters), so the whole family can understand it.")]
    s = head(TPL, title, desc, url, [("Home", SITE), ("Duas & Azkar", url)], faqs, article=False)
    s = s.replace('"../../', '"../').replace("'../../", "'../")
    cards = "".join(f'<a class="post-card dua-hub-card" href="{o}/"><div class="dhc-ar" lang="ar" dir="rtl">{PAGES[o]["ar_title"]}</div><div class="pc-body"><span class="pc-tag">{len(PAGES[o]["items"])} duas</span>'
                    f'<h3>{re.sub(r"<[^>]+>", "", PAGES[o]["h1"])}</h3><p>{PAGES[o]["card"]}</p><span class="in-link" style="display:inline-block;margin-top:10px">Read with meaning</span></div></a>' for o in ORDER)
    guides = ('<a class="chip" href="../resources/tajweed-rules/">Tajweed rules for beginners</a><a class="chip" href="../resources/noorani-qaida-guide/">Noorani Qaida lesson guide</a>'
              '<a class="chip" href="../resources/how-many-rakats/">How many rakats in each prayer</a>')
    hero = ('<section class="page-hero pattern-dark dua-hero"><div class="container page-hero-grid"><div class="hero-text"><span class="eyebrow">Free Library</span>'
            '<h1>Duas &amp; Azkar <span class="gold">in English and Urdu</span></h1>'
            '<p class="hero-lead">Authentic duas and azkar from the Quran and Sunnah for every part of the day, each with the Arabic, an easy transliteration, its meaning in English and Roman Urdu, and the reference. Free for every family.</p></div>'
            f'<div class="hero-right"><div class="illus-wrap">{frame_ar("أَدْعِيَة وَأَذْكَار")}</div></div></div></section>')
    body = (f'<section class="sec bg-white"><div class="container"><div class="section-head"><span class="eyebrow">Duas by Topic</span><h2>Masnoon Duas and Azkar with Meaning</h2>'
            f'<p>Choose a topic. Every page shows the Arabic, transliteration, English and Roman Urdu meaning, and the source.</p></div><div class="fgrid dua-hub">{cards}</div></div></section>'
            '<section class="sec bg-cream-2 qaida-band"><div class="container"><div class="qb-in"><div class="qb-ar" lang="ar">القَاعِدَةُ النُّورَانِيَّة</div><div class="qb-txt"><span class="eyebrow">Free Download</span><h2>Free Noorani Qaida PDF</h2><p>Our own 16-page Noorani Qaida practice book: 13 lessons from the Arabic letters to Surah Al-Fatiha, for children and adults.</p><a href="../downloads/noorani-qaida-quran-online-tarteel.pdf" class="btn btn-gold" data-track="qaida_pdf_download" target="_blank" rel="noopener">Download the Qaida PDF (free)</a></div></div></div></section>'
            f'<section class="sec bg-cream" style="padding:64px 0"><div class="container"><div class="section-head" style="margin-bottom:22px"><span class="eyebrow">Learning Guides</span><h2>Free Quran Learning Guides</h2></div>'
            f'<div class="chip-row" style="justify-content:center">{guides}</div></div></section>')
    a = s.index('<section class="page-hero'); b = s.index('<section class="cta-sec')
    s = s[:a] + hero + body + s[b:]
    s = re.sub(r'<h2>How Many Rakats: Questions Answered</h2>', '<h2>Duas &amp; Azkar: Questions Answered</h2>', s)
    i = s.index('id="faq"'); fa = s.index('<div class="faq-wrap">', i) + len('<div class="faq-wrap">'); fb = s.index('</div></div></section>', fa)
    s = s[:fa] + details(faqs) + s[fb:]
    s = s.replace('value="Guide: How Many Rakats"', 'value="Duas & Azkar hub"').replace('<body data-nav="resources">', '<body data-nav="duas">')
    os.makedirs(os.path.join(ROOT, "duas-azkar"), exist_ok=True)
    open(os.path.join(ROOT, "duas-azkar", "index.html"), "w").write(s)


if __name__ == "__main__":
    for slug in ORDER:
        build_page(slug, PAGES[slug])
    build_hub()
    print("built", len(ORDER), "dua pages + hub")
