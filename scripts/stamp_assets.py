#!/usr/bin/env python3
"""Add ?v=<content hash> to site.css / site.js / fees.js links on every page so browsers never use a stale copy."""
import hashlib, glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = {n: hashlib.md5(open(os.path.join(ROOT, "assets", n), "rb").read()).hexdigest()[:8] for n in ("site.css", "site.js", "fees.js")}
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = o = open(f).read()
    for n, v in h.items():
        s = re.sub(r'(assets/' + re.escape(n) + r')(\?v=[0-9a-f]+)?"', r'\1?v=' + v + '"', s)
    if s != o:
        open(f, "w").write(s)
print(h)
