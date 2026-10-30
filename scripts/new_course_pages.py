#!/usr/bin/env python3
"""Create the 5 new course pages from the Islamic Studies page template. Safe to re-run (overwrites the 5 pages)."""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from faqlib import details, ld

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, "online-islamic-studies", "index.html")).read()
SITE = "https://quranonlinetarteel.net/"
A = lambda href, text: f'<a href="../{href}" class="in-link">{text}</a>'
TICK = '<span class="tick"><svg width="14" height="14"><use href="#i-tick"/></svg></span>'


# ---------- original illustrations (no people, no faces) ----------
def frame(uid, title, inner):
    return (f'<svg class="illus" viewBox="0 0 480 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}"><title>{title}</title>'
            f'<defs><linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2c47e"/><stop offset="1" stop-color="#a97f2e"/></linearGradient>'
            f'<linearGradient id="{uid}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e261a"/><stop offset="1" stop-color="#14110c"/></linearGradient>'
            f'<radialGradient id="{uid}glow" cx=".5" cy=".35" r=".6"><stop offset="0" stop-color="#c79b45" stop-opacity=".45"/><stop offset="1" stop-color="#c79b45" stop-opacity="0"/></radialGradient>'
            f'<pattern id="{uid}pat" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M20 3l5 12 12 5-12 5-5 12-5-12-12-5 12-5z" fill="none" stroke="#c79b45" stroke-opacity=".14"/></pattern></defs>'
            f'<path d="M60 400V170C60 80 150 22 240 22s180 58 180 148V400Z" fill="url(#{uid}bg)"/>'
            f'<path d="M60 400V170C60 80 150 22 240 22s180 58 180 148V400Z" fill="url(#{uid}pat)"/>'
            f'<ellipse cx="240" cy="140" rx="190" ry="150" fill="url(#{uid}glow)"/>'
            f'<path d="M48 400V168C48 72 142 10 240 10s192 62 192 158V400" fill="none" stroke="url(#{uid}g)" stroke-width="2.5"/>'
            f'<path d="M72 400V172C72 92 156 36 240 36s168 56 168 136V400" fill="none" stroke="#c79b45" stroke-opacity=".35" stroke-width="1"/>'
            + inner + "</svg>")


def star(x, y, r, op=.7):
    pts = []
    import math
    for i in range(16):
        rr = r if i % 2 == 0 else r * .7
        a = math.pi / 8 * i
        pts.append(f"{x + rr * math.sin(a):.1f},{y - rr * math.cos(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="#e2c47e" opacity="{op}"/>'


def crescent(x, y, r):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e2c47e"/><circle cx="{x + r * .42}" cy="{y - r * .28}" r="{r * .84}" fill="#2a2318"/>'


def open_book(cx, cy, w, text, fs=34, uid="b"):
    h = w * .55
    return (f'<g transform="translate({cx},{cy})"><path d="M0 {-h*.42}C{-w*.25} {-h*.62} {-w*.42} {-h*.58} {-w/2} {-h*.5}V{h*.5}C{-w*.42} {h*.42} {-w*.25} {h*.38} 0 {h*.55}Z" fill="#fbf7ee"/>'
            f'<path d="M0 {-h*.42}C{w*.25} {-h*.62} {w*.42} {-h*.58} {w/2} {-h*.5}V{h*.5}C{w*.42} {h*.42} {w*.25} {h*.38} 0 {h*.55}Z" fill="#f4ecdb"/>'
            f'<path d="M0 {-h*.42}V{h*.55}" stroke="#a97f2e" stroke-width="2"/>'
            f'<path d="M{-w/2-6} {-h*.5+6}V{h*.5+8}C{-w*.3} {h*.45} {-w*.12} {h*.5} 0 {h*.66}C{w*.12} {h*.5} {w*.3} {h*.45} {w/2+6} {h*.5+8}V{-h*.5+6}" fill="none" stroke="url(#{uid}g)" stroke-width="4"/>'
            f'<text x="0" y="{fs*.35}" text-anchor="middle" font-family="Amiri, \'Traditional Arabic\', serif" font-size="{fs}" fill="#14110c">{text}</text></g>')


ILL = {
 "salah": lambda u: frame(u, "Prayer mat for learning salah step by step",
    crescent(240, 92, 22) + star(150, 110, 7) + star(330, 120, 6, .5) +
    '<g transform="translate(240,265)"><rect x="-92" y="-108" width="184" height="236" rx="14" fill="#2f5d50"/>'
    '<rect x="-80" y="-96" width="160" height="212" rx="10" fill="none" stroke="#e2c47e" stroke-width="2.5"/>'
    '<path d="M-52 116V-30C-52 -74 -26 -92 0 -92S52 -74 52 -30V116" fill="#25574a" stroke="#e2c47e" stroke-width="2"/>'
    '<path d="M-30 -28C-30 -52 -16 -64 0 -64S30 -52 30 -28" fill="none" stroke="#e2c47e" stroke-opacity=".6" stroke-width="1.5"/>'
    + "".join(f'<rect x="{-62 + i * 26}" y="88" width="14" height="14" rx="2" transform="rotate(45 {-55 + i * 26} 95)" fill="#e2c47e" opacity=".75"/>' for i in range(5)) +
    '<path d="M-92 -78H-108M-92 -48H-108M-92 -18H-108M-92 12H-108M-92 42H-108M-92 72H-108M92 -78H108M92 -48H108M92 -18H108M92 12H108M92 42H108M92 72H108" stroke="#e2c47e" stroke-width="2" stroke-linecap="round"/></g>'),
 "juzamma": lambda u: frame(u, "Open Quran at Juz Amma, the short surahs",
    star(130, 96, 7) + star(352, 104, 6, .55) + crescent(240, 70, 16) +
    open_book(240, 230, 290, "عَمَّ يَتَسَاءَلُونَ", 34, u) +
    "".join(f'<circle cx="{120 + i * 10}" cy="352" r="3" fill="#e2c47e" opacity="{.35 + (i % 5) * .12:.2f}"/>' for i in range(25))),
 "duas": lambda u: frame(u, "Lantern and words of dua for the daily duas course",
    star(140, 90, 7) + star(345, 112, 6, .5) + star(300, 70, 5, .6) +
    '<g transform="translate(240,120)"><line x1="0" y1="-60" x2="0" y2="-20" stroke="#c79b45" stroke-width="2"/><circle cx="0" cy="-16" r="6" fill="none" stroke="#c79b45" stroke-width="2"/>'
    '<path d="M-22 8C-22 -6 -12 -12 0 -12S22 -6 22 8Z" fill="url(#' + u + 'g)"/><rect x="-28" y="6" width="56" height="7" rx="2" fill="#a97f2e"/>'
    '<path d="M-26 13H26L31 66H-31Z" fill="#e2c47e" opacity=".9"/><path d="M-18 18H18L22 61H-22Z" fill="#fff3cf"/><ellipse cx="0" cy="40" rx="9" ry="14" fill="#ffd27a"/>'
    '<rect x="-34" y="64" width="68" height="8" rx="2" fill="#a97f2e"/></g>'
    '<text x="240" y="285" text-anchor="middle" font-family="Amiri, serif" font-size="46" fill="#fbf7ee">رَّبِّ زِدْنِي عِلْمًا</text>'
    '<path d="M150 318H330" stroke="url(#' + u + 'g)" stroke-width="2"/><path d="M200 334H280" stroke="#c79b45" stroke-opacity=".5" stroke-width="1.5"/>'),
 "hadith40": lambda u: frame(u, "Stack of hadith books with the number forty",
    star(140, 96, 7) + star(340, 100, 6, .5) +
    '<g transform="translate(240,250)">'
    '<rect x="-120" y="40" width="240" height="34" rx="6" fill="#2f5d50"/><rect x="-120" y="40" width="240" height="34" rx="6" fill="none" stroke="#e2c47e" stroke-opacity=".6" stroke-width="2"/>'
    '<rect x="-108" y="4" width="216" height="34" rx="6" fill="#b5655a"/><rect x="-108" y="4" width="216" height="34" rx="6" fill="none" stroke="#e2c47e" stroke-opacity=".6" stroke-width="2"/>'
    '<rect x="-96" y="-32" width="192" height="34" rx="6" fill="#3c6e74"/><rect x="-96" y="-32" width="192" height="34" rx="6" fill="none" stroke="#e2c47e" stroke-opacity=".6" stroke-width="2"/>'
    '<path d="M-100 57H100M-90 21H90M-80 -15H80" stroke="#e2c47e" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="6 6"/>'
    '<circle cx="0" cy="-104" r="58" fill="url(#' + u + 'g)"/><circle cx="0" cy="-104" r="48" fill="#14110c"/>'
    '<text x="0" y="-86" text-anchor="middle" font-family="Amiri, serif" font-size="54" fill="#e2c47e">٤٠</text></g>'),
 "newmuslim": lambda u: frame(u, "Sunrise with crescent and open Quran for new Muslims",
    '<circle cx="240" cy="250" r="120" fill="#e2c47e" opacity=".14"/><circle cx="240" cy="250" r="86" fill="#e2c47e" opacity=".22"/>'
    + "".join(f'<line x1="240" y1="250" x2="{240 + 150 * __import__("math").cos(__import__("math").pi * (1 + i / 8)):.1f}" y2="{250 + 150 * __import__("math").sin(__import__("math").pi * (1 + i / 8)):.1f}" stroke="#e2c47e" stroke-opacity=".25" stroke-width="2"/>' for i in range(1, 8))
    + crescent(240, 120, 26) + star(286, 96, 8, .9) + star(150, 130, 6, .5) + star(330, 160, 5, .5) +
    '<path d="M70 300H410" stroke="url(#' + u + 'g)" stroke-width="2.5"/>' + open_book(240, 330, 230, "بِسْمِ ٱللَّهِ", 30, u)),
}


# ---------- page content ----------
PAGES = {
 "juz-amma-memorization-online": dict(
  cid="juzamma", course_opt="Juz Amma Memorisation", nav="Juz Amma Memorisation", ill="juzamma",
  title="Juz Amma Memorization Online for Kids | Amma Para Hifz",
  desc="Memorize Juz Amma online with a female teacher. Live 1-on-1 classes for kids and women to learn the short surahs (Amma Para) with Tajweed. 2 free classes.",
  course_name="Juz Amma Memorization Online Classes", crumb="Juz Amma Memorization",
  eyebrow="Short Surahs, Strong Start",
  h1='Juz Amma Memorization Online <span class="gold">for Kids and Women</span>',
  lead="Memorize Juz Amma, the 30th Juz of the Quran also called Amma Para, in live one-to-one online classes with a female teacher. Your teacher listens to every ayah, corrects your Tajweed and builds a gentle daily revision routine, so the short surahs you use in salah stay with you for life.",
  points=["All 37 short surahs", "Correct Tajweed from day one", "Daily revision plan", "Female teachers"],
  what_h2="What Is Juz Amma and Why Memorize It First?",
  what=("<p>Juz Amma is the 30th and last Juz of the Quran. It begins with Surah An-Naba (<em>Amma yatasa'alun</em>) and ends with Surah An-Nas, 37 surahs in all. Most of them are short, which is why Juz Amma memorization is the first Hifz goal for so many children and adults.</p>"
        "<p>These are the surahs we recite most in salah, so learning them well brings your prayer to life. Many children start from Surah An-Nas and work backwards, one short surah at a time, while women often memorize alongside their children.</p>"
        "<h3>For kids</h3><p>Short, cheerful lessons with lots of repetition, praise and a little homework, as part of our " + A("online-quran-classes-for-kids/", "online Quran classes for kids") + ".</p>"
        "<h3>For women</h3><p>A calm, private class with a female teacher who corrects you gently, at a time that fits your day.</p>"),
  topics_h2="What You Learn in Our Juz Amma Memorization Classes",
  topics=[("ن", "The Short Surahs", "Memorize from An-Nas to An-Naba, or follow the order your teacher suggests for your level."),
          ("ت", "Tajweed While You Memorize", "Correct makharij, ghunnah and madd from the start, so mistakes never set in. See our " + A("online-tajweed-classes/", "online Tajweed classes") + "."),
          ("ر", "Daily Revision", "A simple routine of new lesson, recent revision and old revision keeps every surah fresh."),
          ("م", "Meaning in Simple Words", "A short explanation of each surah in English or Urdu, so children know what they are saying."),
          ("ص", "Using Surahs in Salah", "Practise reciting your new surahs in prayer with confidence."),
          ("ح", "Next Steps to Hifz", "Finish Juz Amma and move on to our full " + A("online-hifz-program/", "online Hifz program") + " if you wish.")],
  steps_h2="How Our Online Juz Amma Classes Work",
  steps=[("Tell Us Your Level", "Share your child's age, or your own, and whether they can already read the Quran."),
         ("2 Free Classes", "Your female teacher listens, checks reading and starts the first surah."),
         ("Daily Plan", "Choose 2, 4 or 5 days a week with a clear memorization and revision plan."),
         ("Practise at Home", "A few minutes of daily listening and repetition between classes.")],
  mini=("Give your child the surahs they will recite for life", "Start Juz Amma memorization with 2 free classes."),
  wa="Assalamu alaikum, I want Juz Amma memorization classes.",
  faqs=[("How many surahs are in Juz Amma?", "Juz Amma has 37 surahs, from Surah An-Naba (78) to Surah An-Nas (114). It is the 30th and last Juz of the Quran, also called Amma Para."),
        ("How long does it take to memorize Juz Amma?", "It depends on age, reading level and how many days a week you study. Short surahs can be memorized in a few classes, and longer ones take more time. Your teacher will give you a realistic plan after the free classes."),
        ("Does my child need to read the Quran before memorizing Juz Amma?", "It helps, but it is not required. Younger children can memorize by listening and repeating after the teacher, while learning to read with " + A("noorani-qaida-online/", "Noorani Qaida") + " at the same time."),
        ("What age can my child start Juz Amma memorization?", "Many children start the shortest surahs from around age 4 or 5, learning by listening and repeating. Lessons are kept gentle and short so they enjoy it."),
        ("Can adults and women memorize Juz Amma online?", "Yes. Many sisters memorize Juz Amma to strengthen their salah. Your female teacher sets a pace that fits your day, with private one-to-one classes.")],
 ),
 "online-salah-classes": dict(
  cid="salah", course_opt="Salah (Prayer) Lessons", nav="Salah (Namaz) Classes", ill="salah",
  title="Online Salah Classes | Learn How to Pray Namaz Online",
  desc="Learn how to pray salah step by step in live online namaz classes with a female teacher. Wudu, rakats and what to recite, for kids, women and new Muslims. 2 free classes.",
  course_name="Online Salah Classes: Learn How to Pray Namaz", crumb="Online Salah Classes",
  eyebrow="Learn to Pray, Step by Step",
  h1='Online Salah Classes: <span class="gold">Learn How to Pray Namaz</span>',
  lead="Learn how to pray salah correctly, step by step, in live one-to-one online namaz classes with a female teacher. From wudu to the final salam, your teacher shows you what to do, what to recite and how many rakats each prayer has, with patient practice until you can pray with confidence.",
  points=["Wudu step by step", "What to recite in each position", "Rakats of the 5 daily prayers", "For kids, women and new Muslims"],
  what_h2="What Are Online Salah Classes?",
  what=("<p>Salah is the second pillar of Islam and the first thing we will be asked about. Our online salah classes teach children and women the complete prayer in a calm, one-to-one setting, so nothing is skipped and no question feels too small.</p>"
        "<p>Your teacher demonstrates each step, listens to your recitation and corrects you kindly. Lessons focus on the agreed basics of prayer. Where practice differs between schools, the teacher follows what your family practises.</p>"
        "<h3>Namaz classes for kids</h3><p>Children learn wudu and salah through short, friendly lessons and lots of practice, alongside their " + A("online-quran-classes-for-kids/", "Quran classes for kids") + ".</p>"
        "<h3>Salah lessons for women and new Muslims</h3><p>Sisters who never learned properly, or who are " + A("quran-classes-for-new-muslims/", "new to Islam") + ", learn privately with a female teacher, at their own pace.</p>"),
  topics_h2="What You Learn in Our Namaz Classes",
  topics=[("و", "Wudu (Ablution)", "Each step of wudu in order, and what breaks it, practised in class."),
          ("ص", "The Positions of Salah", "Standing, ruku, sujood and sitting, with the correct movements for each."),
          ("ف", "What to Recite", "Takbir, Surah Al-Fatiha, a short surah, the words of ruku and sujood, tashahhud and salam, with correct pronunciation."),
          ("ر", "Rakats of Each Prayer", "Fajr 2, Dhuhr 4, Asr 4, Maghrib 3 and Isha 4 fard rakats. See our " + A("resources/how-many-rakats/", "how many rakats guide") + "."),
          ("م", "Meaning of the Words", "Understand what you are saying in salah, explained in English or Urdu."),
          ("ق", "Short Surahs for Salah", "Memorize short surahs to recite in prayer with our " + A("juz-amma-memorization-online/", "Juz Amma memorization classes") + ".")],
  steps_h2="How Our Online Namaz Classes Work",
  steps=[("Tell Us Who Is Learning", "A child, yourself or both. Share what you already know."),
         ("2 Free Classes", "Your female teacher starts with wudu and the first steps of prayer."),
         ("Weekly Plan", "Choose 2, 4 or 5 days a week. Most students pray confidently within a few weeks of practice."),
         ("Pray at Home", "Practise each prayer at home and bring questions to the next class.")],
  mini=("Help your child fall in love with salah", "Start learning how to pray with 2 free classes."),
  wa="Assalamu alaikum, I want online salah (namaz) classes.",
  faqs=[("Can I really learn how to pray salah online?", "Yes. In a live one-to-one class your teacher watches each step, listens to your recitation and corrects you on the spot. Young children keep their camera on so the teacher can guide their movements, and for women the camera is optional."),
        ("What age should a child start learning salah?", "Many families begin gently around age 7, and younger children often enjoy copying their parents before that. Our teachers adapt each lesson to your child's age."),
        ("Do I need to know Arabic to learn salah?", "No. Your teacher teaches the Arabic words of the prayer slowly, with their meaning in English or Urdu, until you can recite them correctly."),
        ("Which school of thought do you follow for salah?", "Lessons focus on the agreed basics of prayer. Where practice differs between schools, your teacher explains kindly and follows what your family practises."),
        ("Are salah classes available for new Muslim sisters?", "Yes. New Muslim sisters learn salah privately with a female teacher, starting from wudu and the shahada, at a gentle pace. See our " + A("quran-classes-for-new-muslims/", "classes for new Muslims") + ".")],
 ),
 "online-duas-course": dict(
  cid="duas", course_opt="Daily Duas Course", nav="Daily Duas Course", ill="duas",
  title="Masnoon Duas Course Online | Daily Duas for Kids & Women",
  desc="Learn masnoon duas online with a female teacher. Daily duas for kids, morning and evening adhkar and Rabbana duas with meaning in English and Urdu. 2 free classes.",
  course_name="Online Masnoon Duas Course for Kids and Women", crumb="Daily Duas Course",
  eyebrow="Duas for Every Moment",
  h1='Masnoon Duas Course Online: <span class="gold">Daily Duas for Kids and Women</span>',
  lead="Learn the masnoon duas of the Prophet, peace be upon him, for every part of the day, in a live online duas course with a female teacher. Children and women learn each dua with correct Arabic pronunciation, its meaning in English or Urdu and when to say it, so remembering Allah becomes a daily habit.",
  points=["Daily masnoon duas", "Morning and evening adhkar", "Rabbana duas from the Quran", "Meaning in English and Urdu"],
  what_h2="What Is Our Online Duas Course?",
  what=("<p>Duas are how we speak to Allah throughout the day: when we wake up, eat, leave the house, travel and go to sleep. Our online duas course teaches these short, beautiful duas one by one, with the Arabic, the meaning and the moment to say them.</p>"
        "<p>Every dua we teach comes from the Quran or from authentic hadith, with its reference. Lessons are short and repetitive for children and calm and private for women.</p>"
        "<h3>Daily duas for kids</h3><p>Children learn a new dua at a time through repetition, stories and practice, as part of " + A("online-islamic-studies/", "Islamic studies for kids") + ".</p>"
        "<h3>Duas for women</h3><p>Sisters learn the morning and evening adhkar, duas from the Quran and duas for hard times, privately with a female teacher.</p>"),
  topics_h2="Duas You Learn in Our Masnoon Duas Course",
  topics=[("ص", "Morning and Evening Adhkar", "The remembrance of Allah for the start and end of each day."),
          ("ي", "Everyday Duas for Kids", "Waking up, sleeping, eating, entering and leaving home, the toilet and travelling."),
          ("ر", "Rabbana Duas from the Quran", "Duas such as <em>Rabbana atina fid-dunya hasanah</em> (Al-Baqarah 2:201)."),
          ("ك", "Ayatul Kursi and the 3 Quls", "Learn Ayatul Kursi (Al-Baqarah 2:255) and Surahs Al-Ikhlas, Al-Falaq and An-Nas for protection."),
          ("ن", "Duas After Namaz", "The adhkar after the obligatory prayers, linked to our " + A("online-salah-classes/", "online salah classes") + "."),
          ("ع", "Duas for Hard Times", "Duas for worry, illness and gratitude, with their meaning and reference.")],
  steps_h2="How Our Online Duas Classes Work",
  steps=[("Tell Us Who Is Learning", "Your child's age, or your own goals."),
         ("2 Free Classes", "Your female teacher starts with the most-used daily duas."),
         ("Weekly Plan", "Choose 2, 4 or 5 days a week, or add duas to your Quran classes."),
         ("Use Them Daily", "Say each new dua at the right moment until it becomes a habit.")],
  mini=("Fill your child's day with the remembrance of Allah", "Start the duas course with 2 free classes."),
  wa="Assalamu alaikum, I want the online duas course.",
  faqs=[("What are masnoon duas?", "Masnoon duas are the duas taught by the Prophet Muhammad, peace be upon him, for daily moments such as waking up, eating, leaving home and sleeping. We teach them with the Arabic, the meaning and their hadith reference."),
        ("Which duas should kids learn first?", "Most children start with the duas they use every day: before and after eating, before sleeping and after waking up, and when entering and leaving the home. Your teacher adds new duas as your child grows."),
        ("Are the duas taught with meaning?", "Yes. Every dua is taught with its meaning in English or Urdu, so children and women understand what they are asking Allah for."),
        ("Can duas be added to my child's Quran classes?", "Yes. Many families add a few minutes of duas to each Quran class, or study duas on their own plan."),
        ("Do you teach the morning and evening adhkar?", "Yes. Women and older children learn the morning and evening adhkar from authentic sources, with correct pronunciation and meaning.")],
 ),
 "40-hadith-for-kids": dict(
  cid="hadith40", course_opt="40 Hadith for Kids", nav="40 Hadith for Kids", ill="hadith40",
  title="40 Hadith for Kids Online | Hadith Classes with Meaning",
  desc="Online 40 Hadith classes for kids with a female teacher. Short, authentic hadith with Arabic, meaning and a lesson for daily life, in English or Urdu. 2 free classes.",
  course_name="40 Hadith for Kids Online Classes", crumb="40 Hadith for Kids",
  eyebrow="Words of the Prophet for Little Hearts",
  h1='40 Hadith for Kids: <span class="gold">Online Hadith Classes with Meaning</span>',
  lead="Our 40 Hadith for kids classes help children memorize short, authentic sayings of the Prophet Muhammad, peace be upon him, and live by them. A female teacher explains each hadith in simple English or Urdu, with a story, a lesson for daily life and plenty of practice.",
  points=["Short, authentic hadith", "Arabic, meaning and reference", "A lesson for daily life", "Live 1-on-1 with a female teacher"],
  what_h2="What Is the 40 Hadith for Kids Course?",
  what=("<p>For centuries, Muslim children have grown up memorizing forty hadith. Our course follows that tradition with short, authentic hadith chosen for young learners, many from Imam an-Nawawi's famous Forty Hadith collection.</p>"
        "<p>Children learn the Arabic, its meaning and how to act on it at home and at school. For example, the first hadith teaches that <em>actions are judged by intentions</em> (Sahih al-Bukhari 1), and another that <em>none of you truly believes until he loves for his brother what he loves for himself</em> (Sahih al-Bukhari 13, Sahih Muslim 45).</p>"
        "<p>The course sits alongside our " + A("online-islamic-studies/", "Islamic studies classes") + " and " + A("online-quran-classes-for-kids/", "online Quran classes for kids") + ".</p>"),
  topics_h2="What Kids Learn in Our Hadith Classes",
  topics=[("ح", "Short Authentic Hadith", "Easy hadith from Sahih collections, with their reference."),
          ("ن", "Intention and Sincerity", "Doing good for the sake of Allah, starting with the hadith of intentions."),
          ("أ", "Good Manners (Adab)", "Kindness, honesty, respect for parents and caring for others."),
          ("ق", "Stories Behind the Hadith", "Simple stories that help children remember each lesson."),
          ("ح", "Memorization with Revision", "Memorize each hadith in Arabic with regular revision."),
          ("ع", "Acting on What We Learn", "A small daily action for each hadith, so learning becomes character.")],
  steps_h2="How Our Online Hadith Classes for Kids Work",
  steps=[("Tell Us Your Child's Age", "So the teacher chooses the right hadith and pace."),
         ("2 Free Classes", "Meet your female teacher and learn the first hadith."),
         ("Weekly Plan", "Choose 2, 4 or 5 days a week, or add hadith to Quran classes."),
         ("Live It at Home", "A small daily action helps each hadith become part of your child's character.")],
  mini=("Raise your child on the words of the Prophet", "Start 40 Hadith for kids with 2 free classes."),
  wa="Assalamu alaikum, I want 40 Hadith classes for my child.",
  faqs=[("What is the 40 Hadith for kids course?", "It is a course where children memorize and understand short, authentic hadith, many from Imam an-Nawawi's Forty Hadith, with the Arabic, the meaning in English or Urdu and a lesson for daily life."),
        ("What age is the 40 Hadith course for?", "It suits children from around age 6 to teenagers. Younger children learn shorter hadith with more stories and repetition."),
        ("Are the hadith authentic?", "Yes. We only teach authentic hadith, each with its source, for example Sahih al-Bukhari or Sahih Muslim."),
        ("Will my child memorize the hadith in Arabic?", "Yes. Children memorize each hadith in Arabic, with regular revision, and learn its meaning so they understand what they say."),
        ("Can hadith be combined with Quran classes?", "Yes. Many parents add a few minutes of hadith to each Quran class, or study it on its own plan.")],
 ),
 "quran-classes-for-new-muslims": dict(
  cid="newmuslim", course_opt="Classes for New Muslims", nav="Classes for New Muslims", ill="newmuslim",
  title="Quran Classes for New Muslims | Revert Sisters & Kids",
  desc="Online Quran and Islam classes for new Muslims: revert sisters and their children. Learn salah, Al-Fatiha and Quran reading with a patient female teacher. 2 free classes.",
  course_name="Online Quran and Islam Classes for New Muslims", crumb="Classes for New Muslims",
  eyebrow="Welcome to Islam, Sister",
  h1='Quran Classes for New Muslims: <span class="gold">For Revert Sisters and Their Children</span>',
  lead="Welcome, sister. Our online classes for new Muslims help revert sisters and their children learn the basics of Islam with a patient female teacher: the meaning of the shahada, wudu and salah, Surah Al-Fatiha and how to read the Quran, one gentle step at a time, in English.",
  points=["For revert sisters and children", "Salah from the very first step", "Read the Quran from zero", "Patient female teachers"],
  what_h2="Online Islam Classes for New Muslim Sisters",
  what=("<p>Becoming Muslim is a beautiful beginning, and it can also feel like there is a lot to learn. Our new Muslim classes take away the pressure. You learn privately, one-to-one, with a female teacher who answers every question kindly and never makes you feel rushed.</p>"
        "<p>We start with what you need first: the meaning of the shahada, how to make wudu and how to pray. Then, at your own pace, you learn to read the Quran from the Arabic letters with " + A("noorani-qaida-online/", "Noorani Qaida") + ".</p>"
        "<h3>For your children too</h3><p>Children of revert families learn alongside you, with their own friendly lessons, so the whole family grows in faith together. These classes are for sisters and children only.</p>"),
  topics_h2="What You Learn in Our New Muslim Classes",
  topics=[("ش", "The Shahada and Its Meaning", "<em>La ilaha illallah, Muhammadur Rasulullah</em>, and what it means for your life."),
          ("و", "Wudu and Salah", "How to purify and pray, step by step, with our " + A("online-salah-classes/", "online salah classes") + "."),
          ("ف", "Surah Al-Fatiha and Short Surahs", "The surahs you need for prayer, with meaning and correct pronunciation."),
          ("ق", "Reading the Quran from Zero", "The Arabic letters and sounds, until you can read the Quran yourself."),
          ("ي", "Everyday Islam", "Daily duas, the pillars of Islam and iman, and Islamic manners, explained simply."),
          ("ع", "A Safe Place for Questions", "Ask anything, privately, and get calm answers from the Quran and Sunnah.")],
  steps_h2="How Our New Muslim Classes Work",
  steps=[("Tell Us About You", "Who is learning and what you already know. There is no wrong place to start."),
         ("2 Free Classes", "Meet your female teacher and begin with the shahada and wudu."),
         ("Your Own Pace", "Choose 2, 4 or 5 days a week, at a time that fits your life."),
         ("Grow Step by Step", "Salah first, then Quran reading and everyday Islam.")],
  mini=("You do not have to learn alone", "Start your journey with 2 free classes and a female teacher."),
  wa="Assalamu alaikum, I am a new Muslim and would like to start classes.",
  faqs=[("Are your classes for new Muslims only for women?", "Yes. Our classes are for revert sisters and for children under 18. Every teacher is a woman. We do not teach adult men."),
        ("I don't know any Arabic. Can I still learn?", "Yes. Many new Muslims start with no Arabic at all. Your teacher teaches in English, starting with what you need for salah, and you learn to read the Arabic letters step by step."),
        ("What should a new Muslim learn first?", "Most sisters start with the meaning of the shahada, wudu and how to pray, including Surah Al-Fatiha. After that comes Quran reading and everyday Islam, at your own pace."),
        ("Can my children join the classes too?", "Yes. Children of revert families can learn with their own teacher or alongside you, with lessons suited to their age."),
        ("Are classes private?", "Yes. Every class is one-to-one with a female teacher. For women the camera is optional, classes are never recorded and your details are never shared.")],
 ),
}


def build(slug, P):
    s = TPL
    url = SITE + slug + "/"
    # head
    s = re.sub(r"<title>.*?</title>", f"<title>{P['title']}</title>", s, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'(<meta ' + re.escape(attr) + r' content=")[^"]*(")', lambda m: m.group(1) + P["desc"] + m.group(2), s)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta ' + re.escape(attr) + r' content=")[^"]*(")', lambda m: m.group(1) + P["title"] + m.group(2), s)
    s = s.replace(SITE + "online-islamic-studies/", url)
    # Course schema name/description
    s = s.replace('"name": "Online Islamic Studies Classes"', f'"name": "{P["course_name"]}"')
    s = re.sub(r'("@type": "Course", "name": "[^"]*", "description": ")[^"]*(")', lambda m: m.group(1) + P["desc"] + m.group(2), s, count=1)
    s = re.sub(r'("position": 2, "name": ")[^"]*(")', lambda m: m.group(1) + P["crumb"] + m.group(2), s, count=1)
    # FAQ schema + section are rebuilt below
    faqs = P["faqs"]
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', lambda m: ld(faqs), s, count=1, flags=re.S)
    # hero
    s = re.sub(r'(<section class="page-hero pattern-dark"><div class="container page-hero-grid"><div class="hero-text">).*?(</div><div class="hero-right">)',
               lambda m: m.group(1) + f'<span class="eyebrow">{P["eyebrow"]}</span><h1>{P["h1"]}</h1><p class="hero-lead">{P["lead"]}</p><ul class="hero-points">'
               + "".join(f"<li>{TICK}{x}</li>" for x in P["points"]) + "</ul>" + m.group(2), s, count=1, flags=re.S)
    s = s.replace('value="Islamic studies page (bottom)"', f'value="{P["crumb"]} page (bottom)"').replace('value="Islamic studies page"', f'value="{P["crumb"]} page"')
    s = s.replace("<option selected>Islamic Studies</option>", "<option>Islamic Studies</option>")
    s = s.replace(f"<option>{P['course_opt']}</option>", f"<option selected>{P['course_opt']}</option>")
    # main body sections: replace from first section after hero up to the explore chips section
    a = s.index('<section class="sec bg-cream"><div class="container split">')
    b = s.index('<section class="sec bg-white" style="padding:70px 0">')
    fc = "".join(f'<div class="fcard"><span class="ar-mark">{ar}</span><h3>{h}</h3><p>{p}</p></div>' for ar, h, p in P["topics"])
    st = "".join(f'<li class="step"><div class="step-n"><span>{i+1}</span></div><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(P["steps"]))
    body = (f'<section class="sec bg-cream"><div class="container split"><div class="prose"><span class="eyebrow">About the Course</span><h2>{P["what_h2"]}</h2>{P["what"]}</div>'
            f'<div class="split-media"><div class="illus-wrap">{ILL[P["ill"]](P["cid"][:3] + "x")}</div></div></div></section>'
            '<div class="divider on-white" aria-hidden="true"><span><i></i></span></div>'
            f'<section class="sec bg-white"><div class="container"><div class="section-head"><span class="eyebrow">What You Learn</span><h2>{P["topics_h2"]}</h2><p>Every lesson is live, one-to-one and matched to the student\'s age and level.</p></div><div class="fgrid ">{fc}</div></div></section>'
            '<div class="divider on-cream2" aria-hidden="true"><span><i></i></span></div>'
            f'<section class="sec bg-cream-2"><div class="container"><div class="section-head"><span class="eyebrow">How to Start</span><h2>{P["steps_h2"]}</h2></div><ol class="steps">{st}</ol>'
            f'<div class="mini-cta"><div><h3>{P["mini"][0]}</h3><p>{P["mini"][1]}</p></div><div class="acts"><a href="../free-trial/" class="btn btn-gold">Book 2 Free Classes <svg width="16" height="16"><use href="#i-arrow"/></svg></a>'
            f'<a href="https://wa.me/923345259952" data-wa="{P["wa"]}" data-wa-loc="mini-cta" class="btn btn-wa"><svg width="18" height="18"><use href="#i-wa"/></svg>WhatsApp</a></div></div></div></section>')
    s = s[:a] + body + s[b:]
    # remove old fees block (rebuilt by build_fees.py)
    s = re.sub(r"<!--FEES:course-->.*?<!--/FEES-->", "", s, flags=re.S)
    # CTA whatsapp text
    s = s.replace('data-wa="Assalamu alaikum, I want to join online Islamic studies classes."', f'data-wa="{P["wa"]}"')
    # FAQ section
    s = re.sub(r'<h2>Online Islamic Studies: Frequently Asked Questions</h2>', f'<h2>{P["crumb"]}: Frequently Asked Questions</h2>', s)
    i = s.index('id="faq"'); fa = s.index('<div class="faq-wrap">', i) + len('<div class="faq-wrap">'); fb = s.index('</div></div></section>', fa)
    s = s[:fa] + details(faqs) + s[fb:]
    s = re.sub(r'<a class="chip" href="\.\./' + re.escape(slug) + r'/">[^<]*</a>', "", s)
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(s)


for slug, P in PAGES.items():
    build(slug, P)
    print("built", slug)
