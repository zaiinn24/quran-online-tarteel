#!/usr/bin/env python3
"""Free branded PDFs (A4) rendered from HTML with Chromium (correct Arabic shaping):
  downloads/tajweed-rules-pdf-quran-online-tarteel.pdf
  downloads/morning-evening-adhkar-pdf-quran-online-tarteel.pdf
Usage: python3 scripts/build_resource_pdfs.py"""
import html as H, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import duas_data  # noqa
FONTS = "file://" + os.path.join(ROOT, "assets", "fonts")
Q = {s["id"]: {v["id"]: v["text"] for v in s["verses"]} for s in json.load(open(os.path.join(ROOT, "data", "quran-uthmani.json"), encoding="utf-8"))}
AR_NUM = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def ayahs(s, a1, a2):
    return " ".join(Q[s][i] + " ﴿" + str(i).translate(AR_NUM) + "﴾" for i in range(a1, a2 + 1))


CSS = """
@font-face{font-family:F;src:url(FONTS/fraunces-latin-opsz-normal.woff2)}
@font-face{font-family:M;font-weight:400;src:url(FONTS/manrope-latin-400-normal.woff2)}
@font-face{font-family:M;font-weight:600;src:url(FONTS/manrope-latin-600-normal.woff2)}
@font-face{font-family:M;font-weight:800;src:url(FONTS/manrope-latin-800-normal.woff2)}
@font-face{font-family:A;font-weight:400;src:url(FONTS/amiri-arabic-400-normal.woff2)}
@font-face{font-family:A;font-weight:700;src:url(FONTS/amiri-arabic-700-normal.woff2)}
@page{size:A4;margin:16mm 15mm 18mm}
*{box-sizing:border-box}
body{font-family:M;color:#2b251c;font-size:10.5pt;line-height:1.55;margin:0}
h1,h2,h3{font-family:F;font-weight:600;color:#14110c;margin:0}
.cover{height:262mm;background:#14110c;color:#e9e0cd;border-radius:6mm;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:20mm;page-break-after:always}
.cover:before{content:"";position:absolute;inset:0;opacity:.16;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='none' stroke='%23e2c47e' stroke-width='1.1'%3E%3Cpath d='M40 4l10.6 25.4L76 40 50.6 50.6 40 76 29.4 50.6 4 40l25.4-10.6z'/%3E%3Crect x='22' y='22' width='36' height='36' transform='rotate(45 40 40)'/%3E%3Ccircle cx='40' cy='40' r='9'/%3E%3C/g%3E%3C/svg%3E")}
.cover:after{content:"";position:absolute;inset:7mm;border:1px solid rgba(226,196,126,.4);border-radius:4mm}
.cover>*{position:relative;z-index:1}
.cover .ar{font-family:A;font-weight:700;font-size:44pt;color:#e2c47e;margin-bottom:8mm}
.cover h1{color:#fff;font-size:30pt;line-height:1.15;margin-bottom:6mm}
.cover p{font-size:12pt;color:#d9cfba;max-width:140mm;margin:0 auto 10mm}
.cover .brand{font-family:F;font-size:14pt;color:#e2c47e}
.cover .url{font-size:10pt;color:#cfc4ac;margin-top:2mm}
.chip{display:inline-block;font-size:8.5pt;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#e2c47e;border:1px solid rgba(226,196,126,.6);border-radius:99px;padding:2mm 5mm;margin-bottom:8mm}
h2{font-size:17pt;margin:8mm 0 3mm;padding-top:3mm;border-top:2px solid #c79b45}
h2.first{margin-top:0}
h3{font-size:12.5pt;margin:5mm 0 2mm}
p{margin:0 0 3mm}
table{width:100%;border-collapse:collapse;margin:2mm 0 5mm;font-size:10pt;page-break-inside:avoid}
th{background:#14110c;color:#e2c47e;text-align:left;padding:2.4mm 3mm;font-weight:800;font-size:9pt}
td{padding:2.4mm 3mm;border-bottom:1px solid #e6dcc6;vertical-align:top}
tr:nth-child(even) td{background:#fcf9f2}
.ar{font-family:A;direction:rtl}
td .ar{font-size:15pt;line-height:1.5}
.box{background:#fbf3e1;border:1px solid rgba(199,155,69,.45);border-radius:3mm;padding:4mm 5mm;margin:4mm 0;page-break-inside:avoid}
.card{border:1px solid #e6dcc6;border-radius:3mm;padding:4.5mm 5mm;margin:0 0 4.5mm;page-break-inside:avoid}
.card .t{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2mm}
.card .t b{font-family:F;font-size:12.5pt;color:#14110c;font-weight:600}
.card .t span{font-size:8.5pt;font-weight:800;color:#86601a;background:#f4ecdb;border-radius:99px;padding:1mm 3mm;white-space:nowrap}
.card .a{font-family:A;direction:rtl;text-align:right;font-size:17pt;line-height:2;color:#14110c;margin-bottom:2mm}
.card .tr{font-style:italic;color:#6e6453;margin-bottom:1.5mm}
.card .en{margin-bottom:1mm}
.card .ur{color:#6e6453;font-size:9.5pt;margin-bottom:1.5mm}
.card .ref{font-size:8.5pt;letter-spacing:.06em;text-transform:uppercase;color:#86601a;font-weight:800}
.end{page-break-before:always;background:#14110c;color:#e9e0cd;border-radius:6mm;padding:16mm;text-align:center}
.end h2{color:#fff;border:0;font-size:20pt;margin:0 0 5mm}
.end p{color:#d9cfba;font-size:11pt}
.end ul{list-style:none;padding:0;margin:6mm auto;max-width:120mm;text-align:left}
.end li{padding:2mm 0;border-bottom:1px dashed rgba(226,196,126,.3)}
.end li:before{content:"\\2713  ";color:#e2c47e;font-weight:800}
.end .go{display:inline-block;background:#c79b45;color:#14110c;font-weight:800;border-radius:99px;padding:4mm 9mm;margin-top:4mm;font-size:12pt}
.end .small{font-size:9pt;color:#bfb39a;margin-top:6mm}
""".replace("FONTS", FONTS)

FOOT = ('<div style="width:100%;font-family:Arial;font-size:7.5pt;color:#86601a;padding:0 15mm;display:flex;justify-content:space-between">'
        '<span>Quran Online Tarteel &middot; quranonlinetarteel.net</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')

END = ('<div class="end"><div class="chip">Learn with a teacher</div><h2>Learn the Quran with a Female Teacher</h2>'
       '<p>A PDF shows you the words. A teacher makes sure every letter is right. At Quran Online Tarteel, female teachers teach children and women live, one to one, in English, Urdu or Arabic.</p>'
       '<ul><li>Noorani Qaida, Quran reading, Tajweed and Hifz</li><li>Translation, Tafseer, salah and daily duas</li>'
       '<li>Classes at times that suit your country</li><li>2 free trial classes, then a simple monthly fee paid in advance</li></ul>'
       '<div class="go">Book 2 free classes: quranonlinetarteel.net/free-trial</div>'
       '<p class="small">WhatsApp +92 334 5259952 &middot; info@quranonlinetarteel.net<br>Free to share for personal and teaching use. Please do not sell it.</p></div>')


def cover(ar, title, sub, chip):
    return (f'<div class="cover"><div class="chip">{chip}</div><div class="ar">{ar}</div><h1>{title}</h1><p>{sub}</p>'
            '<div class="brand">Quran Online Tarteel</div><div class="url">quranonlinetarteel.net</div></div>')


def t(rows, head):
    return ("<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")


def ar(x):
    return f'<span class="ar">{x}</span>'


def tajweed_html():
    b = cover("التجويد", "Tajweed Rules for Beginners", "A clear guide to the main rules of Tajweed, with Arabic examples and charts, from makharij to madd.", "Free PDF Guide")
    b += '<h2 class="first">What Is Tajweed?</h2>'
    b += ('<p>Tajweed means reciting the Quran correctly: every letter from its right place (makhraj), with its right qualities (sifaat), length and nasal sound. '
          'Allah says: "And recite the Quran with measured recitation (tartil)" (Quran 73:4). Mistakes that change a letter or meaning are called clear mistakes (lahn jali) and must be avoided. '
          'Mistakes that only spoil the beauty of recitation are hidden mistakes (lahn khafi).</p>')
    b += '<div class="box"><b>How to use this guide:</b> learn one section at a time, find the rule on a page of Juz Amma, recite it slowly, then recite it to a teacher. Tajweed is learned by listening and being corrected.</div>'
    b += "<h2>1. Makharij: Where Letters Come From</h2><p>Most teachers follow Imam Ibn al-Jazari: 17 points of articulation in 5 areas.</p>"
    b += t([["Empty space of mouth and throat (Al-Jawf)", "The three madd letters: " + ar("ا و ي")],
            ["Throat (Al-Halq)", "Deepest: " + ar("ء ه") + " &nbsp; Middle: " + ar("ع ح") + " &nbsp; Top: " + ar("غ خ")],
            ["Tongue (Al-Lisan)", ar("ق ك ج ش ي ض ل ن ر ط د ت ص س ز ظ ذ ث")],
            ["Lips (Ash-Shafatan)", ar("ف") + " (lower lip and upper teeth), " + ar("ب م و") + " (both lips)"],
            ["Nasal passage (Al-Khayshum)", "The ghunnah of noon and meem"]], ["Area", "Letters"])
    b += '<div class="box"><b>Test any letter:</b> say it with a sukoon after a hamza with fatha, for example ' + ar("أَبْ، أَعْ، أَقْ") + '. Where the sound stops is its makhraj.</div>'
    b += "<h2>2. Heavy and Light Letters</h2>"
    b += "<p>Seven letters are always heavy (full-mouthed), remembered as " + ar("خُصَّ ضَغْطٍ قِظْ") + ": " + ar("خ ص ض غ ط ق ظ") + ". Keep them distinct from their light partners:</p>"
    b += t([[ar("س") + " / " + ar("ص"), "Seen is light, Saad is heavy"], [ar("ت") + " / " + ar("ط"), "Ta is light, the heavy Ta is deep"],
            [ar("د") + " / " + ar("ض"), "Dal is light, Daad is heavy and unique to Arabic"], [ar("ذ") + " / " + ar("ظ"), "Both like 'th' in 'this', Dha is heavy"],
            [ar("ك") + " / " + ar("ق"), "Kaf from the front, Qaf from the very back of the tongue"], [ar("ه") + " / " + ar("ح"), "Soft h from the chest, sharp h from the throat"]],
           ["Pair", "Difference"])
    b += "<h2>3. Noon Sakinah and Tanween</h2><p>A noon with sukoon (" + ar("نْ") + ") or tanween (" + ar("ـً ـٍ ـٌ") + ") follows one of four rules, depending on the next letter.</p>"
    b += t([["Izhar (clear)", ar("ء ه ع ح غ خ"), "Pronounce the noon clearly, no ghunnah", ar("مِنْ عِلْمٍ")],
            ["Idgham with ghunnah", ar("ي ن م و"), "Merge into the next letter with a 2 count ghunnah", ar("مَن يَقُولُ")],
            ["Idgham without ghunnah", ar("ل ر"), "Merge fully, no ghunnah", ar("مِن رَّبِّهِمْ")],
            ["Iqlab (changing)", ar("ب"), "Change noon to a hidden meem with ghunnah", ar("مِنۢ بَعْدِ")],
            ["Ikhfa (hiding)", "The other 15 letters", "Hide the noon with a 2 count ghunnah", ar("مِن قَبْلِ")]],
           ["Rule", "Letters", "What to do", "Example"])
    b += '<div class="box"><b>Memory tips:</b> the six Idgham letters are in ' + ar("يَرْمَلُونَ") + ', the four with ghunnah in ' + ar("يَنْمُو") + '. Idgham only happens between two words: in ' + ar("الدُّنْيَا، بُنْيَانٌ، قِنْوَانٌ، صِنْوَانٌ") + ' the noon is read clearly.</div>'
    b += "<h2>4. Meem Sakinah</h2>"
    b += t([["Ikhfa shafawi", ar("ب"), "Hide the meem with ghunnah, lips lightly closed", ar("تَرْمِيهِم بِحِجَارَةٍ")],
            ["Idgham shafawi", ar("م"), "Merge into the next meem with ghunnah", ar("لَهُم مَّا")],
            ["Izhar shafawi", "All other letters", "Pronounce the meem clearly", ar("أَمْ لَمْ")]], ["Rule", "Next letter", "What to do", "Example"])
    b += "<h2>5. Ghunnah</h2><p>Noon and meem with a shaddah (" + ar("نّ مّ") + ") are always read with a ghunnah (nasal sound) of about 2 counts, as in " + ar("إِنَّ") + " and " + ar("ثُمَّ") + ". Pinch your nose: if the sound stops, your ghunnah is coming from the right place.</p>"
    b += "<h2>6. Qalqalah</h2><p>Five letters, remembered as " + ar("قُطْبُ جَدٍّ") + " (" + ar("ق ط ب ج د") + "), are released with a slight echo when they carry a sukoon.</p>"
    b += t([["Minor (sughra)", "Sukoon in the middle of reading", "Light bounce", ar("يَجْعَلُونَ")],
            ["Major (kubra)", "Stopping on the letter at a verse end", "Stronger bounce", ar("أَحَدْ")]], ["Level", "When", "Strength", "Example"])
    b += '<div class="box"><b>Do not add a vowel:</b> ' + ar("أَحَدْ") + ' bounces at the end, but must not become "ahada".</div>'
    b += "<h2>7. Madd: Lengthening</h2><p>The madd letters are alif after fatha, waw sakinah after damma and ya sakinah after kasra. Counts below follow Hafs from Asim.</p>"
    b += t([["Natural (tabi'i)", "No hamza or sukoon after the madd letter", "2", ar("قَالَ")],
            ["Muttasil (connected)", "Hamza after it in the same word", "4 or 5", ar("جَآءَ")],
            ["Munfasil (separated)", "Hamza at the start of the next word", "4 or 5 (2 also narrated)", ar("يَٰٓأَيُّهَا")],
            ["Badal", "Hamza before the madd letter", "2", ar("ءَامَنُوا۟")],
            ["'Aarid lis-sukoon", "Stopping after a madd letter", "2, 4 or 6", ar("نَسْتَعِينْ")],
            ["Leen", "Stopping after waw or ya sakinah following a fatha", "2, 4 or 6", ar("خَوْفْ")],
            ["Lazim", "Permanent sukoon or shaddah after the madd letter", "6", ar("ٱلضَّآلِّينَ")]],
           ["Type", "When", "Counts", "Example"])
    b += "<h2>8. Lam Rules</h2>"
    b += t([["Lam qamariyyah (pronounced)", ar("ا ب ج ح خ ع غ ف ق ك م و ه ي"), ar("ٱلْقَمَرُ")],
            ["Lam shamsiyyah (silent, next letter doubled)", ar("ت ث د ذ ر ز س ش ص ض ط ظ ل ن"), ar("ٱلشَّمْسُ")]], ["Rule", "Letters after ٱل", "Example"])
    b += "<p>The lam in the name " + ar("ٱللَّه") + " is heavy after a fatha or damma (" + ar("قَالَ ٱللَّهُ") + ") and light after a kasra (" + ar("بِسْمِ ٱللَّهِ") + ").</p>"
    b += "<h2>9. Ra: Heavy or Light</h2>"
    b += t([["Heavy", "Ra with fatha or damma, or sukoon after fatha or damma", ar("رَبِّ، قُرْءَان")],
            ["Light", "Ra with kasra, or sukoon after kasra", ar("رِجَال، فِرْعَوْن")]], ["Ra is", "When (basic rule)", "Example"])
    b += "<p>There are more detailed cases, which your teacher will explain once the basics are steady.</p>"
    b += "<h2>10. Stop Signs in the Mushaf</h2>"
    b += t([[ar("مـ"), "Necessary stop: stop here"], [ar("لا"), "Do not stop here"], [ar("ج"), "Stopping and continuing are both fine"],
            [ar("صلى"), "Continuing is preferred"], [ar("قلى"), "Stopping is preferred"], [ar("∴ ∴"), "Stop at one of the two places, not both"]],
           ["Sign", "Meaning"])
    b += '<div class="box"><b>Practise with:</b> Surah Al-Fatiha (madd, lam rules), Surah Al-Ikhlas (qalqalah), Surah Al-Falaq (ikhfa) and Surah An-Nas (ghunnah). Read more guides on our blog: quranonlinetarteel.net/blog</div>'
    return b + END


def adhkar_html():
    items = duas_data.PAGES["morning-evening-azkar"]["items"]
    b = cover("أذكار الصباح والمساء", "Morning and Evening Adhkar", "Authentic morning and evening remembrance from the Quran and Sunnah, with Arabic, transliteration, meaning in English and Roman Urdu, counts and references.", "Free PDF")
    b += '<h2 class="first">When to Read Them</h2>'
    b += ("<p>Read the morning adhkar after Fajr until sunrise, and the evening adhkar after Asr until sunset (many scholars allow them after Maghrib too). "
          "Allah says: \"And glorify Him morning and evening\" (Quran 33:42). They are a shield and a source of peace for the whole day.</p>")
    b += t([["Ayatul Kursi", "1"], ["The 3 Quls", "3 each"], ["Asbahna wa asbahal mulku lillah", "1"], ["Allahumma bika asbahna", "1"], ["Sayyid al-Istighfar", "1"],
            ["Allahumma 'afini fi badani", "3"], ["Bismillahil ladhi la yadurru", "3"], ["Ya hayyu ya qayyum", "1"], ["SubhanAllahi wa bihamdihi", "100"],
            ["A'udhu bikalimatillahit tammat (evening)", "3"]], ["Dhikr", "How many times"])
    b += '<div class="box"><b>In the evening:</b> say <i>amsayna</i> (we have reached the evening) in place of <i>asbahna</i> (we have reached the morning), and <i>amsal mulku</i> in place of <i>asbahal mulku</i>. In the evening of the fourth dhikr the order becomes: <i>bika amsayna wa bika asbahna ... wa ilaykal masir</i>.</div>'
    b += "<h2>The Adhkar</h2>"
    for it in items:
        title, a, tr, en, ur, cnt, ref = it[:7]
        if isinstance(a, tuple):
            _, su, ay, _, _ = a
            a = ayahs(su, ay, ay)
        elif a == "QULS":
            a = (f"سورة الإخلاص: {ayahs(112, 1, 4)}<br>سورة الفلق: {ayahs(113, 1, 5)}<br>سورة الناس: {ayahs(114, 1, 6)}")
        ref = H.unescape(__import__("re").sub(r"<[^>]+>", "", ref)).replace("See the full text on our Ayatul Kursi and 4 Quls page.", "").strip()
        times = f"{cnt} time" + ("" if str(cnt) == "1" else "s")
        b += (f'<div class="card"><div class="t"><b>{H.escape(title)}</b><span>{H.escape(times)}</span></div><div class="a">{a}</div>'
              f'<div class="tr">{H.escape(tr)}</div><div class="en">{H.escape(en)}</div><div class="ur">{H.escape(ur)}</div><div class="ref">{H.escape(ref)}</div></div>')
    return b + END


def render(page, body, out, title):
    h = f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
    tmp = os.path.join(ROOT, "scripts", "_pdf_tmp.html")
    open(tmp, "w", encoding="utf-8").write(h)
    page.goto("file://" + tmp)
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(400)
    page.pdf(path=out, format="A4", print_background=True, display_header_footer=True, header_template="<div></div>", footer_template=FOOT,
             margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
    os.remove(tmp)
    print("pdf", os.path.basename(out), os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        render(pg, tajweed_html(), os.path.join(ROOT, "downloads", "tajweed-rules-pdf-quran-online-tarteel.pdf"), "Tajweed Rules for Beginners (Free PDF) - Quran Online Tarteel")
        render(pg, adhkar_html(), os.path.join(ROOT, "downloads", "morning-evening-adhkar-pdf-quran-online-tarteel.pdf"), "Morning and Evening Adhkar (Free PDF) - Quran Online Tarteel")
        b.close()
