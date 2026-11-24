#!/usr/bin/env python3
"""Bring the service pages up to the content brief: every FAQ answer 60-80 words with internal links,
9-10 FAQs per page, and a table on pages that had none. Idempotent: existing answers are matched by question
and the extra text is only appended once. Run after build_fees.py (which owns the 'How much...' answers)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from faqlib import read_items, replace_section_items, set_ld, strip

PLAN = json.load(open(os.path.join(ROOT, "scripts", "blog_posts", "_plan.json")))
TODAY = "2026-11-24"


def L(path, text):
    """internal link from a depth-1 page; links to scheduled blog posts are unwrapped by the middleware until live"""
    m = re.match(r"blog/([a-z0-9-]+)/", path)
    extra = ""
    if m and PLAN.get(m.group(1), "") > TODAY:
        extra = f' data-pub="{PLAN[m.group(1)]}" data-pub-mode="unwrap"'
    return f'<a href="../{path}" class="in-link"{extra}>{text}</a>'


TRIAL = L("free-trial/", "2 free trial classes")
FEES = L("fees/", "fees page")

# question -> text appended to the existing answer
ADD = {
 "online-quran-classes-for-kids": {
  "What is the best age to start online Quran classes for kids?": f" Younger children can begin by listening to short surahs and learning daily duas. Read our guide on {L('blog/how-to-teach-quran-to-kids-at-home/', 'how to teach Quran to kids at home')} for what to do before classes start.",
  "Do boys also learn with female teachers?": " Boys progress just as well with a female teacher. The same safeguarding rules apply to every child: the class link goes to the parent, and parents can sit in on any lesson.",
  "Can I watch my child's Quran class?": f" Watching a few lessons also shows you how to help with revision at home. Our {L('faq/', 'FAQ and safeguarding page')} explains every rule we follow for children's classes.",
  "How long is each class for kids?": " Thirty minutes is long enough for a full lesson and short enough for young children to stay focused. Hifz students sometimes book back-to-back classes on revision days, and older children can move to longer classes when they are ready.",
  "How many days a week should my child study?": f" Children in the Noorani Qaida stage remember far more with frequent short lessons than with one long weekly class. Compare the 2 day, 4 day and weekend plans on our {FEES}.",
  "What does my child need for online Quran classes?": " Headphones help a lot, because the teacher needs to hear every letter clearly. Classes work on WhatsApp video, Skype, Google Meet or Zoom, whichever your family prefers, and the teacher shares the book pages as pictures.",
  "Are your online Quran classes for kids free?": f" The trial lets you judge the teacher, the timing and your child's comfort before choosing a plan. After the trial, fees are paid monthly in advance. See the full list of prices on our {FEES}.",
 },
 "online-quran-classes-for-women": {
  "Are your online Quran classes only for women?": f" Girls and boys under 18 are taught too, but adult men are not enrolled. That keeps every class comfortable for sisters. Meet our {L('female-quran-teachers/', 'female Quran teachers')} to see who will teach you.",
  "I am an adult and cannot read Arabic. Can I still learn?": f" Many sisters start from zero in their thirties, forties or later. Read our guide to {L('blog/learn-quran-as-an-adult-woman/', 'learning Quran as an adult woman')} for a simple 6 month plan.",
  "Can I keep my camera off during class?": "",
  "What times are classes available?": f" Mothers often choose school hours, early mornings or late evenings after the children sleep. Classes run in every time zone, and our country pages, such as {L('online-quran-classes-uk/', 'online Quran classes in the UK')}, list typical slots.",
  "Can I learn Hifz as a working woman?": f" A realistic daily lesson of a few lines, revised in your salah, adds up over time. Read {L('blog/how-to-memorize-quran/', 'how to memorize the Quran')} for a timetable that fits a busy day.",
  "Can my daughter and I study together?": f" Many mothers book their class straight after their daughter's, or sit in on it, so the whole family learns the same lessons. Families with more than one student also get a family discount, explained on our {FEES}.",
 },
 "female-quran-teachers": {
  "Are all your Quran teachers female?": f" They teach children under 18, both boys and girls, and adult women. Read our guide on {L('blog/how-to-choose-a-female-quran-teacher/', 'how to choose a female Quran teacher online')} to know what to look for.",
  "How are your female Quran teachers checked?": " Every teacher has 10 or more years of teaching experience, and her recitation and teaching are checked by the academy before she teaches. We also listen to feedback from families after the trial and throughout the year.",
  "Will I have the same teacher every class?": " Staying with one teacher means she knows exactly which letters, rules or pages you find hard. If you ever want a different teacher, we arrange one within 2 to 3 days.",
  "Can I choose a teacher who speaks Urdu or Arabic too?": " Tell us your preferred language when you book. Our teachers explain in English, Urdu or Arabic, and the Quran is always read in Arabic. Children raised abroad usually prefer English, while many mothers choose Urdu.",
  "Can I meet the teacher before paying?": f" The {TRIAL} are with the teacher who will continue with you, so you can judge her patience, corrections and timing first. After the trial, fees are paid monthly in advance.",
 },
 "noorani-qaida-online": {
  "How long does it take to finish Noorani Qaida online?": f" Adults are often faster, around 2 to 4 months. Read {L('blog/how-long-does-it-take-to-learn-quran/', 'how long it takes to learn the Quran')} for realistic timelines at every stage.",
  "What age can a child start Noorani Qaida?": f" Before that, children can learn the letter sounds by listening. Our guide to the {L('blog/arabic-alphabet/', 'Arabic alphabet')} has a simple 4 week plan parents can use at home.",
  "Do I need to buy a Noorani Qaida book?": f" You can also download our free {L('downloads/noorani-qaida-quran-online-tarteel.pdf', 'Noorani Qaida PDF')} and print it, and read our {L('resources/noorani-qaida-guide/', 'Noorani Qaida guide')} to see what each lesson teaches.",
  "Can adults learn Noorani Qaida online?": f" Many women, new Muslims and parents learn the Qaida as adults. Adults usually move faster than children because they understand explanations quickly. See our {L('online-quran-classes-for-women/', 'Quran classes for women')} and {L('quran-classes-for-new-muslims/', 'classes for new Muslims')}.",
  "What comes after Noorani Qaida?": f" After the Qaida, students move to {L('learn-quran-online-for-beginners/', 'Quran reading (Nazra)')}, usually starting with the short surahs of Juz Amma, then add {L('online-tajweed-classes/', 'Tajweed')} once reading is steady.",
 },
 "learn-quran-online-for-beginners": {
  "How long does it take to learn to read the Quran online?": f" Children usually need longer than adults. Read {L('blog/how-to-learn-quran-online/', 'how to learn Quran online')} for the full order of stages and what each one involves.",
  "Is this course for adults or kids?": f" Children start through our {L('online-quran-classes-for-kids/', 'online Quran classes for kids')}, and sisters through our {L('online-quran-classes-for-women/', 'Quran classes for women')}. The teacher places every student at the right stage after the free trial.",
  "What is the difference between Nazra and Tajweed?": f" Most students learn basic Tajweed alongside reading, then study it properly later. Read {L('blog/what-is-tajweed/', 'what Tajweed is')} for a simple explanation.",
  "Which Mushaf do you use?": f" Students can also use a colour-coded Tajweed mushaf, which marks the rules in colour. Read our guide to the {L('blog/colour-coded-tajweed-quran/', 'colour-coded Tajweed Quran')} to see whether it suits you.",
  "Can I learn to read the Quran online for free?": f" Our {TRIAL} are completely free, with no payment details needed. After that, fees are paid monthly in advance. You can also practise with our free {L('downloads/noorani-qaida-quran-online-tarteel.pdf', 'Noorani Qaida PDF')}.",
 },
 "online-tajweed-classes": {
  "How long does it take to learn Tajweed online?": f" Applying the rules confidently across the whole Quran usually takes about a year of practice. Read {L('blog/what-is-tajweed/', 'what Tajweed is and why it matters')} before you start.",
  "Can I learn Tajweed online without knowing Arabic?": f" You only need to read Arabic letters, not speak Arabic. If you cannot read yet, start with {L('noorani-qaida-online/', 'Noorani Qaida online')}. Our teachers explain the rules in English, Urdu or Arabic.",
  "Are your Tajweed classes for kids too?": f" Children learn by copying the correct sound, so Tajweed is built into their reading lessons from the start. See our {L('online-quran-classes-for-kids/', 'online Quran classes for kids')} for how lessons are structured.",
  "Is a colour-coded Tajweed Quran helpful?": f" The colours show where a rule applies, but a teacher shows how it should sound. Read our guide to the {L('blog/colour-coded-tajweed-quran/', 'colour-coded Tajweed Quran')} and download our free {L('downloads/tajweed-rules-pdf-quran-online-tarteel.pdf', 'Tajweed rules PDF')}.",
  "Do you teach makharij in detail?": f" Correct makharij come before every other rule, because a letter from the wrong place becomes a different letter. Read our guide to {L('blog/makharij-al-huroof/', 'makharij al-huroof')} for the 17 points of articulation.",
 },
 "online-hifz-program": {
  "How long does it take to memorise the whole Quran online?": f" Part-time students alongside school often take 3 to 5 years. Read {L('blog/how-to-memorize-quran/', 'how to memorize the Quran')} for sample timetables for children and adults.",
  "What is the best age to start Hifz?": f" Reading fluently with basic Tajweed matters more than age. Read {L('blog/what-is-hifz/', 'what Hifz is and the best age to start')} for the signs that a child is ready.",
  "Can I do Hifz part time while at school or work?": " Most of our Hifz students memorise part time. A small daily lesson after Fajr, revision in the evening and two to four classes a week with the teacher add up steadily over the years.",
  "How do you make sure students do not forget?": " Every class includes sabaq (new lesson), sabqi (recent revision) and manzil (older revision), and the teacher keeps a record of weak pages. Parents get regular updates on WhatsApp so revision continues at home.",
  "Is there a dua for memorising the Quran?": f" Many students also say Rabbi zidni ilma, My Lord, increase me in knowledge (Quran 20:114). See our guide to {L('blog/dua-for-success-protection-knowledge/', 'duas for success, protection and knowledge')}.",
 },
 "quran-translation-tafseer-classes": {
  "Which Tafseer do you use in class?": f" Teachers draw on trusted classical and modern works and keep explanations simple. Read {L('blog/tafseer-for-beginners/', 'Tafseer for beginners')} for an overview of well-known tafseer books.",
  "Do I need to know Arabic for Tafseer classes?": f" You should be able to read the Quran, but you do not need to speak Arabic. Word by word translation is taught in English, Urdu or Arabic. See our comparison of the {L('blog/best-english-translation-of-quran/', 'best English translations of the Quran')}.",
  "Are Tafseer classes available for kids?": f" For younger children, we teach the meaning of short surahs and stories of the Prophets in a simpler way, through {L('online-islamic-studies/', 'Islamic studies online')} and our {L('blog/islamic-stories-for-kids/', 'Islamic stories for kids')}.",
  "How long does the Tafseer course take?": " Most students begin with Al-Fatiha and Juz Amma, the surahs they recite most in salah, then continue surah by surah at a pace that suits them. Classes are usually 45 to 60 minutes.",
  "Can I learn translation and Tajweed together?": f" Many sisters spend part of each class on recitation and part on meaning. Our {L('online-tajweed-classes/', 'online Tajweed classes')} can be combined with translation in one plan.",
 },
 "online-islamic-studies": {
  "Can Islamic studies be combined with Quran classes?": f" Many families add a few minutes of Islamic studies at the end of each Quran class. Children can also join {L('40-hadith-for-kids/', '40 Hadith for kids')} or the {L('online-duas-course/', 'daily duas course')}.",
  "What age are your Islamic studies classes for?": f" Lessons are adjusted for each age: stories and simple manners for young children, and more detail on salah, belief and character for older students. Try our {L('blog/islamic-stories-for-kids/', 'Islamic stories for kids')} at home too.",
  "Do you teach how to pray salah?": f" For a focused course, see our {L('online-salah-classes/', 'online salah classes')}, and read {L('blog/how-to-pray-salah-step-by-step/', 'how to pray salah step by step')} and {L('blog/how-to-perform-wudu/', 'how to perform wudu')}.",
  "Are classes taught in English?": " Our teachers explain in English, Urdu or Arabic, whichever the student understands best. Children raised in the UK, USA, Canada and Australia usually prefer English, while many mothers choose Urdu.",
  "Which school of thought do you follow?": " Where practices differ between schools, the teacher follows what the family practises and explains the differences respectfully. Parents can tell us their preference when they book the free trial.",
 },
 "online-duas-course": {
  "What are masnoon duas?": f" Browse our free {L('duas-azkar/', 'duas and azkar library')} for the Arabic, transliteration and meaning of each one.",
  "Which duas should kids learn first?": f" See our {L('duas-azkar/daily-duas-for-kids/', 'daily duas for kids')} with meaning in English and Urdu, and read {L('blog/what-is-dua/', 'what dua is and how to make it')}.",
  "Are the duas taught with meaning?": " Understanding the meaning turns memorised words into a real conversation with Allah. Teachers explain each dua in English, Urdu or Arabic and link it to the right moment in the day.",
  "Can duas be added to my child's Quran classes?": f" Many families spend the last few minutes of each Quran class on one dua. See our {L('online-quran-classes-for-kids/', 'online Quran classes for kids')} for how lessons are planned.",
  "Do you teach the morning and evening adhkar?": f" Read them on our {L('duas-azkar/morning-evening-azkar/', 'morning and evening azkar')} page or download the free {L('downloads/morning-evening-adhkar-pdf-quran-online-tarteel.pdf', 'morning and evening adhkar PDF')}.",
 },
 "online-salah-classes": {
  "What age should a child start learning salah?": f" Read {L('blog/how-to-pray-salah-step-by-step/', 'how to pray salah step by step')} for tips on teaching children gently, one prayer at a time.",
  "Do I need to know Arabic to learn salah?": f" New learners start with Al-Fatiha, the words of ruku and sujood and the tashahhud. Our {L('blog/how-to-perform-wudu/', 'wudu guide')} covers the steps before prayer.",
  "Which school of thought do you follow for salah?": f" The teacher follows what your family practises, and explains small differences respectfully. Our guide to {L('blog/sunnah-prayers/', 'sunnah prayers')} shows where counts differ between schools.",
  "Are salah classes available for new Muslim sisters?": f" See our {L('quran-classes-for-new-muslims/', 'Quran classes for new Muslims')}, which combine salah, short surahs and the basics of reading at a gentle pace.",
 },
 "juz-amma-memorization-online": {
  "How many surahs are in Juz Amma?": f" Start with the shortest ones. Our list of {L('blog/short-surahs-for-kids/', 'short surahs for kids')} gives the best order for the first 14.",
  "Does my child need to read the Quran before memorizing Juz Amma?": f" Children who are still in the {L('noorani-qaida-online/', 'Noorani Qaida')} can memorise by listening and repeating, while reading lessons continue alongside.",
  "What age can my child start Juz Amma memorization?": f" Read {L('blog/what-is-hifz/', 'what Hifz is and the best age to start')} if you are thinking about full memorisation later.",
  "Can adults and women memorize Juz Amma online?": f" Many sisters memorise Juz Amma to recite more variety in salah. See our {L('online-quran-classes-for-women/', 'Quran classes for women')} and the {L('online-hifz-program/', 'online Hifz program')}.",
 },
 "40-hadith-for-kids": {
  "How much do 40 Hadith classes cost?": "",
  "What is the 40 Hadith for kids course?": f" Each hadith is linked to a real-life situation, like kindness, honesty or intention. Pair it with our {L('blog/islamic-stories-for-kids/', 'Islamic stories for kids')} at bedtime.",
  "What age is the 40 Hadith course for?": " Younger children learn shorter hadith with simple stories, while older children learn longer ones with more explanation. The teacher adjusts the pace to each child after the free trial.",
  "Are the hadith authentic?": " Imam an-Nawawi chose hadith that scholars have accepted, and each lesson gives the source, such as Sahih al-Bukhari or Sahih Muslim, so families can look it up.",
  "Will my child memorize the hadith in Arabic?": " Children usually memorise the short Arabic text with its meaning, and longer hadith by their key words. The goal is understanding and practice, not only memorisation.",
  "Can hadith be combined with Quran classes?": f" Many families add one hadith at the end of each Quran class. See our {L('online-islamic-studies/', 'Islamic studies online')} and {L('online-quran-classes-for-kids/', 'online Quran classes for kids')}.",
 },
 "quran-classes-for-new-muslims": {
  "I don't know any Arabic. Can I still learn?": " Our teachers explain everything in English, Urdu or Arabic, and the very first lessons are only letters and sounds. Many reverts are surprised how quickly the letters become familiar with a patient teacher and short daily practice.",
  "Are your classes for new Muslims only for women?": f" Revert sisters and their children, both girls and boys under 18, are welcome. Meet our {L('female-quran-teachers/', 'female Quran teachers')}.",
  "What should a new Muslim learn first?": f" Read {L('blog/how-to-pray-salah-step-by-step/', 'how to pray salah step by step')} and {L('blog/how-to-perform-wudu/', 'how to perform wudu')} for the basics you can start this week.",
  "Can my children join the classes too?": f" Children have their own one to one classes with a female teacher, and many families book them back to back. See our {L('online-quran-classes-for-kids/', 'online Quran classes for kids')}.",
  "Are classes private?": f" Classes are one to one, never recorded, and you control your camera. Read our {L('faq/', 'FAQ and safeguarding page')} for the full privacy rules.",
 },
}

NEW = {
 "online-quran-classes-for-kids": [
  ("Which course should my child start with?", f"Most children start with {L('noorani-qaida-online/', 'Noorani Qaida online')}, which teaches the Arabic letters, sounds and joining. Children who can already read move to Quran reading (Nazra), then {L('online-tajweed-classes/', 'Tajweed')}, and many add {L('juz-amma-memorization-online/', 'Juz Amma memorisation')} early. The teacher checks your child's level in the free trial and suggests the right starting point, so you do not need to decide alone."),
  ("How do you keep young children focused online?", f"Classes are short, about 30 minutes, and the teacher uses the book on screen, repetition, praise and small games to keep young children engaged. A parent nearby helps a lot. If a child is tired or restless, the teacher shortens the new lesson and focuses on revision. Our guide on {L('blog/how-to-teach-quran-to-kids-at-home/', 'teaching Quran to kids at home')} has tips that support classes."),
  ("Do you teach children salah and duas too?", f"Yes. Alongside reading, children can learn {L('online-salah-classes/', 'salah')}, {L('online-duas-course/', 'daily duas')}, {L('40-hadith-for-kids/', '40 Hadith for kids')} and stories of the Prophets. Many families spend the last few minutes of each Quran class on one dua or one hadith, so learning connects to daily life. Tell us what you would like your child to learn and the teacher will plan it."),
 ],
 "online-quran-classes-for-women": [
  ("What can women learn in your classes?", f"Women can learn the {L('noorani-qaida-online/', 'Noorani Qaida')}, Quran reading, {L('online-tajweed-classes/', 'Tajweed')}, the {L('online-hifz-program/', 'Hifz program')}, {L('quran-translation-tafseer-classes/', 'translation and Tafseer')}, salah and daily duas. Every class is one to one with a female teacher, so you start at your own level and move at your own pace. The teacher suggests a plan after your free trial."),
  ("Can I continue classes during my period?", "Many scholars allow a woman on her period to recite from memory or for learning, while others restrict it, and most say she should not touch the mushaf directly. Many sisters continue with a screen, gloves or a separate book, or use those days for translation and duas. Tell your teacher which view you follow and she will plan the lessons around it."),
  ("Do you teach new Muslim sisters?", f"Yes. Revert sisters can start from the very first Arabic letters with a patient female teacher, alongside salah and the meaning of short surahs. There is no group to keep up with and no question is too basic. See our {L('quran-classes-for-new-muslims/', 'Quran classes for new Muslims')} for how the first weeks usually look."),
  ("How much do online Quran classes for women cost?", f"Fees are monthly and depend on the course and how many days a week you study. Reading, Qaida and Tajweed cost less than Hifz or Tafseer. Every sister starts with {TRIAL}, and after that the fee is paid monthly in advance. See prices in your own currency on our {FEES}, and ask about the family discount."),
 ],
 "female-quran-teachers": [
  ("Which courses do your female teachers teach?", f"Our female teachers teach {L('noorani-qaida-online/', 'Noorani Qaida')}, Quran reading, {L('online-tajweed-classes/', 'Tajweed')}, {L('online-hifz-program/', 'Hifz')}, {L('quran-translation-tafseer-classes/', 'translation and Tafseer')}, {L('online-islamic-studies/', 'Islamic studies')}, salah and daily duas. Each teacher focuses on the courses she knows best, and we match you with the right one after the free trial, based on age, level and language."),
  ("Do your teachers teach students in my country?", f"Yes. We teach families in many countries, including the {L('online-quran-classes-usa/', 'USA')}, {L('online-quran-classes-uk/', 'UK')}, {L('online-quran-classes-canada/', 'Canada')}, {L('online-quran-classes-australia/', 'Australia')}, the {L('online-quran-classes-uae/', 'UAE')} and {L('online-quran-classes-saudi-arabia/', 'Saudi Arabia')}. Classes are booked in your local time, and each country page lists the usual slots and fees in your currency."),
  ("How do I book a female Quran teacher?", f"Fill in the short form on this page or message us on WhatsApp with the student's age, level, preferred language and time. We reply within 24 hours and arrange {TRIAL} with a female teacher. If you are happy, you continue with the same teacher, and fees are paid monthly in advance after the trial."),
  ("Do teachers give updates to parents?", "Yes. Teachers send parents regular updates on WhatsApp about what the child learned, what to revise and how they are doing. Parents can also sit in on any lesson. We do not run formal tests or certificates, but you always know exactly where your child is and what comes next."),
 ],
 "noorani-qaida-online": [
  ("What does the Noorani Qaida teach?", f"The Noorani Qaida teaches the 28 Arabic letters, their sounds and shapes, joining letters, short and long vowels, sukoon, shaddah, tanween and the first Tajweed basics. It prepares the student to read directly from the Quran. Read our {L('resources/noorani-qaida-guide/', 'Noorani Qaida guide')} for what each lesson covers, in order."),
  ("How many days a week should my child study the Qaida?", f"Young children in the Qaida stage do best with 4 short classes a week, because they remember letters through frequent repetition. Older children and adults often manage well with 2 classes a week plus 10 minutes of daily practice. Compare the 2 day, 4 day and weekend plans on our {FEES}."),
  ("Do you teach Tajweed in the Noorani Qaida?", f"Yes. Correct makharij, heavy and light letters, ghunnah and madd are taught from the first Qaida lessons, by copying the teacher's sound. That way children do not form habits that need fixing later. Full Tajweed rules come in our {L('online-tajweed-classes/', 'online Tajweed classes')} once reading is steady."),
 ],
 "learn-quran-online-for-beginners": [
  ("What will I learn in the Quran reading course?", f"You will learn to read directly from the Quran with growing speed and confidence, usually starting with Juz Amma and moving through the Quran page by page. The teacher corrects every letter and introduces basic Tajweed as you go. If you cannot read Arabic letters yet, you start with {L('noorani-qaida-online/', 'Noorani Qaida online')} first."),
  ("How many classes a week do beginners need?", f"Most beginners do well with 2 to 4 classes of about 30 minutes each week, plus 10 minutes of daily practice. Children usually need more frequent classes than adults. Compare plans on our {FEES}, and read {L('blog/how-long-does-it-take-to-learn-quran/', 'how long it takes to learn the Quran')} for realistic timelines."),
  ("Can I learn to read the Quran in English or Urdu?", f"Yes. The Quran is always read in Arabic, but our teachers explain the letters, rules and corrections in English, Urdu or Arabic, whichever you understand best. Read {L('blog/learn-quran-in-urdu-english-arabic/', 'learn Quran in Urdu, English or Arabic')} to choose the right teaching language for you or your child."),
 ],
 "online-tajweed-classes": [
  ("What Tajweed rules will I learn?", f"You will learn makharij, the qualities of letters, the rules of noon sakinah and tanween, meem sakinah, ghunnah, {L('blog/qalqalah-in-tajweed/', 'qalqalah')}, {L('blog/madd-in-tajweed/', 'madd')}, lam and ra rules and where to stop. Our {L('resources/tajweed-rules/', 'Tajweed rules for beginners')} gives the full list, and the teacher applies each rule to the pages you read."),
  ("Do you correct Al-Fatiha in Tajweed classes?", "Yes. Al-Fatiha is recited in every rakat of every prayer, so the teacher usually corrects it first, letter by letter. Many adult students are surprised how much their salah improves after a few weeks. After Al-Fatiha, the teacher moves to the short surahs you recite most, then to longer passages."),
  ("How many classes a week do I need for Tajweed?", f"Two classes a week with daily practice suits most adults, while children often do better with four shorter classes. Each class is about 30 minutes. Compare plans on our {FEES}. Every student starts with {TRIAL}, and after that fees are paid monthly in advance."),
 ],
 "online-hifz-program": [
  ("How many lines will my child memorise each day?", "Beginners usually start with 3 to 5 lines a day, and confident students move to half a page or a full page. The teacher sets the amount after checking memory and reading speed, and lowers it if revision starts to slip. Strong revision always comes before speed in our program."),
  ("Do I need to read fluently before starting Hifz?", f"Yes. Students should read the Quran fluently with basic Tajweed before full Hifz, because memorising with mistakes means memorising the mistakes. If reading is still slow, start with {L('learn-quran-online-for-beginners/', 'Quran reading')} or {L('online-tajweed-classes/', 'Tajweed classes')}, or begin with {L('juz-amma-memorization-online/', 'Juz Amma memorisation')}."),
  ("Is the Hifz program available for girls and women?", "Yes. Girls, boys under 18 and adult women can join, and every teacher is female. Many mothers memorise part time with a few lines a day, and many girls complete Hifz alongside school. Classes are one to one, so each student moves at her own pace."),
 ],
 "quran-translation-tafseer-classes": [
  ("What will I learn in Translation and Tafseer classes?", f"You will learn the meaning of the Quran word by word, the context of verses, the lessons they teach and how the Prophet, peace be upon him, explained them. Most students start with Al-Fatiha and Juz Amma, so their salah becomes more meaningful straight away. Read {L('blog/tafseer-for-beginners/', 'Tafseer for beginners')} to see how we approach it."),
  ("Are Translation and Tafseer classes taught in Urdu?", f"Yes. Teachers explain in English, Urdu or Arabic, whichever you understand best. Many sisters choose Urdu, while students raised abroad usually prefer English. You can also compare well-known {L('blog/best-english-translation-of-quran/', 'English translations')} and Urdu translations with your teacher."),
  ("How much do Tafseer classes cost?", f"Tafseer classes are longer, about 45 to 60 minutes, so the monthly fee is higher than reading classes. Prices depend on how many days a week you study and are shown in your currency on our {FEES}. Every student starts with {TRIAL}, and after that fees are paid monthly in advance."),
 ],
 "online-islamic-studies": [
  ("What topics do Islamic studies classes cover?", f"Classes cover the pillars of Islam and iman, salah and wudu, daily duas, stories of the Prophets, good manners and selected hadith, adjusted to the student's age. See our guides on {L('blog/how-to-perform-wudu/', 'wudu')} and {L('blog/what-is-dua/', 'dua')} for examples of what is taught."),
  ("Are Islamic studies classes one to one?", "Yes. Every class is live and one to one with a female teacher, so the lessons follow your child's age, questions and pace. Parents are welcome to sit in. Many families combine Islamic studies with Quran reading in the same weekly plan, spending part of each class on each."),
  ("Do you teach Islamic studies to new Muslims?", f"Yes. New Muslim sisters and their children can learn the basics of belief, salah, wudu and daily duas step by step, with no question too simple. See our {L('quran-classes-for-new-muslims/', 'Quran classes for new Muslims')} for how the first weeks usually look."),
  ("How can I book Islamic studies classes?", f"Fill in the form on this page or message us on WhatsApp with the student's age and what you would like covered. We reply within 24 hours and arrange {TRIAL} with a female teacher. After the trial, fees are paid monthly in advance."),
 ],
 "online-duas-course": [
  ("How many duas will my child learn?", "Most children learn the everyday duas first, about 15 to 20, covering waking up, sleeping, eating, the toilet, leaving home and travel. Then they move on to the morning and evening adhkar and Rabbana duas from the Quran. The teacher adds one new dua at a time and revises the old ones every class."),
  ("Are the duas from authentic sources?", f"Yes. Every dua comes from the Quran or authentic hadith, and each one is taught with its reference, such as Sahih al-Bukhari, Sahih Muslim or Hisn al-Muslim. You can check them in our free {L('duas-azkar/', 'duas and azkar library')}, which lists the source of every dua."),
  ("Can women join the duas course?", f"Yes. Women learn the Arabic, pronunciation and meaning of daily duas, the adhkar and the Rabbana duas with a female teacher. Many sisters add the course to their Quran or Tajweed classes. See our {L('online-quran-classes-for-women/', 'Quran classes for women')} and {L('blog/what-is-dhikr/', 'what dhikr is')}."),
  ("How long are duas classes?", f"Classes are about 30 minutes, which is enough for one or two new duas plus revision. Children can join 2 or 4 days a week, or on weekends. Every student starts with {TRIAL}, and after that fees are paid monthly in advance."),
 ],
 "online-salah-classes": [
  ("What will I learn in online salah classes?", f"You will learn wudu, every position of salah, Al-Fatiha and short surahs, the words of ruku and sujood, the tashahhud and Durood Ibrahim, with their meaning. Children also learn how many rakats each prayer has. Our {L('resources/how-many-rakats/', 'rakat chart')} and {L('blog/sunnah-prayers/', 'sunnah prayers guide')} help at home."),
  ("How long does it take to learn salah?", "Many adults can pray on their own within a few weeks, starting with the movements and Al-Fatiha. Learning all the words with correct pronunciation and meaning usually takes 2 to 3 months of regular classes. Children often learn over a longer time, one prayer at a time."),
  ("Can children and parents learn salah together?", f"Yes. Many mothers learn alongside their children, or book classes back to back so the family practises the same lesson. Praying together at home is the best revision. Read {L('blog/how-to-pray-salah-step-by-step/', 'how to pray salah step by step')} for tips on teaching children gently."),
  ("How much do salah classes cost?", f"Fees are monthly and depend on how many days a week you study. Message us on WhatsApp and we will share them, or see our {FEES} for other courses. Every student starts with {TRIAL}, and after that fees are paid monthly in advance. Families with more than one student get a discount."),
 ],
 "juz-amma-memorization-online": [
  ("Which surah should my child memorise first?", f"Most children start with Al-Fatiha, then the shortest surahs at the end of the Quran, usually An-Nas, Al-Falaq and Al-Ikhlas, moving backwards through Juz Amma. Our list of {L('blog/short-surahs-for-kids/', 'short surahs for kids')} gives a tested order for the first 14 surahs with their meanings."),
  ("How do you help children remember the surahs?", "Each class includes the new lines, revision of recent surahs and a quick check of older ones. Children recite the surahs in their own salah, and parents get WhatsApp updates on what to revise at home. Little and often, with daily listening, keeps the surahs strong."),
  ("Will my child learn the meaning of the surahs?", f"Yes. The teacher explains the meaning of each surah in simple words in English, Urdu or Arabic, and tells the story behind surahs like Al-Fil and Al-Masad. Children remember surahs better when they understand them. Older children can continue with {L('quran-translation-tafseer-classes/', 'translation and Tafseer')}."),
  ("What comes after Juz Amma?", f"Many families add {L('blog/surah-al-mulk-benefits/', 'Surah Al-Mulk')}, the first ten verses of {L('blog/surah-al-kahf-on-friday/', 'Surah Al-Kahf')} and Surah Yasin, then decide whether to start the full {L('online-hifz-program/', 'Hifz program')}. The teacher will suggest the next step based on your child's reading and memory."),
 ],
 "40-hadith-for-kids": [
  ("Which hadith are in the course?", "The course follows Imam an-Nawawi's Forty Hadith, which includes the hadith of intention, the hadith of Jibreel on Islam, iman and ihsan, and hadith on kindness, honesty, good manners and avoiding harm. Teachers choose the order and depth to suit the child's age."),
  ("How long does the 40 Hadith course take?", "Most children learn one hadith every week or two, so the course usually takes several months to a year, depending on age and class frequency. Younger children may learn the shorter hadith first and return to the longer ones later. Revision is part of every class."),
  ("How does this course help my child's character?", f"Each hadith is linked to everyday life: telling the truth, being kind to parents, sharing, controlling anger and having a good intention. Children are encouraged to practise one lesson each week. Many parents pair it with our {L('online-duas-course/', 'daily duas course')} and {L('online-salah-classes/', 'salah classes')}."),
  ("How do I book the 40 Hadith course?", f"Fill in the form on this page or message us on WhatsApp with your child's age and level. We reply within 24 hours and arrange {TRIAL} with a female teacher. After the trial, fees are paid monthly in advance, and families with more than one child get a discount."),
 ],
 "quran-classes-for-new-muslims": [
  ("How long does it take a new Muslim to learn salah?", f"Many new Muslims can pray on their own within a few weeks, starting with the movements and Al-Fatiha. Learning all the words with meaning usually takes 2 to 3 months of regular classes. Read {L('blog/how-to-pray-salah-step-by-step/', 'how to pray salah step by step')} for a simple first-month plan."),
  ("Will I learn to read the Quran in Arabic?", f"Yes. You start with the Arabic letters through {L('noorani-qaida-online/', 'Noorani Qaida')}, then move to reading the Quran itself. Many reverts read slowly within 6 to 9 months of regular classes. Meanwhile, your teacher helps you memorise Al-Fatiha and short surahs for salah."),
  ("Can I learn the meaning of what I recite?", f"Yes. Teachers explain Al-Fatiha and the short surahs word by word in English, Urdu or Arabic, so your salah becomes meaningful from the start. Later you can join our {L('quran-translation-tafseer-classes/', 'translation and Tafseer classes')} and read our guide to the {L('blog/best-english-translation-of-quran/', 'best English translation of the Quran')}."),
  ("How do I start classes as a new Muslim?", f"Fill in the form on this page or message us on WhatsApp. Tell us what you already know, even if it is nothing, and when you are free. We reply within 24 hours and arrange {TRIAL} with a patient female teacher. After the trial, fees are paid monthly in advance."),
 ],
}

# a table for pages that had none (inserted before the 'Latest from the blog' section)
TABLES = {
 "female-quran-teachers": ("What Our Female Teachers Offer", "How our female Quran teachers compare with what families usually look for.",
   ["What families ask for", "With Quran Online Tarteel"],
   [["Teacher gender", "Always a female teacher"], ["Students", "Children under 18 and adult women only"], ["Class format", "Live, one to one, about 30 minutes"],
    ["Experience", "10 or more years of teaching each"], ["Teaching language", "English, Urdu or Arabic"], ["Parents", "Welcome to sit in on any lesson"],
    ["Trial", "2 free classes before any payment"]]),
 "online-islamic-studies": ("What Children Learn at Each Age", "Lessons are adjusted to the student's age and level.",
   ["Age", "Typical topics", "Related course"],
   [["4 to 6", "Kalima, short duas, stories of the Prophets, good manners", L("online-duas-course/", "Daily duas course")],
    ["7 to 10", "Wudu, salah, the pillars of Islam and iman, short hadith", L("online-salah-classes/", "Online salah classes")],
    ["11 to 17", "Meaning of surahs, character, seerah, 40 Hadith", L("40-hadith-for-kids/", "40 Hadith for kids")],
    ["Women", "Belief, salah, duas and practical fiqh questions", L("online-quran-classes-for-women/", "Quran classes for women")]]),
 "online-duas-course": ("Duas Taught in the Course", "Children start with everyday duas, then move on to adhkar and Quranic duas.",
   ["Stage", "Examples", "Read online"],
   [["Everyday duas", "Waking, sleeping, eating, toilet, leaving home", L("duas-azkar/daily-duas-for-kids/", "Daily duas for kids")],
    ["Protection", "Ayatul Kursi and the 3 Quls", L("duas-azkar/ayatul-kursi-and-4-quls/", "Ayatul Kursi and 4 Quls")],
    ["Daily adhkar", "Morning and evening adhkar, after salah", L("duas-azkar/morning-evening-azkar/", "Morning and evening azkar")],
    ["Quranic duas", "Rabbana duas for parents, knowledge and forgiveness", L("duas-azkar/rabbana-duas/", "40 Rabbana duas")]]),
 "online-salah-classes": ("What You Learn in Salah Classes", "A typical order for children, women and new Muslims.",
   ["Step", "What you learn", "Guide"],
   [["1", "Wudu and its dua", L("blog/how-to-perform-wudu/", "How to perform wudu")],
    ["2", "The positions of salah and the number of rakats", L("resources/how-many-rakats/", "How many rakats")],
    ["3", "Al-Fatiha and short surahs", L("blog/short-surahs-for-kids/", "Short surahs for kids")],
    ["4", "Words of ruku, sujood, tashahhud and Durood", L("blog/how-to-pray-salah-step-by-step/", "How to pray salah")],
    ["5", "Sunnah prayers, Witr and adhkar after salah", L("blog/sunnah-prayers/", "Sunnah prayers")]]),
 "juz-amma-memorization-online": ("A Suggested Order for Juz Amma", "Most children start with the shortest surahs and move backwards through the juz.",
   ["Stage", "Surahs", "Verses"],
   [["1", "Al-Fatiha, Al-Ikhlas, Al-Falaq, An-Nas", "7, 4, 5, 6"], ["2", "Al-Kawthar, Al-Asr, An-Nasr, Al-Kafirun", "3, 3, 3, 6"],
    ["3", "Al-Masad, Quraysh, Al-Ma'un, Al-Fil", "5, 4, 7, 5"], ["4", "Al-Humazah, At-Takathur, Al-Qari'ah, Al-Adiyat", "9, 8, 11, 11"],
    ["5", "The rest of Juz Amma, up to An-Naba", "Longer surahs, a few lines at a time"]]),
 "40-hadith-for-kids": ("Examples from the 40 Hadith", "A few of the hadith children learn, and the lesson each one teaches.",
   ["Hadith", "Lesson for children", "Source"],
   [["Actions are by intentions", "Do good for Allah, not to show off", "Sahih al-Bukhari 1, Sahih Muslim 1907"],
    ["None of you truly believes until he loves for his brother what he loves for himself", "Share and care for others", "Sahih al-Bukhari 13, Sahih Muslim 45"],
    ["Whoever believes in Allah and the Last Day, let him speak good or keep silent", "Think before you speak", "Sahih al-Bukhari 6018, Sahih Muslim 47"],
    ["Do not become angry", "Control anger", "Sahih al-Bukhari 6116"]]),
 "quran-classes-for-new-muslims": ("A Gentle Plan for the First Months", "Every revert is different. This is a typical order your teacher may follow.",
   ["Time", "Focus", "Guide"],
   [["Weeks 1 to 2", "Wudu, the movements of salah, the shahadah", L("blog/how-to-perform-wudu/", "How to perform wudu")],
    ["Weeks 3 to 4", "Al-Fatiha with meaning", L("blog/how-to-pray-salah-step-by-step/", "How to pray salah")],
    ["Months 2 to 3", "Arabic letters, short surahs, tashahhud", L("blog/arabic-alphabet/", "Arabic alphabet")],
    ["Months 4 to 9", "Noorani Qaida, then reading the Quran", L("noorani-qaida-online/", "Noorani Qaida online")]]),
}


def table_html(title, sub, head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f'<td data-label="{head[i]}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return (f'<!--SVCTABLE--><section class="sec bg-cream"><div class="container"><div class="section-head"><span class="eyebrow">At a Glance</span>'
            f'<h2>{title}</h2><p>{sub}</p></div><div class="table-wrap"><div class="table-scroll"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div></div></div></section><!--/SVCTABLE-->')


def main():
    for page in ADD:
        f = os.path.join(ROOT, page, "index.html")
        s = open(f, encoding="utf-8").read()
        items = read_items(s)
        out = []
        for q, a in items:
            add = ADD[page].get(strip(q), "")
            if add and strip(add)[-40:] not in strip(a):
                a = a.rstrip() + add
            out.append((q, a))
        have = {strip(q) for q, _ in out}
        out += [(q, a) for q, a in NEW.get(page, []) if q not in have]
        s = replace_section_items(s, out)
        s = set_ld(s, out)
        if page in TABLES:
            s = re.sub(r"<!--SVCTABLE-->.*?<!--/SVCTABLE-->", "", s, flags=re.S)
            anchor = "<!--BLOGLATEST-->" if "<!--BLOGLATEST-->" in s else '<section class="cta-sec dark pattern-dark" id="enrol">'
            s = s.replace(anchor, table_html(*TABLES[page]) + anchor, 1)
        assert "—" not in s
        open(f, "w", encoding="utf-8").write(s)
        short = [(strip(q)[:40], len(strip(a).split())) for q, a in out if len(strip(a).split()) < 45]
        print(page, len(out), "faqs", "short:", short)


if __name__ == "__main__":
    main()
