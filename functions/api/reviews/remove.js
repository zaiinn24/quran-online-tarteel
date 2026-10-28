// GET shows a confirm page (so email link scanners can't remove reviews by accident); POST removes.
const page = (title, msg, form = "") => new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${title}</title>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#14110c;color:#efe3c4;display:grid;place-items:center;min-height:100vh;padding:20px}
.c{max-width:460px;background:#1d1913;border:1px solid #c79b45;border-radius:18px;padding:28px;text-align:center}h1{color:#e2c47e;font-size:22px}
button{background:#c79b45;color:#14110c;border:0;border-radius:99px;padding:12px 24px;font-weight:800;font-size:15px;cursor:pointer}</style></head>
<body><div class="c"><h1>${title}</h1><p>${msg}</p>${form}</div></body></html>`, { headers: { "content-type": "text/html; charset=utf-8", "x-robots-tag": "noindex" } });

async function find(env, id, t) {
  if (!env.DB || !/^[0-9a-f-]{36}$/.test(id) || !/^[0-9a-f]{32}$/.test(t)) return null;
  return env.DB.prepare("SELECT id,name,status FROM reviews WHERE id=? AND token=?").bind(id, t).first();
}

export async function onRequestGet({ env, request }) {
  const u = new URL(request.url), id = u.searchParams.get("id") || "", t = u.searchParams.get("t") || "";
  const r = await find(env, id, t);
  if (!r) return page("Link not valid", "This remove link is not valid.");
  if (r.status !== "live") return page("Already removed", "This review is no longer on the website.");
  return page("Remove this review?", `Review by <b>${String(r.name).replace(/[<>&"]/g, "")}</b> will be taken off the website.`,
    `<form method="post"><input type="hidden" name="id" value="${id}"><input type="hidden" name="t" value="${t}"><button type="submit">Yes, remove it</button></form>`);
}

export async function onRequestPost({ env, request }) {
  const f = await request.formData(), id = String(f.get("id") || ""), t = String(f.get("t") || "");
  const r = await find(env, id, t);
  if (!r) return page("Link not valid", "This remove link is not valid.");
  await env.DB.prepare("UPDATE reviews SET status='removed' WHERE id=?").bind(id).run();
  return page("Review removed", "Done. The review has been removed from the website.");
}
