#!/usr/bin/env python3
"""Render a 1200x630 featured image (plus a 640px card copy) for every blog post: brand dark/gold
Islamic geometric artwork, the Arabic keyword in Amiri and the post title. No people, self-hosted WebP.
Usage: python3 scripts/blog_images.py [slug ...]   (no args = only posts missing an image)"""
import io, json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "blog", "img")
FONTS = "file://" + os.path.join(ROOT, "assets", "fonts")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from build_blog import load_posts, CAT, LEGACY  # noqa

TINT = {  # category accent (second colour in the artwork)
    "learn-quran": "#c79b45", "tajweed": "#d8a657", "kids": "#e0a96d", "women": "#c98f7a", "hifz": "#b9a25a",
    "salah": "#7fa38a", "duas": "#8fa9b8", "knowledge": "#c79b45", "ramadan": "#9d8fc4", "guides": "#c7b37f"}
MOTIF = {
    "learn-quran": "book", "tajweed": "wave", "kids": "star", "women": "lamp", "hifz": "book", "salah": "arch",
    "duas": "hands", "knowledge": "book", "ramadan": "moon", "guides": "compass"}

SVGS = {
    "book": '<path d="M150 300c-50-40-110-48-150-34V70c40-14 100-6 150 34z M170 300c50-40 110-48 150-34V70c-40-14-100-6-150 34z" fill="none" stroke="ACC" stroke-width="6"/><path d="M160 110v196" stroke="ACC" stroke-width="4"/>',
    "wave": '<path d="M0 190c40-60 80-60 120 0s80 60 120 0 80-60 120 0" fill="none" stroke="ACC" stroke-width="7" stroke-linecap="round"/><path d="M0 240c40-40 80-40 120 0s80 40 120 0 80-40 120 0" fill="none" stroke="ACC" stroke-opacity=".5" stroke-width="5" stroke-linecap="round"/>',
    "star": '<path d="M180 30l34 82 88 8-67 58 20 86-75-45-75 45 20-86-67-58 88-8z" fill="none" stroke="ACC" stroke-width="7" stroke-linejoin="round"/><circle cx="180" cy="160" r="30" fill="ACC" fill-opacity=".25"/>',
    "lamp": '<path d="M180 20v40M140 60h80l-10 40c40 20 60 60 60 100 0 50-40 90-90 90s-90-40-90-90c0-40 20-80 60-100z" fill="none" stroke="ACC" stroke-width="7" stroke-linejoin="round"/><circle cx="180" cy="200" r="28" fill="ACC" fill-opacity=".35"/>',
    "arch": '<path d="M60 330V170c0-70 55-130 120-150 65 20 120 80 120 150v160" fill="none" stroke="ACC" stroke-width="8"/><path d="M110 330V185c0-45 30-85 70-100 40 15 70 55 70 100v145" fill="none" stroke="ACC" stroke-opacity=".5" stroke-width="5"/>',
    "hands": '<path d="M100 320c-10-60-20-120 0-180 10-30 40-30 45 0l10 90M260 320c10-60 20-120 0-180-10-30-40-30-45 0l-10 90" fill="none" stroke="ACC" stroke-width="7" stroke-linecap="round"/><circle cx="180" cy="80" r="22" fill="ACC" fill-opacity=".35"/>',
    "moon": '<path d="M230 40a130 130 0 1 0 60 230A110 110 0 1 1 230 40z" fill="ACC" fill-opacity=".85"/><path d="M300 90l8 20 20 8-20 8-8 20-8-20-20-8 20-8z" fill="ACC"/>',
    "compass": '<circle cx="180" cy="170" r="130" fill="none" stroke="ACC" stroke-width="6"/><path d="M180 60l30 110-30 110-30-110z" fill="ACC" fill-opacity=".6"/><circle cx="180" cy="170" r="12" fill="ACC"/>',
}

TPL = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(FONTS/fraunces-latin-opsz-normal.woff2)}
@font-face{font-family:M;font-weight:800;src:url(FONTS/manrope-latin-800-normal.woff2)}
@font-face{font-family:M;font-weight:600;src:url(FONTS/manrope-latin-600-normal.woff2)}
@font-face{font-family:A;font-weight:700;src:url(FONTS/amiri-arabic-700-normal.woff2)}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;background:#14110c;position:relative;font-family:M}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 78% 30%,rgba(199,155,69,.30),transparent 55%),radial-gradient(circle at 10% 100%,ACCA,transparent 50%),linear-gradient(135deg,#1d1913,#14110c 60%)}
.pat{position:absolute;inset:0;opacity:.16;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90' viewBox='0 0 80 80'%3E%3Cg fill='none' stroke='%23e2c47e' stroke-width='1.1'%3E%3Cpath d='M40 4l10.6 25.4L76 40 50.6 50.6 40 76 29.4 50.6 4 40l25.4-10.6z'/%3E%3Crect x='22' y='22' width='36' height='36' transform='rotate(45 40 40)'/%3E%3Ccircle cx='40' cy='40' r='9'/%3E%3C/g%3E%3C/svg%3E")}
.frame{position:absolute;inset:22px;border:1.5px solid rgba(226,196,126,.35);border-radius:26px}
.frame:after{content:"";position:absolute;inset:8px;border:1px solid rgba(226,196,126,.15);border-radius:20px}
.l{position:absolute;left:78px;top:72px;width:640px;height:486px;display:flex;flex-direction:column;justify-content:center}
.chip{align-self:flex-start;font-weight:800;font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:#e2c47e;border:1.5px solid rgba(226,196,126,.5);padding:9px 18px;border-radius:999px;background:rgba(226,196,126,.08)}
h1{font-family:F;font-weight:600;color:#fff;font-size:SIZEpx;line-height:1.12;margin:26px 0 24px;letter-spacing:-.01em}
.brand{display:flex;align-items:center;gap:14px;color:#cfc4ac;font-weight:600;font-size:19px}
.brand i{display:block;width:38px;height:2px;background:#c79b45}
.r{position:absolute;right:70px;top:60px;width:380px;height:510px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.medal{width:360px;height:360px;position:relative;display:grid;place-items:center}
.medal svg.o{position:absolute;inset:0}
.medal .ic{position:absolute;inset:92px;opacity:.95}
.ar{font-family:A;font-weight:700;color:#e2c47e;font-size:ARSIZEpx;direction:rtl;margin-top:6px;text-shadow:0 6px 30px rgba(199,155,69,.35);white-space:nowrap}
</style></head><body><div class="bg"></div><div class="pat"></div><div class="frame"></div>
<div class="l"><span class="chip">CHIP</span><h1>TITLE</h1><div class="brand"><i></i>Quran Online Tarteel</div></div>
<div class="r"><div class="medal"><svg class="o" viewBox="0 0 360 360"><g fill="none" stroke="#c79b45"><rect x="62" y="62" width="236" height="236" rx="6" stroke-width="3"/><rect x="62" y="62" width="236" height="236" rx="6" stroke-width="3" transform="rotate(45 180 180)"/><circle cx="180" cy="180" r="112" stroke-opacity=".45" stroke-width="2"/><circle cx="180" cy="180" r="150" stroke-opacity=".22" stroke-width="1.5" stroke-dasharray="4 8"/></g></svg>
<svg class="ic" viewBox="0 0 360 340">ICON</svg></div><div class="ar">ARABIC</div></div>
</body></html>"""


def hexa(c, a):
    c = c.lstrip("#")
    return f"rgba({int(c[0:2],16)},{int(c[2:4],16)},{int(c[4:6],16)},{a})"


def render(page, slug, title, cat, ar):
    acc = TINT.get(cat, "#c79b45")
    n = len(title)
    size = 62 if n <= 38 else 56 if n <= 52 else 50 if n <= 64 else 44
    arsize = 64 if len(ar) <= 10 else 52 if len(ar) <= 16 else 42
    h = (TPL.replace("FONTS", FONTS).replace("ACCA", hexa(acc, .22)).replace("ARSIZE", str(arsize)).replace("SIZE", str(size))
         .replace("CHIP", CAT.get(cat, "Guide")).replace("TITLE", title).replace("ARABIC", ar)
         .replace("ICON", SVGS[MOTIF.get(cat, "book")].replace("ACC", acc)))
    tmp = os.path.join(ROOT, "scripts", "_img_tmp.html")
    open(tmp, "w", encoding="utf-8").write(h)
    page.goto("file://" + tmp)
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(150)
    os.remove(tmp)
    png = page.screenshot(type="png")
    im = Image.open(io.BytesIO(png)).convert("RGB")
    im.save(os.path.join(OUT, slug + ".webp"), "WEBP", quality=84, method=6)
    im.resize((640, 336), Image.LANCZOS).save(os.path.join(OUT, slug + "-640.webp"), "WEBP", quality=82, method=6)


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [(p["slug"], p.get("imgtitle", p["h1"]), p["cat"], p["ar"]) for p in load_posts()]
    jobs += [(l["img"], l["title"], l["cat"], {"tajweed": "التجويد", "learn-quran": "القاعدة النورانية", "salah": "الصلاة"}[l["cat"]]) for l in LEGACY]
    jobs += [("blog-cover", "Guides for learning the Quran at home", "learn-quran", "ترتيل")]
    want = set(sys.argv[1:])
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page(viewport={"width": 1200, "height": 630})
        for slug, title, cat, ar in jobs:
            if want and slug not in want and "all" not in want:
                continue
            if not want and os.path.exists(os.path.join(OUT, slug + ".webp")):
                continue
            render(page, slug, title, cat, ar)
            print("img", slug)
        b.close()


if __name__ == "__main__":
    main()
