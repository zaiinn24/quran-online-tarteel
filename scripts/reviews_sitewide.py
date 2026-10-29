#!/usr/bin/env python3
"""Step 8: real family reviews. Adds a (hidden until reviews exist) reviews section to the main pages, the review form on /contact/,
and loads assets/reviews.js. Safe to run again (idempotent)."""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = ("blog", "duas-azkar", "resources", "privacy-policy", "terms", "contact", "assets", "data", "downloads", "functions", "scripts")
COURSES = ["Noorani Qaida", "Quran Reading (Nazra)", "Tajweed", "Hifz", "Translation and Tafseer", "Islamic Studies",
           "Juz Amma Memorisation", "Salah (Prayer) Lessons", "Daily Duas Course", "40 Hadith for Kids", "Classes for New Muslims"]
COUNTRIES = ["United States", "United Kingdom", "Canada", "Australia", "UAE", "Saudi Arabia", "Pakistan", "Other"]


def section(prefix, bg, limit=6, form_link=True):
    btn = (f'<div class="rv-more"><a href="{prefix}contact/#review" class="btn btn-dark">Write a review</a></div>' if form_link else "")
    return (f'<!--REVIEWS--><section class="sec {bg} reviews-sec" data-reviews data-limit="{limit}" hidden><div class="container">'
            f'<div class="section-head"><span class="eyebrow">Family Reviews</span><h2>What Families Say About Us</h2><p class="rv-sum"></p></div>'
            f'<div class="rv-grid"></div>{btn}</div></section><!--/REVIEWS-->')


def anchor(rel, s):
    """Where reviews persuade most: homepage after 'why families choose us'; course, country and fee pages right after the fees;
    about after the founder's story; free trial and female teachers right after the first section; otherwise before the FAQ."""
    def after_section(start):
        return s.index("</section>", start) + len("</section>")
    if rel == "index.html":
        return s.index('<section class="sec bg-cream" id="how"')
    if "<!--/FEES-->" in s:
        return s.index("<!--/FEES-->") + len("<!--/FEES-->")
    if "<!--/STORY-->" in s:
        return s.index("<!--/STORY-->") + len("<!--/STORY-->")
    if rel.split(os.sep)[0] in ("free-trial", "female-quran-teachers"):
        h = s.index('<section class="page-hero')
        return after_section(s.index('<section class="sec', after_section(h)))
    m = re.search(r'<section class="sec ([\w-]+)"[^>]*id="faq"', s) or re.search(r'<section class="cta-sec', s) or re.search(r'<footer', s)
    return m.start() if m else None


def add_script(s, prefix):
    s = re.sub(r'<script src="[^"]*assets/reviews\.js[^"]*" defer></script>', "", s)
    return s.replace("</body>", f'<script src="{prefix}assets/reviews.js" defer></script></body>', 1)


def form_html():
    opts = lambda xs: "".join(f"<option>{x}</option>" for x in xs)
    stars = "".join(f'<input type="radio" id="rvs{n}" name="stars" value="{n}"><label for="rvs{n}" title="{n} star{"s" if n > 1 else ""}">&#9733;</label>' for n in (5, 4, 3, 2, 1))
    return (
        '<!--REVIEWFORM--><section class="sec bg-cream" id="review"><div class="container"><div class="rv-form-wrap">'
        '<div class="rv-intro"><span class="eyebrow">Share Your Experience</span><h2>Write a Review</h2>'
        '<p>Has your child or have you learned with us? Your honest words help other families choose with confidence.</p>'
        '<ul class="rv-points"><li>Your review appears on our website straight away</li><li>Only your first name or initials, country and course are shown</li>'
        '<li>Links and website addresses are removed automatically</li></ul></div>'
        '<div class="form-card flat rv-form"><div class="form-body"><form data-review-form novalidate>'
        '<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
        '<div class="field"><span class="rv-lbl" id="rvsl">Your rating</span><div class="stars-in" role="radiogroup" aria-labelledby="rvsl">' + stars + '</div></div>'
        '<div class="field-row"><div class="field"><label for="rvn">Your name</label><input id="rvn" name="name" type="text" maxlength="40" autocomplete="given-name" placeholder="e.g. Sara or Umm Ali" required></div>'
        f'<div class="field"><label for="rvc">Country</label><select id="rvc" name="country"><option value="">Select</option>{opts(COUNTRIES)}</select></div></div>'
        f'<div class="field-row"><div class="field"><label for="rvk">Course</label><select id="rvk" name="course"><option value="">Select</option>{opts(COURSES)}</select></div>'
        '<div class="field"><label for="rvw">Who learns with us?</label><select id="rvw" name="who"><option value="">Select</option><option>My child</option><option>Myself</option></select></div></div>'
        '<div class="field"><label for="rvb">Your review</label><textarea id="rvb" name="review" maxlength="600" placeholder="How are the classes going? What do you like about your teacher?" required></textarea></div>'
        '<div class="rv-ts"></div><p class="rv-msg" role="alert"></p>'
        '<button type="submit" class="btn btn-gold">Publish my review <svg><use href="#i-arrow"/></svg></button>'
        '<p class="form-note"><svg><use href="#i-lock"/></svg>We never show your email or phone number.</p>'
        '</form></div></div></div></div></section>' + section("../", "bg-white", 12, form_link=False) + '<!--/REVIEWFORM-->')


def main():
    done = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        top = rel.split(os.sep)[0]
        if top in SKIP_DIRS or rel == "404.html":
            continue
        depth = rel.count(os.sep)
        prefix = "../" * depth
        s = open(f).read()
        s = re.sub(r"<!--REVIEWS-->.*?<!--/REVIEWS-->", "", s, flags=re.S)
        pos = anchor(rel, s)
        if pos is None:
            print("no anchor", rel); continue
        prev = re.findall(r'<section class="(?:sec )?[^"]*?(bg-[\w-]+|dark)', s[:pos])
        nxt = re.findall(r'<section class="(?:sec )?[^"]*?(bg-[\w-]+|dark)', s[pos:])
        used = {(prev[-1] if prev else ""), (nxt[0] if nxt else "")}
        bg = next(b for b in ("bg-white", "bg-cream", "bg-cream-2") if b not in used)
        s = s[:pos] + section(prefix, bg) + s[pos:]
        s = add_script(s, prefix)
        open(f, "w").write(s)
        done.append(rel)
    c = os.path.join(ROOT, "contact", "index.html")
    s = open(c).read()
    s = re.sub(r"<!--REVIEWFORM-->.*?<!--/REVIEWFORM-->", "", s, flags=re.S)
    i = s.index('<section class="sec bg-white" id="faq"')
    s = s[:i] + form_html() + s[i:]
    s = add_script(s, "../")
    open(c, "w").write(s)
    print(len(done), "pages + contact form")


if __name__ == "__main__":
    main()
