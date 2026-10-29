#!/usr/bin/env python3
"""Step 9: About page story in the founder's (a mother's) voice + 'Our promise to every parent' + homepage founder note.
Facts used are only the ones the owner confirmed: teaching since 2010, 500+ children taught worldwide, female teachers with 10+ years'
experience, recitation checked before teaching, parents may sit in, link goes to the parent's phone, children keep camera on,
teacher camera off (turned on once if parents want to confirm she is a woman), no recordings, same teacher. Idempotent."""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ILLUS = ('<svg class="illus story-illus" viewBox="0 0 480 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A Quran on a wooden stand beside a lamp, teaching since 2010">'
         '<title>Teaching the Quran since 2010</title><defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2c47e"/><stop offset="1" stop-color="#a97f2e"/></linearGradient>'
         '<linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e261a"/><stop offset="1" stop-color="#14110c"/></linearGradient>'
         '<radialGradient id="sgl" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#c79b45" stop-opacity=".45"/><stop offset="1" stop-color="#c79b45" stop-opacity="0"/></radialGradient>'
         '<pattern id="spat" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M20 3l5 12 12 5-12 5-5 12-5-12-12-5 12-5z" fill="none" stroke="#c79b45" stroke-opacity=".13"/></pattern></defs>'
         '<path d="M60 440V180C60 86 150 24 240 24s180 62 180 156V440Z" fill="url(#sbg)"/><path d="M60 440V180C60 86 150 24 240 24s180 62 180 156V440Z" fill="url(#spat)"/>'
         '<ellipse cx="240" cy="190" rx="190" ry="160" fill="url(#sgl)"/>'
         '<path d="M48 440V176C48 76 142 12 240 12s192 64 192 164V440" fill="none" stroke="url(#sg)" stroke-width="2.5"/>'
         # rehal (wooden stand)
         '<path d="M150 360L240 300L330 360" fill="none" stroke="#a97f2e" stroke-width="10" stroke-linecap="round"/>'
         '<path d="M150 300L240 360L330 300" fill="none" stroke="#8a6420" stroke-width="10" stroke-linecap="round"/>'
         # open book
         '<path d="M240 300C210 284 172 280 136 286V214C172 208 210 212 240 228Z" fill="#fbf3df" stroke="#c79b45" stroke-width="2"/>'
         '<path d="M240 300C270 284 308 280 344 286V214C308 208 270 212 240 228Z" fill="#f6ead0" stroke="#c79b45" stroke-width="2"/>'
         '<g stroke="#c79b45" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"><path d="M154 232H222M154 246H222M154 260H222M154 274H210"/><path d="M258 232H326M258 246H326M258 260H326M270 274H326"/></g>'
         # lamp
         '<g transform="translate(372,250)"><path d="M-14 0C-14-14-6-22 0-30C6-22 14-14 14 0Z" fill="#ffd27a"/><ellipse cx="0" cy="0" rx="26" ry="9" fill="url(#sg)"/><path d="M-26 0C-22 16 22 16 26 0" fill="#a97f2e"/></g>'
         # seal
         '<g transform="translate(240,112)"><circle r="46" fill="none" stroke="url(#sg)" stroke-width="2.5"/><circle r="38" fill="none" stroke="#c79b45" stroke-opacity=".4"/>'
         '<text y="-8" text-anchor="middle" font-family="Manrope, sans-serif" font-size="11" font-weight="800" letter-spacing="2" fill="#e2c47e">SINCE</text>'
         '<text y="18" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="26" font-weight="700" fill="#fbf7ee">2010</text></g>'
         '</svg>')

STORY = (
    '<!--STORY--><section class="sec bg-cream story-sec" id="our-story"><div class="container"><div class="story-grid">'
    f'<div class="story-media"><div class="illus-wrap">{ILLUS}</div></div>'
    '<div class="story-letter"><span class="eyebrow">Our Story</span><h2>A Note from Our Founder, a Mother</h2>'
    '<div class="letter-card"><span class="q-mark" aria-hidden="true">&ldquo;</span>'
    '<p class="letter-salam">Assalamu alaikum,</p>'
    '<p>I began teaching the Quran in 2010, one child at a time. As a mother, I know the questions that sit in a parent&rsquo;s heart before the first lesson: <em>Will the teacher be patient with my child? Will my daughter feel safe? Will my son really learn, or just sit in front of a screen?</em></p>'
    '<p>Those questions shaped everything we do. Every teacher here is a woman with more than ten years of teaching, and before she teaches a single child we listen to her recitation and watch how she teaches. Parents can sit in on any lesson, and the class link always comes to your phone, not your child&rsquo;s.</p>'
    '<p>Since then, more than 500 children around the world have learned with us. Some started with the Arabic alphabet and now read the Quran by themselves. And it is never too late: mothers learn with us too, gently and at their own pace. Nothing makes me happier.</p>'
    '<p class="letter-ur" lang="ur-Latn">Mera khwab bas itna hai ke har bacha Quran ko sahi bhi parhe aur pyaar se bhi.</p>'
    '<p class="letter-en-small">(My only dream is that every child reads the Quran correctly, and with love.)</p>'
    '<p class="letter-sign"><span>With duas for your family,</span><b>Founder, Quran Online Tarteel</b></p></div>'
    '<div class="story-stats"><div><b>2010</b><span>Teaching since</span></div><div><b>500+</b><span>Children taught worldwide</span></div>'
    '<div><b>10+ yrs</b><span>Experience, every teacher</span></div><div><b>1 to 1</b><span>Every single class</span></div></div>'
    '</div></div></div></section><!--/STORY-->')

PROMISES = [
    ("Your child learns with a woman", "Every teacher is a woman. Her camera stays off in class, and if you want to be sure, she will turn it on once so you can see for yourself."),
    ("You are always welcome", "Sit in on any lesson, any day. You never need to ask first."),
    ("The link comes to you", "Class links and messages go to the parent&rsquo;s phone number, never straight to your child."),
    ("Children stay in view", "Young children keep their camera on, so the teacher can see that they are following and focused."),
    ("No recordings, ever", "Lessons are never recorded, by us or by anyone else. What happens in class stays private."),
    ("The same teacher every time", "Your child keeps the same teacher week after week, so trust and progress build together. Want a change? Just tell us."),
]
ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="#e2c47e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>'
PROMISE_SEC = (
    '<!--PROMISE--><section class="sec bg-white promise-sec" id="our-promise"><div class="container"><div class="section-head"><span class="eyebrow">Safety and Trust</span>'
    '<h2>Our Promise to Every Parent</h2><p>Simple rules we keep in every class, so you can relax while your child learns.</p></div>'
    '<div class="promise-grid">' + "".join(f'<div class="promise"><span class="pr-ic">{ICON}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in PROMISES) +
    '</div><div class="promise-cta"><a href="../free-trial/" class="btn btn-gold">See it for yourself: 2 free classes <svg><use href="#i-arrow"/></svg></a></div></div></section><!--/PROMISE-->')

HOME_NOTE = (
    '<!--FOUNDERNOTE--><div class="founder-note"><span class="fn-seal" aria-hidden="true"><small>SINCE</small>2010</span>'
    '<p><span class="fn-q">&ldquo;As a mother, I know what parents worry about before the first lesson. That is why every teacher here is a woman, '
    'every class is one to one, and you are always welcome to sit in.&rdquo;</span>'
    '<span class="fn-by">Our founder, teaching the Quran since 2010 &middot; <a href="about/#our-story" class="in-link">Read our story</a></span></p></div><!--/FOUNDERNOTE-->')

CSS = '''
/* about story + promises + founder note */
.story-grid{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:56px;align-items:start}
.story-media{position:sticky;top:110px}
.story-media .illus-wrap{max-width:440px;margin:0 auto}
.story-letter h2{margin:8px 0 22px}
.letter-card{position:relative;background:#fffdf8;border:1px solid #ead9b3;border-radius:24px;padding:34px 34px 28px;box-shadow:0 30px 60px -40px rgba(20,17,12,.45)}
.letter-card::before{content:"";position:absolute;inset:8px;border:1px dashed rgba(199,155,69,.35);border-radius:18px;pointer-events:none}
.q-mark{position:absolute;top:-28px;left:26px;font-family:var(--serif);font-size:92px;line-height:1;color:#c79b45}
.letter-card p{font-size:16.5px;line-height:1.8;color:var(--text);margin:0 0 14px}
.letter-card em{color:var(--ink)}
.letter-salam{font-family:var(--serif);font-size:20px!important;color:var(--ink)!important;font-weight:600}
.letter-ur{font-family:var(--serif);font-style:italic;font-size:19px!important;color:var(--gold-deep)!important;margin:20px 0 2px!important}
.letter-en-small{font-size:14px!important;color:var(--muted)!important}
.letter-sign{display:flex;flex-direction:column;gap:2px;margin:18px 0 0!important;padding-top:14px;border-top:1px solid #efe3c6}
.letter-sign span{font-style:italic;color:var(--muted);font-size:15px}.letter-sign b{font-family:var(--serif);font-size:18px;color:var(--ink)}
.story-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:22px}
.story-stats div{background:#14110c;border-radius:16px;padding:14px 10px;text-align:center;display:flex;flex-direction:column;gap:4px}
.story-stats b{font-family:var(--serif);font-size:24px;color:#e2c47e;line-height:1.1}.story-stats span{font-size:12.5px;color:#d9ccb0;line-height:1.35}
.promise-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.promise{display:flex;gap:16px;align-items:flex-start;background:#fffdf8;border:1px solid #efe3c6;border-radius:20px;padding:22px}
.pr-ic{flex:none;width:48px;height:48px;border-radius:14px;background:radial-gradient(circle at 50% 35%,#3a3124,#14110c);display:grid;place-items:center}
.pr-ic svg{width:26px;height:26px}
.promise h3{font-size:18px;margin:2px 0 6px}.promise p{margin:0;font-size:15px;line-height:1.65;color:var(--muted)}
.promise-cta{text-align:center;margin-top:30px}
.founder-note{display:flex;align-items:center;gap:22px;max-width:860px;margin:30px auto 0;background:#fffdf8;border:1px solid #ead9b3;border-radius:22px;padding:20px 26px;box-shadow:0 24px 50px -40px rgba(20,17,12,.45)}
.fn-seal{flex:none;width:76px;height:76px;border-radius:50%;background:radial-gradient(circle at 50% 35%,#3a3124,#14110c);border:2px solid #c79b45;color:#fbf7ee;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:var(--serif);font-size:20px;font-weight:700;line-height:1}
.fn-seal small{font-family:var(--sans);font-size:9px;letter-spacing:.18em;color:#e2c47e;margin-bottom:3px}
.founder-note p{margin:0;display:flex;flex-direction:column;gap:8px}
.fn-q{font-family:var(--serif);font-size:18px;line-height:1.55;color:var(--ink);font-style:italic}
.fn-by{font-size:14px;color:var(--muted)}
@media(max-width:980px){.story-grid{grid-template-columns:1fr;gap:0}.story-media{display:none}.promise-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.letter-card{padding:28px 20px 22px}.letter-card p{font-size:15.5px}.story-stats{grid-template-columns:repeat(2,1fr)}.promise-grid{grid-template-columns:1fr}.promise{padding:18px}
.founder-note{flex-direction:column;text-align:center;padding:20px 18px;gap:14px}.fn-q{font-size:16.5px}}
'''


def main():
    p = os.path.join(ROOT, "about", "index.html")
    s = open(p).read()
    for tag in ("STORY", "PROMISE"):
        s = re.sub(rf"<!--{tag}-->.*?<!--/{tag}-->", "", s, flags=re.S)
    a = s.index('<section class="sec', s.index('<section class="page-hero'))
    s = s[:a] + STORY + s[a:]
    # alternate backgrounds after the story: mission -> white, why -> cream
    s = s.replace('<section class="sec bg-cream"><div class="container split">', '<section class="sec bg-white"><div class="container split">', 1)
    i = s.index("What Makes Us Different")
    j = s.rfind('<section class="sec bg-white"', 0, i)
    s = s[:j] + '<section class="sec bg-cream"' + s[j + len('<section class="sec bg-white"'):]
    k = s.index('<section class="sec bg-cream-2"', i)
    s = s[:k] + PROMISE_SEC + s[k:]
    s = s.replace('<section class="sec bg-cream-2"', '<section class="sec bg-cream"', 1) if False else s
    s = s.replace('Book 2 free classes and see how we teach.', 'Book 2 free classes. Sit in, listen, and decide for yourself.')
    # Organization schema: founding year
    s = re.sub(r'("@type": "EducationalOrganization",)(?! "foundingDate")', r'\1 "foundingDate": "2010",', s, count=1)
    open(p, "w").write(s)

    h = os.path.join(ROOT, "index.html")
    s = open(h).read()
    s = re.sub(r"<!--FOUNDERNOTE-->.*?<!--/FOUNDERNOTE-->", "", s, flags=re.S)
    anchor = '<p class="who-note">'
    s = s.replace(anchor, HOME_NOTE + anchor, 1)
    open(h, "w").write(s)

    c = os.path.join(ROOT, "assets", "site.css")
    css = open(c).read()
    css = re.sub(r"\n/\* about story \+ promises \+ founder note \*/.*?(?=\n/\*|\Z)", "", css, flags=re.S)
    open(c, "w").write(css.rstrip("\n") + "\n" + CSS)
    print("about story + promise + home note")


if __name__ == "__main__":
    main()
