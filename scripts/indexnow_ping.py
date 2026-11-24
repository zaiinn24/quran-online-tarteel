#!/usr/bin/env python3
"""Send URLs to IndexNow (Bing, Yandex, Seznam, Naver share submissions).

Usage:
  python3 scripts/indexnow_ping.py today   # blog posts that go live today (PKT) + /blog/ + home
  python3 scripts/indexnow_ping.py all     # every URL in the live sitemap (future posts are already filtered out)
  python3 scripts/indexnow_ping.py URL...  # specific URLs
"""
import json, os, re, sys, urllib.request, datetime

HOST = "quranonlinetarteel.net"
SITE = f"https://{HOST}"
KEY = "4742f7238a9e600c2414aa796655ae44"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def today_pkt():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).date().isoformat()


def todays_urls():
    plan = json.load(open(os.path.join(ROOT, "scripts", "blog_posts", "_plan.json")))
    day = today_pkt()
    posts = [f"{SITE}/blog/{slug}/" for slug, d in plan.items() if d == day]
    if not posts:
        return []
    return posts + [f"{SITE}/blog/", f"{SITE}/"]


def sitemap_urls():
    req = urllib.request.Request(f"{SITE}/sitemap.xml", headers={"User-Agent": "indexnow-ping"})
    xml = urllib.request.urlopen(req, timeout=30).read().decode()
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def submit(urls):
    if not urls:
        print("Nothing to submit today.")
        return
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"{SITE}/{KEY}.txt",
        "urlList": urls[:10000],
    }).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body,
        headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print("IndexNow", r.status, "for", len(urls), "URLs")
    except urllib.error.HTTPError as e:
        print("IndexNow error", e.code, e.read().decode()[:300])
        sys.exit(1)
    for u in urls:
        print(" ", u)


if __name__ == "__main__":
    arg = sys.argv[1:] or ["today"]
    if arg == ["today"]:
        submit(todays_urls())
    elif arg == ["all"]:
        submit(sitemap_urls())
    else:
        submit(arg)
