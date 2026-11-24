#!/usr/bin/env python3
"""Add the free-PDF download blocks and PDF keywords to the Tajweed rules and Morning/Evening adhkar pages.
Idempotent; run after build_duas.py / any regeneration of those pages, then stamp_assets.py."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M4 19h16"/></svg>'
PAGES = {
    "resources/tajweed-rules/index.html": dict(
        pdf="tajweed-rules-pdf-quran-online-tarteel.pdf", head="Tajweed Rules PDF: Free Download",
        text="Get every rule on this page as a printable 7 page A4 guide: makharij, heavy letters, noon and meem sakinah, ghunnah, qalqalah, madd, lam and ra rules and stop signs, with Arabic examples and charts.",
        title="Tajweed Rules for Beginners: Free PDF, Chart and Examples",
        desc="Tajweed rules for beginners with a free PDF: makharij, noon sakinah and tanween, meem sakinah, ghunnah, qalqalah and madd, with charts and Arabic examples.",
        h1='Tajweed Rules for <span class="gold">Beginners</span> (Free PDF)'),
    "duas-azkar/morning-evening-azkar/index.html": dict(
        pdf="morning-evening-adhkar-pdf-quran-online-tarteel.pdf", head="Morning and Evening Adhkar PDF: Free Download",
        text="Keep the adhkar on your phone or print them for the fridge: a 9 page A4 booklet with the Arabic, transliteration, English and Roman Urdu meaning, how many times to say each one and its reference.",
        title=None, desc=None, h1=None),
}


def block(pdf, head, text, pre):
    return (f'<!--PDFDL--><section class="pdf-dl-sec"><div class="container"><div class="pdf-dl"><div class="pdf-ic">{IC}</div>'
            f'<div class="pdf-tx"><h2>{head}</h2><p>{text}</p></div>'
            f'<a class="btn btn-gold" href="{pre}downloads/{pdf}" download data-pdf="{pdf}">Download Free PDF</a></div></div></section><!--/PDFDL-->')


for rel, c in PAGES.items():
    f = os.path.join(ROOT, rel)
    s = open(f, encoding="utf-8").read()
    pre = "../" * rel.count("/")
    s = re.sub(r"<!--PDFDL-->.*?<!--/PDFDL-->", "", s, flags=re.S)
    i = s.index("<main")
    j = s.index("</section>", i) + len("</section>")  # right after the hero
    s = s[:j] + block(c["pdf"], c["head"], c["text"], pre) + s[j:]
    if c["title"]:
        s = re.sub(r"<title>[^<]*</title>", f"<title>{c['title']}</title>", s, count=1)
        for prop in ['property="og:title"', 'name="twitter:title"']:
            s = re.sub(r'(<meta %s content=")[^"]*' % re.escape(prop), lambda m: m.group(1) + c["title"], s, count=1)
        for prop in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
            s = re.sub(r'(<meta %s content=")[^"]*' % re.escape(prop), lambda m: m.group(1) + c["desc"], s, count=1)
        s = re.sub(r"<h1>.*?</h1>", lambda m: f"<h1>{c['h1']}</h1>", s, count=1, flags=re.S)
    open(f, "w", encoding="utf-8").write(s)
    print("pdf block on", rel)
