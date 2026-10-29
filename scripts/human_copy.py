#!/usr/bin/env python3
"""Step 9: small human touches on every lead form (warm founder line under the button, warmer thank-you). Idempotent."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = '<p class="form-note"><svg><use href="#i-lock"/></svg>Your details stay private. We never share them.</p>'
HUMAN = '<!--HUMAN--><p class="form-human">&ldquo;Every child who joins us is looked after like one of our own.&rdquo; <span>Our founder, a mother, teaching since 2010</span></p><!--/HUMAN-->'
OLD_OK = '<p>Your request is in. Our team will message you on WhatsApp within 24 hours.</p>'
NEW_OK = '<p>Your request is in. We will message you on WhatsApp within 24 hours, in sha Allah. We are so happy you are starting this journey with us.</p>'
n = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = o = open(f).read()
    s = re.sub(r"<!--HUMAN-->.*?<!--/HUMAN-->", "", s, flags=re.S)
    s = s.replace(NOTE, NOTE + HUMAN).replace(OLD_OK, NEW_OK)
    if s != o:
        open(f, "w").write(s); n += 1
c = os.path.join(ROOT, "assets", "site.css"); css = open(c).read()
if ".form-human" not in css:
    css += "\n.form-human{margin:12px 0 0;text-align:center;font-family:var(--serif);font-style:italic;font-size:15px;line-height:1.5;color:var(--ink)}.form-human span{display:block;font-family:var(--sans);font-style:normal;font-size:12px;color:var(--muted);margin-top:2px}\n"
    open(c, "w").write(css)
print(n, "files")
