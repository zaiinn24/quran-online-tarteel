#!/usr/bin/env python3
"""Build 8 country pages (Saudi Arabia, Qatar, Kuwait, Oman, Bahrain, New Zealand, Ireland, South Africa)
from the live UAE page (same structure and design), with country-specific content and FAQs.
Then run: build_fees.py (fees in local currency), sitewide_countries (menu, chips, forms), policy_strip.py, stamp_assets.py."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from faqlib import replace_section_items, set_ld

L = lambda h, t: f'<a href="../{h}" class="in-link">{t}</a>'
PAY = ("Families abroad usually pay by bank transfer or Western Union, or a relative in Pakistan pays for them by JazzCash, Easypaisa or bank transfer. "
       "The fee is paid monthly, in advance, after your " + L("free-trial/", "2 free classes") + ", and we share the payment details on WhatsApp. "
       "We do not take card or PayPal payments at the moment.")
GULF_TIMES = [("Morning", "Mothers at home, younger children", "Reading, Tajweed, Tafseer"),
              ("After school", "School children", "Noorani Qaida, Nazra, short Hifz lessons"),
              ("Evening", "Older children, working women", "Tajweed, Hifz revision"),
              ("Weekends", "Busy families", "Longer lessons, catch-up classes")]
WEST_TIMES = [("After school", "School children", "Noorani Qaida, Nazra, short Hifz lessons"),
              ("Early evening", "Older children, working women", "Tajweed, Hifz revision"),
              ("Weekend mornings", "Busy families", "Longer lessons, Tafseer"),
              ("School holidays", "Children who want to move faster", "Extra days, Juz Amma, Hifz")]


def gulf(c):
    """shared Gulf wording"""
    return dict(
        how=("No traffic, no long drives", f"There is no drive across {c['city1']} to a Quran centre and no waiting outside in the heat. Your child logs in from home at the booked time and the lesson starts."),
        kids_a=("Classes around the school week", f"Weekday lessons are usually booked after school, whether your child attends a {c['school']}. Weekend slots suit families who want longer lessons, and school holidays are a good time to add extra days."),
        kids_b=("The same teacher if you move", f"Many families in {c['the']} relocate for work or return to Pakistan. With online classes, your child keeps the same teacher and the same progress after a move, wherever you go next."),
        compare_local="Typical Quran centre class",
        compare_travel="Drive there and back in traffic",
        times=GULF_TIMES,
        lang_q=f"Do your teachers teach in Arabic, Urdu and English?",
        lang_a=(f"Yes. Our teachers explain in English, Urdu or Arabic, whichever your child understands best. Many Pakistani and Indian families in {c['the']} choose Urdu, "
                f"Arab families often prefer Arabic, and children at international schools usually prefer English. The Quran itself is always read in Arabic. "
                f"Tell us your preference when you book and we will match the right teacher."),
    )


C = {
 "saudi-arabia": dict(
    name="Saudi Arabia", the="Saudi Arabia", the_cap="Saudi Arabia", adj="Saudi", city1="Riyadh", tz="Arabia Standard Time (AST, UTC+3)",
    title="Online Quran Classes in Saudi Arabia | Female Teachers",
    desc="Online Quran classes in Saudi Arabia for kids and women with female teachers. Live 1-on-1 lessons in Saudi time, in English, Urdu or Arabic. 2 free classes.",
    eyebrow="Female Quran Teachers Across the Kingdom",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in Saudi Arabia for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in Saudi time for families in Riyadh, Jeddah, Dammam, Makkah, Madinah and across the Kingdom, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+966 50 123 4567", school="Saudi school or an international school",
    note="Pakistan is two hours ahead of Saudi Arabia, so after-school and evening slots in Saudi time are easy to book. Saudi Arabia does not change its clocks, so your class time stays the same all year. Our weekend plan runs on Saturday and Sunday.",
    cities_q="Do you teach families in Riyadh, Jeddah and Dammam?",
    cities_a="Yes. We teach families anywhere in Saudi Arabia, including Riyadh, Jeddah, Dammam, Al Khobar, Makkah, Madinah, Taif and Abha. All classes are online and booked in Saudi time, so it makes no difference which city you live in. You only need a phone, tablet or laptop and a steady internet connection, and the class link is always sent to the parent.",
    extra_q="Why learn online when there are Quran circles in Saudi Arabia?",
    extra_a="Many children in Saudi Arabia attend Quran circles at the masjid, which are a blessing. Online classes add what a busy circle often cannot: one-to-one attention, a female teacher, explanations in English or Urdu for expat children, and times that fit around school. Many families use both, with online lessons for focused Tajweed and Hifz revision at home.",
 ),
 "qatar": dict(
    name="Qatar", the="Qatar", the_cap="Qatar", adj="Qatari", city1="Doha", tz="Arabia Standard Time (AST, UTC+3)",
    title="Online Quran Classes in Qatar | Female Quran Teachers Online",
    desc="Online Quran classes in Qatar for kids and women with female teachers. Live 1-on-1 lessons in Qatar time for families in Doha, in English, Urdu or Arabic.",
    eyebrow="Female Quran Teachers for Families in Qatar",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in Qatar for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in Qatar time for families in Doha, Al Rayyan, Al Wakrah, Lusail and Al Khor, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+974 3312 3456", school="Qatari school or an international school",
    note="Pakistan is two hours ahead of Qatar, so after-school and evening slots in Qatar time are easy to book. Qatar does not change its clocks, so your class time stays the same all year. Our weekend plan runs on Saturday and Sunday.",
    cities_q="Do you teach families in Doha and Al Rayyan?",
    cities_a="Yes. We teach families anywhere in Qatar, including Doha, Al Rayyan, Al Wakrah, Lusail, Al Khor and Umm Salal. All classes are online and booked in Qatar time, so your location makes no difference. You only need a phone, tablet or laptop and a steady internet connection. The class link and timing are always sent to the parent, never directly to the child.",
    extra_q="Can my child keep learning if we move back to Pakistan?",
    extra_a="Yes. Many families in Qatar move for work, and online classes go with you. If you move back to Pakistan or to another country, your child keeps the same female teacher, the same lesson plan and the same progress. We simply adjust the class time to your new time zone, and nothing else changes for your child.",
 ),
 "kuwait": dict(
    name="Kuwait", the="Kuwait", the_cap="Kuwait", adj="Kuwaiti", city1="Kuwait City", tz="Arabia Standard Time (AST, UTC+3)",
    title="Online Quran Classes in Kuwait | Female Quran Teachers Online",
    desc="Online Quran classes in Kuwait for kids and women with female teachers. Live 1-on-1 lessons in Kuwait time, in English, Urdu or Arabic. 2 free classes.",
    eyebrow="Female Quran Teachers for Families in Kuwait",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in Kuwait for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in Kuwait time for families in Kuwait City, Hawalli, Salmiya, Farwaniya, Jahra and Ahmadi, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+965 5012 3456", school="Kuwaiti school or an international school",
    note="Pakistan is two hours ahead of Kuwait, so after-school and evening slots in Kuwait time are easy to book. Kuwait does not change its clocks, so your class time stays the same all year. Our weekend plan runs on Saturday and Sunday.",
    cities_q="Do you teach families in Kuwait City, Salmiya and Farwaniya?",
    cities_a="Yes. We teach families anywhere in Kuwait, including Kuwait City, Hawalli, Salmiya, Farwaniya, Jahra, Ahmadi and Mangaf. All classes are online and booked in Kuwait time, so your area makes no difference. You only need a phone, tablet or laptop and a steady internet connection, and parents receive the class link and timing directly.",
    extra_q="Can my child keep learning if we move back to Pakistan?",
    extra_a="Yes. Many families in Kuwait move for work, and online classes move with you. If you return to Pakistan or relocate to another country, your child keeps the same female teacher, the same lesson plan and the same progress. We only adjust the class time to your new time zone, so your child's Quran routine continues without a break.",
 ),
 "oman": dict(
    name="Oman", the="Oman", the_cap="Oman", adj="Omani", city1="Muscat", tz="Gulf Standard Time (GST, UTC+4)",
    title="Online Quran Classes in Oman | Female Quran Teachers Online",
    desc="Online Quran classes in Oman for kids and women with female teachers. Live 1-on-1 lessons in Oman time for Muscat, Salalah and Sohar. 2 free classes.",
    eyebrow="Female Quran Teachers for Families in Oman",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in Oman for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in Oman time for families in Muscat, Seeb, Salalah, Sohar, Nizwa and Sur, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+968 9212 3456", school="local school or an international school",
    note="Pakistan is only one hour ahead of Oman, so almost every slot from morning to evening is easy to book. Oman does not change its clocks, so your class time stays the same all year. Our weekend plan runs on Saturday and Sunday.",
    cities_q="Do you teach families in Muscat, Salalah and Sohar?",
    cities_a="Yes. We teach families anywhere in Oman, including Muscat, Seeb, Salalah, Sohar, Nizwa, Sur and Ibri. All classes are online and booked in Oman time, so it makes no difference where you live, even in smaller towns far from a Quran centre. You only need a phone, tablet or laptop and a steady internet connection.",
    extra_q="Can my child keep learning if we move back to Pakistan?",
    extra_a="Yes. Many families in Oman move for work, and online classes go wherever you go. If you return to Pakistan or move to another country, your child keeps the same female teacher, the same lesson plan and the same progress. Because Pakistan is only one hour ahead of Oman, the class time usually changes very little after the move.",
 ),
 "bahrain": dict(
    name="Bahrain", the="Bahrain", the_cap="Bahrain", adj="Bahraini", city1="Manama", tz="Arabia Standard Time (AST, UTC+3)",
    title="Online Quran Classes in Bahrain | Female Quran Teachers Online",
    desc="Online Quran classes in Bahrain for kids and women with female teachers. Live 1-on-1 lessons in Bahrain time for Manama, Riffa and Muharraq. 2 free classes.",
    eyebrow="Female Quran Teachers for Families in Bahrain",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in Bahrain for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in Bahrain time for families in Manama, Riffa, Muharraq, Isa Town and Hamad Town, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+973 3612 3456", school="local school or an international school",
    note="Pakistan is two hours ahead of Bahrain, so after-school and evening slots in Bahrain time are easy to book. Bahrain does not change its clocks, so your class time stays the same all year. Our weekend plan runs on Saturday and Sunday.",
    cities_q="Do you teach families in Manama, Riffa and Muharraq?",
    cities_a="Yes. We teach families anywhere in Bahrain, including Manama, Riffa, Muharraq, Isa Town, Hamad Town, Juffair and Saar. All classes are online and booked in Bahrain time, so your area makes no difference. You only need a phone, tablet or laptop and a steady internet connection, and the class link always goes to the parent.",
    extra_q="Can my child keep learning if we move back to Pakistan?",
    extra_a="Yes. Many families in Bahrain move for work, and online classes go with you. If you return to Pakistan or relocate to another country, your child keeps the same female teacher, the same lesson plan and the same progress. We simply adjust the class time to your new time zone, so the Quran routine continues without starting again.",
 ),
 "new-zealand": dict(
    name="New Zealand", the="New Zealand", the_cap="New Zealand", adj="New Zealand", city1="Auckland", tz="New Zealand time (NZST, UTC+12, or NZDT, UTC+13 in summer)",
    title="Online Quran Classes in New Zealand | Female Teachers Online",
    desc="Online Quran classes in New Zealand for kids and women with female teachers. Live 1-on-1 lessons in NZ time for Auckland, Wellington and Christchurch.",
    eyebrow="Female Quran Teachers for Families in New Zealand",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in New Zealand for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in New Zealand time for families in Auckland, Wellington, Christchurch, Hamilton and beyond, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+64 21 123 4567",
    note="Pakistan is 7 hours behind New Zealand (8 hours during New Zealand daylight saving), so after-school and evening slots in New Zealand fall in Pakistan's daytime and are easy to book. Early mornings in New Zealand are the middle of the night in Pakistan, so ask us first if you need one. We adjust your class time when New Zealand clocks change.",
    how=("A Quran teacher even far from a mosque", "Many families outside Auckland and Wellington have no Quran teacher nearby, or only a weekend class. With online classes, a child in Hamilton, Dunedin or a small town gets the same live one-to-one lesson, with just a laptop or tablet and an internet connection."),
    kids_a=("Alongside weekend madrasa classes", "Many Muslim children in New Zealand attend a weekend madrasa at the local mosque. One-to-one online lessons add focused Quran reading and Tajweed practice during the week, at your child's own pace, so they do not fall behind between weekends."),
    kids_b=("Classes around the school day", "Weekday lessons are usually booked after school, and Saturday or Sunday slots suit families who want longer lessons. The school holidays between terms are a good time to add extra days and move faster through the Qaida or Hifz."),
    compare_local="Typical mosque or madrasa class", compare_travel="Drive there and back, often far",
    times=WEST_TIMES,
    lang_q="Do your teachers teach in English?",
    lang_a="Yes. Our teachers explain in English, Urdu or Arabic, so children who grew up in New Zealand and study in English at school can follow every lesson easily. Many Pakistani and Arab families also choose Urdu or Arabic for mothers. The Quran itself is always read in Arabic. Tell us your preference when you book and we will match the right teacher.",
    cities_q="Do you teach families in Auckland, Wellington and Christchurch?",
    cities_a="Yes. We teach families anywhere in New Zealand, including Auckland, Wellington, Christchurch, Hamilton, Tauranga, Dunedin and Palmerston North. All classes are online and booked in New Zealand time, so it makes no difference how far you live from a mosque. You only need a laptop, tablet or phone and a steady internet connection.",
    extra_q="Do class times change when New Zealand clocks change?",
    extra_a="Your class stays at the same New Zealand time all year. New Zealand moves its clocks forward in late September and back in early April, while Pakistan does not change its clocks, so we adjust the teacher's side of the timetable for you. You do not need to do anything. We will message you on WhatsApp before each change so you know.",
 ),
 "ireland": dict(
    name="Ireland", the="Ireland", the_cap="Ireland", adj="Irish", city1="Dublin", tz="Irish time (GMT in winter, IST, UTC+1, in summer)",
    title="Online Quran Classes in Ireland | Female Quran Teachers Online",
    desc="Online Quran classes in Ireland for kids and women with female teachers. Live 1-on-1 lessons in Irish time for Dublin, Cork and Galway. 2 free classes.",
    eyebrow="Female Quran Teachers for Families in Ireland",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in Ireland for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in Irish time for families in Dublin, Cork, Galway, Limerick, Waterford and beyond, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+353 85 123 4567",
    note="Pakistan is 5 hours ahead of Ireland in winter and 4 hours ahead in summer, so after-school slots, early evenings and weekend mornings in Ireland are the easiest times to book. Late evenings in Ireland are very late at night in Pakistan, so ask us first if you need one. We adjust your class time when Irish clocks change.",
    how=("A Quran teacher wherever you live", "Outside Dublin, many families have no Quran teacher nearby, or only a weekend class at the mosque. With online classes, a child in Cork, Galway, Limerick or a small town gets the same live one-to-one lesson, with just a laptop or tablet and an internet connection."),
    kids_a=("Alongside weekend madrasa classes", "Many Muslim children in Ireland attend a weekend madrasa at the local mosque or Islamic centre. One-to-one online lessons add focused Quran reading and Tajweed practice during the week, at your child's own pace, so progress does not stop between weekends."),
    kids_b=("Classes around the school day", "Weekday lessons are usually booked after school, and Saturday or Sunday morning slots suit families who want longer lessons. Mid-term breaks and the summer holidays are a good time to add extra days and move faster through the Qaida or Hifz."),
    compare_local="Typical mosque or madrasa class", compare_travel="Drive there and back, often far",
    times=WEST_TIMES,
    lang_q="Do your teachers teach in English?",
    lang_a="Yes. Our teachers explain in English, Urdu or Arabic, so children who grew up in Ireland and study in English at school can follow every lesson easily. Many Pakistani and Arab families also choose Urdu or Arabic for mothers. Classes are not taught in Irish. The Quran itself is always read in Arabic. Tell us your preference when you book.",
    cities_q="Do you teach families in Dublin, Cork and Galway?",
    cities_a="Yes. We teach families anywhere in Ireland, including Dublin, Cork, Galway, Limerick, Waterford, Athlone, Dundalk and Ennis. All classes are online and booked in Irish time, so it makes no difference how far you live from a mosque or Islamic centre. You only need a laptop, tablet or phone and a steady internet connection.",
    extra_q="Do class times change when Irish clocks change?",
    extra_a="Your class stays at the same Irish time all year. Ireland moves its clocks forward in late March and back in late October, while Pakistan does not change its clocks, so we adjust the teacher's side of the timetable for you. You do not need to do anything, and we will message you on WhatsApp before each change.",
 ),
 "south-africa": dict(
    name="South Africa", the="South Africa", the_cap="South Africa", adj="South African", city1="Johannesburg", tz="South African Standard Time (SAST, UTC+2)",
    title="Online Quran Classes in South Africa | Female Quran Teachers",
    desc="Online Quran classes in South Africa for kids and women with female teachers. Live 1-on-1 lessons in SA time for Johannesburg, Cape Town and Durban.",
    eyebrow="Female Quran Teachers for Families in South Africa",
    lead="Quran Online Tarteel offers live one-to-one online Quran classes in South Africa for children and women, taught only by female teachers in English, Urdu or Arabic. Lessons are booked in South African time for families in Johannesburg, Cape Town, Durban, Pretoria and beyond, and cover Noorani Qaida, Quran reading, Tajweed and Hifz. Your first 2 classes are free.",
    phone="+27 82 123 4567",
    note="Pakistan is 3 hours ahead of South Africa, so after-school and early evening slots in South Africa are easy to book. South Africa does not change its clocks, so your class time stays the same all year. Tell us your city and preferred time when you book.",
    how=("No rushing between school and madressa", "Many children in South Africa go straight from school to afternoon madressa. Online classes can replace that rush or add to it: your child logs in from home at the booked time, with no drive across town, and gets a teacher's full attention for the whole lesson."),
    kids_a=("Alongside afternoon madressa", "Many Muslim children in South Africa attend afternoon madressa, which teaches Quran, duas and Islamic manners in a group. One-to-one online lessons add focused Tajweed and Hifz practice at your child's own pace, or give a full Quran lesson where no madressa is nearby."),
    kids_b=("Classes around the school day", "Weekday lessons are usually booked after school, and Saturday or Sunday slots suit families who want longer lessons. School holidays between terms are a good time to add extra days and move faster through the Qaida or Hifz."),
    compare_local="Typical madressa class", compare_travel="Drive there and back after school",
    times=WEST_TIMES,
    lang_q="Do your teachers teach in English?",
    lang_a="Yes. Our teachers explain in English, Urdu or Arabic, so children in South Africa who study in English at school can follow every lesson easily. Classes are not taught in Afrikaans or other local languages, and the Quran itself is always read in Arabic. Tell us your child's age and level when you book and we will match the right teacher.",
    cities_q="Do you teach families in Johannesburg, Cape Town and Durban?",
    cities_a="Yes. We teach families anywhere in South Africa, including Johannesburg, Cape Town, Durban, Pretoria, Port Elizabeth (Gqeberha), Lenasia, Pietermaritzburg and Polokwane. All classes are online and booked in South African time, so your city makes no difference. You only need a laptop, tablet or phone and a steady internet connection.",
    extra_q="Can online classes replace afternoon madressa?",
    extra_a="For many families, yes. One-to-one online classes cover Noorani Qaida, Quran reading, Tajweed, Hifz, salah and daily duas, so a child can learn everything madressa teaches, at their own pace. Other families keep madressa for its community and add online lessons for focused Quran practice. Try 2 free classes first and decide what suits your child.",
 ),
}
for k, c in C.items():
    if "how" not in c:
        for kk, vv in gulf(c).items():
            c.setdefault(kk, vv)


def faqs(c):
    n = c["the"]
    return [
        (f"How much do online Quran classes cost in {n}?", "PLACEHOLDER (filled by build_fees.py)"),
        (c["cities_q"], c["cities_a"]),
        (f"Are there online Quran classes for women in {n}?",
         f"Yes. Women of any age in {n} can learn to read the Quran, improve Tajweed, memorise surahs or study translation and Tafseer with a female teacher. "
         f"Classes are private and one-to-one, and many mothers book lessons while the children are at school. We do not enrol adult men. See our "
         + L("online-quran-classes-for-women/", "online Quran classes for women") + "."),
        (f"What class times are available in {n}?",
         f"Classes run after school, in the evening and at weekends, and on weekday mornings where time zones allow, all booked in {c['tz']}. {c['note']}"),
        (c["lang_q"], c["lang_a"]),
        (f"How do I pay for online Quran classes from {n}?", PAY + f" The monthly fees in {c['word']} are in the fees table on this page."),
        (c["extra_q"], c["extra_a"]),
        (f"Are online Quran classes safe for children in {n}?",
         "Yes. Every teacher is female, every class is one-to-one, and we only teach children under 18 and adult women. The class link and timing always go to the parent, "
         "never directly to the child, and parents are welcome to sit in on any lesson. We never record classes. Read our " + L("faq/", "FAQ and safeguarding page") + " for the full rules."),
        ("Are classes held during Ramadan?",
         "Yes. In Ramadan the class timings change, and we agree new times with you before the month begins, around suhoor, school and iftar. "
         "Classes are off on Eid and on Pakistan's public holidays. See our " + L("blog/ramadan-quran-plan/", "Ramadan Quran plan") + " for ideas to make the month count."),
    ]


WORD = {"saudi-arabia": "Saudi riyals", "qatar": "Qatari riyals", "kuwait": "Kuwaiti dinars", "oman": "Omani rials", "bahrain": "Bahraini dinars",
        "new-zealand": "New Zealand dollars", "ireland": "euros", "south-africa": "South African rand"}


def build(key, c):
    c["word"] = WORD[key]
    s = open(os.path.join(ROOT, "online-quran-classes-uae", "index.html"), encoding="utf-8").read()
    slug = f"online-quran-classes-{key}"
    URL = f"https://quranonlinetarteel.net/{slug}/"
    n, cap = c["the"], c["name"]

    def rep(old, new, cnt=1):
        nonlocal s
        k = s.count(old)
        assert k == cnt, (key, k, old[:90])
        s = s.replace(old, new)

    def rx(pat, new, k=1):
        nonlocal s
        s2, m = re.subn(pat, new, s, flags=re.S)
        assert m == k, (key, m, pat[:80])
        s = s2

    s = re.sub(r"<title>.*?</title>", f"<title>{c['title']}</title>", s, count=1)
    for prop in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        rx(r'(<meta %s content=")[^"]*' % re.escape(prop), lambda m: m.group(1) + c["desc"])
    for prop in ['property="og:title"', 'name="twitter:title"']:
        rx(r'(<meta %s content=")[^"]*' % re.escape(prop), lambda m: m.group(1) + c["title"])
    rep("https://quranonlinetarteel.net/online-quran-classes-uae/", URL, cnt=s.count("https://quranonlinetarteel.net/online-quran-classes-uae/"))
    rep('"name": "Online Quran Classes in the UAE with Female Teachers"', f'"name": "Online Quran Classes in {cap} with Female Teachers"')
    rx(r'("description": ")Online Quran classes in the UAE for kids[^"]*"', lambda m: m.group(1) + c["desc"] + '"')
    rep('{"@type": "Country", "name": "UAE"}', '{"@type": "Country", "name": "%s"}' % cap, cnt=2)
    rep('"name": "Online Quran Classes in UAE", "item"', f'"name": "Online Quran Classes in {cap}", "item"')
    # hero
    rep('<span class="eyebrow">Female Quran Teachers Across the Emirates</span>', f'<span class="eyebrow">{c["eyebrow"]}</span>')
    s = re.sub(r"<h1>.*?</h1>", lambda m: f'<h1>Online Quran Classes in {cap} with <span class="gold">Female Teachers</span></h1>', s, count=1, flags=re.S)
    s = re.sub(r'<p class="hero-lead">.*?</p>', lambda m: f'<p class="hero-lead">{c["lead"]}</p>', s, count=1, flags=re.S)
    rep("</span>Classes in UAE time</li>", f"</span>Classes in {cap} time</li>")
    rep('value="UAE page"', f'value="{cap} page"')
    rep('value="UAE page (bottom)"', f'value="{cap} page (bottom)"')
    rep('name="country" value="UAE"', f'name="country" value="{cap}"')
    rep('placeholder="+971 50 123 4567"', f'placeholder="{c["phone"]}"', cnt=2)
    # how it works
    rep("<h2>How Do Online Quran Classes Work in the UAE?</h2><p>Online Quran classes in the UAE are",
        f"<h2>How Do Online Quran Classes Work in {n}?</h2><p>Online Quran classes in {n} are")
    rep("<h3>No traffic, no pick-ups</h3><p>There is no drive across the city to a Quran centre and no waiting outside. Your child logs in from home at the booked time and the lesson starts.</p>",
        f"<h3>{c['how'][0]}</h3><p>{c['how'][1]}</p>")
    rep("<h3>Who can join from the UAE</h3>", f"<h3>Who can join from {n}</h3>")
    rep("<h2>Which Online Quran Courses Can You Take in the UAE?</h2>", f"<h2>Which Online Quran Courses Can You Take in {n}?</h2>")
    # kids
    rep("<h2>Online Quran Classes for Kids in the UAE</h2><p>Online Quran classes for kids in the UAE fit around",
        f"<h2>Online Quran Classes for Kids in {n}</h2><p>Online Quran classes for kids in {n} fit around")
    rep("<h3>Classes around the school week</h3><p>Weekday lessons are usually booked after school, and weekend slots suit families who want longer lessons. School holidays are a good time to add extra days.</p>",
        f"<h3>{c['kids_a'][0]}</h3><p>{c['kids_a'][1]}</p>")
    rep("<h3>The same teacher if you move</h3><p>Many families in the UAE relocate for work. With online classes, your child keeps the same teacher and the same progress after a move, in the UAE or abroad.</p>",
        f"<h3>{c['kids_b'][0]}</h3><p>{c['kids_b'][1]}</p>")
    # women
    rep("<h2>Online Quran Classes for Women in the UAE</h2><p>Our online Quran classes for women in the UAE are",
        f"<h2>Online Quran Classes for Women in {n}</h2><p>Our online Quran classes for women in {n} are")
    # class times
    rows = "".join(f'<tr><td data-label="Time of day"><span class="lvl">{a}</span></td><td data-label="Who it usually suits">{b}</td><td data-label="Good for">{g}</td></tr>' for a, b, g in c["times"])
    rx(r"<h2>Class Times in the UAE</h2>.*?</section>",
       f"<h2>Class Times in {cap}</h2><p>All classes are booked in {c['tz']}. These are the slots families in {n} ask for most often.</p></div>"
       '<div class="table-wrap"><div class="table-scroll"><table class=""><thead><tr><th>Time of day</th><th>Who it usually suits</th><th>Good for</th></tr></thead><tbody>'
       + rows + f'</tbody></table></div></div><p style="text-align:center;color:var(--muted);margin-top:16px">{c["note"]}</p></div></section>')
    # compare
    rep("<h2>Online Quran Classes vs Quran Centre Classes in the UAE</h2><p>Many UAE families have used a local Quran centre.",
        f"<h2>Online Quran Classes vs {c["compare_local"].replace("Typical ", "").replace(" class", "").title().replace(" Or ", " or ")} Classes in {n}</h2><p>Many families in {n} have used a local {c['compare_local'].replace('Typical ', '').replace(' class', '')}.")
    rep("Typical Quran centre class", c["compare_local"], cnt=s.count("Typical Quran centre class"))
    rep(">Drive there and back in traffic<", f">{c['compare_travel']}<")
    if c["compare_local"] != "Typical Quran centre class":
        rep(">Depends on the centre<", ">Depends on the teacher<")
        rep(">Fixed centre timings<", ">Fixed class timings<")
    # why
    rep('<span class="eyebrow">Why UAE Families Choose Us</span><h2>Why Families in the UAE Choose a Female Online Quran Teacher</h2><p>For many parents in the UAE,',
        f'<span class="eyebrow">Why Families in {cap} Choose Us</span><h2>Why Families in {n} Choose a Female Online Quran Teacher</h2><p>For many parents in {n},')
    rep("<h2>How to Start Online Quran Classes in the UAE in 4 Steps</h2>", f"<h2>How to Start Online Quran Classes in {n} in 4 Steps</h2>")
    rep("<h3>Ready to start Quran classes in the UAE?</h3>", f"<h3>Ready to start Quran classes in {n}?</h3>")
    rep("Class times that suit families in the UAE", f"Class times that suit families in {n}")
    rep('data-wa="Assalamu alaikum, I am in the UAE and want to book free Quran classes."', f'data-wa="Assalamu alaikum, I am in {n} and want to book free Quran classes."')
    # FAQ
    F = faqs(c)
    s = replace_section_items(s, F)
    s = set_ld(s, F)
    rx(r"<h2>Online Quran Classes in UAE: Frequently Asked Questions</h2>", f"<h2>Online Quran Classes in {cap}: Frequently Asked Questions</h2>")
    # leftovers
    main = s[s.index("<main"):s.index("</main>")]
    main = re.sub(r"<!--FEES:country-->.*?<!--/FEES-->|<!--FEEHERO-->.*?<!--/FEEHERO-->|<option[^>]*>UAE</option>|online-quran-classes-uae/|classes in UAE<|Classes in UAE<", "", main, flags=re.S)
    left = re.findall(r".{40}(?:UAE|[Ee]mirate|Dubai|Abu Dhabi|Sharjah|Ajman|dirham).{40}", main)
    assert "—" not in s
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    open(os.path.join(ROOT, slug, "index.html"), "w", encoding="utf-8").write(s)
    print(slug, "title", len(c["title"]), "desc", len(c["desc"]), "lead words", len(c["lead"].split()), "leftovers:", left)
    for q, a in F[1:]:
        w = len(re.sub("<[^>]+>", "", a).split())
        if not 45 <= w <= 95:
            print("   faq words", w, q)


if __name__ == "__main__":
    for k, c in C.items():
        build(k, c)
