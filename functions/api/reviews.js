// Quran Online Tarteel - reviews API (Cloudflare Pages Function + D1). Free tier.
// GET  /api/reviews?limit=6   -> live reviews (plain text only)
// POST /api/reviews           -> new review (Turnstile + honeypot + rate limit), auto-published, email with a remove link
const LEAD_EMAIL = "rehanabashir6543@gmail.com";
const CC_EMAIL = "zainulabideen4356@gmail.com";
const COURSES = ["Noorani Qaida", "Quran Reading (Nazra)", "Tajweed", "Hifz", "Translation and Tafseer", "Islamic Studies",
  "Juz Amma Memorisation", "Salah (Prayer) Lessons", "Daily Duas Course", "40 Hadith for Kids", "Classes for New Muslims"];
const WHO = ["My child", "Myself"];

const json = (data, status = 200, extra = {}) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", ...extra } });

// strip HTML, links and control characters: reviews are shown as plain text only (no XSS, no spam backlinks)
const clean = (s, n) => String(s ?? "")
  .replace(/<[^>]*>/g, " ")
  .replace(/(https?:\/\/|www\.)\S+/gi, "")
  .replace(/\b[\w.-]+\.(com|net|org|pk|uk|io|co|info|xyz|ru|top|site|online|shop)\b\S*/gi, "")
  .replace(/[\u0000-\u001f\u007f]/g, " ")
  .replace(/\s+/g, " ").trim().slice(0, n);

async function ensure(db) {
  await db.prepare(`CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, country TEXT, course TEXT, who TEXT, stars INTEGER NOT NULL,
    body TEXT NOT NULL, created INTEGER NOT NULL, token TEXT NOT NULL, status TEXT NOT NULL, iph TEXT)`).run();
}

async function sha(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
}

export async function onRequestGet({ env, request }) {
  const sitekey = env.TURNSTILE_SITEKEY || "";
  if (!env.DB) return json({ reviews: [], count: 0, avg: 0, sitekey: "" });
  await ensure(env.DB);
  const url = new URL(request.url);
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "6", 10) || 6, 1), 50);
  const rows = await env.DB.prepare(
    "SELECT name,country,course,who,stars,body,created FROM reviews WHERE status='live' ORDER BY created DESC LIMIT ?").bind(limit).all();
  const agg = await env.DB.prepare("SELECT COUNT(*) AS c, AVG(stars) AS a FROM reviews WHERE status='live'").first();
  return json({ reviews: rows.results || [], count: agg?.c || 0, avg: agg?.a ? Math.round(agg.a * 10) / 10 : 0, sitekey: env.TURNSTILE_SECRET ? sitekey : "" },
    200, { "cache-control": "public, max-age=60" });
}

export async function onRequestPost({ env, request }) {
  // no spam check configured = no reviews accepted (never open the form to bots)
  if (!env.DB || !env.TURNSTILE_SECRET) return json({ ok: false, error: "Reviews are opening very soon. Please try again later." }, 503);
  const ct = request.headers.get("content-type") || "";
  if (!ct.includes("application/json") || Number(request.headers.get("content-length") || 0) > 8000) return json({ ok: false, error: "Bad request." }, 400);
  let d;
  try { d = await request.json(); } catch { return json({ ok: false, error: "Bad request." }, 400); }
  if (d.website) return json({ ok: true }); // honeypot: bots fill hidden field, pretend success

  const name = clean(d.name, 40), body = clean(d.review, 600), country = clean(d.country, 40);
  const course = COURSES.includes(d.course) ? d.course : "";
  const who = WHO.includes(d.who) ? d.who : "";
  const stars = parseInt(d.stars, 10);
  if (name.length < 2 || body.length < 20 || !(stars >= 1 && stars <= 5))
    return json({ ok: false, error: "Please add your name, a star rating and at least a few words." }, 400);

  const ip = request.headers.get("CF-Connecting-IP") || "";
  {
    const form = new FormData();
    form.append("secret", env.TURNSTILE_SECRET);
    form.append("response", String(d.turnstile || ""));
    form.append("remoteip", ip);
    const v = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form }).then(r => r.json()).catch(() => ({}));
    if (!v.success) return json({ ok: false, error: "Please complete the security check and try again." }, 400);
  }

  await ensure(env.DB);
  const iph = await sha(ip + "|qot-reviews");
  const recent = await env.DB.prepare("SELECT COUNT(*) AS c FROM reviews WHERE iph=? AND created>?").bind(iph, Date.now() - 86400000).first();
  if ((recent?.c || 0) >= 2) return json({ ok: false, error: "Thank you! You have already left a review today." }, 429);

  const id = crypto.randomUUID(), token = crypto.randomUUID().replace(/-/g, "");
  await env.DB.prepare("INSERT INTO reviews (id,name,country,course,who,stars,body,created,token,status,iph) VALUES (?,?,?,?,?,?,?,?,?,?,?)")
    .bind(id, name, country, course, who, stars, body, Date.now(), token, "live", iph).run();

  const origin = new URL(request.url).origin;
  const removeLink = `${origin}/api/reviews/remove?id=${id}&t=${token}`;
  try {
    await fetch(`https://formsubmit.co/ajax/${LEAD_EMAIL}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json", "Origin": origin, "Referer": origin + "/contact/" },
      body: JSON.stringify({
        _subject: `New ${stars}-star review from ${name} - Quran Online Tarteel`, _template: "table", _captcha: "false", _cc: CC_EMAIL,
        name, stars: "★".repeat(stars), country, course, who, review: body,
        status: "Published on the website automatically",
        remove_this_review: removeLink,
      }),
    });
  } catch (e) { /* email failure must not block the review */ }
  return json({ ok: true });
}
