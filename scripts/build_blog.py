#!/usr/bin/env python3
"""Build the blog: scripts/blog_posts/*.md -> blog/<slug>/index.html, blog/index.html listing,
sitemap + llms.txt entries and the publish schedule used by functions/_middleware.js.

Posts with a future `date` are committed now but hidden by the Pages middleware until that date
(Pakistan time), so every post goes live on its own day without anyone touching the site."""
import glob, html, json, math, os, re
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scripts", "blog_posts")
SITE = "https://quranonlinetarteel.net"

CATS = [  # slug, label
    ("learn-quran", "Learn Quran"), ("tajweed", "Tajweed"), ("kids", "Kids and Parents"),
    ("women", "Women"), ("hifz", "Hifz"), ("salah", "Salah and Worship"),
    ("duas", "Duas and Dhikr"), ("knowledge", "Quran Knowledge"), ("ramadan", "Ramadan"),
    ("guides", "Guides and Comparisons"),
]
CAT = dict(CATS)
# older articles that already live under /resources/ (shown in the listing too)
LEGACY = [
    dict(url="../resources/tajweed-rules/", title="Tajweed Rules for Beginners", cat="tajweed", date="2026-10-20",
         excerpt="The main rules of Tajweed explained simply: noon sakinah, meem sakinah, ghunnah, qalqalah and madd.",
         img="legacy-tajweed-rules", mins=6),
    dict(url="../resources/noorani-qaida-guide/", title="Noorani Qaida Guide: Lessons, Order and Tips", cat="learn-quran",
         date="2026-10-20", excerpt="What each stage of the Noorani Qaida teaches, how long it takes and how parents can help at home.",
         img="legacy-noorani-qaida-guide", mins=6),
    dict(url="../resources/how-many-rakats/", title="How Many Rakats in Each Prayer?", cat="salah", date="2026-10-20",
         excerpt="A simple chart of the fard rakats of Fajr, Dhuhr, Asr, Maghrib and Isha, for kids and new learners.",
         img="legacy-how-many-rakats", mins=3),
]
COMPETITORS = ("tarteelequran.com", "qutor.com", "alazharclasses.com", "equranschool.com", "burujacademy.com",
               "quranacademy.io", "studioarabiya.com", "bayyinah", "learnquran.online")

SVG_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
SVG_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
SVG_USER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>'


def iv(name):
    """cache-busting version for a blog image file"""
    import hashlib
    f = os.path.join(ROOT, "blog", "img", name)
    return hashlib.md5(open(f, "rb").read()).hexdigest()[:8] if os.path.exists(f) else "0"


def esc(s):
    return html.escape(s, quote=True)


def slugify(s):
    s = re.sub(r"<[^>]+>", "", s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60]


def nice_date(d):
    y, m, dd = d.split("-")
    mon = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December"][int(m) - 1]
    return f"{int(dd)} {mon} {y}"


# ---------------------------------------------------------------- parsing
def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        raw = open(f, encoding="utf-8").read()
        _, fm, body = raw.split("---", 2)
        meta = {}
        for line in fm.strip().splitlines():
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
        meta["body"] = body.strip()
        meta["file"] = os.path.basename(f)
        posts.append(meta)
    posts.sort(key=lambda p: p["date"])
    return posts


MD = markdown.Markdown(extensions=["tables", "sane_lists"])


def md(text):
    MD.reset()
    return MD.convert(text)


def md_inline(text):
    h = md(text)
    return re.sub(r"^<p>(.*)</p>$", r"\1", h.strip(), flags=re.S)


_Q = None
_D = None


def ayah_text(ref):
    global _Q
    if _Q is None:
        _Q = {s["id"]: {v["id"]: v["text"] for v in s["verses"]} for s in json.load(open(os.path.join(ROOT, "data", "quran-uthmani.json"), encoding="utf-8"))}
    sur, a = ref.split(":")
    a1, _, a2 = a.partition("-")
    a2 = a2 or a1
    return " ".join(_Q[int(sur)][i] + " \uFD3F" + str(i).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")) + "\uFD3E" if a1 != a2 else _Q[int(sur)][i] for i in range(int(a1), int(a2) + 1))


def dua_lookup(q):
    global _D
    if _D is None:
        import sys
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import duas_data
        _D = []
        for pg in duas_data.PAGES.values():
            _D += [it for it in pg.get("items", []) if isinstance(it, tuple) and len(it) >= 7]
        try:
            import duas_more
            for pg in getattr(duas_more, "PAGES", {}).values():
                _D += [it for it in pg.get("items", []) if isinstance(it, tuple) and len(it) >= 7]
        except Exception:
            pass
    ql = q.lower()
    for it in _D:
        if ql in it[0].lower() or ql in it[2].lower() or ql in it[3].lower():
            return it
    raise SystemExit("dua not found: " + q)


def render_blocks(body, ctx):
    """Turn :::blocks into HTML placeholders, then run markdown over the rest."""
    stash = []

    def put(h):
        stash.append(h)
        return f"\n\nBLOCKX{len(stash) - 1}X\n\n"

    out, lines, i = [], body.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^:::(\w+)\s*(.*)$", line)
        if not m:
            out.append(line)
            i += 1
            continue
        kind, arg = m.group(1), m.group(2).strip()
        j = i + 1
        inner = []
        while j < len(lines) and lines[j].strip() != ":::":
            inner.append(lines[j])
            j += 1
        i = j + 1
        txt = "\n".join(inner).strip()
        if kind in ("key", "tip", "note", "warn"):
            title = arg or {"key": "Key takeaways", "tip": "Teacher's tip", "note": "Good to know", "warn": "Take care"}[kind]
            out.append(put(f'<div class="bp-box bp-{kind}"><div class="bp-box-t">{esc(title)}</div>{md(txt)}</div>'))
        elif kind == "quote":
            d = {}
            for l in inner:
                if ":" in l:
                    k, v = l.split(":", 1)
                    d[k.strip()] = v.strip()
            if d.get("ayah"):
                d.setdefault("ar", ayah_text(d["ayah"]))
                if "ref" not in d:
                    s_, a_ = d["ayah"].split(":")
                    d["ref"] = f"Quran {s_}:{a_}"
            if d.get("dua"):
                it = dua_lookup(d["dua"])
                ar = it[1]
                if isinstance(ar, tuple):
                    _, su, a1, w1, w2 = ar
                    ar = " ".join(ayah_text(f"{su}:{a1}").split()[w1 or 0:w2])
                d.setdefault("ar", ar); d.setdefault("tr", it[2]); d.setdefault("en", it[3]); d.setdefault("ref", it[6])
            h = '<figure class="bp-quote">'
            if d.get("ar"):
                h += f'<div class="q-ar" lang="ar" dir="rtl">{esc(d["ar"])}</div>'
            if d.get("tr"):
                h += f'<div class="q-tr">{esc(d["tr"])}</div>'
            if d.get("en"):
                h += f'<blockquote class="q-en">{md_inline(d["en"])}</blockquote>'
            if d.get("ref"):
                h += f'<figcaption class="q-ref">{md_inline(d["ref"])}</figcaption>'
            out.append(put(h + "</figure>"))
        elif kind == "cards":
            items = [l[2:] for l in inner if l.startswith("- ")]
            cls = "bp-cards c3" if arg == "3" else "bp-cards"
            h = f'<div class="{cls}">'
            for it in items:
                t, _, d = it.partition("|")
                t = t.strip().strip("*")
                h += f'<div class="bp-card"><h4>{md_inline(t)}</h4><p>{md_inline(d.strip())}</p></div>'
            out.append(put(h + "</div>"))
        elif kind == "steps":
            items = [re.sub(r"^\d+\.\s*", "", l) for l in inner if re.match(r"^\d+\.", l)]
            h = '<div class="bp-steps">'
            for it in items:
                h += f'<div class="bp-step"><p>{md_inline(it)}</p></div>'
            out.append(put(h + "</div>"))
        elif kind == "cta":
            parts = [p.strip() for p in arg.split("|")]
            head, text, label, link = (parts + ["", "", "Book 2 Free Classes", "/free-trial/"])[:4]
            out.append(put(f'<div class="bp-cta"><div><h4>{esc(head)}</h4><p>{md_inline(text)}</p></div>'
                           f'<a class="btn btn-gold" href="{link}">{esc(label)}</a></div>'))
        elif kind == "faq":
            qa, q = [], None
            for l in inner:
                if l.startswith("Q:"):
                    q = l[2:].strip()
                elif l.startswith("A:") and q:
                    qa.append((q, l[2:].strip()))
                    q = None
            ctx["faq"] = qa
        else:
            raise SystemExit(f"unknown block {kind} in {ctx['slug']}")
    h = md("\n".join(out))
    h = re.sub(r"<p>BLOCKX(\d+)X</p>", lambda m: stash[int(m.group(1))], h)
    return h


def fix_links(h, post, sched):
    def rep(m):
        attrs, href = m.group(1), m.group(2)
        extra = ""
        if href.startswith("http"):
            rel = "noopener"
            if any(c in href for c in COMPETITORS):
                rel = "nofollow noopener"
            extra = f' target="_blank" rel="{rel}"'
        elif href.startswith("/"):
            mm = re.match(r"^/blog/([a-z0-9-]+)/", href)
            if mm:
                tgt = mm.group(1)
                if tgt not in sched:
                    raise SystemExit(f"{post['slug']}: link to unknown post {tgt}")
                if sched[tgt] > post["date"]:
                    extra = f' data-pub="{sched[tgt]}" data-pub-mode="unwrap"'
            path = href[1:]
            if path.split("#")[0] and not path.startswith("blog/") and not os.path.exists(os.path.join(ROOT, path.split("#")[0].split("?")[0], "index.html")) \
                    and not os.path.exists(os.path.join(ROOT, path.split("#")[0])):
                raise SystemExit(f"{post['slug']}: broken internal link {href}")
            href = "../../" + path
        return f'<a{attrs} href="{href}"{extra}>'

    return re.sub(r'<a([^>]*?) href="([^"]+)">', rep, h)


def wrap_tables(h):
    def rep(m):
        cols = len(re.findall(r"<th[\s>]", m.group(1).split("</tr>")[0]))
        cls = "bp-table wide" if cols >= 5 else "bp-table"
        return f'<div class="{cls}"><table>{m.group(1)}</table></div>'
    return re.sub(r"<table>(.*?)</table>", rep, h, flags=re.S)


def add_ids(h, toc):
    used = set()

    def rep(m):
        tag, inner = m.group(1), m.group(2)
        i = slugify(inner) or "s"
        while i in used:
            i += "-2"
        used.add(i)
        if tag == "h2":
            toc.append((i, re.sub(r"<[^>]+>", "", inner)))
        return f'<{tag} id="{i}">{inner}</{tag}>'

    return re.sub(r"<(h2|h3)>(.*?)</\1>", rep, h)


# ---------------------------------------------------------------- shell
def shell_parts():
    t = open(os.path.join(ROOT, "resources", "tajweed-rules", "index.html"), encoding="utf-8").read()
    ga = t[:t.index('<meta charset="UTF-8">')]
    icon = re.search(r'<link rel="icon"[^>]*>', t).group(0)
    css = re.search(r'<link rel="stylesheet" href="\.\./\.\./assets/site\.css[^"]*">', t).group(0)
    body_start = t.index("<body")
    head_end = t.index("<main>")
    header = t[body_start:head_end].replace('data-nav="resources"', 'data-nav="blog"', 1)
    footer = t[t.index("</main>") + len("</main>"):]
    brand_svg = re.search(r'<a href="\.\./\.\./" class="qot-brand"[^>]*>\s*(<svg.*?</svg>)', t, re.S).group(1)
    return ga, icon, css, header, footer, brand_svg


def cta_section(post, n):
    t = open(os.path.join(ROOT, "resources", "how-many-rakats", "index.html"), encoding="utf-8").read()
    i = t.find("Begin Your Quran Journey")
    k = t.rfind("<section", 0, i)
    e = t.find("</section>", i) + 10
    s = t[k:e]
    s = s.replace('value="Guide: How Many Rakats"', f'value="Blog: {esc(post["h1"])}"')
    s = re.sub(r'\bf28([a-z])\b', lambda m: f"b{n}{m.group(1)}", s)
    s = s.replace('id="hs1"', f'id="bh{n}s"').replace('for="hs1"', f'for="bh{n}s"')
    s = s.replace('id="hd1"', f'id="bh{n}d"')
    return s


def head(title, desc, canon, extra_meta, ld, css_href, ga, icon, sitecss, kw=None, og_img=None, og_type="article"):
    h = ga + '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    h += f"<title>{esc(title)}</title>\n<meta name=\"description\" content=\"{esc(desc)}\">\n"
    if kw:
        h += f'<meta name="keywords" content="{esc(kw)}">\n'
    h += '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    h += f'<link rel="canonical" href="{canon}">\n'
    h += f'<meta property="og:type" content="{og_type}">\n<meta property="og:site_name" content="Quran Online Tarteel">\n'
    h += f'<meta property="og:title" content="{esc(title)}">\n<meta property="og:description" content="{esc(desc)}">\n'
    h += f'<meta property="og:url" content="{canon}">\n<meta property="og:locale" content="en_US">\n'
    if og_img:
        h += f'<meta property="og:image" content="{og_img}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        h += '<meta name="twitter:card" content="summary_large_image">\n'
        h += f'<meta name="twitter:image" content="{og_img}">\n'
    else:
        h += '<meta name="twitter:card" content="summary">\n'
    h += f'<meta name="twitter:title" content="{esc(title)}">\n<meta name="twitter:description" content="{esc(desc)}">\n'
    h += extra_meta
    h += '<meta name="theme-color" content="#14110c">\n' + icon + "\n<noscript></noscript>\n"
    h += '<link rel="preload" href="/assets/fonts/manrope-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
    h += '<link rel="preload" href="/assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
    h += sitecss.replace("../../", css_href) + "\n"
    h += f'<link rel="stylesheet" href="{css_href}assets/blog.css">\n'
    for obj in ld:
        h += '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + h + "</head>\n"


def card(p, base, big=False, pub_attr=True):
    url = p.get("url") or f'{base}{p["slug"]}/'
    img = p.get("img") or p["slug"]
    attr = f' data-pub="{p["date"]}"' if pub_attr else ""
    cls = "bl-card bl-big" if big else "bl-card"
    return (f'<a class="{cls}" href="{url}" data-cat="{p["cat"]}"{attr}>'
            f'<div class="bl-img"><img src="{base}img/{img}-640.webp?v={iv(img + "-640.webp")}" srcset="{base}img/{img}-640.webp?v={iv(img + "-640.webp")} 640w, {base}img/{img}.webp?v={iv(img + ".webp")} 1200w" '
            f'sizes="(max-width:640px) 100vw, (max-width:960px) 50vw, 400px" width="1200" height="630" loading="lazy" decoding="async" alt="{esc(p["title"])}"></div>'
            f'<div class="bl-body"><span class="bl-cat">{esc(CAT[p["cat"]])}</span><h3>{esc(p["title"])}</h3>'
            f'<p>{esc(p["excerpt"])}</p><div class="bl-foot"><span>{nice_date(p["date"])}</span><b>{p["mins"]} min read</b></div></div></a>')


# ---------------------------------------------------------------- build
def build():
    ga, icon, sitecss, header, footer, brand_svg = shell_parts()
    posts = load_posts()
    sched = json.load(open(os.path.join(SRC, "_plan.json")))  # every planned post, written or not yet
    assert len({p["slug"] for p in posts}) == len(posts), "duplicate slug"
    for p in posts:
        assert sched.get(p["slug"]) == p["date"], f'{p["slug"]}: date does not match _plan.json'
    missing = [s for s in sched if s not in {p["slug"] for p in posts}]
    if missing:
        print("NOT WRITTEN YET:", len(missing))
    for n, p in enumerate(posts, 1):
        ctx = {"slug": p["slug"], "faq": []}
        body = render_blocks(p["body"], ctx)
        body = wrap_tables(body)
        toc = []
        body = add_ids(body, toc)
        body = fix_links(body, p, sched)
        # first paragraph = intro
        body = body.replace("<p>", '<p class="bp-intro">', 1)
        words = len(re.sub(r"<[^>]+>", " ", body).split()) + sum(len((q + a).split()) for q, a in ctx["faq"])
        p["mins"] = max(3, math.ceil(words / 220))
        p["words"] = words
        p["faq"] = ctx["faq"]
        p["html"] = body
        p["toc"] = toc
        p["n"] = n
    for p in posts:
        write_post(p, posts, sched, ga, icon, sitecss, header, footer, brand_svg)
    write_index(posts, ga, icon, sitecss)
    write_schedule(posts)
    write_sitemap(posts)
    write_llms(posts)
    json.dump([{k: p[k] for k in ("slug", "title", "cat", "date", "ar", "words")} for p in posts],
              open(os.path.join(ROOT, "scripts", "blog_posts", "_index.json"), "w"), indent=1, ensure_ascii=False)
    for p in posts:
        print(p["date"], p["slug"], p["words"], "words", len(p["faq"]), "faq", len(p["toc"]), "h2")


def related_for(p, posts):
    want = [s.strip() for s in p.get("related", "").split(",") if s.strip()]
    by = {q["slug"]: q for q in posts}
    rel = [by[s] for s in want if s in by]
    for q in posts:  # same category, then nearest in time
        if len(rel) >= 6:
            break
        if q is not p and q not in rel and q["cat"] == p["cat"]:
            rel.append(q)
    for q in sorted(posts, key=lambda q: abs(int(q["date"].replace("-", "")) - int(p["date"].replace("-", "")))):
        if len(rel) >= 6:
            break
        if q is not p and q not in rel:
            rel.append(q)
    for l in LEGACY:  # always-live fallbacks, so the section is never empty
        rel.append(dict(l, url="../" + l["url"]))
    return rel


def write_post(p, posts, sched, ga, icon, sitecss, header, footer, brand_svg):
    canon = f"{SITE}/blog/{p['slug']}/"
    img = f"{SITE}/blog/img/{p['slug']}-og.webp"  # titled version for social sharing
    ld = [{
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["h1"], "description": p["desc"],
        "image": [img], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
        "mainEntityOfPage": canon, "articleSection": CAT[p["cat"]], "keywords": p["kw"], "inLanguage": "en",
        "wordCount": p["words"],
        "author": {"@type": "Organization", "name": "Quran Online Tarteel", "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": "Quran Online Tarteel", "url": SITE + "/"}}]
    if p["faq"]:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a)}}
            for q, a in p["faq"]]})
    ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": p["h1"], "item": canon}]})
    extra = (f'<meta property="article:published_time" content="{p["date"]}T00:00:00+05:00">\n'
             f'<meta property="article:section" content="{esc(CAT[p["cat"]])}">\n')
    out = head(p["title"], p["desc"], canon, extra, ld, "../../", ga, icon, sitecss, kw=p["kw"], og_img=img)
    out += header + "<main>\n"
    out += (f'<section class="page-hero pattern-dark bp-hero"><div class="container"><div class="bp-hero-in">'
            f'<span class="bp-chip">{esc(CAT[p["cat"]])}</span><h1>{esc(p["h1"])}</h1>'
            f'<p class="hero-lead">{esc(p["excerpt"])}</p>'
            f'<div class="bp-meta"><span>{SVG_USER}Quran Online Tarteel</span><span>{SVG_CAL}<time datetime="{p["date"]}">{nice_date(p["date"])}</time></span>'
            f'<span>{SVG_CLOCK}{p["mins"]} min read</span></div></div></div></section>\n')
    out += (f'<div class="bp-feature"><img src="../img/{p["slug"]}.webp?v={iv(p["slug"] + ".webp")}" width="1200" height="630" alt="{esc(p["alt"])}" '
            f'fetchpriority="high" decoding="async"></div>\n')
    toc_items = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in p["toc"])
    if p["faq"]:
        toc_items += '<li><a href="#faq">Frequently asked questions</a></li>'
    links = [l.split("=", 1) for l in p.get("side", "").split(";") if "=" in l]
    side_links = "".join(f'<a href="../../{u.strip().lstrip("/")}">{esc(t.strip())}</a>' for t, u in links)
    out += '<section class="bp-wrap"><div class="container"><div class="bp-layout">'
    out += ('<article class="bp-content">'
            f'<details class="bp-toc-m"><summary>In this article</summary><ol>{toc_items}</ol></details>'
            + p["html"] +
            f'<div class="bp-author"><div class="av">{brand_svg}</div><div><strong>Written by the Quran Online Tarteel team</strong>'
            '<p>Quran Online Tarteel is an online Quran academy where female teachers teach children and women live, one to one, '
            'in English, Urdu and Arabic. Read more <a href="../../about/">about our academy</a> or see our '
            '<a href="../../female-quran-teachers/">female Quran teachers</a>.</p></div></div></article>')
    out += ('<aside class="bp-aside">'
            f'<nav class="bp-side bp-toc" aria-label="Table of contents"><h2>In this article</h2><ol>{toc_items}</ol></nav>'
            '<div class="bp-side bp-side-cta"><h2>2 Free Classes</h2><p>Try a live one to one class with a female teacher. No payment until you decide to continue.</p>'
            '<a class="btn btn-gold" href="#enrol">Book Free Classes</a></div>'
            + (f'<div class="bp-side bp-side-links"><h2>Related courses</h2>{side_links}</div>' if side_links else "") +
            '</aside></div></div></section>\n')
    out += cta_section(p, p["n"]) + "\n"
    if p["faq"]:
        items = "".join(
            f'<details class="faq"{" open" if k == 0 else ""}><summary><h3>{esc(q)}</h3><span class="pm"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span></summary>'
            f'<div class="ans">{fix_links(md_inline(a), p, sched)}</div></details>'
            for k, (q, a) in enumerate(p["faq"]))
        out += (f'<section class="sec bg-cream" id="faq"><div class="container"><div class="section-head"><span class="eyebrow">Questions and Answers</span>'
                f'<h2>{esc(p.get("faqtitle", "Frequently Asked Questions"))}</h2></div><div class="faq-wrap">{items}</div></div></section>\n')
    rel = related_for(p, posts)
    cards = ""
    for q in rel:
        c = card(q, "../", pub_attr="url" not in q and q["date"] > p["date"])
        cards += c
    out += ('<section class="sec bg-white bp-related"><div class="container"><div class="section-head"><span class="eyebrow">Keep Reading</span>'
            f'<h2>More from the Blog</h2></div><div class="fgrid bl-grid" data-limit="3">{cards}</div>'
            '<p style="text-align:center;margin-top:30px"><a class="btn btn-gold" href="../">See all articles</a></p></div></section>\n')
    out += "</main>\n" + footer.replace("<footer", "<footer", 1)
    out = out.replace("</body>", BLOG_JS + "</body>")
    d = os.path.join(ROOT, "blog", p["slug"])
    os.makedirs(d, exist_ok=True)
    assert "—" not in out, f"em dash in {p['slug']}"
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)


# small script: hide not-yet-published cards (backup for the middleware), cap related cards, highlight TOC
BLOG_JS = """<script>(function(){var t=new Date(Date.now()+5*36e5).toISOString().slice(0,10);
document.querySelectorAll('[data-pub]').forEach(function(e){if(e.getAttribute('data-pub')>t){if(e.getAttribute('data-pub-mode')==='unwrap'){e.replaceWith(document.createTextNode(e.textContent))}else{e.remove()}}});
document.querySelectorAll('[data-limit]').forEach(function(g){var n=+g.getAttribute('data-limit');[].slice.call(g.children).forEach(function(c,i){if(i>=n)c.remove()})});
var l=[].slice.call(document.querySelectorAll('.bp-toc a'));if(l.length&&'IntersectionObserver'in window){var m={};l.forEach(function(a){m[a.getAttribute('href').slice(1)]=a});
var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){l.forEach(function(a){a.classList.remove('on')});var a=m[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-20% 0px -70% 0px'});
Object.keys(m).forEach(function(id){var h=document.getElementById(id);if(h)o.observe(h)})}})();</script>
"""

INDEX_JS = """<script>(function(){var t=new Date(Date.now()+5*36e5).toISOString().slice(0,10);
var g=document.getElementById('blGrid');[].slice.call(g.querySelectorAll('[data-pub]')).forEach(function(e){if(e.getAttribute('data-pub')>t)e.remove()});
var cards=[].slice.call(g.children);if(cards[0])cards[0].classList.add('bl-big');
var bs=[].slice.call(document.querySelectorAll('.bl-filters button'));
bs.forEach(function(b){var c=b.getAttribute('data-f');var n=c==='all'?cards.length:cards.filter(function(x){return x.getAttribute('data-cat')===c}).length;
 var s=b.querySelector('span');if(s)s.textContent=n;if(!n&&c!=='all')b.remove()});
function go(c){bs.forEach(function(b){b.classList.toggle('on',b.getAttribute('data-f')===c)});var first=true;
 cards.forEach(function(x){var on=c==='all'||x.getAttribute('data-cat')===c;x.hidden=!on;x.classList.remove('bl-big');if(on&&first&&c==='all'){x.classList.add('bl-big')}if(on)first=false})}
bs.forEach(function(b){b.addEventListener('click',function(){var c=b.getAttribute('data-f');go(c);history.replaceState(null,'',c==='all'?location.pathname:'#'+c)})});
var h=location.hash.slice(1);if(h&&document.querySelector('.bl-filters [data-f="'+h+'"]'))go(h)})();</script>
"""


def write_index(posts, ga, icon, sitecss):
    p0 = os.path.join(ROOT, "blog", "index.html")
    t = open(p0, encoding="utf-8").read()
    body_start = t.index("<body")
    header = t[body_start:t.index("<main>")]
    footer = t[t.index("</main>") + len("</main>"):]
    footer = re.sub(r"<script>\(function\(\)\{var t=new Date.*?</script>\n", "", footer, flags=re.S)
    canon = SITE + "/blog/"
    title = "Quran Blog: Learn Quran, Tajweed, Duas and Salah Guides"
    desc = ("Free guides from Quran Online Tarteel: learn the Quran online, Tajweed rules, Hifz tips, duas, dhikr, "
            "salah and Ramadan, written for parents, kids and women.")
    items = sorted(posts + LEGACY, key=lambda p: p["date"], reverse=True)
    ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Quran Online Tarteel Blog", "url": canon,
           "description": desc, "publisher": {"@type": "Organization", "name": "Quran Online Tarteel", "url": SITE + "/"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Blog", "item": canon}]}]
    out = head(title, desc, canon, "", ld, "../", ga, icon, sitecss.replace("../../", "../../"), og_img=f"{SITE}/blog/img/blog-cover-og.webp", og_type="website")
    out = out.replace('href="../../assets/site.css', 'href="../assets/site.css')
    out += header + "<main>\n"
    out += ('<section class="page-hero pattern-dark center"><div class="container page-hero-grid"><div class="hero-text">'
            '<span class="eyebrow">Articles and Guides</span><h1>The Quran Online Tarteel <span class="gold">Blog</span></h1>'
            '<p class="hero-lead">Practical guides for parents, children and sisters learning the Quran: reading, Tajweed, Hifz, '
            'duas, salah and Ramadan, written by an academy that teaches in English, Urdu and Arabic.</p></div></div></section>\n')
    chips = '<button type="button" class="on" data-f="all">All articles<span></span></button>' + "".join(
        f'<button type="button" data-f="{s}" id="{s}">{esc(l)}<span></span></button>' for s, l in CATS)
    cards = "".join(card(p, "", pub_attr="url" not in p) for p in items)
    out += ('<section class="sec bg-cream"><div class="container"><div class="section-head"><span class="eyebrow">Browse by Topic</span>'
            '<h2>Latest Articles on Learning the Quran</h2></div>'
            f'<div class="bl-filters" role="toolbar" aria-label="Filter articles by category">{chips}</div>'
            f'<div class="bl-grid" id="blGrid">{cards}</div></div></section>\n')
    out += ('<section class="sec bg-white"><div class="container" style="text-align:center;max-width:820px">'
            '<span class="eyebrow">Learn with a Teacher</span><h2>Ready to Learn the Quran Properly?</h2>'
            '<p style="color:var(--muted);margin:14px auto 26px">Articles help, but recitation is learned by listening and being corrected. '
            'Our female teachers teach <a href="../online-quran-classes-for-kids/">online Quran classes for kids</a>, '
            '<a href="../online-quran-classes-for-women/">Quran classes for women</a>, <a href="../noorani-qaida-online/">Noorani Qaida</a>, '
            '<a href="../online-tajweed-classes/">Tajweed</a> and the <a href="../online-hifz-program/">Hifz program</a>, live and one to one.</p>'
            '<a class="btn btn-gold" href="../free-trial/">Book 2 Free Classes</a></div></section>\n')
    out += "</main>\n" + footer
    out = out.replace("</body>", INDEX_JS + "</body>")
    assert "—" not in out
    open(p0, "w", encoding="utf-8").write(out)


def write_schedule(posts):
    f = os.path.join(ROOT, "functions", "_middleware.js")
    s = open(f, encoding="utf-8").read()
    sched = json.dumps({p["slug"]: p["date"] for p in posts}, indent=0)
    s = re.sub(r"const SCHEDULE = \{.*?\};", "const SCHEDULE = " + sched + ";", s, flags=re.S)
    open(f, "w", encoding="utf-8").write(s)


def write_sitemap(posts):
    f = os.path.join(ROOT, "sitemap.xml")
    s = open(f, encoding="utf-8").read()
    s = re.sub(r"\s*<url><loc>https://quranonlinetarteel\.net/blog/[a-z0-9-]+/</loc>.*?</url>", "", s)
    add = "".join(f'\n  <url><loc>{SITE}/blog/{p["slug"]}/</loc><lastmod>{p.get("updated", p["date"])}</lastmod><priority>0.7</priority></url>'
                  for p in posts)
    s = s.replace("\n</urlset>", add + "\n</urlset>")
    open(f, "w", encoding="utf-8").write(s)


def write_llms(posts):
    f = os.path.join(ROOT, "llms.txt")
    s = open(f, encoding="utf-8").read()
    block = "## Blog articles\n\n" + "".join(f'- [{p["h1"]}]({SITE}/blog/{p["slug"]}/): {p["desc"]}\n' for p in posts)
    if "## Blog articles" in s:
        s = re.sub(r"## Blog articles\n\n(?:- .*\n)*", block, s)
    else:
        s = s.rstrip("\n") + "\n\n" + block
    open(f, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    build()
