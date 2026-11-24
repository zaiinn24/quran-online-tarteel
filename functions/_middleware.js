// Quran Online Tarteel - scheduled blog publishing (Cloudflare Pages middleware).
// Every blog post is committed in advance with a publish date. Until that date (Pakistan time, UTC+5):
//   - /blog/<slug>/ answers 404
//   - cards and links pointing to it are removed from blog pages
//   - it is left out of /sitemap.xml and /llms.txt
// SCHEDULE is written by scripts/build_blog.py. Do not edit by hand.
const SCHEDULE = {
"how-to-learn-quran-online": "2026-11-24"
};

const today = () => new Date(Date.now() + 5 * 3600 * 1000).toISOString().slice(0, 10);

async function notFound(env, url) {
  let r = await env.ASSETS.fetch(new Request(new URL("/404.html", url)));
  if (r.status >= 300 && r.status < 400 && r.headers.get("location")) {
    r = await env.ASSETS.fetch(new Request(new URL(r.headers.get("location"), url)));
  }
  return new Response(r.body, { status: 404, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
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
    const out = new HTMLRewriter().on("[data-pub]", new Hide(t)).transform(res);
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

  return next();
}
