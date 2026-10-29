#!/usr/bin/env python3
"""Our own colour Noorani Qaida (Urdu instructions, English help).
Teaching method of the traditional Noorani Qaida: classic lesson order, colour-coded harakat, letters joined in different colours so the
broken shapes are visible, and hijje (spelling) under every practice word. All pages, wording and layout are our own.
Arabic is shaped with HarfBuzz and drawn as vector SVG so every haraka can have its own colour.
Surahs: King Fahd Complex Uthmani text (data/quran-uthmani.json).
Usage: TMPDIR=<dir> python3 scripts/build_qaida_color.py <fonts_dir>"""
import os, sys, io, json, subprocess, html as H
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import uharfbuzz as hb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = sys.argv[1] if len(sys.argv) > 1 else "."
Q = json.load(open(os.path.join(ROOT, "data", "quran-uthmani.json")))
from quran_text import fix as _qfix
for _s in Q:
    for _v in _s["verses"]:
        _v["text"] = _qfix(_v["text"])
OUT_HTML = os.path.join(os.environ.get("TMPDIR", "/tmp"), "qaida-color.html")
OUT_PDF = os.path.join(ROOT, "downloads", "noorani-qaida-quran-online-tarteel.pdf")
UD = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
AD = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

# ---------------- colours ----------------
INK = "#111111"
RED, BLUE, GREEN, ORANGE, PURPLE, PINK = "#d0021b", "#1257c4", "#178a2e", "#e86a00", "#7b2cbf", "#c2185b"
F, K, D = "َ", "ِ", "ُ"
FT, KT, DT = "ً", "ٍ", "ٌ"
SUK, SHAD, MADD = "ْ", "ّ", "ٓ"
KZ, KE, UP = "ٰ", "ٖ", "ٗ"
MARK_COLOR = {F: RED, FT: RED, KZ: RED, K: BLUE, KT: BLUE, KE: BLUE, D: GREEN, DT: GREEN, UP: GREEN,
              SUK: ORANGE, "ۡ": ORANGE, SHAD: PURPLE, MADD: PINK, "ٔ": INK, "ٕ": INK}
VOWELS = {F: "زبر", K: "زیر", D: "پیش", FT: "دو زبر", KT: "دو زیر", DT: "دو پیش", KZ: "کھڑا زبر", KE: "کھڑی زیر", UP: "اُلٹا پیش"}
VCOL = {F: RED, FT: RED, KZ: RED, K: BLUE, KT: BLUE, KE: BLUE, D: GREEN, DT: GREEN, UP: GREEN}
ALT = [RED, BLUE, GREEN, PURPLE]

# ---------------- font + shaping ----------------
_f = TTFont(f"{FONTS}/fontsource-amiri-5.3.0/files/amiri-arabic-400-normal.woff2")
_f.flavor = None
_b = io.BytesIO(); _f.save(_b)
FONT = hb.Font(hb.Face(_b.getvalue()))
GS = _f.getGlyphSet()
NAMES = _f.getGlyphOrder()
GDEF = _f["GDEF"].table.GlyphClassDef.classDefs
UPEM = _f["head"].unitsPerEm
REV = {}
for cp, gn in _f.getBestCmap().items():
    REV.setdefault(gn, chr(cp))
BOX_TOP, BOX_BOT, PAD = 820, -380, 40   # minimum box (font units); grows to fit marks and tails
_paths = {}


def gpath(gn):
    if gn not in _paths:
        pen = SVGPathPen(GS)
        GS[gn].draw(pen)
        _paths[gn] = pen.getCommands()
    return _paths[gn]


def ar(text, size=40, base_colors=None, title=None):
    """Shape `text` and return an inline SVG. Marks are coloured by type; base letters black unless base_colors[char_index] is set."""
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    buf.cluster_level = hb.BufferClusterLevel.MONOTONE_CHARACTERS
    hb.shape(FONT, buf)
    x = 0
    parts = []
    used = {}
    top, bot, left, right = BOX_TOP, BOX_BOT, 0, 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        ext = FONT.get_glyph_extents(info.codepoint)
        if ext and ext.width:
            gx, gy = x + pos.x_offset, pos.y_offset
            top = max(top, gy + ext.y_bearing + PAD)
            bot = min(bot, gy + ext.y_bearing + ext.height - PAD)
            left = min(left, gx + ext.x_bearing - PAD)
            right = max(right, gx + ext.x_bearing + ext.width + PAD)
        gn = NAMES[info.codepoint]
        cl = info.cluster
        is_mark = GDEF.get(gn) == 3
        col = INK
        if is_mark:
            ch = REV.get(gn)
            if ch is None or ch not in MARK_COLOR:
                # unnamed mark variant: use the marks of this cluster in order
                marks = [c for c in text[cl:cl + 4] if c in MARK_COLOR]
                k = used.get(cl, 0); used[cl] = k + 1
                ch = marks[k] if k < len(marks) else None
            col = MARK_COLOR.get(ch, INK)
        elif base_colors and cl in base_colors:
            col = base_colors[cl]
        d = gpath(gn)
        if d:
            parts.append(f'<path transform="translate({x + pos.x_offset},{pos.y_offset})" fill="{col}" d="{d}"/>')
        x += pos.x_advance
    right = max(right, x)
    w, hh = right - left, top - bot
    hpx = size * hh / UPEM
    wpx = size * w / UPEM
    t = f'<title>{H.escape(title or text)}</title>'
    return (f'<svg class="a" role="img" aria-label="{H.escape(title or text)}" width="{wpx:.1f}" height="{hpx:.1f}" viewBox="{left} {-top} {w} {hh}">{t}'
            f'<g transform="scale(1,-1)">{"".join(parts)}</g></svg>')


# ---------------- letters + hijje ----------------
LETTERS = [("ا", "الف"), ("ب", "با"), ("ت", "تا"), ("ث", "ثا"), ("ج", "جیم"), ("ح", "حا"), ("خ", "خا"), ("د", "دال"), ("ذ", "ذال"),
           ("ر", "را"), ("ز", "زا"), ("س", "سین"), ("ش", "شین"), ("ص", "صاد"), ("ض", "ضاد"), ("ط", "طا"), ("ظ", "ظا"), ("ع", "عین"),
           ("غ", "غین"), ("ف", "فا"), ("ق", "قاف"), ("ك", "کاف"), ("ل", "لام"), ("م", "میم"), ("ن", "نون"), ("و", "واؤ"), ("ه", "ہا"),
           ("ء", "ہمزہ"), ("ي", "یا")]
NAME = dict(LETTERS)
NAME.update({"أ": "الف", "إ": "الف", "آ": "الف", "ة": "گول تا", "ى": "یا", "ؤ": "واؤ", "ئ": "یا"})
NONJOIN = set("اأإآدذرزوؤء")
ALL = [l for l, _ in LETTERS]
CONS = [l for l in ALL if l != "ا"]
ISMARK = lambda c: "ً" <= c <= "ٟ" or c in (KZ, "ۡ")


def units(word):
    u = []
    for c in word:
        if ISMARK(c) and u:
            u[-1][1] += c
        else:
            u.append([c, ""])
    return u


def vowel_of(m):
    for v in (FT, KT, DT, F, K, D, KZ, KE, UP):
        if v in m:
            return v
    return None


def syl(text, color):
    return f'<span class="sy" style="color:{color}" lang="ar">{text}</span>'


def hijje(word):
    """Urdu spelling, e.g. کاف زبر کَ، تا زبر تَ، با زبر بَ: کَتَبَ"""
    u = units(word)
    steps = []
    i = 0
    while i < len(u):
        c, m = u[i]
        v = vowel_of(m)
        if not v:
            i += 1
            continue
        s = c + m
        parts = [NAME.get(c, c)]
        if SHAD in m:
            parts.append("شد")
        nxt = u[i + 1] if i + 1 < len(u) else None
        if nxt and v in (F, FT) and nxt[0] == "ا" and not vowel_of(nxt[1]):
            if v == F:
                parts.append("الف")
            s += nxt[0] + nxt[1]; i += 1
            if MADD in nxt[1]:
                parts.append("مد")
        elif nxt and ((v == K and nxt[0] == "ي") or (v == D and nxt[0] == "و")) and not vowel_of(nxt[1]) and SUK not in nxt[1]:
            parts.append(NAME[nxt[0]]); s += nxt[0] + nxt[1]; i += 1
            if MADD in nxt[1]:
                parts.append("مد")
        parts.append(VOWELS[v])
        steps.append(f'{" ".join(parts)} {syl(s, VCOL[v])}')
        if i + 1 < len(u) and (SUK in u[i + 1][1] or "ۡ" in u[i + 1][1]):
            c2, m2 = u[i + 1]
            s2 = s + c2 + m2
            steps.append(f'{NAME.get(c2, c2)} جزم {syl(s2, ORANGE)}')
            i += 1
        i += 1
    return "، ".join(steps) + f' <b>=</b> {syl(word, INK)}'


# ---------------- extra marks used by the Quran text (standard Unicode after quran_text.fix) ----------------
TEAL, GREY = "#00897b", "#9e9e9e"
OFT, ODT, OKT = "ࣰ", "ࣱ", "ࣲ"
MARK_COLOR.update({c: RED for c in "\u06d6\u06d7\u06d8\u06d9\u06da\u06db"})
MARK_COLOR.update({OFT: RED, OKT: BLUE, ODT: GREEN, "۟": GREY, "ۥ": GREEN, "ۦ": BLUE, "ۢ": TEAL, "ۭ": TEAL})
VOWELS.update({OFT: "دو زبر", ODT: "دو پیش", OKT: "دو زیر"})
VCOL.update({OFT: RED, ODT: GREEN, OKT: BLUE})
NAME.update({"ؤ": "ہمزہ", "ئ": "ہمزہ"})
ISMARK = lambda c: ("ً" <= c <= "ٟ") or c == "ٰ" or ("ۖ" <= c <= "ۭ") or ("ࣰ" <= c <= "ࣲ")


def vowel_of(m):
    if KZ in m:
        return KZ
    for v in (FT, KT, DT, OFT, ODT, OKT, F, K, D, KE, UP):
        if v in m:
            return v
    return None


import qaida_mine as QM

SURAH_UR = {s["id"]: s["name"] for s in Q}


def ref(s, a):
    return f'{SURAH_UR[s]} {str(s).translate(AD)}:{str(a).translate(AD)}'


# ---------------- page builders ----------------
PAGES = []
LESSONS = []   # (lesson number, urdu title, first page)


def page(lesson, ur_title, en_title, body, ur_note, en_note, legend=True, part=""):
    n = len(PAGES) + 3   # cover = 1, contents = 2
    if not LESSONS or LESSONS[-1][0] != lesson:
        LESSONS.append((lesson, ur_title, n))
    leg = ""
    if legend:
        leg = ('<div class="legend">' + "".join(f'<span style="--c:{c}"><i></i>{t}</span>' for t, c in
               [("زبر", RED), ("زیر", BLUE), ("پیش", GREEN), ("جزم", ORANGE), ("شد", PURPLE), ("مد", PINK)]) + '</div>')
    PAGES.append(
        f'<section class="pg"><div class="frame"><header><div class="hd-row"><span class="pno">صفحہ {str(n).translate(UD)}</span>'
        f'<span class="sabaq">سبق نمبر {str(lesson).translate(UD)}{part}</span><span class="bk">نورانی قاعدہ</span></div>'
        f'<h2>{ur_title}</h2><span class="en">Lesson {lesson} · {en_title}</span></header>{leg}'
        f'<div class="body">{body}</div>'
        f'<div class="note"><p class="ur-note"><b>ہدایات:</b> {ur_note}</p><p class="en-note">{en_note}</p></div>'
        f'<footer><span>quranonlinetarteel.net</span><span>Page {n}</span></footer></div></section>')


def grid(items, cols, cls="", rows=None):
    n = rows or -(-len(items) // cols)
    items = list(items) + [("", "")] * (n * cols - len(items))
    wgt = n * (1.8 if "hj" in cls else (1.35 if "ph" in cls else 1))
    return (f'<div class="grid {cls}" style="grid-template-columns:repeat({cols},1fr);flex:{wgt}">' + "".join(
        f'<div class="cell">{a}' + (f'<span class="nm">{b}</span>' if b else "") + "</div>" for a, b in items) + "</div>")


def chunks(lst, n):
    """split into pages of at most n items, balanced so the last page is not nearly empty"""
    pages = max(1, -(-len(lst) // n))
    per = -(-len(lst) // pages)
    return [lst[i:i + per] for i in range(0, len(lst), per)]


def part_label(i, total):
    return f" ({str(i + 1).translate(UD)})" if total > 1 else ""


def word_pages(lesson, ur_title, en_title, words, ur_note, en_note, per=12, size=56):
    import re as _re
    longest = max(len(_re.sub("<[^>]+>", "", hijje(w))) for w in words)
    cols = 3
    if longest > 95:
        per, size, cols = 8, 56, 2
    cs = chunks(words, per)
    for i, ch in enumerate(cs):
        page(lesson, ur_title, en_title, grid([(ar(w, size), hijje(w)) for w in ch], cols, "hj"),
             ur_note, en_note, part=part_label(i, len(cs)))


def drill_pages(lesson, ur_title, en_title, items, ur_note, en_note, per=48, cols=6, size=36):
    cs = chunks(items, per)
    for i, ch in enumerate(cs):
        page(lesson, ur_title, en_title, grid([(ar(x, size), "") for x in ch], cols, "tight"), ur_note, en_note, part=part_label(i, len(cs)))


def phrase(a, b, s, v, hl_a=None, hl_b=0, ca=ORANGE, cb=TEAL, size=44, whole_b=False):
    text = a + " " + b
    cols = {}
    if hl_a is not None:
        cols[hl_a] = ca
    if whole_b:
        cols.update({k: cb for k in range(len(a) + 1, len(text))})
    else:
        cols[len(a) + 1 + hl_b] = cb
    return (ar(text, size, cols), "")


def last_base_index(w):
    """index of the last base letter carrying the rule (skip a trailing silent alif after fathatan)"""
    idx = [i for i, c in enumerate(w) if not ISMARK(c)]
    if len(idx) > 1 and w[idx[-1]] == "ا" and not any(ISMARK(c) for c in w[idx[-1] + 1:]):
        return idx[-2]
    return idx[-1]


L = 0


def lesson():
    global L
    L += 1
    return L


# ===== 1. single letters + look-alike letters =====
n = lesson()
page(n, "حروفِ مفردات", "Single Letters",
     grid([(ar(l, 64), f'<span style="color:{ALT[i % 3]}">{nm}</span>') for i, (l, nm) in enumerate(LETTERS)], 5, "big"),
     "ہر حرف کو اس کے نام سے صاف اور درست مخرج کے ساتھ پڑھیں۔ دائیں سے بائیں پڑھیں اور ہر خانے پر انگلی رکھیں۔ پہلے استاد سے سنیں، پھر خود دہرائیں۔",
     "Read each letter by its name, right to left, pointing to every box. Listen to your teacher first, then repeat.", legend=False, part=" (ا)")
groups = [("بتث", "نقطوں سے پہچانیں"), ("جحخ", "نقطہ اندر، کوئی نہیں، اوپر"), ("دذ", ""), ("رز", ""), ("سش", ""), ("صض", ""), ("طظ", ""), ("عغ", ""), ("فق", "فا ایک نقطہ، قاف دو"), ("ءا", "ہمزہ اور الف الگ ہیں"), ("هة", "ہا اور گول تا"), ("وي", "")]
gitems = []
for g, tip in groups:
    letters = "&nbsp;&nbsp;".join(ar(ch, 52, {0: ALT[k % 3]}) for k, ch in enumerate(g)).replace("&nbsp;&nbsp;", '<span class="sp"></span>')
    names = " · ".join(f'<span style="color:{ALT[k % 3]}">{NAME.get(ch, "گول تا")}</span>' for k, ch in enumerate(g))
    gitems.append((f'<span class="row-ar">{letters}</span>', names + (f"<small>{tip}</small>" if tip else "")))
page(n, "ملتی جلتی شکل والے حروف", "Look-alike Letters", grid(gitems, 3, "words"),
     "یہ حروف شکل میں ملتے جلتے ہیں، فرق صرف نقطوں یا چھوٹی سی علامت کا ہے۔ ہر خانے میں نقطوں کو گن کر حرف پہچانیں اور نام لیں۔",
     "These letters look alike; only the dots or a small stroke differ. Count the dots and name each letter.", legend=False, part=" (ب)")

# ===== 2. joined letters =====
n = lesson()
ZWJ = "‍"
forms = []
for l, nm in LETTERS:
    if l == "ء":
        continue
    if l in NONJOIN:
        forms.append((nm, [l, ZWJ + l, "—", "—"]))
    else:
        forms.append((nm, [l, ZWJ + l, ZWJ + l + ZWJ, l + ZWJ]))
head = [("", "<b>نام</b>"), ("", "<b>الگ</b>"), ("", "<b>آخر</b>"), ("", "<b>درمیان</b>"), ("", "<b>شروع</b>")]
for i, ch in enumerate(chunks(forms, 14)):
    items = list(head)
    for nm, fs in ch:
        items.append(("", f'<span class="fname">{nm}</span>'))
        for k, f in enumerate(fs):
            items.append((ar(f, 34, {0: RED, 1: RED}) if f != "—" else '<span class="dash">—</span>', ""))
    page(n, "حروف کی شکلیں: شروع، درمیان، آخر", "Letter Shapes", grid(items, 5, "forms"),
         "جملے میں حرف کی شکل اس کی جگہ کے مطابق بدلتی ہے: شروع میں، درمیان میں اور آخر میں۔ ہر سطر میں ایک ہی حرف کی چاروں شکلیں ہیں۔ چھ حروف (ا د ذ ر ز و) اگلے حرف سے نہیں ملتے۔",
         "A letter's shape changes with its place in a word: start, middle, end. Six letters (ا د ذ ر ز و) never join to the next letter.",
         legend=False, part=f" ({str(i + 1).translate(UD)})")


def formula(a, b):
    top = f'{ar(b, 24, {0: BLUE})}<span class="plus">+</span>{ar(a, 24, {0: RED})}'
    return f'{ar(a + b, 46, {0: RED, 1: BLUE})}<span class="fx">{top}</span>'


seq = [l for l in ALL if l != "ء"]
page(n, "حروفِ مرکبات: الف کے ساتھ", "Joined Letters with Alif", grid([(formula(l, "ا"), "") for l in seq if l not in NONJOIN], 6, "fx-grid"),
     "جب حرف دوسرے حرف سے ملتا ہے تو اس کی شکل ٹوٹ جاتی ہے۔ سرخ حصہ پہلا حرف ہے اور نیلا دوسرا۔ ہر جوڑ کو یوں پڑھیں: «با: بے الف»۔",
     "Letters change shape when they join. The red part is the first letter, the blue part the second.", legend=False, part=" (الف)")
pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1) if seq[i] not in NONJOIN]
pairs += [("ل", "ا"), ("ب", "ي"), ("ن", "ي"), ("ت", "ي"), ("ف", "ي"), ("ك", "م"), ("ل", "م"), ("س", "ل"), ("ه", "م"), ("ع", "ن"), ("ف", "ي"), ("ح", "م")]
for i, ch in enumerate(chunks(pairs[:36], 36)):
    page(n, "حروفِ مرکبات: دو حروف", "Joined Letters: Pairs", grid([(formula(a, b), "") for a, b in ch], 6, "fx-grid"),
         "ہر خانے میں اوپر دو الگ حروف ہیں اور نیچے وہی حروف ملے ہوئے۔ ٹوٹی ہوئی شکل کو پہچانیں اور حروف کے نام لے کر پڑھیں۔",
         "Each box shows two separate letters and, below, the same letters joined. Spot the broken shape and name the letters.", legend=False,
         part=f" ({str(i + 1).translate(UD)})")
trip = []
for i in range(0, len(seq) - 2):
    a, b, c = seq[i], seq[i + 1], seq[i + 2]
    if a not in NONJOIN and b not in NONJOIN:
        trip.append(a + b + c)
trip += ["بسم", "قلم", "علم", "نعم", "لكم", "منه", "فيه", "حمد", "سجد", "غفر", "شكر", "صبر", "خلق", "رزق", "كتب", "نصر"]
for i, ch in enumerate(chunks(trip[:32], 32)):
    page(n, "حروفِ مرکبات: تین حروف", "Joined Letters: Three Letters",
         grid([(ar(t, 46, {0: RED, 1: BLUE, 2: GREEN}), " ".join(f'<span style="color:{c}">{NAME[x]}</span>' for x, c in zip(t, (RED, BLUE, GREEN)))) for t in ch], 4, "words"),
         "تین حروف ملے ہوئے ہیں: سرخ پہلا، نیلا دوسرا اور سبز تیسرا حرف۔ نیچے لکھے ناموں کو دیکھ کر ہر حرف کو الگ پہچانیں۔",
         "Three joined letters: red is the first, blue the second, green the third. Name each one.", legend=False, part=f" ({str(i + 1).translate(UD)})")

# ===== 3. muqattaat =====
n = lesson()
muq = [(2, 1), (7, 1), (10, 1), (13, 1), (19, 1), (20, 1), (26, 1), (27, 1), (36, 1), (38, 1), (40, 1), (42, 2), (50, 1), (68, 1)]
MUQ_UR = {2: "الف لام میم", 7: "الف لام میم صاد", 10: "الف لام را", 13: "الف لام میم را", 19: "کاف ہا یا عین صاد", 20: "طا ہا",
          26: "طا سین میم", 27: "طا سین", 36: "یا سین", 38: "صاد", 40: "حا میم", 42: "عین سین قاف", 50: "قاف", 68: "نون"}
first = lambda s, a: Q[s - 1]["verses"][a - 1]["text"].split(" ")[0].rstrip("ۚۖۗۛ")
page(n, "حروفِ مقطعات", "Disjoined Letters",
     grid([(ar(first(s, a), 50), MUQ_UR[s]) for s, a in muq], 4, "words"),
     "یہ حروف قرآن مجید کی بعض سورتوں کے شروع میں آتے ہیں۔ انہیں ملا کر نہیں بلکہ الگ الگ ان کے ناموں سے پڑھا جاتا ہے، جیسے: الٓمٓ = الف لام میم۔ گلابی نشان (مد) پر آواز لمبی کریں۔",
     "Read these letters one by one by their names, e.g. Alif Laam Meem. Stretch the sound where you see the pink madd sign.")


# ===== 4-5. harakat =====
def hrow(marks, l):
    out = []
    for h in marks:
        b = ("إ" if h in (K, KT) else "أ") if l == "ا" else l
        out.append(b + h + ("ا" if h == FT and l not in ("ا", "ء", "ة") else ""))
    return out


n = lesson()
for h, nm_ur, nm_en, col in [(F, "زبر", "Fatha", "سرخ"), (K, "زیر", "Kasra", "نیلی"), (D, "پیش", "Damma", "سبز")]:
    page(n, f"حرکات: {nm_ur}", f"Short Vowels: {nm_en}", grid([(ar(x, 44), NAME[l] + " " + nm_ur) for l in ALL for x in hrow((h,), l)], 6, "words"),
         f"{nm_ur} ({col} علامت) کے ساتھ ہر حرف پڑھیں۔ ہجے کریں: «با {nm_ur}»، پھر آواز نکالیں۔ آواز کو کھینچے بغیر، جھٹکے سے پڑھیں۔",
         f"Read every letter with {nm_en.lower()}. Say the letter name and the vowel, then the sound. Keep it short.", part=f" ({nm_ur})")
drill_pages(n, "حرکات کی مشق: زبر، زیر، پیش", "Short Vowels Together", [x for l in ALL for x in hrow((F, K, D), l)],
            "اب تینوں حرکتیں ایک ساتھ: بَ بِ بُ۔ دائیں سے بائیں ہر سطر روانی سے پڑھیں۔",
            "Now all three together: ba bi bu. Read each row right to left.")
n = lesson()
word_pages(n, "حرکات کی مشق: قرآنی الفاظ", "Practice: Short Vowels (Quran words)", QM.harakat(48),
           "یہ الفاظ قرآن مجید سے لیے گئے ہیں۔ ہر لفظ کے نیچے اس کے ہجے لکھے ہیں: پہلے ہجے کریں، پھر پورا لفظ روانی سے پڑھیں۔",
           "Words from the Quran with their spelling underneath. Spell first, then read the whole word smoothly.")

# ===== 6-7. tanween =====
n = lesson()
drill_pages(n, "تنوین: دو زبر، دو زیر، دو پیش", "Tanween (Double Vowels)", [x for l in ALL for x in hrow((FT, KT, DT), l)],
            "دو زبر، دو زیر اور دو پیش کو تنوین کہتے ہیں۔ تنوین میں آخر میں نون ساکن کی آواز آتی ہے: بَن، بِن، بُن۔ دو زبر کے ساتھ لکھا الف پڑھا نہیں جاتا۔",
            "Tanween adds an 'n' at the end: ban, bin, bun. The alif written after a double fatha is silent.")
n = lesson()
word_pages(n, "تنوین کی مشق: قرآنی الفاظ", "Practice: Tanween (Quran words)", QM.tanween(36),
           "تنوین والے الفاظ کے ہجے کریں، جیسے: الف زبر اَ، حا زبر حَ، دال دو پیش دُن = اَحَدٌ۔ قرآن میں تنوین کبھی ایک کے اوپر ایک اور کبھی آگے پیچھے لکھی جاتی ہے، دونوں کا پڑھنا ایک ہے۔",
           "Spell, then read. In the Quran script tanween is written stacked or staggered; both are read the same.")

# ===== 8. standing vowels =====
n = lesson()
st = []
for l in ["ب", "ت", "ل", "م", "ن", "ه", "ف", "ك", "س", "ذ"]:
    st += [l + KZ, l + KE, l + UP]
page(n, "کھڑا زبر، کھڑی زیر، اُلٹا پیش", "Standing Vowels", grid([(ar(x, 46), "") for x in st], 6, "words"),
     "کھڑا زبر، کھڑی زیر اور اُلٹا پیش کو ایک الف کے برابر (دو حرکت) کھینچ کر پڑھیں: بَا، بِی، بُو۔",
     "Standing fatha, standing kasra and reversed damma are read long, two counts: baa, bee, boo.")
word_pages(n, "کھڑے زبر کی مشق: قرآنی الفاظ", "Practice: Standing Fatha (Quran words)", QM.khari(12),
           "قرآن مجید میں کھڑا زبر بہت آتا ہے، جیسے: ذٰلِکَ، ہٰذَا۔ اسے ایک الف کے برابر کھینچ کر پڑھیں۔",
           "The standing fatha is common in the Quran, as in dhaalika and haadhaa. Read it long, two counts.")

# ===== 9. madd letters =====
n = lesson()
md = []
for l in CONS[:24]:
    md += [l + F + "ا", l + K + "ي", l + D + "و"]
page(n, "حروفِ مدّہ", "Long Vowels (Madd Letters)",
     grid([(ar(x, 36, {1: RED} if x.endswith("ا") else ({1: BLUE} if x.endswith("ي") else {1: GREEN})), "") for x in md[:54]], 6, "tight"),
     "زبر کے بعد الف، زیر کے بعد یا اور پیش کے بعد واؤ حروفِ مدّہ ہیں (رنگین)۔ انہیں ایک الف کے برابر کھینچیں۔ ہجے: با الف زبر بَا، با یا زیر بِی، با واؤ پیش بُو۔",
     "Alif after fatha, ya after kasra and waw after damma (coloured) are long: two counts. Spell: ba alif zabar baa.")
word_pages(n, "حروفِ مدّہ کی مشق: قرآنی الفاظ", "Practice: Madd Letters (Quran words)", QM.madd(48),
           "حروفِ مدّہ والے الفاظ کے ہجے کریں اور مدّہ کو ایک الف کے برابر کھینچیں، جیسے: قاف الف زبر قَا، لام زبر لَ = قَالَ۔",
           "Spell and stretch the madd letter for two counts: qaaf alif zabar qaa, laam zabar la = qaala.")

# ===== 10. leen =====
n = lesson()
ln = []
for l in CONS[:24]:
    ln += [l + F + "يْ", l + F + "وْ"]
page(n, "حروفِ لین", "Soft Letters (Leen)", grid([(ar(x, 36), "") for x in ln[:48]], 6, "tight"),
     "زبر کے بعد واؤ ساکن یا یا ساکن ہو تو یہ حروفِ لین ہیں۔ انہیں نرمی سے پڑھیں، نہ کھینچیں نہ جھٹکا دیں: بَیْ، بَوْ۔",
     "Waw or ya with sukoon after a fatha is soft: read gently, without stretching: bay, baw.")
word_pages(n, "حروفِ لین کی مشق: قرآنی الفاظ", "Practice: Leen (Quran words)", QM.leen(12),
           "قرآن مجید میں جزم کی علامت (ۡ) چھوٹے سر جیسی ہوتی ہے۔ ہجے: یا زبر یَ، واؤ جزم یَوْ، میم زبر مَ = یَوْمَ۔",
           "In the Quran script the sukoon looks like a small head (ۡ). Spell: ya zabar ya, waw jazm yaw, meem zabar ma = yawma.")

# ===== 11. sukoon =====
n = lesson()
sk = []
for l in CONS[:24]:
    sk += ["أَ" + l + SUK, "إِ" + l + SUK, "أُ" + l + SUK]
drill_pages(n, "جزم (سکون)", "Sukoon (Jazm)", sk,
            "جزم (نارنجی) والا حرف اپنی حرکت نہیں رکھتا، اسے پچھلے حرف کے ساتھ ملا کر ٹھہراؤ سے پڑھیں۔ ہجے: الف زبر اَ، با جزم اَبْ۔",
            "A letter with sukoon (orange) has no vowel: join it to the letter before. Spell: alif zabar a, ba jazm ab.")
word_pages(n, "جزم کی مشق: قرآنی الفاظ", "Practice: Sukoon (Quran words)", QM.sukoon(48),
           "ہجے کریں: یا زبر یَ، عین جزم یَعْ، لام زبر لَ، میم پیش مُ = یَعْلَمُ۔ پھر پورا لفظ روانی سے پڑھیں۔",
           "Spell: ya zabar ya, ain jazm ya', laam zabar la, meem pesh mu = ya'lamu.")

# ===== 12. tashdeed =====
n = lesson()
sh = []
for l in CONS[:24]:
    sh += ["أَ" + l + SHAD + F, "أَ" + l + SHAD + K, "أَ" + l + SHAD + D]
drill_pages(n, "تشدید (شد)", "Shaddah (Tashdeed)", sh,
            "تشدید (جامنی) والا حرف دو بار پڑھا جاتا ہے: ایک بار پچھلے حرف کے ساتھ ساکن اور پھر اپنی حرکت کے ساتھ۔ جیسے: اَبَّ = اَبْ بَ۔",
            "A letter with shaddah (purple) is read twice: once with sukoon, then with its vowel: ab-ba.")
word_pages(n, "تشدید کی مشق: قرآنی الفاظ", "Practice: Shaddah (Quran words)", QM.shadda(36),
           "تشدید والے حرف پر زور دے کر پڑھیں۔ ہجے: الف زیر اِ، نون شد زبر نَّ = اِنَّ۔ نون اور میم مشدد میں غنہ کریں۔",
           "Press on the doubled letter. Spell: alif zer i, noon shadd zabar nna = inna. Add ghunnah on a doubled noon or meem.")
word_pages(n, "دو تشدید والے الفاظ", "Practice: Two Shaddahs (Quran words)", QM.shadda(12, True),
           "ان الفاظ میں دو جگہ تشدید ہے۔ ہر تشدید پر ٹھہر کر، صحیح زور کے ساتھ پڑھیں۔",
           "These words have two doubled letters. Press on each one clearly.")

# ===== 13. madd sign =====
n = lesson()
mdd = [l + F + "ا" + MADD + "ءَ" for l in ["ج", "ش", "س", "ب", "ف", "ر", "ل", "م", "ن", "ك", "ه", "ت"]]
mdd += [l + D + "و" + MADD + "ءُ" for l in ["س", "ج", "ب", "ن", "ف", "ل"]]
mdd += [l + K + "ي" + MADD + "ءِ" for l in ["ج", "س", "ب", "ن", "ف", "ل"]]
page(n, "مد", "The Madd Sign", grid([(ar(x, 46), "") for x in mdd], 4, "words"),
     "حرفِ مدّہ پر مد کی علامت (گلابی ~) ہو تو آواز کو ایک الف سے زیادہ، تقریباً چار سے پانچ حرکت تک کھینچیں۔ صحیح مقدار استاد سے سن کر سیکھیں۔",
     "When the pink madd sign is on a long vowel, stretch it longer, about four to five counts. Learn the length from your teacher.")
page(n, "مد کی مشق: قرآنی الفاظ", "Practice: Madd (Quran words)",
     grid([(ar(w, 52), "") for w in QM.madd_sign(12)], 3, "ph"),
     "ان الفاظ میں مد کی علامت ہے۔ مد والی جگہ پر آواز کو چار سے پانچ حرکت تک کھینچیں، جیسے: جَآءَ، شَآءَ۔",
     "These words carry the madd sign. Stretch those vowels four to five counts, as in jaaa'a.", part=" (مشق)")

# ===== 14. ghunnah + qalqalah =====
n = lesson()
page(n, "غنہ: نون مشدد اور میم مشدد", "Ghunnah (Nasal Sound)",
     grid([(ar(w, 52), "") for w in QM.ghunna(12)], 3, "ph"),
     "نون مشدد (نّ) اور میم مشدد (مّ) پر غنہ کریں، یعنی آواز کو ناک میں لے جا کر تقریباً دو حرکت تک روکیں، جیسے: اِنَّ، ثُمَّ۔",
     "On a doubled noon or meem, hold a nasal sound (ghunnah) for about two counts: inna, thumma.")
n = lesson()
page(n, "قلقلہ: ق ط ب ج د", "Qalqalah (Echo Letters)",
     grid([(ar(w, 52, {i: TEAL for i, c in enumerate(w) if c in "قطبجد" and w[i + 1:i + 2] == SUK}), "") for w in QM.qalqala(12)], 3, "ph"),
     "حروفِ قلقلہ پانچ ہیں: ق ط ب ج د (قُطْبُ جَدٍّ)۔ جب یہ ساکن ہوں تو ان کی آواز میں ہلکی سی گونج (جھٹکا) دیں، جیسے: قَدْ، قَبْلُ۔",
     "The five qalqalah letters are ق ط ب ج د. When they have sukoon, give a light bounce to the sound: qad, qabl.")

# ===== 15. noon sakin & tanween =====
n = lesson()
NR = QM.noon_rules(6)
RULES = [("izhar", "اظہار", "Izhar", "حروفِ حلقی (ء ہ ع ح غ خ) سے پہلے نون ساکن یا تنوین کو صاف ظاہر کر کے، بغیر غنہ کے پڑھیں۔"),
         ("idgham", "ادغام", "Idgham", "حروفِ یَرْمَلُوْن (ی ر م ل و ن) سے پہلے نون ساکن یا تنوین اگلے حرف میں مل جاتا ہے: ی ن م و میں غنہ کے ساتھ، ل اور ر میں بغیر غنہ کے۔"),
         ("iqlab", "اقلاب", "Iqlab", "با سے پہلے نون ساکن یا تنوین میم سے بدل جاتا ہے اور غنہ کے ساتھ پڑھا جاتا ہے۔ قرآن میں یہاں چھوٹی میم (ۢ) لکھی ہوتی ہے۔"),
         ("ikhfa", "اخفاء", "Ikhfa", "باقی پندرہ حروف سے پہلے نون ساکن یا تنوین کو چھپا کر، غنہ کے ساتھ پڑھیں۔")]
for grp in (RULES[:2], RULES[2:]):
    body = ""
    for key, ur, en, expl in grp:
        items = [phrase(a, b, s, v, last_base_index(a)) for a, b, s, v, kind in NR[key][:6]]
        body += f'<div class="rule"><h4><b>{ur}</b> <i>{en}</i> {expl}</h4></div>' + grid(items, 3, "ph")
    page(n, "نون ساکن اور تنوین کے قاعدے", "Noon Sakin and Tanween Rules", body,
         "نارنجی حرف نون ساکن یا تنوین والا ہے اور سبز اگلا حرف۔ اگلے حرف کو دیکھ کر قاعدہ پہچانیں اور استاد سے سن کر صحیح ادائیگی سیکھیں۔",
         "Orange marks the noon sakin or tanween letter, green the next letter. Find the rule from the next letter.", legend=False,
         part=" (ا)" if grp[0][0] == "izhar" else " (ب)")

# ===== 16. meem sakin =====
n = lesson()
MR = QM.meem_rules(4)
body = ""
for key, ur, en, expl in [("ikhfa", "اخفائے شفوی", "Ikhfa Shafawi", "میم ساکن کے بعد با ہو تو میم کو غنہ کے ساتھ چھپا کر پڑھیں۔"),
                          ("idgham", "ادغامِ شفوی", "Idgham Shafawi", "میم ساکن کے بعد میم ہو تو دونوں مل کر میم مشدد بن جاتی ہیں، غنہ کے ساتھ۔"),
                          ("izhar", "اظہارِ شفوی", "Izhar Shafawi", "باقی تمام حروف سے پہلے میم ساکن کو صاف ظاہر کریں، خاص طور پر واؤ اور فا سے پہلے۔")]:
    items = [phrase(a, b, s, v, last_base_index(a)) for a, b, s, v in MR[key][:3]]
    body += f'<div class="rule"><h4><b>{ur}</b> <i>{en}</i> {expl}</h4></div>' + grid(items, 3, "ph")
page(n, "میم ساکن کے قاعدے", "Meem Sakin Rules", body,
     "نارنجی حرف میم ساکن ہے اور سبز اگلا حرف۔ با سے پہلے اخفاء، میم سے پہلے ادغام اور باقی حروف سے پہلے اظہار۔",
     "Orange is the meem sakin, green the next letter: before ب hide it, before م merge it, before all others say it clearly.", legend=False)

# ===== 17. Allah + ra =====
n = lesson()
AL = QM.allah(3)
hv, lt = QM.ra(6)
body = (f'<div class="rule"><h4><b>لفظ اللہ</b> پہلے حرف پر زبر یا پیش ہو تو اللہ کا لام پُر (موٹا) پڑھیں، زیر ہو تو باریک۔</h4></div>'
        + grid([phrase(a, b, s, v, None, 2, cb=RED, whole_b=True) for a, b, s, v in AL["heavy"][:3]] + [phrase(a, b, s, v, None, 2, cb=BLUE, whole_b=True) for a, b, s, v in AL["light"][:3]], 3, "ph")
        + f'<div class="rule"><h4><b>حرف را</b> را پر زبر یا پیش ہو تو پُر (موٹا) پڑھیں، زیر ہو تو باریک۔</h4></div>'
        + grid([(ar(w, 46, {i: RED for i, c in enumerate(w) if c == "ر"}), "پُر") for w in hv[:3]]
               + [(ar(w, 46, {i: BLUE for i, c in enumerate(w) if c == "ر"}), "باریک") for w in lt[:3]], 3, "ph"))
page(n, "پُر اور باریک: لفظ اللہ اور را", "Heavy and Light: Allah and Ra", body,
     "سرخ = پُر (موٹی آواز)، نیلا = باریک (پتلی آواز)۔ حروفِ مستعلیہ (خ ص ض غ ط ق ظ) ہمیشہ پُر پڑھے جاتے ہیں۔",
     "Red = heavy (full), blue = light (thin). The letters خ ص ض غ ط ق ظ are always heavy.", legend=False)

# ===== 18. hamzat al-wasl + silent letters =====
n = lesson()
body = (f'<div class="rule"><h4><b>ہمزۃ الوصل (ٱ)</b> ملا کر پڑھتے وقت یہ الف نہیں پڑھا جاتا، پچھلا حرف سیدھا اگلے حرف سے مل جاتا ہے: بِسْمِ اللّٰہ = بِسْمِلّٰہ۔</h4></div>'
        + grid([phrase(a, b, s, v, None, 0, cb=GREY) for a, b, s, v in QM.wasl(6)], 3, "ph")
        + f'<div class="rule"><h4><b>گول نشان (۟)</b> جس حرف پر یہ نشان ہو وہ لکھا تو جاتا ہے مگر پڑھا نہیں جاتا، جیسے: قَالُوا۟ = قَالُوْ۔</h4></div>'
        + grid([(ar(w, 46), "") for w in QM.silent(6)], 3, "ph"))
page(n, "ہمزۃ الوصل اور خاموش حروف", "Joining Alif and Silent Letters", body,
     "سرمئی حروف لکھے ہوئے ہیں مگر ملا کر پڑھنے میں آواز نہیں دیتے۔ استاد سے سن کر ملا کر پڑھنے کی مشق کریں۔",
     "Grey letters are written but not sounded when you read on. Practise joining the words with your teacher.", legend=False)

# ===== 19. waqf signs =====
n = lesson()
WX = QM.waqf_examples()
SIGNS = [("ۘ", "م", "وقفِ لازم: یہاں رکنا ضروری ہے۔"), ("ۗ", "قلى", "رکنا بہتر ہے، ملانا بھی جائز ہے۔"),
         ("ۖ", "صلى", "ملا کر پڑھنا بہتر ہے، رکنا بھی جائز ہے۔"), ("ۚ", "ج", "رکنا اور ملانا دونوں برابر جائز ہیں۔"),
         ("ۙ", "لا", "یہاں نہ رکیں، ملا کر پڑھیں۔"), ("ۛ", "∴", "تین نقطے دو جگہ ہوں تو ان میں سے کسی ایک پر رکیں، دونوں پر نہیں۔")]
rows = []
for sign, nm, expl in SIGNS:
    ex = WX.get(sign)
    rows.append((ar("\u0640\u0640" + sign + "\u0640\u0640", 34, {0: "#cccccc", 1: "#cccccc", 3: "#cccccc", 4: "#cccccc"}), f'<b>{nm}</b> {expl}'))
    rows.append((ar(ex[0], 30) if ex else "", ""))
rows += [(ar("\u06dd", 34), '<b>آیت</b> گول دائرہ آیت کا اختتام ہے۔ یہاں رکنا سنت ہے، سانس لے کر اگلی آیت شروع کریں۔'), ("", "")]
page(n, "وقف کی علامات", "Stopping Signs (Madinah Mushaf)", grid(rows, 2, "waqf"),
     "تلاوت میں سانس صرف وقف کی جگہ پر لیں۔ اوپر کی علامات مصحفِ مدینہ کی ہیں، ہر علامت کے ساتھ قرآن سے ایک مثال دی گئی ہے۔",
     "Breathe only where stopping is allowed. These are the signs of the Madinah Mushaf, each with an example from the Quran.", legend=False)

# ===== 20. makharij =====
n = lesson()
MKH = [("جوف (منہ اور حلق کا خالی حصہ)", "اوي", "حروفِ مدّہ: آواز منہ کی خالی جگہ سے نکلتی ہے۔"),
       ("حلق", "ءهعحغخ", "حلق کے نیچے، درمیان اور اوپر کے حصے سے۔"),
       ("زبان", "قكجشيضلنرطدتظذثصسز", "زبان کے مختلف حصے تالو اور دانتوں سے لگ کر یہ اٹھارہ حروف ادا کرتے ہیں۔"),
       ("ہونٹ", "فبمو", "فا نچلے ہونٹ اور اوپر کے دانتوں سے، با میم واؤ دونوں ہونٹوں سے۔"),
       ("خیشوم (ناک)", "نم", "غنہ کی آواز ناک سے نکلتی ہے: نون اور میم کا غنہ۔")]
items = []
for place, letters, expl in MKH:
    items.append(("", f'<b class="mk">{place}</b>'))
    items.append(('<span class="row-ar">' + '<span class="sp"></span>'.join(ar(l, 36, {0: ALT[k % 4]}) for k, l in enumerate(letters)) + '</span>', f'<span class="mx">{expl}</span>'))
page(n, "مخارج: حروف کہاں سے نکلتے ہیں", "Makharij: Where the Letters Come From", grid(items, 2, "mkh"),
     "ہر حرف کا اپنا مخرج (نکلنے کی جگہ) ہے۔ حرف کو ساکن کر کے اس سے پہلے ہمزہ زبر لگائیں (اَبْ، اَتْ) تو اس کا مخرج آسانی سے محسوس ہوتا ہے۔",
     "Every letter has its own exit point. Say it with sukoon after a hamza (ab, at) to feel where it comes from.", legend=False)


# ===== 21. Quran practice =====
def surah(n_, size):
    vs = Q[n_ - 1]["verses"]
    body = "".join(f'{v["text"]} <span class="an">({str(v["id"]).translate(AD)})</span> ' for v in vs)
    bism = "" if n_ in (1, 9) else '<p class="bism" lang="ar">بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ</p>'
    return (f'<div class="surah"><h3>سورۃ {Q[n_ - 1]["name"]} <small>Surah {Q[n_ - 1]["transliteration"]}</small></h3>'
            f'{bism}<p class="ayat" lang="ar" dir="rtl" style="font-size:{size}px">{body}</p></div>')


n = lesson()
page(n, "قرآنی مشق: سورۃ الفاتحہ", "Quran Practice: Al-Fatiha", surah(1, 44),
     "اب قرآن مجید کی پہلی سورت پڑھیں۔ آہستہ، ٹھہر ٹھہر کر اور صحیح مخارج کے ساتھ۔ (رسم الخط: مصحفِ مدینہ)",
     "Now read the opening surah of the Quran, slowly and carefully. (Madinah Mushaf script.)", legend=False)
for i, grp in enumerate([(103, 104), (105, 106, 107), (108, 109, 110), (111, 112), (113, 114)]):
    page(n, "قرآنی مشق: آخری سورتیں", "Quran Practice: The Last Surahs", "".join(surah(x, 28 if len(grp) == 2 else 26) for x in grp),
         "یہ سورتیں نماز میں کثرت سے پڑھی جاتی ہیں۔ استاد کے ساتھ پڑھ کر روزانہ دہرائیں اور یاد کریں۔",
         "These surahs are read often in salah. Read them with your teacher and revise them every day.", legend=False,
         part=f" ({str(i + 1).translate(UD)})")
# ---------------- css + document ----------------
def ff(fam, path, w):
    return f"@font-face{{font-family:'{fam}';src:url('file://{path}') format('woff2');font-weight:{w}}}"


fonts = "".join([
    ff("Amiri", f"{FONTS}/fontsource-amiri-5.3.0/files/amiri-arabic-400-normal.woff2", 400),
    ff("Amiri", f"{FONTS}/fontsource-amiri-5.3.0/files/amiri-arabic-700-normal.woff2", 700),
    ff("Nastaliq", f"{FONTS}/fontsource-noto-nastaliq-urdu/files/noto-nastaliq-urdu-arabic-400-normal.woff2", 400),
    ff("Nastaliq", f"{FONTS}/fontsource-noto-nastaliq-urdu/files/noto-nastaliq-urdu-arabic-700-normal.woff2", 700),
    ff("Manrope", f"{FONTS}/fontsource-manrope-5.3.0/files/manrope-latin-500-normal.woff2", 500),
    ff("Manrope", f"{FONTS}/fontsource-manrope-5.3.0/files/manrope-latin-800-normal.woff2", 800),
    ff("Fraunces", f"{FONTS}/fontsource-fraunces-5.3.0/files/fraunces-latin-600-normal.woff2", 600),
])
G1, G2, GOLD = "#0b5d3f", "#e9f6ef", "#c99a2e"
CSS = fonts + f"""
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Manrope,sans-serif;color:#111;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;padding:8mm;page-break-after:always;background:#fff;overflow:hidden}}
.frame{{height:100%;border:2.5px solid {G1};border-radius:10px;padding:0 7mm 4mm;display:flex;flex-direction:column;position:relative;
 background:linear-gradient(#fff,#fff) padding-box}}
.frame::before{{content:"";position:absolute;inset:3px;border:1px solid {GOLD};border-radius:8px;pointer-events:none}}
header{{margin:0 -7mm 3mm;background:{G1};color:#fff;border-radius:7px 7px 0 0;padding:2mm 7mm 2.5mm;text-align:center;position:relative}}
header::after{{content:"";position:absolute;left:0;right:0;bottom:-3px;height:3px;background:{GOLD}}}
.hd-row{{display:flex;justify-content:space-between;align-items:center;direction:rtl;font-family:Nastaliq,serif;font-size:12px;line-height:2.1}}
.sabaq{{background:{GOLD};color:#1a1200;padding:0 14px;border-radius:99px;font-weight:700}}
.pno,.bk{{color:#cfe9dc}}
h2{{font-family:Nastaliq,serif;font-weight:700;font-size:26px;line-height:2.35;margin:-3mm 0 0;color:#fff;direction:rtl}}
.en{{display:block;font-size:9.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#f3d98a;margin-top:0;position:relative;z-index:2}}
.legend{{display:flex;justify-content:center;gap:7px;direction:rtl;margin:0 0 2.5mm;flex-wrap:wrap}}
.legend span{{font-family:Nastaliq,serif;font-size:11.5px;line-height:1.9;color:var(--c);border:1.2px solid var(--c);border-radius:99px;padding:0 9px;display:flex;align-items:center;gap:5px;background:#fff}}
.legend i{{width:8px;height:8px;border-radius:50%;background:var(--c);display:inline-block}}
.body{{flex:1;display:flex;flex-direction:column;min-height:0}}
.grid{{display:grid;grid-auto-rows:1fr;min-height:0;direction:rtl;border:2px solid {G1};border-radius:8px;overflow:hidden;background:{G1};gap:1.5px}}
.cell{{background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:0;padding:1mm 1mm;gap:1mm}}
.cell:nth-child(even){{background:#fbfaf3}}
.grid.tight .cell:nth-child(6n+1),.grid.tight .cell:nth-child(6n+2),.grid.tight .cell:nth-child(6n+3){{background:{G2}}}
.grid.tight .cell:nth-child(6n+4),.grid.tight .cell:nth-child(6n+5),.grid.tight .cell:nth-child(6n+6){{background:#fffdf3}}
svg.a{{display:block;overflow:visible}}
.nm{{font-family:Nastaliq,serif;font-size:13px;line-height:1.9;direction:rtl;text-align:center;color:#333}}
.nm small{{display:block;font-size:10px;color:#777;line-height:1.7}}
.big .nm{{font-size:15px}}
.fx{{display:flex;align-items:center;gap:3px;direction:ltr;opacity:.95}}.plus{{font-weight:800;color:#666;font-size:14px}}
.hj .cell{{justify-content:space-between;padding:1.5mm 2mm 1mm}}
.hj .nm{{font-size:12.5px;line-height:2.15;color:#222}}
.sy{{font-family:Amiri,serif;font-size:17px;font-weight:700}}
.gap{{height:3mm;flex:none}}
.note{{margin-top:3mm;border:1.5px solid {GOLD};border-radius:8px;padding:1.2mm 4mm 1.5mm;background:#fff8e1}}
.ur-note{{font-family:Nastaliq,serif;font-size:12.5px;line-height:2.15;margin:0;text-align:right;direction:rtl;color:#1d1d1d}}.ur-note b{{color:{RED}}}
.en-note{{font-size:9.5px;margin:0;color:#5a5140}}
footer{{display:flex;justify-content:space-between;font-size:8.5px;color:#7b8a80;margin-top:1.8mm;letter-spacing:.05em}}
.surah{{border:2px solid {G1};border-radius:8px;padding:2mm 6mm 3mm;margin-bottom:3mm;background:#fffdf6}}
.surah h3{{margin:0;text-align:center;font-family:Nastaliq,serif;font-size:16px;line-height:2;color:{G1};direction:rtl}}
.surah h3 small{{display:block;font-family:Manrope,sans-serif;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:{GOLD};line-height:1.2}}
.bism{{font-family:Amiri,serif;font-size:24px;text-align:center;margin:0;color:{G1}}}
.ayat{{font-family:Amiri,serif;line-height:2.2;margin:0;text-align:justify;text-align-last:center}}
.an{{color:{GOLD};font-size:.7em}}
.cover .frame{{background:{G1};color:#fff;align-items:center;justify-content:center;text-align:center;gap:4mm;padding:10mm}}
.cover .ar-big{{font-family:Amiri,serif;font-size:58px;line-height:1.5;color:#fff}}
.cover h1{{font-family:Nastaliq,serif;font-size:46px;line-height:2.2;margin:0;color:#f3d98a}}
.cover .en-t{{font-family:Fraunces,serif;font-size:30px;color:#f3d98a;margin:0}}
.cover p{{margin:0;font-size:12.5px;line-height:1.7;max-width:135mm;color:#e3f1ea}}
.cover .orn{{width:70mm;height:2px;background:linear-gradient(90deg,transparent,{GOLD},transparent)}}
.cover .site{{font-weight:800;letter-spacing:.16em;font-size:11px;color:#f3d98a}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;direction:rtl}}
.chips span{{font-family:Nastaliq,serif;font-size:13px;line-height:2;padding:0 10px;border-radius:99px;background:#fff;color:var(--c);border:1.5px solid var(--c)}}
.toc{{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm;direction:rtl;margin-top:1mm}}
.toc div{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px dotted #9bb;font-family:Nastaliq,serif;font-size:14px;line-height:2.25}}
.toc .n{{font-family:Manrope;font-size:10.5px;color:{G1};font-weight:800;direction:ltr}}
.howto{{font-family:Nastaliq,serif;font-size:13.5px;line-height:2.2;direction:rtl;text-align:right;margin:3mm 0 0;padding-right:6mm}}
.keybox{{margin-top:3mm;border:2px solid {G1};border-radius:8px;padding:2mm 4mm;direction:rtl}}
.keybox h4{{font-family:Nastaliq,serif;margin:0;font-size:15px;line-height:2;color:{G1}}}
.keyrow{{display:grid;grid-template-columns:repeat(6,1fr);gap:2mm;text-align:center}}
.keyrow div{{border-radius:6px;background:#f7f7f2;padding:1mm 0}}
.keyrow b{{display:block;font-family:Nastaliq,serif;font-size:12px;line-height:2;font-weight:400}}
.row-ar{{display:flex;align-items:center;justify-content:center;gap:0;direction:rtl;flex-wrap:wrap}}.sp{{display:inline-block;width:5mm}}
.nm small{{display:block;font-size:9.5px;color:#7a7a7a;line-height:1.6}}
.hj .nm small{{font-size:9px;margin-top:-1mm}}
.forms .cell{{padding:0}}.forms .cell:nth-child(-n+5){{background:{G1}!important}}.forms .cell:nth-child(-n+5) .nm{{color:#fff;font-size:13px}}
.fname{{color:{G1};font-weight:700;font-size:14px}}.dash{{color:#bbb;font-size:20px}}
.rule{{margin:1.5mm 0 1.5mm}}.rule h4{{margin:0;font-family:Nastaliq,serif;font-weight:400;font-size:12.5px;line-height:2.1;direction:rtl;text-align:right;color:#222;background:#eef7f2;border-right:4px solid {G1};padding:0 3mm;border-radius:4px}}
.rule h4 b{{color:{G1};font-size:15px;margin-left:2mm}}.rule h4 i{{font-family:Manrope,sans-serif;font-style:normal;font-size:9px;color:{GOLD};letter-spacing:.08em;margin-left:2mm}}
.ph .cell{{padding:1mm 1mm}}
.waqf{{grid-template-columns:42% 58%!important}}.waqf .cell:nth-child(odd){{background:#fff8e1;flex-direction:row;justify-content:flex-start;gap:2mm;padding:0 3mm}}.waqf .cell:nth-child(odd) svg{{flex:none}}.waqf .nm{{font-size:12px;line-height:2;text-align:right;padding:0 1mm}}.waqf .cell:nth-child(even) .nm{{text-align:center}}.waqf .nm b{{color:{RED};font-size:15px;margin-left:2mm}}
.sign{{display:inline-block;min-width:16mm;text-align:center}}
.mkh{{grid-template-columns:28% 72%!important}}.mkh .cell:nth-child(odd){{background:#eef7f2}}.mk{{font-size:15px;color:{G1};font-weight:700}}.mx{{font-size:11.5px;color:#444}}
"""

cover = ('<section class="pg cover"><div class="frame">' + ar("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", 54).replace('fill="#111111"', 'fill="#ffffff"') +
         '<div class="orn"></div><h1>نورانی قاعدہ</h1><p class="en-t">Noorani Qaida</p>'
         '<div class="chips">' + "".join(f'<span style="--c:{c}">{t}</span>' for t, c in [("زبر", RED), ("زیر", BLUE), ("پیش", GREEN), ("جزم", ORANGE), ("شد", PURPLE), ("مد", PINK)]) + '</div>'
         f'<p>{len(LESSONS)} lessons and {len(PAGES) + 3} pages: colour-coded harakat, spelling (hijje) under every practice word, real Quran words with references, tajweed rules and Urdu instructions on every page.</p>'
         '<div class="orn"></div><p class="site">QURAN ONLINE TARTEEL · quranonlinetarteel.net</p></div></section>')
key = ('<div class="keybox"><h4>رنگوں کی پہچان</h4><div class="keyrow">' + "".join(
    f'<div>{ar(x, 34)}<b style="color:{c}">{t}</b></div>' for x, t, c in
    [("بَ", "زبر", RED), ("بِ", "زیر", BLUE), ("بُ", "پیش", GREEN), ("أَبْ", "جزم", ORANGE), ("أَبَّ", "شد", PURPLE), ("بَآ", "مد", PINK)]) + '</div></div>')
toc = ('<section class="pg"><div class="frame"><header><div class="hd-row"><span class="pno">صفحہ ۲</span><span class="sabaq">فہرست</span><span class="bk">نورانی قاعدہ</span></div>'
       '<h2>اسباق کی فہرست</h2><span class="en">Contents · Colour key · How to use</span></header>'
       '<div class="toc">' + "".join(f'<div><span>سبق {str(n_).translate(UD)}: {t}</span><span class="n">p. {p}</span></div>' for n_, t, p in LESSONS) + '</div>' + key +
       '<ol class="howto"><li>روزانہ تھوڑا پڑھیں: دس سے پندرہ منٹ روزانہ، ہفتے میں ایک لمبے سبق سے بہتر ہیں۔</li>'
       '<li>دائیں سے بائیں پڑھیں اور ہر خانے پر انگلی رکھیں۔ رنگ دیکھ کر حرکت پہچانیں۔</li>'
       '<li>پہلے صحیح آواز اور مخرج، رفتار بعد میں خود آ جائے گی۔ کوئی سبق نہ چھوڑیں۔</li>'
       '<li>استاد کے ساتھ پڑھیں۔ کتاب آپ کی آواز نہیں سن سکتی، استاد چھوٹی غلطیاں بروقت درست کرتا ہے۔</li>'
       '<li>ہر سبق سے پہلے دعا کریں: رَبِّ زِدْنِيْ عِلْمًا، «اے میرے رب! میرے علم میں اضافہ فرما» (طٰہٰ ۱۱۴)۔</li></ol>'
       '<footer><span>quranonlinetarteel.net</span><span>Page 2</span></footer></div></section>')
end = ('<section class="pg cover"><div class="frame">' + ar("مَا شَاءَ اللَّهُ", 60).replace('fill="#111111"', 'fill="#ffffff"') +
       '<div class="orn"></div><h1>مبارک ہو!</h1><p class="en-t">Well done!</p>'
       '<p>You have finished the Noorani Qaida. The next step is reading the Quran itself with Tajweed, page by page.</p>'
       '<p>Learn with a female teacher, live and one to one: <b style="color:#f3d98a">quranonlinetarteel.net</b> · 2 free classes</p>'
       '<div class="orn"></div><p class="site">QURAN ONLINE TARTEEL</p></div></section>')
doc = (f'<!doctype html><html lang="ur"><head><meta charset="utf-8"><title>Noorani Qaida (Colour) - Quran Online Tarteel</title><style>{CSS}</style></head>'
       f'<body>{cover}{toc}{"".join(PAGES)}{end}</body></html>')
open(OUT_HTML, "w").write(doc)
os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{OUT_HTML}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);
const ov=await p.evaluate(()=>{{const pgs=[...document.querySelectorAll('.pg')];return [...document.querySelectorAll('.cell,.note,.body,.surah')].filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>pgs.indexOf(e.closest('.pg'))+1)}});
console.log('OVERFLOW pages', JSON.stringify([...new Set(ov)]));
await p.pdf({{path:'{OUT_PDF}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print("PDF:", OUT_PDF, os.path.getsize(OUT_PDF) // 1024, "KB,", len(PAGES) + 3, "pages,", len(LESSONS), "lessons")
