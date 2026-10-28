"""Helpers to read/replace FAQ blocks (visible <details> + FAQPage JSON-LD) on a page."""
import re, json

PLUS = '<span class="pm"><svg><use href="#i-plus"/></svg></span>'
DET = re.compile(r'<details class="faq"( open)?><summary><h3>(.*?)</h3>.*?<div class="ans">(.*?)</div></details>', re.S)
LD = re.compile(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', re.S)


def strip(a):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", a)).strip()


def details(items, open_first=True):
    return "".join(f'<details class="faq"{" open" if (i == 0 and open_first) else ""}><summary><h3>{q}</h3>{PLUS}</summary><div class="ans">{a}</div></details>'
                   for i, (q, a) in enumerate(items))


def ld(items):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}, ensure_ascii=False) + "</script>"


def read_items(s, start_marker='id="faq"'):
    i = s.index(start_marker)
    j = s.index("</section>", i)
    return [(m.group(2), m.group(3)) for m in DET.finditer(s[i:j])]


def replace_section_items(s, items, start_marker='id="faq"'):
    i = s.index(start_marker)
    a = s.index('<div class="faq-wrap">', i) + len('<div class="faq-wrap">')
    b = s.index('</div></div></section>', a)
    return s[:a] + details(items) + s[b:]


def set_ld(s, items):
    return LD.sub(lambda m: ld(items), s, count=1)
