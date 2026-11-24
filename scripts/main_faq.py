#!/usr/bin/env python3
"""Build the main /faq/ help centre to the content brief: quick-facts table, section jump links,
5 sections of direct-answer FAQs (about 50-80 words each, internal links) and one FAQPage schema. Safe to re-run."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from faqlib import details, ld, LD
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "fees.json")))
PLAN = json.load(open(os.path.join(ROOT, "scripts", "blog_posts", "_plan.json")))
TODAY = "2026-11-24"


def L(href, text):
    m = re.match(r"blog/([a-z0-9-]+)/", href)
    extra = f' data-pub="{PLAN[m.group(1)]}" data-pub-mode="unwrap"' if m and PLAN.get(m.group(1), "") > TODAY else ""
    return f'<a href="../{href}" class="in-link"{extra}>{text}</a>'


TRIAL = L("free-trial/", "2 free trial classes")
SECTIONS = [
 ("About Our Classes", "classes", [
  ("Can you really learn Quran online?", "Yes. In a live one-to-one class your teacher hears every letter and corrects you on the spot, just as she would sitting beside you. You read from a shared screen, repeat after the teacher and practise between lessons. Since 2010 we have taught more than 500 children around the world this way. Read " + L("blog/how-to-learn-quran-online/", "how to learn Quran online") + " for the full step-by-step path."),
  ("What courses do you offer?", "We teach " + L("noorani-qaida-online/", "Noorani Qaida") + ", " + L("learn-quran-online-for-beginners/", "Quran reading (Nazra)") + ", " + L("online-tajweed-classes/", "Tajweed") + ", the " + L("online-hifz-program/", "Hifz program") + ", " + L("quran-translation-tafseer-classes/", "Translation and Tafseer") + ", " + L("online-islamic-studies/", "Islamic studies") + ", " + L("online-salah-classes/", "salah") + ", " + L("online-duas-course/", "daily duas") + ", " + L("juz-amma-memorization-online/", "Juz Amma memorisation") + ", " + L("40-hadith-for-kids/", "40 Hadith for kids") + " and " + L("quran-classes-for-new-muslims/", "classes for new Muslims") + ". Every course is live and one to one with a female teacher."),
  ("Are classes one-to-one or in groups?", "Every class is one to one: one student, one teacher, full attention for the whole lesson. There are no group classes. This means the student recites for most of the class and every mistake is corrected straight away, which is why one to one learning is usually faster than a crowded madrasa class. Read our comparison of " + L("blog/online-vs-local-quran-classes/", "online and local Quran classes") + "."),
  ("How long is each class?", "Most classes are 25 to 30 minutes, and Translation and Tafseer classes are 45 to 60 minutes. You choose 2 days a week, 4 days a week or weekend classes. Thirty minutes is long enough for a full lesson and short enough for young children to stay focused. Compare every plan and price on our " + L("fees/", "fees page") + "."),
  ("Which language do teachers use?", "Our teachers explain in English, Urdu or Arabic, whichever the student understands best. The Quran itself is always read in Arabic. Children raised in the UK, USA, Canada or Australia usually prefer English, while many mothers choose Urdu and Arab families often choose Arabic. Read " + L("blog/learn-quran-in-urdu-english-arabic/", "which teaching language is best") + " to decide."),
  ("Which app are classes on?", "Classes run on whichever app you prefer: WhatsApp video, Skype, Google Meet or Zoom. You need a laptop, tablet or phone with a camera, a steady internet connection and a quiet corner. Headphones help a lot, because the teacher needs to hear every letter clearly. The teacher shares the book pages as pictures, so nothing needs to be installed."),
  ("Do I need to know Arabic before starting?", "No. Beginners of any age start with " + L("noorani-qaida-online/", "Noorani Qaida online") + ", which teaches the Arabic letters and sounds step by step until you can read the Quran yourself. You do not need to speak Arabic at all. Our guide to the " + L("blog/arabic-alphabet/", "Arabic alphabet") + " shows what the first weeks look like."),
  ("How long does it take to learn the Quran?", "Most beginners finish the Noorani Qaida in 3 to 6 months and read the Quran slowly within 6 to 12 months of regular classes. Fluent reading with Tajweed usually takes one to two years, and full Hifz 2 to 5 years. Read " + L("blog/how-long-does-it-take-to-learn-quran/", "how long it takes to learn the Quran") + " for realistic timelines at every stage."),
 ]),
 ("Teachers and Safeguarding", "safety", [
  ("Are all your teachers female?", "Yes. Every teacher at Quran Online Tarteel is a woman with 10 or more years of teaching experience, and her recitation and teaching are checked by the academy before she teaches. Female teachers teach both boys and girls under 18 and adult women. Meet our " + L("female-quran-teachers/", "female Quran teachers") + " or read " + L("blog/how-to-choose-a-female-quran-teacher/", "how to choose a female Quran teacher") + "."),
  ("Who can join Quran Online Tarteel?", "Girls and boys under 18, from around age 4 or 5, and women of any age can join. We do not enrol adult men, which keeps every class comfortable for families and sisters. See our " + L("online-quran-classes-for-kids/", "Quran classes for kids") + " and " + L("online-quran-classes-for-women/", "Quran classes for women") + " for how lessons work for each group."),
  ("Can parents watch their child's classes?", "Yes, always. Parents are welcome to sit in on any lesson, and the class link and timing are sent to the parent's phone number, never to the child directly. We ask that children's classes take place in a shared family space, not a closed room. Watching a few lessons also shows you how to help with revision at home."),
  ("Do cameras need to be on?", "Young children keep their camera on so the teacher can see them, help them focus and check the page they are reading. For women, the camera is your choice: many sisters show only the mushaf or share the screen. The focus of every class is the recitation, and your privacy always comes first."),
  ("Are classes recorded?", "No. We never record classes, and we ask parents not to record them either, so your family's privacy stays private. If you want to revise a lesson, the teacher shares the pages and tells you exactly what to practise. Read our " + L("privacy-policy/", "privacy policy") + " for how we handle your details."),
  ("Will my child have the same teacher every time?", "Yes. Your child stays with the same teacher, so she knows exactly where your child is, which letters or rules need work and how your child learns best. If you ever want a different teacher, tell us and we will arrange one within 2 to 3 days, without any fuss."),
  ("How is my personal information used?", "Only to arrange and run your classes. We never sell or share your details with anyone. Your name, WhatsApp number and email are used to book the free trial, send class timings and share updates from the teacher. Read our " + L("privacy-policy/", "privacy policy") + " and " + L("terms/", "terms and conditions") + " for the full details."),
 ]),
 ("Trial, Fees and Payment", "fees", [
  ("Is there a free trial?", "Yes. Every new student gets " + TRIAL + " with a female teacher, with nothing to pay and no card details needed. The trial lets you judge the teacher, the timing and the student's comfort before choosing a plan. Fill in the short form on any page or message us on WhatsApp, and we reply within 24 hours."),
  ("How much are the fees?", "Fees are monthly, per student. Noorani Qaida, Quran reading and Tajweed are $40 (Rs 5,000) for 2 days a week, $60 (Rs 8,000) for 4 days a week and $60 (Rs 8,000) for weekend classes, with 25 to 30 minute classes. Hifz and Tafseer cost more. Every course and currency, including GBP, CAD, AUD, AED and SAR, is on our " + L("fees/", "fees and plans page") + "."),
  ("Why do you take fees in advance?", "Because your teacher keeps your fixed class time for you for the whole month and plans her schedule around it. You only pay after your 2 free trial classes, so you already know the teacher before paying. If you skip the free trial, the fee is paid before the first class. Our refund policy protects you if it does not work out."),
  ("Can I get a refund?", "Yes. If you decide to stop within the first 2 classes of a paid month, we refund 100% of that month's fee. If you stop by the middle of the month, we refund 50% of that month's fee. Just message us on WhatsApp and we will arrange it. The full policy is in our " + L("terms/", "terms and conditions") + "."),
  ("How do I pay in Pakistan?", "You can pay by JazzCash, Easypaisa or bank transfer. The fee is paid monthly, in advance, after your 2 free classes, and we share the payment details on WhatsApp. Fees in Pakistan are shown in rupees on our " + L("online-quran-classes-pakistan/", "online Quran classes in Pakistan") + " page and the " + L("fees/", "fees page") + "."),
  ("How do I pay from abroad?", "Families in the USA, UK, Canada, Australia, the Gulf and elsewhere pay by bank transfer or Western Union, or a relative in Pakistan pays for them by JazzCash, Easypaisa or bank transfer. We share the details on WhatsApp after your free classes. We do not take card or PayPal payments at the moment. Each country page shows fees in your currency."),
  ("Is there a family discount?", "Yes. When more than one child, or a mother and child, learn with us, you get a family discount. Just tell us on WhatsApp how many students will join and which courses, and we will share your family fee. Many families book classes back to back so siblings or mother and child learn at the same time."),
  ("Are books, tests or certificates included?", "Your teacher shares the pages you need as pictures, so you do not need to buy anything to start. If you would like a printed book, she will tell you which one to buy, or you can print our free " + L("downloads/noorani-qaida-quran-online-tarteel.pdf", "Noorani Qaida PDF") + ". We do not run formal tests or certificates, but the teacher keeps you updated on progress."),
 ]),
 ("Timings, Holidays and Ramadan", "timings", [
  ("Which time zones do you teach in?", "Any time zone. We teach families in the " + L("online-quran-classes-usa/", "USA") + ", " + L("online-quran-classes-uk/", "UK") + ", " + L("online-quran-classes-canada/", "Canada") + ", " + L("online-quran-classes-australia/", "Australia") + ", " + L("online-quran-classes-uae/", "UAE") + ", " + L("online-quran-classes-saudi-arabia/", "Saudi Arabia") + ", " + L("online-quran-classes-qatar/", "Qatar") + ", " + L("online-quran-classes-new-zealand/", "New Zealand") + ", " + L("online-quran-classes-ireland/", "Ireland") + ", " + L("online-quran-classes-south-africa/", "South Africa") + " and more. Classes are booked in your local time."),
  ("Can I change my class time?", "Yes, whenever your teacher is free at the new time. Message us on WhatsApp with the time you would like and we will check her schedule for you. If daylight saving changes the time difference, we adjust the teacher's side of the timetable so your class stays at the same local time."),
  ("What happens if the teacher misses a class?", "Whenever a class is missed from our side, because of illness, a power cut or an internet problem at the teacher's end, we always make it up, at the weekend or on any weekday your child is free. You never lose a class that you paid for because of us."),
  ("Are classes held on Eid and public holidays?", "Classes are off on Eid and on Pakistan's government holidays, such as 9th and 10th Muharram and 12 Rabi ul Awwal, and these days are not made up. Your teacher tells you in advance which days are off. Classes continue as normal on other countries' public holidays unless you ask for a break."),
  ("What happens in Ramadan?", "Classes continue in Ramadan, but the timings change around suhoor, school and iftar. We agree new times with you before the month begins. Many families make Ramadan a time for extra Quran goals: see our " + L("blog/ramadan-quran-plan/", "Ramadan Quran plan") + " and " + L("duas-azkar/ramadan-duas/", "Ramadan duas") + "."),
 ]),
 ("Learning at Home", "home", [
  ("How can I help my child practise at home?", "Sit with your child for 10 to 15 minutes a day, start with revision of the last lesson, then practise the teacher's new lesson. Praise effort and keep it gentle. You do not need to read Arabic yourself to help. Read " + L("blog/how-to-teach-quran-to-kids-at-home/", "how to teach Quran to kids at home") + " for 12 practical tips."),
  ("Which surahs should my child memorise first?", "Start with Al-Fatiha, because it is recited in every rakat of salah, then the shortest surahs at the end of the Quran, such as An-Nas, Al-Falaq and Al-Ikhlas. See our list of " + L("blog/short-surahs-for-kids/", "short surahs for kids") + " and our " + L("juz-amma-memorization-online/", "Juz Amma memorisation") + " classes for a tested order."),
  ("Do you have free resources?", "Yes. You can download our free " + L("downloads/noorani-qaida-quran-online-tarteel.pdf", "Noorani Qaida PDF") + ", " + L("downloads/tajweed-rules-pdf-quran-online-tarteel.pdf", "Tajweed rules PDF") + " and " + L("downloads/morning-evening-adhkar-pdf-quran-online-tarteel.pdf", "morning and evening adhkar PDF") + ". Our " + L("duas-azkar/", "duas and azkar library") + " and " + L("blog/", "blog") + " have guides on Tajweed, Hifz, salah, duas and Ramadan."),
  ("What should my child learn alongside the Quran?", "Many families add salah, daily duas and a few hadith, so learning connects to daily life. Short lessons on these can be added at the end of Quran classes. See our " + L("online-salah-classes/", "online salah classes") + ", " + L("online-duas-course/", "daily duas course") + ", " + L("40-hadith-for-kids/", "40 Hadith for kids") + " and " + L("blog/islamic-stories-for-kids/", "Islamic stories for kids") + "."),
 ]),
]

FACTS = [("Teachers", "Female teachers only, 10+ years of experience"), ("Students", "Girls and boys under 18, and women"),
         ("Format", "Live, one to one, 25 to 30 minutes (Tafseer 45 to 60)"), ("Languages", "English, Urdu or Arabic"),
         ("Plans", "2 days a week, 4 days a week or weekends"), ("Free trial", "2 free classes, no card needed"),
         ("Payment", "Monthly, in advance, after the free trial"), ("Refunds", "100% within the first 2 classes of a paid month, 50% by mid-month"),
         ("Time zones", "Classes booked in your local time")]

p = os.path.join(ROOT, "faq", "index.html")
s = open(p).read()
bgs = ["bg-cream", "bg-white", "bg-cream", "bg-white", "bg-cream"]
facts = ("<section class=\"sec bg-white\" id=\"quick-facts\"><div class=\"container\"><div class=\"section-head\"><span class=\"eyebrow\">At a Glance</span>"
         "<h2>Quran Online Tarteel: Quick Facts</h2><p>The short answers families ask most before booking. Jump to a section below for the details.</p></div>"
         "<div class=\"table-wrap\"><div class=\"table-scroll\"><table><thead><tr><th>Question</th><th>Answer</th></tr></thead><tbody>"
         + "".join(f'<tr><td data-label="Question"><span class="lvl">{a}</span></td><td data-label="Answer">{b}</td></tr>' for a, b in FACTS)
         + "</tbody></table></div></div><div class=\"faq-jump\">"
         + "".join(f'<a class="chip" href="#faq-{sid}">{title}</a>' for title, sid, _ in SECTIONS)
         + "</div></div></section>")
html = facts
for i, (title, sid, items) in enumerate(SECTIONS):
    html += f'<div class="divider {"on-white" if bgs[i]=="bg-white" else ""}" aria-hidden="true"><span><i></i></span></div>'
    html += (f'<section class="sec {bgs[i]}" id="faq{i}"><div class="container"><div class="section-head" id="faq-{sid}"><span class="eyebrow">FAQ</span>'
             f'<h2>{title}</h2></div><div class="faq-wrap">{details(items, open_first=(i==0))}</div></div></section>')
a = s.index('<section class="sec bg-white" id="quick-facts">') if 'id="quick-facts"' in s else s.index('<section class="sec bg-cream" id="faq0">')
b = s.index('<section class="cta-sec dark pattern-dark" id="enrol">')
if "<!--BLOGLATEST-->" in s[a:b]:
    b = s.index("<!--BLOGLATEST-->", a)
s = s[:a] + html + s[b:]
allitems = [it for _, _, items in SECTIONS for it in items]
s = LD.sub(lambda m: ld(allitems), s, count=1)
s = re.sub(r'<p class="hero-lead">.*?</p>', '<p class="hero-lead">Clear answers to everything families ask before joining Quran Online Tarteel: how online classes work, our female teachers and safeguarding, the free trial, fees paid in advance, refunds, timings and learning at home.</p>', s, count=1, flags=re.S)
for prop in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
    s = re.sub(r'(<meta %s content=")[^"]*' % re.escape(prop), lambda m: m.group(1) + "Online Quran classes FAQ: female teachers, safeguarding, the 2 free trial classes, fees paid monthly in advance, refunds, timings and Ramadan.", s, count=1)
assert "—" not in s
open(p, "w").write(s)
print(len(allitems), "questions")
for q, a_ in allitems:
    w = len(re.sub("<[^>]+>", "", a_).split())
    if not 45 <= w <= 85:
        print("  words", w, q)
