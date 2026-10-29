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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = sys.argv[1] if len(sys.argv) > 1 else "."
Q = json.load(open(os.path.join(ROOT, "data", "quran-uthmani.json")))
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
ASC, DESC = 1200, -700   # tight box for drill text (font units)
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
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
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
    w = max(x, 1)
    hpx = size * (ASC - DESC) / UPEM
    wpx = size * w / UPEM
    t = f'<title>{H.escape(title or text)}</title>'
    return (f'<svg class="a" role="img" aria-label="{H.escape(title or text)}" width="{wpx:.1f}" height="{hpx:.1f}" viewBox="0 {-ASC} {w} {ASC - DESC}">{t}'
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


# ---------------- page builders ----------------
PAGES = []


def page(lesson, ur_title, en_title, body, ur_note, en_note, legend=True, part=""):
    n = len(PAGES) + 3   # cover = 1, contents = 2
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
    wgt = n * (1.8 if "hj" in cls else 1)
    return (f'<div class="grid {cls}" style="grid-template-columns:repeat({cols},1fr);flex:{wgt}">' + "".join(
        f'<div class="cell">{a}' + (f'<span class="nm">{b}</span>' if b else "") + "</div>" for a, b in items) + "</div>")


def chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


# 1. single letters
page(1, "حروفِ مفردات", "Single Letters",
     grid([(ar(l, 64), f'<span style="color:{ALT[i % 3]}">{nm}</span>') for i, (l, nm) in enumerate(LETTERS)], 5, "big"),
     "ہر حرف کو اس کے نام سے صاف اور درست مخرج کے ساتھ پڑھیں۔ دائیں سے بائیں پڑھیں اور ہر خانے پر انگلی رکھیں۔ پہلے استاد سے سنیں، پھر خود دہرائیں۔",
     "Read each letter by its name, right to left, pointing to every box. Listen to your teacher first, then repeat.", legend=False)

# 2. joined letters: formula cards (two letters → joined, each letter its own colour)
def formula(a, b):
    joined = a + b
    top = f'{ar(b, 24, {0: BLUE})}<span class="plus">+</span>{ar(a, 24, {0: RED})}'
    return f'<span class="fx">{top}</span>{ar(joined, 44, {0: RED, 1: BLUE})}'


seq = [l for l in ALL if l != "ء"]
f_items = [(formula(l, "ا"), "") for l in seq if l not in NONJOIN]
page(2, "حروفِ مرکبات", "Joined Letters (with Alif)", grid(f_items, 6, "fx-grid"),
     "جب حرف دوسرے حرف سے ملتا ہے تو اس کی شکل ٹوٹ جاتی ہے۔ سرخ حصہ پہلا حرف ہے اور نیلا حصہ دوسرا۔ ہر جوڑ کو یوں پڑھیں: «با: بے الف»۔",
     "Letters change shape when they join. The red part is the first letter, the blue part the second.", legend=False, part=" (الف)")
pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1) if seq[i] not in NONJOIN]
pairs += [(a, b) for a, b in [("ل", "ا"), ("ب", "ي"), ("ن", "ي"), ("ت", "ي"), ("ف", "ي"), ("ك", "م"), ("ل", "م"), ("س", "ل")]]
page(2, "حروفِ مرکبات", "Joined Letters (pairs)", grid([(formula(a, b), "") for a, b in pairs[:30]], 6, "fx-grid"),
     "ہر خانے میں اوپر دو الگ حروف ہیں اور نیچے وہی حروف ملے ہوئے۔ ٹوٹی ہوئی شکل کو پہچانیں اور حروف کے نام لے کر پڑھیں۔",
     "Each box shows two separate letters and, below, the same letters joined. Spot the broken shape and name the letters.", legend=False, part=" (جوڑ)")
trip = []
for i in range(0, len(seq) - 2):
    a, b, c = seq[i], seq[i + 1], seq[i + 2]
    if a not in NONJOIN and b not in NONJOIN:
        trip.append(a + b + c)
trip += ["بسم", "قلم", "علم", "نعم", "لكم", "منه", "فيه", "حمد", "سجد", "غفر", "شكر", "صبر"]
page(2, "حروفِ مرکبات", "Joined Letters (three letters)",
     grid([(ar(t, 46, {0: RED, 1: BLUE, 2: GREEN}), " ".join(f'<span style="color:{c}">{NAME[x]}</span>' for x, c in zip(t, (RED, BLUE, GREEN)))) for t in trip[:28]], 4, "words"),
     "تین حروف ملے ہوئے ہیں: سرخ پہلا، نیلا دوسرا اور سبز تیسرا حرف۔ نیچے لکھے ناموں کو دیکھ کر ہر حرف کو الگ پہچانیں۔",
     "Three joined letters: red is the first, blue the second, green the third. Name each one.", legend=False, part=" (تین حروف)")

# 3. muqattaat
muq = [(2, 1), (7, 1), (10, 1), (13, 1), (19, 1), (20, 1), (26, 1), (27, 1), (36, 1), (38, 1), (40, 1), (42, 2), (50, 1), (68, 1)]
MUQ_UR = {2: "الف لام میم", 7: "الف لام میم صاد", 10: "الف لام را", 13: "الف لام میم را", 19: "کاف ہا یا عین صاد", 20: "طا ہا",
          26: "طا سین میم", 27: "طا سین", 36: "یا سین", 38: "صاد", 40: "حا میم", 42: "عین سین قاف", 50: "قاف", 68: "نون"}
first = lambda s, a: Q[s - 1]["verses"][a - 1]["text"].split(" ")[0].rstrip("ۚۖۗۛ")
page(3, "حروفِ مقطعات", "Disjoined Letters",
     grid([(ar(first(s, a), 50), f'{MUQ_UR[s]}<small>سورۃ {Q[s - 1]["name"]}</small>') for s, a in muq], 4, "words"),
     "یہ حروف قرآن مجید کی بعض سورتوں کے شروع میں آتے ہیں۔ انہیں ملا کر نہیں بلکہ الگ الگ ان کے ناموں سے پڑھا جاتا ہے، جیسے: الٓمٓ = الف لام میم۔ گلابی نشان (مد) پر آواز لمبی کریں۔",
     "Read these letters one by one by their names, e.g. Alif Laam Meem. Stretch the sound where you see the pink madd sign.")


# 4. harakat
def hrow(marks, l):
    out = []
    for h in marks:
        b = ("إ" if h in (K, KT) else "أ") if l == "ا" else l
        out.append(b + h + ("ا" if h == FT and l not in ("ا", "ء", "ة") else ""))
    return out


drill = [x for l in ALL for x in hrow((F, K, D), l)]
for i, ch in enumerate(chunks(drill, 48)):
    page(4, "حرکات: زبر، زیر، پیش", "Short Vowels", grid([(ar(x, 36), "") for x in ch], 6, "tight"),
         "زبر (سرخ) سے «اَ»، زیر (نیلا) سے «اِ» اور پیش (سبز) سے «اُ» کی آواز نکلتی ہے۔ ہجے کریں: با زبر بَ، با زیر بِ، با پیش بُ۔ آواز کو کھینچے بغیر پڑھیں۔",
         "Fatha (red) = a, kasra (blue) = i, damma (green) = u. Spell: ba zabar ba, ba zer bi, ba pesh bu. Keep the sounds short.",
         part=f" ({'ا' if i == 0 else 'ب'})")

# 5. harakat words with hijje
w5 = ["كَتَبَ", "ذَهَبَ", "جَلَسَ", "خَلَقَ", "فَتَحَ", "نَصَرَ", "رَزَقَ", "سَمِعَ", "عَلِمَ", "شَرِبَ", "حَسُنَ", "كَرُمَ",
      "صَبَرَ", "شَكَرَ", "دَخَلَ", "خَرَجَ", "رَجَعَ", "زَرَعَ", "أَخَذَ", "أَكَلَ", "سَأَلَ", "قَرَأَ", "حَمِدَ", "غَفَرَ"]
for i, ch in enumerate(chunks(w5, 12)):
    page(5, "حرکات کی مشق", "Practice: Short Vowels (with spelling)", grid([(ar(w, 56), hijje(w)) for w in ch], 3, "hj"),
         "ہر لفظ کے نیچے اس کے ہجے لکھے ہیں۔ پہلے ہجے کریں، پھر پورا لفظ روانی سے پڑھیں۔ رنگ دیکھ کر حرکت پہچانیں۔",
         "The spelling is under every word. Spell first, then read the whole word smoothly.", part=f" ({str(i + 1).translate(UD)})")

# 6. tanween
drill = [x for l in ALL for x in hrow((FT, KT, DT), l)]
for i, ch in enumerate(chunks(drill, 48)):
    page(6, "تنوین: دو زبر، دو زیر، دو پیش", "Tanween (Double Vowels)", grid([(ar(x, 36), "") for x in ch], 6, "tight"),
         "دو زبر، دو زیر اور دو پیش کو تنوین کہتے ہیں۔ تنوین میں آخر میں نون ساکن کی آواز آتی ہے: بَن، بِن، بُن۔ دو زبر کے ساتھ لکھا الف پڑھا نہیں جاتا۔",
         "Tanween adds an 'n' at the end: ban, bin, bun. The alif written after a double fatha is silent.", part=f" ({'ا' if i == 0 else 'ب'})")

# 7. tanween words
w7 = ["أَحَدٌ", "وَلَدٌ", "قَمَرٌ", "جَبَلٌ", "شَجَرٌ", "حَسَنٌ", "مَلِكٌ", "ثَمَرٌ", "عَمَلٌ", "خَبَرٌ", "رَجُلٌ", "بَشَرٌ",
      "وَلَدًا", "عَمَلًا", "سَبَبًا", "بَشَرًا", "حَسَنًا", "سَفَرًا", "حَسَنٍ", "عَمَلٍ", "جَبَلٍ", "شَجَرٍ", "قَمَرٍ", "فَرَسٍ"]
for i, ch in enumerate(chunks(w7, 12)):
    page(7, "تنوین کی مشق", "Practice: Tanween (with spelling)", grid([(ar(w, 56), hijje(w)) for w in ch], 3, "hj"),
         "تنوین والے الفاظ کے ہجے کریں، جیسے: الف زبر اَ، حا زبر حَ، دال دو پیش دٌ = اَحَدٌ۔ پھر روانی سے پڑھیں۔",
         "Spell, then read: alif zabar a, ha zabar ha, dal do pesh dun = ahadun.", part=f" ({str(i + 1).translate(UD)})")

# 8. standing vowels
st = []
for l in ["ب", "ت", "ل", "م", "ن", "ه", "ف", "ك", "س"]:
    st += [l + KZ, l + KE, l + UP]
sw = ["ذٰلِكَ", "لَهٗ", "بِهٖ"]
page(8, "کھڑا زبر، کھڑی زیر، اُلٹا پیش", "Standing Vowels",
     grid([(ar(x, 44), "") for x in st], 6, "words") + '<div class="gap"></div>' + grid([(ar(w, 50), hijje(w)) for w in sw], 3, "hj"),
     "کھڑا زبر، کھڑی زیر اور اُلٹا پیش کو ایک الف کے برابر (دو حرکت) کھینچ کر پڑھیں: بَا، بِی، بُو۔",
     "Standing fatha, standing kasra and reversed damma are read long, two counts: baa, bee, boo.")

# 9. madd letters
md = []
for l in CONS[:24]:
    md += [l + F + "ا", l + K + "ي", l + D + "و"]
page(9, "حروفِ مدّہ", "Long Vowels (Madd Letters)", grid([(ar(x, 36, {1: RED} if x.endswith("ا") else ({1: BLUE} if x.endswith("ي") else {1: GREEN})), "") for x in md[:54]], 6, "tight"),
     "زبر کے بعد الف، زیر کے بعد یا اور پیش کے بعد واؤ حروفِ مدّہ ہیں (رنگین)۔ انہیں ایک الف کے برابر کھینچیں۔ ہجے: با الف زبر بَا، با یا زیر بِی، با واؤ پیش بُو۔",
     "Alif after fatha, ya after kasra and waw after damma (coloured) are long: two counts. Spell: ba alif zabar baa.")
w10 = ["قَالَ", "كَانَ", "بَابٌ", "نَارٌ", "قِيلَ", "دِينٌ", "يَقُولُ", "نُورٌ", "كِتَابٌ", "رَسُولٌ", "عَظِيمٌ", "كَرِيمٌ"]
page(9, "حروفِ مدّہ کی مشق", "Practice: Madd (with spelling)", grid([(ar(w, 56), hijje(w)) for w in w10], 3, "hj"),
     "حروفِ مدّہ والے الفاظ کے ہجے کریں اور مدّہ کو ایک الف کے برابر کھینچیں، جیسے: قاف الف زبر قَا، لام زبر لَ = قَالَ۔",
     "Spell and stretch the madd letter for two counts: qaaf alif zabar qaa, laam zabar la = qaala.", part=" (مشق)")

# 10. leen
ln = []
for l in CONS[:24]:
    ln += [l + F + "يْ", l + F + "وْ"]
wl = ["خَوْفٌ", "بَيْتٌ", "يَوْمٌ", "قَوْمٌ", "عَيْنٌ", "لَيْلٌ"]
page(10, "حروفِ لین", "Soft Letters (Leen)",
     grid([(ar(x, 36), "") for x in ln[:30]], 6, "tight") + '<div class="gap"></div>' + grid([(ar(w, 46), hijje(w)) for w in wl], 3, "hj"),
     "زبر کے بعد واؤ ساکن یا یا ساکن ہو تو یہ حروفِ لین ہیں۔ انہیں نرمی سے پڑھیں، نہ کھینچیں نہ جھٹکا دیں: بَیْ، بَوْ۔",
     "Waw or ya with sukoon after a fatha is soft: read gently, without stretching: bay, baw.")

# 11. sukoon
sk = []
for l in CONS[:24]:
    sk += ["أَ" + l + SUK, "إِ" + l + SUK, "أُ" + l + SUK]
for i, ch in enumerate(chunks(sk, 48)):
    page(11, "جزم (سکون)", "Sukoon (Jazm)", grid([(ar(x, 36), "") for x in ch], 6, "tight"),
         "جزم (نارنجی) والا حرف اپنی حرکت نہیں رکھتا، اسے پچھلے حرف کے ساتھ ملا کر ٹھہراؤ سے پڑھیں۔ ہجے: الف زبر اَ، با جزم اَبْ۔",
         "A letter with sukoon (orange) has no vowel: join it to the letter before. Spell: alif zabar a, ba jazm ab.", part=f" ({'ا' if i == 0 else 'ب'})")
w12 = ["مِنْ", "عَنْ", "لَمْ", "قُلْ", "هَلْ", "قَدْ", "يَعْلَمُ", "يَشْرَبُ", "يَسْمَعُ", "يَفْتَحُ", "يَذْهَبُ", "قَلْبٌ",
       "مَسْجِدٌ", "مَغْرِبٌ", "مَشْرِقٌ", "أَكْبَرُ", "أَنْعَمْتَ", "يَخْلُقُ"]
for i, ch in enumerate(chunks(w12, 12)):
    page(12, "جزم کی مشق", "Practice: Sukoon (with spelling)", grid([(ar(w, 56), hijje(w)) for w in ch], 3, "hj"),
         "ہجے کریں: یا زبر یَ، عین جزم یَعْ، لام زبر لَ، میم پیش مُ = یَعْلَمُ۔ پھر پورا لفظ روانی سے پڑھیں۔",
         "Spell: ya zabar ya, ain jazm ya', laam zabar la, meem pesh mu = ya'lamu.", part=f" ({str(i + 1).translate(UD)})")

# 13. tashdeed
sh = []
for l in CONS[:24]:
    sh += ["أَ" + l + SHAD + F, "أَ" + l + SHAD + K, "أَ" + l + SHAD + D]
for i, ch in enumerate(chunks(sh, 48)):
    page(13, "تشدید (شد)", "Shaddah (Tashdeed)", grid([(ar(x, 36), "") for x in ch], 6, "tight"),
         "تشدید (جامنی) والا حرف دو بار پڑھا جاتا ہے: ایک بار پچھلے حرف کے ساتھ ساکن اور پھر اپنی حرکت کے ساتھ۔ جیسے: اَبَّ = اَبْ بَ۔",
         "A letter with shaddah (purple) is read twice: once with sukoon, then with its vowel: ab-ba.", part=f" ({'ا' if i == 0 else 'ب'})")
w14 = ["رَبِّ", "إِنَّ", "ثُمَّ", "كُلٌّ", "حَقٌّ", "رَبُّكَ", "مُحَمَّدٌ", "عَلَّمَ", "قَدَّرَ", "كَذَّبَ", "صَدَّقَ", "جَنَّةٌ"]
page(14, "تشدید کی مشق", "Practice: Shaddah (with spelling)", grid([(ar(w, 56), hijje(w)) for w in w14], 3, "hj"),
     "تشدید والے حرف پر زور دے کر پڑھیں۔ نون مشدد اور میم مشدد میں غنہ کریں (آواز ناک میں لے جائیں)، جیسے: اِنَّ، ثُمَّ۔",
     "Press on the doubled letter. With a doubled noon or meem add ghunnah (a nasal sound): inna, thumma.")

# 15. madd sign
mdd = [l + F + "ا" + MADD + "ءَ" for l in ["ج", "ش", "س", "ب", "ف", "ر", "ل", "م", "ن", "ك", "ه", "ت"]]
mdd += [l + D + "و" + MADD + "ءُ" for l in ["س", "ج", "ب", "ن", "ف", "ل"]]
mdd += [l + K + "ي" + MADD + "ءِ" for l in ["ج", "س", "ب", "ن", "ف", "ل"]]
page(15, "مد", "The Madd Sign", grid([(ar(x, 46), "") for x in mdd], 4, "words"),
     "حرفِ مدّہ پر مد کی علامت (گلابی ~) ہو تو آواز کو ایک الف سے زیادہ، تقریباً چار سے پانچ حرکت تک کھینچیں۔ صحیح مقدار استاد سے سن کر سیکھیں۔",
     "When the pink madd sign is on a long vowel, stretch it longer, about four to five counts. Learn the length from your teacher.")


# 16-17. Quran
def surah(n, size):
    vs = Q[n - 1]["verses"]
    body = "".join(f'{v["text"]} <span class="an">({str(v["id"]).translate(AD)})</span> ' for v in vs)
    bism = "" if n in (1, 9) else '<p class="bism" lang="ar">بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ</p>'
    return (f'<div class="surah"><h3>سورۃ {Q[n - 1]["name"]} <small>Surah {Q[n - 1]["transliteration"]}</small></h3>'
            f'{bism}<p class="ayat" lang="ar" dir="rtl" style="font-size:{size}px">{body}</p></div>')


page(16, "قرآنی مشق: سورۃ الفاتحہ", "Quran Practice: Al-Fatiha", surah(1, 44),
     "اب قرآن مجید کی پہلی سورت پڑھیں۔ آہستہ، ٹھہر ٹھہر کر اور صحیح مخارج کے ساتھ۔ (رسم الخط: مصحفِ مدینہ)",
     "Now read the opening surah of the Quran, slowly and carefully. (Madinah Mushaf script.)", legend=False)
page(17, "قرآنی مشق: آخری سورتیں", "Quran Practice: The Last Surahs", surah(112, 30) + surah(113, 29) + surah(114, 29),
     "یہ سورتیں نماز میں کثرت سے پڑھی جاتی ہیں۔ استاد کے ساتھ پڑھ کر روزانہ دہرائیں اور یاد کریں۔",
     "These surahs are read often in salah. Read them with your teacher and revise them every day.", legend=False)


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
.grid{{display:grid;grid-auto-rows:1fr;min-height:0;direction:rtl;border:2px solid {G1};border-radius:8px;overflow:hidden;background:{G1};gap:1.2px}}
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
.hj .nm{{font-size:12.5px;line-height:2.3;color:#222}}
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
"""
cover = ('<section class="pg cover"><div class="frame">' + ar("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", 54).replace('fill="#111111"', 'fill="#ffffff"') +
         '<div class="orn"></div><h1>نورانی قاعدہ</h1><p class="en-t">Noorani Qaida</p>'
         '<div class="chips">' + "".join(f'<span style="--c:{c}">{t}</span>' for t, c in [("زبر", RED), ("زیر", BLUE), ("پیش", GREEN), ("جزم", ORANGE), ("شد", PURPLE), ("مد", PINK)]) + '</div>'
         '<p>Colour-coded harakat, spelling (hijje) under every practice word and Urdu instructions on every page, from the first letter to reading the Quran.</p>'
         '<div class="orn"></div><p class="site">QURAN ONLINE TARTEEL · quranonlinetarteel.net</p></div></section>')
TOC = [("حروفِ مفردات", 1), ("حروفِ مرکبات", 2), ("حروفِ مقطعات", 3), ("حرکات", 4), ("حرکات کی مشق", 5), ("تنوین", 6), ("تنوین کی مشق", 7),
       ("کھڑی حرکات", 8), ("حروفِ مدّہ", 9), ("حروفِ لین", 10), ("جزم", 11), ("جزم کی مشق", 12), ("تشدید", 13), ("تشدید کی مشق", 14),
       ("مد", 15), ("سورۃ الفاتحہ", 16), ("آخری سورتیں", 17)]
key = ('<div class="keybox"><h4>رنگوں کی پہچان</h4><div class="keyrow">' + "".join(
    f'<div>{ar(x, 34)}<b style="color:{c}">{t}</b></div>' for x, t, c in
    [("بَ", "زبر", RED), ("بِ", "زیر", BLUE), ("بُ", "پیش", GREEN), ("أَبْ", "جزم", ORANGE), ("أَبَّ", "شد", PURPLE), ("بَآ", "مد", PINK)]) + '</div></div>')
toc = ('<section class="pg"><div class="frame"><header><div class="hd-row"><span class="pno">صفحہ ۲</span><span class="sabaq">فہرست</span><span class="bk">نورانی قاعدہ</span></div>'
       '<h2>اسباق کی فہرست</h2><span class="en">Contents · Colour key · How to use</span></header>'
       '<div class="toc">' + "".join(f'<div><span>سبق {str(n).translate(UD)}: {t}</span><span class="n">{n}</span></div>' for t, n in TOC) + '</div>' + key +
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
await p.pdf({{path:'{OUT_PDF}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print("PDF:", OUT_PDF, os.path.getsize(OUT_PDF) // 1024, "KB,", len(PAGES) + 3, "pages")
