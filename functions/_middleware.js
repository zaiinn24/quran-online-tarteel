// Quran Online Tarteel - scheduled blog publishing (Cloudflare Pages middleware).
// Also filters the 'Latest from the blog' section on the homepage, service and country pages (see _routes.json).
// Every blog post is committed in advance with a publish date. Until that date (Pakistan time, UTC+5):
//   - /blog/<slug>/ answers 404
//   - cards and links pointing to it are removed from blog pages
//   - it is left out of /sitemap.xml and /llms.txt
// SCHEDULE is written by scripts/build_blog.py. Do not edit by hand.
const SCHEDULE = {
"how-to-learn-quran-online": "2026-11-24",
"how-to-pray-salah-step-by-step": "2026-11-27",
"what-is-tajweed": "2026-11-30",
"best-online-quran-classes": "2026-12-03",
"what-is-dua": "2026-12-06",
"arabic-alphabet": "2026-12-09",
"what-is-dhikr": "2026-12-12",
"how-to-teach-quran-to-kids-at-home": "2026-12-15",
"sunnah-prayers": "2026-12-18",
"how-to-memorize-quran": "2026-12-21",
"dua-for-success-protection-knowledge": "2026-12-24",
"how-to-choose-a-female-quran-teacher": "2026-12-27",
"benefits-of-reciting-quran": "2026-12-30",
"how-to-perform-wudu": "2027-01-02",
"learn-quran-as-an-adult-woman": "2027-01-05",
"islamic-stories-for-kids": "2027-01-08",
"best-english-translation-of-quran": "2027-01-11",
"noon-sakinah-and-tanween-rules": "2027-01-14",
"how-long-does-it-take-to-learn-quran": "2027-01-17",
"what-is-hifz": "2027-01-20",
"learn-quran-in-urdu-english-arabic": "2027-01-23",
"ramadan-quran-plan": "2027-01-26",
"makharij-al-huroof": "2027-01-29",
"prepare-kids-for-ramadan": "2027-02-01",
"tafseer-for-beginners": "2027-02-04",
"surah-al-mulk-benefits": "2027-02-07",
"short-surahs-for-kids": "2027-02-10",
"qalqalah-in-tajweed": "2027-02-13",
"online-vs-local-quran-classes": "2027-02-16",
"madd-in-tajweed": "2027-02-19",
"laylatul-qadr-last-ten-nights": "2027-02-22",
"colour-coded-tajweed-quran": "2027-02-25",
"surah-al-kahf-on-friday": "2027-02-28"
};

const today = () => new Date(Date.now() + 5 * 3600 * 1000).toISOString().slice(0, 10);

async function notFound(env, url) {
  let r = await env.ASSETS.fetch(new Request(new URL("/404.html", url)));
  if (r.status >= 300 && r.status < 400 && r.headers.get("location")) {
    r = await env.ASSETS.fetch(new Request(new URL(r.headers.get("location"), url)));
  }
  return new Response(r.body, { status: 404, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
}

// 'Latest from the blog' cards: drop posts that are not live yet and keep only the first 3
class Latest {
  constructor(t) { this.t = t; this.n = 0; }
  element(el) {
    const d = el.getAttribute("data-pub");
    if ((d && d > this.t) || this.n >= 3) el.remove();
    else this.n++;
  }
}

class Hide {
  constructor(t) { this.t = t; }
  element(el) {
    const d = el.getAttribute("data-pub");
    if (d && d > this.t) {
      if (el.getAttribute("data-pub-mode") === "unwrap") el.removeAndKeepContent();
      else el.remove();
    }
  }
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const path = url.pathname;
  const t = today();

  if (path.startsWith("/blog")) {
    const m = path.match(/^\/blog\/([a-z0-9-]+)\/?(index\.html)?$/);
    if (m && SCHEDULE[m[1]] && SCHEDULE[m[1]] > t) return notFound(env, url);
    const res = await next();
    const ct = res.headers.get("content-type") || "";
    if (!ct.includes("text/html")) return res;
    const out = new HTMLRewriter().on("[data-latest]", new Latest(t)).on("[data-pub]:not([data-latest])", new Hide(t)).transform(res);
    const h = new Headers(out.headers);
    h.set("cache-control", "public, max-age=0, must-revalidate");
    return new Response(out.body, { status: out.status, headers: h });
  }

  if (path === "/sitemap.xml" || path === "/llms.txt") {
    const res = await next();
    if (res.status !== 200) return res;
    let body = await res.text();
    const future = Object.keys(SCHEDULE).filter(s => SCHEDULE[s] > t);
    if (path === "/sitemap.xml") {
      body = body.replace(/\s*<url><loc>[^<]*\/blog\/([a-z0-9-]+)\/<\/loc>.*?<\/url>/g, (all, s) => (future.includes(s) ? "" : all));
      const live = Object.values(SCHEDULE).filter(d => d <= t).sort().pop();
      if (live) body = body.replace(/(<loc>https:\/\/quranonlinetarteel\.net\/blog\/<\/loc><lastmod>)[^<]*/, "$1" + live);
    } else {
      body = body.split("\n").filter(l => !future.some(s => l.includes("/blog/" + s + "/"))).join("\n");
    }
    const h = new Headers(res.headers);
    h.set("cache-control", "public, max-age=0, must-revalidate");
    h.delete("content-length");
    return new Response(body, { status: 200, headers: h });
  }

  // homepage, service and country pages: same filtering for their 'Latest from the blog' section and blog links
  const res = await next();
  const ct = res.headers.get("content-type") || "";
  if (res.status !== 200 || !ct.includes("text/html")) return res;
  const out = new HTMLRewriter().on("[data-latest]", new Latest(t)).on("a[data-pub]", new Hide(t)).transform(res);
  const h = new Headers(out.headers);
  h.set("cache-control", "public, max-age=0, must-revalidate");
  return new Response(out.body, { status: out.status, headers: h });
}
