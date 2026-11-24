#!/usr/bin/env python3
"""Sitewide 'Good to know before you book' strip (teaching languages, advance fees, refund policy)
above the footer of every page, plus a one-line note above every booking form's submit button.
Idempotent: re-run after any page generator (build_blog.py, build_fees.py, build_duas.py ...)."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IC_LANG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h9M8.5 3v2M6 5c.8 3.5 3 6 6 7.5M11 5c-.8 3.6-3.4 6.6-7 8"/><path d="M13 21l4-9 4 9M14.4 18h5.2"/></svg>'
IC_PAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/></svg>'
IC_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>'


def strip(pre):
    return ('<!--POLICY--><aside class="policy-strip" aria-label="Good to know before you book"><div class="container">'
            '<p class="ps-head">Good to know before you book</p><div class="ps-grid">'
            f'<div class="ps-item"><span class="ps-ic">{IC_LANG}</span><div><strong>Teachers in English, Urdu and Arabic</strong>'
            '<p>Your female teacher explains every lesson in the language you understand best. The Quran itself is always read in Arabic.</p></div></div>'
            f'<div class="ps-item"><span class="ps-ic">{IC_PAY}</span><div><strong>Monthly fees, paid in advance</strong>'
            '<p>Start with 2 free classes. To continue, the fee is paid at the start of every month. If you skip the free trial, you pay before the first class.</p></div></div>'
            f'<div class="ps-item"><span class="ps-ic">{IC_SHIELD}</span><div><strong>Fair refund policy</strong>'
            '<p>Stop within the first 2 classes of a paid month and get 100% back. Stop by the middle of the month and get 50% back. '
            f'<a href="{pre}fees/#payment">How payment works</a></p></div></div>'
            '</div></div></aside><!--/POLICY-->\n')


NOTE = ('<!--PNOTE--><p class="form-policy">Teachers explain in <b>English, Urdu or Arabic</b>. '
        'After your 2 free classes, fees are paid <b>monthly in advance</b>.</p><!--/PNOTE-->')


def prefix(f):
    rel = os.path.relpath(f, ROOT)
    depth = rel.count(os.sep)
    return "../" * depth


def main():
    n = 0
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if "/.git/" in f or "/scripts/" in f:
            continue
        s = o = open(f, encoding="utf-8").read()
        if '<footer class="qot-foot">' not in s:
            continue
        s = re.sub(r"<!--POLICY-->.*?<!--/POLICY-->\n?", "", s, flags=re.S)
        s = s.replace('<footer class="qot-foot">', strip(prefix(f)) + '<footer class="qot-foot">', 1)
        s = re.sub(r"<!--PNOTE-->.*?<!--/PNOTE-->", "", s, flags=re.S)
        s = re.sub(r'(<button type="submit" class="btn btn-gold)', NOTE + r"\1", s)
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
            n += 1
    print("policy strip on", n, "pages")


if __name__ == "__main__":
    main()
