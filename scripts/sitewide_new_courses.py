#!/usr/bin/env python3
"""Wire the 5 new course pages into the whole site: forms, nav, footer, homepage grid, explore chips, sitemap. Safe to re-run."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW = [  # slug, nav label, chip text, form option
    ("juz-amma-memorization-online", "Juz Amma Memorisation", "Juz Amma memorization online", "Juz Amma Memorisation"),
    ("online-salah-classes", "Salah (Namaz) Classes", "Online salah classes", "Salah (Prayer) Lessons"),
    ("online-duas-course", "Daily Duas Course", "Masnoon duas course", "Daily Duas Course"),
    ("40-hadith-for-kids", "40 Hadith for Kids", "40 Hadith for kids", "40 Hadith for Kids"),
    ("quran-classes-for-new-muslims", "Classes for New Muslims", "Quran classes for new Muslims", "Classes for New Muslims"),
]
CARDS = [
    ("juz-amma-memorization-online", "Short surahs", "عَمَّ", "Juz Amma Memorisation", "Memorize the 37 short surahs of Amma Para with Tajweed and a daily revision plan.", "Juz Amma memorization"),
    ("online-salah-classes", "Prayer", "صَلَاة", "Salah (Namaz) Classes", "Learn wudu and how to pray step by step: what to do, what to recite and how many rakats.", "Online salah classes"),
    ("online-duas-course", "Daily duas", "دُعَاء", "Daily Duas Course", "Masnoon duas, morning and evening adhkar and Rabbana duas with meaning.", "Masnoon duas course"),
    ("40-hadith-for-kids", "Kids", "حَدِيث", "40 Hadith for Kids", "Short, authentic hadith with meaning, a story and a lesson for daily life.", "40 Hadith for kids"),
    ("quran-classes-for-new-muslims", "New Muslims", "شَهَادَة", "Classes for New Muslims", "Gentle classes for revert sisters and their children: salah, Al-Fatiha and Quran reading.", "Classes for new Muslims"),
]
ARROW = '<svg width="14" height="14"><use href="#i-arrow"/></svg>'

for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = o = open(f).read()
    rel = os.path.relpath(f, ROOT)
    pre = "" if rel in ("index.html", "404.html") else "../" * (rel.count("/"))
    if rel == "404.html":
        m = re.search(r'href="([^"]*)online-islamic-studies/"', s)
        pre = m.group(1) if m else "/"
    # 1. form course options
    opts = "".join(f"<option>{o4}</option>" for _, _, _, o4 in NEW)
    s = re.sub(r'(<option(?: selected)?>Islamic Studies</option>)(?!<option>Juz Amma)', lambda m: m.group(1) + opts, s)
    # 2. nav dropdown
    if "qot-dropdown" in s and 'online-salah-classes/">Salah' not in s:
        s = re.sub(r'(<a href="([^"]*)online-islamic-studies/">Islamic Studies</a>)',
                   lambda m: m.group(1) + "".join(f'\n            <a href="{m.group(2)}{sl}/">{lab}</a>' for sl, lab, _, _ in NEW), s, count=1)
    # 3. footer courses
    if "<h4>Courses</h4>" in s and 'online-salah-classes/">Salah Classes' not in s:
        s = re.sub(r'(<li><a href="([^"]*)online-hifz-program/">Hifz Program</a></li>)',
                   lambda m: m.group(1) + f'\n        <li><a href="{m.group(2)}juz-amma-memorization-online/">Juz Amma Memorisation</a></li>'
                   f'\n        <li><a href="{m.group(2)}online-salah-classes/">Salah Classes</a></li>'
                   f'\n        <li><a href="{m.group(2)}quran-classes-for-new-muslims/">New Muslims</a></li>', s, count=1)
    # 4. explore chips
    if 'class="chip-row"' in s and 'class="chip" href="' + pre + 'online-salah-classes/"' not in s:
        s = re.sub(r'(<a class="chip" href="([^"]*)free-trial/">[^<]*</a>)',
                   lambda m: "".join(f'<a class="chip" href="{m.group(2)}{sl}/">{chip}</a>' for sl, _, chip, _ in NEW if sl not in rel) + m.group(1), s, count=1)
    if s != o:
        open(f, "w").write(s)

# 5. homepage course grid
p = os.path.join(ROOT, "index.html")
s = open(p).read()
if 'class="course" href="online-salah-classes/"' not in s:
    cards = "".join(
        f'\n      <a class="course" href="{sl}/">\n        <div class="course-top"><span class="course-tag">{tag}</span><span class="ar">{ar}</span></div>\n'
        f'        <div class="course-body">\n          <h3>{h}</h3>\n          <p>{p_}</p>\n          <span class="more">{more} <span>{ARROW}</span></span>\n        </div>\n      </a>'
        for sl, tag, ar, h, p_, more in CARDS)
    i = s.index('<a class="course" href="online-islamic-studies/">')
    j = s.index("</a>", i) + 4
    s = s[:j] + cards + s[j:]
    s = s.replace("<p>Eight structured courses, one clear path.", "<p>Thirteen structured courses, one clear path.")
    open(p, "w").write(s)

# 6. sitemap
p = os.path.join(ROOT, "sitemap.xml")
s = open(p).read()
for sl, *_ in NEW:
    if f"/{sl}/" not in s:
        s = s.replace("</urlset>", f"  <url><loc>https://quranonlinetarteel.net/{sl}/</loc><lastmod>2026-10-29</lastmod><priority>0.8</priority></url>\n</urlset>")
open(p, "w").write(s)
print("wired")
