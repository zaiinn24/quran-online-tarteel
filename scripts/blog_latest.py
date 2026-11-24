#!/usr/bin/env python3
"""'Latest from the blog' section on the homepage, service pages and country pages.
Every post is listed (topic-matched first, newest first) with its publish date; the Pages middleware
(and a small inline script as a fallback) removes posts that are not live yet and keeps the first 3.
So the section updates itself on each publish day. Run after build_blog.py. Idempotent."""
import json, os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = json.load(open(os.path.join(ROOT, "scripts", "blog_posts", "_index.json")))
LEGACY = [dict(url="resources/tajweed-rules/", title="Tajweed Rules for Beginners", cat="tajweed", img="legacy-tajweed-rules",
               excerpt="The main rules of Tajweed explained simply, with examples.", mins=6),
          dict(url="resources/noorani-qaida-guide/", title="Noorani Qaida Guide: Lessons, Order and Tips", cat="learn-quran", img="legacy-noorani-qaida-guide",
               excerpt="What each stage of the Noorani Qaida teaches and how parents can help.", mins=6),
          dict(url="resources/how-many-rakats/", title="How Many Rakats in Each Prayer?", cat="salah", img="legacy-how-many-rakats",
               excerpt="A simple chart of the fard rakats of the five daily prayers.", mins=3)]
CATL = {"learn-quran": "Learn Quran", "tajweed": "Tajweed", "kids": "Kids and Parents", "women": "Women", "hifz": "Hifz",
        "salah": "Salah and Worship", "duas": "Duas and Dhikr", "knowledge": "Quran Knowledge", "ramadan": "Ramadan", "guides": "Guides and Comparisons"}
PAGES = {  # page -> preferred categories (others follow, newest first)
    "index.html": [],
    "online-quran-classes-for-kids": ["kids", "learn-quran", "ramadan"],
    "online-quran-classes-for-women": ["women", "learn-quran", "knowledge"],
    "female-quran-teachers": ["women", "guides"],
    "noorani-qaida-online": ["learn-quran", "kids"],
    "learn-quran-online-for-beginners": ["learn-quran", "tajweed"],
    "online-tajweed-classes": ["tajweed"],
    "online-hifz-program": ["hifz", "knowledge"],
    "quran-translation-tafseer-classes": ["knowledge", "guides"],
    "online-islamic-studies": ["knowledge", "salah", "kids"],
    "online-duas-course": ["duas", "ramadan"],
    "online-salah-classes": ["salah", "duas"],
    "juz-amma-memorization-online": ["hifz", "kids"],
    "40-hadith-for-kids": ["kids", "knowledge"],
    "quran-classes-for-new-muslims": ["salah", "learn-quran"],
    "fees": ["guides", "learn-quran"],
    "free-trial": ["learn-quran", "guides"],
    "faq": ["guides", "learn-quran"],
}
for d in sorted(os.listdir(ROOT)):
    if d.startswith("online-quran-classes-") and d not in PAGES and os.path.exists(os.path.join(ROOT, d, "index.html")):
        PAGES[d] = ["learn-quran", "kids", "women"]

JS = ("<script>(function(){var t=new Date(Date.now()+5*36e5).toISOString().slice(0,10),n=0;"
      "document.querySelectorAll('[data-latest]').forEach(function(e){var d=e.getAttribute('data-pub');"
      "if((d&&d>t)||n>=3){e.remove()}else{n++}})})();</script>")


def nice(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {['January','February','March','April','May','June','July','August','September','October','November','December'][int(m)-1]} {y}"


def card(p, pre):
    url = pre + (p.get("url") or f'blog/{p["slug"]}/')
    img = p.get("img") or p["slug"]
    pub = f' data-pub="{p["date"]}"' if "date" in p else ""
    date = f'<span>{nice(p["date"])}</span>' if "date" in p else "<span>Free guide</span>"
    return (f'<a class="lb-card" href="{url}" data-latest{pub}><div class="lb-img"><img src="{pre}blog/img/{img}-640.webp" width="640" height="336" loading="lazy" decoding="async" alt="{html.escape(p["title"])}"></div>'
            f'<div class="lb-body"><span class="lb-cat">{CATL[p["cat"]]}</span><h3>{html.escape(p["title"])}</h3><p>{html.escape(p["excerpt"])}</p>'
            f'<div class="lb-foot">{date}<b>{p["mins"]} min read</b></div></div></a>')


def section(page, cats, pre):
    posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    first = [p for p in posts if p["cat"] in cats]
    rest = [p for p in posts if p["cat"] not in cats]
    leg = [l for l in LEGACY if l["cat"] in cats] + [l for l in LEGACY if l["cat"] not in cats]
    cards = "".join(card(p, pre) for p in first + rest + leg)
    return ('<!--BLOGLATEST--><section class="sec bg-white lb-sec" aria-label="Latest from the blog"><div class="container">'
            '<div class="section-head"><span class="eyebrow">From Our Blog</span><h2>Latest Guides from Our Blog</h2>'
            '<p>Free, practical articles on learning the Quran, Tajweed, Hifz, duas and salah, written by our academy.</p></div>'
            f'<div class="lb-grid">{cards}</div><p class="lb-more"><a class="btn btn-gold" href="{pre}blog/">Read all articles</a></p>'
            f'</div></section>{JS}<!--/BLOGLATEST-->')


def main():
    n = 0
    for page, cats in PAGES.items():
        f = os.path.join(ROOT, page if page.endswith(".html") else os.path.join(page, "index.html"))
        s = open(f, encoding="utf-8").read()
        pre = "" if page == "index.html" else "../"
        s = re.sub(r"<!--BLOGLATEST-->.*?<!--/BLOGLATEST-->", "", s, flags=re.S)
        anchor = '<section class="cta-sec dark pattern-dark" id="enrol">'
        if anchor not in s:
            print("no anchor", page); continue
        s = s.replace(anchor, section(page, cats, pre) + anchor, 1)
        open(f, "w", encoding="utf-8").write(s)
        n += 1
    # routes: every page that carries the section goes through the middleware
    r = os.path.join(ROOT, "_routes.json")
    inc = ["/api/*", "/blog", "/blog/*", "/sitemap.xml", "/llms.txt", "/"] + [f"/{p}/" for p in PAGES if p != "index.html"]
    json.dump({"version": 1, "include": inc, "exclude": ["/blog/img/*"]}, open(r, "w"))
    print("latest-from-blog on", n, "pages; routes", len(inc))


if __name__ == "__main__":
    main()
