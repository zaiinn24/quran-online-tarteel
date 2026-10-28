#!/usr/bin/env python3
"""Replace the copy-paste FAQs on country pages with country-specific ones. Safe to re-run."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from faqlib import read_items, replace_section_items, set_ld
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = ("Can my son learn with a female Quran teacher?", "What does my child need", "What do we need for online",
        "Are online Quran classes as good as", "Is an online Quran teacher better than a home tutor?",
        "How do I book the 2 free online Quran classes?", "How do I book free online Quran classes in the UK?",
        "How do I book the free online Quran classes in")
FEES = '<a href="../fees/" class="in-link">fees and plans</a>'
TRIAL = '<a href="../free-trial/" class="in-link">2 free classes</a>'
FAQ = '<a href="../faq/" class="in-link">FAQ page</a>'
PAY_ABROAD = ("Families abroad usually pay by bank transfer or Western Union, or a relative in Pakistan pays for them by JazzCash, Easypaisa or bank transfer. "
              "The fee is paid monthly, in advance, and we share the payment details on WhatsApp after your " + TRIAL + ". We do not take card or PayPal payments at the moment.")
NEW = {
 "online-quran-classes-usa": [
  ("How do I pay for online Quran classes from the USA?", PAY_ABROAD + " See " + FEES + " for the dollar fees."),
  ("Can classes fit around school and weekends in the USA?", "Yes. Most American families choose weekday evenings after school or weekend mornings, in Eastern, Central, Mountain or Pacific time. Tell us the times that suit your family in the form and we will match you with a teacher who is free then."),
  ("What happens to my class time when US clocks change?", "Daylight saving moves the time difference with Pakistan by one hour. Message us on WhatsApp before the clocks change and we will confirm your class time with your teacher. If the same local time is not free, we offer the nearest time she is available."),
  ("Can my child learn in English?", "Yes. Our teachers teach in English and Urdu, so children who grew up in America can follow every explanation easily. The Quran itself is always read in Arabic."),
 ],
 "online-quran-classes-uk": [
  ("How do I pay for online Quran classes from the UK?", PAY_ABROAD + " See " + FEES + " for the fees in pounds."),
  ("Do classes continue in UK school holidays?", "Yes. Classes carry on through half-term and the summer holidays, which is a lovely time for children to make extra progress. Classes are only off on Eid and on Pakistan's public holidays, and those days are not made up. See our " + FAQ + " for the full holiday policy."),
  ("What happens to my class time when UK clocks change?", "When the UK moves between GMT and BST, the time difference with Pakistan changes by one hour. Message us on WhatsApp before the clocks change and we will confirm your class time with your teacher, or offer the nearest time she is free."),
  ("Can my child be taught in English?", "Yes. Our teachers explain in English or Urdu, whichever your child is more comfortable with, while the Quran is always read in Arabic."),
 ],
 "online-quran-classes-canada": [
  ("How do I pay for online Quran classes from Canada?", PAY_ABROAD + " See " + FEES + " for the fees in Canadian dollars."),
  ("Are weekend Quran classes available in Canada?", "Yes. Saturday and Sunday mornings are popular with Canadian families, and weekday evenings after school work well too. Tell us your preferred times and province in the form and we will find a teacher who is free then."),
  ("What happens to my class time when Canadian clocks change?", "Daylight saving changes the time difference with Pakistan by one hour. Message us on WhatsApp before the clocks change and we will confirm your class time with your teacher, or offer the nearest time she is free."),
  ("Can my child learn in English or French?", "Our teachers teach in English and Urdu. Classes are not taught in French, but most children in Canada follow English explanations easily, and the Quran is always read in Arabic."),
 ],
 "online-quran-classes-australia": [
  ("How do I pay for online Quran classes from Australia?", PAY_ABROAD + " See " + FEES + " for the fees in Australian dollars."),
  ("What are the easiest class times to book in Australia?", "Afternoons and evenings in Australia fall during the day in Pakistan, so these are the easiest times to book, including after school. Early mornings in Australia are night time in Pakistan, so ask us first if you need one."),
  ("What happens to my class time when Australian clocks change?", "When daylight saving starts or ends in your state, the time difference with Pakistan changes by one hour. Message us on WhatsApp beforehand and we will confirm your class time with your teacher, or offer the nearest time she is free."),
  ("Can my child learn in English?", "Yes. Our teachers explain in English or Urdu, so children raised in Australia understand every lesson. The Quran is always read in Arabic."),
 ],
 "online-quran-classes-uae": [
  ("How do I pay for online Quran classes from the UAE?", PAY_ABROAD + " See " + FEES + " for the fees in dirhams."),
  ("Is the time difference with Pakistan a problem?", "Not at all. Pakistan is only one hour ahead of the UAE, so almost any time of day works, including straight after school and on Saturday and Sunday."),
  ("Do your teachers teach in Urdu and English?", "Yes. Many families in Dubai, Abu Dhabi and Sharjah choose Urdu, others prefer English. Your teacher explains in whichever your child understands best, and the Quran is always read in Arabic."),
  ("Are classes held during Ramadan?", "Yes. In Ramadan the class timings change, and we agree new times with you before the month begins. Classes are off on Eid and on Pakistan's public holidays."),
 ],
 "online-quran-classes-pakistan": [
  ("How do I pay the fee in Pakistan?", "You can pay by JazzCash, Easypaisa or bank transfer. The fee is paid monthly, in advance, and we share the details on WhatsApp after your " + TRIAL + ". See " + FEES + " for every course in rupees."),
  ("What happens if there is load-shedding or an internet problem?", "If load-shedding or an internet problem stops a class at the teacher's end, we always make the class up, at the weekend or on any weekday your child is free. If the problem is at your end, please message your teacher as early as you can. Those classes are not automatically made up, but she will try her best to fit one in."),
  ("Are classes taught in Urdu?", "Yes. Our teachers explain in Urdu or English, whichever your child is more comfortable with. The Quran is always read in Arabic."),
  ("Are classes held on public holidays and in Ramadan?", "Classes are off on Eid and on Pakistan's government holidays, such as 9th and 10th Muharram and 12 Rabi ul Awwal, and these days are not made up. In Ramadan the class timings change, and we agree new times with you."),
 ],
}
for page, new in NEW.items():
    p = os.path.join(ROOT, page, "index.html")
    s = open(p).read()
    items = [(q, a) for q, a in read_items(s) if not q.startswith(DROP) and q not in [n for n, _ in new]]
    items += new
    s = replace_section_items(s, items)
    s = set_ld(s, items)
    if page in ("online-quran-classes-pakistan", "online-quran-classes-uae"):
        where = "Pakistan" if "pakistan" in page else "the UAE"
        s = s.replace("<li><span class=\"tick\"><svg", "<li><span class=\"tick\"><svg")  # noop anchor
        s = s.replace("Times for US, UK, Canada, Australia and more", f"Class times that suit families in {where}")
    open(p, "w").write(s)
    print(page, len(items))
