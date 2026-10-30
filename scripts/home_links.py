#!/usr/bin/env python3
"""Homepage internal linking: free library section (duas, azkar, Qaida PDF, guides), country strip, richer organisation schema,
and /llms.txt for AI assistants. Idempotent."""
import os, re, json, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quranonlinetarteel.net/"

TILES = [
    ("duas-azkar/", "أَذْكَار", "Duas & Azkar Library", "188 authentic duas in Arabic, English and Roman Urdu.", "Free library"),
    ("duas-azkar/morning-evening-azkar/", "الصَّبَاح<br>وَالمَسَاء", "Morning and Evening Azkar", "The daily adhkar with how many times to read each.", "22 duas"),
    ("duas-azkar/azkar-after-namaz/", "بَعْدَ<br>الصَّلَاة", "Azkar After Namaz", "Tasbih, Ayatul Kursi and duas after every prayer.", "12 duas"),
    ("duas-azkar/daily-duas-for-kids/", "أَدْعِيَة", "Daily Duas for Kids", "Waking, eating, wudu, leaving home and more.", "20 duas"),
    ("duas-azkar/rabbana-duas/", "رَبَّنَا", "40 Rabbana Duas", "Every Rabbana dua from the Quran with meaning.", "45 duas"),
    ("duas-azkar/ayatul-kursi-and-4-quls/", "آيَةُ<br>الكُرْسِيّ", "Ayatul Kursi and 4 Quls", "Full Arabic text with meaning in English and Urdu.", "Quran"),
    ("downloads/noorani-qaida-quran-online-tarteel.pdf", "القَاعِدَة", "Noorani Qaida PDF", "Free 63-page colour Qaida with hijje and tajweed.", "Free PDF"),
    ("resources/tajweed-rules/", "تَجْوِيد", "Tajweed Rules for Beginners", "Noon sakinah, meem sakinah, qalqalah and madd.", "Guide"),
    ("resources/how-many-rakats/", "صَلَاة", "How Many Rakats in Each Prayer", "A simple chart of the five daily prayers.", "Guide"),
]
COUNTRIES = [("online-quran-classes-usa/", "USA"), ("online-quran-classes-uk/", "UK"), ("online-quran-classes-canada/", "Canada"),
             ("online-quran-classes-australia/", "Australia"), ("online-quran-classes-uae/", "UAE"), ("online-quran-classes-pakistan/", "Pakistan")]


def tile(href, ar, title, desc, meta):
    pdf = href.endswith(".pdf")
    extra = ' data-track="qaida_pdf_download" target="_blank" rel="noopener"' if pdf else ""
    return (f'<a class="lib-tile" href="{href}"{extra}><span class="lt-ar" lang="ar" dir="rtl">{ar}</span><span class="lt-body"><span class="lt-meta">{meta}</span>'
            f'<span class="lt-title">{H.escape(title)}</span><span class="lt-desc">{H.escape(desc)}</span></span><span class="lt-go" aria-hidden="true">&rarr;</span></a>')


LIB = ('<section class="sec bg-white" id="resources"><div class="container"><div class="section-head"><span class="eyebrow">Free Islamic Library</span>'
       '<h2>Free Duas, Azkar and Quran Learning Resources</h2>'
       '<p>Authentic duas from the Quran and Sunnah with meanings in English and Roman Urdu, our own Noorani Qaida PDF and simple guides to practise between classes.</p></div>'
       '<p class="swipe-hint swipe-top" aria-hidden="true">Swipe for more <span>&rarr;</span></p>'
       '<div class="lib-grid home-lib">' + "".join(tile(*t) for t in TILES) + '</div>'
       '<div class="center-cta"><a href="duas-azkar/" class="btn btn-dark">Browse all 188 duas <svg><use href="#i-arrow"/></svg></a></div></div></section>')

COUNTRY = ('<!--COUNTRIES--><section class="sec bg-white country-sec" id="countries"><div class="container"><div class="section-head" style="margin-bottom:22px"><span class="eyebrow">Classes in Your Time Zone</span>'
           '<h2>Online Quran Classes Wherever You Live</h2>'
           '<p>Female teachers for families in the USA, UK, Canada, Australia, the UAE and Pakistan, with fees shown in your own currency.</p></div>'
           '<div class="chip-row country-chips">' + "".join(f'<a class="chip" href="{h}">Online Quran classes in {n}</a>' for h, n in COUNTRIES) +
           '<a class="chip chip-gold" href="fees/">See fees and plans</a></div></div></section><!--/COUNTRIES-->')

CSS = '''
/* homepage library + countries */
.home-lib{margin-bottom:6px}
.country-sec{padding:64px 0}
.country-chips{justify-content:center}
.chip-gold{background:linear-gradient(135deg,#e2c47e,#b8913f)!important;color:#14110c!important;border-color:transparent!important;font-weight:800}
@media(max-width:640px){#resources .lib-grid{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;margin:0 -20px;padding:4px 20px 14px;scrollbar-width:none}
#resources .lib-grid::-webkit-scrollbar{display:none}#resources .lib-grid>*{flex:0 0 84%;scroll-snap-align:center}.country-sec{padding:48px 0}}
'''

COURSES = [("Noorani Qaida", "noorani-qaida-online/"), ("Quran Reading for Beginners", "learn-quran-online-for-beginners/"),
           ("Tajweed", "online-tajweed-classes/"), ("Hifz (Quran Memorisation)", "online-hifz-program/"),
           ("Quran Translation and Tafseer", "quran-translation-tafseer-classes/"), ("Islamic Studies", "online-islamic-studies/"),
           ("Juz Amma Memorisation", "juz-amma-memorization-online/"), ("Salah (Prayer) Classes", "online-salah-classes/"),
           ("Daily Duas Course", "online-duas-course/"), ("40 Hadith for Kids", "40-hadith-for-kids/"),
           ("Quran Classes for New Muslims", "quran-classes-for-new-muslims/"), ("Quran Classes for Kids", "online-quran-classes-for-kids/"),
           ("Quran Classes for Women", "online-quran-classes-for-women/")]


def main():
    p = os.path.join(ROOT, "index.html")
    s = open(p).read()
    a = s.index('<section class="sec bg-white" id="resources">')
    b = s.index('</section>', a) + len('</section>')
    s = s[:a] + LIB + s[b:]
    s = re.sub(r"<!--COUNTRIES-->.*?<!--/COUNTRIES-->", "", s, flags=re.S)
    f = s.index('<section class="sec bg-cream" id="faq"')
    s = s[:f] + COUNTRY + s[f:]

    def org(m):
        d = json.loads(m.group(1))
        if d.get("@type") != "EducationalOrganization":
            return m.group(0)
        d.update({"foundingDate": "2010", "knowsLanguage": ["en", "ur", "ar"],
                  "slogan": "Online Quran classes for kids and women with female teachers",
                  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Online Quran courses",
                                      "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Course", "name": n, "url": SITE + u,
                                                           "provider": {"@id": SITE + "#org"}}} for n, u in COURSES]}})
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
    s = re.sub(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "EducationalOrganization".*?)</script>', org, s, count=1, flags=re.S)
    open(p, "w").write(s)

    c = os.path.join(ROOT, "assets", "site.css")
    css = open(c).read()
    css = re.sub(r"\n/\* homepage library \+ countries \*/.*?(?=\n/\*|\Z)", "", css, flags=re.S)
    open(c, "w").write(css.rstrip("\n") + "\n" + CSS)

    # llms.txt: plain summary for AI assistants
    lines = ["# Quran Online Tarteel", "",
             "> Online Quran academy (since 2010) teaching children under 18 and women in live one-to-one classes, taught only by female teachers. "
             "Families in the USA, UK, Canada, Australia, the UAE and Pakistan. Every new student starts with 2 free classes.", "",
             "Key facts: female teachers only, each with 10+ years of experience; 500+ children taught; 1-to-1 live classes; parents can sit in; "
             "plans of 2, 4 or 5 days a week; 25–30 minute classes (Tafseer 45–60); fees from $20 a month; WhatsApp +92 334 5259952.", "",
             "## Courses"] + [f"- [{n}]({SITE}{u})" for n, u in COURSES] + ["", "## Fees and booking",
             f"- [Fees and plans]({SITE}fees/)", f"- [Book 2 free classes]({SITE}free-trial/)", f"- [FAQ and safeguarding]({SITE}faq/)",
             f"- [About us]({SITE}about/)", f"- [Female Quran teachers]({SITE}female-quran-teachers/)", "", "## Countries"] + \
            [f"- [Online Quran classes in {n}]({SITE}{u})" for u, n in COUNTRIES] + ["", "## Free resources",
             f"- [Duas & Azkar library: 188 authentic duas with English and Roman Urdu meaning]({SITE}duas-azkar/)",
             f"- [Free Noorani Qaida PDF (63 colour pages)]({SITE}downloads/noorani-qaida-quran-online-tarteel.pdf)",
             f"- [Tajweed rules for beginners]({SITE}resources/tajweed-rules/)", f"- [Noorani Qaida lesson guide]({SITE}resources/noorani-qaida-guide/)",
             f"- [How many rakats in each prayer]({SITE}resources/how-many-rakats/)", ""]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(lines))
    print("homepage library + countries + schema + llms.txt")


if __name__ == "__main__":
    main()
