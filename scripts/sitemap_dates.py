#!/usr/bin/env python3
"""Set each sitemap <lastmod> to the date that page (or PDF) last changed in git. Run after committing page changes."""
import re, subprocess, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "sitemap.xml")
s = open(p).read()


def lm(m):
    rel = m.group(1).replace("https://quranonlinetarteel.net/", "")
    f = rel if rel.endswith(".pdf") else rel + "index.html"
    d = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip()
    return re.sub(r"<lastmod>[^<]*", "<lastmod>" + d, m.group(0)) if d else m.group(0)


open(p, "w").write(re.sub(r"<url><loc>([^<]*)</loc><lastmod>[^<]*</lastmod>.*?</url>", lm, s))
print("sitemap dates updated")
