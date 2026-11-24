#!/usr/bin/env python3
"""Keep every page in sync with the list of country pages: header Countries menu, 'explore' chips on country pages,
the country <select> in every booking form, sitemap.xml and llms.txt. Idempotent."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quranonlinetarteel.net/"
# slug, menu label, chip label, form option
COUNTRIES = [
    ("usa", "Quran Classes in USA", "Online Quran classes in USA", "United States"),
    ("uk", "Quran Classes in UK", "Online Quran classes UK", "United Kingdom"),
    ("canada", "Quran Classes in Canada", "Online Quran classes in Canada", "Canada"),
    ("australia", "Quran Classes in Australia", "Online Quran classes Australia", "Australia"),
    ("new-zealand", "Quran Classes in New Zealand", "Online Quran classes in New Zealand", "New Zealand"),
    ("ireland", "Quran Classes in Ireland", "Online Quran classes in Ireland", "Ireland"),
    ("south-africa", "Quran Classes in South Africa", "Online Quran classes in South Africa", "South Africa"),
    ("uae", "Quran Classes in UAE", "Online Quran classes in UAE", "UAE"),
    ("saudi-arabia", "Quran Classes in Saudi Arabia", "Online Quran classes in Saudi Arabia", "Saudi Arabia"),
    ("qatar", "Quran Classes in Qatar", "Online Quran classes in Qatar", "Qatar"),
    ("kuwait", "Quran Classes in Kuwait", "Online Quran classes in Kuwait", "Kuwait"),
    ("oman", "Quran Classes in Oman", "Online Quran classes in Oman", "Oman"),
    ("bahrain", "Quran Classes in Bahrain", "Online Quran classes in Bahrain", "Bahrain"),
    ("philippines", "Quran Classes in Philippines", "Online Quran classes in Philippines", "Philippines"),
    ("pakistan", "Quran Classes in Pakistan", "Online Quran classes in Pakistan", "Pakistan"),
]
SLUGS = "|".join(re.escape(c[0]) for c in COUNTRIES)


def pre(f):
    return "../" * os.path.relpath(f, ROOT).count(os.sep)


def main():
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if "/scripts/" in f or "/.git/" in f:
            continue
        s = o = open(f, encoding="utf-8").read()
        p = pre(f)
        # 1) header menu: rebuild the Countries dropdown
        def menu(m):
            ind = m.group(1)
            links = "".join(f'\n{ind}  <a href="{p}online-quran-classes-{sl}/">{ml}</a>' for sl, ml, _, _ in COUNTRIES)
            return f'{ind}<div class="qot-dropdown qot-dd-countries">{links}\n{ind}</div>'
        s = re.sub(r'([ \t]*)<div class="qot-dropdown(?: qot-dd-countries)?">\s*<a href="[./]*online-quran-classes-usa/">.*?\n\1</div>', menu, s, count=1, flags=re.S)
        # 2) explore chips on country pages: all countries except this page
        me = re.search(r"online-quran-classes-([a-z-]+)/index\.html$", f)
        me = me.group(1) if me else None
        if me in [c[0] for c in COUNTRIES] and 'class="chip"' in s:
            s = re.sub(r'<a class="chip" href="\.\./online-quran-classes-(?:%s)/">[^<]*</a>' % SLUGS, "", s)
            chips = "".join(f'<a class="chip" href="../online-quran-classes-{sl}/">{cl}</a>' for sl, _, cl, _ in COUNTRIES if sl != me)
            s = re.sub(r'(<a class="chip" href="\.\./resources/how-many-rakats/">[^<]*</a>)', lambda m: m.group(1) + chips, s, count=1)
        # 3) country select in forms
        def sel(m):
            head, body = m.group(1), m.group(2)
            chosen = re.search(r"<option selected>([^<]*)</option>", body)
            chosen = chosen.group(1) if chosen else None
            if me in [c[0] for c in COUNTRIES]:
                chosen = [c[3] for c in COUNTRIES if c[0] == me][0]
            opts = '<option value="">Select</option>' + "".join(
                f'<option{" selected" if o == chosen else ""}>{o}</option>' for o in [c[3] for c in COUNTRIES] + ["Other"])
            return head + opts + "</select>"
        s = re.sub(r'(<select id="[^"]*" name="country"[^>]*>)(.*?)</select>', sel, s, flags=re.S)
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
    # 4) sitemap
    sm = os.path.join(ROOT, "sitemap.xml")
    t = open(sm).read()
    for sl, *_ in COUNTRIES:
        u = f"{SITE}online-quran-classes-{sl}/"
        if u not in t:
            t = t.replace("  <url><loc>https://quranonlinetarteel.net/online-quran-classes-philippines/",
                          f"  <url><loc>{u}</loc><lastmod>2026-11-24</lastmod><priority>0.8</priority></url>\n  <url><loc>https://quranonlinetarteel.net/online-quran-classes-philippines/", 1)
    open(sm, "w").write(t)
    print("sitemap country urls:", sum(f"online-quran-classes-{c[0]}/" in t for c in COUNTRIES), "of", len(COUNTRIES))


if __name__ == "__main__":
    main()
