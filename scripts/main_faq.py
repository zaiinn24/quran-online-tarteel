#!/usr/bin/env python3
"""Build the main /faq/ help centre (4 sections + one FAQPage schema). Safe to re-run."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from faqlib import details, ld, LD
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "fees.json")))
L = lambda href, text: f'<a href="../{href}" class="in-link">{text}</a>'
SECTIONS = [
 ("About Our Classes", [
  ("Can you really learn Quran online?", "Yes. In a live one-to-one class your teacher hears every letter and corrects you on the spot, just as she would sitting beside you. Students read from a shared screen, repeat after the teacher and practise between lessons. Since 2010, we have taught more than 500 children around the world this way."),
  ("What courses do you offer?", "We teach " + L("noorani-qaida-online/", "Noorani Qaida") + ", " + L("learn-quran-online-for-beginners/", "Quran reading (Nazra)") + ", " + L("online-tajweed-classes/", "Tajweed") + ", " + L("online-hifz-program/", "Hifz") + ", " + L("quran-translation-tafseer-classes/", "Translation and Tafseer") + " and " + L("online-islamic-studies/", "Islamic Studies") + ", plus Juz Amma memorisation, Salah lessons, a daily Duas course, 40 Hadith for kids and classes for new Muslims. We do not teach Arabic language, Ijazah or Qirat courses."),
  ("Are classes one-to-one or in groups?", "Every class is one-to-one: one student, one teacher, full attention. There are no group classes."),
  ("How long is each class?", "Classes are 25 to 30 minutes. Translation and Tafseer classes are 45 to 60 minutes. You choose 2 or 4 days a week, or weekend classes. Young children do well with this length too."),
  ("Which language do teachers use?", "Our teachers explain in Urdu and English, whichever the student understands best. The Quran itself is always read in Arabic."),
  ("Which app are classes on?", "Whichever you prefer: WhatsApp video, Skype, Google Meet or Zoom. A laptop, tablet or phone with a camera, a steady internet connection and a quiet corner are all you need. A headset helps."),
  ("Do I need to know Arabic before starting?", "No. Beginners of any age start with Noorani Qaida, which teaches the Arabic letters and sounds step by step until you can read the Quran yourself."),
 ]),
 ("Teachers and Safeguarding", [
  ("Are all your teachers female?", "Yes, every teacher at Quran Online Tarteel is a woman, with 10 or more years of teaching experience. Each teacher's recitation and teaching is checked by the academy before she teaches. Read more about our " + L("female-quran-teachers/", "female Quran teachers") + "."),
  ("Who can join Quran Online Tarteel?", "Girls and boys under 18, from around age 4 or 5, and women of any age. We do not enrol adult men. See " + L("online-quran-classes-for-kids/", "Quran classes for kids") + " and " + L("online-quran-classes-for-women/", "Quran classes for women") + "."),
  ("Can parents watch their child's classes?", "Yes, always. Parents are welcome to sit in on any lesson, and the class link and timing are sent to the parent's phone number, never to the child directly."),
  ("Do cameras need to be on?", "Young children keep their camera on so the teacher can see them and keep them focused. For women, the camera is your choice. Teachers keep their own camera off during lessons, but if you would like to confirm your teacher is a woman, she will turn her camera on once."),
  ("Are classes recorded?", "No. We never record classes, and parents are asked not to record them either. Your family's privacy stays private."),
  ("Will my child have the same teacher every time?", "Yes. Your child stays with the same teacher, so she knows exactly where they are. If you ever want a different teacher, just tell us and we will arrange one within 2 to 3 days."),
  ("How is my personal information used?", "Only to arrange and run your classes. We never sell or share your details. Read our " + L("privacy-policy/", "privacy policy") + "."),
 ]),
 ("Trial, Fees and Payment", [
  ("Is there a free trial?", "Yes. Every new student gets 2 free classes with a female teacher, with nothing to pay. " + L("free-trial/", "Book your 2 free classes") + "."),
  ("How much are the fees?", "Fees are monthly, per student. Noorani Qaida, Quran reading and Tajweed are $40 (Rs 5,000) for 2 days a week, $60 (Rs 8,000) for 4 days a week and $60 (Rs 8,000) for weekend classes, with 25–30 minute classes. Every course and currency is on our " + L("fees/", "fees and plans page") + "."),
  ("How do I pay in Pakistan?", "By JazzCash, Easypaisa or bank transfer. The fee is paid monthly, in advance."),
  ("How do I pay from abroad?", "Families in the USA, UK, Canada, Australia, the UAE and elsewhere pay by bank transfer or Western Union, or a relative in Pakistan pays for them by JazzCash, Easypaisa or bank transfer. We share the payment details on WhatsApp after your free classes. We do not take card or PayPal payments at the moment."),
  ("Is there a family discount?", "Yes. When more than one child, or a mother and child, learn with us, you get a special family discount. Just ask us on WhatsApp."),
  ("Can I get a refund?", "Yes. If you have paid but decide not to start, you get a full refund. If you stop in the middle of a month, we refund 50% of that month's fee."),
  ("Are books, tests or certificates included?", "Your teacher shares the pages you need as pictures, so you do not need to buy anything to start. If you would like a printed book, she will tell you which one. We do not run formal tests, reports or certificates. Instead, your teacher keeps you updated on WhatsApp about how the student is doing."),
 ]),
 ("Missed Classes, Holidays and Timings", [
  ("What happens if the teacher misses a class?", "Our teachers are human too, and sometimes life happens: an illness, load-shedding or an internet problem at the teacher's end. Whenever a class is missed from our side, we always make it up, at the weekend or on any weekday your child is free. Not a single lesson is lost, and we are truly grateful for your patience and understanding."),
  ("What if my child misses a class?", "Please let your teacher know as early as you can. Classes missed by the student are not automatically made up, but if your teacher has a free slot she will try her best to fit one in."),
  ("Can I change my class time?", "Yes, whenever your teacher is free at the new time. Message us on WhatsApp and we will check her schedule for you."),
  ("Are classes held on Eid and public holidays?", "Classes are off on Eid and on Pakistan's government holidays, such as 9th and 10th Muharram and 12 Rabi ul Awwal. These days are not made up."),
  ("What happens in Ramadan?", "Classes continue in Ramadan, but the timings change. We agree new times with you before the month begins."),
  ("Which time zones do you teach in?", "Any time zone. We teach families in the " + L("online-quran-classes-usa/", "USA") + ", " + L("online-quran-classes-uk/", "UK") + ", " + L("online-quran-classes-canada/", "Canada") + ", " + L("online-quran-classes-australia/", "Australia") + ", the " + L("online-quran-classes-uae/", "UAE") + ", " + L("online-quran-classes-pakistan/", "Pakistan") + " and beyond."),
 ]),
]
p = os.path.join(ROOT, "faq", "index.html")
s = open(p).read()
bgs = ["bg-cream", "bg-white", "bg-cream", "bg-white"]
html = ""
for i, (title, items) in enumerate(SECTIONS):
    if i:
        html += f'<div class="divider {"on-white" if bgs[i]=="bg-white" else ""}" aria-hidden="true"><span><i></i></span></div>'
    html += (f'<section class="sec {bgs[i]}" id="faq{i}"><div class="container"><div class="section-head"><span class="eyebrow">FAQ</span>'
             f'<h2>{title}</h2></div><div class="faq-wrap">{details(items, open_first=(i==0))}</div></div></section>')
a = s.index('<section class="sec bg-cream" id="faq0">')
b = s.index('<section class="cta-sec dark pattern-dark" id="enrol">')
s = s[:a] + html + s[b:]
allitems = [it for _, items in SECTIONS for it in items]
s = LD.sub(lambda m: ld(allitems), s, count=1)
s = s.replace("Everything families ask before joining Quran Online Tarteel: how online classes work, who teaches, how children are kept safe, the free trial, fees and timings.",
              "Everything families ask before joining Quran Online Tarteel: how online classes work, who teaches, how children are kept safe, the free trial, fees, payment, missed classes and holidays.")
open(p, "w").write(s)
print(len(allitems), "questions")
